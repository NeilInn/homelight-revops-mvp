import pandas as pd
import numpy as np
from datetime import datetime, date
import streamlit as st

st.set_page_config(page_title="Referral-to-Revenue Scorecard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_referrals.csv", parse_dates=[
        "referral_date","close_date","invoice_sent_date","last_touch"
    ])
    # Ensure date columns are proper datetime objects
    date_cols = ["referral_date","close_date","invoice_sent_date","last_touch"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today().normalize()
    df["days_to_close"] = (df["close_date"] - df["referral_date"]).dt.days
    df["amount_invoiced"] = df["amount_invoiced"].fillna(0)
    df["amount_collected"] = df["amount_collected"].fillna(0)
    df["leakage_delta"] = (df["commission_due"].fillna(0)) - df["amount_collected"]
    df["days_outstanding"] = np.where(df["invoice_sent_date"].notna(),
                                      (today - df["invoice_sent_date"]).dt.days, np.nan)
    # Rule-based risk (explainable)
    def risk(row):
        # If fully collected, no risk
        due = row.get("commission_due") or 0
        collected = row.get("amount_collected", 0)
        if collected >= due:
            return 0
        
        risk = 0
        if (row.get("stage") in ["Closed Won"]) and (collected < due):
            risk += 2
        if pd.notna(row.get("days_outstanding")) and row["days_outstanding"] > 30:
            risk += 2
        if (row.get("leakage_delta") or 0) > 0:
            risk += 1
        if pd.notna(row.get("last_touch")) and (pd.Timestamp.today().normalize() - row["last_touch"]).days > 14:
            risk += 1
        if isinstance(row.get("special_terms"), str) and "legacy" in row["special_terms"].lower():
            risk += 1
        return risk
    df["risk_score"] = df.apply(risk, axis=1)
    
    # Repeat offender detection: add +1 risk if agent has 2+ at-risk deals
    agent_risk_counts = df[df["risk_score"] >= 2].groupby("agent_name").size()
    repeat_offenders = agent_risk_counts[agent_risk_counts >= 2].index
    df.loc[df["agent_name"].isin(repeat_offenders), "risk_score"] += 1
    
    df["collection_status"] = np.where(df["amount_collected"] >= df["commission_due"], "Collected",
                                np.where(df["invoice_sent_date"].notna(), "Invoiced", "Not Invoiced"))
    return df

df = compute_features(load_data())

st.title("Referral‑to‑Revenue Scorecard")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Referrals", int(len(df)))
with col2:
    closed = (df["stage"] == "Closed Won").sum()
    st.metric("Closed Won", int(closed))
with col3:
    conv = (closed / max(len(df),1)) * 100
    st.metric("Conversion %", f"{conv:.1f}%")
with col4:
    to_collect = (df["commission_due"].fillna(0) - df["amount_collected"].fillna(0)).clip(lower=0).sum()
    st.metric("$ Outstanding", f"${to_collect:,.0f}")
with col5:
    aging = df["days_outstanding"].dropna()
    avg_aging = aging.mean() if len(aging)>0 else 0
    st.metric("Avg Aging (days)", f"{avg_aging:.0f}")

st.subheader("Agent Risk Summary")

# Build agent-level aggregation
agent_summary = df.groupby("agent_name").agg({
    "referral_id": "count",
    "risk_score": lambda x: (x >= 2).sum(),
    "commission_due": lambda x: x.fillna(0).sum(),
    "amount_collected": lambda x: x.fillna(0).sum()
}).reset_index()

agent_summary.columns = ["agent_name", "total_deals", "at_risk_deals", "total_due", "total_collected"]
agent_summary["outstanding"] = (agent_summary["total_due"] - agent_summary["total_collected"]).clip(lower=0)
agent_summary["collection_rate"] = np.where(
    agent_summary["total_due"] > 0,
    (agent_summary["total_collected"] / agent_summary["total_due"] * 100),
    100
)

# Priority flags
def get_priority(row):
    if row["at_risk_deals"] >= 2 or row["outstanding"] > 20000:
        return "🔴 High Priority"
    elif row["at_risk_deals"] == 1 or (row["outstanding"] >= 10000 and row["outstanding"] <= 20000):
        return "🟡 Medium Priority"
    else:
        return "🟢 Normal"

agent_summary["priority"] = agent_summary.apply(get_priority, axis=1)

# Sort by priority (High -> Medium -> Normal) and outstanding
priority_order = {"🔴 High Priority": 0, "🟡 Medium Priority": 1, "🟢 Normal": 2}
agent_summary["priority_sort"] = agent_summary["priority"].map(priority_order)
agent_summary = agent_summary.sort_values(["priority_sort", "outstanding"], ascending=[True, False])

# Format for display
display_summary = agent_summary[[
    "priority", "agent_name", "total_deals", "at_risk_deals", "outstanding", "collection_rate"
]].copy()
display_summary["outstanding"] = display_summary["outstanding"].apply(lambda x: f"${x:,.0f}")
display_summary["collection_rate"] = display_summary["collection_rate"].apply(lambda x: f"{x:.1f}%")

st.dataframe(display_summary, use_container_width=True, hide_index=True)

st.subheader("At‑Risk Accounts")
risk_df = df[df["risk_score"] >= 2].sort_values(["risk_score","days_outstanding","leakage_delta"], ascending=[False, False, False])
st.dataframe(risk_df[["referral_id","client_name","agent_name","stage","commission_due","amount_collected","leakage_delta","days_outstanding","risk_score","last_touch","special_terms"]], use_container_width=True)

st.download_button(
    label="Download At‑Risk CSV",
    data=risk_df.to_csv(index=False).encode("utf-8"),
    file_name="at_risk_accounts.csv",
    mime="text/csv"
)

st.subheader("📧 Email Generator")
st.write("Generate collection emails for at-risk accounts with outstanding balances.")

# Filter for accounts that need emails (invoiced but not fully collected)
email_candidates = df[
    (df["invoice_sent_date"].notna()) & 
    (df["amount_collected"] < df["commission_due"])
].copy()

if len(email_candidates) > 0:
    # Let user select which account to email
    email_options = [
        f"{row['referral_id']} - {row['client_name']} ({row['agent_name']}) - ${row['commission_due'] - row['amount_collected']:,.0f} outstanding"
        for idx, row in email_candidates.iterrows()
    ]
    
    selected_email = st.selectbox("Select account to generate email for:", email_options)
    
    # Get the selected row
    selected_idx = email_options.index(selected_email)
    selected_row = email_candidates.iloc[selected_idx]
    
    # Determine template based on days outstanding
    days_out = selected_row.get('days_outstanding')
    if pd.notna(days_out):
        days_out = int(days_out)
        if days_out <= 14:
            template_name = "Template #1: Friendly Reminder (7-14 days)"
        elif days_out <= 30:
            template_name = "Template #2: Value-oriented (15-30 days)"
        elif days_out <= 45:
            template_name = "Template #3: Clear next step (30-45 days)"
        else:
            template_name = "Template #4: Escalation (45+ days)"
    else:
        template_name = "Template #1: Friendly Reminder"
        days_out = 0
    
    st.info(f"📋 Using {template_name} ({days_out} days outstanding)")
    
    # Fill in template
    agent_name = selected_row['agent_name']
    client_name = selected_row['client_name']
    referral_id = selected_row['referral_id']
    amount_due = selected_row['commission_due']
    amount_due_str = f"${amount_due:,.0f}"
    
    invoice_date = selected_row['invoice_sent_date']
    if pd.notna(invoice_date):
        invoice_date_str = pd.Timestamp(invoice_date).strftime('%B %d, %Y')
    else:
        invoice_date_str = '[invoice date]'
    
    # Generate email based on days outstanding
    if days_out <= 14:
        subject = f"Quick follow-up on {client_name} referral ({referral_id})"
        body = f"""Hi {agent_name},

Hope all's well! Following up on the invoice for the {client_name} referral sent on {invoice_date_str} for {amount_due_str}. 
Let me know if you need any further details. I'm also happy to assist investigating further if needed. 

Thanks so much,
Neil Inn"""
    elif days_out <= 30:
        subject = f"Aligning on {client_name} referral — invoice {referral_id}"
        body = f"""Hi {agent_name},

Checking in on the {amount_due_str} invoice for {client_name}. We want to keep everything simple and timely for your team. 
Can you share the expected payment date? If there are any discrepancies with closing docs, I can help reconcile quickly.

Appreciate you,
Neil"""
    elif days_out <= 45:
        subject = f"Next step for {referral_id} — scheduling a quick sync?"
        body = f"""Hi {agent_name},

We're at {days_out} days since invoicing on {client_name} ({amount_due_str}). If payment is queued, great — if not, could we align on a date this week? I'm happy to jump on a 10-minute call to resolve any blockers.

Best,
Neil"""
    else:
        subject = f"Action needed — {client_name} referral {referral_id}"
        body = f"""Hi {agent_name},

We're at {days_out} days outstanding for {client_name} ({amount_due_str}). 
Please confirm payment status or share any issues today so we can resolve quickly. I've attached the original invoice and closing statement for convenience.

Thank you,
Neil"""
    
    # Display the email
    st.markdown("**Subject:**")
    st.code(subject, language=None)
    
    st.markdown("**Body:**")
    st.text_area("", body, height=200, key="email_body")
    
    # Agent email input (in production, this would come from your data)
    agent_email = st.text_input("📧 Enter agent's email address:", placeholder="agent@example.com", key="agent_email_input")
    
    # Action buttons
    col_draft, col_manual = st.columns(2)
    
    with col_draft:
        # Try to import Gmail helper
        gmail_available = True
        try:
            import sys
            sys.path.append('scripts')
            from gmail_helper import create_draft
        except ImportError:
            gmail_available = False
        
        if gmail_available:
            if st.button("📨 Create Gmail Draft", type="primary", use_container_width=True, disabled=not agent_email):
                if agent_email:
                    with st.spinner("Creating draft in Gmail..."):
                        try:
                            draft_id = create_draft(
                                to_email=agent_email,
                                subject=subject,
                                body=body
                            )
                            if draft_id:
                                st.success(f"✅ Draft created! Check your Gmail drafts folder.")
                                st.caption(f"Draft ID: {draft_id}")
                            else:
                                st.error("❌ Failed to create draft. See setup instructions in docs/gmail_setup_guide.md")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            st.info("💡 Run setup first: See docs/gmail_setup_guide.md")
                else:
                    st.warning("⚠️ Please enter the agent's email address first")
        else:
            st.button("📨 Create Gmail Draft (Setup Required)", disabled=True, use_container_width=True)
            with st.expander("ℹ️ How to enable Gmail drafts"):
                st.markdown("""
                1. Install packages: `pip install -r requirements.txt`
                2. Follow setup guide: `docs/gmail_setup_guide.md`
                3. Restart the dashboard
                """)
    
    with col_manual:
        st.button("📋 Copy to Clipboard", help="Copy email to clipboard (coming soon)", use_container_width=True)
    
    st.caption("💡 Tip: Enter agent's email, then click 'Create Gmail Draft' to create a draft in your Gmail!")
    
else:
    st.success("✅ No outstanding invoices need follow-up emails at this time!")

st.subheader("Referral Client Database")

# Helper to format money safely
def fmt_money(x):
    try:
        return f"${float(x):,.0f}"
    except:
        return "-"

# Search functionality
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    search_query = st.text_input("🔍 Search by client name, agent, or referral ID", "")

# Filter dataframe based on search
if search_query:
    search_lower = search_query.lower()
    filtered_df = df[
        df["client_name"].str.lower().str.contains(search_lower, na=False) |
        df["agent_name"].str.lower().str.contains(search_lower, na=False) |
        df["referral_id"].str.lower().str.contains(search_lower, na=False)
    ]
    if len(filtered_df) == 0:
        st.warning(f"No results found for '{search_query}'")
        filtered_df = df
else:
    filtered_df = df

# Selection
row_id = st.selectbox("Pick a referral to inspect", filtered_df["referral_id"])

detail = df[df["referral_id"] == row_id].iloc[0]
due = detail.get("commission_due")
due = float(due) if pd.notna(due) else 0
collected = detail.get("amount_collected")
collected = float(collected) if pd.notna(collected) else 0
outstanding = max(due - collected, 0)
pct_collected = (collected / due * 100) if due > 0 else 0
status = detail.get("collection_status", "Unknown")
stage = detail.get("stage", "Unknown")
days_outstanding = detail.get("days_outstanding")
days_outstanding_disp = int(days_outstanding) if pd.notna(days_outstanding) else None
last_touch = detail.get("last_touch")
days_since_touch = (pd.Timestamp.today().normalize() - last_touch).days if pd.notna(last_touch) else None
risk = detail.get("risk_score")
risk = int(risk) if pd.notna(risk) else 0

# Header card
st.markdown("### " + f"{detail['client_name']} • {detail['agent_name']}")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Stage", stage)
with m2:
    st.metric("Status", status)
with m3:
    st.metric("Risk Score", risk)
with m4:
    st.metric("Days Outstanding", days_outstanding_disp if days_outstanding_disp is not None else 0)

# Money bar
st.write("**Collections Progress**")
st.progress(min(max(pct_collected/100, 0), 1))
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Commission Due", fmt_money(due))
with c2:
    st.metric("Collected", fmt_money(collected))
with c3:
    st.metric("Outstanding", fmt_money(outstanding))

# Quick context chips
chips = []
if days_since_touch is not None:
    chips.append(f"Last touch: {days_since_touch}d ago")
if isinstance(detail.get("special_terms"), str) and detail["special_terms"].strip():
    chips.append(f"Notes: {detail['special_terms']}")
if chips:
    st.caption(" • ".join(chips))

# Recommended next action (simple heuristic)
def recommended_action(d):
    # Early stage deals - no commission yet
    if due == 0 or stage not in ["Closed Won"]:
        return "Deal in progress — monitor for close. No collections action needed yet."
    
    # Closed & fully collected
    if outstanding <= 0 and due > 0:
        return "No action needed — fully collected. Close out and archive."
    
    # Closed but not yet invoiced
    if status == "Not Invoiced":
        return "Send invoice today. Add a 7-day reminder and a 14-day escalation."
    
    # Invoiced but not collected
    if status == "Invoiced":
        if days_outstanding_disp and days_outstanding_disp > 45:
            return "Escalation email + attach invoice & closing docs; propose 10-min call."
        if days_outstanding_disp and days_outstanding_disp > 30:
            return "Firm reminder; request payment date; offer quick sync to resolve blockers."
        return "Friendly nudge; confirm receipt; offer to resend invoice."
    
    return "Review docs and align with Finance; verify close/commission details."

st.markdown("**Recommended next step**")
st.info(recommended_action(detail))

# Timeline & raw data
with st.expander("Timeline"):
    st.write(f"Referral date: {detail['referral_date']}")
    st.write(f"Close date: {detail['close_date'] if pd.notna(detail['close_date']) else '—'}")
    st.write(f"Invoice sent: {detail['invoice_sent_date'] if pd.notna(detail['invoice_sent_date']) else '—'}")
    st.write(f"Last touch: {detail['last_touch'] if pd.notna(detail['last_touch']) else '—'}")

with st.expander("Raw fields"):
    st.json({k:(str(v) if hasattr(v, 'isoformat') else (str(v) if pd.isna(v) else v))
             for k,v in detail.to_dict().items()})

st.caption("MVP: Swap in Retool + Zapier + Gmail Drafts for production‑ready workflow.")

# HomeLight RevOps MVP — Referral‑to‑Revenue Scorecard & Collections Accelerator

> **Interview Project for HomeLight** | Built in 3 hours | Production-ready MVP

A full-stack revenue operations dashboard that identifies at-risk referral commissions, prioritizes collection efforts by agent/partner, and automates follow-up emails with Gmail integration.

**🎯 Problem Solved:** Revenue teams struggle to track hundreds of referral commissions, identify payment risks early, and follow up consistently. This dashboard makes it instant.

**💡 Key Innovation:** Agent-level risk aggregation (not just deal-level) + "repeat offender" detection + smart email templates that adapt to days outstanding.

## What this includes
- **Scorecard dashboard (Streamlit)** with KPIs: referral volume, conversion %, $ to collect, aging, SLA breaches, and leakage risks.
- **Agent Risk Summary** — aggregated view showing which agents have the most at-risk deals and outstanding balances.
- **Risk scoring** (simple, explainable rules) with **repeat offender detection** (+1 risk for agents with 2+ at-risk deals).
- **Email Generator** — automatically fills collection email templates based on days outstanding.
- **Gmail Draft Integration** — create ready-to-send drafts in your Gmail with one click (optional, requires setup).
- **Collections accelerator** — ready‑to‑paste email templates with merge fields.
- **Data pipeline** (Python) that transforms a raw referrals CSV into clean metrics/features for the dashboard.
- **Sample data** so you can demo immediately.

> This MVP is intentionally lightweight so it can be demoed in a 2‑minute video.

## Quickstart

### Mac/Linux
```bash
# 1) Create & activate a virtual env
python3 -m venv .venv
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the dashboard
streamlit run app/streamlit_app.py
```

### Windows PowerShell
```powershell
# 1) Create & activate a virtual env
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Run the dashboard
streamlit run app/streamlit_app.py
```

> **Note:** If you get an execution policy error on Windows, use `.\.venv\Scripts\activate.bat` instead.

## (Optional) Enable Gmail Draft Creation

To create email drafts directly from the dashboard:

```bash
# 1) Follow the setup guide
# See: docs/gmail_setup_guide.md

# 2) Run the setup script
python scripts/setup_gmail.py

# 3) Restart the dashboard
streamlit run app/streamlit_app.py
```

Now you'll have a "Create Gmail Draft" button in the Email Generator! 📨

## Data model (data/sample_referrals.csv)
| column | type | description |
|---|---|---|
| referral_id | string | unique id |
| client_name | string | buyer/seller name |
| agent_name | string | referral partner |
| stage | enum | Referred, Engaged, Under Contract, Closed Won, Closed Lost |
| referral_date | date | YYYY‑MM‑DD |
| close_date | date | if closed |
| commission_pct | float | expected % |
| price | float | deal price if known |
| commission_due | float | expected $ commission |
| invoice_sent_date | date | when invoice was sent |
| amount_invoiced | float | $ invoiced |
| amount_collected | float | $ collected |
| last_touch | date | last touch with agent |
| special_terms | string | free‑text flags (legacy relationships, disputes, etc.) |

The pipeline derives:
- **days_to_close**, **days_outstanding**, **collection_status**, **leakage_delta** (due ‑ collected), and a simple **risk_score**.

## How to demo in 2 minutes
1. **Open dashboard** → show KPIs + “At‑Risk” table.
2. **Click a row** → show account timeline and recommended next action.
3. **Open `email_templates.md`** → copy the template that matches the scenario.
4. (Optional) Run `scripts/draft_emails.py` to create Gmail drafts from a CSV of contacts.

## Folder layout
```
app/                # Streamlit UI
scripts/            # ETL + (optional) Gmail draft creator
data/               # Sample CSVs
```

---

### Why this maps to the role
- **Streamline referral‑to‑revenue** with a visible path to collection.
- **AI‑first workflows** via templated, context‑aware outreach (easy to upgrade to GPT).
- **Own scorecards**: single‑pane KPIs with drilldowns.
- **Enhance collections**: surface leakage + aging, standardize follow‑ups.
- **Cross‑functional ready**: Finance can reconcile; Ops can enforce SLAs.


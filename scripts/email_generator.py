"""
Email Template Generator for Collections
Automatically fills in email templates with referral data
"""
import pandas as pd
from datetime import datetime

def get_template_choice(days_outstanding):
    """Select the appropriate template based on days outstanding"""
    if days_outstanding is None or days_outstanding < 7:
        return None
    elif days_outstanding <= 14:
        return 1
    elif days_outstanding <= 30:
        return 2
    elif days_outstanding <= 45:
        return 3
    else:
        return 4

def generate_email(referral_data):
    """Generate a filled-in email template for a referral"""
    
    agent_name = referral_data.get('agent_name', 'there')
    client_name = referral_data.get('client_name', '')
    referral_id = referral_data.get('referral_id', '')
    amount_due = referral_data.get('commission_due', 0)
    amount_due_str = f"${amount_due:,.0f}"
    
    invoice_date = referral_data.get('invoice_sent_date', '')
    if pd.notna(invoice_date):
        invoice_date = pd.Timestamp(invoice_date).strftime('%B %d, %Y')
    else:
        invoice_date = '[invoice date]'
    
    days_outstanding = referral_data.get('days_outstanding')
    if pd.notna(days_outstanding):
        days_outstanding = int(days_outstanding)
    else:
        days_outstanding = None
    
    template_num = get_template_choice(days_outstanding)
    
    if template_num is None:
        return "No email needed - not yet 7 days outstanding."
    
    templates = {
        1: {
            'subject': f"Quick follow-up on {client_name} referral ({referral_id})",
            'body': f"""Hi {agent_name},

Hope all's well! Following up on the invoice for the {client_name} referral sent on {invoice_date} for {amount_due_str}. 
Let me know if you need any further details. I'm also happy to assist investigating further if needed. 

Thanks so much,
Neil Inn"""
        },
        2: {
            'subject': f"Aligning on {client_name} referral — invoice {referral_id}",
            'body': f"""Hi {agent_name},

Checking in on the {amount_due_str} invoice for {client_name}. We want to keep everything simple and timely for your team. 
Can you share the expected payment date? If there are any discrepancies with closing docs, I can help reconcile quickly.

Appreciate you,
Neil"""
        },
        3: {
            'subject': f"Next step for {referral_id} — scheduling a quick sync?",
            'body': f"""Hi {agent_name},

We're at {days_outstanding} days since invoicing on {client_name} ({amount_due_str}). If payment is queued, great — if not, could we align on a date this week? I'm happy to jump on a 10-minute call to resolve any blockers.

Best,
Neil"""
        },
        4: {
            'subject': f"Action needed — {client_name} referral {referral_id}",
            'body': f"""Hi {agent_name},

We're at {days_outstanding} days outstanding for {client_name} ({amount_due_str}). 
Please confirm payment status or share any issues today so we can resolve quickly. I've attached the original invoice and closing statement for convenience.

Thank you,
Neil"""
        }
    }
    
    return templates[template_num]

def generate_emails_for_at_risk():
    """Generate emails for all at-risk accounts"""
    df = pd.read_csv('data/sample_referrals.csv', parse_dates=['invoice_sent_date'])
    
    # Calculate days outstanding
    today = pd.Timestamp.today().normalize()
    df['days_outstanding'] = (today - df['invoice_sent_date']).dt.days
    
    # Get at-risk accounts (those with outstanding balances and invoiced)
    df['outstanding'] = df['commission_due'].fillna(0) - df['amount_collected'].fillna(0)
    at_risk = df[(df['outstanding'] > 0) & (df['invoice_sent_date'].notna())]
    
    print("=" * 60)
    print("COLLECTION EMAILS FOR AT-RISK ACCOUNTS")
    print("=" * 60)
    
    for idx, row in at_risk.iterrows():
        email = generate_email(row)
        if isinstance(email, dict):
            print(f"\n\n{'='*60}")
            print(f"TO: {row['agent_name']} (re: {row['client_name']})")
            print(f"Days Outstanding: {int(row['days_outstanding']) if pd.notna(row['days_outstanding']) else 'N/A'}")
            print(f"Outstanding: ${row['outstanding']:,.0f}")
            print("-" * 60)
            print(f"SUBJECT: {email['subject']}")
            print("-" * 60)
            print(email['body'])
            print("=" * 60)

if __name__ == "__main__":
    generate_emails_for_at_risk()


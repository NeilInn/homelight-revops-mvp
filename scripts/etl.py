import pandas as pd
from dateutil import parser

def transform(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv, parse_dates=["referral_date","close_date","invoice_sent_date","last_touch"])
    # Compute features similar to the Streamlit app
    from datetime import datetime
    today = pd.Timestamp.today().normalize()
    df["days_to_close"] = (df["close_date"] - df["referral_date"]).dt.days
    df["amount_invoiced"] = df["amount_invoiced"].fillna(0)
    df["amount_collected"] = df["amount_collected"].fillna(0)
    df["leakage_delta"] = (df["commission_due"].fillna(0)) - df["amount_collected"]
    df["days_outstanding"] = pd.Series(pd.NA, index=df.index)
    mask = df["invoice_sent_date"].notna()
    df.loc[mask, "days_outstanding"] = (today - df.loc[mask,"invoice_sent_date"]).dt.days
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    transform("data/sample_referrals.csv", "data/referrals_features.csv")

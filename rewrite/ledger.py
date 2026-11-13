import pandas as pd

def load_ledger(path):
    df = pd.read_excel(path, sheet_name="Ledger")
    df = df.dropna(subset=["MemberID"])
    df["Account"] = df["Account"].str.upper()
    return df

def end_of_day(rows, account, first_date, as_of):
    acct = rows[rows["Account"] == account]
    daily = acct.groupby("PostedDate")["RunningBalance"].last()
    days = pd.date_range(first_date, as_of)
    return daily.reindex(days).ffill()
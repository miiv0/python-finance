import pandas as pd

def load_ledger(path):
    df = pd.read_excel(path, sheet_name="Ledger")
    df = df.dropna(subset=["MemberID"])
    df["Account"] = df["Account"].str.upper()
    return df

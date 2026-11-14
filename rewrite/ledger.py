from dataclasses import dataclass

import pandas as pd

def load_ledger(path):
    df = pd.read_excel(path, sheet_name="Ledger")
    df = df.dropna(subset=["MemberID"])
    df["Account"] = df["Account"].str.upper()
    return df

def end_of_day(rows, account, first_date, as_of):
    acct = rows[rows["Account"] == account]
    if len(acct) == 0:
        opening = 0.0
    else:
        opening = acct["RunningBalance"].iloc[0] - acct["Amount"].iloc[0]
    daily = acct.groupby("PostedDate")["RunningBalance"].last()
    days = pd.date_range(first_date, as_of)
    return daily.reindex(days).ffill().fillna(opening)

@dataclass
class MemberHistory:
    member_id: str
    rows: pd.DataFrame
    first_date: pd.Timestamp
    last_date: pd.Timestamp
    chk: pd.Series
    sav: pd.Series

def build_history(member_id, rows, as_of):
    rows = rows[rows["PostedDate"] <= as_of].sort_values("PostedDate", kind="stable")
    chk_rows = rows[rows["Account"] == "CHK"]
    if len(chk_rows) == 0:
        first_date = as_of
    else:
        first_date = chk_rows["PostedDate"].min()
    chk = end_of_day(rows, "CHK", first_date, as_of)
    sav = end_of_day(rows, "SAV", first_date, as_of)
    return MemberHistory(member_id, rows, first_date, as_of, chk, sav)

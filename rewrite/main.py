import pandas as pd
from ledger import load_ledger

df = load_ledger("data/members_ledger.xlsx")
print(df.head())
print(len(df))

a = df[df["MemberID"] == "A"]
a = a.sort_values("PostedDate", kind="stable")

df.groupby("Channel")["Amount"].sum()

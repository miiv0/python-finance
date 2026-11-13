import pandas as pd
from ledger import load_ledger

df = load_ledger("data/members_ledger.xlsx")
print(df.head())
print(len(df))

a = df[df["MemberID"] == "A"]
a = a.sort_values("PostedDate", kind="stable")
as_of = df["PostedDate"].max()
chk = a[a["Account"] == "CHK"]
first_date = chk["PostedDate"].min()
daily = chk.groupby("PostedDate")["RunningBalance"].last()
days = pd.date_range(first_date, as_of)
daily = daily.reindex(days).ffill()

print(len(daily))
print(daily.head(10))
print(daily["2025-10-28"])
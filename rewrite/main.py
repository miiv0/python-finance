import pandas as pd
from ledger import load_ledger, end_of_day

df = load_ledger("data/members_ledger.xlsx")
print(df.head())
print(len(df))

a = df[df["MemberID"] == "A"]
a = a.sort_values("PostedDate", kind="stable")
as_of = df["PostedDate"].max()
chk = a[a["Account"] == "CHK"]
first_date = chk["PostedDate"].min()
daily = end_of_day(a, "CHK", first_date, as_of)

print(len(daily))
print(daily.head(10))
print(daily["2025-10-28"])

sav = end_of_day(a, "SAV", first_date, as_of)
print(sav.head())

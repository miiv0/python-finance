import pandas as pd

from ledger import load_ledger, build_history

df = load_ledger("data/members_ledger.xlsx")
as_of = df["PostedDate"].max()

h = build_history("A", df[df["MemberID"] == "A"], as_of)

print(h.first_date)
print(len(h.chk))
print(h.chk["2025-10-28"])
print(h.sav.head())

early = h.up_to(pd.Timestamp("2026-06-01"))
print(early.last_date)
print(len(early.chk))
print(early.rows["PostedDate"].max())
print(h.last_date)

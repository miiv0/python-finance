from ledger import load_ledger, build_history

df = load_ledger("data/members_ledger.xlsx")
as_of = df["PostedDate"].max()

h = build_history("A", df[df["MemberID"] == "A"], as_of)

print(h.first_date)
print(len(h.chk))
print(h.chk["2025-10-28"])
print(h.sav.head())

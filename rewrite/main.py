import pandas as pd

from ledger import load_histories

histories = load_histories("data/members_ledger.xlsx")

for h in histories:
    print(h.member_id, h.profile.name, h.first_date.date(), len(h.chk), h.chk.iloc[-1], h.sav.iloc[-1])

a = histories[0]
print(a.chk["2025-10-28"])
print(a.profile.courtesy_pay, a.profile.overdraft_fee)

early = a.up_to(pd.Timestamp("2026-06-01"))
print(early.last_date.date(), len(early.chk), early.profile.name)

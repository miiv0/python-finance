from ledger import load_histories
from recurring import detect

for h in load_histories("data/members_ledger.xlsx"):
    for item in detect(h):
        print(h.member_id, item["description"], item["cadence"], item["day"], round(item["amount"], 2))

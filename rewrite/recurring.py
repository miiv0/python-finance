import pandas as pd

def find_candidates(history):
    rows = history.rows
    rows = rows[rows["Account"] == "CHK"]
    rows = rows[~rows["Category"].isin(["Fee", "Loan proceeds"])]
    candidates = []
    for description, group in rows.groupby("Description"):
        if len(group) < 3:
            continue
        all_pos = (group["Amount"] > 0).all()
        all_neg = (group["Amount"] < 0).all()    
        if not all_pos and not all_neg:
            continue
        kind = "income" if all_pos else "bill"
        candidates.append((description, kind, group)) 
    return candidates

def group_stats(group):
    gaps = group["PostedDate"].diff().dt.days.dropna()
    med_gap = gaps.median()
    amounts = group["Amount"]
    recent = amounts.tail(26)
    cv = recent.std(ddof=0) / abs(recent.mean())
    amount = amounts.tail(6).median() if cv < 0.03 else recent.mean()
    return gaps, med_gap, cv, amount

def detect(history):
    found = []
    for description, kind, group in find_candidates(history):
        gaps, med_gap, cv, amount = group_stats(group)
        if cv > 0.40:
            continue
        share7 = ((gaps - 7).abs() <= 1).mean()
        share14 = ((gaps - 14).abs() <= 1).mean()
        if 6 <= med_gap <= 8 and share7 >= 0.75:
            found.append({
                "description": description,
                "kind": kind,
                "cadence": "weekly",
                "day": 0,
                "amount": amount,
            })
            continue
        if 13 <= med_gap <= 15 and share14 >= 0.75:
            found.append({
                "description": description,
                "kind": kind,
                "cadence": "biweekly",
                "day": 0,
                "amount": amount,
            })
            continue
        days = group["PostedDate"].dt.day
        if 27 <= med_gap <= 34 and days.std(ddof=0) <= 2.5:
            found.append({
                "description": description,
                "kind": kind,
                "cadence": "monthly",
                "day": round(days.median()),
                "amount": amount,
            })
    return found

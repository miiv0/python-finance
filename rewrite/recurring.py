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
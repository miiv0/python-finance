import pandas as pd

df = pd.read_excel("data/members_ledger.xlsx", sheet_name="Ledger")
print(df.head())
print(df.columns)
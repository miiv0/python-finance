from dataclasses import dataclass

import pandas as pd

from settings import ALERT_THRESHOLD


def load_ledger(path):
    df = pd.read_excel(path, sheet_name="Ledger")
    df = df.dropna(subset=["MemberID"])
    df["Account"] = df["Account"].str.upper()
    return df


@dataclass
class MemberProfile:
    member_id: str
    name: str = ""
    member_since: pd.Timestamp | None = None
    product: str = ""
    courtesy_pay: bool = False
    overdraft_fee: float = 35
    max_fees_per_day: int = 3
    min_item_for_fee: float = 15
    card_overdraft_opt_in: bool = False
    nsf_fee: float = 0
    savings_first: bool = False
    low_balance_alert: bool = False
    alert_threshold: float = ALERT_THRESHOLD
    direct_deposit: bool = False
    external_card_debt: float = 0
    external_card_apr: float = 0
    notes: str = ""


MEMBER_COLUMNS = {
    "MemberID": "member_id",
    "Name": "name",
    "MemberSince": "member_since",
    "Product": "product",
    "CourtesyPay": "courtesy_pay",
    "OverdraftFee": "overdraft_fee",
    "MaxFeesPerDay": "max_fees_per_day",
    "MinItemForFee": "min_item_for_fee",
    "CardOverdraftOptIn": "card_overdraft_opt_in",
    "NsfFee": "nsf_fee",
    "SavingsFirst": "savings_first",
    "LowBalanceAlert": "low_balance_alert",
    "AlertThreshold": "alert_threshold",
    "DirectDeposit": "direct_deposit",
    "ExternalCardDebt": "external_card_debt",
    "ExternalCardApr": "external_card_apr",
    "Notes": "notes",
}


def load_members(path):
    df = pd.read_excel(path, sheet_name="Members")
    df = df.dropna(subset=["MemberID"])
    profiles = []
    for row in df.to_dict("records"):
        fields = {MEMBER_COLUMNS[col]: value for col, value in row.items() if col in MEMBER_COLUMNS and pd.notna(value)}
        profiles.append(MemberProfile(**fields))
    return profiles


def end_of_day(rows, account, first_date, as_of):
    acct = rows[rows["Account"] == account]
    if len(acct) == 0:
        opening = 0.0
    else:
        opening = acct["RunningBalance"].iloc[0] - acct["Amount"].iloc[0]
    daily = acct.groupby("PostedDate")["RunningBalance"].last()
    days = pd.date_range(first_date, as_of)
    return daily.reindex(days).ffill().fillna(opening)


@dataclass
class MemberHistory:
    profile: MemberProfile
    rows: pd.DataFrame
    first_date: pd.Timestamp
    last_date: pd.Timestamp
    chk: pd.Series
    sav: pd.Series

    @property
    def member_id(self):
        return self.profile.member_id

    def up_to(self, cutoff):
        return build_history(self.profile, self.rows, min(cutoff, self.last_date))


def build_history(profile, rows, as_of):
    rows = rows[rows["PostedDate"] <= as_of].sort_values("PostedDate", kind="stable")
    chk_rows = rows[rows["Account"] == "CHK"]
    if len(chk_rows) == 0:
        first_date = as_of
    else:
        first_date = chk_rows["PostedDate"].min()
    chk = end_of_day(rows, "CHK", first_date, as_of)
    sav = end_of_day(rows, "SAV", first_date, as_of)
    return MemberHistory(profile, rows, first_date, as_of, chk, sav)


def load_histories(path):
    ledger = load_ledger(path)
    as_of = ledger["PostedDate"].max()
    histories = []
    for profile in load_members(path):
        rows = ledger[ledger["MemberID"] == profile.member_id]
        if len(rows) > 0:
            histories.append(build_history(profile, rows, as_of))
    return histories

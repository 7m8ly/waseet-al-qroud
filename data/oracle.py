"""
Reference calculator for the synthetic test data (rulebook v1.2).

PURPOSE
  Used ONLY while building and validating the data: it checks that the numbers we
  planted in each case really produce the outcome we intended. It is written
  independently of the engine and must NEVER be imported by engine/ or by the
  evaluation harness. Expected outcomes in the case files are the *planted
  intentions* (written by hand in cases_spec.py); this oracle is a cross-check.

All money is integer IQD. All comparisons are exact integer comparisons (no floats).
"""
import csv
import re
from datetime import date

AS_OF = date(2026, 10, 31)
AS_OF_MONTH = (2026, 10)
WINDOW_MONTHS = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
FEE_PCT = 12                      # annual flat fee, percent (assumption, see DECISIONS.md D1)

PRODUCTS = {
    "micro":    dict(amount_min=250_000,   amount_max=2_500_000,  term_min=3,  term_max=12, activity_months_min=12),
    "minor":    dict(amount_min=2_500_001, amount_max=8_000_000,  term_min=13, term_max=20, activity_months_min=36),
    "moderate": dict(amount_min=8_000_001, amount_max=15_000_000, term_min=21, term_max=30, activity_months_min=60),
}
ACTIVITY_PROOF = {"lease_contract", "business_licence", "professional_licence",
                  "purchase_invoices", "inspection_report"}                      # C8
INCOME_EVIDENCE = {"lease_contract", "purchase_invoices", "inspection_report"}   # E4
GUARANTEE_TYPES = {"guarantor", "collateral_document"}
WALLET_TYPES = {"inflow", "self_transfer", "refund", "loan_proceeds", "outflow"}
C_RULES = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]


def ceil_div(a, b):
    return -(-a // b)


def installment(amount, term, fee_pct=FEE_PCT):
    """amount * (1 + fee * term/12) / term, rounded UP to the next dinar, exact integer maths."""
    return ceil_div(amount * (1200 + fee_pct * term), 1200 * term)


def product_of(amount):
    for name, p in PRODUCTS.items():
        if p["amount_min"] <= amount <= p["amount_max"]:
            return name
    return None


def activity_months(start):          # start = "YYYY-MM"
    y, m = (int(x) for x in start.split("-"))
    return (AS_OF_MONTH[0] - y) * 12 + (AS_OF_MONTH[1] - m)


_AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ـ": ""})


def norm_name(s):
    s = re.sub(r"[\u064B-\u0652]", "", s or "")
    return re.sub(r"\s+", " ", s.translate(_AR_MAP)).strip().lower()


def read_wallet(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["date"], int(r["amount"]), r["type"]))
    return rows


def wallet_stats(rows):
    """Indicators 3 and 4 (the two that feed rules). Returns dict."""
    first = min(r[0] for r in rows)
    fy, fm = int(first[:4]), int(first[5:7])
    months_of_history = (AS_OF_MONTH[0] - fy) * 12 + (AS_OF_MONTH[1] - fm) + 1
    avail = [m for m in WINDOW_MONTHS if (int(m[:4]), int(m[5:])) >= (fy, fm)]
    totals = {m: 0 for m in avail}
    count = 0
    for d, a, t in rows:
        if t == "inflow" and d[:7] in totals:
            totals[d[:7]] += a
            count += 1
    vals = sorted(totals.values())
    n = len(vals)
    median = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2] + 1) // 2   # half-up
    sufficient = months_of_history >= 3 and count >= 20
    return dict(months_of_history=months_of_history, inflow_count=count,
                typical_monthly_income=median, monthly_totals=totals,
                data_depth="sufficient" if sufficient else "low_data")


def alternative(amount, term, income, obl, product):
    p = PRODUCTS[product]
    T = p["term_max"]
    cap = income // 2 - obl
    if cap <= 0:
        return None
    for t in range(term + 1, T + 1):                                     # step 1: shortest longer term that fits
        if (obl + installment(amount, t)) * 2 <= income:
            return {"amount": amount, "term_months": t}
    k, m = 1200 + FEE_PCT * T, 1200 * T                                  # step 2: reduce amount at max term
    a = (cap * m) // k
    a = (a // 10_000) * 10_000
    while a >= p["amount_min"] and (obl + installment(a, T)) * 2 > income:
        a -= 10_000
    if a < p["amount_min"]:
        return None
    return {"amount": a, "term_months": T}


def evaluate(case, wallet_rows):
    """case = parsed case dict; wallet_rows = list or None. Returns the expected block."""
    ap, rq = case["applicant"], case["request"]
    docs = ap.get("documents") or []
    failed = []

    # --- completeness C1..C10
    c = {
        "C1": bool(ap.get("name")) and ap.get("identity_document_provided") is True,
        "C2": bool(ap.get("wallet_phone")),
        "C3": bool(ap.get("residence")),
        "C4": bool(ap.get("activity")) and bool(ap.get("activity_start")),
        "C5": isinstance(ap.get("declared_net_monthly_income"), int) and ap["declared_net_monthly_income"] > 0,
        "C6": rq.get("amount") is not None and rq.get("term_months") is not None,
        "C7": bool(ap.get("loan_purpose")),
        "C8": any(d["type"] in ACTIVITY_PROOF for d in docs),
        "C9": ap.get("guarantee") in GUARANTEE_TYPES,
        "C10": ap.get("consent_wallet") in (True, False),
    }
    failed += [k for k in C_RULES if not c[k]]

    amount, term = rq.get("amount"), rq.get("term_months")
    income, obl = ap.get("declared_net_monthly_income"), ap.get("existing_obligations", 0)
    prod = product_of(amount) if amount is not None else None
    inst = installment(amount, term) if (amount is not None and term is not None) else None
    act_m = activity_months(ap["activity_start"]) if ap.get("activity_start") else None

    # --- wallet (only if consent given and file present)
    stats = wallet_stats(wallet_rows) if (ap.get("consent_wallet") is True and wallet_rows) else None
    depth = stats["data_depth"] if stats else "not_read"

    # --- product limits, eligibility
    if amount is not None and term is not None:
        p = PRODUCTS.get(prod)
        if p is None or not (p["term_min"] <= term <= p["term_max"]):
            failed.append("P1")
    if not (18 <= ap.get("age", 0) <= 65):
        failed.append("E1")
    if prod and act_m is not None and act_m < PRODUCTS[prod]["activity_months_min"]:
        failed.append("E2")
    e3_ratio = None
    if inst is not None and isinstance(income, int) and income > 0:
        e3_ratio = round((obl + inst) / income, 4)
        if (obl + inst) * 2 > income:
            failed.append("E3")
    income_doc = any(d["type"] in INCOME_EVIDENCE for d in docs)
    if not (depth == "sufficient" or income_doc):
        failed.append("E4")

    # --- consistency
    x1 = False
    e3_wallet = None
    if depth == "sufficient" and isinstance(income, int):
        x1 = stats["typical_monthly_income"] * 100 < income * 60
        if x1:
            failed.append("X1")
            if inst is not None:
                e3_wallet = round((obl + inst) / stats["typical_monthly_income"], 4)
    names = {norm_name(ap.get("name"))}
    if any(norm_name(d.get("name_on_document")) not in names for d in docs):
        failed.append("X2")
    if ap.get("contradictory_answers") is True:           # reserved for dialogue-level tests
        failed.append("X3")

    # --- state by priority
    fs = set(failed)
    if fs & set(C_RULES):
        state = "incomplete"
    elif fs & {"X2", "X3"}:
        state = "needs_clarification"
    elif fs & {"E1", "E2", "P1", "E3"}:
        state = "outside_product_limits"
    elif "E4" in fs:
        state = "needs_clarification"
    elif "X1" in fs:
        state = "needs_clarification"
    else:
        state = "ready_for_review"

    alt = None
    if state == "outside_product_limits" and fs & {"E1", "E2", "P1", "E3"} == {"E3"}:
        alt = alternative(amount, term, income, obl, prod)

    order = C_RULES + ["P1", "E1", "E2", "E3", "E4", "X1", "X2", "X3"]
    exp = {
        "state": state,
        "failed_rules": [r for r in order if r in fs],
        "product": prod,
        "activity_months": act_m,
        "installment": inst,
        "e3_ratio": e3_ratio,
    }
    if e3_wallet is not None:
        exp["e3_ratio_wallet"] = e3_wallet
    exp["typical_monthly_income"] = stats["typical_monthly_income"] if stats else None
    exp["data_depth"] = depth
    exp["labels"] = ["low_data"] if depth == "low_data" else []
    exp["alternative"] = alt
    exp["field_visit_required"] = True
    return exp

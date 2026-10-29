"""
Deterministic synthetic wallet generator.

The monthly real-inflow TOTALS and the inflow COUNTS are planned by hand in
cases_spec.py (so the median and data depth are known in advance). This script
only decides how each monthly total is split into individual transactions and
on which days, using a fixed seed per case. It also adds rows of the other
types (self_transfer, refund, loan_proceeds, outflow) that the engine must
exclude from "real inflow".

Types: inflow, self_transfer, refund, loan_proceeds, outflow
CSV columns: date (YYYY-MM-DD), amount (positive integer IQD), type
No real data is used anywhere.
"""
import calendar
import csv
import hashlib
import math
import random

UNIT = 500   # every transaction is a multiple of 500 IQD


def case_rng(case_id, base_seed=2026):
    h = int(hashlib.sha256(f"{base_seed}:{case_id}".encode()).hexdigest(), 16) % (2**32)
    return random.Random(h)


def split_total(total, n, rng):
    """n positive multiples of UNIT that sum exactly to total."""
    assert total % UNIT == 0, f"total {total} must be a multiple of {UNIT}"
    units = total // UNIT
    assert units >= n, "too many transactions for this total"
    w = [math.exp(rng.gauss(0, 0.55)) for _ in range(n)]
    s = sum(w)
    parts = [max(1, int(units * x / s)) for x in w]
    diff = units - sum(parts)
    i = 0
    while diff != 0:
        j = i % n
        if diff > 0:
            parts[j] += 1
            diff -= 1
        elif parts[j] > 1:
            parts[j] -= 1
            diff += 1
        i += 1
    return [p * UNIT for p in parts]


def pick_days(month, n, rng, spread=True):
    y, m = int(month[:4]), int(month[5:])
    last = calendar.monthrange(y, m)[1]
    if spread and n >= 4:
        days = [min(last, max(1, int((i + rng.random()) * last / n) + 1)) for i in range(n)]
    else:
        days = [rng.randint(1, last) for _ in range(n)]
    return sorted(days)


def month_list(first, last="2026-10"):
    y, m = int(first[:4]), int(first[5:])
    out = []
    while (y, m) <= (int(last[:4]), int(last[5:])):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def make_wallet(case_id, plan):
    """
    plan = dict(first='YYYY-MM',
                totals=[monthly real-inflow totals from first month to 2026-10],
                counts=int | [per-month inflow counts],
                distractors=[(month, day, amount, type), ...])
    Returns sorted list of (date, amount, type).
    """
    rng = case_rng(case_id)
    months = month_list(plan["first"])
    assert len(plan["totals"]) == len(months), f"{case_id}: need {len(months)} monthly totals"
    counts = plan["counts"] if isinstance(plan["counts"], list) else [plan["counts"]] * len(months)
    rows = []
    for mo, tot, n in zip(months, plan["totals"], counts):
        for d, a in zip(pick_days(mo, n, rng, spread=n >= 8), split_total(tot, n, rng)):
            rows.append((f"{mo}-{d:02d}", a, "inflow"))
        # outflows: supplier / household payments (excluded from income)
        n_out = rng.randint(6, 10)
        out_total = int(tot * rng.uniform(0.45, 0.75)) // UNIT * UNIT
        for d, a in zip(pick_days(mo, n_out, rng, spread=False), split_total(max(out_total, n_out * UNIT), n_out, rng)):
            rows.append((f"{mo}-{d:02d}", a, "outflow"))
    for mo, day, amt, typ in plan.get("distractors", []):
        assert typ in {"self_transfer", "refund", "loan_proceeds"}
        rows.append((f"{mo}-{day:02d}", amt, typ))
    rows.sort(key=lambda r: (r[0], r[2], r[1]))
    return rows


def write_wallet(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "amount", "type"])
        w.writerows(rows)

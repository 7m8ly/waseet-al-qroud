"""
Validate every case file (held-out, dev, fairness twins).

  python data/cases_validate.py

Checks: file shape and types, split folders, unique ids and names, wallet files (columns, types,
dates <= as_of, integer amounts), consent <-> wallet consistency, and that the median, inflow count
and data depth in `expected` are what the wallet CSV really contains. It also re-runs the independent
oracle and compares the whole `expected` block. Exit code 1 on any problem.
Uses only PyYAML + the standard library (the engine's Pydantic models are a separate thing).
"""
import csv
import glob
import os
import sys

import yaml

import oracle

ROOT = os.path.dirname(os.path.abspath(__file__))
errors = []


def err(cid, msg):
    errors.append(f"{cid}: {msg}")


REQUIRED_APPLICANT = ["name", "gender", "age", "residence", "governorate", "identity_document_provided",
                      "wallet_phone", "activity", "activity_start", "declared_net_monthly_income",
                      "existing_obligations", "loan_purpose", "guarantee", "consent_wallet", "documents"]


def check_shape(c, path):
    cid = c.get("id", path)
    for k in ["id", "split", "scenario", "as_of", "applicant", "request", "wallet", "expected"]:
        if k not in c:
            err(cid, f"missing key {k}")
            return False
    a = c["applicant"]
    for k in REQUIRED_APPLICANT:
        if k not in a:
            err(cid, f"applicant.{k} missing")
    if str(c["as_of"]) != "2026-10-31":
        err(cid, "as_of must be 2026-10-31")
    if not isinstance(a.get("age"), int):
        err(cid, "age must be int")
    if a.get("gender") not in ("m", "f"):
        err(cid, "gender must be m or f")
    if not str(a.get("wallet_phone", "")).startswith("SYN-"):
        err(cid, "wallet_phone must be an obviously synthetic SYN- value")
    for d in a.get("documents", []):
        if d.get("type") not in oracle.ACTIVITY_PROOF or not d.get("name_on_document"):
            err(cid, f"bad document {d}")
    if a.get("guarantee") not in (None, "guarantor", "collateral_document"):
        err(cid, "bad guarantee value")
    if a.get("consent_wallet") not in (True, False, None):
        err(cid, "bad consent value")
    return True


def check_wallet(c, base):
    cid = c["id"]
    a = c["applicant"]
    if c["wallet"] is None:
        if a["consent_wallet"] is True:
            err(cid, "consent_wallet is true but no wallet file")
        return None
    if a["consent_wallet"] is not True:
        err(cid, "wallet file present although consent is not true")
    path = os.path.join(base, c["wallet"])
    if not os.path.exists(path):
        err(cid, f"wallet file not found: {c['wallet']}")
        return None
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames != ["date", "amount", "type"]:
            err(cid, f"wallet columns are {rd.fieldnames}")
            return None
        rows = []
        for i, r in enumerate(rd, start=2):
            try:
                amt = int(r["amount"])
            except ValueError:
                err(cid, f"line {i}: amount not an integer")
                continue
            if amt <= 0:
                err(cid, f"line {i}: amount must be positive")
            if r["type"] not in oracle.WALLET_TYPES:
                err(cid, f"line {i}: unknown type {r['type']}")
            if r["date"] > "2026-10-31":
                err(cid, f"line {i}: date after as_of")
            rows.append((r["date"], amt, r["type"]))
    if not rows:
        err(cid, "empty wallet")
        return None
    return rows


def main():
    seen_ids, seen_names = set(), {}
    counts = {}
    paths = []
    for sub in ("heldout", "dev"):
        paths += sorted(glob.glob(os.path.join(ROOT, sub, "cases", "*.yaml")))
    twins = sorted(glob.glob(os.path.join(ROOT, "fairness", "pairs", "*.yaml")))

    for p in paths:
        base = os.path.dirname(os.path.dirname(p))
        c = yaml.safe_load(open(p, encoding="utf-8"))
        if not check_shape(c, p):
            continue
        cid = c["id"]
        if cid in seen_ids:
            err(cid, "duplicate id")
        seen_ids.add(cid)
        sub = os.path.basename(base)
        if (sub == "heldout") != (c["split"] == "heldout"):
            err(cid, "split does not match folder")
        if cid != os.path.splitext(os.path.basename(p))[0]:
            err(cid, "id does not match file name")
        rows = check_wallet(c, base)
        exp = oracle.evaluate(c, rows)
        if exp != c["expected"]:
            diff = {k: (c["expected"].get(k), exp.get(k)) for k in set(exp) | set(c["expected"]) if c["expected"].get(k) != exp.get(k)}
            err(cid, f"expected block disagrees with the wallet/oracle: {diff}")
        # product letter in the id must match the product derived from the amount
        letter = {"M": "micro", "N": "minor", "D": "moderate"}[cid.split("-")[1]]
        if exp["product"] != letter:
            err(cid, f"id says {letter} but amount maps to {exp['product']}")
        counts[(c["split"], letter)] = counts.get((c["split"], letter), 0) + 1
        for nm in [c["applicant"]["name"]]:
            if nm in seen_names:
                err(cid, f"name reused from {seen_names[nm]}")
            seen_names[nm] = cid
    for split, per in (("heldout", 4), ("dev", 8)):
        for prod in ("micro", "minor", "moderate"):
            if counts.get((split, prod), 0) != per:
                err("COUNT", f"{split}/{prod}: expected {per}, found {counts.get((split, prod), 0)}")

    # fairness twins: same wallet and numbers, only name / gender / governorate differ
    for p in twins:
        t = yaml.safe_load(open(p, encoding="utf-8"))
        cid = t["id"]
        base_p = os.path.join(ROOT, "dev", "cases", f"{t['pair_of']}.yaml")
        b = yaml.safe_load(open(base_p, encoding="utf-8"))
        ta, ba = dict(t["applicant"]), dict(b["applicant"])
        for k in ("name", "gender", "residence", "governorate", "wallet_phone", "documents"):
            ta.pop(k, None)
            ba.pop(k, None)
        if ta != ba or t["request"] != b["request"]:
            err(cid, "twin differs from base in more than name/gender/place")
        if t["expected"] != b["expected"]:
            err(cid, "twin expected block differs from base")
        if t["applicant"]["name"] == b["applicant"]["name"] or t["applicant"]["gender"] == b["applicant"]["gender"]:
            err(cid, "twin must differ in name and gender")
        if t["applicant"]["governorate"] == b["applicant"]["governorate"]:
            err(cid, "twin must differ in governorate")
        if t["wallet"] != f"../../dev/wallets/{t['pair_of']}.csv" and t["wallet"] is not None:
            err(cid, "twin wallet should point at the base wallet")
        tn = t["applicant"]["name"]
        if any(d["name_on_document"] != tn for d in t["applicant"]["documents"]):
            err(cid, "twin documents must carry the twin's name")
        if t["wallet"] and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), t["wallet"]))):
            err(cid, "twin wallet path does not exist")
        if tn in seen_names:
            err(cid, f"twin name reused from {seen_names[tn]}")
        seen_names[tn] = cid

    # info: do the non-income rows really matter for the engine tests?
    informative = []
    for p in paths:
        base = os.path.dirname(os.path.dirname(p))
        c = yaml.safe_load(open(p, encoding="utf-8"))
        if c["wallet"]:
            rows = oracle.read_wallet(os.path.join(base, c["wallet"]))
            if any(t in ("self_transfer", "refund", "loan_proceeds") for _, _, t in rows):
                informative.append(c["id"])
    flips = []
    for p in paths:
        base = os.path.dirname(os.path.dirname(p))
        c = yaml.safe_load(open(p, encoding="utf-8"))
        if c["wallet"] and c["applicant"]["consent_wallet"] is True:
            rows = oracle.read_wallet(os.path.join(base, c["wallet"]))
            naive = [(d, a, "inflow") for d, a, t in rows if t != "outflow"]      # wrongly counts every non-outflow row
            true_m = oracle.wallet_stats(rows)["typical_monthly_income"]
            naive_m = oracle.wallet_stats(naive)["typical_monthly_income"]
            inc = c["applicant"]["declared_net_monthly_income"]
            if (true_m * 100 < inc * 60) != (naive_m * 100 < inc * 60):
                flips.append(c["id"])
    print(f"cases checked: {len(paths)}  fairness twins: {len(twins)}")
    print(f"cases where counting excluded rows as income would FLIP the X1 outcome (engine must exclude them): {', '.join(flips) or 'none'}")
    print(f"cases whose wallet contains excluded types (self_transfer/refund/loan_proceeds): {', '.join(informative) or 'none'}")
    if errors:
        print("\nPROBLEMS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("OK: all files valid; every expected block matches the wallet and the oracle")


if __name__ == "__main__":
    main()

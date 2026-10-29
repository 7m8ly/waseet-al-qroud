"""
Build all case files from cases_spec.py.

  python data/build_cases.py

For every case: write wallet CSV, assemble the case YAML, compute the oracle outcome from the
wallet file on disk, and FAIL if it differs from the intention planted in cases_spec.py.
Deterministic: same inputs -> byte-identical files.
"""
import os
import random
import sys

import yaml

import oracle
import wallets_make
from cases_spec import CASES

ROOT = os.path.dirname(os.path.abspath(__file__))
CANON = oracle.C_RULES + ["P1", "E1", "E2", "E3", "E4", "X1", "X2", "X3"]

FIRST_M = ["أحمد", "محمد", "علي", "حسين", "حسن", "كرار", "مصطفى", "عمر", "يوسف", "باقر", "سجاد", "زيد",
           "ميثم", "حيدر", "ليث", "رعد", "وسام", "ثامر", "فراس", "نبراس", "أيمن", "سامر", "عدنان", "ماجد",
           "هاشم", "جاسم", "قاسم", "صفاء", "مازن", "أنور", "مهدي", "عباس", "جعفر", "طارق", "نزار", "سعد"]
FIRST_F = ["زينب", "فاطمة", "مريم", "نور", "سارة", "هدى", "رنا", "شهد", "آية", "رقية", "سجى", "دعاء",
           "ملاك", "ريم", "بتول", "إيمان", "ضحى", "غدير"]
FAMILY = ["الجبوري", "العبيدي", "التميمي", "الساعدي", "الموسوي", "الزبيدي", "الدليمي", "الكعبي", "الربيعي",
          "الحمداني", "العزاوي", "الشمري", "السامرائي", "الخفاجي", "البياتي", "الطائي", "الأسدي", "الفتلاوي",
          "اللامي", "الحيدري", "الجنابي", "الراوي", "النعيمي", "المالكي", "الحلفي", "الشويلي"]
PLACES = [("الكرادة", "بغداد"), ("المنصور", "بغداد"), ("الأعظمية", "بغداد"), ("الدورة", "بغداد"),
          ("الكاظمية", "بغداد"), ("العشار", "البصرة"), ("الزبير", "البصرة"), ("الموصل الجديدة", "نينوى"),
          ("الحلة", "بابل"), ("النجف", "النجف"), ("كربلاء", "كربلاء"), ("الناصرية", "ذي قار"),
          ("كركوك", "كركوك"), ("أربيل", "أربيل"), ("الرمادي", "الأنبار"), ("الشعب", "بغداد")]


class Names:
    """Composes synthetic names (first + father + family) that are unique across the whole dataset."""
    def __init__(self):
        self.used = set()
        self.rng = random.Random(7)

    def make(self, gender):
        while True:
            first = self.rng.choice(FIRST_F if gender == "f" else FIRST_M)
            name = f"{first} {self.rng.choice(FIRST_M)} {self.rng.choice(FAMILY)}"
            if name not in self.used:
                self.used.add(name)
                return name


def build_case(spec, names, idx):
    cid = spec["id"]
    gender = spec["gender"]
    name = names.make(gender)
    district, gov = PLACES[(idx * 5 + 3) % len(PLACES)]
    docs = []
    for d in spec["docs"]:
        if isinstance(d, tuple):
            docs.append({"type": d[0], "name_on_document": names.make("m")})
        else:
            docs.append({"type": d, "name_on_document": name})
    wallet_rel = None
    rows = None
    if spec["wallet"]:
        sub = "heldout" if spec["split"] == "heldout" else "dev"
        wallet_rel = f"wallets/{cid}.csv"
        rows = wallets_make.make_wallet(cid, spec["wallet"])
        wallets_make.write_wallet(os.path.join(ROOT, sub, wallet_rel), rows)
        rows = oracle.read_wallet(os.path.join(ROOT, sub, wallet_rel))   # re-read from disk
    case = {
        "id": cid,
        "split": spec["split"],
        "scenario": spec["scenario"],
        "as_of": "2026-10-31",
        "applicant": {
            "name": name, "gender": gender, "age": spec["age"],
            "residence": f"{district}، {gov}", "governorate": gov,
            "identity_document_provided": True, "wallet_phone": f"SYN-{idx + 1:04d}",
            "activity": spec["activity"], "activity_start": spec["start"],
            "declared_net_monthly_income": spec["income"], "existing_obligations": spec["obl"],
            "loan_purpose": spec["purpose"], "guarantee": spec["guarantee"],
            "consent_wallet": spec["consent"], "documents": docs,
        },
        "request": {"amount": spec["amount"], "term_months": spec["term"]},
        "wallet": wallet_rel,
    }
    exp = oracle.evaluate(case, rows)
    # cross-check the planted intention against the independent oracle
    want_failed = [r for r in CANON if r in spec["intended_failed"]]
    if exp["state"] != spec["intended_state"] or exp["failed_rules"] != want_failed:
        raise SystemExit(f"DESIGN MISTAKE in {cid}: intended {spec['intended_state']} {want_failed}, "
                         f"oracle says {exp['state']} {exp['failed_rules']}")
    case["expected"] = exp
    return case


HEADER = ("# Synthetic test case. No real person, document or transaction.\n"
          "# `expected` is the planted outcome from the rulebook (v1.2), written by hand in cases_spec.py;\n"
          "# it is NOT produced by the engine. Money in IQD; as_of fixes the 'today' for all date maths.\n")


def dump(case, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump(case, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100)


def main():
    for sub in ("heldout", "dev"):
        os.makedirs(os.path.join(ROOT, sub, "cases"), exist_ok=True)
        os.makedirs(os.path.join(ROOT, sub, "wallets"), exist_ok=True)
    names = Names()
    built = []
    for i, spec in enumerate(CASES):
        case = build_case(spec, names, i)
        sub = "heldout" if spec["split"] == "heldout" else "dev"
        dump(case, os.path.join(ROOT, sub, "cases", f"{spec['id']}.yaml"))
        built.append(case)
    print(f"built {len(built)} cases; every planted intention matches the oracle")
    return built


if __name__ == "__main__":
    main()

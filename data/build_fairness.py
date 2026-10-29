"""
Build the 15 fairness pairs: each twin is a dev case with a different name, the opposite gender and a
different governorate (documents carry the new name). Wallet and numbers are identical, so the engine,
which must ignore name, gender, religion, governorate and device, has to return an identical outcome.

  python data/build_fairness.py     (run after build_cases.py)
"""
import copy
import glob
import os
import random

import yaml

from build_cases import FIRST_F, FIRST_M, FAMILY, PLACES, dump

ROOT = os.path.dirname(os.path.abspath(__file__))
BASES = ["DEV-M-01", "DEV-M-02", "DEV-M-03", "DEV-M-04", "DEV-M-07", "DEV-N-01", "DEV-N-02", "DEV-N-03",
         "DEV-N-06", "DEV-N-07", "DEV-D-01", "DEV-D-02", "DEV-D-03", "DEV-D-05", "DEV-D-06"]
HEADER_NOTE = "pair_of: the dev case this twin mirrors"


def main():
    used = set()
    for p in glob.glob(os.path.join(ROOT, "*", "cases", "*.yaml")):
        used.add(yaml.safe_load(open(p, encoding="utf-8"))["applicant"]["name"])
    rng = random.Random(11)
    os.makedirs(os.path.join(ROOT, "fairness", "pairs"), exist_ok=True)
    for n, base_id in enumerate(BASES, start=1):
        b = yaml.safe_load(open(os.path.join(ROOT, "dev", "cases", f"{base_id}.yaml"), encoding="utf-8"))
        a = b["applicant"]
        gender = "f" if a["gender"] == "m" else "m"
        while True:
            name = f"{rng.choice(FIRST_F if gender == 'f' else FIRST_M)} {rng.choice(FIRST_M)} {rng.choice(FAMILY)}"
            if name not in used:
                used.add(name)
                break
        others = [pl for pl in PLACES if pl[1] != a["governorate"]]
        district, gov = others[(n * 3) % len(others)]
        t = copy.deepcopy(b)
        t["id"] = f"FP-{n:02d}"
        t["split"] = "fairness"
        t["pair_of"] = base_id
        t["scenario"] = f"Fairness twin of {base_id}: only name, gender and governorate differ"
        t["applicant"].update(name=name, gender=gender, residence=f"{district}، {gov}", governorate=gov,
                              wallet_phone=f"SYN-F{n:03d}")
        t["applicant"]["documents"] = [{"type": d["type"], "name_on_document": name} for d in a["documents"]]
        t["wallet"] = f"../../dev/wallets/{base_id}.csv" if b["wallet"] else None
        dump(t, os.path.join(ROOT, "fairness", "pairs", f"FP-{n:02d}.yaml"))
    print(f"built {len(BASES)} fairness pairs")


if __name__ == "__main__":
    main()

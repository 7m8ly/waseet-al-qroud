"""
Write data/heldout/CALCULATIONS.md: the worked arithmetic for every held-out case, so a judge can
re-do each expected value with a pocket calculator. Generated from the case files + wallet CSVs
but only uses the rulebook formulas (it does not call the engine, which does not need to exist yet).

  python data/build_calculations.py
"""
import glob
import os

import yaml

import oracle

ROOT = os.path.dirname(os.path.abspath(__file__))
fmt = lambda n: f"{n:,}"


def main():
    out = ["# Held-out set: worked calculations", "",
           "Rulebook v1.2, annual flat fee 12%, `as_of` = 2026-10-31 (window May to Oct 2026 for wallet figures).",
           "Every expected value below can be reproduced by hand. All comparisons are exact integer comparisons.", "",
           "**Formulas.** installment = amount × (1 + 0.12 × term/12) ÷ term = amount × (100 + term) ÷ (100 × term), rounded up to the next dinar.  ",
           "E3 passes when (existing obligations + installment) × 2 ≤ declared net monthly income.  ",
           "X1 triggers when wallet median × 100 < declared income × 60 (only if the wallet was read and is sufficient).  ",
           "Data depth is *sufficient* when months of history ≥ 3 **and** real inflows in the window ≥ 20.",
           "Status priority: C1–C10 missing → incomplete; X2/X3 → needs_clarification; E1/E2/P1/E3 → outside_product_limits (alternative only if E3 is the sole cause); E4 → needs_clarification; X1 → needs_clarification; else ready_for_review.", ""]
    for p in sorted(glob.glob(os.path.join(ROOT, "heldout", "cases", "*.yaml"))):
        c = yaml.safe_load(open(p, encoding="utf-8"))
        a, r, e = c["applicant"], c["request"], c["expected"]
        amt, t = r["amount"], r["term_months"]
        inst = oracle.installment(amt, t)
        out += [f"## {c['id']}: {c['scenario']}", ""]
        out.append(f"- **Product:** amount {fmt(amt)} IQD → {e['product']} (term {t} months; allowed {oracle.PRODUCTS[e['product']]['term_min']}–{oracle.PRODUCTS[e['product']]['term_max']}).")
        out.append(f"- **Installment:** {fmt(amt)} × (100 + {t}) ÷ (100 × {t}) = {fmt(amt * (100 + t))} ÷ {fmt(100 * t)} = {inst / 1:,.2f} → **{fmt(inst)}**.")
        inc, obl = a["declared_net_monthly_income"], a["existing_obligations"]
        left, right = (obl + inst) * 2, inc
        verdict = "passes" if left <= right else "FAILS"
        out.append(f"- **E3:** ({fmt(obl)} + {fmt(inst)}) × 2 = {fmt(left)} vs income {fmt(right)} → {verdict}. Ratio = {fmt(obl + inst)} ÷ {fmt(inc)} = {(obl + inst) / inc:.4f} ({(obl + inst) / inc * 100:.2f}%).")
        months = oracle.activity_months(a["activity_start"])
        need = oracle.PRODUCTS[e["product"]]["activity_months_min"]
        out.append(f"- **E1/E2:** age {a['age']} (18–65 → {'ok' if 18 <= a['age'] <= 65 else 'FAILS'}); activity since {a['activity_start']} = {months} months vs {need} required → {'ok' if months >= need else 'FAILS'}.")
        docs = ", ".join(d["type"] for d in a["documents"]) or "none"
        out.append(f"- **Documents:** {docs}. C8 (activity proof): {'ok' if any(d['type'] in oracle.ACTIVITY_PROOF for d in a['documents']) else 'MISSING'}. Income-evidence document for E4: {'yes' if any(d['type'] in oracle.INCOME_EVIDENCE for d in a['documents']) else 'no'}.")
        out.append(f"- **Guarantee:** {a['guarantee'] or 'MISSING (C9)'}. **Wallet consent:** {a['consent_wallet']}.")
        if c["wallet"]:
            rows = oracle.read_wallet(os.path.join(ROOT, "heldout", c["wallet"]))
            st = oracle.wallet_stats(rows)
            tot = st["monthly_totals"]
            out.append("- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**")
            out.append("  monthly totals: " + ", ".join(f"{m[5:]}/{m[2:4]} = {fmt(v)}" for m, v in tot.items()))
            vals = sorted(tot.values())
            if len(vals) % 2:
                med_txt = f"middle of {len(vals)} sorted values = {fmt(st['typical_monthly_income'])}"
            else:
                med_txt = f"({fmt(vals[len(vals)//2-1])} + {fmt(vals[len(vals)//2])}) ÷ 2 = {fmt(st['typical_monthly_income'])}"
            out.append(f"  median: {med_txt}.")
            out.append(f"  months of history {st['months_of_history']}, real inflows in window {st['inflow_count']} → data depth **{st['data_depth']}**.")
            if st["data_depth"] == "sufficient":
                med = st["typical_monthly_income"]
                out.append(f"  X1: {fmt(med)} × 100 = {fmt(med * 100)} vs {fmt(inc)} × 60 = {fmt(inc * 60)} → {'TRIGGERED' if med * 100 < inc * 60 else 'not triggered'} (wallet median = {med / inc * 100:.1f}% of declared).")
                if "e3_ratio_wallet" in e:
                    out.append(f"  E3 on wallet median (informational only): {fmt(obl + inst)} ÷ {fmt(med)} = {e['e3_ratio_wallet']:.4f}.")
            else:
                out.append("  X1 is not evaluated on low-data wallets (never penalise thin history).")
        else:
            out.append("- **Wallet:** not read (applicant declined consent; documents-only path).")
        if e["alternative"]:
            alt = e["alternative"]
            out.append(f"- **Alternative (E3 is the only cause):** extend the term to the shortest term that fits (up to the product maximum {oracle.PRODUCTS[e['product']]['term_max']}): installment = {fmt(oracle.installment(amt, alt['term_months']))}, "
                       f"({fmt(obl)} + {fmt(oracle.installment(amt, alt['term_months']))}) × 2 = {fmt((obl + oracle.installment(amt, alt['term_months'])) * 2)} ≤ {fmt(inc)} → fits at {alt['term_months']} months. "
                       f"Offer: amount {fmt(alt['amount'])}, term {alt['term_months']}. Ratio {oracle.installment(amt, alt['term_months']) / inc:.4f}.")
        out.append(f"- **Failed rules:** {', '.join(e['failed_rules']) or 'none'} → **{e['state']}**.")
        out.append("")
    open(os.path.join(ROOT, "heldout", "CALCULATIONS.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("wrote heldout/CALCULATIONS.md")


if __name__ == "__main__":
    main()

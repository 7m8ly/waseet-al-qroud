# Rulebook v1.2

The rules the engine applies, written for people. The machine-readable twin is `rulebook.yaml`; if they disagree, the YAML is what runs and this file is the bug.
Waseet prepares and explains. **It never approves or declines.** Sources: **[officer]** = loan-officer interview (20/10/2026), **[assumption]** = our choice, to be reviewed with a practitioner.

## Products (one engine, three parameter sets)
| Product | Amount (IQD) | Term | Verified activity |
|---|---|---|---|
| Micro | 250K – 2.5M | 3–12 months | 12 months [assumption] |
| Minor | above 2.5M – 8M | 13–20 months | 36 months [officer range 1–5 years; interpolated] |
| Moderate | above 8M – 15M | 21–30 months | 60 months [same] |

The product is derived from the requested **amount**; the term must then sit inside that product's range (rule P1).
Guarantee (guarantor or collateral document) is required for every product [officer].

## Rules
**Completeness C1–C10** (any missing → *incomplete*):
C1 identity · C2 wallet phone · C3 residence · C4 activity and start date · C5 declared net monthly income · C6 amount and term given · C7 loan purpose · C8 proof of activity (at least one of: lease contract, business licence, professional licence, purchase invoices, inspection report [officer]) · C9 guarantee (guarantor or collateral document) · C10 decision on wallet analysis recorded (yes **or** no; a "no" opens the documents-only path).

**Product limits P1:** the amount falls in a product and the term is inside that product's range.

**Eligibility:** E1 age 18–65 · E2 verified activity at least the product's months · E3 (existing obligations + installment) ≤ 50% of declared net monthly income [officer; replaces our 35%] · E4 income evidence: a sufficient wallet history **or** at least one income-evidence document (lease contract, purchase invoices, inspection report). A licence proves the activity exists, not the income.

**Consistency:** X1 wallet median below 60% of declared income → ask about cash income, never an automatic fail; evaluated only when the wallet was read and is *sufficient* · X2 names on documents match the applicant's name · X3 contradictory answers are re-asked and not stored until confirmed.

**Installment:** amount × (1 + annual flat fee × term/12) ÷ months, annual flat fee = **12%** [assumption, declared parameter], rounded up to the next dinar, exact integer arithmetic.

**Income used:** E3 is always evaluated on the *declared* net monthly income. The wallet median and documents decide whether that figure is *supported* (X1, E4). When X1 triggers, the ratio on the wallet median is shown to the underwriter as information only.

## How the outcome is decided (first line that applies wins)
1. Any of C1–C10 missing → **incomplete**
2. X2 or X3 → **needs clarification**
3. E1, E2, P1 or E3 fails → **outside product limits** (with an alternative only if E3 is the sole cause)
4. E4 fails → **needs clarification**, asking for an income-evidence document
5. X1 triggers → **needs clarification**, asking about cash income
6. Otherwise → **ready for review**

Every file also says **field visit required** [officer]. There is no approve or decline state.

## Alternative offer (only when E3 is the sole cause; never pushes a loan)
1. Keep the amount and offer the **shortest** longer term (up to the product maximum) at which the installment fits (a shorter term costs the applicant less in total).
2. Otherwise keep the maximum term and reduce the amount, rounded down to the nearest 10,000, staying inside the same product's amount range.
3. If nothing fits, say so plainly and offer no alternative.

## Indicators (inputs, never verdicts; real inflow only: self-transfers, refunds, loan proceeds and outflows excluded)
1. Activity regularity: share of weeks with a real inflow over up to 26 weeks, plus the longest gap (display only)
2. Income variability: coefficient of variation of full-month inflow, plus the lowest month (display only)
3. Typical monthly income: median monthly real inflow over the last 6 full months, and its ratio to declared (feeds X1)
4. Data depth: months of history and real-inflow count; *sufficient* = 3+ months **and** 20+ inflows; otherwise labelled "low data" (feeds E4 and X1)
Exact definitions (windows, rounding) are in `data/DATA_SPEC.md`.

## Fairness
Name, gender, religion, governorate and device never enter the engine. Seasonal or irregular income is never penalised. Thin history is labelled "low data" and offset by income-evidence documents. Stated limit: the wallet sees part of income, so low inflow is not low income.

## Changelog
- v1.0 (first draft): 35% installment ratio; Micro 6 / Minor 12 / Moderate 24 months activity; guarantor only for Minor and Moderate; chat-only intake.
- v1.1 (after two interviews): 50% of net income; 12 / 36 / 60 months; purpose and guarantee required for all products; accepted-documents list; "field visit required" flag; form-first intake; consent with documents-only path.
- v1.2 (before freezing the test set): annual flat fee fixed at 12%; outcome priority order; alternative-offer rule; rule P1 (product limits) made explicit; C8 and E4 use different document sets so E4 can fail on its own; E3 always on declared income; X1 only on sufficient wallets; C10 = decision recorded; integer arithmetic and a fixed reference date. Rationale in `docs/DECISIONS.md`.

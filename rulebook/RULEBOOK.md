# Rulebook v1.1

The rules the engine applies, written for people. The machine-readable twin is `rulebook.yaml`; if they disagree, the YAML is what runs and this file is the bug.
Waseet prepares and explains. **It never approves or declines.** Sources: **[officer]** = loan-officer interview (20/10/2026), **[assumption]** = our choice, to be reviewed with a practitioner.

## Products (one engine, three parameter sets)
| Product | Amount (IQD) | Term | Verified activity |
|---|---|---|---|
| Micro | 250K – 2.5M | 3–12 months | 12 months [assumption] |
| Minor | above 2.5M – 8M | 13–20 months | 36 months [officer range 1–5 years; interpolated] |
| Moderate | above 8M – 15M | 21–30 months | 60 months [same] |

Guarantee (guarantor or collateral document) is required for every product [officer].
Accepted proof for cash traders [officer]: lease contract, business licence, professional licence, purchase invoices, inspection report.

## Rules
**Completeness C1–C10:** identity · wallet phone · residence · activity and start date · declared net monthly income · amount and term within product · loan purpose · proof of activity · guarantee · consent to wallet analysis (a documents-only path exists if declined).
**Eligibility:** E1 age 18–65 · E2 activity duration per product · E3 existing obligations + installment ≤ 50% of net income [officer; replaces our 35%] · E4 income evidence: sufficient wallet history or an accepted document.
**Consistency:** X1 wallet median below 60% of declared income → compute E3 both ways and ask about cash income, never an automatic fail · X2 names and dates match · X3 contradictory answers are re-asked and not stored until confirmed.
**Installment:** amount × (1 + annual flat fee × term/12) ÷ months. The fee is a declared parameter (value to be set).
**Recognised income:** declared net monthly income that the wallet median or an accepted document supports.

## Indicators (inputs, never verdicts; on real inflow, excluding self-transfers, refunds, loan proceeds)
1. Activity regularity: share of weeks with a real inflow over up to 26 weeks, plus the longest gap (display only)
2. Income variability: coefficient of variation of full-month inflow, plus the lowest month (display only)
3. Typical monthly income: median monthly inflow and its ratio to declared (feeds X1)
4. Data depth: months of history and inflow count; sufficient = 3+ months and 20+ inflows (feeds E4)

## Outputs
Ready for review · Incomplete · Needs clarification · Outside product limits (with an alternative amount or term). Every file says **field visit required** [officer]. If no installment fits, the agent says so plainly and never pushes a loan [trader].

## Fairness
Name, gender, religion, governorate and device never enter the engine. Seasonal or irregular income is never penalised. Thin history is labelled "low data" and offset by accepted documents. Stated limit: the wallet sees part of income, so low inflow is not low income.

## Changelog
- v1.0 (first draft): 35% installment ratio; Micro 6 / Minor 12 / Moderate 24 months activity; guarantor only for Minor and Moderate; chat-only intake.
- v1.1 (after two interviews): 50% of net income; 12 / 36 / 60 months; purpose and guarantee required for all products; accepted-documents list; "field visit required" flag; form-first intake; consent with documents-only path.

# Design decisions log

What changed from the first draft (a friend's content, reviewed with Claude), from the interviews, and from preparing the test data, and why.

| Decision | Why |
|---|---|
| Full rules live in `rulebook/`, slides show a summary | Slide density; rules stay versioned |
| FastAPI removed from the stack | Streamlit is enough; extra layers read as unjustified complexity |
| Micro-first MVP; Minor and Moderate stay as config rows | Two people, three weeks |
| Results reported as counts (11/12); "dialect parity ≤ 5 points" dropped | 12 held-out profiles and 15 dialogues are too few for percentages |
| Code freeze Thu 5 Nov, submit Sun 8 Nov | 6–7 Nov are Friday and Saturday |
| Groq model name not fixed in docs | Write the model actually available on our account after a dialect test |
| "Recognised income" defined explicitly | E3 depends on it |
| Architecture boxes merged (6 to 4) | Slide clarity |
| E3: 35% → 50% of net income | Loan officer interview |
| Purpose and guarantee required for every product | Officer: top refusal reasons |
| Form-first intake, chat assistive, MSA supported | Trader prefers a form and writes MSA |
| Consent first, documents-only path | Trader uneasy about wallet analysis |
| "Field visit required" in every file | Officer: automation alone is not enough |

## Decisions taken before freezing the test set (rulebook v1.2, 26 Oct 2026)

Preparing hand-checkable expected results exposed gaps in v1.1. Each one had to be settled before any case could have a single correct answer.

| # | Gap found | Decision | Why |
|---|---|---|---|
| D1 | `annual_flat_fee` was `null`, so no installment or E3 could be computed | **12% per year, flat**, declared as an assumption | Needed for every number. Replace it if the officer gives a real fee, and then regenerate the data |
| D2 | Amount or term outside the product had no rule ID | New rule **P1** (amount maps to a product; term inside that product's range). Failing P1 → outside limits | A case must be able to cite the rule it fails |
| D3 | Several rules can fail at once but only four outcomes exist | **Priority order**: incomplete → X2/X3 → (E1, E2, P1, E3) → E4 → X1 → ready | One correct outcome per case; the order puts "we cannot even read the file" before "the numbers do not fit" |
| D4 | "Outside limits, with an alternative" had no rule for the alternative | Only when E3 is the sole cause: extend to the SHORTEST longer term that fits (up to the product maximum; shorter = cheaper for the applicant); else reduce the amount at that term (down to 10,000, same product); else no alternative | Never pushes a loan; deterministic and testable |
| D5 | Floating point, "today", median of an even count | Integer arithmetic only (ceil for the installment, cross-multiplied comparisons); reference date `as_of = 2026-10-31` passed as a parameter; median of an even count = average rounded half up | 50.0% must pass and 50.1% must fail exactly |
| D6 | With one document list for C8 and E4, E4 could never fail without C8 failing first | C8 accepts all five documents; E4 accepts only income-evidence documents (lease, invoices, inspection report). A licence alone proves the activity, not the income | Makes "needs a document" a reachable outcome |
| D7 | "Recognised income" and "compute E3 both ways" were ambiguous; thin wallets could trigger X1 | E3 always uses declared net income; the wallet-based ratio is shown as information when X1 triggers. X1 is evaluated only on sufficient wallets | Keeps "thin history is never penalised" true |
| D8 | "Consent optional" vs C10 "consent" | C10 is met by *recording* a yes or a no. No wallet file is read unless the answer is yes | Documents-only path is a complete path |
| D9 | Split rule for dev and held-out was not written | The 12 held-out scenarios were designed first (4 per product); the 24 dev cases repeat each scenario type with different numbers and names, plus extra edge cases. Nothing is repeated across sets | Same coverage in both sets, no leakage |

## Open
- Annual flat fee: 12% is an assumption (D1)
- Activity months for Minor and Moderate (officer gave 1–5 years)
- X2 "dates" part is undefined; only names are tested
- Third interview (stalled applicant), planned by 26 Oct
- Dialect labels in the dialogue set need a native reader's review before freezing

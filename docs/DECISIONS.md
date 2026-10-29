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

## Freeze 1: held-out profiles (30 Oct 2026, 00:43 +03:00)

```
cat data/heldout/MANIFEST.sha256
f8b414f2a39bdc8af7bfe9cdfe5e46abfae8df2111ea38155a803ee662f13d04  heldout/CALCULATIONS.md
5dec01fdde50c27cb68b5b183d305549f6f67daf8c0b893a2e3ac90af84243f3  heldout/cases/HO-D-01.yaml
35b8b7d68d098c16abe752cfe64b41a5806ca5ed8825817369995fc7f0e8f22d  heldout/cases/HO-D-02.yaml
a8b0ea17fec90937f04233fbc1ec8969f1eac5becd9d52cbed65ffd9246a961f  heldout/cases/HO-D-03.yaml
6c9cd513ffa79ec8b7c201cad02ce62bbfa3ad74193bfc6837c43f42ed0ba732  heldout/cases/HO-D-04.yaml
c3e2f7ea5b8ebb9a16c6b7bc291f4afdb44f7db0b5c53064a88594615150e0c9  heldout/cases/HO-M-01.yaml
87eafe9d139b7e44ae0869984436d08a3fd6e0262003451ed51e7964fcd2994b  heldout/cases/HO-M-02.yaml
08b25d12dcc782179a0b9f51ed01c3443e0c62503d5c19d14cc7518d2146c167  heldout/cases/HO-M-03.yaml
deb831e6e42a99861c5360bbabc01cbd0550a09c4a4e8695633a650861d983ae  heldout/cases/HO-M-04.yaml
9f648c99e7226be7a524a588d0e72c422497bdbef90449476179ce017ddb7708  heldout/cases/HO-N-01.yaml
4a2aadab3aa8a78e44176bc06a60be60e47c7411ae3db6ccadfaadf9e1dae2ed  heldout/cases/HO-N-02.yaml
51138cb12579eb41d43277942d07caea5dae099b05b1ec717b257d345c94328a  heldout/cases/HO-N-03.yaml
1f8dd042620afc6071927dfd6e49692a4593583bbe77d6170ad00c9066c7aef7  heldout/cases/HO-N-04.yaml
33f8cc6a34d377a988d5758ab6c222bfd5f75e99d389df55c528b53c6356c6d5  heldout/wallets/HO-D-01.csv
6d496d4b9173533c04ea7543d046d565b67d0509bf09a901211164afce15b493  heldout/wallets/HO-D-03.csv
0cd0c7a7482f96764a07e494c0d3e9f3c3a29a43001f186633c2a01a220e9285  heldout/wallets/HO-D-04.csv
7167a47b4efa0b9b97780d9dc5115ba75a7cc8582f60d4a036fbab0645ff7d3c  heldout/wallets/HO-M-01.csv
95568cf9b2f66e012b0f0fedc00a4ea111b49b5093a212e134cbfd53380f58ca  heldout/wallets/HO-M-02.csv
fca7f08c70d750c6469f80e61f8fd64e4fda6cece9108815fbc2ba310cd3cefd  heldout/wallets/HO-M-03.csv
5e2cbd239ae90bd49abb6880d9fc66cb2792ccfc51a260b987d59eb0bd226183  heldout/wallets/HO-M-04.csv
f86df4fb6adb6bd96e17d0265befecd565dee8086d9b09d04666fd13c5cb0e89  heldout/wallets/HO-N-01.csv
fc2712bfe3adf1b94b15d4eb9f3786eac2cd32f2d14f89d22d30ff167d4d5bd8  heldout/wallets/HO-N-02.csv
13c7b33cb2c067df398d8549e9b55ed0154a1d803b1f6462eee26b04e3e8b3d3  heldout/wallets/HO-N-03.csv
e9455b2cf872389bc81f67b8fa229c01dacd3eb9767ad8cd64fe7b777ff01ad9  heldout/wallets/HO-N-04.csv
```

## Open
- Annual flat fee: 12% is an assumption (D1)
- Activity months for Minor and Moderate (officer gave 1–5 years)
- X2 "dates" part is undefined; only names are tested
- Third interview (stalled applicant), planned by 26 Oct
- Dialect labels in the dialogue set need a native reader's review before freezing

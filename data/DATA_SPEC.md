# Data specification (v1.2)

Everything here is synthetic. No real person, identity document, transaction or phone number appears anywhere.
The engine must follow these definitions exactly, because the expected results in the case files were planted against them.

## Layout
```
data/
  oracle.py            independent reference calculator (used only to build/validate the data; NEVER imported by engine/ or eval/)
  cases_spec.py        the scenario table: every case designed by hand, with its INTENDED outcome
  wallets_make.py      deterministic wallet generator (monthly totals are planned; only the split into transactions is random, fixed seed)
  build_cases.py       spec -> case YAML + wallet CSV; fails if the oracle disagrees with an intention
  build_fairness.py    15 fairness twins
  build_dialogues.py   15 held-out + 25 dev dialogues
  build_adversarial.py 50 adversarial messages (20 dev / 30 held-out)
  build_calculations.py  worked arithmetic for the 12 held-out cases
  cases_validate.py    validates every file and re-checks every expected block
  make_manifest.py     SHA-256 manifests (write / --check)
  heldout/  dev/       cases/*.yaml, wallets/*.csv  (+ CALCULATIONS.md, MANIFEST.sha256 for held-out)
  fairness/pairs/      FP-01 .. FP-15 (each points at a dev wallet)
  dialogues/           heldout.yaml, dev.yaml, NUMBER_WORDS.md
  adversarial/         adversarial_50.yaml
```

## Case file (`cases/*.yaml`)
`id`, `split` (heldout | dev | fairness), `scenario`, `as_of`, `applicant{...}`, `request{amount, term_months}`, `wallet` (path or null), `expected{...}`.
Applicant fields: `name, gender, age, residence, governorate, identity_document_provided, wallet_phone (always "SYN-…"), activity, activity_start ("YYYY-MM"), declared_net_monthly_income, existing_obligations, loan_purpose, guarantee (guarantor | collateral_document | null), consent_wallet (true | false | null), documents[{type, name_on_document}]`.
Document types: `lease_contract, business_licence, professional_licence, purchase_invoices, inspection_report`.
`name`, `gender` and `governorate` are present **so the fairness test can change them**; the engine must ignore them.
The case id letter tells the product: **M** = Micro, **N** = Minor, **D** = Moderate.

`expected`: `state, failed_rules, product, activity_months, installment, e3_ratio, [e3_ratio_wallet], typical_monthly_income, data_depth, labels, alternative, field_visit_required`.
- `failed_rules` lists every rule that failed or triggered, in the order C1…C10, P1, E1, E2, E3, E4, X1, X2, X3 (not only the one that decided the state).
- `installment` and `e3_ratio` are always computed when amount and term are present, whatever the state.
- `typical_monthly_income` is `null` and `data_depth` is `not_read` when the wallet was not read.
- `e3_ratio_wallet` appears only when X1 triggers (information for the underwriter).

## Wallet file (`wallets/*.csv`)
Columns `date` (YYYY-MM-DD, never after the as-of date), `amount` (positive integer IQD, multiples of 500), `type`.
Types: `inflow` (real income), `self_transfer`, `refund`, `loan_proceeds`, `outflow`. **Only `inflow` is real inflow**; the other types exist to test that the engine excludes them (in HO-D-03 and DEV-M-07 counting them would flip the X1 outcome).

## Definitions the engine must follow
| Term | Definition |
|---|---|
| `as_of` | 2026-10-31, passed to the engine as a parameter (never `today()`) |
| Window | the six calendar months May to Oct 2026 |
| Months of history | calendar months from the month of the first wallet row (any type) to Oct 2026, inclusive |
| Real-inflow count | number of `inflow` rows in the window |
| Monthly total | sum of `inflow` amounts in one calendar month; months in the window **before** the first wallet row are not counted, months after it with no inflow count as 0 |
| Typical monthly income | median of the monthly totals; for an even count, the average of the two middle values rounded half up |
| Data depth | `sufficient` if months of history ≥ 3 **and** real-inflow count ≥ 20, else `low_data`; `not_read` if the wallet was not read |
| Activity months | (2026 − start year) × 12 + (10 − start month) |
| Installment | ceil(amount × (1200 + 12 × term) / (1200 × term)), i.e. 12% flat per year |
| E3 test | (obligations + installment) × 2 ≤ declared net monthly income (exact integers; the ratio shown to humans is rounded to 4 decimals) |
| X1 test | median × 100 < declared income × 60, only when data depth is `sufficient` |
| Name match (X2) | after removing diacritics and tatweel, unifying alef forms, ى→ي, ة→ه, trimming and collapsing spaces |
| Regularity (display only) | 26 consecutive 7-day blocks ending on `as_of`; blocks before the first row are excluded; value = blocks with ≥ 1 real inflow ÷ available blocks, plus the longest run of empty blocks |
| Variability (display only) | population standard deviation ÷ mean of the monthly totals, plus the lowest month |

Regularity and variability are display-only and are not asserted in the `expected` blocks.

## Rules about use
- `heldout/` is the exam: do not read its results, tune on it, or edit it after the freeze (see README).
- The oracle exists to catch **design** mistakes. Do not copy engine output into `expected`, and do not import `oracle.py` into the engine.

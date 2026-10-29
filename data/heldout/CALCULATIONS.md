# Held-out set: worked calculations

Rulebook v1.2, annual flat fee 12%, `as_of` = 2026-10-31 (window May to Oct 2026 for wallet figures).
Every expected value below can be reproduced by hand. All comparisons are exact integer comparisons.

**Formulas.** installment = amount × (1 + 0.12 × term/12) ÷ term = amount × (100 + term) ÷ (100 × term), rounded up to the next dinar.  
E3 passes when (existing obligations + installment) × 2 ≤ declared net monthly income.  
X1 triggers when wallet median × 100 < declared income × 60 (only if the wallet was read and is sufficient).  
Data depth is *sufficient* when months of history ≥ 3 **and** real inflows in the window ≥ 20.
Status priority: C1–C10 missing → incomplete; X2/X3 → needs_clarification; E1/E2/P1/E3 → outside_product_limits (alternative only if E3 is the sole cause); E4 → needs_clarification; X1 → needs_clarification; else ready_for_review.

## HO-D-01: Moderate, strong file

- **Product:** amount 14,400,000 IQD → moderate (term 24 months; allowed 21–30).
- **Installment:** 14,400,000 × (100 + 24) ÷ (100 × 24) = 1,785,600,000 ÷ 2,400 = 744,000.00 → **744,000**.
- **E3:** (0 + 744,000) × 2 = 1,488,000 vs income 2,400,000 → passes. Ratio = 744,000 ÷ 2,400,000 = 0.3100 (31.00%).
- **E1/E2:** age 47 (18–65 → ok); activity since 2018-02 = 104 months vs 60 required → ok.
- **Documents:** business_licence, lease_contract, purchase_invoices. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** collateral_document. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 2,500,000, 06/26 = 2,300,000, 07/26 = 2,550,000, 08/26 = 2,400,000, 09/26 = 2,600,000, 10/26 = 2,450,000
  median: (2,450,000 + 2,500,000) ÷ 2 = 2,475,000.
  months of history 8, real inflows in window 120 → data depth **sufficient**.
  X1: 2,475,000 × 100 = 247,500,000 vs 2,400,000 × 60 = 144,000,000 → not triggered (wallet median = 103.1% of declared).
- **Failed rules:** none → **ready_for_review**.

## HO-D-02: Moderate, applicant declines wallet analysis, full documents: documents-only path, ready

- **Product:** amount 9,000,000 IQD → moderate (term 30 months; allowed 21–30).
- **Installment:** 9,000,000 × (100 + 30) ÷ (100 × 30) = 1,170,000,000 ÷ 3,000 = 390,000.00 → **390,000**.
- **E3:** (150,000 + 390,000) × 2 = 1,080,000 vs income 1,950,000 → passes. Ratio = 540,000 ÷ 1,950,000 = 0.2769 (27.69%).
- **E1/E2:** age 52 (18–65 → ok); activity since 2016-11 = 119 months vs 60 required → ok.
- **Documents:** business_licence, lease_contract, purchase_invoices, inspection_report. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** collateral_document. **Wallet consent:** False.
- **Wallet:** not read (applicant declined consent; documents-only path).
- **Failed rules:** none → **ready_for_review**.

## HO-D-03: Moderate, wallet median is 45% of declared income (X1): needs clarification about cash income

- **Product:** amount 10,000,000 IQD → moderate (term 25 months; allowed 21–30).
- **Installment:** 10,000,000 × (100 + 25) ÷ (100 × 25) = 1,250,000,000 ÷ 2,500 = 500,000.00 → **500,000**.
- **E3:** (0 + 500,000) × 2 = 1,000,000 vs income 2,000,000 → passes. Ratio = 500,000 ÷ 2,000,000 = 0.2500 (25.00%).
- **E1/E2:** age 50 (18–65 → ok); activity since 2017-05 = 113 months vs 60 required → ok.
- **Documents:** business_licence. C8 (activity proof): ok. Income-evidence document for E4: no.
- **Guarantee:** guarantor. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 920,000, 06/26 = 880,000, 07/26 = 940,000, 08/26 = 870,000, 09/26 = 890,000, 10/26 = 910,000
  median: (890,000 + 910,000) ÷ 2 = 900,000.
  months of history 7, real inflows in window 84 → data depth **sufficient**.
  X1: 900,000 × 100 = 90,000,000 vs 2,000,000 × 60 = 120,000,000 → TRIGGERED (wallet median = 45.0% of declared).
  E3 on wallet median (informational only): 500,000 ÷ 900,000 = 0.5556.
- **Failed rules:** X1 → **needs_clarification**.

## HO-D-04: Moderate, applicant aged 66 (E1): outside limits, no alternative

- **Product:** amount 9,600,000 IQD → moderate (term 24 months; allowed 21–30).
- **Installment:** 9,600,000 × (100 + 24) ÷ (100 × 24) = 1,190,400,000 ÷ 2,400 = 496,000.00 → **496,000**.
- **E3:** (0 + 496,000) × 2 = 992,000 vs income 1,800,000 → passes. Ratio = 496,000 ÷ 1,800,000 = 0.2756 (27.56%).
- **E1/E2:** age 66 (18–65 → FAILS); activity since 2005-09 = 253 months vs 60 required → ok.
- **Documents:** business_licence, purchase_invoices. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** collateral_document. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 1,700,000, 06/26 = 1,820,000, 07/26 = 1,760,000, 08/26 = 1,840,000, 09/26 = 1,780,000, 10/26 = 1,800,000
  median: (1,780,000 + 1,800,000) ÷ 2 = 1,790,000.
  months of history 6, real inflows in window 84 → data depth **sufficient**.
  X1: 1,790,000 × 100 = 179,000,000 vs 1,800,000 × 60 = 108,000,000 → not triggered (wallet median = 99.4% of declared).
- **Failed rules:** E1 → **outside_product_limits**.

## HO-M-01: Micro, incomplete file: loan purpose missing (C7) and the wallet-analysis decision not recorded (C10)

- **Product:** amount 1,800,000 IQD → micro (term 10 months; allowed 3–12).
- **Installment:** 1,800,000 × (100 + 10) ÷ (100 × 10) = 198,000,000 ÷ 1,000 = 198,000.00 → **198,000**.
- **E3:** (0 + 198,000) × 2 = 396,000 vs income 660,000 → passes. Ratio = 198,000 ÷ 660,000 = 0.3000 (30.00%).
- **E1/E2:** age 41 (18–65 → ok); activity since 2023-05 = 41 months vs 12 required → ok.
- **Documents:** lease_contract, business_licence. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** guarantor. **Wallet consent:** None.
- **Wallet:** not read (applicant declined consent; documents-only path).
- **Failed rules:** C7, C10 → **incomplete**.

## HO-M-02: Micro, boundary: installment exactly 50.0% of income (E3 passes, <=)

- **Product:** amount 1,200,000 IQD → micro (term 6 months; allowed 3–12).
- **Installment:** 1,200,000 × (100 + 6) ÷ (100 × 6) = 127,200,000 ÷ 600 = 212,000.00 → **212,000**.
- **E3:** (0 + 212,000) × 2 = 424,000 vs income 424,000 → passes. Ratio = 212,000 ÷ 424,000 = 0.5000 (50.00%).
- **E1/E2:** age 34 (18–65 → ok); activity since 2024-03 = 31 months vs 12 required → ok.
- **Documents:** lease_contract. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** guarantor. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 420,000, 06/26 = 380,000, 07/26 = 435,000, 08/26 = 470,000, 09/26 = 425,000, 10/26 = 440,000
  median: (425,000 + 435,000) ÷ 2 = 430,000.
  months of history 6, real inflows in window 72 → data depth **sufficient**.
  X1: 430,000 × 100 = 43,000,000 vs 424,000 × 60 = 25,440,000 → not triggered (wallet median = 101.4% of declared).
- **Failed rules:** none → **ready_for_review**.

## HO-M-03: Micro, boundary: installment 50.1% of income (E3 fails, alternative: 7 months)

- **Product:** amount 1,200,000 IQD → micro (term 6 months; allowed 3–12).
- **Installment:** 1,200,000 × (100 + 6) ÷ (100 × 6) = 127,200,000 ÷ 600 = 212,000.00 → **212,000**.
- **E3:** (0 + 212,000) × 2 = 424,000 vs income 423,000 → FAILS. Ratio = 212,000 ÷ 423,000 = 0.5012 (50.12%).
- **E1/E2:** age 29 (18–65 → ok); activity since 2022-11 = 47 months vs 12 required → ok.
- **Documents:** business_licence, purchase_invoices. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** collateral_document. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 06/26 = 405,000, 07/26 = 440,000, 08/26 = 428,000, 09/26 = 415,000, 10/26 = 455,000
  median: middle of 5 sorted values = 428,000.
  months of history 5, real inflows in window 55 → data depth **sufficient**.
  X1: 428,000 × 100 = 42,800,000 vs 423,000 × 60 = 25,380,000 → not triggered (wallet median = 101.2% of declared).
- **Alternative (E3 is the only cause):** extend the term to the shortest term that fits (up to the product maximum 12): installment = 183,429, (0 + 183,429) × 2 = 366,858 ≤ 423,000 → fits at 7 months. Offer: amount 1,200,000, term 7. Ratio 0.4336.
- **Failed rules:** E3 → **outside_product_limits**.

## HO-M-04: Micro, thin wallet (2 months) offset by a lease contract: ready, labelled low_data

- **Product:** amount 900,000 IQD → micro (term 10 months; allowed 3–12).
- **Installment:** 900,000 × (100 + 10) ÷ (100 × 10) = 99,000,000 ÷ 1,000 = 99,000.00 → **99,000**.
- **E3:** (0 + 99,000) × 2 = 198,000 vs income 400,000 → passes. Ratio = 99,000 ÷ 400,000 = 0.2475 (24.75%).
- **E1/E2:** age 26 (18–65 → ok); activity since 2025-02 = 20 months vs 12 required → ok.
- **Documents:** lease_contract. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** guarantor. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 09/26 = 360,000, 10/26 = 430,000
  median: (360,000 + 430,000) ÷ 2 = 395,000.
  months of history 2, real inflows in window 26 → data depth **low_data**.
  X1 is not evaluated on low-data wallets (never penalise thin history).
- **Failed rules:** none → **ready_for_review**.

## HO-N-01: Minor, guarantee missing (C9): incomplete

- **Product:** amount 4,000,000 IQD → minor (term 16 months; allowed 13–20).
- **Installment:** 4,000,000 × (100 + 16) ÷ (100 × 16) = 464,000,000 ÷ 1,600 = 290,000.00 → **290,000**.
- **E3:** (0 + 290,000) × 2 = 580,000 vs income 1,100,000 → passes. Ratio = 290,000 ÷ 1,100,000 = 0.2636 (26.36%).
- **E1/E2:** age 38 (18–65 → ok); activity since 2021-06 = 64 months vs 36 required → ok.
- **Documents:** business_licence, purchase_invoices. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** MISSING (C9). **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 1,100,000, 06/26 = 1,180,000, 07/26 = 1,020,000, 08/26 = 1,130,000, 09/26 = 1,090,000, 10/26 = 1,160,000
  median: (1,100,000 + 1,130,000) ÷ 2 = 1,115,000.
  months of history 7, real inflows in window 90 → data depth **sufficient**.
  X1: 1,115,000 × 100 = 111,500,000 vs 1,100,000 × 60 = 66,000,000 → not triggered (wallet median = 101.4% of declared).
- **Failed rules:** C9 → **incomplete**.

## HO-N-02: Minor, seasonal taxi driver: two weak months, wallet median still >= 60% of declared; must not be penalised (fairness)

- **Product:** amount 3,000,000 IQD → minor (term 15 months; allowed 13–20).
- **Installment:** 3,000,000 × (100 + 15) ÷ (100 × 15) = 345,000,000 ÷ 1,500 = 230,000.00 → **230,000**.
- **E3:** (0 + 230,000) × 2 = 460,000 vs income 800,000 → passes. Ratio = 230,000 ÷ 800,000 = 0.2875 (28.75%).
- **E1/E2:** age 45 (18–65 → ok); activity since 2019-09 = 85 months vs 36 required → ok.
- **Documents:** professional_licence. C8 (activity proof): ok. Income-evidence document for E4: no.
- **Guarantee:** collateral_document. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 700,000, 06/26 = 250,000, 07/26 = 220,000, 08/26 = 480,000, 09/26 = 750,000, 10/26 = 690,000
  median: (480,000 + 690,000) ÷ 2 = 585,000.
  months of history 8, real inflows in window 62 → data depth **sufficient**.
  X1: 585,000 × 100 = 58,500,000 vs 800,000 × 60 = 48,000,000 → not triggered (wallet median = 73.1% of declared).
- **Failed rules:** none → **ready_for_review**.

## HO-N-03: Minor, activity only 30 months, 36 required (E2): outside limits, no alternative

- **Product:** amount 3,500,000 IQD → minor (term 14 months; allowed 13–20).
- **Installment:** 3,500,000 × (100 + 14) ÷ (100 × 14) = 399,000,000 ÷ 1,400 = 285,000.00 → **285,000**.
- **E3:** (0 + 285,000) × 2 = 570,000 vs income 950,000 → passes. Ratio = 285,000 ÷ 950,000 = 0.3000 (30.00%).
- **E1/E2:** age 33 (18–65 → ok); activity since 2024-04 = 30 months vs 36 required → FAILS.
- **Documents:** business_licence, lease_contract. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** guarantor. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 960,000, 06/26 = 940,000, 07/26 = 980,000, 08/26 = 920,000, 09/26 = 970,000, 10/26 = 950,000
  median: (950,000 + 960,000) ÷ 2 = 955,000.
  months of history 7, real inflows in window 78 → data depth **sufficient**.
  X1: 955,000 × 100 = 95,500,000 vs 950,000 × 60 = 57,000,000 → not triggered (wallet median = 100.5% of declared).
- **Failed rules:** E2 → **outside_product_limits**.

## HO-N-04: Minor, business licence is in a different name from the applicant (X2): needs clarification

- **Product:** amount 5,000,000 IQD → minor (term 20 months; allowed 13–20).
- **Installment:** 5,000,000 × (100 + 20) ÷ (100 × 20) = 600,000,000 ÷ 2,000 = 300,000.00 → **300,000**.
- **E3:** (0 + 300,000) × 2 = 600,000 vs income 1,300,000 → passes. Ratio = 300,000 ÷ 1,300,000 = 0.2308 (23.08%).
- **E1/E2:** age 42 (18–65 → ok); activity since 2020-08 = 74 months vs 36 required → ok.
- **Documents:** business_licence, lease_contract. C8 (activity proof): ok. Income-evidence document for E4: yes.
- **Guarantee:** guarantor. **Wallet consent:** True.
- **Wallet (real inflow only; self_transfer, refund, loan_proceeds, outflow excluded):**
  monthly totals: 05/26 = 1,280,000, 06/26 = 1,350,000, 07/26 = 1,310,000, 08/26 = 1,390,000, 09/26 = 1,300,000, 10/26 = 1,330,000
  median: (1,310,000 + 1,330,000) ÷ 2 = 1,320,000.
  months of history 6, real inflows in window 90 → data depth **sufficient**.
  X1: 1,320,000 × 100 = 132,000,000 vs 1,300,000 × 60 = 78,000,000 → not triggered (wallet median = 101.5% of declared).
- **Failed rules:** X2 → **needs_clarification**.


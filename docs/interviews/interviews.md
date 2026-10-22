# Field Validation: Stakeholder Interviews

**Project:** Waseet Al-Qroud, AI Loan Officer Agent (Topic 03) · Agentic AI Challenge Iraq
**Authors:** Ahmed Mohammed · Mustafa Ahmed
**Last updated:** 20 October 2026

---

## 1. Overview

| | |
|---|---|
| **Purpose** | Test our assumptions about applicants, loan officers and the application process before fixing the rulebook. |
| **Method** | Semi-structured, in-person interviews with a fixed question set per role. |
| **Ethics** | Verbal consent for anonymised use. Participants are identified by role and district only. No personal, financial or identity data was collected. |
| **Status** | 2 of 3 interviews completed. Interview #3 is pending. |

| # | Date | Role | Location | Status |
|---|------|------|----------|--------|
| 1 | 19 Oct 2026 | Small merchant | Al-Shorja, Baghdad | Completed |
| 2 | 20 Oct 2026 | Loan officer | Al-Jadriyah, Baghdad | Completed |
| 3 | [date] | Stalled applicant | [location] | Pending |

> **Evidence note.** Answers were recorded by the interviewers as written notes in Arabic and translated here. Arabic excerpts keep the recorded wording with spelling lightly normalised. These interviews inform design assumptions; they are not statistical evidence.

---

## 2. Key Findings at a Glance

1. **A human must stay in the loop.** The officer states that automated processing alone is insufficient and that site inspection is required.
2. **Collateral and purpose of financing decide outcomes.** They are the leading reasons for rejection.
3. **Missing documents lead to rejection or postponement.** Requirements are simple, so the cost of an incomplete file falls on the applicant, not on officer time.
4. **Affordability is tight for small earners.** The merchant reports no spare income for installments.
5. **Trust and channel preferences are specific.** The merchant prefers a form to chat, writes in Modern Standard Arabic, dislikes transaction analysis and trusts officially licensed wallets.

---

## 3. Interview Records

### Interview #1: Small merchant

| | |
|---|---|
| **Date and place** | 19 October 2026, 11:30 AM · Al-Shorja, Baghdad |
| **Profile** | Trader in a traditional market. About 1,000,000 IQD of income per month passes through an e-wallet. Does not currently need credit, so he is a user-side reference, not a target applicant. |

**Q1. How do you establish your monthly income? Do you use an e-wallet, and how much of your income passes through it?**
Uses the Qi Card e-wallet. About 1,000,000 IQD of income passes through it monthly.

**Q2. Have you considered a loan? What stopped or delayed you?**
No, because he does not need one.

**Q3. What documents do you expect to be asked for? What do you not know?**
Expects the lender to require title deeds that can be sold if the borrower defaults, so that the lender always holds security to recover the amount.

**Q4. If someone explained a shortfall or delay, how should the explanation be given?**
As complete answers to the questions asked, supported by electronically recorded statements.

**Q5. Do you prefer a conversation or a form? Which language do you write in?**
Prefers the form because it gives time to think. Writes in Modern Standard Arabic (Fusha).

**Q6. Does analysis of your wallet transactions bother you? What reassures you?**
Dislikes it. Reassurance comes from the wallet's official issuance, for example a wallet licensed with Central Bank approval.

**Q7. What monthly installment could you pay without pressure?**
None. Income is almost fully allocated to living requirements.

**Recorded wording (Arabic)**
- «أفضل الاستمارة على المحادثة لأنها تعطيني فرصة للتفكير»
- «الذي يطمئنني على المحفظة هو الصدور الرسمي لها»
- «الدخل موزع على المتطلبات الحياتية بشكل كامل»

---

### Interview #2: Loan officer

| | |
|---|---|
| **Date and place** | 20 October 2026, 11:00 AM · Al-Jadriyah, Baghdad |
| **Profile** | Practising loan officer. His answers on duration and ratios likely reflect larger loans than Waseet's small-to-medium scope (see §4.2). |

**Q1. What is most often missing from small applicants' files?**
Data, documentation and the accuracy of submitted data.

**Q2. How much time goes to chasing documents compared with assessment?**
Not much, because the requirements are simple and not complex. If a required document is missing, the application is rejected or postponed.

**Q3. What are the most common reasons for rejection? Does the applicant understand them?**
Lack of collateral against the amount granted, and the feasibility or purpose of the financing. Whether applicants understand the reasons was not stated.

**Q4. Which documents do you accept as evidence of activity and income for cash-based applicants?**
Lease contract, business licence, professional practice licence, purchase invoices for goods, a project inspection report, and similar.

**Q5. What payment-to-income ratio is acceptable? When do you require a guarantor?**
The monthly installment must not exceed 50% of income or net income. The guarantor trigger was not stated separately; collateral was discussed under Q3.

**Q6. How long an activity history do you require, for small and large loans?**
Depends on the loan amount, from one year to five years.

**Q7. If a ready, organised file arrived with open questions, what must it contain?**
Complete applicant information, the requested amount, the purpose of financing and the collateral.

**Q8. What must an automated tool never do?**
Automated processing alone is not enough. On-site field inspection is required.

**Recorded wording (Arabic)**
- «الإدارة الآلية غير كافية وحدها، يتطلب إجراء كشوفات موقعية»
- «من أكثر أسباب الرفض عدم توفر ضمانات... والجدوى أو الغرض»
- «ألا يتجاوز القسط الشهري 50٪ من الدخل أو صافي الدخل»

---

### Interview #3: Stalled applicant (pending)

Planned questions: where the process stopped and whether the reason was explained; what would have helped to know from the start; how many visits or document submissions were needed; whether the outcome felt fair, and why.
*To be added before the MVP.*

---

## 4. Implications for the Design

### 4.1 Reframing the problem

We assumed loan officers lose most of their time chasing paperwork. The officer's answer shows otherwise: requirements are simple, and incomplete files are rejected or postponed. **The cost of an incomplete file therefore falls on the applicant.** Waseet's value is to tell the applicant exactly what is missing, including collateral and purpose, before the file reaches the officer, and to hand over a complete, consistent file.

### 4.2 Calibrating thresholds to Waseet's scope

The officer's figures probably come from larger loans than ours (Micro to Moderate, up to 15M IQD). We neither copy them nor ignore them. The rule we apply:

- **Scale-independent figures are adopted.** The installment ceiling is a ratio, not a size-dependent value. We use the officer's 50% of net income as the hard limit and keep our 35% as a visible "tight" flag.
- **Size-dependent figures are anchored and interpolated.** The one-to-five-year activity requirement grows with loan size. Our products sit at the small end, so we anchor at his lower bound and step up within his range: Micro 12, Minor 24, Moderate 36 months.
- **Everything lives in `rulebook.yaml`.** The thresholds are parameters, so a lender can replace them with its own policy without touching the engine.
- **Open item.** Confirm with the officer which loan sizes his one-to-five-year range applies to (see §6).

### 4.3 Decisions

| # | Finding | Decision | Affected file | Status |
|---|---------|----------|---------------|--------|
| 1 | Collateral and purpose drive rejections | Add completeness items: C10 purpose and feasibility statement, C11 collateral or guarantee type. The agent states up front which security is typically expected. Valuation stays with the human. | `rulebook/rulebook.yaml` | Proposed |
| 2 | Officer's accepted-evidence list | Align C7 (proof of activity) to: lease contract, business licence, professional practice licence, purchase invoices, inspection report. Wallet statement is supporting evidence. | `rulebook/rulebook.yaml` | Proposed |
| 3 | Activity period of 1 to 5 years by amount | Micro 12, Minor 24, Moderate 36 months (§4.2). | `rulebook/rulebook.yaml` | Proposed |
| 4 | 50% of net income ceiling; merchant reports tight budgets | E3 uses declared net income. Hard limit 50%; "tight" flag above 35% shown to applicant and underwriter. | `rulebook/rulebook.yaml` | Proposed |
| 5 | Preference for a form; Modern Standard Arabic | After the chat, show a reviewable summary form (also serves as the confirmation gate). Iraqi Arabic stays the default; Modern Standard Arabic is selectable. | `app/` | Proposed |
| 6 | Unease about wallet analysis; trust from licensed providers | Consent screen stating what is read and why; documents-only route, never penalised. Wallet-provider agnostic. | `app/`, C9, E5 | Proposed |
| 7 | Explanations must cite recorded statements | Every explanation fact carries its source (tool and period). | `engine/`, grounding check | Proposed |
| 8 | Field inspection required | Underwriter file includes a "recommended field verification" list. | `build_underwriter_file()` | Proposed |

*Change "Proposed" to "Adopted" once the team confirms each row and record the change in `rulebook/CHANGELOG.md`.*

---

## 5. Limitations

- Two interviews, one lending institution, and a merchant who does not currently need a loan.
- The officer's scale of lending likely exceeds Waseet's scope.
- Notes are paraphrased and translated.
- Findings shape assumptions to be tested; they do not establish prevalence.

---

## 6. Follow-up Questions

1. Which loan sizes does the one-to-five-year activity requirement apply to, and what is required below roughly 8M IQD?
2. Which collateral types are accepted for small loans, and when is a guarantor accepted instead?
3. Do applicants understand rejection reasons today?
4. What exactly is checked during a site visit?
5. What are typical amounts and terms for first-time small borrowers?

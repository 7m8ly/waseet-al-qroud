# Design decisions log

What changed from the first draft (a friend's content, reviewed with Claude) and from the interviews, and why.

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

## Open
- Annual flat fee value
- Activity months for Minor and Moderate (officer gave 1–5 years)
- Third interview (stalled applicant), planned by 26 Oct

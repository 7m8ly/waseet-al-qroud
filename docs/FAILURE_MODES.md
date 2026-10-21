# Failure modes and how each is handled

| # | Failure | Detection | Handling |
|---|---|---|---|
| 1 | Amount misread (dialect, MSA, Arabizi, number words) | Pydantic validation; confirmation gate | Numbers come from form fields; free text must be confirmed; unconfirmed figures are never stored |
| 2 | Pressure for a verdict / prompt injection | Decision-language filter; logged event | Scripted safe reply; no tool can decide |
| 3 | Explanation cites an invented number | Grounding check against `explanation_facts` | One retry, then a fixed safe template |
| 4 | Declared income not supported by wallet (cash, thin history) | X1; "low data" label | Ask about cash income; accept documents; never auto-fail |
| 5 | Applicant refuses wallet analysis | Consent step | Documents-only path |
| 6 | No installment fits the income | E3 | Say so plainly; offer a smaller amount or longer term; never push a loan |
| 7 | Free-tier limit or outage in a demo | HTTP 429 / timeout | Provider switch, response cache, local fallback model |

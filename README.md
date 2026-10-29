<p align="center">
  <img src="assets/logo.png" alt="Waseet Al-Qroud Logo" width="180" height="180">
</p>

<h1 align="center">Waseet Al-Qroud (وسيط القروض)</h1>

<p align="center">
  <strong>AI Loan Officer Agent</strong> · Agentic AI Challenge Iraq (ZainCash) · Topic 03<br>
  <strong>Ahmed Mohammed & Mustafa Ahmed</strong>
</p>

---

Small-credit applicants in Iraq don't know what is required and are declined without a reason they can act on. Waseet collects the application (guided form, with an optional chat assistant that understands Iraqi dialect, Modern Standard Arabic and Arabizi), checks it against a **written rulebook**, explains every gap in plain words, and hands a complete file to a loan officer. **It never approves or declines. A human decides, and every file says a field visit is required.**

## Principles
1. Prepare and explain; a human decides.
2. The model converses, the code judges (rules, math and state live in Python).
3. Every number traces to a tool result.
4. Fair by construction: name, gender, religion, governorate and device never enter the engine.

## Architecture
Applicant → intake + confirmation gate (LLM → JSON, Pydantic) → deterministic core (six tools, SQLite, audit log) → explanation + guards (facts-only phrasing, verdict filter, number-grounding check, safe-template fallback) → underwriter file → human decision.
Tools: `check_completeness` · `compute_indicators` · `run_rules` · `compute_installment_options` · `build_explanation_facts` · `build_underwriter_file`.

## Repository
| Folder | Contents |
|---|---|
| `rulebook/` | `RULEBOOK.md` (readable) and `rulebook.yaml` (what the engine reads), v1.1 |
| `engine/` | deterministic core |
| `llm/` | prompts, extraction schemas, guards |
| `data/` | synthetic cases, wallets, dialogues, adversarial messages, build scripts (see `data/README.md`) |
| `data/heldout/` | the frozen exam (git tag `testset-frozen`), with `MANIFEST.sha256` |
| `eval/` | tests (pytest), promptfoo configs, results |
| `app/` | Streamlit app (applicant and underwriter views) |
| `docs/` | `interviews/`, `MODELS.md`, `FAILURE_MODES.md`, `DECISIONS.md` |

## Status (update at every milestone)
- [x] Design brief submitted (22 Oct 2026)
- [x] Held-out set frozen (by 29 Oct)
- [ ] Engine and tests, Micro first (by 31 Oct)
- [ ] LLM layer + Streamlit end to end (by 5 Nov)
- [ ] MVP submitted (8 Nov)

## Data and honesty
All data is synthetic: no real person, document or transaction. Results are reported as counts on a frozen held-out set (e.g. 11/12), misses included.

## Run (not ready yet)
```
pip install -r requirements.txt
cp .env.example .env   # add your own keys; never commit .env
streamlit run app/main.py
```

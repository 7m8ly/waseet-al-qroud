# Waseet Al-Qroud (وسيط القروض) 🇮🇶

> AI Loan Officer Agent for **Agentic AI Challenge Iraq** (ZainCash).

## 📌 Overview

**Waseet Al-Qroud** transforms a messy, opaque credit intake process into a complete, explained file in the time it takes to have a conversation. It allows small traders, drivers, and home-based workers in Iraq to apply for small loans effortlessly by chatting naturally in the **Iraqi dialect**.

## 🛡️ Core Architecture & Philosophy

Unlike typical naive LLM applications, Waseet Al-Qroud strictly separates conversational fluidity from critical decision-making:

- **The LLM Layer:** Handles dialect NLU, friendly chat, field extraction, and grounded explanations. *It never computes rules, numbers, or credit decisions.*
- **The Deterministic Core:** A robust Python-based engine that owns all completeness checks, consistency validations, loan rulebooks, and wallet indicators.
- **Human-in-the-Loop:** Every collected file is presented clearly to a human loan officer who makes the final, binding credit decision.

## 📂 Repository Structure(Maybe will be like this)

```text
├── rulebook/          # Written eligibility rules, tiers, and policy thresholds
├── engine/            # Deterministic core (completeness, consistency, rules, math)
├── llm/               # Prompts, NLU definitions, and guardrails
├── data/              # Synthetic applicant profiles & Iraqi-dialect dialogue datasets
├── eval/              # Held-out test sets, evaluation scripts, and metrics (promptfoo)
├── app/               # Streamlit web interface for applicants and underwriter view
└── docs/              # User interviews, edge cases, failure modes, and design briefs
```

## 🚀 Getting Started & Local Run(Not Ready for now🙃)

### 1. Clone the repository:
```bash
git clone https://github.com/7m8ly/waseet-al-qroud.git
cd waseet-al-qroud
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set up your environment variables (`.env`):
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Streamlit app:
```bash
streamlit run app/main.py
```

## 🎯 Challenge Context

Developed for the **Agentic AI Challenge Iraq** by ZainCash. Built with a strict commitment to safety, zero-tolerance guardrails against hallucinated loan decisions, and full audit logging for every tool call.
# Models, tools and data (disclosure)

| Part | Provider / tool | Model | Status |
|---|---|---|---|
| Development LLM | Groq (open model) | TODO: exact name from our console | to confirm |
| Volume and Arabic | Google AI Studio | Gemini Flash-Lite | planned |
| Spot quality checks | Google AI Studio | Gemini Flash | planned |
| Offline fallback | Ollama | TODO | planned |

Stack: Python, Pydantic, SQLite, Streamlit, pytest, promptfoo, Git.
AI assistants: Claude (planning, design-brief drafting and review). TODO: add every other tool and what it was used for.
Data: 100% synthetic, LLM-generated from our schema, sample hand-verified; seeds and prompts saved in `data/`.

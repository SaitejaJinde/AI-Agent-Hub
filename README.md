# AI-Agent-Hub

This repository contains a backend (FastAPI) and a frontend (Vite + TypeScript) for an agent hub project.

This commit adds dependency manifest and makes several defensive code changes so the backend is more robust when started locally.

How to run the backend (basic)

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the backend with uvicorn (from repo root):

```bash
uvicorn backend.main:app --reload
```

Notes and environment variables

- The backend uses python-dotenv to load environment variables from a `.env` file. Create a `.env` in the repo root with any required keys for your LLM provider (for example `OPENAI_API_KEY=...`) or other services.
- The exact variables required depend on the LLM client implementation (see `backend/llm_client.py`).

What I changed

- Added `requirements.txt` at repo root.
- Made imports in `backend` packages use relative imports to avoid import-time issues when running as a package.
- Hardened the return/value handling in `backend/agent.py` to accept different shapes from `app.invoke`.
- Added helpers in `backend/langgraph_agent.py` to safely run awaitables from sync code and to tolerate LLM/tool invoke results that are either strings, objects with `.content`, or coroutines.
- Improved filename parsing for the MCP filesystem tool path extraction (strips punctuation and quotes).

Recommended next steps (manual)

- Pin concrete package versions in `requirements.txt` after testing.
- Add a top-level `README.md` with more details about the frontend and deployment.
- Add tests and CI to validate the runtime behavior of the LLM client and the `langgraph` integration.


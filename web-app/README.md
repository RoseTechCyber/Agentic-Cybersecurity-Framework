# Web app README

This branch contains a minimal FastAPI backend to expose agent and RAG endpoints.

How to run (dev):

1. Create a virtual environment and install dependencies:
   python -m venv .venv
   . .venv/bin/activate   # or .\.venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt

2. Start a local inference server (see agents/ or foundry-windows-local examples) or set LOCAL_INFERENCE_URL.

3. Run the FastAPI app:
   uvicorn web-app.backend.app.main:app --reload --host 0.0.0.0 --port 8080

Endpoints:
- GET /health
- POST /agents/run  (body: {"agent":"name","input":{}})
- POST /rag/query   (body: {"query":"..."})

Hybrid option:
- To enable hybrid fallback to Azure/OpenAI set USE_HYBRID=true and configure AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY in env.

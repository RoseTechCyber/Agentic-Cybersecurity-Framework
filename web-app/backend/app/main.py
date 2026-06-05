from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="ACSF Web API")

@app.get("/health")
def health():
    return {"status": "ok"}

class AgentRunRequest(BaseModel):
    agent: str
    input: Dict[str, Any]

@app.post("/agents/run")
def run_agent(req: AgentRunRequest):
    # placeholder: call orchestrator / reasoning agent
    return {"agent": req.agent, "result": {"note": "stub - runs agent pipeline"}}

class RAGQuery(BaseModel):
    query: str

@app.post("/rag/query")
def rag_query(q: RAGQuery):
    # placeholder: retrieve docs from Chroma, call LLM, return answer
    return {"query": q.query, "answer": "stubbed answer"}

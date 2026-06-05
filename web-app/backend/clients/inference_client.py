"""
Inference client for web-app: tries local inference server first (llama-cpp local FastAPI),
falls back to Azure/OpenAI if configured (hybrid mode). This client is intentionally
minimal and demonstrates the routing pattern.
"""
import os
import requests
from typing import Dict, Any

LOCAL_INFERENCE_URL = os.environ.get("LOCAL_INFERENCE_URL", "http://localhost:9000/generate")
USE_HYBRID = os.environ.get("USE_HYBRID", "false").lower() == "true"

# Optional Azure/OpenAI config (environment)
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_KEY = os.environ.get("AZURE_OPENAI_KEY")


def call_local(prompt: str) -> Dict[str, Any]:
    resp = requests.post(LOCAL_INFERENCE_URL, json={"prompt": prompt, "max_tokens": 256}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def call_azure(prompt: str) -> Dict[str, Any]:
    # Placeholder: implement Azure/OpenAI call here if configured
    if not AZURE_ENDPOINT or not AZURE_KEY:
        raise RuntimeError("Azure/OpenAI not configured")
    return {"text": "[azure fallback response]"}


def generate(prompt: str) -> str:
    try:
        local = call_local(prompt)
        return local.get("text") or str(local)
    except Exception:
        if USE_HYBRID:
            az = call_azure(prompt)
            return az.get("text") or str(az)
        raise

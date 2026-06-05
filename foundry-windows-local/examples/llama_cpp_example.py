"""
Native Windows example: load a GGML quantized LLaMA model using llama-cpp-python and run a simple prompt.
Requirements:
- Python 3.9+
- pip install llama-cpp-python
- Download a GGML quantized model (e.g., ggml-model-q4_0.bin) and place it in C:\models\
"""
from llama_cpp import Llama
import os

MODEL_PATH = os.environ.get('LLAMA_MODEL_PATH', r"C:\models\ggml-model-q4_0.bin")

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}. Set LLAMA_MODEL_PATH env or place model there.")
        return
    llm = Llama(model_path=MODEL_PATH)
    prompt = "Provide a short checklist for triaging a suspicious Windows host.")
    resp = llm(prompt, max_tokens=200)
    print(resp)

if __name__ == '__main__':
    main()

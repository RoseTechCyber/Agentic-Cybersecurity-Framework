# Windows native LLaMA quickstart

## Install Python and dependencies

1. Install Python 3.9+ from https://www.python.org/downloads/windows/
2. Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\activate
3. Install required package:
   pip install --upgrade pip
   pip install llama-cpp-python

## Obtain a GGML quantized model
- Download a compatible GGML quantized model (respect licenses) and place the .bin file in C:\models\
- Set environment variable LLAMA_MODEL_PATH to the full path or edit examples accordingly.

## Run example
   python foundry-windows-local/examples/llama_cpp_example.py


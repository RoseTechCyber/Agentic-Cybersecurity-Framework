# Foundry Windows Local

This folder contains native-Windows guidance and examples to run local LLaMA models without WSL.

Contents:
- examples/llama_cpp_example.py: simple example using llama-cpp-python and a GGML quantized model.
- install/README.md: quick steps to install dependencies on Windows.

Notes:
- This is intended for development/experimentation. Quantized GGML models are required for CPU-only usage.
- Do NOT commit model binaries to this repo.

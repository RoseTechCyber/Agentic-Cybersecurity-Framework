# GPU examples and notes

This directory contains guidance and minimal examples for running a GPU-backed inference server locally.

Recommended stacks:
- vLLM (server) + Transformers model
- text-generation-inference (TGI) + HF models

Example: vLLM Docker (Linux GPU with NVIDIA runtime)

1. Ensure NVIDIA drivers + Docker with nvidia-container-toolkit installed.
2. Example docker-compose snippet (not included here): use image ghcr.io/vllm/vllm:latest or a custom build.
3. Run the service and point web-app or agents to the inference endpoint.

Notes on Windows GPU:
- Prefer WSL2 + CUDA for best compatibility with Linux containers.
- Alternatively, build Windows-native inference using ONNX + DirectML or llama.cpp built with CUDA support.
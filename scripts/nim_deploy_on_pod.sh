#!/bin/bash
# ADC Mission Control — NIM Proof of Concept
# Run this INSIDE the RunPod pod after it boots

echo "=== ADC NIM Proof of Concept ==="
echo "GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)"
echo ""

# Install vLLM (open source inference engine, NIM-compatible API)
echo "Installing vLLM..."
pip install vllm --quiet 2>/dev/null

# Download and serve Qwen 3 8B
echo ""
echo "Starting Qwen 3 8B inference server..."
echo "This will download the model (~16GB) and start serving on port 8000"
echo "API will be OpenAI-compatible at http://localhost:8000/v1/chat/completions"
echo ""

python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-8B \
    --host 0.0.0.0 \
    --port 8000 \
    --max-model-len 4096 \
    --trust-remote-code \
    --dtype auto \
    --gpu-memory-utilization 0.9

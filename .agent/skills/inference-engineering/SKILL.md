---
name: inference-engineering
description: High-performance LLM serving, continuous batching, PagedAttention, KV-cache sizing, quantization (AWQ, GPTQ, GGUF), and inference engines (vLLM, TensorRT-LLM, llama.cpp).
---

# Inference Engineering & High-Throughput Serving

Inference engineering optimizes LLM serving latency (Time to First Token - TTFT, Inter-Token Latency - ITL), throughput (tokens/second), and hardware utilization.

## Core Serving Engines

1. **vLLM:**
   - **PagedAttention:** Virtual memory paging for KV-cache eliminating memory fragmentation and enabling up to 4x throughput.
   - **Continuous Batching:** Dynamically groups incoming requests at the token iteration level rather than request level.
   - **Speculative Decoding:** Uses a small draft model to generate candidate tokens verified in parallel by the target model.

2. **TensorRT-LLM:**
   - Compiled TensorRT execution graphs for NVIDIA GPUs.
   - Kernel fusion (fused multi-head attention, fused GEMM + activation).
   - In-flight batching and FP8 matrix multiplication.

3. **llama.cpp / Ollama:**
   - CPU and consumer GPU local inference using quantized GGUF models.
   - Direct memory mapping (`mmap`) for instant model loading.

## Optimization & Memory Formulae
- **KV Cache Size Calculation:**
  $$\text{KV Memory (bytes)} = 2 \times 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{seq\_len} \times \text{batch\_size}$$
- **Quantization Selection:**
  - **AWQ (Activation-aware Weight Quantization):** Best for 4-bit GPU serving with minimal perplexity degradation.
  - **GGUF:** Best for CPU/Apple Silicon offloading.
  - **FP8 (E4M3 / E5M2):** Native support on NVIDIA Ada Lovelace / Hopper architectures.

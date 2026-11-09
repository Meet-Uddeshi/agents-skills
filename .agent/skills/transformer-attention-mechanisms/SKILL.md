---
name: transformer-attention-mechanisms
description: Implementation and mathematical foundations of Transformers, Attention mechanisms (MHA, GQA, MQA), FlashAttention, RoPE, KV-cache engineering, and Mixture of Experts (MoE).
---

# Transformer Architectures & Attention Mechanisms

This skill covers the deep mathematical formulation, PyTorch implementations, and kernel optimizations for modern Transformer models and attention variants.

## Mathematical Formulation

### 1. Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$$
Where $Q \in \mathbb{R}^{B \times H \times N \times d_k}$, $K \in \mathbb{R}^{B \times H \times S \times d_k}$, $V \in \mathbb{R}^{B \times H \times S \times d_v}$, and $M$ is the causal/padding mask.

### 2. Attention Variants
- **Multi-Head Attention (MHA):** Every query head has an independent key and value head ($H_q = H_k = H_v$). High memory bandwidth consumption during autoregressive generation.
- **Multi-Query Attention (MQA):** All query heads share a single key head and a single value head ($H_k = H_v = 1$). Maximizes generation throughput at minor quality cost.
- **Grouped-Query Attention (GQA):** Partitions query heads into $G$ groups, with each group sharing one key and value head ($H_k = H_v = G$, e.g., Llama 3 with 32 query heads and 8 key/value heads). Optimal balance between quality and inference memory.

### 3. FlashAttention (v1, v2, v3)
- **Problem:** Standard attention materializes $N \times N$ attention matrix in GPU HBM, resulting in $O(N^2)$ memory reads/writes.
- **Solution:** IO-aware tiling. Divides $Q, K, V$ into blocks, loads them into fast on-chip SRAM, computes attention incrementally using online softmax normalization, and recomputes intermediate values in backward pass.

### 4. Rotary Position Embedding (RoPE)
Transforms 2D coordinate pairs $(x_{2i}, x_{2i+1})$ via a 2D rotation matrix:
$$R_{\Theta, m}^{2d} = \begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix}$$
Preserves relative positional distances while maintaining inner-product compatibility.

### 5. Mixture of Experts (MoE)
- Routing equation with top-$k$ gating:
  $$y = \sum_{i \in \text{TopK}(G(x), k)} G(x)_i E_i(x)$$
- Load balancing loss added during training to prevent expert collapse.

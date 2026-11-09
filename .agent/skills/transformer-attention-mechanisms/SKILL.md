---
name: transformer-attention-mechanisms
description: Implementation and mathematical foundations of Transformers, Attention mechanisms (MHA, GQA, MQA), FlashAttention, RoPE, KV-cache engineering, and Mixture of Experts (MoE).
---

# Transformer Architectures & Attention Mechanisms

This skill covers the deep mathematical formulations, modular PyTorch implementations, and kernel optimizations for modern Transformer models, attention variants, and token routing algorithms.

---

## 1. Attention Mechanisms: Mathematical Formulations

### 1.1 Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$$
Where:
- $Q \in \mathbb{R}^{B \times H_q \times N \times d_k}$ (Queries)
- $K \in \mathbb{R}^{B \times H_k \times S \times d_k}$ (Keys)
- $V \in \mathbb{R}^{B \times H_v \times S \times d_v}$ (Values)
- $M \in \mathbb{R}^{N \times S}$ is the causal or padding attention mask ($-\infty$ on illegal positions)
- The scaling factor $\frac{1}{\sqrt{d_k}}$ prevents dot products from growing excessively large in high dimensions, which would drive softmax into regions with vanishing gradients.

---

## 2. Attention Variants & PyTorch Implementations

### 2.1 Grouped-Query Attention (GQA) Implementation
In GQA, $H_q$ query heads are divided into $H_{kv}$ groups. Each group of $\frac{H_q}{H_{kv}}$ query heads shares a single key and value head.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model: int, num_query_heads: int, num_kv_heads: int, max_seq_len: int = 4096):
        super().__init__()
        assert num_query_heads % num_kv_heads == 0, "Query heads must be a multiple of KV heads"
        self.d_model = d_model
        self.num_query_heads = num_query_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = d_model // num_query_heads
        self.num_queries_per_kv = num_query_heads // num_kv_heads

        self.q_proj = nn.Linear(d_model, num_query_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(d_model, num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(d_model, num_kv_heads * self.head_dim, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        B, S, _ = x.shape
        
        # Project Q, K, V
        q = self.q_proj(x).view(B, S, self.num_query_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)

        # Repeat K and V across the query head groups
        if self.num_queries_per_kv > 1:
            k = k.repeat_interleave(self.num_queries_per_kv, dim=1)
            v = v.repeat_interleave(self.num_queries_per_kv, dim=1)

        # Scaled Dot-Product Attention (using optimized kernel)
        out = F.scaled_dot_product_attention(
            q, k, v,
            attn_mask=mask,
            dropout_p=0.0,
            is_causal=(mask is None and S > 1)
        )

        out = out.transpose(1, 2).contiguous().view(B, S, self.d_model)
        return self.out_proj(out)
```

---

## 3. Rotary Position Embedding (RoPE)

RoPE encodes relative position by rotating the query and key vectors in complex 2D planes, preserving inner-product properties without adding absolute position vectors to embeddings.

### 3.1 Mathematical Implementation
```python
class RotaryEmbedding(nn.Module):
    def __init__(self, dim: int, max_seq_len: int = 8192, theta: float = 500000.0):
        super().__init__()
        self.dim = dim
        inv_freq = 1.0 / (theta ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)

    def forward(self, x: torch.Tensor, seq_len: int):
        t = torch.arange(seq_len, device=x.device, dtype=self.inv_freq.dtype)
        freqs = torch.outer(t, self.inv_freq)
        # Construct rotation frequencies: [seq_len, dim/2] -> [seq_len, dim]
        emb = torch.cat((freqs, freqs), dim=-1)
        return emb.cos(), emb.sin()

def apply_rotary_pos_emb(q: torch.Tensor, k: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor):
    # Rotate half function: [-x2, x1]
    def rotate_half(x):
        x1 = x[..., :x.shape[-1] // 2]
        x2 = x[..., x.shape[-1] // 2:]
        return torch.cat((-x2, x1), dim=-1)

    cos = cos.unsqueeze(0).unsqueeze(0) # [1, 1, S, D]
    sin = sin.unsqueeze(0).unsqueeze(0)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed
```

---

## 4. Modern Transformer Decoder Block

Combines **RMSNorm**, **Grouped-Query Attention**, **RoPE**, and **SwiGLU FFN** (the standard architectural backbone of Llama-3, Mistral, and Qwen).

```python
class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        variance = x.pow(2).mean(-1, keepdim=True)
        return x * torch.rsqrt(variance + self.eps) * self.weight

class SwiGLUFFN(nn.Module):
    def __init__(self, d_model: int, d_ffn: int):
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ffn, bias=False)
        self.w_up = nn.Linear(d_model, d_ffn, bias=False)
        self.w_down = nn.Linear(d_ffn, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))

class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, num_q_heads: int, num_kv_heads: int, d_ffn: int):
        super().__init__()
        self.attn_norm = RMSNorm(d_model)
        self.attn = GroupedQueryAttention(d_model, num_q_heads, num_kv_heads)
        self.ffn_norm = RMSNorm(d_model)
        self.ffn = SwiGLUFFN(d_model, d_ffn)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        # Pre-LN residual connections
        x = x + self.attn(self.attn_norm(x), mask=mask)
        x = x + self.ffn(self.ffn_norm(x))
        return x
```

---

## 5. Mixture of Experts (MoE) Architecture

MoE replaces dense FFN layers with multiple expert networks and a gating router:

```python
class MoERouter(nn.Module):
    def __init__(self, d_model: int, num_experts: int, top_k: int = 2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, num_experts, bias=False)

    def forward(self, x: torch.Tensor):
        logits = self.gate(x) # [B, S, num_experts]
        weights = F.softmax(logits, dim=-1)
        topk_weights, topk_indices = torch.topk(weights, self.top_k, dim=-1)
        # Normalize top-k weights to sum to 1
        topk_weights = topk_weights / topk_weights.sum(dim=-1, keepdim=True)
        return topk_weights, topk_indices
```

---

## 6. Mandatory Rules & Anti-Patterns

### Anti-Patterns to Strictly Avoid
- **Post-LN Instability:** Never use Post-LayerNorm in deep transformers (>20 layers); gradients degrade without aggressive warmups. Always use Pre-LN or RMSNorm.
- **Materializing Full Attention Tensors:** Never perform manual `(q @ k.T) / scale` on sequences $> 2,048$ tokens without calling `torch.nn.functional.scaled_dot_product_attention` or FlashAttention. Doing so triggers catastrophic $O(N^2)$ memory allocation.
- **Ignoring RoPE Inverse Frequency Caching:** Never recompute trigonometric inverse frequencies during every forward pass. Register them as persistent buffers.

### Mandatory Verification Checklist
1. Is scaled dot-product attention scaled by $\frac{1}{\sqrt{d_k}}$?
2. Are causal attention masks applied prior to softmax normalization?
3. Does Grouped-Query Attention cleanly repeat KV heads across query groups?
4. Are Pre-LN residual streams preserved throughout all decoder blocks?

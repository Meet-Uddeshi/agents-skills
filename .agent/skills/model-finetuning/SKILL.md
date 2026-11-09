---
name: model-finetuning
description: Parameter-Efficient Fine-Tuning (PEFT), LoRA, QLoRA, DoRA, 4-bit/8-bit quantization (BitsAndBytes, AWQ), HuggingFace Transformers/TRL, and Weights & Biases tracking.
---

# Model Fine-Tuning & Quantization

This skill covers training methodologies for adapting foundation models to specialized domains using minimal GPU compute and memory.

## Fine-Tuning Paradigms

### 1. Parameter-Efficient Fine-Tuning (PEFT)
- **LoRA (Low-Rank Adaptation):**
  Decomposes weight updates $\Delta W \in \mathbb{R}^{d \times k}$ into two low-rank matrices $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ where $r \ll \min(d, k)$:
  $$W = W_0 + \frac{\alpha}{r} (B \cdot A)$$
  Freezes base model weights $W_0$; trains only $A$ and $B$, reducing trainable parameters by >99%.
- **QLoRA (Quantized LoRA):**
  Quantizes base model to 4-bit NormalFloat (NF4), uses Double Quantization to save memory, and applies Paged Optimizers to manage memory spikes during backward pass.
- **DoRA (Weight-Decomposed Low-Rank Adaptation):**
  Decomposes weights into magnitude and direction components, applying LoRA solely to the directional component for higher accuracy.

### 2. Alignment & Training Formats
- **Supervised Fine-Tuning (SFT):** Training on conversational prompt/response pairs with causal loss masking on prompt tokens.
- **Direct Preference Optimization (DPO):** Directly optimizes policy using preference pairs $(y_w, y_l)$ without training a separate reward model:
  $$\mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

### 3. Experiment Tracking with Weights & Biases (W&B)
- Log training/validation loss, learning rate schedule, gradient norm, and GPU memory utilization.
- Track hyperparameter sweeps using Optuna or W&B Sweeps (Bayesian / Hyperband).

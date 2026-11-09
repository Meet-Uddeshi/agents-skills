---
name: model-finetuning
description: Parameter-Efficient Fine-Tuning (PEFT), LoRA, QLoRA, DoRA, 4-bit/8-bit quantization (BitsAndBytes, AWQ), HuggingFace Transformers/TRL, and Weights & Biases tracking.
---

# Model Fine-Tuning & Quantization

This skill covers the end-to-end engineering of model adaptation, parameter-efficient fine-tuning (PEFT), quantization, and alignment pipelines using minimal GPU memory.

---

## 1. Parameter-Efficient Fine-Tuning (PEFT): Mathematical Formulations

### 1.1 LoRA (Low-Rank Adaptation)
Full fine-tuning updates all parameters $W \in \mathbb{R}^{d \times k}$. LoRA decomposes the weight update $\Delta W$ into two low-rank matrices $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$, where the rank $r \ll \min(d, k)$:

$$W_{\text{adapted}} = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

- $W_0$ is frozen during training.
- Matrix $A$ is initialized with Gaussian noise $\mathcal{N}(0, \sigma^2)$, and matrix $B$ is initialized to zero, ensuring $\Delta W = 0$ at the start of training.
- The scaling factor $\frac{\alpha}{r}$ stabilizes hyperparameter tuning when changing rank $r$.

---

## 2. QLoRA: 4-bit Quantized Fine-Tuning

QLoRA enables fine-tuning 70B parameter models on a single 48GB GPU (or 7B/8B models on a 16GB GPU) through three core innovations:
1. **NF4 (NormalFloat4):** An information-theoretically optimal quantile quantization for normally distributed weights.
2. **Double Quantization (DQ):** Quantizes the quantization constants, saving 0.37 bits per parameter.
3. **Paged Optimizers:** Uses CUDA unified memory to page memory spikes during gradient updates to CPU RAM.

### 2.1 Production QLoRA Configuration in PyTorch
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def setup_qlora_model(model_id: str):
    # 1. 4-bit Quantization Config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )

    # 2. Load Base Model in 4-bit
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=False
    )
    model = prepare_model_for_kbit_training(model)

    # 3. LoRA Configuration targeting all linear layers
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]
    )

    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    return model
```

---

## 3. Supervised Fine-Tuning (SFT) with HuggingFace TRL

```python
from trl import SFTTrainer, SFTConfig
from datasets import Dataset

def train_sft(model, tokenizer, dataset: Dataset):
    training_args = SFTConfig(
        output_dir="checkpoints/qlora-sft",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        save_strategy="epoch",
        bf16=True,
        max_seq_length=4096,
        report_to="wandb"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=model.peft_config["default"],
        processing_class=tokenizer,
        args=training_args
    )

    trainer.train()
    # Save adapter weights
    trainer.model.save_pretrained("adapters/final_lora")
```

---

## 4. Direct Preference Optimization (DPO)

DPO eliminates the need for training a separate reward model or RL training loops by directly optimizing the language model policy:

$$\mathcal{L}_{\text{DPO}}(\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

- $y_w$: Chosen / preferred response.
- $y_l$: Rejected response.
- $\beta$: Temperature parameter controlling divergence from reference model $\pi_{\text{ref}}$ (typically $0.1$).

---

## 5. Experiment Tracking with Weights & Biases (W&B)

```python
import wandb

def init_wandb_tracking(project_name: str, run_name: str, config: dict):
    wandb.init(
        project=project_name,
        name=run_name,
        config=config,
        reinit=True
    )
    # Log custom evaluation metrics
    wandb.define_metric("eval/loss", summary="min")
    wandb.define_metric("train/loss", summary="min")
```

---

## 6. Mandatory Quality Gates & Anti-Patterns

### Anti-Patterns to Avoid
- **Targeting Only Attention Projections:** Never apply LoRA solely to `q_proj` and `v_proj`. Benchmark evidence shows that targeting FFN layers (`gate_proj`, `up_proj`, `down_proj`) recovers nearly 100% of full fine-tuning performance.
- **Forgetting Adapter Merge for Inference:** Never deploy an unmerged LoRA adapter in high-throughput inference servers. Use `model.merge_and_unload()` before exporting to ONNX or vLLM to eliminate adapter forwarding overhead.
- **Overfitting on Small Datasets:** If training samples $< 1,000$, keep rank $r \le 8$ and set dropout $\ge 0.10$ to prevent catastrophic forgetting.

### Verification Checklist
1. Are trainable parameters verified to be $< 1.5\%$ of total model weights?
2. Is base model precision set to BF16 (or FP16 on older architectures)?
3. Are loss curves and gradient norms monitored via W&B or MLflow?
4. Are adapters cleanly merged before production export?

---
name: mlops-pipeline
description: Production MLOps architecture, DVC data versioning, ONNX dynamic export, Triton Inference Server deployment, MLflow registry, and automated drift monitoring.
---

# Production MLOps Pipeline and Deployment Architecture

This skill defines the engineering protocols for transitioning machine learning models from experimentation into fault-tolerant, high-throughput, observable production serving infrastructure.

---

## 1. MLOps Architectural Principles

1. **Immutable Model Lineage:** Every production model artifact must link deterministically to an exact git commit hash, a dataset snapshot hash (DVC), a training run identifier (MLflow/W&B), and a verifiable hardware runtime environment (Docker digest).
2. **Framework-Agnostic Serving:** Separate model training (PyTorch, TensorFlow, JAX) from inference runtimes. Compile trained weights into standardized execution graphs (ONNX, TensorRT, TorchScript) to eliminate Python interpreter bottlenecks.
3. **Hardware Acceleration Optimization:** Target execution engines specifically for hardware platforms: TensorRT for NVIDIA GPUs, OpenVINO for Intel x86 CPUs, CoreML for Apple Silicon, and Triton Inference Server for unified heterogeneous cluster orchestration.
4. **Continuous Quality and Drift Guardrails:** Continuously measure input data drift, target distribution shift, and latency percentiles (p50, p95, p99) against pre-deployment baselines.

---

## 2. Data and Pipeline Versioning with DVC

Data Version Control (DVC) decouples multi-gigabyte training corpora and weight checkpoints from git repositories while maintaining synchronicity with git branch histories.

### 2.1 Complete dvc.yaml Pipeline Definition

```yaml
stages:
  prepare_dataset:
    cmd: python src/data/prepare.py --raw data/raw --out data/processed
    deps:
      - src/data/prepare.py
      - data/raw
    outs:
      - data/processed:
          cache: true
          persist: false

  train_model:
    cmd: python src/train.py --data data/processed --config configs/train.yaml --out models/checkpoint
    deps:
      - src/train.py
      - configs/train.yaml
      - data/processed
    params:
      - configs/train.yaml:
          - batch_size
          - learning_rate
          - weight_decay
          - epochs
    outs:
      - models/checkpoint:
          cache: true
    metrics:
      - evaluation/train_metrics.json:
          cache: false

  evaluate_model:
    cmd: python src/evaluate.py --model models/checkpoint --test data/processed/test.parquet --out evaluation
    deps:
      - src/evaluate.py
      - models/checkpoint
      - data/processed/test.parquet
    metrics:
      - evaluation/eval_metrics.json:
          cache: false
    plots:
      - evaluation/roc_curve.csv:
          x: fpr
          y: tpr
          template: simple
```

### 2.2 DVC Remote Configuration Workflow

```bash
# Initialize DVC within repository
dvc init

# Configure S3 or MinIO remote storage
dvc remote add -d production_storage s3://mlops-model-registry-production/dvc-store
dvc remote modify production_storage endpointurl https://storage.internal.net:9000

# Stage, track dataset, and push
dvc add data/raw/training_corpus.parquet
git add data/raw/training_corpus.parquet.dvc .gitignore
git commit -m "chore(dvc): track version 2.4.0 training corpus"
dvc push
```

---

## 3. High-Performance Model Export: PyTorch to ONNX

Production deployment requires exporting dynamic PyTorch computational graphs to ONNX Open Neural Network Exchange format with dynamic batch and sequence axes.

### 3.1 Production ONNX Export and Numerical Validation Script

```python
"""
Production ONNX Export and Numerical Parity Verification Script
Exports a transformer / feature extractor model with dynamic axes and validates parity.
"""

from typing import Dict, Any, Tuple
import os
import torch
import torch.nn as nn
import numpy as np
import onnx
import onnxruntime as ort


class FeatureExtractor(nn.Module):
    """Example production neural module with dynamic sequence and batch inputs."""
    def __init__(self, input_dim: int = 768, hidden_dim: int = 512, num_classes: int = 10):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.head = nn.Linear(hidden_dim, num_classes)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        # Compute masked mean pooling
        features = self.encoder(input_ids)
        mask_expanded = attention_mask.unsqueeze(-1).expand_as(features)
        sum_features = torch.sum(features * mask_expanded, dim=1)
        sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
        pooled = sum_features / sum_mask
        logits = self.head(pooled)
        return logits


def export_and_validate_onnx(
    model: nn.Module,
    output_path: str,
    feature_dim: int = 768,
    tolerance: float = 1e-4,
) -> bool:
    """
    Exports a PyTorch model to ONNX with dynamic batch and sequence length dimensions,
    verifying structural validity and numeric parity against PyTorch eager output.
    """
    model.eval()
    dummy_batch = 2
    dummy_seq_len = 16

    # Create representative dummy inputs
    dummy_input_ids = torch.randn(dummy_batch, dummy_seq_len, feature_dim, dtype=torch.float32)
    dummy_mask = torch.ones(dummy_batch, dummy_seq_len, dtype=torch.float32)

    # Define dynamic axes dictionary for variable workloads
    dynamic_axes = {
        "input_features": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "logits": {0: "batch_size"},
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    print(f"Exporting model to {output_path}...")
    torch.onnx.export(
        model,
        (dummy_input_ids, dummy_mask),
        output_path,
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input_features", "attention_mask"],
        output_names=["logits"],
        dynamic_axes=dynamic_axes,
    )

    # 1. Structural Validation
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX model structure checked successfully.")

    # 2. Numerical Parity Check
    with torch.no_grad():
        torch_output = model(dummy_input_ids, dummy_mask).cpu().numpy()

    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    ort_session = ort.InferenceSession(output_path, providers=providers)

    ort_inputs = {
        "input_features": dummy_input_ids.cpu().numpy(),
        "attention_mask": dummy_mask.cpu().numpy(),
    }
    ort_output = ort_session.run(None, ort_inputs)[0]

    max_diff = np.max(np.abs(torch_output - ort_output))
    mean_diff = np.mean(np.abs(torch_output - ort_output))

    print(f"Numerical verification complete: Max absolute error = {max_diff:.3e}, Mean error = {mean_diff:.3e}")
    if max_diff > tolerance:
        raise ValueError(f"Numerical disparity exceeded threshold: {max_diff} > {tolerance}")

    print("ONNX dynamic export fully validated for production.")
    return True
```

---

## 4. Triton Inference Server Deployment

Triton Inference Server optimizes GPU utilization across concurrent pipelines with dynamic batching, model pipelining, and multiple execution backends (TensorRT, ONNX Runtime, Python).

### 4.1 Model Repository Hierarchy

```
model_repository/
└── text_classifier/
    ├── config.pbtxt
    ├── 1/
    │   └── model.onnx
    └── 2/
        └── model.onnx
```

### 4.2 Production config.pbtxt Configuration

```protobuf
name: "text_classifier"
platform: "onnxruntime_onnx"
max_batch_size: 64

input [
  {
    name: "input_features"
    data_type: TYPE_FP32
    dims: [ -1, 768 ]
  },
  {
    name: "attention_mask"
    data_type: TYPE_FP32
    dims: [ -1 ]
  }
]

output [
  {
    name: "logits"
    data_type: TYPE_FP32
    dims: [ 10 ]
  }
]

# Production Dynamic Batching to aggregate requests within microsecond windows
dynamic_batching {
  max_queue_delay_microseconds: 5000
  preferred_batch_size: [ 8, 16, 32, 64 ]
}

# GPU Instance Execution Allocation
instance_group [
  {
    count: 2
    kind: KIND_GPU
    gpus: [ 0 ]
  }
]

# Model Warmup to prevent initial request latency spikes
model_warmup [
  {
    name: "warmup_request"
    batch_size: 16
    inputs {
      key: "input_features"
      value: {
        data_type: TYPE_FP32
        dims: [ 16, 32, 768 ]
        random_data: true
      }
    }
    inputs {
      key: "attention_mask"
      value: {
        data_type: TYPE_FP32
        dims: [ 16, 32 ]
        random_data: true
      }
    }
  }
]
```

### 4.3 High-Throughput Async Triton Client

```python
"""
Async Triton Inference Client with gRPC streaming and concurrent request pools.
"""

from typing import List, Dict, Any
import asyncio
import numpy as np
import tritonclient.grpc.aio as grpcclient
from tritonclient.utils import InferenceServerException


class TritonServiceClient:
    def __init__(self, server_url: str = "localhost:8001"):
        self.server_url = server_url
        self.client: grpcclient.InferenceServerClient = None

    async def connect(self):
        self.client = grpcclient.InferenceServerClient(url=self.server_url)
        is_live = await self.client.is_server_live()
        is_ready = await self.client.is_server_ready()
        if not (is_live and is_ready):
            raise ConnectionError(f"Triton server at {self.server_url} is not ready.")

    async def infer(
        self,
        model_name: str,
        input_features: np.ndarray,
        attention_mask: np.ndarray,
    ) -> np.ndarray:
        """
        Executes an asynchronous inference request via gRPC.
        """
        inputs = []
        outputs = []

        # Setup feature tensor
        feat_input = grpcclient.InferInput("input_features", input_features.shape, "FP32")
        feat_input.set_data_from_numpy(input_features.astype(np.float32))
        inputs.append(feat_input)

        # Setup mask tensor
        mask_input = grpcclient.InferInput("attention_mask", attention_mask.shape, "FP32")
        mask_input.set_data_from_numpy(attention_mask.astype(np.float32))
        inputs.append(mask_input)

        # Output binding
        output_binding = grpcclient.InferRequestedOutput("logits")
        outputs.append(output_binding)

        response = await self.client.infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs,
        )

        logits = response.as_numpy("logits")
        return logits

    async def close(self):
        if self.client:
            await self.client.close()
```

---

## 5. Statistical Drift Detection and Observability

Production models suffer from distribution shifts caused by seasonal variations, platform schema changes, and upstream sensor drift.

### 5.1 Mathematical Formulations

#### 1. Population Stability Index (PSI)
Quantifies the divergence between actual inference distribution $A$ and baseline training distribution $E$ across $K$ discrete bins:
$$\text{PSI} = \sum_{k=1}^K \left( A_k - E_k \right) \times \ln\left(\frac{A_k}{E_k}\right)$$

Interpretation standard:
- $\text{PSI} < 0.10$: Negligible shift; no intervention required.
- $0.10 \le \text{PSI} \le 0.25$: Moderate shift; schedule model retraining and inspect data pipelines.
- $\text{PSI} > 0.25$: Significant shift; immediate alarm, rollback or fallback to conservative heuristic.

#### 2. Two-Sample Kolmogorov-Smirnov (KS) Statistic
Evaluates whether continuous empirical cumulative distribution functions $F_1(x)$ and $F_2(x)$ differ significantly:
$$D = \sup_x \left| F_1(x) - F_2(x) \right|$$

---

### 5.2 Automated Drift Monitor Script

```python
"""
Production Data Drift and Statistical Distribution Monitor
Calculates PSI and KS-test metrics for inference feature streams against golden baselines.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from scipy import stats


class ProductionDriftMonitor:
    def __init__(self, baseline_features: np.ndarray, feature_names: List[str], num_bins: int = 10):
        self.feature_names = feature_names
        self.num_bins = num_bins
        self.baseline_features = baseline_features
        self.bins: Dict[str, np.ndarray] = {}
        self.baseline_dist: Dict[str, np.ndarray] = {}
        self._compute_baseline_distributions()

    def _compute_baseline_distributions(self):
        for idx, name in enumerate(self.feature_names):
            vals = self.baseline_features[:, idx]
            quantiles = np.linspace(0, 100, self.num_bins + 1)
            bins = np.percentile(vals, quantiles)
            bins[0] = -np.inf
            bins[-1] = np.inf
            self.bins[name] = bins

            hist, _ = np.histogram(vals, bins=bins)
            # Add Laplace smoothing to prevent division by zero in log ratios
            prob = (hist + 1e-4) / (len(vals) + 1e-4 * self.num_bins)
            self.baseline_dist[name] = prob

    def calculate_psi(self, current_features: np.ndarray) -> Dict[str, float]:
        """
        Computes Population Stability Index (PSI) for each feature.
        """
        psi_scores = {}
        for idx, name in enumerate(self.feature_names):
            vals = current_features[:, idx]
            bins = self.bins[name]
            hist, _ = np.histogram(vals, bins=bins)
            prob = (hist + 1e-4) / (len(vals) + 1e-4 * self.num_bins)
            baseline_prob = self.baseline_dist[name]

            # PSI = sum((actual - expected) * ln(actual / expected))
            psi = np.sum((prob - baseline_prob) * np.log(prob / baseline_prob))
            psi_scores[name] = float(psi)
        return psi_scores

    def calculate_ks_test(self, current_features: np.ndarray) -> Dict[str, Dict[str, float]]:
        """
        Runs Kolmogorov-Smirnov test on continuous feature distributions.
        """
        ks_results = {}
        for idx, name in enumerate(self.feature_names):
            baseline_vals = self.baseline_features[:, idx]
            current_vals = current_features[:, idx]
            res = stats.ks_2samp(baseline_vals, current_vals)
            ks_results[name] = {
                "statistic": float(res.statistic),
                "p_value": float(res.pvalue),
                "is_drift_detected": bool(res.pvalue < 0.05),
            }
        return ks_results

    def generate_drift_report(self, current_features: np.ndarray) -> Dict[str, Any]:
        psi_scores = self.calculate_psi(current_features)
        ks_scores = self.calculate_ks_test(current_features)

        alerts = []
        for name, psi in psi_scores.items():
            if psi > 0.25:
                alerts.append(f"CRITICAL: Feature '{name}' exhibited major drift (PSI: {psi:.4f} > 0.25)")
            elif psi > 0.10:
                alerts.append(f"WARNING: Feature '{name}' exhibited moderate drift (PSI: {psi:.4f} > 0.10)")

        return {
            "psi_metrics": psi_scores,
            "ks_metrics": ks_scores,
            "alert_count": len(alerts),
            "alerts": alerts,
            "overall_status": "UNHEALTHY" if len(alerts) > 0 else "HEALTHY",
        }
```

---

## 6. MLOps Best Practices Checklist

- [ ] **Data Versioning:** Datasets in S3/MinIO synced with DVC commits tracked in git.
- [ ] **Deterministic Pipelines:** All preprocessing steps defined in code with pinned seeds (`torch.manual_seed(42)`).
- [ ] **Dynamic Graph Export:** Models exported to ONNX / TensorRT with verified numerical equivalence ($< 10^{-4}$).
- [ ] **Triton Deployment:** Dynamic batching parameters tuned for target SLOs (e.g. 5ms queue delay).
- [ ] **Observability:** Hourly PSI and daily KS drift metrics published to Prometheus / Datadog dashboards.
- [ ] **Rollback Automation:** Automated Canary deployment with instant traffic divert on spike in 5xx errors or sudden PSI surge.

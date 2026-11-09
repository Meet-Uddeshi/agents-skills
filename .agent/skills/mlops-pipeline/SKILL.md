---
name: mlops-pipeline
description: Production MLOps, model registries (MLflow), ONNX Runtime export, Triton Inference Server, data versioning with DVC, and model performance/drift monitoring.
---

# Production MLOps & Model Deployment

This skill establishes automated, reproducible pipelines for moving models from research notebooks to scalable production infrastructure.

## Core MLOps Pipeline Stages

### 1. Data & Artifact Versioning (DVC)
- Decouple code git tracking from heavy data/model artifact storage (S3, GCS, MinIO).
- Track dataset commits and lineage hashes in `.dvc` tracking files.

### 2. Model Packaging & Export
- **ONNX (Open Neural Network Exchange):** Convert PyTorch/TensorFlow models to ONNX graph format using dynamic axis shapes for flexible batching and sequence length.
- **TorchScript / TorchDynamo:** Trace or script PyTorch modules for C++ runtime execution.
- **TensorRT Engine Compilation:** Compile ONNX graphs into precision-tuned (FP16/INT8) TensorRT engines targeting specific GPU architectures.

### 3. Serving via Triton Inference Server
- Model repository layout: `models/<model_name>/1/model.plan` (or `model.onnx`).
- `config.pbtxt` configuration:
  - Dynamic batching: `max_queue_delay_microseconds` and `max_batch_size`.
  - Multi-instance GPU placement: `instance_group [ { count: 2, kind: KIND_GPU } ]`.

### 4. Operational Monitoring & Drift Detection
- **Data Drift:** Measure distribution shifts between inference inputs and training baselines using Population Stability Index (PSI) or Kolmogorov-Smirnov test.
- **Concept Drift:** Monitor degradation in downstream business metrics (e.g., click-through rate, precision, conversion).

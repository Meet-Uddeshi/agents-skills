---
name: deep-learning-cv
description: Deep learning engineering with PyTorch, TensorFlow, Keras, OpenCV image/video processing, YOLO (v8/v9/v11), object detection, and Vision-Language Models (VLMs).
---

# Deep Learning & Computer Vision

This skill covers end-to-end computer vision pipelines, custom deep neural network architectures in PyTorch/TensorFlow, and multimodal vision-language models (VLMs).

---

## 1. PyTorch Deep Learning Engineering Foundations

### 1.1 Robust Training Loop with Mixed Precision & Gradient Clipping
```python
import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler
from torch.utils.data import DataLoader

def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    max_norm: float = 1.0
) -> float:
    model.train()
    scaler = GradScaler()
    total_loss = 0.0

    for batch_idx, (inputs, targets) in enumerate(dataloader):
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)

        # Mixed precision context
        with autocast(dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16):
            outputs = model(inputs)
            loss = criterion(outputs, targets)

        scaler.scale(loss).backward()
        
        # Unscale before gradient clipping
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_norm)
        
        scaler.step(optimizer)
        scaler.update()
        total_loss += loss.item()

    return total_loss / len(dataloader)
```

---

## 2. Computer Vision with OpenCV

### 2.1 Multi-Threaded RTSP Stream Capture (Zero-Latency Frame Buffer)
A standard single-threaded `cv2.VideoCapture` accumulates network latency and buffer lag. A dedicated thread decouples frame ingestion from inference.

```python
import cv2
import threading
import queue
import time

class RTSPCaptureThread:
    def __init__(self, rtsp_url: str):
        self.cap = cv2.VideoCapture(rtsp_url)
        self.q = queue.Queue(maxsize=2) # Keep only latest 2 frames
        self.running = True
        self.thread = threading.Thread(target=self._capture_worker, daemon=True)
        self.thread.start()

    def _capture_worker(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            if self.q.full():
                try:
                    self.q.get_nowait() # Drop stale frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def stop(self):
        self.running = False
        self.cap.release()
```

### 2.2 Preprocessing & Color Transformations
```python
import numpy as np

def preprocess_image_for_model(frame: np.ndarray, target_size: tuple = (640, 640)) -> torch.Tensor:
    # 1. Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 2. Letterbox resize maintaining aspect ratio
    h, w = rgb.shape[:2]
    scale = min(target_size[0] / h, target_size[1] / w)
    nh, nw = int(h * scale), int(w * scale)
    resized = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_LINEAR)
    
    canvas = np.full((target_size[0], target_size[1], 3), 114, dtype=np.uint8)
    canvas[(target_size[0] - nh) // 2 : (target_size[0] - nh) // 2 + nh,
           (target_size[1] - nw) // 2 : (target_size[1] - nw) // 2 + nw] = resized
           
    # 3. Normalize to [0, 1] and transpose to CHW
    tensor = torch.from_numpy(canvas).permute(2, 0, 1).float() / 255.0
    return tensor.unsqueeze(0) # [1, 3, H, W]
```

---

## 3. Real-Time Detection with YOLO (v8, v9, v11)

### 3.1 Training & Post-Processing Pipeline
```python
from ultralytics import YOLO

def train_and_export_yolo():
    # Load pretrained model
    model = YOLO("yolov8m.pt")

    # Train on custom dataset
    model.train(
        data="dataset.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        optimizer="AdamW",
        lr0=1e-3,
        weight_decay=0.0005,
        project="runs/detect",
        name="custom_yolo"
    )

    # Export to ONNX with dynamic batching for production serving
    model.export(format="onnx", dynamic=True, simplify=True)
```

---

## 4. Vision-Language Models (VLMs)

### 4.1 Multimodal Projector Architecture (LLaVA / CLIP Pattern)
A VLM integrates a frozen visual transformer backbone with an autoregressive language model via a multimodal projector:

```python
class MultimodalProjector(nn.Module):
    def __init__(self, vision_dim: int, llm_dim: int):
        super().__init__()
        # Two-layer MLP projector with GELU activation
        self.linear_1 = nn.Linear(vision_dim, llm_dim, bias=True)
        self.act = nn.GELU()
        self.linear_2 = nn.Linear(llm_dim, llm_dim, bias=True)

    def forward(self, image_features: torch.Tensor) -> torch.Tensor:
        # Projects visual patch tokens [B, num_patches, vision_dim] -> [B, num_patches, llm_dim]
        return self.linear_2(self.act(self.linear_1(image_features)))
```

---

## 5. Mandatory Quality Gates & Anti-Patterns

### Anti-Patterns to Avoid
- **Blocking GUI Calls in Production Pipelines:** Never leave `cv2.imshow()` or `cv2.waitKey()` inside backend services or API endpoints.
- **Buffer Bloat in RTSP Ingestion:** Never read video streams synchronously in the inference thread. Unprocessed frames accumulate in OS network buffers, introducing seconds of artificial lag.
- **Silent Loss Divergence:** Always guard training loops against `NaN` losses by asserting `torch.isfinite(loss)` before backward pass.

### Verification Checklist
1. Is mixed precision enabled (`torch.cuda.amp`) with appropriate gradient scaling?
2. Are video frames captured asynchronously via dedicated threads?
3. Is non-maximum suppression (NMS) tuned with verified IoU thresholds ($\text{IoU} \approx 0.45$)?
4. Are image preprocessing steps normalized identically between training and inference?

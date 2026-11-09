---
name: deep-learning-cv
description: Deep learning engineering with PyTorch, TensorFlow, Keras, OpenCV image/video processing, YOLO (v8/v9/v11), object detection, and Vision-Language Models (VLMs).
---

# Deep Learning & Computer Vision

This skill covers end-to-end computer vision pipelines, custom deep neural network architectures, and multimodal vision-language models.

## Core Technical Areas

### 1. Framework Engineering (PyTorch, TensorFlow, Keras)
- Custom `nn.Module` subclasses with explicit forward passes and clean state dictionaries.
- Autograd gradient hooks, mixed precision (`torch.cuda.amp.autocast`), gradient clipping, and learning rate warmups.
- Distributed data parallel (`torch.nn.parallel.DistributedDataParallel`) setups.

### 2. Computer Vision with OpenCV
- Low-level image matrix operations: color space conversions (BGR to RGB, HSV, LAB), affine/perspective transformations, and histogram equalization.
- Filtering: Gaussian blur, Sobel/Laplacian gradients, Canny edge detection, contour analysis, and morphological operations.
- Video stream pipelines: Multi-threaded RTSP frame capture, frame buffer dropping, and background subtraction.

### 3. Real-Time Detection with YOLO (v8, v9, v11)
- Model variants: Nano (n) for edge, Small/Medium (s/m) for real-time, Large/Extra-Large (l/x) for high accuracy.
- Tasks: Object detection, instance segmentation, oriented bounding boxes (OBB), and pose estimation.
- Post-processing: Non-Maximum Suppression (NMS), confidence threshold filtering, and IoU matching.

### 4. Vision-Language Models (VLMs)
- Architecture: Vision encoder (e.g. CLIP ViT, SigLIP) + Projector (MLP / Cross-Attention) + Language model backbone (LLaVA, Qwen-VL, PaliGemma).
- Tasks: Visual question answering, document OCR extraction, visual grounding, and image captioning.

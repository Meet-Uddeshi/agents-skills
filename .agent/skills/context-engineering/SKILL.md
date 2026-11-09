---
name: context-engineering
description: Architect LLM context windows, attention budgeting, prompt assembly, dynamic tool registries, trajectory compaction, and evaluation harnesses.
---

# Context & Harness Engineering

Context engineering governs what enters the LLM context window, when it enters, and how it is structured across multi-turn trajectories to prevent context rot and token waste.

## Core Engineering Principles

### 1. Attention Curve & Token Budgeting
- **Head & Tail Optimization:**
  - Place immutable system instructions, zero-assumption invariants, and high-priority constraints at the **Head**.
  - Place recent tool observations, exact response schemas, and current task focus at the **Tail**.
  - Keep the middle section for compressed reference history; avoid burying critical constraints in the middle where LLM attention degrades.

### 2. Trajectory Compaction & Truncation Policies
- **Sliding Window with Semantic Rollup:** When conversation or tool execution history exceeds 50% of the active context limit, summarize intermediate turns into structured bullet points.
- **Tool Output Pruning:** Never dump full raw JSON responses or multi-megabyte log files into parent context. Extract target keys, row counts, and error messages before appending to prompt history.

### 3. Dynamic Tool Registry RAG
- Avoid defining 50+ tool schemas in a single prompt.
- Use vector or keyword lookup over tool descriptions to dynamically inject only the top 3-5 tools required for the current execution step.

### 4. Evaluation Harnesses (Inspect, Ragas, TruLens)
- Build deterministic evaluation harnesses with frozen dataset inputs.
- Measure 4 primary axes: Task Success Rate, Token Cost Efficiency, Tool Call Precision, and Context Faithfulness.

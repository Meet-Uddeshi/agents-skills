---
name: agentic-frameworks
description: Design, architect, and implement multi-agent systems, state graphs, human-in-the-loop workflows, and low-code agent automation using LangGraph, CrewAI, AutoGen, and n8n/Make.
---

# Agentic Frameworks & Multi-Agent Orchestration

This skill guides the construction of resilient, production-grade agentic architectures.

## Core Architectural Patterns

### 1. LangGraph State Machine Architecture
- **State Schema:** Strongly-typed state using Pydantic or TypedDict.
- **Nodes & Edges:** Pure transition functions. Nodes update state; conditional edges route execution based on tool output or router classification.
- **Cycles & Recursion Limits:** Enforce explicit recursion limits (`recursion_limit=25`) and cycle detection to prevent infinite execution loops.
- **Human-in-the-Loop (HITL):** Checkpointing via persistent state (e.g. SQLite, PostgreSQL saver), pause before destructive tool execution, and resume on user confirmation.

### 2. Hierarchical & Multi-Agent Swarms (CrewAI & AutoGen)
- **Supervisor-Worker Isolation:** Supervisor dispatches scoped micro-tasks to specialist agents. Workers operate in isolated sub-contexts and return condensed findings (under 300 words).
- **Tool Access Isolation:** Bind only necessary tools to specific worker roles (e.g., code-executor only to coding agent, web-search only to research agent).
- **Handoff Payloads:** Structured JSON handoffs defining task objective, discovered invariants, and handoff artifacts.

### 3. Workflow Automation Platforms (n8n, Make.com, Zapier)
- **Webhook Receivers & Triggers:** Design idempotent endpoints receiving incoming event webhooks.
- **Node Wiring:** Chain LLM nodes with branching logic, error catchers, and retry policies.
- **State Synchronization:** Persist run IDs and workflow variables in shared storage.

## Implementation Checklist
1. Validate state schema completeness (no implicit untyped mutations).
2. Guarantee bounded loop execution with explicit termination gates.
3. Insulate worker agent contexts to prevent token pollution.
4. Implement graceful tool error fallback and retry with exponential backoff.

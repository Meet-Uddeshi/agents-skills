---
description: Reverse engineer software features and reference apps. Extract system design, data models, API contracts, and user flows from reference software.
---

# /reverse-engineer - Reference Software Feature Extraction Workflow

$ARGUMENTS

---

## Purpose

Deconstruct reference applications (e.g., Google Photos, Spotify, Linear, Stripe) into reproducible architecture specifications, data schemas, API contracts, and production implementation steps.

---

## Sub-commands

```text
/reverse-engineer inspect [product]    - Extract core capabilities, interaction models, and UI paradigms
/reverse-engineer api [feature]        - Infer REST/GraphQL endpoints, request/response DTOs, and payloads
/reverse-engineer schema [domain]      - Reverse-engineer relational entities, indexes, and state machines
/reverse-engineer scaffold [feature]   - Generate production-ready boilerplate reproducing the reference capability
```

---

## Standard 6-Step Implementation Workflow

1. **Deconstruct User Experience & Flows:**
   - Map entry points, loading states, error states, and optimistic UI transitions.
   - Document interaction behaviors (debounced searches, infinite virtualized scrolling, gesture drags).

2. **Reverse Engineer Data Models:**
   - Define database entities, relations, primary/foreign keys, and normalization.
   - Specify index strategies for low-latency queries (GIN/GiST, composite b-tree).

3. **Reconstruct API Contracts:**
   - Define OpenAPI / TypeScript contracts for all endpoints.
   - Specify query parameters, pagination strategies (cursor-based vs offset), and response payloads.

4. **Identify Algorithmic & Infrastructure Requirements:**
   - Isolate core algorithms (e.g. vector embeddings for semantic search, background task queues, object storage CDN).
   - Document third-party services and dependencies.

5. **Scaffold Local Implementation:**
   - Generate modular component structure adhering to workspace standards.
   - Implement clean separation between business logic, data access, and presentation layers.

6. **Verify Parity & Quality Gates:**
   - Execute unit and integration tests covering edge cases and error boundaries.
   - Log design patterns and architectural tradeoffs to .agent/memory/ARCHITECTURE_MEMORY.md.


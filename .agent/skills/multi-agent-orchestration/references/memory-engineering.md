# Cognitive Memory Engineering Protocol

This protocol defines how agents persist, retrieve, and share knowledge across execution turns and sessions, ensuring no agent repeats mistakes or re-discovers already known facts.

## Dual-Tier Cognitive Memory

```text
┌────────────────────────────────────────────────────────┐
│             LAYER 1: SESSION MEMORY (EPHEMERAL)        │
│  - SESSION_FAILURES.md (in working directory)          │
│  - Active blackboard state (.agent/context/BLACKBOARD) │
│  - Cleared / reset between distinct user goals         │
└────────────────────────────────────────────────────────┘
                            ▲
                            │ Promoted on milestone
                            ▼
┌────────────────────────────────────────────────────────┐
│           LAYER 2: ARCHITECTURAL MEMORY (PERSISTENT)   │
│  - .agent/memory/ARCHITECTURE_MEMORY.md                │
│  - .agent/memory/DECISION_LOG.md (ADRs)                │
│  - Permanent workspace invariants across all sessions  │
└────────────────────────────────────────────────────────┘
```

## Layer 1: Ephemeral Session Memory

### `SESSION_FAILURES.md`
Created or updated immediately whenever an attempt fails:
- Failed file edits and incorrect assumptions
- Non-viable CLI flags or build errors
- Dead-end debugging hypotheses

**Rule:** Every agent MUST inspect `SESSION_FAILURES.md` before executing any retry or alternative strategy.

## Layer 2: Persistent Architectural Memory

### `.agent/memory/ARCHITECTURE_MEMORY.md`
Stores permanent project decisions and conventions:
- Technology stack decisions and version pins
- Forbidden patterns (e.g. Purple Ban, emoji ban, direct DB queries from controllers)
- System boundaries, core contracts, and API structures

**Rule:** Before initiating refactoring, adding libraries, or altering schemas, agents MUST consult this document.

## Blackboard Synchronization

When multiple agents participate in a task:
1. `understand-anything` or `project-scanner` discovers codebase facts -> Writes to blackboard.
2. `architect` designs module boundaries -> Reads blackboard invariants.
3. `backend-specialist` / `frontend-specialist` implements code -> Reads constraints, updates status.
4. `test-engineer` / `security-reviewer` verifies code -> Adds verification proofs to blackboard.


# Dynamic Runtime Complexity Escalation Matrix

Any specialist agent operating within the workspace must monitor execution complexity. When a complexity threshold is breached, the agent immediately suspends ad-hoc actions and invokes the designated Superpower skill.

## Escalation Triggers & Actions

| Complexity Indicator | Threshold Condition | Target Superpower Skill | Immediate Protocol |
| :--- | :--- | :--- | :--- |
| **Architectural Ambiguity** | Multiple valid implementation designs or unresolved trade-offs. | `brainstorming` | Stop coding. Present 2-3 approaches with explicit pros/cons and wait for user alignment. |
| **Multi-File / Multi-Step Work** | Change impacts > 2 files or requires > 3 steps. | `writing-plans` & `executing-plans` | Decompose work into bite-sized, sequentially verifiable steps. |
| **Failing Test / Crash / Bug** | Any unhandled exception, syntax error, or failing unit test. | `systematic-debugging` or `root-cause-tracing` | Isolate the minimal reproduction case. Identify root cause before proposing or editing any code. |
| **Core Feature Logic** | Writing new production functions, domain logic, or APIs. | `test-driven-development` | Write failing automated test first (RED), implement minimal code to pass (GREEN), then refactor. |
| **Subagent Task Delegation** | Independent work streams (e.g., UI frontend + API backend). | `subagent-driven-development` | Spawn subagents with strict contracts, isolated contexts, and defined deliverables. |
| **Completion Readiness** | All tasks executed; agent is about to declare success. | `verification-before-completion` | Run automated test suites and verify observable evidence before claiming completion. |

## Escalation Flow

```text
[Normal Agent Execution]
           │
           ▼
[Runtime Complexity Detected?]
     ├── NO  ──> Proceed with standard Fast-Path specialist workflow
     └── YES ──> Record issue in SESSION_FAILURES.md
                 Update .agent/context/BLACKBOARD.md
                 Invoke Superpower Skill (read SKILL.md)
                 Execute disciplined superpower protocol
                 Resume implementation with evidence proof
```


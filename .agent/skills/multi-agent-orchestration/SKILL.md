---
name: multi-agent-orchestration
description: Multi-agent coordination system with dynamic runtime complexity escalation to superpowers, blackboard context sharing, and dual-tier memory engineering. Use when coordinating multiple specialist agents, sharing context across agents, escalating on runtime complexity, or running parallel agent workflows.
license: Apache-2.0
metadata:
  version: "1.0.0"
---

# Multi-Agent Orchestration & Context Engineering

This skill defines the operational execution model for multi-agent systems in Antigravity. It governs how specialist agents collaborate, share context without token bloat, maintain shared memory, and dynamically escalate to Superpower skills when runtime complexity is detected.

## Core Pillars

1. **Dynamic Runtime Complexity Escalation:** When any agent encounters ambiguity, multi-file impact, repeated test failure, or architectural trade-offs, it immediately invokes the appropriate Superpower skill.
2. **Blackboard Context Sharing:** Agents exchange findings, invariants, and intermediate artifacts through `.agent/context/BLACKBOARD.md` and native subagent messaging.
3. **Context Engineering:** Token budget optimization, attention curve prioritization, and progressive disclosure to keep working memory lean.
4. **Memory Engineering:** Dual-tier cognitive memory: ephemeral short-term session memory (`SESSION_FAILURES.md`) and persistent architectural memory (`.agent/memory/ARCHITECTURE_MEMORY.md`).

## Quick Navigation

- [Superpower Escalation Matrix](references/superpower-escalation.md)
- [Context Engineering Guide](references/context-engineering.md)
- [Memory Engineering Protocol](references/memory-engineering.md)
- [Inter-Agent Communication Protocol](references/communication-protocol.md)

## Standard Multi-Agent Execution Flow

### Step 1: Intake & Triage
The primary agent or `orchestrator` analyzes the user prompt:
- If single-domain and low complexity: Execute directly via specialist agent (Fast-Path).
- If multi-domain or complex: Initialize the shared blackboard:
  ```powershell
  python .agent/skills/multi-agent-orchestration/scripts/blackboard.py init --objective "Build auth service"
  ```

### Step 2: Parallel or Sequential Dispatch
Assign discrete work items to specialist agents based on domain triggers:
- Subagents execute within isolated context windows to avoid bloating the parent conversation.
- Each subagent reports structured outcomes (Status, Discovered Invariants, Artifact Paths, Next Step).

### Step 3: Runtime Complexity Escalation Check
At every step, the active agent evaluates runtime indicators:
- If a test fails twice consecutively -> Self-escalate to `systematic-debugging` or `root-cause-tracing`.
- If an architectural trade-off is uncovered -> Self-escalate to `brainstorming`.
- If code modification begins on complex logic -> Self-escalate to `test-driven-development`.
- If a plan exceeds 3 steps -> Self-escalate to `writing-plans` and `executing-plans`.

### Step 4: Context Handoff
Before handing off to another agent, the active agent writes key discoveries to the blackboard:
```powershell
python .agent/skills/multi-agent-orchestration/scripts/blackboard.py add-invariant --key "AuthStrategy" --value "JWT with RS256"
```

### Step 5: Verification Gate
Before declaring completion, invoke `verification-before-completion` or run the verification suite:
```powershell
python .agent/scripts/test_intelligent_routing.py
```


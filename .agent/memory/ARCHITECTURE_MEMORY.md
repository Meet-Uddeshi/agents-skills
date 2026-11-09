# Persistent Workspace Memory

This document stores persistent architectural invariants, established patterns, and cross-session constraints across the repository. All agents query this memory before planning structural, architectural, or multi-file changes.

## System Invariants

1. **Agent Catalog Architecture:**
   - 108 Specialist Agents located in `.agent/agents/*.md`.
   - 365+ Domain Skills located in `.agent/skills/*/SKILL.md`.
   - Workspace rules located in `GEMINI.md`, `.agent/rules/GEMINI.md`, `.agent/rules/agent-matrix.md`, and `.agent/rules/multi-agent-system.md`.
   - Hard Rule File Cap: 24,000 bytes per rule file. Over-limit files are silently truncated by Antigravity. Always maintain rule files under 24 KB.

2. **Zero-Emoji Policy:**
   - Strict ban on decorative emojis across source code, comments, test names, logs, documentation, and commit messages.

3. **Multi-Agent Coordination Model:**
   - Communication: Blackboard architecture via `.agent/context/BLACKBOARD.md` and native Antigravity subagent messaging.
   - Escalation: Runtime complexity triggers immediate self-escalation to Superpower skills.
   - Dual-Tier Memory: Short-term ephemeral `SESSION_FAILURES.md` + long-term persistent `ARCHITECTURE_MEMORY.md`.


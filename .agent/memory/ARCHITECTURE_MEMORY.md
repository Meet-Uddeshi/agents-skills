# Persistent Workspace Memory

This document stores persistent architectural invariants, established patterns, and cross-session constraints across the repository. All agents query this memory before planning structural, architectural, or multi-file changes.

## System Invariants

1. **Agent Catalog Architecture:**
- 110 Specialist Agents located in `.agent/agents/*.md`.
   - 365+ Domain Skills located in `.agent/skills/*/SKILL.md`.
   - Workspace rules located in `GEMINI.md`, `.agent/rules/GEMINI.md`, `.agent/rules/agent-matrix.md`, and `.agent/rules/multi-agent-system.md`.
   - Hard Rule File Cap: 24,000 bytes per rule file. Over-limit files are silently truncated by Antigravity. Always maintain rule files under 24 KB.

2. **Zero-Emoji Policy:**
- Strict ban on decorative emojis across source code, comments, test names, logs, documentation, and commit messages.

3. **Multi-Agent Coordination Model:**
- Communication: Blackboard architecture via `.agent/context/BLACKBOARD.md` and native Antigravity subagent messaging.
   - Escalation: Runtime complexity triggers immediate self-escalation to Superpower skills.
   - Dual-Tier Memory: Short-term ephemeral `SESSION_FAILURES.md` + long-term persistent `ARCHITECTURE_MEMORY.md`.

4. **Universal Zero-Assumption Mandate:**
- If any agent has any doubt, ambiguity, or missing information needed to make a decision, the agent MUST pause and ask the user directly instead of guessing or blindly continuing.
   - Mandatory across all 110 agents, workflows, and automated scripts without exception.

5. **SQLite Context & Memory Engineering:**
- Persistent structured memory and coordination events stored in `.agent/memory/memory.db`.
   - Bounded indexed queries (`LIMIT 5`) prevent LLM context window saturation.
   - Full-text search (FTS5) enables instant semantic keyword retrieval.
   - Dual-mode synchronization guarantees human-readable Markdown files remain synchronized with high-performance SQLite storage.

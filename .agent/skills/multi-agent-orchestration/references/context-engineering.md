# Context Engineering for Multi-Agent Systems

Context is a finite, scarce resource. Context engineering guarantees that participating agents maintain high attention, prevent token exhaustion, and exchange rich signals without context dumps.

## 1. The Attention Curve Invariant

Attention degrades in long context windows, specifically in the middle third:
- **Head (Highest Attention):** Core mission, hard system constraints, active invariants, and input goal.
- **Middle (Lower Attention):** Supporting reference docs, code context, and intermediate logs.
- **Tail (Highest Attention):** Exact output schema, deliverables checklist, and final action constraint.

**Design Rule:** Always place critical operational rules and output formats at the head and tail of agent instructions.

## 2. Progressive Disclosure

Never ingest full directories or large source files upfront:
1. **Level 0 (Index):** Read the index or `SKILL.md` first.
2. **Level 1 (Targeted Subsection):** Read only the specific section or file matching the active need.
3. **Level 2 (Execution Artifact):** Run a script or subagent to extract distilled summaries rather than ingesting raw data.

## 3. Subagent Context Insulation

When an agent must perform intensive reconnaissance (such as scanning 200 files, analyzing AST trees, parsing large logs, or compiling):
- **Spawn a Subagent:** The subagent operates in an isolated context window.
- **Return Compact Synthesis:** The subagent returns at most 300 words containing:
  - Findings summary
  - Target file paths
  - Exact proposed diff or invariant
- The parent agent's context remains lean, clean, and unpolluted.

## 4. Anti-Patterns to Avoid

- Dumping full file contents when only 10 lines changed.
- Repeating already discovered facts in conversation prompts.
- Letting subagents run unconstrained loops without bounding token budgets.
- Omitting clear output formats at the end of prompt dispatches.


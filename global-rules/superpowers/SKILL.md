---
name: superpowers
description: >
  Superpowers agentic framework from obra/superpowers. Enforces disciplined software development
  methodology: process skills first (brainstorming, systematic debugging), Test-Driven Development (TDD),
  structured planning, execution, code reviews, and verification.
---

# Superpowers Agentic Framework

The Superpowers framework establishes a disciplined, test-driven, and systematic software engineering workflow for agentic coding.

## Core Rules of Engagement

1. **Check for Skills First**: Before taking ANY action or responding to any non-trivial user request, check available skills and invoke the relevant one.
2. **Brainstorming Before Coding**: Never jump straight into code for new features. Refine requirements, evaluate trade-offs, present design in manageable sections, and secure user approval.
3. **Systematic Debugging**: For bugs or unexpected behavior, systematically investigate root cause through the 4 phases before modifying code.
4. **Test-Driven Development (TDD)**: Always write failing tests first (RED), implement minimal code to pass (GREEN), then refactor (REFACTOR). Never write implementation code without a failing test.
5. **Rigorous Verification**: Always verify changes using automated tests or reproducible checks before declaring a task complete.

## Complete Skills Catalog

### 1. Development & Lifecycle
- `brainstorming` (`skills/brainstorming/SKILL.md`): Socratic design refinement before writing code or plans.
- `using-git-worktrees` (`skills/using-git-worktrees/SKILL.md`): Isolated workspaces on new branches with clean test baselines.
- `writing-plans` (`skills/writing-plans/SKILL.md`): Breaking approved designs into bite-sized (2-5 min) verifiable tasks.
- `executing-plans` (`skills/executing-plans/SKILL.md`): Batch plan execution with checkpoints and progress tracking.
- `subagent-driven-development` (`skills/subagent-driven-development/SKILL.md`): Dispatching subagents per task for fast iteration.
- `test-driven-development` (`skills/test-driven-development/SKILL.md`): Strict RED-GREEN-REFACTOR cycle.
- `requesting-code-review` (`skills/requesting-code-review/SKILL.md`): Reviewing against spec and plan before merging.
- `receiving-code-review` (`skills/receiving-code-review/SKILL.md`): Responding to and resolving code review feedback.
- `finishing-a-development-branch` (`skills/finishing-a-development-branch/SKILL.md`): Final verification and PR/merge cleanup.

### 2. Testing & Quality Assurance
- `condition-based-waiting` (`skills/condition-based-waiting/SKILL.md`): Async test patterns to prevent flakiness and race conditions.
- `testing-anti-patterns` (`skills/testing-anti-patterns/SKILL.md`): Identifying and avoiding bad testing habits and mock abuse.
- `defense-in-depth` (`skills/defense-in-depth/SKILL.md`): Multi-layer validation and sanitization.
- `verification-before-completion` (`skills/verification-before-completion/SKILL.md`): Evidence-based verification before completion claims.

### 3. Debugging & Troubleshooting
- `systematic-debugging` (`skills/systematic-debugging/SKILL.md`): 4-phase root cause analysis.
- `root-cause-tracing` (`skills/root-cause-tracing/SKILL.md`): Tracing bugs across execution boundaries and state pollution.
- `dispatching-parallel-agents` (`skills/dispatching-parallel-agents/SKILL.md`): Concurrently investigating 3+ independent failures.

### 4. Meta & Skill Management
- `using-superpowers` (`skills/using-superpowers/SKILL.md`): First response protocol and skill execution rules.
- `writing-skills` (`skills/writing-skills/SKILL.md`): Guide for authoring new agent skills.
- `testing-skills-with-subagents` (`skills/testing-skills-with-subagents/SKILL.md`): Testing and benchmarking skill effectiveness.
- `sharing-skills` (`skills/sharing-skills/SKILL.md`): Packaging and distributing skills across repositories.

### 5. Domain-Specific
- `deploying-payload-to-cloudflare` (`skills/deploying-payload-to-cloudflare/SKILL.md`): Deploying Payload CMS to Cloudflare Workers.
- `implementing-schema-org` (`skills/implementing-schema-org/SKILL.md`): Implementing Schema.org structured schemas.

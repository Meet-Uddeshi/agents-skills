# GRAVITAS Prompt Template

3-layer prompt assembly for optimal Gemini performance.
Every GRAVITAS task follows this structure.

---

## The 3-Layer System

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: System (static, load once, cacheable)          │
│  SKILL.md + references loaded only when needed           │
│  → Core protocol, 5 rules, tier classification           │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Task (per-invocation, specific)                │
│  Goal, files, constraints, output format                 │
│  → What to do, where, and how to report it              │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Context (delta for session/subagents)          │
│  Memory, prior findings, session failures               │
│  → What was learned, what failed, current state         │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 1: System Prompt (SKILL.md)

Load once. Cacheable. Contains the full GRAVITAS protocol.

**Contents:**
- 5 Non-negotiable rules
- Tier classification (0/1/2)
- Adaptive reasoning and budget profiles
- Compact recovery state
- Conditional delegation
- Writing protocol
- Output format
- Verification chains

**When to load:** At session start. Once per session.
**When NOT to reload:** Every message (unnecessary, wastes tokens).

---

## Layer 2: Task Prompt

Constructed fresh for each task. Maximum specificity.

### Template

```markdown
## Goal
[One sentence: exactly what to accomplish]

## Files (scope)
- Target: [exact path or "find with grep pattern"]
- Related: [files that need reading or may be affected]
- Tests: [test file path]

## Constraints
- [what NOT to do — specific]
- [what to keep unchanged]
- [scope limit: "only touch files in src/auth/"]

## Context (from recon or prior work)
- [key finding from reconnaissance]
- [specific line numbers if known]
- [recent git changes if relevant]

## Output Format
[exact format — with an example when non-obvious]

## Tier
[0 / 1 / 2] — [brief justification]
```

### Example: Bug Fix Task

```markdown
## Goal
Fix SESSION_TIMEOUT: change from 5_000ms to 30_000ms.
Users are being logged out after 5 seconds.

## Files
- Target: src/auth/session.ts (timeout constant is at line 23)
- Test: src/auth/session.test.ts (assertion at line 47 needs update)
- Config: tsconfig.json (strict mode — types must be correct)

## Constraints
- Only touch these 2 files
- Don't refactor session module (out of scope)
- Don't change other timeout values (there are 3 others — leave them)
- Conventional commit format: "fix: increase session timeout to 30s"

## Context
- Recon found: SESSION_TIMEOUT = 5_000 at session.ts:23
- Test at session.test.ts:47 asserts toBe(5000) — must update
- 2 middleware files import session.ts — they'll need full suite run
- Last change to auth.ts: 6 weeks ago (unrelated)

## Output Format
## What Changed
[files, lines, behavior]

## Evidence
[verbatim vitest output]

VERDICT: PASS

## Tier
1 — moderate, 2 files, clear scope, low risk
```

---

## Layer 3: Context Delta (for resumption and optional subagents)

Minimal context injected at spawn time or after context compression.

### For a conditional subagent

```markdown
## Session Context — [agent name]

### Memory
- SESSION_TIMEOUT at src/auth/session.ts:23 (confirmed via grep)
- Test at session.test.ts:47 (asserts old value — needs update)

### Session Failures
- Tried editing config.ts — wrong file, SESSION_TIMEOUT not there
  → Do NOT touch config.ts

### Current Task State
- Explore: complete (findings above)
- Plan: complete (change lines 23 and 47)
- General: in progress (your job)
- Verify: pending

### Baseline
47/47 tests pass before this change
```

### For Long Sessions (after context compression)

```markdown
## Session Summary — [timestamp]

### What we've established
- Bug: SESSION_TIMEOUT is 5_000 but should be 30_000
- Location: src/auth/session.ts:23
- Test impact: session.test.ts:47 asserts old value
- Scope confirmed: only 2 files need changing

### Session failures
- config.ts was a dead end — do not retry

### Status
General agent implementing now. Verify pending.
```

---

## Assembling the Full Prompt

### Tier 0 (trivial)
```
[Layer 1: SKILL.md — already loaded]
[Layer 2: task only — 3-5 lines]
```

### Tier 1 (standard)
```
[Layer 1: SKILL.md]
[Layer 2: full task template]
[Layer 3: memory + session failures if any]
```

### Tier 2 (high-stakes)
```
[Layer 1: SKILL.md]
[Layer 1+: adversarial-critique.md]
[Layer 2: full task template with Tier 2 extensions]
[Layer 3: full context delta]
[User checkpoint before execution]
```

---

## Subagent Prompt Construction

When spawning a specialized agent, give them a complete Layer 2 + Layer 3:

### Explore Dispatch
```markdown
## Task for Explore
**Goal:** Map [specific area] to answer: [question]
**Scope:** [directory or file pattern]
**Read:** [specific files if known]
**Return:**
  - File map: [file] → [what it contains + key lines]
  - Dependency graph: who imports what
  - Risk flags: ⚠️ anything unexpected
  - Git context: last 5 changes to affected files
Do NOT edit anything.
```

### Verify Dispatch
```markdown
## Task for Verify
**Goal:** Verify the [feature/fix] is correct.
**Scope:** [test files, source files]
**Baseline:** [N] tests passing before change
**Run:**
  tsc --noEmit && eslint . && vitest run
**Edge cases to check:** [list specific cases]
**Return:** VERDICT: PASS or VERDICT: FAIL with full output
```

---

## Quick Templates by Task Type

### Bug Fix
```
Goal: Fix [symptom] — [suspected cause]
Files: [target] + [test]
Constraint: Stay in these files
Output: What Changed + Evidence + VERDICT
Tier: 1
```

### Feature Addition
```
Goal: Add [feature] to [module]
Files: [implementation files] + [test files]
Constraint: [scope limits]
Output: Full ## sections + VERDICT
Tier: 1 or 2 depending on auth/security involvement
```

### Refactor
```
Goal: Refactor [what] to [why]
Files: [all affected files — be exhaustive]
Constraint: No behavior changes, tests must pass unchanged
Output: What Changed + Evidence (before/after pass counts) + VERDICT
Tier: 2 if production module, 1 otherwise
```

### Security Fix
```
Goal: Fix [vulnerability] in [location]
Files: [target] + [tests] + [related modules]
Constraint: Don't introduce new endpoints. Don't change auth logic except the fix.
Output: Threat model + Fix + Security tests + VERDICT
Tier: 2 always
```

---

# 🚀 Intelligent Prompt Practices & Trigger Playbook

Use these prompt patterns to get 100% precision from Antigravity's auto-routing engine without having to memorize agent names.

## 1. Core Prompt Principles for Auto-Routing

1. **State the Tech Stack & Domain Specifically**:
   - Generic: "Build an API" -> Antigravity asks Socratic clarifying questions.
   - Specific: "Create a FastAPI router with Pydantic v2 schemas and async Postgres query" -> Instantly auto-triggers `fastapi-reviewer` + `database-architect`, auto-loads `fastapi-patterns` and `database-design`.
2. **State Intent (Build, Debug, Review, Test, Audit, Simplify)**:
   - "Audit auth controller for SQL injection, IDOR, and OWASP vulnerabilities" -> Instantly auto-triggers `security-auditor` + `security-reviewer`, auto-loads `vulnerability-scanner`.
   - "Refactor this 300-line messy function to be clean, simple, and under 50 lines" -> Instantly auto-triggers `code-simplifier`, auto-loads `clean-code` and `karpathy-guidelines`.
3. **Multi-Domain Requests**:
   - "Build a SaaS billing dashboard with React Tailwind frontend, Stripe webhook API, and Postgres schema" -> Instantly triggers `orchestrator`, which coordinates `frontend-specialist`, `backend-specialist`, and `database-architect`.

---

## 2. Real-World Prompt Examples & What Gets Auto-Triggered

### Example 1: Modern Frontend UI/UX
```markdown
Prompt:
"Create a responsive analytics card component in React with Tailwind CSS v4, supporting dark mode and keyboard accessibility."

Auto-Triggered Agents:
🤖 Applying knowledge of @frontend-specialist + @a11y-architect...
Auto-Loaded Skills:
- frontend-design
- react-best-practices
- tailwind-patterns
- accessibility
- clean-code
```

### Example 2: High-Performance Backend API
```markdown
Prompt:
"Implement an async FastAPI endpoint for user profile updates with Pydantic validation, JWT auth, and rate limiting."

Auto-Triggered Agents:
🤖 Applying knowledge of @fastapi-reviewer + @security-auditor...
Auto-Loaded Skills:
- fastapi-patterns
- api-patterns
- security-review
- clean-code
```

### Example 3: Deep Database Query Tuning & Migration
```markdown
Prompt:
"Analyze why this PostgreSQL query is doing a sequential scan on 1M rows, design the index strategy, and write a safe Prisma migration."

Auto-Triggered Agents:
🤖 Applying knowledge of @database-reviewer + @database-architect...
Auto-Loaded Skills:
- database-design
- postgres-patterns
- prisma-patterns
```

### Example 4: Mobile App with Offline Storage
```markdown
Prompt:
"Build a cross-platform Flutter screen for note taking with Riverpod state management and offline SQLite caching."

Auto-Triggered Agents:
🤖 Applying knowledge of @mobile-developer + @flutter-reviewer...
Auto-Loaded Skills:
- mobile-design
- dart-flutter-patterns
- flutter-dart-code-review
```

### Example 5: Strict TDD Feature Implementation
```markdown
Prompt:
"Add coupon code discount validation to the checkout service using strict TDD. Write the failing unit tests first."

Auto-Triggered Agents:
🤖 Applying knowledge of @tdd-guide + @test-engineer...
Auto-Loaded Skills:
- test-driven-development
- testing-patterns
- tdd-workflow
```

### Example 6: Compiler or Build Error Resolution
```markdown
Prompt:
"My Next.js 15 build is failing with Turbopack module resolution error on dynamic server imports. Fix the build."

Auto-Triggered Agents:
🤖 Applying knowledge of @react-build-resolver + @debugger...
Auto-Loaded Skills:
- nextjs-turbopack
- systematic-debugging
```

### Example 7: Anti-Overengineering & Clean Code Refactoring
```markdown
Prompt:
"This 400-line service class is bloated and overengineered. Simplify it following Karpathy guidelines and clean code, remove dead code, and ensure tests pass."

Auto-Triggered Agents:
🤖 Applying knowledge of @code-simplifier + @refactor-cleaner...
Auto-Loaded Skills:
- clean-code
- karpathy-guidelines
- refactor-cleaner
```

### Example 8: Security & Penetration Testing Audit
```markdown
Prompt:
"Perform a comprehensive security audit of our authentication and session handling code for OWASP Top 10 vulnerabilities, session fixation, and token leakage."

Auto-Triggered Agents:
🤖 Applying knowledge of @security-auditor + @penetration-tester...
Auto-Loaded Skills:
- vulnerability-scanner
- red-team-tactics
- security-review
- defense-in-depth
```

### Example 9: Full DevOps & Docker Setup
```markdown
Prompt:
"Create a production-ready Dockerfile, docker-compose setup, and GitHub Actions CI/CD pipeline with security scanning for our Node.js app."

Auto-Triggered Agents:
🤖 Applying knowledge of @devops-engineer...
Auto-Loaded Skills:
- deployment-procedures
- docker-patterns
- server-management
```

### Example 10: Multi-Domain Full-Stack Orchestration
```markdown
Prompt:
"I want to build a real-time collaborative whiteboarding web application with WebSockets, Canvas, and user presence."

Auto-Triggered Agents:
🤖 Applying knowledge of @orchestrator + @project-planner...
Behavior:
- Halts at Socratic Gate (asks 3 clarifying architecture questions)
- Generates 4-phase architecture and bite-sized plan
- Coordinates @frontend-specialist and @backend-specialist sequentially
```

### Example 11: System Architecture, Process Flow & ER Diagrams (Archify)
```markdown
Prompt:
"Draw high level architecture of our distributed microservices platform, including an ER diagram for billing and a process flow diagram for order fulfillment."

Auto-Triggered Agents:
🤖 Applying knowledge of @architect + @database-architect...
Auto-Loaded Skills:
- archify
- architecture
- database-design
Behavior:
- Selects diagram types: architecture, workflow (process flow), and erd
- Uses archify to generate standalone interactive HTML diagrams with inline SVG and dark/light themes
- Runs archify verification and delivery gates
```

---

## 3. Explicit Mentions & Overrides

When you want to guarantee a specific specialist without relying on keyword detection:
- Use `@agent-name`: e.g., `@rust-reviewer check this async Mutex implementation for deadlocks`
- Use slash commands: e.g., `/brainstorm`, `/create`, `/plan`, `/test`, `/debug`, `/ui-ux-pro-max`
- Override auto-routing: An explicit `@agent-name` in the prompt immediately takes top priority over automatic pattern matching.


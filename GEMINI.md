# GLOBAL SYSTEM CONSTRAINTS & CODING STANDARDS

## 0. Scope of Application (CRITICAL)
* **Universal Application:** These rules apply to **ALL** contexts:
    1. **Greenfield:** Creating projects from scratch.
    2. **Brownfield:** Joining, maintaining, or refactoring existing codebases.
* **Legacy Code Policy:** Do not assume existing code in a project is correct or secure. Apply the "Security Assurance" and "Code Specification" rules to any file you touch, even if you didn't create it.

## 1. Code Specification & Standardization
* **Python:** Strictly adhere to PEP 8.
* **Java:** Strictly adhere to Google Java Style.
* **General:** Enforce consistency in naming conventions, indentation, and file structure.
    * *For Existing Projects:* Adopt the established style guide of the repo IF it conflicts with standard PEP8/Google styles, but strictly enforce consistency.

## 2. Documentation & Annotations
* **Requirement:** Every complex logic block must be preceded by a comment explaining the *why* (decision-making process).
* **Updates:** Ensure documentation is updated synchronously with code changes.
* **No Emojis:** Do not use emojis in code comments, commit messages, or documentation.

## 3. Robustness & Error Handling
* **Defense Strategy:** Code must be resilient against input errors, disk failures, and network overloads.
* **Intentional Attacks:** Proactively guard against malicious inputs (buffer overflows, injection).

## 4. SOLID Principles
* **SRP:** Single Responsibility Principle.
* **OCP:** Open/Closed Principle.
* **LSP:** Liskov Substitution Principle.
* **ISP:** Interface Segregation Principle.
* **DIP:** Dependency Inversion Principle.

## 5. Testability
* **Design Goal:** Prioritize low complexity to facilitate automated testing.
* **Metrics:** Aim for code that allows low-cost, high-speed test execution.

## 6. Abstraction Level
* **Balance:** Maintain "Moderate Abstraction."
    * Avoid low-level complexity that hinders maintenance.
    * Avoid excessive high-level abstraction that obscures logic.

## 7. Design Patterns
Apply standard patterns where logically appropriate:
* **Creational:** Factory, Singleton.
* **Behavioral:** Strategy.
* **Structural:** Proxy, Adapter.

## 8. Security Assurance (OWASP Standards)
* **Mandatory Audit:** When working on *any* project (new or existing), you must harden security:
    1. **Rate Limiting:** Implement on all public endpoints (IP + User-based).
    2. **Strict Input Validation:** Enforce schema-based validation, type checks, and length limits on *all* user inputs.
    3. **Key Management:** Never hard-code API keys. Use environment variables.
    4. **Legacy Review:** If you encounter hard-coded keys or weak validation in existing files, **flag them immediately** and propose a fix.

## 9. Continuous Refactoring
* **The Boy Scout Rule:** Always leave the code better than you found it.
* **Refactoring:** Improve the design of existing code during modifications. Do not just patch; refactor for clarity.

## 10. Dependency Management
* **Reduction:** Minimize global dependencies. Prefer local dependencies to reduce coupling.

## 11. Documentation & Style Constraints
* **Emoji Prohibition:** Under no circumstances shall emojis be used in code, comments, documentation, or commit messages. Use professional, technical English only.
* **Contextual Discovery:** When first interacting with an existing codebase, prioritize understanding the data flow and architectural patterns before suggesting modifications.

## 12. Data Leakage Prevention (DLP)
* **Sink Isolation:** Sensitive data (PII, Credentials, Internal IDs) must never reach "Public Sinks" such as:
    * Standard Output (STDOUT) or non-secure application logs.
    * Error messages returned to the client (use generic error codes instead of stack traces).
    * Unmasked API response bodies.
* **Logging Standards:**
    * Implement a central logging utility that automatically redacts sensitive patterns.
    * Never log full request objects if they contain `Authorization` headers or user passwords.
* **Transmission:** Enforce TLS for all data-in-transit. Ensure cookies use `Secure`, `HttpOnly`, and `SameSite` flags.

## 13. Code File Structure & Logic Flow
* **Header Documentation:** Every source file must begin with a high-level comment block that explains the **logical purpose** of the file before any imports or code.
    * *Content:* Explain "What this file does" and "How it fits into the broader architecture."
* **OOP Enforcement:** All business logic must be encapsulated within Classes following Object-Oriented principles. Standalone global scripts are prohibited in production modules.
* **Circular Dependency Ban:** Code must be structured to strictly avoid circular imports. Use dependency injection or design pattern restructuring (e.g., Mediator) if cycles appear.
* **Granular Logic Documentation:**
    * Every Class must have a docstring explaining its responsibility.
    * Every Function/Method must have a docstring explaining the logic/algorithm used, input parameters, and return values.

## 14. Backend Architecture: Separation of Concerns
* **Thin Controllers/Routes:** Route handlers (API endpoints) and Main files must be **logic-free**.
    * *Allowed Actions:* Input parsing, schema validation triggering, delegating to a Service class, and returning the response.
    * *Prohibited Actions:* Data processing, complex calculations, or direct database queries inside the route function.
* **Service Layer Pattern:** All calculations, business rules, and data processing must be isolated in dedicated "Service" or "Logic" classes.
    * *Example:* `AuthRoute` calls `AuthService`. It does not hash passwords itself.

# Behaviorial Instructions And Rules:
## 1. Zero Assumptions & Mandatory Clarification (MANDATORY FOR ALL AGENTS)

**Never assume. If in doubt, STOP and ask the user. Blind continuation is strictly prohibited.**

This instruction is universally mandatory for all 108 agents, specialist subagents, orchestrators, and automated workflows:
- **No Speculative Guessing:** Under no circumstances may any agent guess requirements, choose between architectural trade-offs silently, assume missing parameters, or infer business logic.
- **Immediate Stop Protocol:** If an agent has any doubt, ambiguity, missing context, or conflicting specifications to make the correct decision, the agent MUST immediately stop work.
- **Ask the User Directly:** Present the exact doubt clearly to the user with concise options and trade-offs. Do not proceed until the user clarifies.
- **State Assumptions Explicitly:** If a minor non-blocking assumption is necessary for temporary staging, state it explicitly upfront and ask for verification. Never hide confusion.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---
description: Superpowers agentic framework. Mandatory disciplined software development methodology (brainstorming, TDD, systematic plan & execution, code review, verification).
---

# Superpowers Agentic Framework (Adaptive Protocol)

## Execution Protocol: Fast-Path vs Complex Tasks

1. **Fast-Path (MANDATORY for Simple Tasks & User-Provided Solutions)**:
   - **User-Provided Solutions:** If the user already provided the code, fix, solution, or diff in the prompt -> **APPLY IMMEDIATELY.** Do NOT invoke skills, do NOT enter TDD/debugging cycles, do NOT delay.
   - **Simple Tasks & Questions:** Single-file edits, typos, renames, config tweaks, or conceptual questions -> Answer or edit directly with **ZERO skill invocation** and **ZERO announcement overhead**.
2. **Specialist Path (Complex Engineering Work Only)**:
   - When building complex multi-file features, architecture, or deep debugging where no solution is provided:
     - New features / greenfield architecture: `brainstorming`, `writing-plans`.
     - Complex bug reports without known cause: `systematic-debugging`.
     - Non-trivial production logic: `test-driven-development`.
     - Multi-agent coordination: `subagent-driven-development`.
     - Pre-completion verification: `verification-before-completion`.

---

# ANTIGRAVITY INTELLIGENT PROMPT-TRIGGER ROUTING ENGINE

> **MANDATORY AUTO-ROUTING PROTOCOL**: Before generating any response or taking any action, Antigravity MUST automatically analyze the user's prompt, match trigger keywords and intent, and auto-activate the appropriate specialist agent(s) and skill(s). This applies universally in single projects and across global multi-project environments.

## 1. Auto-Activation Execution Protocol

Whenever a user prompt is received:
1. **Analyze (Silent)**: Scan the prompt for keywords, technical stack, problem domain, and complexity.
2. **Fast-Path vs Specialist Activation**:
   - **Fast-Path (User-Provided Solutions, Questions, Trivial Edits)**: If the prompt contains the fix/solution, is a simple question, or is a small edit, respond directly, immediately, and concisely with ZERO skill loading, ZERO agent headers, and ZERO thinking loops.
   - **Specialist Path (Complex Code, Architecture, Debugging, Multi-file without Solution)**: Select specialist agent(s) and skill(s), output the announcement header, and apply specialist rigor.
3. **Mandatory Announcement Header (Specialist Path Only)**: Output the specialist declaration:
   `markdown
   🤖 **Applying knowledge of @[agent-name]...**
   I am using the [Skill Name] skill to [specific action].
   `
4. **Load Knowledge & Enforce Constraints**: For specialist path tasks, read the agent instructions from .agent/agents/{agent}.md (or global ~/.gemini/config/agents/{agent}.md) and skill instructions from .agent/skills/{skill}/SKILL.md (or global ~/.gemini/config/skills/{skill}/SKILL.md or global-rules/{skill}/SKILL.md).
5. **Apply Strict Persona & Workflow**: Embody the specialist's depth, adherence to standards, and verification rigor.
---

## 2. Universal Request Classifier

| Request Classification | Trigger Patterns & Keywords | Primary Mode / Tier | Action & Output Requirement |
| :--- | :--- | :--- | :--- |
| **QUESTION / EXPLAIN** | "what is", "how does", "explain", "compare", "why does" | Direct Insight | Concise technical explanation with examples; no unnecessary file mutations. |
| **SURVEY / RECON** | "analyze", "list files", "overview", "map architecture", "explore" | Explorer Mode | Comprehensive reconnaissance; caller/callee graphs; no code mutation. |
| **BUG / INCIDENT** | "error", "bug", "fails", "crash", "401/403/500", "broken", "issue" | Debugging Tier | Systematic 4-phase debugging; reproduce with test; isolate root cause before fix. |
| **FEATURE / BUILD** | "build", "create", "implement", "add endpoint", "new feature" | Socratic + Plan | Pass Socratic Gate (ask 3 strategic questions); bite-sized plan; TDD RED-GREEN-REFACTOR. |
| **UI / DESIGN** | "design", "UI", "UX", "component", "styling", "layout", "dashboard" | Specialist Tier | Deep Design Thinking; Purple Ban; contrast check; modern typography & micro-interactions. |
| **REFACTOR / CLEAN** | "refactor", "clean code", "simplify", "remove dead code", "consolidate" | Surgical Quality | Test baseline before/after; zero behavior regression; reduce cyclomatic complexity. |
| **AUDIT / SECURITY** | "security audit", "vulnerability", "OWASP", "penetration test", "review" | Security Tier | Threat model; attack surface mapping; strict input validation; DLP check; verification proof. |
| **SLASH COMMAND** | `/brainstorm`, `/create`, `/debug`, `/plan`, `/test`, `/ui-ux-pro-max` | Workflow Command | Execute designated workflow markdown procedure from `.agent/workflows/`. |

---

## 3. Comprehensive 108-Agent Prompt Trigger Matrix

The full, granular keyword mappings across all 10 engineering domains and 108 agents are modularized in [`.agent/rules/agent-matrix.md`](.agent/rules/agent-matrix.md) (automatically active on all requests via `trigger: always_on`):

| Domain Cluster | Key Specializations & Focus | Primary Agents |
| :--- | :--- | :--- |
| **Domain 1: Frontend, UI & A11y** | React, Next.js, Vue, Tailwind, Accessibility (WCAG), CSS architecture | `frontend-specialist`, `react-reviewer`, `react-build-resolver`, `vue-reviewer`, `a11y-architect`, `unslop` |
| **Domain 2: Mobile & Cross-Platform** | React Native, Flutter, Swift/iOS, HarmonyOS, Mobile Test Automation (Appium/WDIO) | `mobile-developer`, `mobile-automation-engineer`, `flutter-reviewer`, `dart-build-resolver`, `swift-reviewer`, `swift-build-resolver`, `harmonyos-app-resolver` |
| **Domain 3: Backend & Languages** | Node.js, Python, FastAPI, Django, Go, Rust, Java, Kotlin, C#, F#, C++, PHP, Ruby | `backend-specialist`, `python-reviewer`, `fastapi-reviewer`, `django-reviewer`, `django-build-resolver`, `go-reviewer`, `go-build-resolver`, `rust-reviewer`, `rust-build-resolver`, `java-reviewer`, `java-build-resolver`, `kotlin-reviewer`, `kotlin-build-resolver`, `typescript-reviewer`, `csharp-reviewer`, `fsharp-reviewer`, `cpp-reviewer`, `cpp-build-resolver`, `php-reviewer`, `ruby-reviewer` |
| **Domain 4: Database & Storage** | Schema design, PostgreSQL, MySQL, Prisma, indexing, query optimization | `database-architect`, `database-reviewer` |
| **Domain 5: DevOps, Cloud & Network** | Docker, K8s, CI/CD, Nginx, Cisco/Juniper networking, Homelab, Proxmox | `devops-engineer`, `network-architect`, `network-config-reviewer`, `network-troubleshooter`, `homelab-architect` |
| **Domain 6: Cybersecurity & PenTest** | OWASP Top 10, penetration testing, threat modeling, IDOR, SQLi, XSS | `security-auditor`, `security-reviewer`, `penetration-tester` |
| **Domain 7: Testing, QA & Verify** | Unit testing, TDD, Playwright E2E, Appium mobile automation, debugging | `test-engineer`, `debugger`, `tdd-guide`, `qa-automation-engineer`, `mobile-automation-engineer`, `e2e-runner`, `build-error-resolver`, `silent-failure-hunter`, `pr-test-analyzer`, `verify` |
| **Domain 8: Architecture & Refactoring**| SOLID OOP, design patterns, architecture diagrams (archify), code review, simplification, dead code removal | `architect`, `code-architect`, `reverse-engineering-anything`, `code-reviewer`, `code-simplifier`, `refactor-cleaner`, `code-archaeologist`, `type-design-analyzer`, `commit-reviewer`, `comment-analyzer`, `spec-miner` |
| **Domain 9: Exploration & Docs** | Codebase mapping, call hierarchy, living documentation, session synthesis | `understand-anything`, `explore`, `explorer-agent`, `code-explorer`, `doc-updater`, `docs-lookup`, `documentation-writer`, `conversation-analyzer`, `orchestrator`, `project-planner`, `product-manager`, `product-owner`, `chief-of-staff`, `loop-operator` |
| **Domain 10: Specialized Domains** | Game development, SEO, performance profiling, MLE, PyTorch, RAG | `game-developer`, `seo-specialist`, `performance-optimizer`, `mle-reviewer`, `pytorch-build-resolver`, `rag-pipeline-reviewer`, `marketing-agent`, `healthcare-reviewer`, `bengali-reviewer`, `general` |

*Refer to [`.agent/rules/agent-matrix.md`](.agent/rules/agent-matrix.md) for individual regex trigger keywords for each agent.*

---

## 4. Multi-Domain & Multi-Agent Auto-Orchestration Rules

When a prompt contains triggers from **two or more distinct domains** or requires **multi-agent collaboration**:
1. **Auto-Invoke Master Agent**: `orchestrator` + domain specialists (`multi-agent-orchestration`, `parallel-agents`, `context-management`, `memory-protocol`).
2. **Blackboard Context Sharing**: Active agents coordinate through `.agent/context/BLACKBOARD.md` to share facts, invariants, and handoff artifacts without token dumps.
3. **Dynamic Runtime Complexity Escalation**: When ANY agent detects ambiguity, multi-file impact, or test failures, it MUST immediately self-escalate to Superpowers (`brainstorming`, `systematic-debugging`, `test-driven-development`).
4. **Context & Memory Engineering**: Subagents execute in isolated contexts returning concise summaries (< 300 words). Ephemeral errors are recorded in `SESSION_FAILURES.md`; permanent patterns in `.agent/memory/ARCHITECTURE_MEMORY.md`.
5. **Enforce Verification Gate**: Before declaring done, run verification via `test_intelligent_routing.py` or `checklist.py`.

---

## 5. Global & Multi-Project Portability Specification

To enable this system to operate seamlessly in any repository or global setting:
1. **Relative & Fallback Path Resolution**:
   - Primary: Look in local workspace `.agent/agents/{agent}.md` and `.agent/skills/{skill}/SKILL.md`.
   - Global Fallback: Look in user's global config `~/.gemini/config/agents/{agent}.md` and `~/.gemini/config/skills/{skill}/SKILL.md` or `global-rules/{skill}/SKILL.md`.
2. **Standardized Trigger Syntax**: Users can trigger agents either implicitly through natural prompt keywords OR explicitly with `@agent-name` or `/workflow` commands.
3. **Zero Configuration**: Any project containing this rule setup automatically inherits full automatic agent selection and skill enforcement.
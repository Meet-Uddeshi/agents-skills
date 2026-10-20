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
## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

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

# Superpowers Agentic Framework

## Mandatory Execution Rules

1. **Invoke relevant skills BEFORE any response or action** — check the skills registry before answering clarifying questions, exploring codebases, or writing any code.
2. **First Response Protocol**: If any skill might apply to what you are doing, read the skill (`view_file` on its `SKILL.md`) and follow it exactly.
3. **Brainstorming first (`brainstorming`)**: For new features ("Let's build X"), brainstorm and refine requirements before writing code or planning.
4. **Systematic Debugging first (`systematic-debugging`, `root-cause-tracing`)**: For bug reports or test failures, investigate root cause systematically across the 4 phases before editing code.
5. **Test-Driven Development (`test-driven-development`)**: Always write failing tests first (RED), implement minimal code to pass (GREEN), then refactor (REFACTOR). Watch tests fail before writing implementation.
6. **Bite-Sized Planning & Execution (`writing-plans`, `executing-plans`, `subagent-driven-development`)**: Break designs into 2-5 minute tasks with explicit verification steps.
7. **Code Review & Quality Gates (`requesting-code-review`, `receiving-code-review`)**: Review against plan and quality standards before merging.
8. **Verification Before Completion (`verification-before-completion`)**: Provide concrete test/execution evidence before claiming any task is complete.
9. **Testing Reliability (`condition-based-waiting`, `testing-anti-patterns`, `defense-in-depth`)**: Avoid flaky timeouts, mock abuse, and brittle assertions.
10. **Branch Lifecycle (`using-git-worktrees`, `finishing-a-development-branch`)**: Isolate work and verify clean baselines.


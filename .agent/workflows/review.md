---
description: Comprehensive code review and quality gate workflow. Check correctness, performance, maintainability, type safety, test coverage, and security.
---

# /review - Automated Code Review & Quality Gate Workflow

$ARGUMENTS

---

## Purpose

Perform structured, multi-dimensional code reviews on pull requests, commits, or files. Enforces zero emojis, clean architecture, minimal dependencies, strong typing, and comprehensive test coverage.

---

## Sub-commands

```text
/review pr                             - Review current git diff / pull request changes
/review file [path]                    - Deep review of single source file or module
/review security                       - Target OWASP, injection vulnerabilities, and secret leaks
/review performance                    - Analyze algorithmic complexity, N+1 queries, and memory leaks
```

---

## Standard 6-Step Implementation Workflow

1. **Context & Scope Identification:**
   - Inspect git diff or target files to understand intent, modified surfaces, and affected dependents.
   - Read relevant architecture records from `.agent/memory/ARCHITECTURE_MEMORY.md`.

2. **Correctness & Logic Verification:**
   - Verify edge cases (null/undefined handling, empty collections, integer overflow, async timeouts).
   - Check error propagation, exception boundaries, and transaction rollbacks.

3. **Type Safety & Maintainability:**
   - Check strict typing (avoid `any`, enforce exhaustive switches on discriminated unions).
   - Flag excessive cyclomatic complexity (functions over 50 lines, deep nesting > 3 levels).

4. **Security & Vulnerability Check:**
   - Verify sanitized inputs, parameterized queries, authorization checks, and safe dependency imports.
   - Scan for hardcoded credentials, secret tokens, and sensitive logs.

5. **Test Coverage & Regression Protection:**
   - Confirm new code has corresponding unit, integration, or mobile/E2E tests.
   - Verify negative test assertions and error case coverage.

6. **Generate Structured Review Findings:**
   - Output categorized findings: Blocker (P0), Improvement (P1), Polish (P2).
   - Provide concrete drop-in code suggestions with file and line references.


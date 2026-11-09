---
description: Full spectrum security, accessibility, performance, and dependency vulnerability audit.
---

# /audit - Multi-Dimensional System Audit Workflow

$ARGUMENTS

---

## Purpose

Audit software projects across security posture, accessibility compliance, performance bottlenecks, and dependency supply chain vulnerabilities.

---

## Sub-commands

```text
/audit security                        - Audit codebase for OWASP vulnerabilities, secret leaks, and misconfigurations
/audit a11y                            - Audit UI components for WCAG 2.1 AA compliance, ARIA attributes, and keyboard nav
/audit perf                            - Audit bundle size, Core Web Vitals, memory consumption, and slow queries
/audit deps                            - Audit package dependencies for CVEs, outdated versions, and license compliance
```

---

## Standard 6-Step Implementation Workflow

1. **Pre-Flight Environment Inventory:**
   - Detect package managers (`package.json`, `pnpm-lock.yaml`, `requirements.txt`, `Cargo.lock`, `go.sum`).
   - Identify web frameworks, mobile SDKs, and build tooling.

2. **Automated Static Analysis:**
   - Execute linter and security scanners (`npm audit`, `pip-audit`, `cargo audit`).
   - Scan source code for exposed API keys, private tokens, or hardcoded sensitive URLs.

3. **Accessibility (a11y) Evaluation:**
   - Check semantic HTML elements (`<main>`, `<nav>`, `<button>` vs `<div>`).
   - Validate color contrast ratios (minimum 4.5:1 for normal text, 3:1 for large text).
   - Test keyboard focus order, trap handling, and aria live regions.

4. **Performance & Resource Profiling:**
   - Measure bundle chunk sizes, tree-shaking efficacy, dynamic import boundaries.
   - Profile database queries for missing indexes and unindexed joins.

5. **Risk Classification & Triage:**
   - Assign severity ratings (Critical, High, Medium, Low) based on CVSS scoring and operational impact.
   - Filter false positives with contextual validation.

6. **Generate Remediation Plan:**
   - Output structured remediation roadmap prioritized by severity.
   - Record systemic risks in `.agent/memory/ARCHITECTURE_MEMORY.md`.


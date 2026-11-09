---
description: Mobile test automation workflow. Guides the creation, maintenance, and architectural auditing of mobile test cases, screen objects, and locators.
---

# /mobile-test - Mobile Automation Workflow

$ARGUMENTS

---

## Purpose

Automate, inspect, and maintain enterprise mobile test automation suites across Android and iOS using WebdriverIO, Appium, and Cucumber BDD.

---

## Sub-commands

```text
/mobile-test audit               - Audit mobile automation codebase for architectural anti-patterns
/mobile-test screen [name]       - Scaffold a new Screen Object extending BaseScreen
/mobile-test spec [feature]      - Scaffold a new mobile test spec / feature with externalized data
/mobile-test triage [failure]    - 5-layer diagnostic triage of mobile test execution failure
```

---

## Standard 8-Step Implementation Workflow

1. **Understand Test Intent:** Review functional requirements, preconditions, expected outcomes, and target platform (`Android` / `iOS`).
2. **Inspect Appium Hierarchy:** Analyze live screen hierarchy via Appium Inspector to capture verified `accessibilityId` or unique `resource-id` landmarks.
3. **Configure Test Data:** Externalize scenario inputs, credentials, and verification values into `test-case-data` / `TestDataService`.
4. **Define Locators:** Add primary stable accessibility IDs and structured fallback chains in selector repository files.
5. **Implement Screen Object:** Extend `BaseScreen`, encapsulate actions and readiness checks (`isLoaded()`, `waitUntilLoaded()`), avoid hardcoded assertions.
6. **Implement Step Definitions / Specs:** Write thin cucumber steps or specs calling screen methods and asserting outcomes.
7. **Verify Quality Gates:** Run `python .agent/skills/mobile-automation/scripts/mobile_framework_audit.py` to ensure zero hard sleeps, no brittle index XPaths, and clean typing.
8. **Execute Focused Run:** Run test targeting the specific test case ID or spec file.


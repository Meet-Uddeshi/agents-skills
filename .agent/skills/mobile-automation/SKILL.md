---
name: mobile-automation
description: Production-grade mobile test automation architecture standards for WebdriverIO, Appium, Android UiAutomator2, iOS XCUITest, and Maestro. Covers layered utility design (WaitUtils, MobileActions, GestureUtils, ScrollUtils, LoadingUtils, BaseScreen), resilient locator strategies, Screen Object Model, and enterprise framework quality gates.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile Automation Framework Architecture

Standardized principles for building maintainable, deterministic, and enterprise-ready mobile test automation frameworks across Android and iOS.

---

## 1. Layered Mobile Utility Architecture

The mobile utility layer provides reusable, screen-agnostic automation helpers for screen objects and specs. Utilities must never duplicate WebdriverIO or Appium native behavior, nor contain hardcoded screen selectors.

### 1.1 Utility Responsibility Matrix

| Utility | Primary Responsibility | Depends On | Prohibited Contents | Usage Pattern |
| :--- | :--- | :--- | :--- | :--- |
| `WaitUtils` | Primitive synchronization for displayed, hidden, existing, clickable, enabled, and custom conditions. | WebdriverIO `browser` / Appium element wait APIs. | Screen selectors, business assertions, user actions, or gestures. | Screen classes wait for stable UI state before asserting or interacting. |
| `MobileActions` | User-level element actions (tap, type, clear, text/attribute reads, keyboard management). | `WaitUtils`. | Scroll workflows, gesture primitives, flow orchestration, or loader policies. | Screen classes invoke actions directly or through `BaseScreen`. |
| `GestureUtils` | Physical mobile gestures (swipe, element swipe, long press, coordinate tap, drag). | `WaitUtils`. | High-level scroll search workflows, business validation, or loading waits. | Specialized screens invoke gestures when native gestures are required. |
| `ScrollUtils` | High-level scroll workflows for discovering visible text or elements using bounded swipes. | `GestureUtils`, `WaitUtils`. | Primitive action methods, screen-specific selectors, or loader logic. | Screens scroll to a target before interacting or asserting visibility. |
| `LoadingUtils` | Synchronizes on loading indicators/spinners disappearing without hardcoded locators. | `WaitUtils`. | Hardcoded spinner selectors, screen readiness checks, actions, or gestures. | Screens pass one or more loader selectors and wait for loading completion. |

### 1.2 Architectural Dependency Diagram

```text
Screen Objects / Step Definitions / Specs
                   │
                   ▼
        BaseScreen Orchestration
                   │
    ┌──────────────┼──────────────┬──────────────┐
    ▼              ▼              ▼              ▼
MobileActions  ScrollUtils   LoadingUtils    WaitUtils
    │              │              │              │
    │              ▼              │              │
    │         GestureUtils        │              │
    │              │              │              │
    └──────────────┴──────┬───────┴──────────────┘
                          ▼
                      WaitUtils
                          │
                          ▼
           WebdriverIO / Appium Driver
```

### 1.3 Contributor Rules for Utilities
1. **Screen-Agnostic Design:** Selectors belong strictly in screen objects or dedicated selector repository files. Never place selectors inside utility classes.
2. **Zero Hard Waits:** Strictly prohibit `browser.pause()` or fixed `sleep()` calls. All waits must be bounded, condition-driven synchronization via `WaitUtils`.
3. **Composition Hierarchy:** Workflow utilities compose lower-level utilities:
   - `LoadingUtils` -> `WaitUtils`
   - `ScrollUtils` -> `GestureUtils` + `WaitUtils`
   - `MobileActions` -> `WaitUtils`
4. **Tenant & Brand Agnostic:** Never hardcode tenant, OpCo, brand, or environment logic into utilities. Pass selectors, timeouts, and options from caller screens.
5. **Bounded Swipes:** All scroll routines in `ScrollUtils` must enforce a maximum swipe count (e.g., maximum 5-8 swipes) to prevent infinite loops when an element does not exist.

---

## 2. Screen Object Model (SOM) Standards

1. **One Screen Class Per Logical View:**
   - Extend `BaseScreen` for all screen objects.
   - Encapsulate all UI interaction workflows and state verification queries for that screen.
   - Do not create parallel or duplicate screen objects for the same view.
2. **Stateless and Clean Life-Cycle:**
   - Avoid exporting stateful singleton instances that retain session pollution during parallel test runs. Prefer factory instantiation or scenario-scoped dependency injection.
3. **Readiness Verification Over Visibility:**
   - Provide an explicit `isLoaded()` or `waitUntilLoaded()` method using `WaitUtils` to verify that screen landmarks are interactive, rather than asserting container visibility alone.
4. **Zero Fabricated Test Data:**
   - Screen getters must return genuine UI text or attributes. Never manufacture placeholder strings to mask locator failures. Throw descriptive errors or return empty strings.
5. **No Test Logic in Screen Classes:**
   - Screen classes should perform actions, return states, and handle waits. Business test assertions (`expect()`) belong in step definitions or test specs.

---

## 3. Resilient Mobile Locator Strategy

Mobile locators must withstand app refactors, build changes, and multi-tenant localization.

### 3.1 Locator Priority Ladder
```
1. Accessibility ID (accessibilityId / content-desc / accessibilityLabel)  [HIGHEST PRIORITY]
2. Unique Semantic Resource ID (id / resource-id)                         [STRONG FALLBACK]
3. UiAutomator / iOS Class Chain / Predicate String                       [CONTROLLED FALLBACK]
4. Scoped Semantic XPath (relative to unique landmark container)           [LAST RESORT]
5. Generic Classes / Brittle Positional Indices                           [STRICTLY PROHIBITED]
```

### 3.2 Candidate Fallback Chains
When an accessibility ID is not permanently stable across environments or builds, configure structured candidate chains:
```json
{
  "submitButton": {
    "stable": { "strategy": "accessibilityId", "value": "btn_submit_transaction" },
    "fallbacks": [
      { "strategy": "id", "value": "com.app:id/submit_button" },
      { "strategy": "xpath", "value": "//android.widget.Button[@text='Submit']" }
    ]
  }
}
```
- **Strict Logical Equivalence:** Every fallback candidate must resolve the exact same logical UI control.
- **Shared Timeout Budget:** All candidates in a fallback chain share the single overall lookup timeout budget. Fallbacks do not reset the timer.
- **No State Bypassing:** Fallbacks are evaluated only during element discovery when an earlier candidate is absent. If an element is found but disabled, fail fast.

### 3.3 Localization & Multi-Tenant Separation
- Store localized text and multi-tenant selector variations in externalized selector repository files (e.g., `locators.json` or OpCo/tenant override maps).
- Keep core screen objects referencing logical locator keys rather than hardcoded UI strings.

---

## 4. Test Data & Service Layer Boundaries

Enterprise mobile test automation requires clean architectural seams separating test data, authentication workflows, and UI execution.

```text
Test Specs / Cucumber Features
               │
               ▼
   Workflow / Service Layer  (e.g., AuthService, TransactionService)
               │
    ┌──────────┴──────────┐
    ▼                     ▼
TestDataService       Screen Objects (BaseScreen)
(Excel/JSON/Env)          │
                          ▼
                     Mobile Utilities (WaitUtils, Actions, Gestures)
```

1. **TestDataService:**
   - Externalize all test accounts, credentials, MSISDNs, and scenario inputs into structured data sources (Excel worksheets, JSON fixtures, or encrypted stores).
   - Validate required fields with schema checks and fail fast before test execution begins.
   - Enforce Data Leakage Prevention (DLP): Never log unmasked PINs, OTPs, passwords, or authentication tokens.
2. **Environment vs. Scenario Data:**
   - Environment configurations (app package, activity, base URLs, generic environment OTPs) must be loaded through environment configuration modules.
   - Scenario data (target recipient, transfer amount, test user profile) must be retrieved dynamically per test execution.

---

## 5. Diagnostic Capture & Allure Reporting

1. **Failure Hook Attachments:**
   - Failure screenshots captured automatically.
   - XML page source dump captured on failure for offline hierarchy inspection.
   - Device log slice (ADB Logcat for Android, Syslog for iOS) captured around the failure timestamp.
2. **Allure Environment Metadata:**
   - Attach device metadata: Device model, OS version, platform (`Android` / `iOS`), automation engine (`UiAutomator2` / `XCUITest`), app build version, and tenant/environment name.

---

## 6. Framework Architecture Quality Gates

Before declaring a mobile automation implementation ready for production, verify against the following checklist:
- [ ] No `browser.pause()` or fixed `sleep()` calls present in screens, specs, or utilities.
- [ ] No broad generic class selectors (such as bare `android.widget.EditText`) without unique landmark scoping.
- [ ] No hardcoded test credentials or secrets embedded in test scripts.
- [ ] Utilities remain strictly screen-agnostic and selector-free.
- [ ] Swipes and scroll workflows have explicit upper-bound limits.
- [ ] TypeScript strict typing is maintained across shared utilities and service boundaries.


# Mobile Automation Coding Standards

These standards govern code quality, layer boundaries, and object model design for mobile test automation.

---

## 1. Screen Object Model (SOM) Design

- **Base Class Extension:** Every screen class must extend `BaseScreen`.
- **Single Responsibility:** One screen class per logical screen or dialog. Do not create parallel or duplicate screen objects for the same view.
- **Assertion Isolation:** Never execute test assertions (`expect(...)`) inside screen methods. Screen methods perform user actions and return genuine UI state; test specs or Cucumber steps execute assertions.
- **Zero Fabricated UI State:** Screen getters must report genuine UI attributes. Never return hardcoded or placeholder values (e.g., `'TXN-CONFIRMED'`) to mask unreadable elements.
- **Stateless Instances:** Avoid exporting instantiated stateful screen singletons. Use dependency injection or fresh instances to prevent cross-scenario state pollution in parallel runs.

---

## 2. Utility Layer Composition

- **Screen-Agnostic Utilities:** Utilities (`WaitUtils`, `MobileActions`, `GestureUtils`, `ScrollUtils`, `LoadingUtils`) must remain strictly screen-agnostic and selector-free.
- **Hierarchical Composition:**
  - `LoadingUtils` composes `WaitUtils`.
  - `ScrollUtils` composes `GestureUtils` and `WaitUtils`.
  - `MobileActions` composes `WaitUtils`.
- **Zero Driver Duplication:** Do not wrap WebdriverIO or Appium calls unless providing synchronization, retry logic, or error enrichment.

---

## 3. Thin Step Definitions (Cucumber BDD)

- **Ownership by Screen:** Step definitions must reside in files mapped to the owning screen or capability where the action or verification occurs.
- **No Step-to-Step Invocation:** Never call one Cucumber step from another step. Reuse underlying screen or service methods instead.
- **Thin Execution:** Step definitions must strictly parse inputs, invoke screen/service methods, and assert outcomes. Do not embed raw Appium element lookups or complex loops inside step files.


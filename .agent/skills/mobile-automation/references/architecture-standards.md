# Mobile Framework Architecture & Enterprise Standards

This document establishes the architecture standards, patterns, and audit criteria for enterprise mobile automation codebases.

---

## 1. Modular Configuration Architecture

Do not maintain a monolithic configuration file that mixes runner settings, capabilities, reporting, hooks, and device discovery.

### Recommended Configuration Topology
```text
config/
├── builders/
│   ├── capability.builder.ts     # Builds Android (UiAutomator2) and iOS (XCUITest) capabilities
│   ├── device.provider.ts        # ADB local discovery, emulator pool, or cloud device farm
│   ├── hooks.builder.ts          # Centralized screenshot, page source, and log attachments
│   └── reporter.builder.ts       # Allure metadata, environment properties, and artifact output
├── environments/
│   ├── dev.env.ts
│   ├── staging.env.ts
│   └── uat.env.ts
├── profiles/
│   ├── local-android.conf.ts
│   ├── local-ios.conf.ts
│   └── cloud-farm.conf.ts
└── wdio.base.conf.ts             # Shared timeouts, framework settings, and base options
```

### Contributor Principles
1. **Machine-Agnostic Setup:** Never hardcode user paths (e.g., Homebrew paths or local machine usernames) in scripts or configs. Read `ANDROID_HOME`, `JAVA_HOME`, and SDK locations dynamically from the environment.
2. **Capability Builders:** Expose configurable timeouts (`appium:newCommandTimeout`, `appium:uiautomator2ServerInstallTimeout`) and reset policies (`appium:noReset`, `appium:fullReset`) as typed parameters.
3. **Provider Flexibility:** Support seamless switching between local emulators, local physical devices, and cloud device farms (such as BrowserStack or LambdaTest) via simple environment flags (`EXECUTION_TARGET=local-android` vs `EXECUTION_TARGET=cloud-android`).

---

## 2. Screen Object Model (SOM) Design Rules

### Anti-Patterns to Avoid
- **Duplicated Screen Classes:** Never create separate screen objects for the same screen just because a different test is using it.
- **Embedded Assertions:** Do not embed `expect()` assertions inside screen action methods. Screen methods return data; tests assert outcomes.
- **Stateful Singleton Exports:** Avoid exporting instantiated screen singletons (`export default new LoginScreen()`) when tests run in parallel or require independent state. Prefer class exports or dependency-injected factories.
- **Bypassing Utilities:** Never use raw `browser.waitUntil` or `browser.pause` in screen objects. Delegate all waits to `this.waits` and actions to `this.actions`.

### Standard Screen Object Template
```typescript
import { BaseScreen } from '../base/base.screen';

export class TransferFundsScreen extends BaseScreen {
  // Encapsulated selector definitions
  private readonly selectors = {
    recipientInput: '~txt_recipient_number',
    amountInput: '~txt_transfer_amount',
    confirmButton: '~btn_confirm_transfer',
    processingSpinner: '~spinner_loading',
    successBanner: '~banner_transaction_success',
  };

  async isLoaded(): Promise<boolean> {
    const isInputVisible = await this.waits.isDisplayed(this.selectors.recipientInput);
    const isButtonVisible = await this.waits.isDisplayed(this.selectors.confirmButton);
    return isInputVisible && isButtonVisible;
  }

  async waitUntilLoaded(timeoutMs = 15000): Promise<void> {
    await this.waits.waitForDisplayed(this.selectors.recipientInput, {
      timeoutMs,
      description: 'Transfer Funds Screen recipient input',
    });
  }

  async submitTransfer(recipient: string, amount: string): Promise<void> {
    await this.actions.type(this.selectors.recipientInput, recipient);
    await this.actions.type(this.selectors.amountInput, amount);
    await this.actions.tap(this.selectors.confirmButton);
    await this.loading.waitForDisappear([this.selectors.processingSpinner]);
  }

  async getConfirmationMessage(): Promise<string> {
    return this.actions.getText(this.selectors.successBanner);
  }
}
```

---

## 3. Test Data & Security Governance (DLP)

1. **Separation of Concerns:**
   - **Environment Data:** App packages, bundle IDs, base URLs, backend endpoints, and generic test OTPs belong in environment configuration profiles.
   - **Scenario Data:** User credentials, test phone numbers (MSISDNs), recipient accounts, and transaction values belong in external data sources (Excel files, JSON test fixtures, or secure vault services).
2. **Data Leakage Prevention (DLP):**
   - Mask sensitive information (PINs, passwords, OTPs, CVVs) before outputting to logs, console, or test reports.
   - Centralize logging through a framework logger that redacts patterns matching credit cards, PIN codes, and tokens.
3. **No Hardcoded Literals in Specs:**
   - Specs and Cucumber step definitions must retrieve test data through `testDataService.get(key)` or scenario world context, never hardcoded string literals.

---

## 4. Diagnostics & Failure Triage Protocol

When a test failure occurs during automated test runs, execute a 5-layer diagnostic triage:

```text
               Test Step Failure Occurs
                          │
                          ▼
             [Layer 1: Device / Session]
      Appium session closed? ADB disconnected?
      App crashed / ANR dialog present?
                          │
                          ▼
             [Layer 2: UI State & Loading]
      Loader/spinner still active? Modal overlay blocking?
      Keyboard obstructing target element?
                          │
                          ▼
             [Layer 3: Locator Discovery]
      Target element visible in XML page source?
      Did accessibility ID change or fail candidate chain?
                          │
                          ▼
             [Layer 4: Test Data / Backend]
      Invalid account balance? Account locked?
      Precondition or auth state expired?
                          │
                          ▼
             [Layer 5: Genuine Defect]
      UI rendered correctly, business validation failed.
      Log application defect with attached Allure artifacts.
```

### Artifacts to Capture on Every Failure
1. **Screenshot:** Visual state of the screen at the exact moment of failure.
2. **Page Source Hierarchy (XML):** Full Appium hierarchy dump to verify whether the element was present, hidden, or obscured.
3. **Logcat / Device Logs:** The 500 lines preceding the failure to detect native app crashes, ANRs, or network errors.


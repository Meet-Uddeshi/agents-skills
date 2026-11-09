# Mobile Diagnostics & Reporting Rules

These rules standardize test reporting, failure artifact capture, and CI triage efficiency.

---

## 1. Centralized Failure Hook

- **Automatic Failure Capture:** Test hooks must automatically capture diagnostic artifacts upon any test step or assertion failure:
  1. Full screenshot of the device viewport.
  2. Complete XML page source hierarchy dump from Appium.
  3. Preceding device logs (ADB Logcat for Android, Syslog for iOS).
- **No Direct Spec Capture:** Never manually invoke screenshot saving routines inside individual test spec files. Centralize capture in the test framework `afterTest` / `After` hook.

---

## 2. Allure Metadata Standardization

Every test report must include structured labels:
- **Environment:** `env` (e.g., UAT, Staging, DEV).
- **Platform:** `platformName` (`Android` / `iOS`).
- **Device Details:** Device model, OS version, and UDID.
- **Suite & Capability:** Suite name (Smoke / Regression), functional capability area, and test case ID tag.


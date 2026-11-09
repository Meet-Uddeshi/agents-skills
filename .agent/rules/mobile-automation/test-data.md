# Mobile Test Data & Security Rules

These rules govern test data isolation, credential retrieval, and Data Leakage Prevention (DLP).

---

## 1. Externalized Test Data Architecture

- **No Hardcoded Literals:** Never hardcode credentials, MSISDNs, account numbers, or transaction PINs in feature files, step definitions, or screen objects.
- **Dedicated TestDataService:** Retrieve test account records from structured, externalized datasets (such as Excel sheets, JSON fixtures, or secure vault services).
- **Fail Fast Validation:** If required test data keys are missing or invalid, fail immediately with a descriptive configuration error before launching device sessions.

---

## 2. Environment Configuration vs Scenario Data

- **Environment Settings:** Base URLs, app packages, activity names, bundle IDs, and mock/environment OTPs are environment configurations managed by environment profiles.
- **Scenario Data:** User identities, test payment amounts, and assertion target values are scenario-specific data keyed to test scenario IDs.

---

## 3. Data Leakage Prevention (DLP)

- **Redaction in Logs:** All sensitive values (passwords, PINs, OTPs, CVVs) must be automatically redacted in console output, framework logs, and report attachments.
- **Safe Reporting:** Never expose plain-text credentials in Allure test parameters or step descriptions.


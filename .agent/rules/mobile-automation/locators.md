# Mobile Locator & Selector Rules

These rules enforce robust, multi-tenant resilient locator strategies that withstand OS upgrades, framework refactors, and localization shifts.

---

## 1. Locator Strategy Priority Ladder

Always choose locator strategies according to this strict hierarchy:

1. **Accessibility ID (`accessibilityId`):**
   - Android: `content-desc` attribute.
   - iOS: `accessibilityLabel` or `name` attribute.
   - Highest priority. The primary choice for all interactive elements.
2. **Unique Semantic Resource ID (`id`):**
   - Android: `resource-id` (e.g., `com.company.app:id/submit_button`).
   - Strong fallback when accessibility IDs are absent.
3. **Native Driver Locators:**
   - Android: `UiAutomator` selectors (e.g., `new UiSelector().text("Submit")`).
   - iOS: `class chain` or `predicate string` (e.g., `**/XCUIElementTypeButton[`name == "Submit"`]`).
4. **Scoped Semantic Relative XPath:**
   - Scoped strictly relative to a unique landmark container. Use only when native identifiers do not exist.

---

## 2. Prohibited Locator Anti-Patterns

- **No Bare Generic Classes:** Never use un-scoped generic class selectors such as `className("android.widget.EditText")` or `className("XCUIElementTypeTextField")`.
- **No Positional / Index XPaths:** Selectors like `(//android.widget.EditText)[1]` or `(//android.view.ViewGroup[@clickable='true'])[2]` are strictly prohibited.
- **No Hardcoded Localized UI Text in Core Screens:** UI text that changes with language, tenant, or OpCo must be externalized into selector configuration dictionaries.

---

## 3. Fallback Candidate Chains

When a primary accessibility ID cannot be guaranteed across all builds or environments:
- Configure a primary `stable` candidate and up to two `fallbacks`.
- **Strict Equivalence:** Every fallback candidate must resolve the exact same logical UI control. Never configure an alternative action (e.g., Cancel instead of Submit) as a fallback.
- **Shared Timeout Budget:** All candidates in a fallback chain share the single overall lookup timeout budget. Fallbacks do not reset the timer.
- **Fail Fast on Application State:** If an element is discovered but disabled or obscured, fail fast. Do not switch to fallback candidates to bypass genuine application state.


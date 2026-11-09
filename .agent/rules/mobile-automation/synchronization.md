# Mobile Synchronization & Anti-Flakiness Rules

These rules eliminate race conditions, timeout flakiness, and unstable mobile test execution.

---

## 1. Zero Hard Waits

- **Prohibition:** Strictly forbid `browser.pause(ms)`, `sleep(ms)`, or thread blocking calls in screens, utilities, or test specs.
- **Enforcement:** Every synchronization point must be an explicit, condition-driven wait via `WaitUtils` (e.g., `waitForDisplayed`, `waitForClickable`, `waitForHidden`, or `waitUntil(predicate)`).
- **Implicit Wait Disabled:** Configure the Appium driver implicit wait to zero (`implicit: 0`) to prevent hidden lookup delays when verifying element absence.

---

## 2. Loader & Spinner Dismissal

- **Proactive Overlay Clearing:** When an action triggers background network calls or processing dialogs, wait for the loading spinner or overlay to disappear before attempting the next interaction.
- **Compositional Loading:** Use `LoadingUtils` by passing screen-specific spinner locators. If no spinner appears initially, the check must proceed without blocking.

---

## 3. Bounded Scroll & Gesture Synchronization

- **Upper Bound Guard:** Every scroll routine in `ScrollUtils` must enforce a maximum swipe limit (default: 5-8 swipes). Throw a descriptive timeout error if the element is not found within the limit.
- **Gesture Settling:** Allow viewport settling after physical swipes (e.g., 200-300ms touch physics deceleration) before querying the view hierarchy.
- **Coordinate Independence:** Prefer element-relative swipes (`swipeOnElement`) over absolute screen coordinate gestures to support varying screen dimensions and device aspect ratios.


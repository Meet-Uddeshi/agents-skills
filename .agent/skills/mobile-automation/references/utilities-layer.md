# Mobile Utilities Reference Guide

This reference outlines the technical implementation patterns and contracts for the five core mobile automation utilities and the `BaseScreen` orchestration layer.

---

## 1. WaitUtils Contract

`WaitUtils` provides primitive synchronization for WebdriverIO and Appium element states.

### Key Capabilities
- `waitForDisplayed(target, options?)`: Waits for an element to be visible in viewport.
- `waitForHidden(target, options?)`: Waits for an element or overlay to disappear.
- `waitForExist(target, options?)`: Waits for an element to attach to the view hierarchy.
- `waitForClickable(target, options?)`: Waits for an element to be displayed and enabled for touch interaction.
- `waitForEnabled(target, options?)`: Waits for an element's enabled attribute to be true.
- `waitUntil(conditionFn, options)`: Custom predicate wait with descriptive failure message.

### Critical Implementation Rules
```typescript
// Do not expose generic, unhelpful error messages
export interface WaitOptions {
  timeoutMs?: number;
  intervalMs?: number;
  description?: string;
}

// Bounded wait with descriptive context
export async function waitForDisplayed(
  element: WebdriverIO.Element,
  options: WaitOptions = {}
): Promise<void> {
  const timeout = options.timeoutMs ?? 10000;
  const description = options.description ?? 'element';
  await element.waitForDisplayed({
    timeout,
    interval: options.intervalMs ?? 500,
    timeoutMsg: `Timed out after ${timeout}ms waiting for ${description} to be displayed.`,
  });
}
```

---

## 2. MobileActions Contract

`MobileActions` provides safe, synchronized interactions on mobile elements.

### Key Capabilities
- `tap(target, options?)`: Waits for clickable, then executes native tap.
- `type(target, value, options?)`: Waits for clickable, clears existing text safely, sends keys, and optionally hides keyboard.
- `clear(target)`: Clears input field handling mobile OS quirk variations.
- `getText(target)`: Waits for displayed, returns trimmed text.
- `getAttribute(target, attributeName)`: Reads native attribute (e.g., `content-desc`, `enabled`, `selected`).
- `hideKeyboard()`: Dismisses software keyboard if active without throwing if already hidden.

---

## 3. GestureUtils Contract

`GestureUtils` encapsulates low-level physical touch interactions across Appium drivers (UiAutomator2 and XCUITest).

### Gesture Primitives
- `swipe(direction, percentage, speed)`: Performs a viewport-relative swipe (up, down, left, right).
- `swipeOnElement(element, direction, percentage)`: Swipes relative to a specific element's bounding box.
- `longPress(target, durationMs)`: Touch-and-hold interaction for contextual menus.
- `tapCoordinate(x, y)`: Direct coordinate tap for non-element UI surfaces.

### OEM & Driver Resilience
- Prefers native Appium extension commands (`mobile: swipeGesture` on Android UiAutomator2) with graceful fallback to W3C touch action chains (`browser.action('pointer')`).
- Strictly separates gestures from high-level element search logic.

---

## 4. ScrollUtils Contract

`ScrollUtils` composes `GestureUtils` and `WaitUtils` to discover and navigate to off-screen elements.

### Workflows
- `scrollToElement(targetLocator, options?)`: Swipes in bounded increments until the target element is displayed.
- `scrollToText(text, options?)`: Discovers elements matching specified visible text or content description.

### Bounded Swipe Guard
```typescript
export interface ScrollOptions {
  maxSwipes?: number;
  direction?: 'down' | 'up' | 'right' | 'left';
  swipePercentage?: number;
}

export async function scrollToElement(
  locatorFn: () => Promise<WebdriverIO.Element>,
  options: ScrollOptions = {}
): Promise<WebdriverIO.Element> {
  const maxSwipes = options.maxSwipes ?? 6;
  const direction = options.direction ?? 'down';

  for (let swipeIndex = 0; swipeIndex < maxSwipes; swipeIndex++) {
    const element = await locatorFn();
    if (await element.isDisplayed().catch(() => false)) {
      return element;
    }
    await gestureUtils.swipe(direction, options.swipePercentage ?? 0.5);
  }

  throw new Error(`Exceeded maximum ${maxSwipes} swipes looking for element.`);
}
```

---

## 5. LoadingUtils Contract

`LoadingUtils` coordinates waiting for asynchronous UI loading indicators without hardcoding specific spinner locators.

### Usage
- Accepts one or more loader selectors from caller screens.
- Checks if any loader is currently displayed.
- If displayed, waits for all loaders to disappear within a defined timeout.
- If no loaders are displayed initially, proceeds immediately without penalty.

---

## 6. BaseScreen Orchestration

`BaseScreen` acts as the shared foundation for all screen objects.

```typescript
export abstract class BaseScreen {
  protected readonly waits: WaitUtils;
  protected readonly actions: MobileActions;
  protected readonly gestures: GestureUtils;
  protected readonly scrolls: ScrollUtils;
  protected readonly loading: LoadingUtils;

  constructor() {
    this.waits = new WaitUtils();
    this.actions = new MobileActions(this.waits);
    this.gestures = new GestureUtils(this.waits);
    this.scrolls = new ScrollUtils(this.gestures, this.waits);
    this.loading = new LoadingUtils(this.waits);
  }

  /**
   * Verifies that the screen is fully loaded and ready for interaction.
   */
  abstract isLoaded(): Promise<boolean>;

  /**
   * Bounded wait until the screen landmark is ready.
   */
  abstract waitUntilLoaded(timeoutMs?: number): Promise<void>;
}
```


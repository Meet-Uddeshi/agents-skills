---
description: Eliminate AI slop from UI/UX designs. Remove generic gradients, purple glows, bad padding, low-contrast text, and reset to clean modern design systems.
---

# /unslop - Visual Modernization & Anti-Slop Workflow

$ARGUMENTS

---

## Purpose

Systematically identify and remove AI-generated visual artifacts ("AI slop") including gratuitous gradients, purple/violet neon glows, glassmorphism overuse, floating cards without semantic purpose, poor typographic hierarchy, and arbitrary spacing.

---

## Sub-commands

```text
/unslop audit [target]                 - Scan UI component or page for slop markers, contrast issues, and visual noise
/unslop clean [target]                 - Refactor component to use intentional design tokens and clean layout
/unslop tokens [brand]                 - Generate restrained, high-contrast token palette (neutral gray, crisp borders, purposeful accent)
/unslop typography                     - Reset heading scales, optical line-heights, and tabular numbers
```

---

## Standard 6-Step Implementation Workflow

1. **Slop Detection & Audit:**
   - Scan for multi-stop radial/linear background gradients, oversized rounded pill borders (`rounded-3xl` everywhere), and glowing drop shadows.
   - Flag low-contrast gray text on dark backgrounds violating WCAG AA (minimum 4.5:1).

2. **Establish Design Token Foundation:**
   - Define strict neutral palette (0 to 1000 scale) with one purposeful accent color.
   - Enforce discrete spacing scale (4px grid: 4, 8, 12, 16, 24, 32, 48, 64px).

3. **Restructure Layout & Spacing:**
   - Replace floating nested card stacks with clean borders (`border border-neutral-200 dark:border-neutral-800`).
   - Align content to a disciplined grid with consistent padding and gap definitions.

4. **Refine Typography & Visual Hierarchy:**
   - Restrict font weights to regular (400), medium (500), and semibold (600).
   - Use tabular numerals (`font-mono` or `tabular-nums`) for numeric data and timestamps.

5. **Polish Interactive States:**
   - Remove bouncy over-animated spring transitions; use subtle 150ms ease transitions.
   - Add crisp focus-visible rings for accessibility compliance.

6. **Regression Verification:**
   - Validate responsive layouts across mobile (375px), tablet (768px), and desktop (1440px).
   - Run a11y contrast checks and verify no broken visual states.


---
name: ui-guidance
description: Overlay for graphical UI and web frontend code. Use alongside the repo's implementation skill when implementing or reviewing UI changes.
---

# UI/Frontend Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill (e.g. **coding-guidance-cpp**, **project-core-dev**)
when the change touches UI or frontend code.

Use this as the thin default overlay for ordinary UI work.
If the task is redesign-heavy, frontend-polish heavy, or needs a stronger UX
review checklist, prefer `ui-design-guidance`.

## When to use

The repo includes graphical UI or web frontend code — web views, desktop UI,
embedded panels, or rendering layers.

## Not for

Terminal UIs (ncurses, TUI frameworks) unless the repo explicitly treats them as
UI with design standards. Pure data visualization or plotting libraries are also
out of scope.

## Rules

- Preserve the existing design language unless the task explicitly calls for
  redesign. Do not introduce new color palettes, spacing systems, or component
  patterns without justification.
- Accessibility, layout stability, and responsive behavior are part of done —
  not follow-up work.
- UI changes must not bypass the repo's test and build hygiene.
- Verify visual output manually or with snapshot tests if the repo supports
  them.
- If the repo does not document breakpoints, design tokens, or visual test
  tooling, derive them from nearby UI code and record the fallback evidence in
  any implementation or review note you produce.

## Decision Heuristics

- **Design language check:** before adding a new visual element, grep the
  codebase for an existing element that serves a similar purpose. Match its
  spacing, color tokens, and component structure unless the task requires
  divergence.
- **Evidence fallback:** when the repo lacks UI docs, use the nearest existing
  component or screen as the baseline and name the files inspected.
- **Accessibility bar:** if the change adds interactive elements, verify
  keyboard navigation and screen reader labels. If the repo has no a11y
  testing, add manual verification to the review checklist.
- **Layout stability:** if the change affects layout, test at the repo's
  supported viewport sizes. If those are undocumented, test at the common
  breakpoints already exercised by nearby code or styles. Flag layout shifts
  that appear on resize or content change.

## Validation

A UI change is done when (in addition to the base implementation skill's
validation):

- visual output matches the existing design language or the requested redesign
- interactive elements are keyboard-navigable
- layout is stable across supported viewports
- when automated UI verification is absent, any implementation or review note
  you produce names the screenshots, snapshots, or manual checks used as
  evidence

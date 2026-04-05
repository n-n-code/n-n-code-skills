---
name: ui-design-guidance
description: Canonical overlay for graphical UI and web frontend code that need strong design quality and UX discipline without breaking repo conventions. Use alongside the repo's implementation skill when implementing or reviewing UI changes, redesigns, frontend polish work, or UX-heavy UI updates.
---

# UI Design Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill when the change touches graphical
UI or web frontend code.

This is the stronger UI overlay in this repo.
Prefer it over `ui-guidance` when the task is redesign-heavy, polish-heavy, or
needs explicit UX review beyond basic UI hygiene.

## When to use

- the repo includes graphical UI or web frontend code
- the task asks for UI implementation, redesign, beautification, styling, or
  frontend polish
- the task changes how a feature looks, feels, moves, or is interacted with
- the work includes new pages, components, forms, navigation, responsive layout,
  animation, or charts/data display
- the task asks for UX review or quality improvement, not just visual changes
- the change touches web views, desktop UI, embedded panels, dashboards, pages,
  landing screens, or rendering layers

## Not for

- terminal UIs unless the repo explicitly treats them as product UI
- pure data visualization or plotting libraries without product-interface work
- backend-only changes with no UI surface

## Core workflow

1. Read the touched UI files and nearby components first.
2. Determine the mode:
   - preserve mode when the repo already has a clear design language and the
     user did not ask for redesign
   - redesign mode when the user explicitly wants a new visual direction or the
     current UI is intentionally being reworked
   - UX-review-heavy mode when the main risk is usability, interaction quality,
     responsiveness, forms, navigation, or data presentation
3. In preserve mode, derive tokens, spacing, interaction patterns, breakpoints,
   and component structure from the nearest existing screens or components.
4. In redesign mode, choose one intentional aesthetic direction before coding:
   define the interface purpose, audience, tone, and one memorable visual idea.
5. In UX-review-heavy mode, evaluate the change in this order:
   - accessibility
   - interaction and feedback
   - layout and responsiveness
   - typography and color clarity
   - forms, navigation, and data presentation when they apply
6. Implement real working UI code that fits the chosen mode:
   - preserve mode should feel native to the repo
   - redesign mode should feel distinctive, cohesive, and production-grade
   - UX-review-heavy mode should strengthen usability without drifting away from
     the repo's design language unless redesign is requested
7. Verify accessibility, keyboard behavior, responsive layout stability, and
   visual output with the strongest evidence the repo supports.
8. When the repo lacks UI docs or automated checks, record the fallback
   evidence: files inspected, viewport sizes tested, and screenshots or manual
   checks used.

## Decision rules

- Preserve the existing design language unless the task explicitly calls for
  redesign.
- Accessibility, layout stability, and responsive behavior are part of done,
  not follow-up work.
- UI changes must not bypass the repo's build, test, or review hygiene.
- Match implementation complexity to the visual goal. Refined minimalism needs
  precision and restraint; bold maximalism needs deliberate structure and
  stronger visual systems.
- Before adding a new visual element, grep for a similar existing element and
  reuse its patterns unless redesign mode justifies divergence.
- Prefer concise, durable heuristics over giant style catalogs. Use repo
  context first, not generic design-library sprawl.

## UX priorities

### 1. Accessibility

- interactive elements must be keyboard-navigable
- icon-only controls need labels
- visible focus states must remain intact
- color cannot be the only carrier of meaning
- reduced-motion preferences should be respected when animation is present

### 2. Interaction and feedback

- touch and click targets should be comfortably hittable
- loading, success, and error states must be explicit
- primary interactions must not depend on hover alone
- destructive or async actions need clear user feedback

### 3. Layout and responsiveness

- layout must stay stable across supported viewports
- avoid horizontal scroll and fragile fixed-width assumptions
- spacing should follow the repo's existing scale or the nearest local pattern
- fixed or overlay UI should not obscure essential content

### 4. Typography and color

- body text should remain readable without tiny type or weak contrast
- use semantic tokens or shared variables instead of scattered one-off values
- hierarchy should come from spacing, weight, scale, and contrast, not color
  alone

### 5. Forms, navigation, and data

- inputs need visible labels and local error messages
- navigation state and back-path should be predictable
- charts and data views must remain readable without relying on color alone
- empty, loading, and error states should explain what the user can do next

## Aesthetic rules

- Choose typography intentionally. Avoid default stacks and overused safe
  choices unless the repo already standardizes on them.
- Commit to a cohesive palette and define reusable tokens or variables instead
  of scattering one-off colors.
- Use motion deliberately. Prefer a few meaningful transitions or reveal
  sequences over noisy micro-interactions everywhere.
- Build atmosphere with backgrounds, texture, layering, contrast, shadows, or
  pattern where the design direction benefits from it.
- Avoid generic AI-UI habits: purple-on-white defaults, interchangeable hero
  sections, timid palettes, and cookie-cutter dashboard layouts.
- Keep distinctive choices consistent across the whole surface so the UI feels
  designed rather than decorated.

## Validation

A UI change is done when, in addition to the base implementation skill's
validation:

- visual output matches the existing design language or the requested redesign
- interactive elements are keyboard-navigable and labeled appropriately
- layout is stable across supported viewports or the nearest documented
  fallbacks
- forms, navigation, and feedback states are explicit where they apply
- the evidence names the files, screenshots, snapshots, or manual checks used
  when automated UI verification is absent

## Examples

- `Polish this React settings screen without changing the product style`:
  stay in preserve mode, inspect nearby screens, reuse tokens and spacing, and
  verify keyboard and viewport behavior.
- `Redesign this marketing landing page so it feels memorable`:
  switch to redesign mode, pick one clear aesthetic direction, then implement a
  cohesive page with stronger typography, layout, and motion choices.
- `Review this dashboard for UX issues before release`:
  switch to UX-review-heavy mode, walk the priority list from accessibility
  through data presentation, and report concrete issues with evidence.

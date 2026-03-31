---
name: thinking
description: Planning and design skill. Merges brainstorming, concise planning, and kaizen-style incremental improvement.
---

# Thinking

Read `AGENTS.md` first. This skill adds planning/design guidance.

## Default Stance

- understand the current repo shape before proposing changes
- prefer incremental, testable improvements over rewrites
- keep plans implementation-ready and decision-complete
- remove unnecessary complexity ruthlessly

## Workflow

1. Inspect the current code, docs, and constraints.
2. Clarify goal, success criteria, and out-of-scope items.
3. Compare 2-3 viable approaches when trade-offs matter.
4. Choose the narrowest approach that preserves quality.
5. Produce a concrete plan with validation and risk handling.

## Brainstorming Rules

- ask only the questions that materially change the design
- prefer one issue at a time over broad unfocused discovery
- validate assumptions early when they affect architecture or rollout

## Kaizen Rules

- prefer small improvements that compound
- make invalid states harder to express
- use the type system, validation, and clear contracts to prevent mistakes
- leave touched code better than you found it, but avoid out-of-scope churn

## Plan Rules

A good plan should cover:

- summary and intended outcome
- key changes by subsystem/behavior
- tests and validation
- explicit assumptions and defaults

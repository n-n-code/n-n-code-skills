# AGENTS.md

## Repo Purpose

This repository stores reusable agent skills. Most work should be limited to root documentation and folders under `.agents/skills/`.

## Structure

- Skills live in `.agents/skills/<skill-name>/`
- Each skill must include `SKILL.md`
- Supporting files are allowed when they directly serve the skill

## Skill Composition Model

Skills compose in two tiers:

1. **Principle skills** — portable, unconditional engineering guidance for a
   language or discipline. Example: `coding-guidance-cpp`.
2. **Overlays** — composable rules for a specific domain or project concern.
   Examples: `backend-guidance`, `ui-guidance`, `project-core-dev`,
   `project-vendor-boundary`.

An agent working on a task loads one principle skill plus any applicable overlays.
Overlays add domain-specific rules and validation criteria on top of the
principle skill's universal checks. Overlays should not repeat what the principle
skill already covers.

Workflow skills (**thinking**, **recursive-thinking**, **dream-thinking**,
**security**) are orthogonal — they change *how* you work, not *what domain
rules* apply. They compose with either tier.

## Working Rules

- Preserve the existing folder-based layout unless the task explicitly requires a structural change
- Keep instructions concise, specific, and grounded in files that actually exist
- Update only the skill folder and root docs relevant to the task
- Prefer small, targeted edits over broad repo rewrites

## Validation

There is no repo-specific build, test, or lint workflow yet.

Before finishing, verify:

- new or edited skills still live under `.agents/skills/`
- each skill folder still has `SKILL.md`
- root docs do not claim nonexistent commands or automation
- examples and references point to real files

## Safety

- Do not rename or move published skill folders without explicit instruction
- Do not add generated content unless the task requires it
- Do not invent setup, CI, packaging, or release workflows that are not present in the repo

## Scope

Use this root file for the whole repository. Nested `AGENTS.md` files are not needed unless a subtree later gets a materially different workflow.

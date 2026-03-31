# AGENTS.md

## Repo Purpose

This repository stores reusable agent skills. Most work should be limited to root documentation and folders under `.agents/skills/`.

## Structure

- Skills live in `.agents/skills/<skill-name>/`
- Each skill must include `SKILL.md`
- Supporting files are allowed when they directly serve the skill

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

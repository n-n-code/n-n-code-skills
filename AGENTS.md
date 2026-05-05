# AGENTS.md

## Repo Purpose

This repository stores reusable agent skills. Most work should be limited to root documentation and folders under `.agents/skills/`.

The root currently contains `README.md`, `AGENTS.md`, `LICENSE`, and
`scripts/check-skills.sh` in addition to `.agents/skills/`.

## Structure

- Skills live in `.agents/skills/<skill-name>/`
- Each skill must include `SKILL.md`
- Supporting files such as `references/`, `scripts/`, or templates are allowed when they directly serve the skill
- Repository validation lives in `scripts/check-skills.sh`

## Skill Composition Model

Skills compose in two tiers:

1. **Principle skills** — portable, unconditional engineering guidance for a
   language or discipline. Example: `coding-guidance-cpp`.
2. **Overlays** — composable rules for a specific domain or project concern.
   Examples: `backend-guidance`, `ui-guidance`, `project-core-dev`,
   `project-vendor-boundary`.

Some overlays are **process overlays** rather than domain overlays. They govern
repo workflow or enforcement rules for a class of work. Example:
`development-contract-process`.

Some overlays are **companion overlays**. They layer a narrower workflow onto a
default skill without replacing it. Examples: `documenter-coauthoring`,
`security-identity-access`.

Default composition model:

1. Load one principle skill when the task is language- or discipline-specific.
2. Add the overlays that match the domain or repo concern.
3. Add an orthogonal workflow skill only when the task clearly needs that mode.

Examples:

- routine Python feature work: `coding-guidance-python` + `project-core-dev`
- routine Go feature work: `coding-guidance-go` + `project-core-dev`
- backend feature or config change: principle skill + `backend-guidance` + `project-config-and-tests`
- frontend redesign or polish work: principle skill + `ui-design-guidance`
- prompt design, prompt rewrite, or prompt eval work: `prompt-engineering`
- context setup, long-session compaction, or handoff work: `context-engineering`
- security review of auth flows: `security` + `security-identity-access`

Workflow skills (**context-engineering**, **thinking**,
**recursive-thinking**, **dream-thinking**, **tester-mindset**,
**prompt-engineering**, **security**) are orthogonal —
they change *how* you work, not *what domain or process rules* apply. They
compose with either tier.

Role vocabulary used in this repo:

- **baseline overlay**: thin default overlay for routine work in a domain
- **canonical overlay**: stronger overlay for harder cases in the same domain
- **companion overlay**: optional workflow-focused overlay that composes with a
  baseline overlay for the same job without replacing it
- **template overlay**: pattern for repo-local adaptation rather than the main
  overlay to load here
- **process overlay**: enforcement or workflow guidance that composes with
  implementation skills
- **system skill**: build/create/install skill that produces a repo-owned system

When a skill family has both baseline and canonical overlays, keep that
relationship explicit in the docs instead of letting two near-duplicates drift.
When a skill family has a companion overlay, keep the baseline as the default
and describe clearly when the companion should be added. Example:
`documenter` + `documenter-coauthoring`, or `security` +
`security-identity-access`.

## Working Rules

- Preserve the existing folder-based layout unless the task explicitly requires a structural change
- Keep instructions concise, specific, and grounded in files that actually exist
- Use the repo's role vocabulary consistently when naming or describing skills
- Update only the skill folder and root docs relevant to the task
- Treat `README.md` and `AGENTS.md` as durable repo docs; do not add process or automation claims that the repository does not implement
- Prefer small, targeted edits over broad repo rewrites

## Validation

There is no application build, test, or lint workflow. For repository
structural validation, run:

```bash
bash scripts/check-skills.sh
```

Before finishing, verify:

- new or edited skills still live under `.agents/skills/`
- each skill folder still has `SKILL.md`
- `bash scripts/check-skills.sh` passes when the change affects skill files,
  references, root docs, or validation behavior
- root docs do not claim nonexistent commands or automation
- root docs still match the current root files and published skill inventory
- examples and references point to real files
- likely skill-name references in Markdown point to published local skills

## Safety

- Do not rename or move published skill folders without explicit instruction
- Do not add generated content unless the task requires it
- Do not invent setup, CI, packaging, or release workflows that are not present in the repo

## Scope

Use this root file for the whole repository. Nested `AGENTS.md` files are not needed unless a subtree later gets a materially different workflow.

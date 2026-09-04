# AGENTS.md

## Repo Purpose

This repository stores reusable agent skills. Most work should be limited to
root documentation, `.agents/skills/`, and the validation scripts
under `scripts/`.

## Structure

- Skills live in `.agents/skills/<skill-name>/`
- Each skill must include `SKILL.md`
- `SKILL.md` frontmatter must contain exactly `name` and `description`; the
  declared name must match the skill folder
- Supporting files such as `references/`, `scripts/`, and `assets/` are allowed
  when they directly serve the skill
- `README.md` is the published skill inventory and routing guide; keep it
  aligned whenever a skill is added, removed, or retitled

## Skill Taxonomy

`README.md` is the source of truth for the current skill inventory, family
routing, and composition examples. Do not duplicate that catalog here.

- Start with one principle skill for language- or discipline-specific work,
  add matching domain or project overlays, and add an orthogonal workflow skill
  only when the task needs that mode
- A baseline overlay is the routine default; a canonical overlay is the
  stronger option for harder work in the same domain and should preserve the
  baseline's core expectations
- A companion overlay adds an optional workflow without replacing its baseline
- A process overlay governs workflow or enforcement; a template overlay is a
  pattern for repo-local adaptation
- A system skill builds or installs a repo-owned system instead of guiding
  ordinary execution
- Keep these relationships explicit when adding or revising skills so adjacent
  skills do not drift into overlapping jobs

## Working Rules

- Preserve the existing folder-based layout unless the task explicitly requires a structural change
- Keep instructions concise, specific, and grounded in files that actually exist
- Use the repo's role vocabulary consistently when naming or describing skills
- Update only the skill folder and root docs relevant to the task
- When adding or changing a skill, keep its trigger boundaries distinct from
  neighboring skills and update the relevant `README.md` family and defaults
- Treat `README.md` and `AGENTS.md` as durable repo docs; do not add process or automation claims that the repository does not implement
- Prefer small, targeted edits over broad repo rewrites

## Validation

There is no application build or lint workflow.

For changes to skills, supporting files, root documentation, or validation
behavior, run:

```console
python scripts/check_skills.py
```

When `scripts/check_skills.py` or `scripts/test_check_skills.py` changes, also
run:

```console
python scripts/test_check_skills.py
```

When the metadata parser, executable skill resources, or their tests change,
also run:

```console
python scripts/test_skill_resources.py
```

Report unavailable Bash, real CMake/CTest, or PyYAML checks as skipped, not
passed. Tool discovery and optional overrides are documented in `README.md`.

When `scripts/check-skills.sh` changes, run its wrapper on a Bash-capable
system:

```console
bash scripts/check-skills.sh
```

Before finishing, verify:

- new or edited skills still live under `.agents/skills/`
- each skill folder still has `SKILL.md`
- the applicable validation commands above pass
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

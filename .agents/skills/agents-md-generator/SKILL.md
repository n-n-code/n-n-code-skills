---
name: agents-md-generator
description: Create or revise repository AGENTS.md files from repo inspection, existing docs, and a small number of high-impact clarifications. Use when the user asks to create an AGENTS.md, improve agent instructions for a repo, convert CLAUDE.md-style guidance into AGENTS.md, or write coding-agent instructions for a repository.
---

# AGENTS.md generator

Create portable, high-signal `AGENTS.md` files that are grounded in the actual repository and remain especially useful for Codex-style coding agents.

## Core workflow

1. Identify whether the task is `new`, `revise`, or `migrate`.
2. Inspect the repo before asking avoidable questions.
3. Ask only the missing, high-impact questions.
4. Draft or revise the root `AGENTS.md`.
5. Recommend nested `AGENTS.md` files only when the repo structure clearly needs local overrides.
6. Run a token-optimization pass before finalizing.

Do not skip repo inspection unless the user gives the full repo context directly.

## Phase 1: Identify the task mode

Start by classifying the request:

- `new`: create a root `AGENTS.md` for a repo that does not have one
- `revise`: improve an existing `AGENTS.md`
- `migrate`: consolidate repo guidance from files such as `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, or CI config into a cleaner `AGENTS.md`

If the user asks for "agent instructions", "repo instructions", or "coding-agent guidance", treat that as an `AGENTS.md` request unless they clearly want another format.

## Phase 2: Inspect the repo first

Before asking questions, inspect the repo for the facts that should shape the file.

Look for:

- existing `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, and release docs
- package manifests, build files, test config, lint config, and task runners
- CI workflows in `.github/workflows/`
- monorepo layout, apps, packages, services, or other subtrees with distinct workflows
- repo-specific hazards such as generated code, vendor trees, migrations, secrets, or destructive operations

Prefer targeted inspection over broad reading. Open the minimum set of files needed to answer:

- how to set up the repo
- how to build, test, lint, or validate changes
- what commands matter before commit or PR
- what constraints or forbidden actions agents must respect
- whether any subdirectory genuinely needs its own local override file

Use `references/inspection-and-content-checklist.md` to make sure the repo inspection and final file are complete.

## Phase 3: Ask only the missing questions

After inspection, ask only questions that materially change the final `AGENTS.md`.

Typical missing questions:

- who the primary agent audience is, if the repo serves multiple very different workflows
- how strict the repo should be about tests, formatting, commit hygiene, or review gates
- whether the team wants nested `AGENTS.md` files in specific subtrees
- whether any undocumented local conventions should be treated as required

Do not ask questions that the repo can answer on its own.

If ambiguity remains and the user does not care, choose a sensible default and mark it as an explicit assumption in the final draft.

## Phase 4: Draft or revise the root `AGENTS.md`

Default output is a root `AGENTS.md`.

The file should be concise, executable, and repo-specific. Include only the sections that improve agent execution.

Typical content:

- what this repo is and any structure the agent must understand
- setup/build/test/lint/validation commands
- coding and testing expectations
- review, commit, or PR expectations if the repo clearly has them
- repo-specific boundaries, hazards, or forbidden actions
- where deeper docs live

Do not write a generic manifesto. Prefer concrete commands, boundaries, and decision rules.

When revising:

- preserve real repo constraints
- remove stale, duplicate, or product-branded wording unless the user explicitly wants to keep it
- consolidate scattered instruction text into one coherent document

## Phase 5: Decide on nested `AGENTS.md`

Do not create or recommend nested files by default.

Recommend nested `AGENTS.md` only when a subtree has materially different:

- commands or toolchains
- ownership boundaries
- safety constraints
- generated/vendor rules
- workflow expectations

If nested files are warranted, state clearly:

- which directories need them
- what local overrides belong there
- what should remain in the root file

Use `references/nested-files-and-token-optimization.md` for the decision rules.

## Phase 6: Token optimization pass

Before finalizing:

- delete repeated guidance
- compress broad prose into concrete rules
- remove background explanations the agent does not need
- avoid restating information that is better discovered from the repo
- keep the root file small enough that it reads like an execution guide, not a handbook

If a topic is useful but bulky, move the detail to existing repo docs and point to them from `AGENTS.md` instead of inflating the file.

## Quality bar

The finished `AGENTS.md` should:

- help a coding agent act correctly on the first pass
- include commands and constraints that are actually grounded in the repo
- stay generic enough to remain portable across agent tools
- avoid tool branding unless the repo explicitly depends on it
- recommend nested files only when the repository layout truly needs them

## Examples

### Example: greenfield repo instructions

User request:
`Create an AGENTS.md for this repository.`

Expected behavior:

1. Inspect manifests, CI workflows, README files, and the directory layout.
2. Ask only the missing questions about undocumented constraints.
3. Draft a root `AGENTS.md` with setup, test, lint, review, and safety rules.
4. Recommend nested files only if the repo has clearly different subtrees.
5. Tighten the final wording for token efficiency.

### Example: migrate CLAUDE.md-style guidance

User request:
`Convert this repo's CLAUDE.md guidance into AGENTS.md.`

Expected behavior:

1. Read the existing instruction files and the source-of-truth repo docs.
2. Preserve repo-specific operational rules.
3. Remove stale or product-specific phrasing that does not belong in a generic `AGENTS.md`.
4. Produce a cleaner root `AGENTS.md` and note whether any nested overrides are needed.

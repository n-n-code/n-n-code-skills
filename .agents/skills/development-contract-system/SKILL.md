---
name: development-contract-system
description: Build a portable change-contract system for any repository. Use when creating or porting a repository workflow based on tracked feature records, lifecycle directories, a policy file, a checker, a lifecycle transition helper, and aligned docs/tests.
---

# Development Contract System

Use this skill when a repository needs a deterministic, reviewable workflow for
tracking substantive work through repo-owned feature records instead of ad hoc
notes.

This skill is self-contained on purpose so it can be moved into another repo or
skill collection without depending on the smaller contract skills from this
frame at runtime.
When the target repo already uses local skills, also generate a thin repo-local
process overlay that applies `development-contract-process` against the repo's
concrete policy path and helper commands.

## What this skill builds

A complete repository-local contract system with these parts:

- a repo-owned policy file
- a `feature_records/` directory with lifecycle subdirectories
- a Markdown template for new records
- a root `feature_records/README.md`
- a checker script that validates record structure and changed-path coverage
- a lifecycle transition helper script
- direct shell tests for the checker and lifecycle helper
- repo docs that explain how maintainers should use the system
- optionally, a repo-local process overlay skill that points at the concrete
  policy file, checker command, helper command, and validation profiles

Recommended default layout:

```text
config/change-contract-policy.sh
feature_records/
  README.md
  TEMPLATE.md
  planned/
  active/
  done/
  superseded/
scripts/check-change-contracts.sh
scripts/set-feature-record-lifecycle.sh
scripts/test-change-contracts.sh
scripts/test-feature-record-lifecycle.sh
```

## Use this skill when

- a repo needs tracked change contracts for substantive work
- maintainers need to see what is active, planned, done, or superseded at a glance
- the team wants explicit implementation and verification evidence
- the repo should remain deterministic even if agent-specific folders disappear
- you are porting this workflow from one repo to another

## Do not use this skill when

- the repo only needs a simple issue tracker or TODO list
- the team does not want repo-tracked process artifacts
- there is no appetite for maintaining a checker and template contract

## Core outcome

After this skill is applied, the repository should support this flow:

1. Substantive work requires a feature record update.
2. Feature records live under lifecycle folders:
   `planned/`, `active/`, `done/`, `superseded/`.
3. The record's folder must match its `## Lifecycle` `State`.
4. A checker validates structure, ownership, evidence, and lifecycle placement.
5. A helper script moves records between lifecycle folders and updates the
   lifecycle fields deterministically.
6. Repo docs explain the system clearly enough for maintainers who never use an
   AI assistant.

## Build order

Implement in this order to avoid drift:

1. Discover the repo's real substantive-change surface.
2. Create the repo-owned policy file.
3. Create the `feature_records/` tree and template.
4. Implement the checker against the policy file.
5. Add lifecycle example records or seed records.
6. Add the lifecycle transition helper.
7. Add shell tests for the checker and helper.
8. If the repo uses local skills, add a thin repo-local process overlay that applies the portable process skill to the concrete repo policy.
9. Update README, AGENTS-style docs, and release/hygiene docs.
10. Run the checker and hygiene lanes and fix drift.

## Phase 1: Ground in the repo

Before adding anything:

- read the repo's main README and agent or maintainer guidance if present
- identify the directories and top-level files that count as substantive
- identify existing validation commands
- identify whether the repo already has a tracked plans folder or release
  checklist
- identify whether the repo is CMake-first, Makefile-based, Cargo-based, npm,
  or another ecosystem so command examples fit the repo

Do not guess substantive paths if the repo already has clear boundaries in docs,
workflows, or layout.

## Phase 2: Create the policy file

Create one repo-owned policy file in a neutral location such as:

- `config/change-contract-policy.sh`
- `repo_meta/change-contract-policy.sh`

Do not place it under `.agents/` if repo scripts, CI, or humans depend on it.

The policy file should declare:

- plan directory
- template basename
- substantive path patterns
- substantive top-level files
- required section headings
- allowed lifecycle values
- allowed uncertainty/cost values
- allowed evidence statuses
- allowed yes/no values when evidence entries track impact
- allowed implementation/verification status values when ownership notes are enforced
- evidence lane names
- checker command
- named validation profiles

Good default values:

- plan directory: `feature_records`
- template basename: `TEMPLATE.md`
- lifecycle values: `planned`, `active`, `superseded`, `done`
- evidence lanes: `Tests`, `Docs`, `Analyzers`, `Install validation`,
  `Release hygiene`

## Phase 3: Create `feature_records/`

Create this structure:

```text
feature_records/
  README.md
  TEMPLATE.md
  planned/
  active/
  done/
  superseded/
  .gitignore
```

The root `README.md` should explain:

- what the directory is for
- what each lifecycle folder means
- that folder and lifecycle state must match
- that `superseded/` records must set `Superseded by`
- how to use the lifecycle transition helper

The template should require sections similar to:

- `Motivation`
- `Proposed Behavior`
- `Lifecycle`
- `Contract`
- `Uncertainty And Cost`
- `Responsibilities`
- `Evidence Matrix`
- `Implementation Notes`
- `Verification Notes`
- `Waivers`
- `Files to Add/Modify`
- `Testing Strategy`

The template should say that records belong in the lifecycle folder matching
their `State`.

The `.gitignore` should:

- ignore everything by default
- keep `.gitignore`, `README.md`, and `TEMPLATE.md`
- keep lifecycle directories
- keep Markdown files inside lifecycle directories

## Phase 4: Implement the checker

Create a repo-owned checker script, typically
`scripts/check-change-contracts.sh`.

The checker should:

- load the policy file
- detect changed files from:
  - an explicit env var override
  - a git diff range when available
  - local modified/untracked files otherwise
- decide whether a substantive repo-owned change occurred
- fail if substantive changes exist without a non-template feature record update
- scan feature records recursively under `feature_records/*/*.md`
- ignore `feature_records/README.md` and `feature_records/TEMPLATE.md`
- validate required sections
- validate lifecycle fields
- validate evidence lanes and allowed statuses
- validate implementation owner versus responsibilities implementer
- validate verification owner versus responsibilities verifier
- validate self-validation and waiver rules
- validate that the parent lifecycle directory matches the `Lifecycle` state
- require `Superseded by` when the state is `superseded`

Prefer a lightweight shell checker with `awk` if the repo already uses shell for
workflow enforcement. If the repo is strongly standardized on another scripting
language, it is acceptable to implement the checker in that language instead.

## Phase 5: Add lifecycle examples

Seed the system with at least one valid example record in each lifecycle folder:

- one `planned`
- one `active`
- one `done`
- one `superseded`

The `superseded` example must point to a real replacement record.

These examples make the workflow browseable immediately and help humans
understand the intended shape without reading the template first.
If the repo already has real records ready to migrate, real records are better
than synthetic examples.

## Phase 6: Add the lifecycle transition helper

Create a repo-owned helper such as:

- `scripts/set-feature-record-lifecycle.sh`

It should:

- accept `<record-path> <target-state>`
- optionally accept `--repo-root`
- require `--superseded-by <path>` for `superseded`
- validate that the record exists
- validate that it lives under the feature-records tree
- reject the root `README.md` and `TEMPLATE.md`
- update the `Lifecycle` `State`
- update `Superseded by`
- move the file into the correct lifecycle directory

Good default transition usage:

```bash
bash scripts/set-feature-record-lifecycle.sh feature_records/planned/<record>.md active
bash scripts/set-feature-record-lifecycle.sh feature_records/active/<record>.md done
bash scripts/set-feature-record-lifecycle.sh \
  --superseded-by feature_records/done/<replacement>.md \
  feature_records/active/<record>.md superseded
```

## Phase 7: Add tests

Add direct tests for both the checker and the lifecycle helper.

Checker tests should cover:

- valid record passes
- missing required section fails
- invalid uncertainty/status values fail
- missing verifier fails
- waived without rationale fails
- superseded without pointer fails
- mismatched lifecycle folder and `State` fails
- substantive change without record update fails
- policy override with a different plan directory still works

Lifecycle helper tests should cover:

- moving `planned -> active`
- moving `active -> done`
- moving `active -> superseded` with replacement
- rejecting `superseded` without replacement
- checker still passes after helper-driven transitions

Prefer shell tests when the checker/helper are shell scripts.

## Phase 8: Add a repo-local process overlay when the repo uses skills

If the target repository keeps project-local skills, generate a thin overlay
that:

- names the concrete policy file path
- tells the agent to apply `development-contract-process`
- names the checker command and lifecycle helper command
- points at the repo policy's validation profiles
- avoids restating schema details already enforced by policy and checker

Do not generate this overlay when the repo does not use local skills. The repo
must remain usable for humans and scripts without any skill dependency.

## Phase 9: Update docs

Update the repo docs so a human maintainer can use the system without the skill:

- main README
- AGENTS-style maintainer guidance
- release checklist or hygiene docs
- feature-records README

The main README should include a readable lifecycle diagram, for example:

```text
                 start work                 complete + verify
  +-----------+  ---------->  +----------+  ----------------->  +--------+
  | planned/  |               | active/  |                     | done/  |
  +-----------+               +----------+                     +--------+
                                     |
                                     | replace with newer record
                                     v
                               +---------------+
                               | superseded/   |
                               +---------------+

  rule: records in `superseded/` must set `Superseded by` to the replacement record
```

Also document the lifecycle helper command explicitly.

## Decision rules

- Prefer repo-owned files under `config/`, `scripts/`, and `feature_records/`
  over agent-specific locations.
- Keep the policy file as the single source of truth for checker behavior.
- Keep the checker and lifecycle helper deterministic and local-first.
- Prefer a small explicit schema over a flexible but vague document format.
- Keep feature records as Markdown so they are easy to review in git.
- Keep lifecycle visibility obvious from the directory tree.
- Seed each lifecycle folder with an example record unless the repo already has
  real records.
- When the repo uses local skills, keep the repo-local process overlay thin and aligned
  with the policy, checker, template, and docs.
- If the repo has a release checklist, point it at the checker and lifecycle
  docs.

## Final acceptance criteria

The system is complete when:

- the repo has a neutral policy file
- `feature_records/` exists with root docs/template and lifecycle subdirectories
- the checker enforces lifecycle and evidence rules
- the helper script performs lifecycle transitions deterministically
- direct tests exist for checker and helper
- if the repo uses local skills, the repo-local process overlay points at the concrete
  policy/checker/helper without duplicating schema literals
- repo docs explain the lifecycle model and helper commands
- the repo's hygiene or validation path includes the checker

## Output expectations

When using this skill, leave behind:

- the full repo-owned contract system
- example lifecycle records or migrated real records
- tests that prove checker and helper behavior
- docs aligned with the system
- a concise summary of what was validated and what remains manual

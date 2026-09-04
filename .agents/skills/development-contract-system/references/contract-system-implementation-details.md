# Contract System Implementation Details

Load this reference while implementing `development-contract-system`. Keep the
main skill focused on build order and acceptance criteria; keep schema,
checker, helper, and docs mechanics here.

## Policy file

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

Good defaults:

- plan directory: `feature_records`
- template basename: `TEMPLATE.md`
- lifecycle values: `planned`, `active`, `superseded`, `done`
- evidence lanes: `Tests`, `Docs`, `Analyzers`, `Install validation`,
  `Release hygiene`

## Feature records tree

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

## Checker behavior

Create a repo-owned checker script, typically
`scripts/check-change-contracts.sh`.

The checker should:

- read the policy file; document trusted-code execution if shell policy is sourced
- detect changed files from an explicit env var override, a git diff range when
  available, or local modified/untracked files otherwise
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

Handle changed-path input without whitespace splitting, including renamed and
deleted files. A record update must cover the actual substantive change; an
unrelated record or synthetic example cannot satisfy coverage. Validate the
replacement target of a superseded record and reject broken or cyclic links.

Prefer a lightweight shell checker with `awk` if the repo already uses shell for
workflow enforcement. If the repo is strongly standardized on another scripting
language, it is acceptable to implement the checker in that language instead.

## Lifecycle examples

Keep clearly labeled, valid test fixtures for each lifecycle state:

- one `planned`
- one `active`
- one `done`
- one `superseded`

The `superseded` example must point to a real replacement record.

Keep synthetic examples outside the live record inventory and exclude them from
changed-path coverage. Demonstrate the workflow in docs or fixtures without
claiming that invented work was performed or independently verified. Migrate
real records when available, preserving their actual status and evidence.

## Lifecycle helper

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

Resolve source and destination under the configured record tree, including
symlink behavior. Reject collisions and unsafe paths before mutation. Stage the
updated content and transition so a failure cannot silently lose the original
or leave folder/state disagreement; restore only helper-owned changes. Validate
the replacement record before superseding and preserve unrelated edits.

Good default transition usage:

```bash
bash scripts/set-feature-record-lifecycle.sh feature_records/planned/<record>.md active
bash scripts/set-feature-record-lifecycle.sh feature_records/active/<record>.md done
bash scripts/set-feature-record-lifecycle.sh \
  --superseded-by feature_records/done/<replacement>.md \
  feature_records/active/<record>.md superseded
```

## Direct tests

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
- renamed/deleted paths and filenames containing spaces are handled correctly
- an unrelated record or example fixture cannot satisfy changed-path coverage

Lifecycle helper tests should cover:

- moving `planned -> active`
- moving `active -> done`
- moving `active -> superseded` with replacement
- rejecting `superseded` without replacement
- checker still passes after helper-driven transitions
- destination collision and paths outside the record tree leave inputs intact
- write/move failure preserves or restores a consistent original record
- invalid or cyclic replacement links are rejected

Prefer shell tests when the checker/helper are shell scripts.

## README diagram

When useful, include a readable lifecycle diagram:

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

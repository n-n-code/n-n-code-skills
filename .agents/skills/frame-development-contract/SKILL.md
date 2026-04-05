---
name: frame-development-contract
description: Repo-local overlay for the development contract system in this frame. Use when work may trigger a tracked change contract and you need the repo's concrete policy, plan directory, or validation profiles.
---

# Frame Development Contract

Read `config/change-contract-policy.sh`, then apply the shared development-contract workflow from `development-contract-core`.
Treat repo guidance as secondary to the policy file for contract mechanics; if they disagree, fix the mismatch instead of guessing.

## Use this skill when

- work may touch a substantive path or top-level file listed in `config/change-contract-policy.sh`
- creating, updating, or verifying a non-template plan under the repo policy's plan directory
- deciding which validation profile this repo expects for a change

Do not use this skill alone for generic coding advice; pair it with a more specific implementation skill when needed.

## Repo overlay workflow

1. Read the touched files before editing.
2. Read `config/change-contract-policy.sh` for the plan directory, substantive path rules, required lanes, and validation profiles.
3. Apply `development-contract-core` for the generic workflow and decision rules.
4. If the change is substantive under repo policy, update a non-template plan in the lifecycle subdirectory under `feature_records/` that matches the record's `State`.
   Prefer `bash scripts/set-feature-record-lifecycle.sh` when changing an existing record's lifecycle.
5. Keep verifier notes concrete: record commands, observed results, and any contract mismatches explicitly.
6. Run the smallest repo policy profile that proves the change, then extend when the surface justifies it.
7. Before closing work, run the checker command declared in `config/change-contract-policy.sh`.

## Decision rules

- Treat `config/change-contract-policy.sh` as the source of truth for what is substantive in this repo.
- Do not leave a substantive change without a non-template plan update.
- Use `bash scripts/set-feature-record-lifecycle.sh --superseded-by ...` when superseding a record so the replacement link is updated with the move.
- Keep the repo overlay thin: change policy data first, then only add prose when the repo needs extra human guidance that policy cannot express.
- If repo policy and docs disagree, fix the policy or the docs so the checker, template, and guidance converge again.

## Repo validation profiles

Use the policy file's named profiles as the default command sets:

- `FRAME_CONTRACT_VALIDATION_PROFILE_DOCS`
- `FRAME_CONTRACT_VALIDATION_PROFILE_CODE`
- `FRAME_CONTRACT_VALIDATION_PROFILE_RELEASE`

## Output expectations

When this skill applies, the final work should leave behind:

- code or docs aligned with repo guidance and policy
- an updated non-template `feature_records/<state>/...` plan when the change is substantive
- explicit verifier evidence in the plan
- repo policy, docs, and checker behavior that still agree
- a concise report of what was validated and what could not be validated

## Examples

- `Implement this feature in src/ and wire the tests`:
  read `config/change-contract-policy.sh`, update the relevant `feature_records/active/*.md` plan, implement narrowly, run the code profile, and record verifier commands/results.
- `Update the CI workflow to enforce a new repo rule`:
  treat it as substantive workflow work under policy, update the plan, run the checker, and verify workflow/docs alignment.
- `Finish a feature and accept it`:
  update verification evidence, then run `bash scripts/set-feature-record-lifecycle.sh feature_records/active/<record>.md done`.
- `Port this contract system into another repo`:
  copy the core skill, checker, template, and policy file, then edit the policy file before changing any repo-specific prose.

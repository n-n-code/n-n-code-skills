---
name: development-contract-process
description: Portable workflow for repos that require tracked change contracts, verifier evidence, and smallest-proof validation. Use when a repo has a contract policy file or enforced feature-plan checker.
---

# Development Contract Process

Find the repo's contract policy file and use it as the source of truth for repo-specific paths, plan locations, lanes, and validation profiles.
Treat any separate repo guidance as secondary unless it contradicts policy; if it does, fix the mismatch instead of guessing.

This is a process overlay, not a thinking aid. Pair it with the repo's implementation skill for the touched code and any repo-local contract overlay that names the actual policy path and helper commands.

## Use this skill when

- work may trigger a tracked change contract
- a repo requires a plan update for substantive changes
- a checker validates plan structure, ownership, or evidence
- you need to choose the smallest proving validation set for a substantive change

## Core workflow

1. Read the touched files and the repo contract policy file before editing.
2. Decide whether the change is substantive using policy data rather than guesswork.
3. If the change is substantive, create or update a non-template plan in the policy-defined plan directory.
4. Keep the plan aligned with the repo's enforced template, required evidence lanes, and lifecycle-directory rules.
5. Keep implementation ownership and verification ownership explicit.
6. Record verifier commands, observed results, and contract mismatches concretely.
7. Run the smallest validation profile that proves the change, then extend only when the surface justifies it.
8. Before closing work, run the repo's checker command and any additional checks implied by the chosen validation profile.

## Operator quickstart

Use this compact path unless the repo overlay says otherwise:

1. Read the touched files.
2. Read the repo policy file.
3. Decide whether the touched paths are substantive under policy.
4. If substantive, update the existing non-template record or create one from the repo template.
5. Implement narrowly.
6. Record verifier commands, observed results, and mismatches in the record.
7. Run the smallest proving validation profile plus the checker command.
8. If lifecycle state changed, use the repo's lifecycle helper instead of a manual move.

## Decision rules

- Treat the policy file as the single source of truth for substantive-path detection, plan location, section requirements, lane names, and default validation commands.
- If the repo ships a lifecycle transition helper, prefer it over manual file moves so path and lifecycle state stay synchronized.
- Do not duplicate repo literals across the skill, docs, checker, and template when policy can express them once.
- Keep the schema stable by default; use policy for repo-level variation and only change the schema when portability or correctness requires it.
- Prefer small repo overlays over forking the core skill.
- If a repo needs extra instructions that policy cannot express, add them in a thin overlay skill rather than bloating the core.
- Prefer updating an existing active record over creating scattered new notes for the same change.
- Keep the operator path lightweight: policy decides what is substantive, and the checker enforces the contract.

## Output expectations

When this skill applies, the final work should leave behind:

- code or docs aligned with repo guidance and policy
- a plan update when the change is substantive
- explicit verifier evidence
- a concise report of what was validated and what could not be validated

## References

- `references/policy-reference.md` for the portable policy surface and adoption rules
- `references/operator-quickstart.md` for the compact day-to-day usage path
- `references/repo-overlay-template.md` for the expected shape of a repo-local overlay
- `references/run-release-checklist.example.sh` for a CMake-first pre-release runner scaffold example

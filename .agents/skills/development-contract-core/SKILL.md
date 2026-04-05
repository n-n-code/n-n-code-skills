---
name: development-contract-core
description: Portable workflow for repos that require tracked change contracts, verifier evidence, and smallest-proof validation. Use when a repo has a contract policy file or enforced feature-plan checker.
---

# Development Contract Core

Find the repo's contract policy file and use it as the source of truth for repo-specific paths, plan locations, lanes, and validation profiles.
Treat any separate repo guidance as secondary unless it contradicts policy; if it does, fix the mismatch instead of guessing.

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

## Decision rules

- Treat the policy file as the single source of truth for substantive-path detection, plan location, section requirements, lane names, and default validation commands.
- If the repo ships a lifecycle transition helper, prefer it over manual file moves so path and lifecycle state stay synchronized.
- Do not duplicate repo literals across the skill, docs, checker, and template when policy can express them once.
- Keep the schema stable by default; use policy for repo-level variation and only change the schema when portability or correctness requires it.
- Prefer small repo overlays over forking the core skill.
- If a repo needs extra instructions that policy cannot express, add them in a thin overlay skill rather than bloating the core.

## Output expectations

When this skill applies, the final work should leave behind:

- code or docs aligned with repo guidance and policy
- a plan update when the change is substantive
- explicit verifier evidence
- a concise report of what was validated and what could not be validated

## References

- `references/policy-reference.md` for the portable policy surface and adoption rules
- `references/run-release-checklist.example.sh` for a portable pre-release runner scaffold

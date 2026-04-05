# Repo Overlay Template For Development Contract

Use this as the shape of the repo-local overlay that sits on top of `development-contract-process`.

## Responsibilities of the repo overlay

- name the actual repo policy file path
- name the actual checker command
- name the lifecycle helper command if the repo has one
- call out repo-specific validation profiles when they exist
- identify any repo-specific substantive paths or human workflow rules that policy alone cannot express

## Recommended structure

- Start by telling the agent to read the repo policy file, then apply `development-contract-process`.
- Keep repo-specific instructions thin and operational.
- Treat the policy file as the source of truth for contract mechanics.
- Prefer changing policy data first, then docs, instead of duplicating literals in several places.

## Example overlay flow

1. Read the touched files.
2. Read the repo policy file.
3. Apply `development-contract-process`.
4. If the change is substantive under policy, update a non-template record in the repo's plan directory.
5. Use the lifecycle helper when changing record state.
6. Run the smallest proving validation profile and then the checker command.

## Anti-patterns

- Do not write the overlay as if every repo uses the same policy path, plan directory, or script names unless this is actually true.
- Do not restate schema details already enforced by policy and checker.
- Do not let the overlay drift away from the generated repo docs, template, or checker behavior.

# Development Contract Policy Reference

Use a small repo-local policy file as the source of truth for contract enforcement.

## Minimum policy surface

- plan directory
- template basename
- substantive path patterns
- substantive top-level files
- required section headings
- allowed lifecycle values
- allowed uncertainty/cost values
- evidence lane names
- checker command

Prefer a repo-neutral path such as `config/change-contract-policy.sh`, when the repository itself, CI, or shell scripts depend on the policy.

## Recommended additions

- named validation profiles such as `docs`, `code`, and `release`
- repo-specific examples for install or smoke-test commands
- comments that explain why a path or lane is part of the contract
- a release-runner example kept as a skill reference, while the runnable repo copy lives under `scripts/`
- a repo-owned lifecycle helper when records live in state-specific subdirectories

## Portability rules

- keep policy data repo-local and declarative
- keep the core skill generic
- keep the checker reading the same policy file that humans read
- keep template and docs aligned with policy names
- keep lifecycle folder rules and any transition helper aligned with the checker
- prefer extending policy over cloning the core skill

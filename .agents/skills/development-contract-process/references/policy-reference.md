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
- allowed yes/no values when evidence lines encode impact
- allowed implementation/verification status values when ownership lanes are enforced
- allowed evidence statuses
- evidence lane names
- checker command

Prefer a repo-neutral path such as `config/change-contract-policy.sh`, when the repository itself, CI, or shell scripts depend on the policy.

## Recommended additions

- named validation profiles such as `docs`, `code`, and `release`
- comments that explain the repo's substantive surface and why a path is included
- repo-specific examples for install or smoke-test commands
- a release-runner example kept as a skill reference, while the runnable repo copy lives under `scripts/`
- a repo-owned lifecycle helper when records live in state-specific subdirectories
- a policy variable for the policy file path itself when the repo wants wrappers to export it explicitly

## Portability rules

- keep policy data repo-local and declarative
- keep the core skill generic
- keep the checker reading the same policy file that humans read
- keep template and docs aligned with policy names
- keep lifecycle folder rules and any transition helper aligned with the checker
- prefer extending policy over cloning the core skill
- keep examples honest about ecosystem scope; if an example is CMake- or language-specific, say so directly

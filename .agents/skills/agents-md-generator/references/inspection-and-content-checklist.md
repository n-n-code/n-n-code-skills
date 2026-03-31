# Inspection and content checklist

Use this checklist before drafting or revising `AGENTS.md`.

## Repo inspection

- Find any existing `AGENTS.md`, `CLAUDE.md`, `README.md`, and `CONTRIBUTING.md`.
- Inspect package/build/test/lint configuration.
- Inspect CI workflows for the real validation path.
- Identify major subtrees with different toolchains or workflows.
- Identify generated code, vendor trees, migrations, secrets, deployment surfaces, or other risk areas.

## Root AGENTS.md coverage

- State the repo purpose only if it helps execution.
- Include the setup/build/test/lint commands an agent should actually run.
- Include commit, PR, or review expectations if the repo clearly has them.
- Include repo-specific guardrails and forbidden actions.
- Point to deeper docs rather than copying them.
- Keep the file operational, not aspirational.

## Revision checks

- Remove duplicate guidance copied from other docs.
- Remove stale commands or instructions contradicted by the repo.
- Remove product-specific branding unless it is intentionally required.
- Preserve important local rules and safety constraints.

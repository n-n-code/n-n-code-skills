# Inspection and content checklist

Use this when repository inspection is non-trivial: migrations, multiple manifests or instruction sources, risky validation, conflicting evidence, or a dirty target-file worktree.

## Instruction and worktree state

- Find all root and nested `AGENTS.md` files plus tool-specific instruction entry points such as `CLAUDE.md`.
- Read the applicable existing instructions before proposing replacements or overrides.
- When Git is available, inspect `git status --short` and the target-file diff. Treat existing changes as user-owned and never discard them.
- Identify the intended output path and the directories it governs.

## Repository sources

- Read the minimum relevant `README.md`, `CONTRIBUTING.md`, release, architecture, and policy documentation.
- Inspect package manifests, lockfiles, build files, task runners, test and lint configuration, and CI workflows.
- Identify monorepo packages, apps, services, or other subtrees with materially different toolchains or workflows.
- Identify generated code, vendor trees, migrations, deployment surfaces, and secret-bearing paths. Identify secret locations without reading or reproducing secret values.
- When nesting, adapters, or cross-host compatibility affects the result, check whether the relevant hosts support `AGENTS.md`, nested scope, or another required instruction entry point. Do not infer compatibility from file naming alone.

## Command evidence and execution safety

- Trace every proposed command to an executable configuration or maintained repository document.
- Distinguish what the repository declares from what the current environment can execute.
- Before running a command, assess expected duration, writes, generated artifacts, dependency installation, network access, credentials, and external side effects.
- Prefer the smallest safe command that tests the claim. Ask before costly, destructive, networked, or externally mutating validation.
- Record the exact repository source and execution result separately for material commands; do not remove a valid command solely because the local environment lacks a runtime or dependency.

## Root `AGENTS.md` coverage

- State repository purpose and key structure only where they change agent behavior.
- Include setup, build, test, lint, or validation commands only when repository evidence supports them; state when each applies.
- Include commit, PR, ownership, or review expectations only when explicit policy supports them.
- Include repo-specific guardrails, generated or vendored boundaries, and high-risk operational constraints.
- Point to maintained deeper docs rather than copying them.
- Keep the file operational rather than aspirational, and keep temporary audit findings in the handoff.

## Revision and completion checks

- Preserve unrelated sections and pre-existing worktree changes.
- Remove duplicate, stale, contradicted, or unnecessarily product-branded guidance.
- Verify every mentioned path against the filesystem; use Git inventory as supplemental evidence rather than the sole source.
- Review the final diff for accidental scope expansion and unresolved placeholders.
- Report exact validation performed, checks not run, environment limitations, conflicts, assumptions, and artifacts left behind.

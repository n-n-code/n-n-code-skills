---
name: fuse-skills
description: Combine 2 or more agent skills into one new merged skill without duplicated guidance or lost capability. Use when the user asks to merge, fuse, consolidate, deduplicate, or unify multiple local skills, `skills.sh` skills, or a mix of both into a single portable, precision-dense skill package. Do not use for ordinary multi-skill composition unless the goal is to create a new fused skill.
---

# Fuse Skills

Create one fused skill that keeps the useful behavior from all source skills,
removes overlap, and stays cheap to load.

## Use this skill for

- merging multiple skill folders into one new skill
- combining local repo skills with explicitly named `skills.sh` skills
- removing duplicated rules across overlapping skills
- creating a stronger portable skill while preserving local value when local
  skills are part of the input

## Not for

- runtime composition of several skills without creating a new fused skill
- choosing which existing skills to load for a task when no merged output is
  wanted
- revising only one skill in place unless the goal is to fold other skills into
  it
- broad discovery of related remote skills the user did not ask for

## Required inputs

The user must provide all source skills to combine.

Allowed source-specification levels:

- **fully specified source:** exact local skill path/name, exact inline content, or
  exact remote `owner/repo` plus skill name(s)
- **package-specified remote source:** exact remote `owner/repo`, but the user has
  not yet pinned the skill name(s) inside that package
- **bounded local-family source:** a named local skill family such as
  `backend-*`, `ui-*`, or "the development-contract skills" where the user is
  explicitly asking to fuse local skills from this repo and the family can be
  resolved by inspecting local folders only

Do not accept open-ended discovery beyond those bounds. If the user has not
identified either a specific local skill/family, a specific remote skill, or a
specific package to inspect, stop and ask for that missing scope.

For each source, identify whether it is:

- a local repo skill
- a bounded local repo skill family that must be resolved to explicit local
  skill names before fusion
- an explicit `skills.sh` skill from a named owner/repo package
- raw skill content provided inline

Do not expand scope beyond the provided sources or explicitly named packages.

For remote sources, capture both:

- the package identity in `owner/repo` form
- the specific skill name or names to fuse from that package

If the user provides a GitHub URL instead of `owner/repo`, normalize it to
`owner/repo` before continuing.

If the user provided only a package-specified remote source, you may inspect
that package only to resolve the intended skill name(s). Do not broaden into
general package discovery or substitute a different package.

## Core workflow

1. Inspect the local repo first for relevant conventions, nearby skills, and any
   existing skill-generation guidance.
2. Classify each source as local repo skill, remote `skills.sh` skill, or
   inline content. If the user named a bounded local family, inspect only
   matching local folders, resolve the exact skill names, and report that
   resolution before continuing. Read local sources immediately. For remote
   sources, proceed to step 3.
3. Acquire remote sources through this fallback chain. Stop at the first tier
   that succeeds for each source.

   **Tier 1 — local copies.** Check `skills-lock.json` and
   `npx skills list --json` for already-installed copies of the requested
   skills. If found, read them directly. This is the preferred path because it
   avoids repo mutations.

   **Tier 2 — CLI fetch.** If not installed locally:
   - Verify the CLI is available with `npx skills --help`. If the CLI is
     missing or Node/npm is unavailable, skip to Tier 3.
   - Treat remote sources as package-scoped skills in a named `owner/repo`.
     If the user provided a GitHub URL, normalize it to `owner/repo` first.
   - If the user specified only the package, use `npx skills add <owner/repo> -l`
     only to list that package's skills so you can resolve the exact skill
     name(s). Once resolved, continue with explicit names.
   - Use `npx skills add <owner/repo> --skill <skill-names>` to fetch only
     the named skills.
   - Prefer the least invasive acquisition path available. Use project-local
     installation only when read-only local inspection is unavailable. Do not
     use `--global` unless the user explicitly asked for it.
   - Do not use `skills find` or broad package discovery unless the user asked
     for discovery rather than fusion.
   - Treat fetches as repo mutations. Before any install, note whether the
     worktree is already dirty. After fetching, isolate or clearly report any
     files added or changed as acquisition artifacts, and do not fold them into
     the final deliverable unless the user asked for that.

   **Tier 3 — user-provided content.** If both Tier 1 and Tier 2 fail (no
   local copy, CLI unavailable, network blocked, policy constraints), ask the
   user to provide the skill content inline or as file paths. Do not proceed
   with incomplete sources.
4. Load every source skill (local, fetched, and inline) and record:
   - its trigger scope
   - core workflow steps
   - high-value decision rules
   - references, scripts, or assets that materially matter
   - obvious repetition, drift, or weak sections
   - remote baggage that should probably not ship: giant catalogs, data dumps,
     installer-specific metadata, broad stack assumptions, or helper scripts
     whose value does not survive the fusion
5. Check fusion compatibility before proceeding.
   - Compare the trigger scopes across sources. If one skill says "use for X"
     and another says "never use for X," flag the conflict.
   - Compare capability requirements. If one source needs code execution and
     another needs web search with no overlap in workflow, note the mismatch.
   - Compare abstraction levels. A meta-skill (how to design skills) and a
     domain skill (how to deploy containers) rarely fuse well.
   - If sources are incompatible, recommend against fusion or propose partial
     fusion: a fused core for the compatible subset, plus a companion skill for
     the rest. Do not proceed to the matrix with incompatible sources unless the
     user explicitly overrides.
   - **Fast path:** if all sources are local, there are only 2–3 of them, and
     compatibility is clear (no conflicts, same abstraction level, overlapping
     triggers), use the compact fusion matrix path:
     - write a compact fusion matrix instead of the full matrix:
       `source → keep / merge / drop + reason`
     - keep the same compatibility, stance, generation, and review standards
     - escalate to the full matrix only if a conflict, overlap ambiguity, or
       scope split appears during drafting
6. Build a fusion matrix. For each source skill, extract rows into this
   structure:

   | Source | Element type | Content summary | Verdict |
   |--------|-------------|-----------------|---------|
   | skill-a | trigger | "use when merging…" | keep — broadest scope |
   | skill-a | workflow-step | "load sources" | merge with skill-b step 1 |
   | skill-b | decision-rule | "prefer local naming" | keep — unique |
   | skill-b | reference | "checklist.md" | drop — subsumed by fused review |

   Element types: `trigger`, `workflow-step`, `decision-rule`, `reference`,
   `example`, `anti-pattern`.

   Verdicts: `keep` (into fused core), `merge` (combine with another row),
   `move-to-ref` (demote to references), `drop` (with reason: duplicate /
   weaker / stale / out-of-scope).

   After filling the matrix, confirm:
   - Every high-value behavior has a `keep` or `merge` verdict
   - Every `drop` has an explicit reason
   - Conflicting rows are resolved with a winner and rationale
7. Choose the fusion stance:
   - if any source is a local repo skill, prefer naming, structure, and
     heuristics closer to the local repo when that produces a better local
     result
   - otherwise prefer the most portable wording and structure that preserves
     execution quality
8. Generate a new fused skill package.
   - Default output: a new skill folder with `SKILL.md`
   - In this repo, place new local skills under `.agents/skills/<skill-name>/`
   - If the requested destination already exists, revise it in place only when
     the user clearly asked to replace or extend that skill. Otherwise choose a
     new narrow name and say why.
   - Add `references/` only when detailed audit or variant-specific material
     would bloat the main file
   - Add `scripts/` only when deterministic fetching or transformation is
     meaningfully better than prose
   - If any source is a local repo skill, name the fused result in the same
     local style:
     - use kebab-case
     - avoid generic `merged-*`, `combined-*`, or `fused-*` prefixes unless the
       user asked for them
     - if one local skill is the clear base, keep its naming family and extend
       it narrowly
   - If acquisition created temporary comparison material, keep it out of the
     shipped skill package unless it materially improves repeatable execution
   - If remote acquisition installed or copied local artifacts only for
     inspection, remove those artifacts before finalizing unless the user
     explicitly asked to keep the fetched skill itself
9. Run the review pass in
   [`references/fusion-review-checklist.md`](references/fusion-review-checklist.md).
   The checklist includes simulation validation and precision-density tightening
   as final quality gates. Do not skip them — they catch execution-path bugs
   and bloat that static review misses. If any check fails, revise before
   finalizing.

## Fusion rules

- Keep one canonical version of each rule or workflow step.
- Prefer the clearest and most actionable wording, not the longest wording.
- Preserve valuable capability even when the wording changes.
- Apply the precision-density test: every surviving sentence must change agent
  behavior in at least one realistic scenario. Cut generic filler, repeated
  best-practice text, and examples that do not teach anything new.
- Review remote skills before trusting them. Preserve only guidance that holds
  up after reading the actual skill contents.
- For fetched remote skills, default to keeping heuristics and workflow rules
  while dropping bulky catalogs, datasets, helper scripts, or stack-specific
  assumptions unless they materially improve repeatable execution in the fused
  result.
- Treat cleanup as part of fusion completion: if remote inspection created local
  install artifacts, remove them unless the user asked to keep them.
- If the result still reads like several skills pasted together, refactor again
  until it has one voice and one workflow.
- If two sources disagree, prefer:
  - stronger local heuristics for local-repo use
  - otherwise the more portable and less assumption-heavy rule
- Keep the fused skill focused on one coherent job. If the compatibility gate
  (step 5) was not run or was overridden, re-check here: if sources cover
  genuinely different jobs, recommend separate skills or partial fusion instead
  of forcing a bad merge.

## Review standard

Review the fused result like a senior agent-skill designer.

When local guidance exists, use it during review, especially:

- `.agents/skills/agent-skill-generator/SKILL.md`
- `.agents/skills/agent-skill-generator/references/skill-design-checklist.md`
- `.agents/skills/agent-skill-generator/references/token-optimization.md`
- `skills-lock.json` when remote package identity or installed skill naming
  needs a local cross-check

If those files are unavailable, apply the bundled review checklist and the same
standards: strong triggers, explicit workflow, portability, no important loss,
and high precision density.

## Output requirements

The fused skill should include:

- a kebab-case skill name
- frontmatter with only `name` and `description`
- a trigger-bearing description that says what the fused skill does and when to
  use it
- one procedural `SKILL.md` that another agent can execute without guessing
- optional references only when they reduce token cost

The final response should also summarize:

- where each source came from: local repo, existing local `skills` install, new
  package fetch, or user-provided content
- whether a compact or full fusion matrix was used, and why
- which source behaviors were merged into the core workflow
- which overlapping sections were removed
- which conflicts were resolved in favor of local conventions or portability
- whether any repo mutations occurred during acquisition and how they were handled
- any functionality intentionally excluded and why

## Examples

### Example: local fusion

User request:
`Fuse these local skill folders into one new skill and remove overlap.`

Expected behavior:

1. Read the local skills and nearby repo conventions.
2. Prefer local naming and structure.
3. Produce one fused skill package with duplicate guidance removed.
4. Explain what was preserved, dropped, and rewritten.

### Example: mixed local and remote fusion

User request:
`Combine this local skill with these two skills.sh skills into one portable skill.`

Expected behavior:

1. Read the local skill first.
2. Acquire remote skills via the fallback chain: check local installs, then CLI
   fetch, then ask the user for content.
3. Run the compatibility gate before building the fusion matrix.
4. Preserve useful remote guidance, but prefer local heuristics when they better
   fit the local repo.
5. Simulate execution against representative prompts from each source.
6. Emit one fused skill package and a short merge rationale.

### Example: remote package named, skill unresolved

User request:
`Fuse this local skill with the right skill from owner/repo that handles release docs.`

Expected behavior:

1. Treat `owner/repo` as in scope, but do not inspect unrelated packages.
2. Use package inspection only to resolve the exact remote skill name.
3. Once resolved, continue with explicit skill names and the normal fusion flow.
4. Report any acquisition-side repo mutations separately from the shipped skill.

### Example: not a fusion request

User request:
`Which two existing skills should I load together for this task?`

Expected behavior:

1. Do not trigger `fuse-skills`.
2. Treat this as ordinary skill selection or composition, not creation of a new
   merged skill.

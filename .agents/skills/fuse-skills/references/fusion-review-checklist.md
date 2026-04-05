# Fusion review checklist

Use this after drafting the fused skill and before finalizing.

## Compatibility gate

- Was the compatibility gate (step 5) run before building the fusion matrix?
- If the compact fusion matrix path was used, did the draft still perform the
  same compatibility checks before skipping the full matrix?
- Were trigger scopes compared for contradictions?
- Were capability requirements compared for mismatches?
- Were abstraction levels compared (meta-skill vs. domain skill)?
- If sources were incompatible, was partial fusion offered instead of a forced
  merge?
- If the user overrode incompatibility, is that override noted in the output?

## Scope and coherence

- Does the fused skill still solve one coherent job?
- If the sources covered multiple jobs, did the result narrow scope instead of
  becoming vague?
- Are out-of-scope cases obvious?

## Overlap removal

- Is each workflow step stated once?
- Did the draft remove repeated best-practice language and duplicate examples?
- When two source rules said the same thing, did it keep only the sharper one?

## Capability preservation

- List each source skill's core workflow and decision rules.
- Record where each source was read from: local repo, existing local install,
  new fetch, or user-provided content.
- If the compact fusion matrix path was used, is there still a compact
  `keep / merge / drop` record with reasons?
- Check that every high-value behavior is either:
  - preserved in the fused core
  - moved to references
  - intentionally dropped with a reason
- If something was dropped, was it redundant, weaker, stale, or outside the new
  scope?

## Conflict resolution

- Where sources disagree, is the winning rule explicit?
- If local repo skills were inputs, did the result prefer local conventions when
  that improves local usefulness?
- If no local preference applied, did the result choose the more portable rule?

## Local naming

- If local repo skills were inputs, does the fused name look like a local skill
  name rather than a generic `merged-*` label?
- If one source was the clear base, did the naming stay close to that local
  family?

## Trigger quality

- Does the description clearly say the skill fuses multiple skills into one?
- Does it include phrases like `merge`, `fuse`, `combine`, `consolidate`, or
  `deduplicate`?
- Does it avoid triggering for ordinary multi-skill composition without creating
  a new skill?

## Remote-source verification

- Did the workflow follow the three-tier fallback chain (local → CLI → user)?
- If a remote source was not fully specified, was the package scope at least
  pinned to an exact `owner/repo` before any inspection?
- **Tier 1:** Were `skills-lock.json` and local installs checked before
  attempting a fetch?
- **Tier 2:** Was the CLI verified with `--help` before use? If unavailable,
  did it fall through to Tier 3 instead of failing?
- **Tier 2:** If a GitHub URL was provided, was it normalized to `owner/repo`?
- **Tier 2:** If package inspection was needed, was `-l` used only to resolve
  skill names inside the already-named package?
- **Tier 2:** Were explicit `--skill` arguments used instead of broad
  discovery?
- **Tier 2:** Was the least invasive acquisition path used before falling back
  to project-local installation?
- **Tier 2:** Was `--global` avoided unless the user explicitly wanted it?
- **Tier 2:** Were repo mutations from fetch/install called out and kept out of
  the shipped skill unless intentionally included?
- **Tier 3:** If Tiers 1 and 2 failed, was the user asked for inline content
  or file paths?
- Were fetched remote skill contents actually reviewed before their rules were
  merged into the fused skill?

## Simulation validation

- Were 2–3 representative user prompts tested against the fused workflow (at
  least one per source skill's primary scenario)?
- Was at least one negative prompt checked to confirm the fused skill does not
  trigger for ordinary multi-skill composition or unrelated discovery work?
- Can the agent reach every workflow step without missing context from a prior
  step?
- Are there ambiguous branches where two conditions are both true?
- Does the fused trigger fire for each test prompt, or did fusion accidentally
  narrow the trigger scope?
- Were blocked, ambiguous, or unreachable steps fixed before finalizing?

## Precision density

- Does every surviving sentence change agent behavior in at least one realistic
  scenario?
- Were conditional rules and edge-case handling preserved even when longer than
  generic alternatives?
- Should bulky comparison material move to references?
- Are examples shorter than the instructions they illustrate?
- Is the main `SKILL.md` mostly workflow and decision rules rather than
  explanation?

## Output placement

- If the result is a local repo skill, was it placed under
  `.agents/skills/<skill-name>/`?
- If the destination already existed, did the workflow either revise it because
  the user clearly asked for that, or choose a new narrow name and explain why?

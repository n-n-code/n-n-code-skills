# Skill design checklist

Use this before finalizing a generated or revised skill.

## Problem and scope

- Is the target problem concrete and repeatable?
- Is the skill solving one coherent job rather than several unrelated ones?
- Is the audience clear?
- Are out-of-scope cases obvious from the wording?

## Trigger quality

- Does the frontmatter description say what the skill does?
- Does it say when to use it?
- Does it include phrases a user would actually say?
- Does it avoid vague trigger language like `helps with` or `handles stuff`?
- If over-triggering is a risk, does the description narrow scope clearly?

## Workflow quality

- Are the main steps in the correct order?
- Does the skill investigate local context before asking avoidable questions?
- Are decision points and defaults explicit?
- Does the skill state required inputs and expected outputs?
- Are external dependencies named only when necessary?

## Packaging

- Is `SKILL.md` sufficient on its own?
- If not, are extra details moved into `references/` instead of bloating the main file?
- Are `scripts/` included only for deterministic, repetitive, or fragile tasks?
- Are `assets/` included only when they materially improve execution?

## Validation

- Are there concrete examples or scenarios?
- Does the skill define what success looks like?
- Does it describe how to catch obvious failure modes?
- If assumptions were needed, are they stated explicitly?

## Portability

- Is the wording generic unless the user explicitly asked for a product-specific skill?
- Does the skill avoid environment assumptions it cannot justify?
- If the skill is repo-bound, does it say so plainly?

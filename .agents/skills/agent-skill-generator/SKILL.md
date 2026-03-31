---
name: agent-skill-generator
description: Create or revise reusable agent skills from a problem statement, workflow, or existing skill folder. Use when the user asks to build a skill, design an agent skill for a repo, improve a skill's triggering or structure, audit a skill for token efficiency, or turn a repeated workflow into a portable skill package.
---

# Agent skill generator

Create skills that are generic first, portable across agent environments, and token-optimized.

## Core workflow

1. Capture the target problem.
2. Investigate the current repo for relevant code, docs, scripts, schemas, prompts, and existing skills before asking avoidable questions.
3. Interrogate the user until the target skill is decision-complete.
4. Create or revise the skill package.
5. Run a token-optimization pass before finalizing.

Do not skip steps 2-5 unless the user explicitly narrows scope.

## Phase 1: Capture the target problem

Start by identifying one of these modes:

- `new skill`: create a skill from a rough problem or repeated workflow
- `revise skill`: improve an existing skill folder in place
- `audit skill`: inspect a skill for trigger quality, portability, and token waste before proposing edits

Require the user to provide at least one of:

- the problem the skill should solve
- the workflow the skill should standardize
- the existing skill folder to revise

If the user gives a vague idea, extract a provisional summary in one or two sentences before moving on.

## Phase 2: Investigate the repo first

Before asking questions, inspect the repo or working directory for facts that reduce ambiguity.

Look for:

- existing skills, prompts, plans, and workflow docs
- scripts, CLIs, templates, schemas, examples, or tests relevant to the target workflow
- repo conventions that the new skill should mirror
- tool or plugin dependencies that the skill must mention

Prefer targeted search over broad reading. Search likely directories first, then open only the most relevant files.

Use the repo investigation to answer discoverable questions such as:

- naming conventions
- likely file paths
- existing workflow steps
- validation commands
- whether references, scripts, or assets are warranted

If the repo is thin or unrelated, state that and proceed with a generic skill design.

## Phase 3: Clarification gate

Do not generate the skill until the spec is decision-complete.

Ask only questions that materially affect the generated skill. Prefer concise, direct questions. Push until these are clear:

- primary outcome and success criteria
- who will use the skill and in what environment
- clear trigger phrases and adjacent phrases that should not trigger it
- whether the skill creates, revises, audits, or all three
- required workflow steps and their order
- required inputs and expected outputs
- dependencies on repo files, scripts, tools, MCP servers, or external services
- whether the skill should ship only `SKILL.md` or also `references/`, `scripts/`, or `assets/`
- validation expectations and examples

If a choice remains open and the user does not care, pick a sensible default and record it as an explicit assumption in the final skill package.

## Phase 4: Create or revise the skill

Create a skill folder with the minimum set of files that makes the workflow repeatable.

Default package:

- `SKILL.md`
- `references/` only when details would otherwise bloat `SKILL.md`
- `scripts/` only when deterministic execution or validation is meaningfully better than prose
- `assets/` only when the skill depends on templates, icons, or other bundled artifacts

By default, keep the skill generic and portable. Do not add product-specific metadata files unless the user explicitly requests them.

### Writing rules for `SKILL.md`

- Use only `name` and `description` in YAML frontmatter
- Make `name` kebab-case
- Make `description` carry the trigger burden: what the skill does, when to use it, and concrete trigger phrases
- Keep the body procedural and imperative
- Put core workflow in the main file and move bulky detail into `references/`
- Link every reference file directly from `SKILL.md`
- Keep examples short and representative

### Recommended body shape

Use this structure unless the target skill needs a sharper format:

1. Title and one-line stance
2. Core workflow
3. Important constraints or decision rules
4. Resource map for bundled references/scripts/assets
5. A small number of concrete examples

## Phase 5: Token optimization pass

Before finalizing, aggressively remove waste.

Check for:

- long explanations of concepts the model already knows
- repeated guidance stated in multiple sections
- examples that restate the rules instead of adding signal
- variant-specific detail that belongs in `references/`
- broad "best practices" text that is not specific to the workflow
- instructions that are discoverable from the repo at runtime and do not belong in the skill

Optimize in this order:

1. Delete redundant text.
2. Compress wording.
3. Move detailed material into `references/`.
4. Replace prose with a short checklist when fidelity is unchanged.

If you slim the package, preserve behavior. The goal is lower token cost without losing trigger quality or execution reliability.

Use `references/token-optimization.md` as the final audit checklist.

## Quality bar

The finished skill should:

- trigger for obvious and paraphrased requests
- avoid triggering on adjacent but unrelated work
- tell another agent exactly how to proceed without extra guesswork
- stay concise enough that the main `SKILL.md` is cheap to load
- remain useful outside the current repo unless the user asked for a repo-bound skill

Use `references/skill-design-checklist.md` before finalizing.

## Examples

### Example: new engineering skill

User request:
`Create a skill for handling database migration planning in this repo.`

Expected behavior:

1. Inspect the repo for migration tooling, existing schema docs, deploy steps, and nearby skills.
2. Ask targeted questions about supported databases, rollout constraints, and expected outputs.
3. Create a migration-planning skill with clear triggers, workflow steps, and validation guidance.
4. Move database-specific edge cases into `references/` if they make the main file too long.
5. Run the token audit before finalizing.

### Example: revise an overlong skill

User request:
`This skill triggers too often and is too verbose. Tighten it.`

Expected behavior:

1. Read the existing skill and identify trigger drift, repeated instructions, and bulky detail.
2. Inspect neighboring repo materials to preserve local conventions.
3. Ask only the missing questions needed to resolve scope or intended audience.
4. Rewrite the frontmatter and body so the skill is narrower and cheaper.
5. Summarize what was tightened and what moved to `references/`.

---
name: agent-skill-generator
description: Create or revise reusable agent skills from a problem statement, workflow, or existing skill folder. Use when the user asks to build a skill, design an agent skill for a repo, improve a skill's triggering or structure, validate a skill with representative prompts, audit a skill for token efficiency, or turn a repeated workflow into a portable skill package.
---

# Agent skill generator

Create skills that are generic first, portable by default, repo-bound only when the task requires it, easy to trigger correctly, and cheap to load.

## Core workflow

1. Identify the work mode and target outcome.
2. Investigate the repo or conversation history for reusable facts before asking avoidable questions.
3. Clarify only the decisions that materially change the generated skill.
4. Design the package around progressive disclosure.
5. Create or revise the skill package.
6. Validate with representative prompts when the skill is high-risk, reusable, or objectively testable.
7. Run a trigger-quality and token-optimization pass before finalizing.

Do not skip steps 2-7 unless the user explicitly narrows scope.

## Phase 1: Capture the target problem

Start by identifying one of these modes:

- `new skill`: create a skill from a rough problem or repeated workflow
- `revise skill`: improve an existing skill folder in place
- `audit skill`: inspect a skill for trigger quality, portability, and token waste before proposing edits
- `validate skill`: pressure-test an existing skill with realistic prompts before changing it
- `optimize trigger`: tighten the frontmatter description so the skill activates more reliably without over-triggering

Quick selector:

| If the user asks to... | Use mode |
|---|---|
| build a skill from an idea or repeated workflow | `new skill` |
| improve an existing skill in place | `revise skill` |
| inspect a skill for drift, bloat, or weak triggers before editing | `audit skill` |
| pressure-test a skill with realistic prompts | `validate skill` |
| narrow or strengthen the frontmatter description specifically | `optimize trigger` |

Require the user to provide at least one of:

- the problem the skill should solve
- the workflow the skill should standardize
- the existing skill folder to revise

If the user gives a vague idea, extract a provisional summary in one or two sentences before moving on.

Also capture:

- what success looks like
- whether the skill is portable or intentionally repo-bound
- whether the main risk is missing triggers, over-triggering, vague workflow, or bloat

## Non-goals

Do not use this skill for:

- moving one-line repo guardrails out of `AGENTS.md`
- writing broad repo policy that every session should always load
- documenting a one-off solution that is not reusable
- inventing heavy evaluation harnesses for simple wording edits
- copying remote skill structure or metadata into this repo when the local repo has a different contract

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
- whether AGENTS-level guidance already exists and should stay out of the skill
- whether references, scripts, or assets are warranted

Also inspect the conversation itself for concrete examples. If the user says "turn this into a skill" or is iterating on a workflow already demonstrated in chat, extract:

- the steps they actually followed
- corrections they made
- failure cases they cared about
- inputs, outputs, and artifacts already visible

If the repo is thin or unrelated, state that and proceed with a generic skill design.

## Phase 3: Clarification gate

Do not generate the skill until the spec is decision-complete.

Ask only questions that materially affect the generated skill. Prefer concise, direct questions. Push until these are clear:

- primary outcome and success criteria
- who will use the skill and in what environment
- clear trigger phrases and adjacent phrases that should not trigger it
- whether the description should optimize for broader recall or tighter precision
- whether the skill creates, revises, audits, or all three
- required workflow steps and their order
- required inputs and expected outputs
- dependencies on repo files, scripts, tools, MCP servers, or external services
- whether the skill should ship only `SKILL.md` or also `references/`, `scripts/`, or `assets/`
- validation expectations, examples, and negative cases

If a choice remains open and the user does not care, pick a sensible default and record it as an explicit assumption in the final skill package.

## Phase 3.5: Done criteria

Know what counts as complete before you edit.

- `new skill`: the package is created, the trigger surface is clear, the workflow is actionable, and validation risk is addressed
- `revise skill`: the intended problems are fixed, the repo conventions are preserved, and the delta is summarized
- `audit skill`: the findings are explicit, prioritized, and actionable, even if no edits are made
- `validate skill`: representative positive and negative prompts were reviewed, outcomes were summarized, and residual risk is stated
- `optimize trigger`: the description is tighter, easier to match, checked against adjacent negatives, and no longer carries workflow detail

## Phase 4: Create or revise the skill

Create a skill folder with the minimum set of files that makes the workflow repeatable.

Default package:

- `SKILL.md`
- `references/` only when details would otherwise bloat `SKILL.md`
- `scripts/` only when deterministic execution or validation is meaningfully better than prose
- `assets/` only when the skill depends on templates, icons, or other bundled artifacts

By default, keep the skill generic and portable. Do not add product-specific metadata files unless the user explicitly requests them.

Use progressive disclosure deliberately:

- keep the trigger-bearing metadata and core workflow in `SKILL.md`
- move large catalogs, API details, schemas, and variant-specific guidance into `references/`
- put fragile or repetitive execution in `scripts/`
- keep output resources in `assets/`

Do not duplicate the same guidance across `SKILL.md` and references.

### Writing rules for `SKILL.md`

- Use only `name` and `description` in YAML frontmatter
- Make `name` kebab-case
- Make `description` optimize activation, not teach the workflow
- Make `description` state the job and when to use it in the language a user or agent would actually say
- Optimize the description for searchability: include words the user or agent would actually say, likely file names, and adjacent synonyms when they matter
- Keep workflow details out of the description; if the description summarizes the process, another agent may follow the shortcut and skip the body
- Keep the body procedural and imperative
- Put core workflow in the main file and move bulky detail into `references/`
- Link every reference file directly from `SKILL.md`
- Keep examples short and representative

Keep AGENTS-level policy out of the skill unless it is truly task-specific. Put always-loaded repo guardrails in `AGENTS.md`; use skills for on-demand workflows, domain knowledge, templates, or deeper procedures.

When in doubt between `AGENTS.md` and a skill:

- put always-on policy, repo-wide guardrails, and universal defaults in `AGENTS.md`
- put task-specific workflows, heavy references, examples, and reusable execution logic in the skill

Example split:

- `AGENTS.md`: `Use repo-local path helpers instead of hardcoded temp paths.`
- skill: the multi-step release workflow, linked validation commands, and packaging edge cases

Negative split examples:

- keep `Always run targeted repo searches before asking naming questions.` in `AGENTS.md` if that is a universal repo rule
- do not create a dedicated skill just to say `Prefer kebab-case folder names`

### Recommended body shape

Use this structure unless the target skill needs a sharper format:

1. Title and one-line stance
2. Core workflow
3. Important constraints or decision rules
4. Resource map for bundled references/scripts/assets
5. A small number of concrete examples

## Phase 5: Validation pass

Validate before finalizing whenever the skill is reusable, high-risk, or easy to test objectively.

Minimum standard:

- run 2-3 representative positive prompts
- run at least one negative or adjacent prompt
- note whether the failures came from trigger wording, workflow ambiguity, or missing resources

Decision rule:

- skip validation only for edits that do not change trigger surface, scope, or workflow meaning
- use lightweight prompt simulation for description edits, scope changes, or body rewrites
- use before/after comparison when revising an existing skill with known trigger or behavior problems
- use heavier comparative evaluation only when the user explicitly wants proof or the skill's value is otherwise hard to judge

For the detailed prompt-writing and review workflow, use [references/skill-validation.md](references/skill-validation.md).

## Phase 6: Token optimization pass

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
5. Trim examples and trigger phrases until they are specific but not repetitive.

If you slim the package, preserve behavior. The goal is lower token cost without losing trigger quality or execution reliability.

Use `references/token-optimization.md` as the final audit checklist.

## Quality bar

The finished skill should:

- trigger for obvious and paraphrased requests
- avoid triggering on adjacent but unrelated work
- tell another agent exactly how to proceed without extra guesswork
- stay concise enough that the main `SKILL.md` is cheap to load
- remain useful outside the current repo unless the user asked for a repo-bound skill
- separate always-loaded policy from on-demand skill content
- include enough validation thinking that trigger bugs or workflow gaps are visible before shipping

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

### Example: validate a skill before shipping

User request:
`Pressure-test this skill before we publish it.`

Expected behavior:

1. Read the skill and identify its claimed trigger surface.
2. Write 2-3 realistic positive prompts and at least one negative prompt.
3. Simulate or benchmark the skill against those prompts.
4. Tighten the description or body where the validation exposed gaps.
5. Summarize the remaining risks if full evaluation was not practical.

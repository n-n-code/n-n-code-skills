# n-n-code-skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Storage for reusable agent skills.

This repository keeps skill definitions in a simple folder-based layout so they can be reviewed, revised, and reused without extra tooling. The current contents live under `.agents/skills/`.

## Repository Layout

```text
.agents/
  skills/
    <skill-name>/
      SKILL.md
```

`SKILL.md` is the required file for each skill. A skill folder may also include supporting files such as templates, references, scripts, or assets when the skill needs them.

## Skill Roles

This repo uses a small role vocabulary to keep overlapping skills understandable:

- **Principle skill** — portable, unconditional engineering guidance for a language or discipline.
- **Baseline overlay** — the thin default overlay for routine work in a domain.
- **Canonical overlay** — the stronger overlay for the same domain when the task is more demanding; it should subsume the baseline's core expectations rather than drift into a separate job.
- **Template overlay** — a pattern for repo-local adaptation rather than the default skill to load directly in this repo.
- **Process overlay** — workflow or enforcement guidance that composes with implementation skills.
- **System skill** — a build/create/install skill that leaves behind a repo-owned system rather than only guiding day-to-day execution.

When several skills touch the same job, the docs should name the baseline default and the canonical stronger option explicitly.

## Current Skills

The repository currently contains these skills:

### Skill Authoring And Documentation

- `agent-skill-generator` — create or revise reusable agent skills from a problem statement, workflow, or existing skill folder
- `agents-md-generator` — create or revise repository `AGENTS.md` files from repo inspection and existing docs
- `documenter` — documentation guidance for README files, API docs, code comments, release docs, and AI-friendly project docs

### Principle Skills

- `coding-guidance-cpp` — portable C++ implementation and review guidance for feature work, bug fixes, refactors, and code review

### Overlay Skills

- `backend-guidance` — overlay for backend and server-side networked code such as HTTP handlers, gRPC services, and message consumers
- `development-contract-repo-overlay-template` — template for the thin repo-local overlay a target repository should have after adopting the development-contract system
- `project-config-and-tests` — overlay for config contracts, defaults, path helpers, and deterministic test coverage
- `project-core-dev` — overlay for day-to-day feature work and bug fixes in repo-owned code
- `project-platform-diagnose` — overlay for environment-sensitive diagnosis such as startup issues, install problems, and runtime smoke checks
- `project-release-maintainer` — overlay for release-facing docs, install layout, workflows, licenses, and hygiene scripts
- `project-vendor-boundary` — overlay for app-owned versus vendored dependency boundaries
- `ui-guidance` — thin baseline overlay for ordinary graphical UI and frontend work
- `ui-design-guidance` — canonical strong UI overlay for redesigns, frontend polish, and UX-heavy UI work; extends the baseline with design-direction and UX-priority guidance

UI overlay guidance:

- Start with `ui-guidance` for ordinary UI changes that mostly need repo-native consistency and basic UI hygiene.
- Prefer `ui-design-guidance` when the task needs stronger design direction, more frontend polish, or explicit UX review across accessibility, interaction, layout, forms, navigation, or data display.

### Process And Workflow Skills

- `development-contract-process` — portable process overlay for repos that require tracked change contracts, verifier evidence, and smallest-proof validation
- `development-contract-system` — build a portable change-contract workflow with tracked feature records and lifecycle helpers
- `dream-thinking` — reflective sleep-and-dream heuristic for learning from recent work
- `fuse-skills` — combine multiple skills into one fused skill without duplicated guidance or lost capability
- `recursive-thinking` — recursive self-questioning to stress-test plans, diagnoses, designs, and recommendations
- `security` — security guidance for threat modeling, secure defaults, and security-focused code review
- `thinking` — planning and design guidance for quick-to-medium structured problem solving

## Adding a Skill

1. Create a new folder under `.agents/skills/<skill-name>/`.
2. Add a `SKILL.md` file that states the skill name, when it should be used, and the workflow it expects.
3. Add only the supporting files the skill actually needs.
4. Keep examples and instructions aligned with the files that exist in the folder.

## Editing Guidelines

- Keep skill descriptions concise and operational.
- Prefer repository-grounded instructions over generic advice.
- Keep the skill taxonomy honest: thinking skills change reasoning mode, overlays add domain or process rules, and generator/system skills should say when they produce repo-local overlays.
- Use the role vocabulary consistently: baseline, canonical, template, process, and system should mean the same thing everywhere in the repo.
- Avoid near-duplicate skill families. If several skills cover the same job, document the canonical default and keep specialized variants sharply scoped.
- Preserve stable folder names once a skill is published or referenced elsewhere.
- Avoid adding tooling, build, or install steps unless the repository actually needs them.

## Validation

This repository does not currently have a build or test pipeline. Validation is structural:

- every skill lives under `.agents/skills/`
- every skill has a `SKILL.md`
- documentation claims match the repository contents

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).

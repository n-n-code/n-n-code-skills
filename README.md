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
- `project-config-and-tests` — overlay for config contracts, defaults, path helpers, and deterministic test coverage
- `project-core-dev` — overlay for day-to-day feature work and bug fixes in repo-owned code
- `project-platform-diagnose` — overlay for environment-sensitive diagnosis such as startup issues, install problems, and runtime smoke checks
- `project-release-maintainer` — overlay for release-facing docs, install layout, workflows, licenses, and hygiene scripts
- `project-vendor-boundary` — overlay for app-owned versus vendored dependency boundaries
- `ui-guidance` — overlay for graphical UI and web frontend code

### Workflow Skills

- `development-contract-system` — build a portable change-contract workflow with tracked feature records and lifecycle helpers
- `dream-thinking` — reflective sleep-and-dream heuristic for learning from recent work
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
- Preserve stable folder names once a skill is published or referenced elsewhere.
- Avoid adding tooling, build, or install steps unless the repository actually needs them.

## Validation

This repository does not currently have a build or test pipeline. Validation is structural:

- every skill lives under `.agents/skills/`
- every skill has a `SKILL.md`
- documentation claims match the repository contents

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).

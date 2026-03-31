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

- `agent-skill-generator`
- `agents-md-generator`
- `coder`
- `documenter`
- `project-config-and-tests`
- `project-core-dev`
- `project-platform-diagnose`
- `project-release-maintainer`
- `project-vendor-boundary`
- `security`
- `thinking`

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

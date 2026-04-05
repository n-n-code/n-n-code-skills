# Fusion notes

Second-pass fusion record for the local `agent-skill-generator`.

## Sources reviewed

- local base: `.agents/skills/agent-skill-generator/SKILL.md`
- local fusion rules: `.agents/skills/fuse-skills/SKILL.md`
- remote package: `anthropics/skills` -> `skill-creator`
- remote package: `anthropics/skills` -> `template-skill`
- remote package: `anthropics/claude-code` -> `Skill Development`
- remote package: `vercel/next.js` -> `authoring-skills`
- remote package: `github/awesome-copilot` -> `microsoft-skill-creator`
- remote package: `obra/superpowers` -> `writing-skills`
- remote package: `starchild-ai-agent/official-skills` -> `skill-creator`
- remote page only: `vercel-labs/agent-browser/skill-creator`

## Compatibility stance

These sources were compatible enough to fuse because they all addressed skill authoring or skill validation at the meta-skill level. The main differences were:

- some were portable and generic
- some were plugin- or platform-specific
- some emphasized validation heavily
- some carried extra metadata conventions not suitable for this repo

Local repo conventions won whenever a remote source conflicted with them.

## Compact matrix

| Source | Keep | Merge | Drop | Reason |
|--------|------|-------|------|--------|
| local base | core workflow, portability stance, token focus | yes | no | canonical local starting point |
| fuse-skills | explicit fusion discipline | yes | no | governs how the merge should behave |
| anthropics skill-creator | progressive disclosure, test/iterate mindset, stronger trigger thinking | yes | yes | high-value meta guidance |
| anthropics template-skill | no substantive content | no | yes | placeholder only |
| claude-code Skill Development | progressive disclosure and trigger examples | yes | yes | useful ideas, but plugin-specific structure dropped |
| next.js authoring-skills | AGENTS.md vs skill boundary | yes | yes | valuable repo-policy split, unsupported frontmatter dropped |
| microsoft-skill-creator | research-first stance and local-vs-dynamic content split | yes | yes | Learn MCP specifics dropped as out of scope |
| obra writing-skills | negative prompts, failure-first validation thinking, description discipline | yes | yes | superpowers-specific dependencies dropped |
| starchild skill-creator | degrees-of-freedom framing, lean-body emphasis | yes | yes | platform metadata and refresh flow dropped |
| vercel-labs agent-browser page | concise-is-key and init/package structure ideas | yes | yes | not treated as installed local source |

## Second-pass changes

The second pass made these adjustments:

- moved detailed validation workflow into `references/skill-validation.md`
- made the frontmatter rule sharper: descriptions should optimize activation, not summarize workflow
- added a concrete `AGENTS.md` vs skill split example
- preserved this compact fusion record so later revisions can see what was kept, merged, or dropped

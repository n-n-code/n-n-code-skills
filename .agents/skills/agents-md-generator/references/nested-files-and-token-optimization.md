# Nested files and token optimization

Use this when deciding whether the repo needs more than a root `AGENTS.md`, and when tightening the final output.

## Recommend nested AGENTS.md only when needed

A nested file is justified when a directory has rules that materially differ from the repo root, such as:

- a different build or test workflow
- special review or ownership rules
- vendor or generated-code boundaries
- deployment or migration safety constraints
- a separate app or service with its own operational commands

If the subtree only needs a few extra examples, keep them out of `AGENTS.md` unless they are critical.

## Root vs nested split

Keep in the root file:

- rules that apply to most of the repo
- shared setup/build/test/lint commands
- global safety constraints
- links to deeper docs

Put in a nested file:

- subtree-specific commands
- local hazards or forbidden edits
- local ownership or review expectations
- toolchain differences that would confuse an agent at the root level

## Token optimization

- Prefer crisp rules over explanatory paragraphs.
- Delete duplicate instructions before rewriting.
- Avoid long background sections about how agents work.
- Keep only the commands and constraints that change behavior.
- Link to existing docs instead of reproducing them.
- Do not make the root file a full contributor handbook.

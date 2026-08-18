# Nested files, host adapters, and token optimization

Use this after repository inspection when subtrees differ materially, multiple instruction entry points exist, or the draft remains long or repetitive.

## Confirm instruction semantics

- Identify the coding-agent hosts the repository actually targets.
- Verify whether each host loads root `AGENTS.md`, nested `AGENTS.md`, or a tool-specific file, and how nearer files interact with parent instructions.
- Do not claim inheritance, override, or pointer-following behavior without evidence for the named host.
- If nested behavior is unknown or unsupported, keep one root file and use explicitly scoped subsections.
- Keep a tool-specific entry point as a thin adapter when a host requires it. A pointer is sufficient only when that host reliably follows it.

## Decide whether nesting is justified

Recommend a nested file only when a directory has a durable material difference, such as:

- a distinct build, test, validation, or release workflow
- local ownership or review requirements
- generated or vendored code boundaries
- deployment, migration, credential, or data-safety constraints
- a separate app or service with different operational commands

Do not add a nested file solely for examples, length reduction, speculative future needs, or guidance that belongs in ordinary contributor documentation.

## Split root and local responsibilities

Keep in the root file:

- rules that apply to most of the repository
- shared setup and validation guidance
- global safety constraints
- the repository-wide relationship between instruction files

Put in a nested file:

- subtree-specific commands and exceptions
- local hazards or forbidden edits
- local ownership or review rules
- toolchain differences that would mislead an agent using only the root

Write nested files as local deltas rather than copies of the root. Do not move a global safety rule exclusively into a nested file. State exceptions explicitly instead of relying on ambiguous contradiction.

## Optimize context cost

1. Delete duplicate and generic guidance.
2. Replace explanatory prose with scoped, conditional rules when meaning is preserved.
3. Keep only commands and constraints that change agent behavior.
4. Move background and contributor education to maintained repository docs and link them.
5. Keep temporary assumptions, audit evidence, and point-in-time validation results in the handoff.

After trimming, re-check that every local rule still appears at the correct scope and that the root remains sufficient for agents working outside nested directories.

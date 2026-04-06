---
name: documenter
description: "Baseline overlay for substantial documentation authoring or restructuring: README, specs, ADRs, tutorials, how-to guides, reference docs, explanations, API docs, code comments, changelogs, and agent-facing docs. Use when the agent should classify doc type, ground claims in repo truth, and validate examples before finishing."
---

# Documenter

Documentation workflow for repo docs, technical writing, and inline API comments.

## Priorities

- keep docs accurate, scannable, and current
- identify audience, document type, and source of truth before drafting
- prefer examples and concrete structures over vague prose
- match README/docs to actual build, test, install, and release behavior
- keep public API comments complete enough for generated docs
- keep one document one job; link to neighboring docs instead of mixing modes

## Not For

- binary document manipulation such as `.docx`, `.pdf`, `.pptx`, or `.xlsx`
- regulatory document-control systems, compliance programs, or quality records
- repo-specific doc-site pipelines unless the repo already contains them
- intensive coauthoring sessions for large specs or proposals
  use `documenter-coauthoring` for that mode

## Core Workflow

1. Classify the request before writing:
   - audience: user, contributor, maintainer, reviewer, or agent
   - document type: README, spec, ADR, tutorial, how-to, reference, explanation,
     API doc, code comment, changelog, release note
   - output target: existing file, new file, or inline content
2. Read the current doc plus local source of truth in code, config, build
   scripts, tests, release files, and existing repo guidance.
3. Pick the structure that fits the job:
   - small edit: update only affected sections
   - large or new doc: outline first, then draft section by section
4. Draft in compact Markdown with active voice, present tense, and direct
   wording. Explain before code when the reader needs context.
5. Validate every claim you can:
   - run or inspect commands and examples when feasible
   - check links, paths, identifiers, and filenames
   - if examples cannot be validated, say so instead of implying they were
     checked
6. Tighten before finishing: remove duplication, filler, and mixed-purpose
   sections. Cross-link instead of repeating background.

## Bundled Reference

Load [references/doc-templates.md](references/doc-templates.md) when the task
needs a compact starting structure for README sections, ADRs, endpoint docs,
public API comments, or changelog entries.
## Document Type Rules

Use Diataxis when the request is general documentation rather than a repo
convention with its own fixed format.

- tutorial: for first-time learning by doing; every step should produce a
  visible result
- how-to: for solving one known task; assume baseline knowledge and skip theory
- reference: for facts, options, endpoints, flags, or API contracts; optimize
  for fast lookup
- explanation: for trade-offs, concepts, rationale, and "why"

Keep each document a single dominant type. Link to related docs instead of
mixing tutorial steps, reference tables, and conceptual background in one page.

## README And Project Docs Rules

- answer what it is, how to build it, how to test it, and how to release it
- keep quick start runnable in minutes
- keep top-level structure compact: title, one-line purpose, quick start, key
  commands, important constraints
- avoid stale feature claims and aspirational behavior presented as shipped
- use tables for config, support matrices, or command summaries when they make
  scanning faster

## Specs, ADRs, And Change Docs Rules

- specs and proposals should state audience, problem, constraints, decision, and
  open questions
- ADRs should separate context, decision, and consequences
- changelogs and release notes should emphasize user-visible changes, breaking
  changes, and upgrade action
- if a decision depends on local politics or history, state the consequence
  plainly instead of hinting at it

## Code Comment Rules

- comment why, contracts, and non-obvious behavior
- do not narrate obvious statements line by line
- keep public API comments complete enough for Doxygen/docs generation
- include params, return values, errors, and examples when the API surface needs
  them
- do not invent API behavior that code does not implement

## Documentation Hygiene Rules

- put durable documentation where the repo already expects it; do not force a
  generic `docs/` layout onto repos that use a different structure
- make docs discoverable: link new durable docs from the nearest index, README,
  sidebar, or parent doc when the repo has one
- prefer contextual links over vague text such as "click here"
- use relative links for repo-local docs unless the repo clearly prefers another
  pattern
- keep time-sensitive status, progress snapshots, and point-in-time test output
  out of durable docs unless the file is explicitly meant to record history, as
  in changelogs or ADRs
- when writing docs ahead of implementation, mark planned interfaces clearly and
  replace placeholders with real behavior once the code exists

## Style Rules

- prefer simple, concrete words: `use`, `add`, `run`, `because`
- prefer active voice; passive is acceptable when the actor is irrelevant
- keep paragraphs short; split when a reader would need to re-parse the sentence
- use direct address in tutorials and how-to guides; use neutral voice in
  references
- avoid throat-clearing such as "this section describes" unless it adds meaning

## Validation Rules

- examples should be runnable, inspectable, or clearly marked illustrative
- if public headers or external APIs change, update API comments immediately
- keep checklists actionable
- keep agent-facing docs aligned with repo guidance and local skills
- for AI-facing docs, prefer clear heading hierarchy, self-contained sections,
  and direct file/path references

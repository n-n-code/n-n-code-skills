---
name: documenter-coauthoring
description: Companion overlay for multi-round collaborative drafting of large specs, proposals, decision docs, and similar documents. Use when the workflow needs structured context gathering, explicit outline approval, section-by-section iteration, and reader-testing rather than a direct documentation pass.
---

# Documenter Coauthoring

Structured coauthoring workflow for large docs. Pair this with `documenter`
when the task needs sustained collaboration instead of a direct draft/update.

## Core Workflow

1. Gather context efficiently:
   - ask for audience, desired outcome, constraints, deadline, and template
   - invite a raw context dump; do not force the user to pre-organize it
   - read linked local files and existing docs before asking avoidable questions
2. Propose a structure before drafting the full doc when scope is still fuzzy
   or the document is large.
3. Draft the sections with the most uncertainty first. Summary sections usually
   come last.
4. Refine with surgical edits instead of reprinting the whole document on every
   iteration.
5. Before finishing, do a reader test:
   - check whether a reader without hidden context can follow the decision,
     procedure, or reference entry
   - look for missing assumptions, undefined terms, and filler that adds little
     value

## Decision Rules

- prefer this skill only for substantial docs; small edits should stay with
  `documenter` alone
- defer baseline doc-type, hygiene, style, and validation rules to
  `documenter`; this skill adds collaboration workflow
- when a template exists, align to it early instead of drafting against a
  guessed structure
- ask for approval on the outline when the document shape materially affects the
  content
- keep summary sections until late, after the decision and evidence are clear
- capture user preference from feedback and apply it to later sections

## Exit Criteria

- the full document has a coherent structure
- section order matches reader needs
- important assumptions are stated explicitly
- repeated or low-value text has been removed
- a fresh reader can follow the document without hidden context

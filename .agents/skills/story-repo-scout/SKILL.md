---
name: story-repo-scout
description: Repo scouting workflow for using a story card, ticket, or acceptance criteria to scour the current repository, find relevant files and file paths, and append compact implementation context. Use before coding when a story needs repo context; avoid for story drafting, broad architecture review, security review, or implementation.
---

# Story Repo Scout

Use a story card to find the repo files most likely to matter before
implementation starts. Favor evidence, exact paths, and small output.

## When To Use

- append repo context to a generated story card or implementation ticket
- find likely implementation, test, config, migration, or docs files before coding
- give a human or implementation agent a better starting point for a story
- run a lightweight repo scout when the model is smaller or context is limited

## Not For

- drafting or clarifying the story itself; use `user-story-clarifier`
- implementing code after the relevant context is already clear
- broad architecture review, dependency mapping, or whole-repo documentation
- security review or threat modeling; use `security`

## Core Workflow

1. Read the story card first. If the story is too vague to search, use
   `user-story-clarifier` or ask for the missing behavior before scouting.
2. Extract 3-7 search handles:
   - domain nouns, actors, entities, commands, routes, UI labels, errors, config
     names, data fields, and acceptance-criteria verbs
   - avoid generic terms such as `user`, `data`, `page`, `service`, and `feature`
     unless paired with a specific qualifier
3. Map the repo cheaply:
   - list files with `rg --files` when available
   - inspect root docs, manifests, package files, route/config directories, and
     test directories only enough to orient the search
   - note documented commands, domain glossaries, ADRs, or context docs when
     they explain the story terms
4. Identify workspace boundary. If the repo has `packages/`, `apps/`,
   `services/`, `crates/`, or workspace manifests (`pnpm-workspace.yaml`,
   `lerna.json`, `turbo.json`, `nx.json`, `go.work`, Cargo workspaces, Bazel
   `WORKSPACE`/`MODULE.bazel`), restrict the search to the workspace implied by
   the story. Record the workspace in `Repo Context`. If the story spans
   multiple workspaces, name them and search each separately.
5. Search in passes:
   - exact handles from the story
   - obvious filename/path variants
   - nearby synonyms only if exact searches miss
   - recent git history for files changed near the story domain when exact
     searches miss
   - tests, docs, configs, migrations, fixtures, and generated examples last
6. Open candidate files before including them. When a test file names the
   behavior or acceptance criterion directly, treat it as an anchor — use it to
   find the implementation file it exercises. Record the observed evidence:
   symbol, route, test name, docs phrase, config key, or nearby behavior. Do not
   include a file based only on a filename guess.
7. Rank by implementation value:
   - entry points and handlers
   - behavior owners and domain services
   - data models, schemas, migrations, and config
   - tests, fixtures, and validation commands
   - docs that explain current behavior
8. Compare story language with repo language. If terms conflict with code or
   docs, add an open repo question instead of silently renaming concepts.
9. Mark likely unrelated or do-not-touch files when the search finds tempting
   nearby paths that should not shape the implementation.
10. Keep the result compact. Default cap by target executor:
    - `local-small`: 6-8 paths
    - `standard-agent` / `frontier-gpt` / `human` (default): 10-12 paths
    - up to 15 only when the story explicitly spans multiple workspaces
    Mark speculative or weak matches instead of overstating certainty.
    If no strong hits appear after all passes, report the handles tried and the
    most plausible directories to inspect next; do not invent paths.
11. If the story is in a file and the user asked to update it, append the repo
    context there. Otherwise output an appendable Markdown block.

## Repo Context Output

Use this structure by default:

```markdown
## Repo Context

### Workspace
- Workspace, package, or app the story targets. Omit only for single-workspace repos.

### Search Handles
- Concrete terms searched or derived from the story.

### Relevant Files
| Path | Evidence | Why It Matters | Confidence |
|---|---|---|---|
| path/to/file.ext | Route, symbol, test, docs phrase, or config key observed. | One-line rationale. | High/Medium/Low |

### Likely Entry Points
- path/to/file.ext: where implementation probably starts.

### Tests to Update
- path/to/test.ext: existing test that will need modification for this story.

### Tests and Validation Targets
- path/to/test.ext: behavior or command this may validate.

### Documented Commands
- Commands found in repo docs or manifests that may validate the story.

### Likely Unrelated / Do Not Touch
- path/to/file.ext: why it is nearby but outside this story.
- `None identified` when this output will feed
  `story-implementation-orchestrator` and no boundary was found.

### Open Repo Questions
- Only unresolved repo questions that materially affect implementation.
```

Omit empty sections when they add no signal, except keep `Likely Unrelated / Do
Not Touch` as `None identified` when a full story-to-plan packet or orchestrator
quality gate will consume the output. Prefer exact paths over prose. Include
line numbers only when (a) the symbol's location is non-obvious from the file or
(b) the implementer will need to navigate directly there. Never paste line
numbers as decoration.

Confidence uses the same High/Medium/Low scale as `user-story-clarifier` story
confidence. See
`story-implementation-orchestrator` for the canonical vocabulary block when run
end-to-end.

## Anti-Patterns

Reject and rewrite when these appear:

- **Filename-only match.** Path included because the name looks right but no
  symbol, route, or test was opened to confirm relevance.
- **README phrase, no code.** Documentation mentions the feature but no
  implementation file was found. Record as an open repo question, not as a
  relevant file.
- **Generated code.** `*.pb.go`, `*.generated.*`, `dist/`, `build/`, `target/`,
  `__generated__/`. Point to the source/schema instead.
- **Inflated confidence.** Marking a path `High` when only the filename was
  inspected. Default to `Low` when evidence is thin.

## Small-Model Rules

- Use short search handles and one search pass at a time.
- Cap output at 6-8 paths (see step 10).
- Prefer file paths and one-line rationales over summaries of code.
- Stop when the next file would be another weak guess.
- If no strong hits appear, report the handles tried and the most plausible
  directories to inspect next.

For executor-specific planning rules (token budget, first-action, stop-and-
report), see `story-implementation-planner` `local-small` profile — this skill
does not duplicate that guidance.

## Universal Rules

- Never invent files, symbols, commands, or repo structure.
- Do not paste code snippets unless the user asks.
- Do not run install, build, migration, or test commands while scouting unless
  the user explicitly asks.
- Keep evidence short and concrete; do not summarize whole files.

## Composition Boundaries

- **Pipeline position.** Input comes from `user-story-clarifier` (story card).
  Output is consumed by `story-implementation-planner`. Preserve `Likely
  Unrelated / Do Not Touch` paths verbatim — the planner relies on those
  boundaries.
- Use `user-story-clarifier` first when acceptance criteria, boundaries, or
  expected behavior are unclear.
- Use `story-implementation-planner` after this skill has appended repo context.
- Use `tester-mindset` when the main question is what risk or evidence matters,
  not where the current implementation lives.
- Use `security` for exploit-focused review or threat modeling.

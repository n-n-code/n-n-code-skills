# Documenter Trigger Evals

Use these prompts to spot over-triggering and boundary drift between
`documenter` and `documenter-coauthoring`.

## Expected `documenter`

- "Update the README install steps to match the current CLI flags."
- "Write API docs for these new endpoints."
- "Turn this rough markdown into a clear how-to guide."
- "Add missing public API comments to these headers."
- "Clean up this changelog entry and remove stale claims."

## Expected `documenter` + `documenter-coauthoring`

- "Help me co-author a design doc for the new caching layer."
- "I need to draft a proposal and want to iterate section by section."
- "Let's build this ADR together. Start by helping me shape the outline."
- "I have a lot of context for a spec. Ask questions, then help me draft it."

## Expected Neither

- "Merge these PDFs."
- "Build a docs website with MkDocs and GitHub Pages."
- "Set up a compliance document-control workflow for regulated releases."
- "Summarize this existing markdown file."

If the expected skill choice stops looking obvious, tighten frontmatter before
adding more behavior.

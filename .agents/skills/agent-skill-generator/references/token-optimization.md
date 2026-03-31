# Token optimization

Use this after the skill works. Optimize for lower context cost without reducing execution quality.

## Keep in `SKILL.md`

- the trigger-bearing frontmatter
- the core workflow
- critical decision rules
- short examples that anchor the workflow
- direct links to bundled references

## Move out of `SKILL.md`

- long domain primers
- exhaustive edge-case catalogs
- variant-specific instructions
- large examples
- detailed command references
- documentation that can be discovered from the repo when needed

## Compression rules

- Delete repeated ideas before rewriting sentences.
- Prefer short checklists over explanatory paragraphs.
- Replace generic advice with workflow-specific rules.
- Keep examples only if they teach something not already obvious from the instructions.
- Avoid motivational or narrative text.
- Prefer one sharp sentence over two soft ones.

## Smell tests

The main file is probably too large if:

- multiple sections repeat the same workflow in different words
- examples are longer than the instructions they illustrate
- reference material dominates the core procedure
- the skill explains common engineering ideas instead of repo- or workflow-specific guidance

## Final pass

Ask:

1. What text can be deleted with no loss of behavior?
2. What text belongs in `references/`?
3. What assumptions should be stated once instead of repeated?
4. Is the description still strong enough to trigger correctly after trimming?

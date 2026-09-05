# Format and validation

Use the existing document's conventions and the intended consumer's actual
contract. This reference supports a general visual DESIGN.md; it does not
prescribe an editor, framework, platform, or integration.

## Document structure

For a new document, the [DESIGN.md specification](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)
provides a useful common structure. The linked format was marked `alpha` when
consulted on 2026-09-05. Check the relevant version before a migration or new
compatibility claim; prefer a pinned local consumer contract when available.

Use the applicable `##` sections in this order when following that format:
Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components,
and Do's and Don'ts. The specification permits omissions and aliases such as
Brand & Style, Layout & Spacing, and Elevation. Preserve useful custom sections;
avoid duplicate section headings. Place interaction and accessibility guidance
beside the relevant rules, or in a focused section when that is easier to use.

## Optional structured tokens

The referenced format permits a Markdown body without frontmatter. Add YAML at
the start of the file, between `---` delimiters, when structured values serve
the document's consumer. Tokens define exact values within the document; prose
explains their use. Follow a different consumer schema when explicitly required
rather than assuming every DESIGN.md uses the same fields.

For the referenced schema:

| Area | Fields |
|---|---|
| Identity | `name`, optional `description` and `version` |
| Color | `colors` maps token names to CSS color strings; quote hex values |
| Type | `typography` maps names to `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, and optional `fontFeature`/`fontVariation` |
| Shape and space | `rounded` maps names to dimensions; `spacing` accepts dimensions or numbers |
| Components | `components` maps names to property/value maps, including `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, and `width` |
| Intentional omissions | `omitted` lists sections, optionally with reasons |

Use the consumer's exact property names and supported units. Quote references
such as `"{colors.primary}"` and resolve them to defined values; verify support
before referencing a composite token. Preserve native units and theme semantics
in prose if a chosen token schema cannot represent them faithfully. Do not
invent standard fields for themes, breakpoints, or motion, or assume accepted
extensions survive an export.

Use intentional omissions only for deliberate exclusions, not missing research.
Keep known facts, proposals, and unresolved values distinguishable. If a required
token remains unknown, report the document as incomplete for that consumer and
do not replace a valid artifact with a misleading export-ready version.

## Validation

Check local links and identifiers, duplicate headings, token references, units,
themes/states, and agreement between prose and structured values. Compare
meaningful before/after decisions during updates; a syntax check will not detect
lost rationale or an unintended change of direction.

Use an existing project or consumer validator after inspecting its command,
version, and side effects. Do not install tooling or change configuration just
to complete a documentation check. If unavailable, perform static checks and
state which execution was skipped. Inspect warnings even after a successful
exit status; successful export does not establish document validity.

Parser checks, selected contrast checks, rendered review, accessibility testing,
and actual consumer use establish different things. Report the evidence obtained
without treating one as proof of the others. Keep the artifact useful through
clear rules and a representative reader walkthrough, even when tooling is absent.

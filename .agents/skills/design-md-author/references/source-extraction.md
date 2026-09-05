# Extract design context from implementation sources

<!-- Modified adaptation; see ../ATTRIBUTION.md for source credits and license. -->

Use this when documenting an existing interface from code or resource files.
The approach applies across web, mobile, and desktop projects.

## Discover the actual system

Read the owning product's manifests, entry points, resource references, and
configuration to locate its styling system. Follow the files it actually loads:
tokens, theme resources, shared components, style definitions, layout resources,
fonts, and assets. Inspect project overrides and their scope before relying on
library or platform defaults. Exclude unrelated apps and generated/vendor trees
unless they are needed to resolve a specific dependency.

Read configuration as data. Do not execute modules, install dependencies, run
preprocessors, or repair a build merely to extract design context. Leave values
that require unavailable runtime information unresolved.

Start with shared definitions and the application shell, then sample common
controls, navigation, content containers, forms, and a domain-specific component.
Expand the sample for conflicting variants, themes, or layout conditions. A
single polished screen does not establish the whole product's design system.

## Trace definitions to use

For each significant finding, identify its source, declared value, semantic role,
conditions, and evidence status. Resolve aliases and references through the
active theme, shared styles, component overrides, and property bindings. Account
for precedence, inheritance, scoping, and runtime selection in that system.

Preserve light/dark modes, interaction states, responsive rules, platform
variants, and accessibility settings. Do not flatten conditional values into
one palette or claim a computed result when only declarations were inspected.
Retain native units, relative values, and scaling behavior; convert only with a
verified basis and identify any approximation.

Normalize equivalent representations for analysis while preserving public
identifiers and semantic aliases. Similar values are not necessarily equivalent:
`#333` and `#2c2c2c` may represent distinct states. Record inconsistency and propose
consolidation separately unless an accepted decision establishes the new rule.

## Synthesize useful rules

| Area | Evidence to connect |
|---|---|
| Visual direction | Surfaces, whitespace, density, imagery and emphasis; support descriptive language with concrete choices |
| Color and themes | Surface, text, interactive, border and feedback roles; foreground/background pairings and theme conditions |
| Typography | Font availability/fallbacks, hierarchy, size, weight, tracking, line height and actual component usage |
| Components and states | Variants, shape, padding, borders, elevation, images, focus, feedback and motion |
| Layout and input | Content widths, grouping, spacing, alignment, size/orientation changes, navigation and keyboard/touch behavior |

Use comments and decision records to explain intent only when they remain
consistent with accepted direction and current scope. Keep descriptive language,
exact values, and implementation identifiers together. Report inspected areas
and material gaps; source inspection alone does not verify rendered fidelity or
accessibility. Return to the main workflow to write or update the document.

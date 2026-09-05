# Read an implementation as design evidence

Use this reference to identify the rules an interface actually uses. The output
is a scoped set of findings for document authoring; a successful build is not a
prerequisite.

## Find the files that control the selected product

Follow manifests, entry points, imports, resource registrations, and theme
selection to the definitions loaded by this application. Locate shared styles,
tokens, components, layout resources, fonts, and image assets. Account for
product overrides before relying on framework defaults.

Start with the shell and shared definitions, then inspect a representative
control, navigation pattern, content region, form, and product-specific
component. Add samples when modes, themes, or exceptions could change a rule.
Do not generalize the whole system from its best-looking screen.

Inspect configuration as data. Avoid running modules, preprocessors, installers,
or a build repair merely to discover values. Follow generated or third-party
resources only as far as needed to resolve an actual dependency. Mark values
selected by unavailable runtime state as unresolved.

## Follow a value through its conditions

For a finding that matters to the document, establish:

1. the defining file and identifier;
2. the alias, inheritance, or override path to the component;
3. the theme, state, size, or platform that selects it;
4. whether the result is a declaration, a rendered observation, or an estimate.

Keep those distinctions when summarizing. A declared foreground color is not
the final composited pixel; a platform default is not proof of a local choice.
Check scoping, precedence, bindings, media rules, and active configuration
before describing an effective value.

Keep logical units, relative dimensions, scalable typography, and theme variants.
Convert only with an evidenced basis. Normalize notation for comparison without
merging semantic identities: two tokens may resolve to the same color and still
serve different roles. Similar values can also encode intentional states.
Carry material distinctions into the document: explain both aliases with equal
values and separate tokens whose values merely look alike. If their use sites
are unknown, say so while keeping their identities distinct; do not imply that
they are interchangeable or invent a role to justify the difference.

## Turn findings into applicable rules

Organize findings by the decisions they support rather than by file order:

- where emphasis comes from: hierarchy, surfaces, whitespace, imagery, density;
- which foreground/background roles belong together in each theme;
- how text roles and fonts behave, including fallback and scaling;
- how layout changes with size, orientation, and input;
- which component variants and interaction states are maintained.

Use comments or decision records for intent only when they apply to the current
product and version. Keep contradictory evidence visible and propose any
consolidation separately from describing the present system.

Pass the inspected scope, useful rules, source handles, exceptions, and gaps
back to the main authoring workflow. Source inspection can support an accurate
description of declarations; rendered fidelity, keyboard behavior, and
accessibility require their own observations.

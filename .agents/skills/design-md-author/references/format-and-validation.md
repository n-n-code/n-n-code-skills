# Choose and check the document format

A visual design reference can be plain Markdown. Select its structure by what
the reader and any consuming tool need; its filename alone does not establish
a schema.

## Existing documents and new documents

On an update, retain useful custom sections, heading names, token identifiers,
and theme conventions. Change a format only for an authorized migration or an
evidenced consumer need. Preserve decision rationale during reorganization.

For a new document without a required format, the local scaffold groups design
choices with their usage, sources, and conditions. Omit irrelevant groups and
use prose instead of a table when the relationships are easier to explain that
way. Check that a representative screen can be understood from the result.

## Consumer compatibility

When a tool explicitly consumes the Google Labs DESIGN.md format, consult its
[specification](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)
and the consumer's supported version. The specification inspected on 2026-09-05
was labeled `alpha`; this link is an interoperability reference, not a required
authoring dependency. Confirm the current contract before claiming compatibility.

That format permits a Markdown body without YAML. If using its heading
conventions, arrange applicable sections as Overview, Colors, Typography, Layout,
Elevation & Depth, Shapes, Components, and Do's and Don'ts. Check supported
aliases and omissions against the selected version. Other consumers may expect
a different organization; preserve their actual contract.

Use optional frontmatter only when structured values help the consumer.
For the inspected schema, check these distinctions:

- `colors` maps identifiers to CSS color strings; quote hex literals.
- `typography` groups font properties such as `fontFamily`, `fontSize`,
  `fontWeight`, `lineHeight`, and `letterSpacing`. Validate optional
  `fontFeature` and `fontVariation` support.
- `rounded` and `spacing` encode dimensions, with numbers also accepted by
  `spacing`. Preserve the consumer's units and representation.
- `components` associates names with supported property/value maps.
- `name` identifies the design; `description` and `version` are optional.
- `omitted` expresses a deliberate exclusion, optionally with a reason;
  it is not a substitute for missing evidence.

Resolve references such as `"{colors.accent}"` to an existing token. Check
whether the consumer supports a composite reference or any proposed extension.
Do not invent standard fields for themes, breakpoints, or motion; describe
conditions in prose when the schema cannot represent them faithfully.

Keep unapproved choices out of normative tokens unless the artifact is clearly
a proposal. If a required value is unknown, identify incomplete compatibility
instead of fabricating a value or replacing a valid document with a misleading
export-ready one.

## Checks and evidence limits

Inspect local links, heading uniqueness, identifiers, units, aliases, supported
states, and agreement between prose and structured data. Trace an update's
before/after decisions; syntactically valid output can still lose intent.

Use an existing project or consumer validator after checking its version and
side effects. Read warnings as well as the exit code. Do not install a validator
or change application configuration merely to complete a document check.
When execution is unavailable, perform static checks and say what remains
unverified.

A parser verifies syntax; a consumer exercise verifies only the exercised
interface; source inspection verifies declarations. Contrast measurements,
rendered inspection, keyboard use, and assistive-technology testing answer
different questions. State the evidence obtained without turning one passed
check into a claim of complete accessibility or design fidelity.

# Page design and themes

Read this for page structure, visual changes, theme customization, asset
processing, or conversion of static HTML into Jekyll source.

## Translate purpose into page structure

1. Identify the audience, page purpose, important content, and primary action.
   Use established design choices and nearby pages as evidence. Clarify only
   material gaps; avoid an interview for facts already in the project.
2. Choose the information order and content model before styling. Map each
   region to page content, a layout, an include, or data only where that
   distinction improves maintenance. Avoid extracting every small element.
3. In preserve mode, reuse existing tokens, typography, spacing, components,
   and breakpoints. For an explicitly requested redesign or a new site, define
   a coherent hierarchy and visual direction suited to the content.
4. Implement with semantic HTML, CSS, and the site's existing Jekyll structure.
   Use client-side JavaScript only for interactions that require it. A static
   build does not itself provide a form backend, authentication service, or
   runtime database; identify such a gap only if the requested behavior needs it.

For a design-only response, explain the proposed regions, reusable pieces,
content fields, styles, URLs, and verification approach at the task's scale.
Do not create a design document or change code solely to explain that proposal.

## Reuse layouts and make focused overrides

Inspect the selected layout and its parents, the include chain, stylesheet
entry points, and relevant data before editing. Trace one actual page rather
than assuming conventional names such as `default` or `page` exist.

For a gem theme, locate the installed version with the project's Bundler setup,
for example `bundle info --path <theme-gem>`, and inspect its files. For a remote
theme, identify the configured source/ref and inspect available matching
sources. If unavailable, state the missing evidence rather than inventing an
override target. Follow the theme's documented configuration or style extension
point when it solves the request.

When a file override is necessary, create only the matching file in the site's
source, such as the corresponding layout or include. Local files take
precedence over theme files. Keep installed gems and downloaded theme caches
unchanged. An overridden file will not automatically receive later upstream
changes; avoid copying the entire theme to change one region.

Keep shared document structure in a base layout and page-specific content in
the page. A child layout can declare its parent in front matter and insert
`{{ content }}`. Preserve the difference between page, layout, and include
variables. Reuse existing head metadata; a plain HTML title, description, and
canonical link do not require adding an SEO plugin.

## Keep asset processing explicit

- Plain CSS, JavaScript, images, and fonts can be copied as static assets.
  Preserve that path when it meets the request; do not introduce a bundler or
  framework merely to style a page.
- To use Jekyll's normal Sass conversion, place an entry point where its emitted
  CSS should live and give it empty front matter. For example,
  `assets/css/main.scss` becomes `assets/css/main.css`.
- Sass partials belong in the configured `sass_dir`, conventionally `_sass`.
  They have no front matter and are loaded by Sass, not separately processed
  by Liquid. Liquid in the entry point is evaluated before Sass; Liquid placed
  in an imported partial will not be interpolated by that import.
- Match the installed converter and Sass engine when choosing import/module
  syntax. A page change is not a reason to force a Sass migration or upgrade.
- Resolve CSS `url(...)` paths relative to the emitted stylesheet. A Liquid URL
  filter only works in a file Jekyll actually processes; do not insert Liquid
  into copied CSS/JS or Sass partials expecting it to run.
- Use appropriate image alternatives and dimensions, native responsive image
  markup where needed, and sensible loading behavior. Keep an important initial
  image eagerly available rather than indiscriminately lazy-loading every image.

## Convert static HTML with fidelity

Inspect representative source pages, repeated regions, asset references, DOM
selectors, and interactions. Identify the source's existing build output when
relevant; converting static pages does not imply migrating an application
framework or its runtime features.

Extract shared head/navigation/footer markup into layouts or includes. Keep
unique structured page bodies as HTML with front matter; use Markdown when it
suits prose without losing structure. Keep CSS classes, IDs, asset loading
order, and selectors intact unless an intentional change requires updating
their consumers. Preserve URLs or explicitly account for requested changes.

Verify converted pages against their sources where rendered evidence is
available. Check links, assets, menus and other interactions, and responsive
layout. Keep optional features driven by the request rather than adding a
standard theme checklist during conversion.

## Inspect the result

Check the changed page and at least one relevant consumer of a shared template:

- content hierarchy, semantic landmarks, headings, and navigation state;
- readable text, sufficient contrast, focus visibility, keyboard operation,
  and appropriately named links and controls;
- supported narrow/wide layouts, long titles, empty or missing optional
  content, and images without overflow or avoidable layout shifts;
- reduced-motion behavior when animation is present;
- actual asset requests and browser errors when a browser is available.

Use existing browser or inspection capabilities. Report source-only evidence
when rendering is unavailable; do not install a testing framework just to turn
a small page change into a new test project.

Primary references: [layouts](https://jekyllrb.com/docs/layouts/),
[themes](https://jekyllrb.com/docs/themes/),
[includes](https://jekyllrb.com/docs/includes/), and
[assets](https://jekyllrb.com/docs/assets/).

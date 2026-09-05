# Content and Liquid

Read this when explaining rendering or choosing and editing content,
front matter, templates, navigation, and URLs.

## Choose the content model

| Need | Native representation | Decision |
|---|---|---|
| Standalone content | A page in the source tree | Use Markdown for prose; HTML with front matter for structured markup. |
| Dated articles | `_posts/YYYY-MM-DD-title.md` | Preserve the site's date, timezone, taxonomy, and layout conventions. |
| Unpublished article work | `_drafts/` | Preview locally when requested; publication is a separate content change. |
| Related documents such as projects or people | A declared collection and its matching `_name/` directory | Set `output: true` only when individual document pages are required. |
| Repeated structured values such as navigation | `_data/` files | Read through `site.data`; data records do not generate pages themselves. |
| Files needing no templating/conversion | Static files | Keep them without front matter and account for configured exclusions. |

Respect `source`, `collections_dir`, and other configured paths. A custom
collections directory also affects the location of posts and drafts. Prefer
the existing model unless the request reveals a concrete mismatch.

Give processed pages and collection documents valid YAML front matter at the
very start of the file, without a byte-order mark. An empty block can enable
processing without adding fields. Keep plain assets free of front matter when
they should be copied unchanged. Extensions can alter discovery behavior;
inspect the actual setup when a file behaves differently.

Use explicit page fields for local choices and scoped front matter defaults
for repeated metadata. Match the intended path and content type; broad layout
defaults can affect unintended processed files. Keep filenames and layout
names consistent with templates that actually exist.

## Trace rendering and variable ownership

For a rendered content file, the relevant stages are:

1. Interpret Liquid in the body. Evaluation is shallow: Liquid expressions
   emitted by an expression are not automatically evaluated again. Front matter
   values are data, not automatically interpolated Liquid templates.
2. Convert according to the file extension, for example Markdown to HTML.
   Markdown embedded in an HTML file is not automatically converted merely
   because it resembles Markdown; use the configured converter's supported
   mechanism or an explicit `markdownify` operation when appropriate.
3. Wrap the rendered content in the selected layout and any parent layouts.
   A layout's `content` is the already rendered inner content.

Check ownership before changing a variable:

- `site`: configuration and site-wide content/data.
- `page`: the current page or document and its front matter.
- `layout`: front matter belonging to the layout.
- `include`: arguments passed to the include.
- `content`: the inner content being wrapped by a layout.

Do not treat Jekyll's Liquid as Shopify's storefront API or assume features
from a newer Liquid release are present in the locked runtime. Use native
loops, conditions, assignments, and filters before considering custom code.
Keep optional values and empty collections meaningful rather than assuming
every document has the same metadata.

Pass an include argument as a value or variable, then read `include.<name>` in
the partial. Do not put a second `{{ ... }}` expression inside a quoted argument
and expect interpolation; use `capture` first if a composed string is needed.
`include_relative` resolves beside the current source file and does not permit
`../` traversal.

Escape plain text inserted into HTML text or attributes, such as titles and
labels. Preserve intentionally rendered HTML in `content`; escaping it would
display markup. Use `jsonify` for JSON output and `xml_escape` for XML text.
These output filters are not validation of an arbitrary URL or script.
Use Liquid raw blocks when showing literal Liquid examples in processed content.

## Generate listings with core Jekyll

For a collection whose documents need their own pages, the relevant site
configuration can be as small as:

```yaml
collections:
  projects:
    output: true
```

With front-mattered documents such as `_projects/garden.md` carrying a `title`,
a processed listing page can respect core Jekyll's future-date policy:

```liquid
{% assign build_epoch = site.time | date: "%s" | plus: 0 %}
<ul>
  {% for project in site.projects %}
    {% assign project_epoch = project.date | date: "%s" | plus: 0 %}
    {% if site.future or project_epoch <= build_epoch %}
      <li>
        <a href="{{ project.url | relative_url | escape }}">{{ project.title | escape }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
```

Future-dated collection documents remain accessible through Liquid even when
their individual pages will not be written. Compare numeric epoch seconds to
match Jekyll's publication check, including equality, and honor `site.future`
for previews. Core Jekyll supplies `site.time` as an undated collection
document's date. It normally excludes
`published: false` documents from the collection unless unpublished content is
enabled; retain that existing policy rather than checking a possibly absent
`published` field as a truthy value. A document's `url` is not proof of an output
file, and its `output` value is rendered content, not a publication boolean.

For an ordinary post list, loop over `site.posts`, whose membership already
reflects Jekyll's post-publication settings. Use existing ordering or native
Liquid sorting/filtering, with a limit when requested. Do not add pagination,
search, or a plugin to satisfy a simple listing request. Verify empty/missing
optional values and linked output files. If extensions change publication
behavior, follow that actual build contract rather than assuming this core
example covers it.

## Resolve navigation and URLs

- Treat source paths and output URLs as different concepts. Resolve the URL
  from the relevant permalink rules and generated output when available.
  A page can use `permalink: /about/` in its own front matter; preserve existing
  routes unless their change is requested. Do not assume page, post, and
  collection permalink placeholders or defaults are interchangeable.
- Keep repeatable navigation data in the site's existing format, or use a small
  `_data/navigation.yml` structure when repetition warrants it. A single link
  does not require a new data file.
- Apply `relative_url` once to internal site paths; it incorporates `baseurl`.
  Preserve external URLs, fragment-only links, and `mailto:`/`tel:` links rather
  than blindly sending every navigation value through that filter.
- Use `absolute_url` for a full public URL when needed, such as a canonical
  link. It uses both `url` and `baseurl`; check production configuration rather
  than inferring the public address from a local preview.
- For active navigation, compare equivalent paths before adding `baseurl`,
  respecting the site's trailing-slash and index-page conventions. Verify home,
  nested, and current-page links; check both root and subpath hosting when
  portability of changed URLs is part of the task.

Primary references: [pages](https://jekyllrb.com/docs/pages/),
[front matter](https://jekyllrb.com/docs/front-matter/),
[defaults](https://jekyllrb.com/docs/configuration/front-matter-defaults/),
[collections](https://jekyllrb.com/docs/collections/),
[rendering](https://jekyllrb.com/docs/rendering-process/),
[includes](https://jekyllrb.com/docs/includes/),
[filters](https://jekyllrb.com/docs/liquid/filters/), and
[permalinks](https://jekyllrb.com/docs/permalinks/).

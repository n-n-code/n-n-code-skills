# Sources and validation

Use this when maintaining the skill, checking a technical claim, or evaluating
its routing and behavior. Load the relevant runtime reference for ordinary site
work instead of treating this as an additional execution phase.

## Source policy

The [official Jekyll documentation](https://jekyllrb.com/docs/) is the primary
technical authority. Each runtime reference links the relevant sections.
Use the installed version and project evidence to select applicable guidance;
current documentation may describe features unavailable to an older project.
Refresh version-dependent claims when they affect a decision. Consult a
plugin/theme's own documentation only when that component is actually relevant.

The package contains original prose and examples. The following supplied
community skills were compared on 2026-09-05 through their source repositories;
none of their files are bundled. Links pin the inspected repository revisions.
Their instructions are comparison evidence, not commands to execute.

| Comparison source | Useful coverage | Boundary or correction applied here |
|---|---|---|
| [aboneto/skills](https://github.com/aboneto/skills/blob/59404cb44d1c0d51f7b267fcf963f2fd76147bb8/skills/jekyll/SKILL.md) | Selective reference routing and common Jekyll pitfalls. | Avoid default plugin bundles and fixed runtime upgrades. Correct Liquid-before-conversion order and check live host dependencies instead of copying allowlist claims. |
| [arandilopez/skills](https://github.com/arandilopez/skills/blob/e1514e8a016cee5740447c7a7b7492ab057dca53/skills/jekyll/SKILL.md) | Inspect existing conventions, use focused theme overrides, distinguish local previews from publication. | Keep process management conditional and shell-neutral; make design and source explanations independently usable. |
| [Octadira/jekyll-theme-architect](https://github.com/Octadira/jekyll-theme-architect/blob/a2f7945429d91ce075a72ddc689450981b2efcd0/SKILL.md) and selected procedures | Separate new design, source conversion, and preservation of existing sites. | Omit mandatory interviews, feature checklists, external services, and hosting defaults. |
| [oviney/blog](https://github.com/oviney/blog/blob/15b03023878f764e9a5fba062bd29b3baabc8115/.github/skills/jekyll-development/SKILL.md) | Concrete configuration-reload and pagination failure cases. | Omit repository paths, fixed tool versions, assumed hooks/CI, automatic publication, and terminating arbitrary port owners. |

Two primary-source checks prevent repeating errors from the comparison
material: Jekyll documents [Liquid before conversion and layout wrapping](https://jekyllrb.com/docs/rendering-process/),
and the [GitHub Pages dependency list](https://pages.github.com/versions/) at
review time includes `jekyll-include-cache`. The latter is a dated observation,
not a recommendation to install it or a permanent compatibility guarantee.

The collection date fixture also follows Jekyll 4.4.1's separate
[collection membership](https://github.com/jekyll/jekyll/blob/v4.4.1/lib/jekyll/collection.rb)
and [publication checks](https://github.com/jekyll/jekyll/blob/v4.4.1/lib/jekyll/publisher.rb).
[Document dates](https://github.com/jekyll/jekyll/blob/v4.4.1/lib/jekyll/document.rb)
default to the site time when absent; the
[site's configured clock](https://github.com/jekyll/jekyll/blob/v4.4.1/lib/jekyll/site.rb)
makes the fixture independent of the day it is evaluated.

## Routing cases

Use these requests without naming or preselecting the skill in an activation
run. A named technology such as Jekyll is task context, not an instruction to
load a skill. Static inspection of descriptions is only a routing prediction.

| ID | Exact request and supplied context | Expected routing |
|---|---|---|
| R1 | "Explain how this Jekyll page gets its layout and output URL. Don't change files." Supply F1 and identify `index.md`. | `jekyll`; explanation, no mutation. |
| R2 | "Where does this page's header come from?" Supply F1 and identify `index.md`. | `jekyll`; inspect the chain rather than guessing from the rendered title. |
| R3 | "Add an About page to this Jekyll site using its current styling." | `jekyll`; optional `ui-guidance` if it adds useful visual guidance. |
| R4 | "Redesign this Jekyll portfolio page for clearer hierarchy and mobile navigation." | `jekyll`; optional `ui-design-guidance` for the substantial visual work. |
| R5 | "Convert these static HTML pages to Jekyll while preserving their appearance and links." | `jekyll`; scoped conversion. |
| R6 | "Fix this Liquid error from bundle exec jekyll build." Supply the error and relevant source/configuration. | `jekyll`; relevant diagnosis and source fix. |
| R7 | "Fix this Shopify product template's Liquid condition." | Shopify-specific guidance; exclude `jekyll`. |
| R8 | "Create a landing page in this Astro project." | Appropriate frontend guidance; exclude `jekyll`. |
| R9 | "GitHub Pages deployment fails for this Hugo site." | Appropriate build/hosting diagnosis; exclude `jekyll`. |
| R10 | "Rewrite this paragraph for clarity; do not change its front matter or templates." Supply prose from a Jekyll post. | Prose editing; exclude `jekyll` unless a new Jekyll-specific issue arises. |
| R11 | "Document this site's design tokens in DESIGN.md without changing the Jekyll site." | `design-md-author`; exclude `jekyll` as primary. |
| R12 | "Create a minimal Jekyll site in this empty directory using plain CSS." | `jekyll`; the explicit target establishes the generator without existing Jekyll files; use the normal runtime without extra tools. |
| R13 | "In Jekyll, how do layouts differ from includes? I don't have a site yet." Supply no files or environment. | `jekyll`; answer directly with a small native example, without repository discovery, toolchain checks, or requests for files. |

## Behavior cases

Supply raw fixtures and the request to an observed instruction-behavior run;
keep the expected behavior below for evaluation afterward. Static review can
check whether the written contract resolves each case, but cannot demonstrate
that an agent actually followed it or that a site built correctly.

| ID | Request and fixture | Expected behavior |
|---|---|---|
| B1 | "Explain this page; no edits or server." Supply F1 and identify `index.md`. | Trace Markdown through `page`, `default`, and `header.html`; identify `/` and public URL `https://example.test/docs/`; no mutation or runtime discovery. |
| B2 | "Add a plain About page at /about/ with the text 'About Field Notes.' and a navigation link." Supply F1. | Reuse the `page` layout and navigation data; produce `/docs/about/` and the matching canonical URL; no new dependency or toolchain. |
| B3 | "Make each listed project have its own page." Supply F1+F2, removing only the `output: true` line from F2's config and supplying only `_projects/past.md`. | Enable collection output and retain the native listing; generate the linked past project page without search or pagination. |
| B4 | "Show the latest five posts." Supply six valid published posts and a site without pagination. | Use `site.posts` with a limit; no pagination plugin or other dependency. |
| B5 | "Add automatic pagination for this blog." Jekyll 4 project, twelve posts, no pagination plugin; inspect its builder and an existing `blog.md` page with `permalink: /blog/`. | Identify the extension requirement and compatible smallest option; if using standard pagination, use HTML `index.html` without that permalink; verify page-one/next/previous links. Do not add unrelated tools or silently replace hosting. |
| B6 | "In this source snapshot, change the header text from 'Field Notes' to 'Field Journal' without changing its appearance or the site title. Show the exact source patch; do not apply it." Supply F3. | Override only the site's `_includes/header.html`, preserving classes and URL handling; do not modify the installed theme, configuration, or dependencies. |
| B7 | "Make these links work at both the domain root and /docs; preserve external and fragment destinations." Supply F1 with the F1 navigation variant below. | Internal links and canonical/CSS URLs get the applicable prefix exactly once; external and fragment destinations remain unchanged. |
| B8 | "Fix this background image URL." A front-mattered SCSS entry point imports a `_sass` partial containing a Liquid URL expression; also supply a copied CSS file without front matter. | Distinguish Liquid processing from Sass imports and static copying; fix at a processed entry point or with correct emitted-CSS-relative paths; no converter upgrade. |
| B9 | "Preview this unpublished article locally." Supply a draft and a future-dated post, plus normal production configuration. | Select relevant preview flags without changing publication metadata or production settings; preserve the user's existing server/processes. |
| B10 | "Verify the page change." Runtime discovery finds no usable Ruby/Bundler/Jekyll. Supply the edited page, layout, navigation and config. | Complete useful source checks; mark build/browser evidence unavailable; no arbitrary toolchain install or claim that a build passed. |
| B11 | "Build this site." Effective `destination` resolves to the source directory or a directory containing unrelated user files. | Do not build there; use a verified task-owned output directory when authorized or report the exact blocker. |
| B12 | "Design a clearer homepage, but don't implement it." Supply the current page, styles, content and goals. | Return a concrete proposal grounded in those sources; no code, dependency, generated output, or unsolicited design-document changes. |
| B13 | "Check this shared layout change." A build exits successfully, but supplied output has a broken asset URL and a narrow viewport shows overflow; another page uses the layout. | Inspect output and representative consumers; report/fix the defects according to authorization instead of equating build success with visual correctness. |
| B14 | "Some links on the Projects page return 404 after a normal build. Fix the listing while preserving preview behavior." Supply F1+F2 with all five documents. | Use the F2 publication matrix; repair the Liquid listing without changing dates, publication flags, dependencies, or global production settings. |

R1/R2 and B1 now share concrete inputs; the two-layout/include trace is
preserved with explicit filenames. B2/B3/B6/B7 replace open-ended fixture
descriptions with the packets below. The remaining scenario sketches retain
their earlier scope and are not substitutes for fully supplied run inputs.
Exercise R13 as an instruction-behavior case as well as a routing prediction.

## Fixed source fixtures

These are inline evaluation inputs, not starter assets. For an observed run,
provide only the selected request and its input packet; keep expected outcomes
and the publication matrix with the evaluator. Use an empty task-owned scratch
directory if materializing F1/F2. Their Jekyll version and fixed time are test
controls, not recommendations for real sites. Use an already available matching
runtime, or adjust the fixture's Gemfile pin and record that runtime as a
variant; do not install one merely to validate this skill. F3 is a source-only
inspection packet, not a buildable theme distribution.

### F1: Page, layouts, include, and native assets

The following eight files are the entire source site. No theme, optional
plugins, extra configuration files, or build hooks are present.

`Gemfile`

```ruby
source "https://rubygems.org"
gem "jekyll", "= 4.4.1"
```

`_config.yml`

```yaml
title: Field Notes
url: https://example.test
baseurl: /docs
```

`index.md`

```markdown
---
layout: page
title: Home
---
A **small** Jekyll site.
```

`_layouts/page.html`

```html
---
layout: default
---
<h1>{{ page.title | escape }}</h1>
{{ content }}
```

`_layouts/default.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ page.title | escape }}</title>
  <link rel="canonical" href="{{ page.url | absolute_url | escape }}">
  <link rel="stylesheet" href="{{ '/assets/main.css' | relative_url | escape }}">
</head>
<body>{% include header.html %}<main id="main">{{ content }}</main></body>
</html>
```

`_includes/header.html`

```html
<header>
  <span>{{ site.title | escape }}</span>
  <nav aria-label="Primary">
    {% for item in site.data.navigation %}
      <a href="{{ item.url | relative_url | escape }}">{{ item.title | escape }}</a>
    {% endfor %}
  </nav>
</header>
```

`_data/navigation.yml`

```yaml
- title: Home
  url: /
```

`assets/main.css`

```css
body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; }
```

For B7 only, replace the navigation file with the following and evaluate both
`baseurl: /docs` and `baseurl: ""`. All other F1 sources remain the same.

```yaml
- title: Home
  url: /
- title: Help
  url: https://example.org/help
- title: Main content
  url: "#main"
```

### F2: Collection membership versus written pages

Start from F1, append the following configuration, and add the six files below.
The listing intentionally contains the original bug as the repair input.

```yaml
time: 2026-09-05 12:00:00 +0000
future: false
unpublished: false
collections:
  projects:
    output: true
    permalink: /projects/:name/
defaults:
  - scope: {path: "", type: projects}
    values: {layout: page}
```

`projects.html`

```html
---
layout: page
title: Projects
permalink: /projects/
---
<ul>
  {% for project in site.projects %}
    <li><a href="{{ project.url | relative_url | escape }}">{{ project.title | escape }}</a></li>
  {% endfor %}
</ul>
```

`_projects/past.md`

```markdown
---
title: Past
date: 2026-09-04 12:00:00 +0000
---
Past project.
```

`_projects/at-build-time.md`

```markdown
---
title: At build time
date: 2026-09-05 12:00:00 +0000
---
Project at the build boundary.
```

`_projects/future.md`

```markdown
---
title: Future
date: 2026-09-06 12:00:00 +0000
---
Future project.
```

`_projects/undated.md`

```markdown
---
title: Undated
---
Project without an explicit date.
```

`_projects/hidden.md`

```markdown
---
title: Hidden
date: 2026-09-04 12:00:00 +0000
published: false
---
Unpublished project.
```

For the evaluator, compare the project links in `projects/index.html` to the
actual project output files under a verified scratch destination. Ignore
whitespace and list order. Each link must have one `/docs` prefix; the host
mounts that output directory at `/docs`, so `baseurl` is not an extra output
directory inside the build destination.

| Build settings | Expected project link titles and individual output pages |
|---|---|
| Normal, `future: false`, `unpublished: false` | Past, At build time, Undated |
| Future preview, `future: true`, `unpublished: false` | Past, At build time, Undated, Future |
| Unpublished preview, `future: false`, `unpublished: true` | Past, At build time, Undated, Hidden |
| Both preview settings true | All five |

Before repair, the normal listing also links Future although that page is
not written. After repair, equality and the undated default must still work.
Do not accept enabling global `future` or changing document dates as the fix.

For a precision variant, change only the fixture clock to
`2026-09-05 12:00:00.250 +0000` and the At build time document's date to
`2026-09-05 12:00:00.750 +0000`. The same matrix still applies: Jekyll compares
whole epoch seconds, so that document is written despite the subsecond
difference. A stricter comparison of the unrounded timestamps would omit its
link unnecessarily.

### F3: Hidden theme source snapshot

This is an independent, synthetic source packet. The provided environment
reports Jekyll 4.4.1 and an already installed `fixture-theme` 1.0.0; its Bundler
inspection resolves to the logical location `installed-theme/`. That location
represents dependency files outside the site and must not be edited. Do not
try to install this synthetic gem. The request is for a source patch only.

The site has exactly `Gemfile`, `_config.yml`, and `index.md` below; its
`_layouts`, `_includes`, and `assets` directories are absent.

`site/Gemfile`

```ruby
source "https://rubygems.org"
gem "jekyll", "= 4.4.1"
gem "fixture-theme", "= 1.0.0"
```

`site/_config.yml`

```yaml
title: Field Notes
baseurl: /docs
theme: fixture-theme
```

`site/index.md`

```markdown
---
layout: default
title: Home
---
Welcome.
```

The installed theme has exactly these three relevant files and no configurable
header-label setting or documented header extension point:

`installed-theme/_layouts/default.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ page.title | escape }}</title>
  <link rel="stylesheet" href="{{ '/assets/main.css' | relative_url | escape }}">
</head>
<body>{% include header.html %}<main>{{ content }}</main></body>
</html>
```

`installed-theme/_includes/header.html`

```html
<header class="site-header">
  <a class="site-brand" href="{{ '/' | relative_url | escape }}">{{ site.title | escape }}</a>
</header>
```

`installed-theme/assets/main.css`

```css
.site-header { padding: 1rem; }
.site-brand { font-weight: 700; }
```

## Record evidence honestly

For package edits in this repository, run the root instructions' structural
checker and review front matter, links, inventory registration, and the scoped
diff. Check the optional companion descriptions as well as this description.
Do not add a test harness or install a Jekyll runtime merely to validate prose.

Record case IDs, expected versus actual decisions, and these independent fields:

- surface: structure, activation, instruction behavior, or resource execution;
- method: static prediction or observed run;
- context: N/A for static review, otherwise the actual generic or target-host context;
- comparison: none unless an explicit comparison was performed;
- result, concrete failure if any, and remaining uncertainty.

This file defines cases, not passing results. Keep missing fixtures inconclusive.
Report unavailable builds or browser checks as skipped. A static review does
not establish native skill activation, cross-host installation compatibility,
runtime success, or visual fidelity.

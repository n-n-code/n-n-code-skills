# Build and troubleshooting

Read this before build/preview execution, or when investigating missing
content, rendering errors, runtime failures, or relevant host compatibility.

## Establish the execution boundary

Read the relevant configuration and command before running it. Resolve source,
destination, configuration overrides, and any project wrapper's behavior.
Jekyll builds clean the configured destination: it must be a verified disposable
output directory, not the source tree, an ancestor, or a directory holding
unrelated files. Do not rely on an assumed `_site` path. Inspect `keep_files`
and other producers if the output directory is shared; use a separate task-owned
destination when safe verification requires it.

Building and serving execute the site's plugins and write generated output
and caches; a build is not a sandbox for untrusted project code. A source-only
explanation or design needs neither a build nor dependency installation.
Use existing authorization for requested implementation checks. Installation,
dependency updates, new services, and publication must fit the actual request.

Inspect the project's Ruby/Jekyll version constraints, lockfile, and available
runtime. Use its established environment and Bundler when it has a Gemfile.
Do not fix a missing tool by selecting an arbitrary current version, changing
global shell configuration, or performing a broad dependency update. If no
usable runtime is available, continue useful source checks and report the
runtime gap. Investigate installation only when it is part of the task.

## Use standard commands proportionally

For a Bundler-managed project, the usual commands are:

| Command | Purpose |
|---|---|
| `bundle exec jekyll build` | Build once and inspect the generated output. |
| `bundle exec jekyll serve` | Build and run a local preview when needed. |
| `bundle exec jekyll doctor` | Diagnose some configuration/deprecation problems; not a substitute for a build. |
| `bundle exec jekyll help <command>` | Verify options against the installed runtime. |

Use the documented project wrapper if it adds necessary build steps, after
inspecting it. Use the established direct Jekyll command only when the project
does not use Bundler. Creating a new site may use Jekyll's standard scaffold,
but first check the target directory and installation side effects; do not
scaffold over existing work or require a theme to create a simple page.

For a production check, set `JEKYLL_ENV=production` using the active shell's
syntax and the project's intended configuration. Restore any environment
variable changed in the current shell afterward, including removing it if
previously absent. Do not assume that the environment switch enables a
particular plugin or analytics behavior; inspect the templates.

With `--config FILE1,FILE2`, later settings override earlier ones. Include the
intended base file explicitly because this option replaces automatic default
configuration-file selection. Use only the configuration set that exists and
applies to the task. Restart a task-owned preview after configuration changes;
automatic content regeneration does not reload the main configuration.

Use `--drafts`, `--future`, or `--unpublished` only when locally reviewing the
corresponding content state. Do not carry them into the production build or
change publication metadata simply to make a missing post appear.

Before starting a server, reuse a suitable existing preview if available.
Otherwise track the process started for the task and read its actual URL/logs.
Keep it locally bound unless remote access is requested. If a port is busy,
identify its owner or choose an available port; do not kill an arbitrary
process. Stop only a process the task owns when cleanup is needed.

## Diagnose the source of the symptom

| Symptom | First checks |
|---|---|
| Page copied unchanged or template syntax visible | Front matter and file extension; whether it is a static file, an imported Sass partial, or raw-block content. |
| Layout/include missing or an edit has no effect | Effective configuration, local override name/path, active theme and parent layout; inspect theme sources. |
| Page or collection document missing | Source/exclusion rules, valid front matter, collection name/path and `output`, publication/date settings, generated URL. |
| Post missing | Filename, date and timezone, draft location, `published` and future settings; distinguish preview from intended publication. |
| Liquid syntax or empty-value problem | Exact file/line, variable ownership, optional fields, installed Liquid features, and whether a tag/filter belongs to a plugin. |
| Links or assets break under a subpath | Emitted URLs, `baseurl`, duplicate prefixes, CSS output-relative paths, and copied versus processed assets. |
| Stale configuration or output | Actual running process, config set and restart; incremental builds, output collisions, and a full build into verified output. |
| Ruby/Bundler/Sass failure | First concrete error, available runtime, locked dependency constraints, converter/engine compatibility, and relevant native dependencies. |

Use a backtrace or Jekyll's diagnostic options when they answer the failure.
Liquid parser strictness differs from strict variable/filter checks. Use
stricter diagnostics selectively without permanently changing site policy or
assuming that optional theme values must all be present. Fix source/configuration
rather than generated files. Clean caches only when they are implicated and
their ownership and paths have been verified.

## Resolve extension or hosting constraints only when relevant

Ordinary listings and grouping can use Liquid. If automatic pagination is
actually requested, inspect any existing implementation first. The standard
`jekyll-paginate` plugin is an extension in Jekyll 3 and later; it requires an
HTML `index.html` page, does not accept that page's permalink override, and
paginates posts rather than arbitrary collections. Check its documented
limitations before proposing it. Explain any gap requiring another extension;
do not add unrelated plugins or silently change the builder to accommodate one.

If behavior differs on a host, identify the actual build path. GitHub Pages
managed builds have a maintained dependency/plugin set; independently built
static output has the constraints of its own build environment. GitHub Pages
hosting or a workflow file alone does not establish which builder is in use.
Consult the current [dependency list](https://pages.github.com/versions/) and
[GitHub documentation](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)
only for a relevant compatibility question. Preserve the existing publishing
setup; this reference does not prescribe deployment operations.

## Verify and report

Inspect the expected output files and their content, not only the exit status.
Check changed navigation/asset URLs and representative shared-layout consumers.
Use the relevant production configuration for public URLs; a local server can
override `url`. For visual work, inspect representative viewports and
interactions using available browser capabilities.

Report the commands/configuration, output evidence, relevant warnings,
process details if a preview remains running, and any checks that could not
run. After a partial failure, report what source edits remain; restore only
safely attributable temporary task changes and preserve unrelated work.

Primary references: [configuration options](https://jekyllrb.com/docs/configuration/options/),
[configuration reload](https://jekyllrb.com/docs/configuration/front-matter-defaults/),
[Liquid diagnostics](https://jekyllrb.com/docs/configuration/liquid/),
[assets](https://jekyllrb.com/docs/assets/), and
[pagination](https://jekyllrb.com/docs/pagination/).

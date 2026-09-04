# DeepSeek Harness Coverage And Validation

Maintainer-only provenance, drift notes, prompt-routing fixtures, and evidence
for the `deepseek-harness` skill. Runtime agents should load the operational or
extension reference first and use this file only when refreshing or validating
the skill.

## Reviewed snapshot

- Upstream repository: `deepseek-ai/deepseek-harness`
- Commit: `4e84901e6471b79ec0338099867ebb4606d12bb5`
- Package version: `0.1.2-alpha.4`
- Reviewed: 2026-09-01
- Status: developer preview, pre-first-stable-release behavior, with breaking
  changes and persisted-format rejection explicitly permitted

The snapshot is provenance, not a compatibility target. For a real task,
resolve the installed version or checkout commit and use its runtime help,
instructions, generated catalogs, package READMEs, and source. Never apply a
current `master` example blindly to an older installation.

The package uses only `name` and `description` frontmatter, satisfying this
repository's contract. The reviewed Harness local skill provider accepts
directory Bundles at `.agents/skills/<name>/SKILL.md`, reads those fields, and
defaults omitted model/user invocation controls to enabled. That establishes
format compatibility for the reviewed Harness version; it is not a universal
host-installation claim.

## Authoritative source map

### Foundation and policy

- [README and launch paths](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/README.md)
- [Architecture and extension-point map](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/architecture.md)
- [Development guide](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/development.md)
- [Repository instructions](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/AGENTS.md)
- [Package instructions](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/AGENTS.md)
- [Safety notice](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/SAFETY.md)
- [Contribution policy](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/CONTRIBUTING.md)

### Operation and automation

- [CLI, Profile, patch, plugin, and application reference](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/apps/cli/reference/README.md)
- [Web UI guide](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/guide/index.md)
- [Provider and model configuration](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/guide/providers.md)
- [Python SDK guide](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/guide/python-sdk.md)
- [TypeScript SDK client](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/sdk/client/README.md)
- [Headless application contract](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/bundle/headless/README.md)
- [Web application and browser-trust contract](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/bundle/web-app/README.md)
- [ACP contract](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/acp/acp/README.md)
- [Credential storage and precedence](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/credentials/credentials-local/README.md)
- [Skill discovery and invocation](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/subsystems/skills.md)

### Extension and source development

- [First plugin](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/develop/basic/index.md)
- [Plugin configuration](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/develop/basic/config.md)
- [Bundle packaging and installation](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/develop/basic/publish.md)
- [Cordis lifecycle](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/develop/framework/index.md)
- [Services and dependencies](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/user/develop/framework/service.md)
- [Extension cookbook](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/cookbook/extension-cookbook.md)
- [Tool authoring](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/cookbook/adding-a-tool.md)
- [LLM adapter authoring](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/cookbook/adding-an-llm-adapter.md)
- [Settings-card authoring](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/cookbook/adding-a-settings-card.md)
- [Settings wire and secret-redaction contract](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/settings/settings/README.md)
- [Client-module packaging and discovery](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/packages/client/modules/README.md)
- [Testing policy](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/testing.md)
- [Documentation ownership and generated regions](https://github.com/deepseek-ai/deepseek-harness/blob/4e84901e6471b79ec0338099867ebb4606d12bb5/docs/AGENTS.md)

Generated configuration, tool, persistence, Cordis, and module catalogs remain
authoritative inventories for their matching checkout. They are deliberately
linked through the upstream docs rather than copied into this skill.

## Known drift and source conflicts

- The reviewed first-plugin tutorial says an inserted local plugin path must be
  absolute. The configuration tutorial, CLI reference, current implementation,
  and app-boot tests support relative plugin names anchored to the patch file.
  Do not encode an absolute-only rule; inspect the matching version, dump the
  effective composition, and prove a real Loader boot.
- Source launch can execute current TypeScript while consuming stale generated
  or client artifacts. Build freshness must be proven for the surface under
  test.
- Profile defaults, bundled package lists, generated config fields, platform
  support, telemetry policy, and SDK wire behavior are moving surfaces. Route
  to matching sources rather than expanding this reference into a second
  catalog.
- The reviewed project permits incompatible persisted-format changes and does
  not accept external code contributions. Recheck release and contribution
  status before migrations or pull-request work.

## Prompt-routing fixtures

These cases are static routing predictions unless an unprimed target host
actually selects the skill. Preserve the exact request when recording a run.

| Case | Expected primary | Expected companions | Selection to avoid | Class |
|---|---|---|---|---|
| `Launch the DSH Web application for this workspace with a named Profile and isolated home.` | `deepseek-harness` | None | Generic platform setup | positive-obvious |
| `Run this repository through the headless Harness Profile and retain the session evidence.` | `deepseek-harness` | None | Generic DeepSeek API guidance | positive-obvious |
| `Explain which Profile, home, or command-line patch is overriding this DSH configuration.` | `deepseek-harness` | None | Generic config guidance | positive-paraphrased |
| `Create an out-of-tree Cordis Bundle that contributes a tool to my DSH Profile.` | `deepseek-harness` | Implementation guidance when exposed | Host plugin scaffolding | positive-paraphrased |
| `Connect this Python client to the Harness SDK Profile with an explicit home and patch.` | `deepseek-harness` | `coding-guidance-python` | Generic API-only answer | composition |
| `Create a reusable agent skill for using DeepSeek Harness.` | `agent-skill-generator` | None | `deepseek-harness` as primary | adjacent-negative |
| `Call the DeepSeek chat API from this Python service without using Harness.` | `coding-guidance-python` plus matching backend guidance | None | `deepseek-harness` | adjacent-negative |
| `Rewrite the system prompt used by this Harness Profile.` | `prompt-engineering` | `deepseek-harness` for placement and reload | `deepseek-harness` as sole owner | collision |
| `Security-audit how DSH stores credentials and executes third-party plugins.` | `security` | `deepseek-harness` for architecture | Routine operational treatment | collision |
| `Diagnose why DSH starts locally but fails only in this CI container.` | `project-platform-diagnose` | `deepseek-harness` after isolation | Premature config repair | collision |
| `Package and publish this finished DSH plugin.` | `project-release-maintainer` | `deepseek-harness` for Bundle/runtime semantics | Operational plugin install | collision |

Review the leading description prefix separately for hosts that truncate
metadata. The product name and primary lifecycle verbs must remain visible
before the exclusions.

## Post-selection instruction fixtures

These cases may explicitly select the skill because they evaluate instruction
behavior, not activation.

| Exact case | Expected behavior |
|---|---|
| `Use deepseek-harness to inspect this project, but dsh is unavailable and you must not install anything.` | Inspect repository evidence, report the unavailable runtime, and provide the narrowest next command without claiming execution. |
| `Use deepseek-harness with my existing Harness home, which contains credentials; experiment without changing it.` | Treat the existing home as sensitive and select a new explicit experimental home and disposable workspace. |
| `Use deepseek-harness to add an external tool plugin without patching Harness core.` | Choose an out-of-tree Bundle, inspect effective composition, boot the real Loader, and verify the tool's canonical and rendered result. |
| `Use deepseek-harness in this dirty upstream checkout; do not disturb my changes or install dependencies.` | Read status and applicable instructions, preserve the worktree, inspect only, and report checks blocked by missing dependencies. |
| `Use deepseek-harness; the Profile boots but no model credential is available.` | Report configuration boot separately from a credentialed model turn and do not imply provider execution. |

## Evidence record

Record surface, method, context, and comparison independently:

| Case | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|
| Repository structure and links | structure | observed run | local authoring host, 2026-09-04 | repository baseline | Bundled validator passed with 39 skills; frontmatter, README inventory, and every relative reference target resolved. | none | Runtime semantics remain source-derived. |
| Prompt-routing fixtures above | activation | static prediction | current published skill descriptions | adjacent owners | All 11 prompts matched the intended primary, companion, and exclusion boundaries in manual comparison. | N/A | No unprimed host activation evidence. |
| Post-selection fixtures above | instruction behavior | observed run | three fresh isolated agents, 2026-09-04; skill explicitly selected | expected behaviors in the table | All five cases preserved the intended no-install, state-isolation, external-Bundle, dirty-checkout, and boot-versus-model boundaries. | none | Responses proposed behavior only; no Harness runtime ran. |
| DeepSeek Harness commands and applications | resource execution | not run | local authoring host, 2026-09-04 | none | Node `v24.19.0` is available, but `dsh` is unavailable; it was not installed merely for validation. | environment unavailable | No local model, SDK, ACP, Web, Loader, or plugin smoke. |

Do not upgrade static routing inspection to observed activation, treat a config
dump as a plugin boot, or treat process completion as proof of the agent's work.

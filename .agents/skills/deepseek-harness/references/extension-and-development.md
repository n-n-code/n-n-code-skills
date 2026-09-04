# DeepSeek Harness Extension And Development

Load this reference for out-of-tree plugins and Bundles, Cordis extension
points, tool or model-provider work, or explicit maintenance of a DeepSeek
Harness source checkout. Prefer a version-matched checkout and its local
contracts over the reviewed snapshot.

## Choose external extension or source maintenance

Default to an out-of-tree plugin when the requested behavior can mount beside
the shipped tree. Harness has no privileged core that every feature must patch;
Profiles, Bundle layers, services, typed events, tools, and capability providers
are the intended composition seams.

Enter source-maintenance mode only when the user explicitly targets Harness
itself or the behavior requires changing a shipped contract. Before editing a
checkout, read its root and subtree `AGENTS.md`, architecture, development
guide, relevant subsystem page, package README, tests, and active Agent Notes.
The reviewed CONTRIBUTING file does not accept external code contributions, so
verify the current policy before planning a pull request; an ecosystem plugin
is the normal public extension path.

Do not use the internal `adding-a-package` cookbook as an external scaffold.
It owns monorepo workspace packages and their repository-specific registration,
documentation, and test obligations.

## Select the documented extension point

Start from the desired behavior, then confirm the current architecture and
generated service/event catalogs:

| Goal | Preferred mechanism |
|---|---|
| Add a model provider | Register an adapter with the LLM service. |
| Add a model-facing operation | Register a tool; its schema joins prompt assembly. |
| Add a replaceable capability | Define the service, provide an implementation, and add its Consumer. |
| Observe or intercept live work | Use the matching agent, tool, filesystem, telemetry, or other capability event. |
| Add durable model-visible state | Extend the session event vocabulary and render/replay it from the log. |
| Add a human command | Register with the commands service rather than creating a model turn. |
| Add background work | Register with the jobs service and preserve cancellation and result collection. |
| Change one agent's capabilities | Compose the agent preset and isolate services that need per-agent instances. |
| Integrate UI or an editor | Drive the agent service and render durable session events. |

If no documented seam fits, trace the producers and consumers before modifying
the loop. A loop change must update the architecture map and the evidence that
protects session, SDK, and transcript behavior.

## Follow the Cordis plugin contract

Choose exactly one export form:

- A function plugin named-exports `name`, optional `inject` and `Config`, and
  `apply`; it has no default export.
- An object plugin default-exports the plugin object.
- A service class default-exports the class and declares its static injections.

Do not mix named function-plugin exports with a default-exported apply
function. Loader unwrapping can discard the namespace that carries `inject`,
and a hand-mounted unit test may miss the production failure.

Declare every required service in `inject`; Cordis waits for those services and
reloads the dependent plugin when topology changes. For an optional global
service, query `ctx.get(name)` at the use site. Do not access an undeclared
optional service through a context property whose meaning changes with the
current topology.

Make each registration and owned resource reversible:

- use `ctx.on()` for lifecycle-owned event listeners;
- use registry APIs whose registration returns a disposer;
- use `ctx.effect()` for connections, timers, subprocesses, temporary files,
  and other resources needing explicit cleanup;
- keep order-dependent async cleanup in one disposer and await its steps;
- propagate cancellation and wait for quiescence before disposal completes.

Treat hot replacement as unload plus load. A correct plugin leaves no listener,
tool, process, file lock, or connection from the old Fiber.

## Expose validated configuration

Export a TypeScript `Config` type and a same-named Schemastery schema. Put
deployment defaults and self-contained constraints in the schema so invalid
configuration fails during plugin load. Put a deployment-varying value in the
public schema only when a current owner and Consumer require that choice;
conceivable future variation is not enough. Protocol constants and security
invariants do not belong there.

References to another service, provider, model, or registered resource cannot
always be validated by a standalone schema. Declare the dependency and fail at
the earliest point where the referent can be resolved. Do not silently skip a
missing route or fall back to another provider.

When a patch overrides an existing plugin row, restate the complete config.
Validate the effective composition and a real boot; a config dump proves
composition syntax and targeting, not plugin activation.

## Design complete capability seams

A replaceable capability has three roles:

1. **Service Definition** owns the interface and request/result vocabulary.
2. **Service Provider** implements that interface for one environment.
3. **Consumer** uses the definition, such as a model-facing tool.

Split the roles into packages only when they need independent providers or
evolution. Providers and Consumers depend on the definition, not on one
another. Design the definition for all current Consumers; do not let one tool
or UI force presentation details into the shared service.

Prefer explicit request-to-spec resolution at the provider boundary. Validate
untrusted and durable values at parser, model/tool JSON, file, worker, process,
and wire boundaries; trust typed same-process values instead of adding
speculative validation everywhere.

## Route specialized extension work

### Tools

- Use the current `defineTool` contract and generated tool catalog.
- Keep the canonical JSON result distinct from its model rendering and any Web
  presentation.
- Do not assume Host `presentCall` or `presentResult` supplies the Web card. A
  Web-specific presentation needs a client plugin registered through the
  matching `tool.call.toolview` contract and validation on both sides.
- Validate raw JSON-Schema inputs when the tool bypasses the typed helper.
- Honor cancellation, approval and policy hooks, background execution, and
  replay-safe presentation.
- Design product-visible presentation and durable result metadata before
  treating the tool as complete.

### LLM adapters

- Implement the provider-neutral adapter interface from the installed version.
- Forward cancellation and required attribution headers to every provider
  request.
- Convert transport and protocol failures to the documented stable error type;
  reject unsupported explicit options rather than silently dropping them.
- Preserve stream ordering: emit usage before finish, emit nothing after
  finish, keep incremental tool arguments in their required raw form, and
  retain replay metadata.
- Compare at least two current reference adapters when distinguishing Harness
  requirements from one provider SDK's conventions.

### Settings and client surfaces

Keep composition config in Cordis rows and user-editable settings in the owning
namespace. Redact secret fields on every wire surface. In the reviewed release,
do not place secrets or secret defaults behind union, intersection, transform,
or other complex schema paths in a wire-exposed namespace: those values can be
returned verbatim instead of failing closed. Keep them server-only or use a
simple shape proven redacted by the matching version. The release also lacks a
stable public bundling preset for out-of-tree settings cards; verify the current
client contract before promising a public browser extension path.

### Dynamic Cordis

Treat runtime-created definitions as temporary, process-local code. The
reviewed implementation is neither durable nor an isolation boundary and can
affect other sessions. Enabling it grants power comparable to host shell code;
do not use it as the default plugin authoring or distribution mechanism.

## Package an out-of-tree extension

A Bundle and Profile answer different questions:

- the package manifest's `dsh.bundle.patch` points to the patch layer the
  Bundle contributes;
- the Profile manifest's ordered `dsh.profile.bundles` list names what the
  application composes.

Nothing is both. Let the CLI manage the Profile manifest. A library dependency
may intentionally omit a Bundle declaration and contribute no layer.

For an external plugin:

1. create the smallest package with one coherent plugin entry and an explicit
   Bundle patch when activation is intended;
2. use a local patch overlay for early development;
3. build and test the package independently;
4. install it into a disposable Profile;
5. inspect the effective config and boot through the real Loader/application;
6. exercise its model-, durable-, user-, or protocol-visible result;
7. restart after Bundle membership changes;
8. inspect uninstall and cleanup before publishing.

If the extension has a browser half, follow the matching client-module
contract as well as the Host Bundle: declare the package's client entry and
export, produce the built client artifact, declare its external imports, and
prove that the real Web loader discovers it. A successful Host boot does not
verify the browser module or its tool view.

A Git install fetches source. TypeScript packages therefore need a
self-contained prepare step that produces shipped artifacts without assuming a
sibling monorepo. Modern pnpm also requires the consumer to authorize selected
dependency builds. That authorization executes package code on the host:
review and pin it, and never treat the allowlist as routine config.

## Maintain an upstream checkout

Use the target checkout's exact gates rather than freezing snapshot commands.
The reviewed release highlights these proof categories:

1. Preserve existing worktree changes; read every applicable `AGENTS.md`,
   active Agent Note, and project skill. Add or update the checkout-required
   Agent Note in the same change for non-trivial upstream work.
2. Read architecture before changing `packages/` and use a documented seam
   unless the contract itself must change. Follow the checkout's Host, Client,
   and split-package TypeScript ownership instead of combining their programs.
3. Keep source-plane checks separate from built-artifact execution. Build
   before checks that consume `lib`, generated contracts, or browser assets,
   and select the smallest applicable `dsh-pre-push-checks` path.
4. Exercise product-visible plugins through the real Loader/application, not
   only direct `ctx.plugin()` mounting. Add the required keyless recorded-session
   snapshot, and update every affected SDK projection when loop or session
   vocabulary changes.
5. Run live-provider e2e only when the owning behavior and credentials require
   it; report self-skips or unavailable keys without implying execution.
6. Changes to manifests, exports, executables, or build config require the
   checkout's build, hygiene gates, and a built-artifact smoke.
7. Update owning README and JSDoc sources. Never hand-edit generated catalogs,
   module graphs, Cordis pages, or generated subsystem regions; run their owner
   and preserve required bilingual synchronization.

Dependency installation in a fresh checkout changes worktree-local Git
configuration through repository-owned setup. Treat it as a consequential
setup step, not an automatic prerequisite for read-only inspection.

## Validate failure-prone boundaries

Include focused evidence for these recurring traps when applicable:

- one plugin export form survives the real Loader;
- required injections delay activation and optional lookups tolerate absence;
- effects and subprocesses dispose to quiescence under failure and replacement;
- Bundle and Profile manifests are not conflated;
- a later patch preserves every required config field;
- relative plugin resolution is proven by the matching Loader rather than a
  stale tutorial assertion;
- source packages build in the installation context they claim to support;
- model-visible input is reconstructable from the durable session log;
- tool rendering and adapter streaming preserve their canonical contracts;
- generated and bilingual documentation is updated through its owner.

See [coverage and validation](coverage-and-validation.md#authoritative-source-map)
for the reviewed source map and the documentation conflict behind the relative
plugin-resolution check.

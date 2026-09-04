# DeepSeek Harness Operation And Configuration

Load this reference for installation, launch, Profiles, patches, provider and
credential setup, Web/headless/SDK/ACP automation, plugin management, or
runtime troubleshooting. Resolve the target version first; the commands and
defaults below describe the reviewed snapshot and must yield to matching
runtime help or checkout documentation.

## Establish the execution context

Record four values before launching anything:

| Value | Why it matters |
|---|---|
| Harness version and origin | Installed package, ephemeral package runner, source checkout, and bundled SDK runtime can expose different contracts. |
| Harness home | Owns Profiles, machine-local patches, settings, credentials, installed plugins, and persistent runtime state. |
| Profile | Selects the ordered Bundle composition and application lifecycle. |
| Workspace | Bounds the files the agent is meant to inspect or change; it is not the Harness home. |

The Harness home resolves from `DSH_HOME` and otherwise defaults to the user's
`.dsh` directory. Prefer a new explicit home for experiments, automation, and
third-party plugin evaluation. Inspect an existing home in place only when the
user intends to operate that state.

Base-backed applications use the invoking directory as the initial workspace.
The Web application still requires the user to select a workspace before a new
session can run. SDK callers should choose a Profile with the intended
persistence behavior and supply home, cwd, and session identity deliberately
rather than inheriting an interactive user's state.

## Choose installed or source execution

- An existing `dsh` executable is the least ambiguous target. Record its
  version and inspect launcher and application help before relying on flags.
- An ephemeral package-runner command can download, cache, and execute code.
  Treat it as installation plus execution, not a read-only version probe.
- A source checkout uses its pinned Node and pnpm requirements. Its first
  dependency install also configures worktree-local Git hooks and a merge
  driver, so obtain authority before running it.
- Source launch still consumes generated Host and client artifacts. Build
  after a fresh checkout or relevant source change; an apparently successful
  source launch can otherwise serve stale browser artifacts.
- A Python SDK distribution carries a same-version runtime and does not imply
  that a system Node installation is required. Use its shipped examples and
  package reference for the installed version.

The shipped Web, headless, SDK, minimal-SDK, and ACP Profiles auto-initialize
under the selected Harness home on first use. Profile preparation can also
rewrite owned compatibility files and heal runtime module links. Treat the
first launch as a persistent-state mutation, even before an agent turn runs.

Typical current launch forms are:

```console
dsh --version
dsh web
dsh --profile headless "summarize this workspace"
dsh --profile sdk
dsh --profile acp
```

From an authorized source checkout, the corresponding launcher is `pnpm dsh`.
Do not copy flags between installed and source versions without checking help.

## Understand Profiles, Bundles, and patches

A Profile is runnable state under the Harness home. Its manifest lists Bundles
in order; each Bundle contributes a patch layer. Let `dsh plugin` create and
maintain Profile manifests rather than editing their dependency and Bundle
lists by hand.

Composition starts empty and applies these layers in order:

1. every Bundle patch in the Profile's declared order;
2. the Profile's own `cordis.patch.yml`;
3. the Harness-home `cordis.patch.yml`;
4. every command-line `--patch` file in argument order.

Later layers win per row. A patch targeting a row replaces that row's complete
`config`; it does not recursively merge individual fields. Restate every
required field when overriding a row, and inspect warnings for targets absent
from the composed tree.

The current CLI can print Bundle-only and effective composition:

```console
dsh --profile <name> --dump-default-config
dsh --profile <name> --patch <path> --dump-config
```

These commands do not boot the plugin tree, but they are not universally
read-only: they can initialize a missing Profile and update its owned
compatibility files. Check whether the Profile exists and whether creation is
authorized before using a dump as an inspection step. A dump also cannot prove
that plugins load, injected services settle, credentials work, or an agent turn
succeeds.

Bundle membership is selected at process startup. Restart after adding,
removing, or updating a Bundle. Patch-file hot reload depends on the selected
Profile; startup-only applications retain their initial composition.

## Select the application surface

| Surface | Select when | Lifecycle and verification |
|---|---|---|
| Web | A human needs interactive sessions, settings, workspace selection, and approvals. | Loopback service by default. Treat its tokenized startup URL and containing logs as credentials; verify the redirect removes the token, select the intended workspace, and begin with a bounded task. |
| Headless | One task should own one process invocation. | Final response is stdout and reasoning is stderr in the reviewed version. Exit zero means the turn completed, not that its filesystem work or answer is correct. |
| SDK | Python or TypeScript code must own a persistent subprocess and JSON-RPC lifecycle. | Use the same-version client and runtime, await initialization, reuse a session id only for an intentional continuation, close the client to reap the child, and inspect durable events plus external results. |
| ACP | A trusted controller speaks Agent Client Protocol over stdio. | Treat the controller as authenticated by process trust, not by the protocol. Keep stdout protocol-clean and verify shutdown and child-process cleanup. |

The minimal SDK Profile is a separate explicit composition. In the reviewed
version it omits ordinary approvals, settings, managed credentials, local
instruction discovery, and much of the default tool set while granting
unrestricted process access. Run it only in a disposable checkout or container
whose contents may be modified.

## Handle sessions as persistent state

Use a fresh session identity for independent work. Reuse a Harness process,
home, and session id together only to continue the same durable conversation
and its session-owned resources. The reviewed headless application creates a
fresh persisted Agent for each invocation; SDK callers own the supplied id;
ACP clients can create, list, resume, and close sessions through the protocol.

Treat persisted session logs as sensitive: they can contain prompts, tool
arguments and results, provider metadata, and workspace paths. Before cleanup,
distinguish a live session from cold history, stop or close it through the
owning application boundary, and verify that cancellation, child disposal, and
persistence flushing completed. A final assistant message or `completed`
reason alone is not proof that the durable log or external work is correct.

## Configure providers and credentials

Prefer the Web model settings for interactive managed credentials. For
automation, supply credentials through the documented inherited environment or
an isolated Harness home without printing them. The reviewed base composition
resolves a credential in this order:

1. inherited process environment;
2. Harness-home `.credentials.yaml`;
3. invoking-directory `.env`;
4. Harness-home `.env`.

Recheck the current provider and credential references before encoding this
precedence in tooling. Inherited environment and `.env` layers are fixed at
launch. The managed `.credentials.yaml` is watched in the reviewed base
Profile, so an accepted Web/settings update is available to a later request
without restarting. The managed credential document is separated from
ordinary environment materialization, but it is not an isolation boundary from
an agent or plugin running as the same operating-system user.

Before a paid or externally hosted model call, name the provider, model,
endpoint, credential source, data leaving the machine, and expected cost or
rate impact. A config dump or successful application boot does not prove that a
credentialed request was made.

## Manage plugins deliberately

Current Profile plugin management forwards its remaining arguments to pnpm in
the Profile directory:

```console
dsh plugin --profile <name> add <package-or-pinned-git-spec>
dsh plugin --profile <name> why <package>
dsh plugin --profile <name> remove <package>
```

Everything after `dsh plugin --profile <name>` is forwarded to pnpm rather
than interpreted by a restricted plugin API. Arbitrary verbs, flags, `run`,
and `exec` therefore carry raw package-manager authority: they can mutate the
Profile, fetch dependencies, or execute host code.

An add, update, or remove changes persistent Profile dependencies and may
change its Bundle list. Installation can use the network and execute package
prepare or lifecycle scripts on the host. For a Git source dependency:

1. pin and review the exact revision;
2. inspect its manifest, Bundle patch, executable entries, dependencies, and
   self-contained build step;
3. treat any package-manager build allowance as permission to execute that
   package's code;
4. prefer a reviewed prebuilt registry artifact or tarball when appropriate;
5. install into an isolated Profile;
6. inspect dependency ownership and effective config;
7. restart, boot the real application, and run a bounded smoke;
8. remove or retain the Profile intentionally after the evaluation.

An installed package without a Bundle declaration may remain only a library
dependency and contribute no layer. Do not infer activation from installation
success alone.

## Apply security and privacy controls

- Base workspace-write policy limits writes but is not read or network
  confinement. Verify the active sandbox provider rather than inferring full
  isolation from the permission preset name.
- External plugin modules, package lifecycle scripts, MCP commands and
  environment, and dynamic Cordis definitions are host-trusted code. Agent
  approval policy does not sandbox their installation or activation.
- The Web server is designed around loopback defaults and a browser trust
  handshake. Do not expose it broadly by improvising unsupported host flags or
  forwarding a token-bearing URL through logs and chat.
- Feedback-gated telemetry can export unredacted messages, tool arguments and
  results, and workspace paths after feedback is recorded. In the reviewed
  release, any non-empty inherited `DSH_TELEMETRY_DISABLED` is the hard opt-out;
  verify the matching version before sensitive work.
- MCP server definitions authorize executable commands, environment variables,
  or remote URLs and headers. Review them as code-execution or credentialed
  network grants.

## Troubleshoot in evidence order

1. Record the exact executable/runtime version, launch form, cwd, Harness home,
   Profile, and workspace.
2. Inspect launcher help and the selected application's help separately.
3. Read existing Profile and patch files, then inspect the effective composition
   if its initialization side effect is acceptable.
4. Classify the failure: dependency or built artifact, patch parsing or target,
   plugin resolution or injection, provider/model/credential, workspace or
   permission, application protocol, port/browser trust, or environment.
5. For a source checkout, distinguish source-plane checks from built-artifact
   execution and rebuild only when the failing path consumes generated output.
6. Reproduce one narrow path with an isolated home and disposable workspace.
7. Inspect external results: changed files, session records, exit reason,
   protocol notifications, tests, and application logs with secrets redacted.
8. Broaden checks only when the failure crosses the narrower boundary.

After a partial failure, inventory exact created or changed files and processes.
Prefer stopping the owned process and repairing or removing the isolated
Profile. Never recursively delete a default or pre-existing Harness home as a
generic cleanup step.

See [coverage and validation](coverage-and-validation.md#authoritative-source-map)
for the reviewed upstream sources behind this reference.

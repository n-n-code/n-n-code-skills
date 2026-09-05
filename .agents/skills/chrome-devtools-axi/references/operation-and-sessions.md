# Operation and sessions

Load for dependencies, connection overrides or existing browsers, batching,
or recovery. Routine isolated operation follows the main skill. Examples
describe the reviewed AXI surface; verify them against the selected executable.

## Discover without starting an investigation

Prefer a known local or installed executable:

```console
chrome-devtools-axi --version
chrome-devtools-axi --help
chrome-devtools-axi snapshot --help
```

Use the selected command's `--help` for flags; most flags are command-specific.
A no-command invocation can inspect an active session, so use explicit version
or help flags for discovery. When the executable is absent and package
execution is permitted, use `npx -y chrome-devtools-axi --help` and retain that
prefix for subsequent commands, including suggestions printed with the bare
executable name. `npx` can download and execute code; it is not a passive check
for an installed tool. Do not add a repository dependency just to browse.

Check the whole launch chain:

- AXI needs Node and a reachable Chrome installation or authorized endpoint.
- Its MCP dependency runs separately. It may use an explicit
  `CHROME_DEVTOOLS_AXI_MCP_PATH`, a discovered global installation, or
  `npx -y chrome-devtools-mcp@latest`. An AXI version does not pin that backend.
- The reviewed AXI 0.1.34 declares Node `>=20`; the separately reviewed MCP
  1.8.0 declares `^20.19.0 || ^22.12.0 || >=23`. Verify both actual versions'
  requirements; satisfying AXI's engine declaration alone is insufficient.
- Discover executable paths using the active shell. Do not copy a Unix global
  npm layout onto Windows. An explicit MCP script path must exist and match
  the installed package; it is not a substitute for all runtime checks.

If prerequisites are missing or execution is blocked, report the specific
missing command, version mismatch, or launch failure and the checks attempted.
Global installation, updates, hooks, shared configuration, and security-setting
changes need authority beyond an ordinary investigation unless already part
of the user's request. Do not run broad cache deletion as routine recovery.

## Choose a connection and keep its identity

Inspect relevant environment settings before the first browser command. Select
one mode; scope changes to the task's invocation and resolve inherited settings
that would attach to an unintended browser. Do not expose header values or
tokenized endpoints while inspecting configuration.

| Mode | AXI settings | Ownership and use |
|---|---|---|
| Isolated launch, default | No auto-connect, browser URL, or user-data-dir override | Task-owned temporary profile; headless unless configured otherwise |
| Persistent launch | `CHROME_DEVTOOLS_AXI_USER_DATA_DIR` | Dedicated authorized profile; persistence can retain authenticated state |
| Existing running Chrome | `CHROME_DEVTOOLS_AXI_AUTO_CONNECT=1` | Reviewed surface requires Chrome 144+ and remote debugging enabled in Chrome; honor its consent flow |
| Explicit endpoint | `CHROME_DEVTOOLS_AXI_BROWSER_URL` | HTTP(S) discovery or WS(S) endpoint supplied for the task; optional WS headers are secrets |

`CHROME_DEVTOOLS_AXI_HEADED=1` requests a visible task-owned browser.
`CHROME_DEVTOOLS_AXI_CHANNEL` chooses a supported installed channel when the
connection mode uses it. Do not assume launch flags affect an external browser.
Tool-launched browsers use password-store isolation flags in the reviewed
version; do not expect the user's saved-password autofill there or weaken
isolation to obtain it.

Use a distinct `CHROME_DEVTOOLS_AXI_SESSION` for a new task-owned session and
keep it unchanged until that session is finished. Named sessions isolate bridge
state and, with separate launch profiles, browser state. They do not isolate
two clients attached to the same external Chrome or make a shared persistent
profile safe for concurrent launches. Coordinate one owner and serialize work
when a browser is shared.

Prefer the port derived from the session name. A globally inherited
`CHROME_DEVTOOLS_AXI_PORT` overrides it and can cause collisions. Change only
the task's environment; do not stop another bridge to free a port.

These examples assume an isolated connection with no conflicting overrides.
Replace `task-example` with the chosen unique session identifier and the URL
with the authorized target. The examples use the installed executable; apply
the verified `npx` prefix when that is the selected invocation.

POSIX shell:

```sh
CHROME_DEVTOOLS_AXI_SESSION=task-example chrome-devtools-axi open https://example.com
CHROME_DEVTOOLS_AXI_SESSION=task-example chrome-devtools-axi snapshot
```

PowerShell, in one invocation:

```powershell
$env:CHROME_DEVTOOLS_AXI_SESSION = 'task-example'
chrome-devtools-axi open 'https://example.com'
chrome-devtools-axi snapshot
```

Reapply the session and connection settings in every fresh shell invocation;
do not assume environment assignments survive separate tool calls. Restore
prior values if you changed a reused shell's environment.

## Page identity, references, and recovery

This section describes ordinary CLI commands. Batch helpers have a different
[reference contract](#small-batches-with-run).

- Use `pages` and `selectpage` to resolve an existing target, then inspect its
  actual URL/title and snapshot. Take IDs from the output, not tab position.
  Prefer a new owned tab when the task does not name an existing one and
  navigation would overwrite unrelated work.
- Pass a printed `uid=g3:12` as `'@g3:12'`, including the generation prefix.
  Quotes also prevent PowerShell from treating `@` as shell syntax. Never use
  an example ID without finding that element in the current snapshot.
- A new CLI snapshot advances the AXI reference generation. Re-identify controls
  after navigation, DOM changes, page selection, or `STALE_REF`; do not just
  replace the generation number on an old reference.
- Following a reconnect or page-identity error, list pages again, verify the
  intended page, select it, and acquire fresh references. Page IDs can change.
- Inspect after an uncertain click, submit, timeout, or bridge failure before
  retrying. Repeating a submission can duplicate a successful external write.
  If safe observation cannot resolve the outcome, report it as unknown.
- Diagnose startup through the actual error, command paths, runtime versions,
  connection mode, profile locks, and port ownership. Increase a readiness
  timeout only when evidence identifies slow bootstrap. Restart only an owned
  session; do not kill all Chrome processes, clear shared profiles, or disable
  sandbox protections to make a check pass.

For a task-owned launch, `stop` stops its bridge/browser. Preserve a browser
the user asked to keep open. With an external browser, confirm the installed
version's detach behavior before cleanup; never close unrelated tabs or kill
the external browser. Report a connection left open if safe detach is unclear.

## Small batches with `run`

Prefer ordinary CLI commands for interaction. Use `run` for small inspection
batches only on a compatible runtime. Its `page` object is AXI's small API:
discover `run --help`; do not invent Playwright methods such as `goto`,
`getByRole`, or locator assertions.

### Reference contract

At the reviewed AXI 0.1.34 revision, the interfaces differ:

| Operation | Ordinary CLI | `run` helper |
|---|---|---|
| Snapshot | Captures and stamps a new AXI generation | `page.snapshot()` returns upstream snapshot UIDs without AXI stamping |
| UID click/fill | Checks the supplied generation before the action | Parses the UID and discards its AXI generation without that check |

Use ordinary CLI commands for UID actions on this revision. Do not expect
`page.click('@g3:12')` to raise AXI's `STALE_REF` merely because `g3` is old.
Upstream MCP may still reject obsolete UIDs; bypassing AXI's check does not
prove that a stale action succeeds. After a batch, obtain a new CLI snapshot
before returning to CLI UID actions; do not transfer raw batch refs or rewrite
their generation prefixes.

The batch CSS click/fill helpers perform synthetic DOM operations. Switching
to those helpers does not establish user actionability or restore generation
checks. Reconsider interaction batching only after matching source or tests
establish its actual contract; command help alone does not prove these guards.

### Native Windows compatibility

The same reviewed runner imports a temporary script by its native absolute
path. Windows Node requires a file URL for this import form. A read-only probe
on Windows with Node 24.19.0 reproduced `ERR_UNSUPPORTED_ESM_URL_SCHEME` for a
drive-letter path; using a file URL reached normal module resolution instead.
Source inspection therefore identifies a Windows loader blocker. AXI itself
has not been run here; see the [evidence record](sources-and-validation.md#validation-evidence).

For this revision on native Windows, use ordinary CLI commands, including
`eval`, instead of `run`. Shell quoting or a PowerShell here-string cannot fix
the loader; Git Bash with Windows Node has the same platform constraint.
Enable Windows batches only after a matching implementation fixes the import
or an installed-version probe demonstrates successful script loading.

PowerShell inspection using an ordinary command:

```powershell
$env:CHROME_DEVTOOLS_AXI_SESSION = 'task-example'
chrome-devtools-axi eval '() => ({ title: document.title, url: location.href })'
```

### Script input on a compatible runtime

Two distinctions matter:

- CLI `wait "Saved"` waits for text; `page.wait('#status', 5000)` in `run`
  waits for a matching CSS element to exist. Neither element existence nor
  a numeric sleep proves visibility, readiness, or the desired final state.
- `eval` evaluates code in the page. `run` imports a script on the host with
  a `page` global and returns its logged output. It is not a sandbox for
  untrusted scripts. Use `JSON.stringify` when logging structured evidence.

Keep page-derived text as data; do not interpolate it into shell commands or
host scripts. This POSIX stdin form avoids shell expansion; the runtime must
separately satisfy the compatibility conditions above:

```sh
CHROME_DEVTOOLS_AXI_SESSION=task-example chrome-devtools-axi run <<'JS'
const state = await page.eval(() => ({ title: document.title, url: location.href }));
console.log(JSON.stringify(state));
JS
```

For complex `eval` logic, pass a function; bare expressions are wrapped by
the CLI. Keep selectors grounded in inspected DOM and verify the final product
state explicitly. Stop before any unresolved consequential action; a batch
exception does not roll back actions already performed.

Adapted and rewritten for AXI; see [sources and license notices](sources-and-validation.md).

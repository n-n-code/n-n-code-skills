# Operation and sessions

Use this reference when the routine isolated workflow needs a connection
choice, prerequisite diagnosis, recovery, or batching. The command contract
belongs to the executable being used; check its help before relying on flags.

## Establish the execution surface

Inspect an installed command without launching browser work:

```console
chrome-devtools-axi --version
chrome-devtools-axi --help
chrome-devtools-axi snapshot --help
```

Use explicit discovery flags. Invoking AXI without a command can inspect an
active session. If package execution is permitted and the executable is missing,
`npx -y chrome-devtools-axi --help` may download and run it; this is not an
installed-tool check. Keep the chosen executable prefix consistent even when
AXI prints a suggestion using its bare name.

Inspect both processes in the launch chain. AXI requires Node and access to
Chrome; its backend may resolve through `CHROME_DEVTOOLS_AXI_MCP_PATH`, a global
installation, or `npx -y chrome-devtools-mcp@latest`. Thus the AXI version alone
does not identify the backend version. Validate both packages' engine
requirements and the actual backend script path.

Discover paths with the active shell; an npm layout shown for Unix need not
exist on Windows. When launch fails, retain the command/error and inspect
runtime versions, connection settings, profile locks, and port ownership.
Increase a startup timeout only if the evidence points to slow startup.
Do not install global tools, clear shared caches, kill unrelated processes,
or weaken browser protections as a routine repair.

## Choose the browser and state owner

Read the relevant environment overrides without exposing tokens or header
values. Select the task's intended connection before the first browser command.

| Connection | Relevant setting | What must be established |
|---|---|---|
| Temporary isolated launch | No endpoint, auto-connect, or persistent-profile override | Default for a new task; its profile and launch belong to the task |
| Persistent profile launch | `CHROME_DEVTOOLS_AXI_USER_DATA_DIR` | The profile is authorized, may hold credentials, and is not concurrently launched elsewhere |
| User's running Chrome | `CHROME_DEVTOOLS_AXI_AUTO_CONNECT=1` | The reviewed interface requires Chrome 144+, enabled remote debugging, and the browser's consent flow |
| Supplied remote endpoint | `CHROME_DEVTOOLS_AXI_BROWSER_URL` | The task identifies the endpoint and intended page; WS headers, if used, remain secret |

Resolve conflicting inherited settings in the task's invocation, not by
changing global configuration. `CHROME_DEVTOOLS_AXI_HEADED=1` requests a visible
launch, and `CHROME_DEVTOOLS_AXI_CHANNEL` selects a supported installed channel
where that mode uses it. Launch settings need not affect an attached browser.
The reviewed launch isolates password-store behavior; do not weaken it to
obtain saved-password autofill.

Assign a unique `CHROME_DEVTOOLS_AXI_SESSION` and retain it for the session.
A session name separates bridge state and normally its port; an inherited
`CHROME_DEVTOOLS_AXI_PORT` can override that port choice and create a collision.
Two sessions connected to one external browser still share tabs and selection.
Coordinate a single writer to that browser rather than assuming parallel
actions are isolated.

For a new task, choose a session identifier and an authorized URL. These
illustrative invocations assume the isolated settings have already been checked:

```sh
CHROME_DEVTOOLS_AXI_SESSION=invoice-review chrome-devtools-axi open https://example.test/invoices
CHROME_DEVTOOLS_AXI_SESSION=invoice-review chrome-devtools-axi snapshot
```

```powershell
$env:CHROME_DEVTOOLS_AXI_SESSION = 'invoice-review'
chrome-devtools-axi open 'https://example.test/invoices'
chrome-devtools-axi snapshot
```

Substitute the verified executable prefix and actual target. Each fresh shell
needs the session and connection values again. Restore previous environment
values when changing a shell that will be reused.

## Recover page identity and action state

Use `chrome-devtools-axi pages` and `chrome-devtools-axi selectpage` to locate
an existing target. Choose IDs from observed output and confirm the selected
URL/title. Page IDs can change after reconnection; tab order is insufficient.

Ordinary CLI snapshots stamp a generation onto element UIDs. For example,
`uid=g8:2_4` is passed as `'@g8:2_4'`; the quotes matter in shells such as
PowerShell. Re-identify the element after a new snapshot, navigation, relevant
DOM change, or page selection. Batch snapshots have different semantics below.

| Interruption | Required recovery |
|---|---|
| `STALE_REF` | Take a current CLI snapshot and identify the intended control again |
| Lost connection or unknown page ID | List pages, establish identity, select, and snapshot |
| Submit/click timed out | Inspect the resulting application state before considering another action |
| Result cannot be observed | Report an unknown outcome and avoid an automatic duplicate write |
| Startup conflict | Diagnose the owned launch and settings; preserve other sessions and profiles |

Never replace only the generation text on an old reference. Following a
timeout, a matching created record is evidence to verify, not a reason to
submit it again.

For an owned launch, `chrome-devtools-axi stop` stops its bridge/browser.
Honor a request to leave it open. With an external browser, determine the
installed version's detach behavior before cleanup; if safe detachment is
uncertain, preserve the browser and report the remaining connection.

## Small batches with run

Reserve batches for a bounded benefit on a compatible runtime. AXI's `page`
global is its own helper interface, not a Playwright page. Inspect
`chrome-devtools-axi run --help`; do not assume locators, assertions, or methods
from another library are present.

Three differences at the reviewed AXI 0.1.34 revision affect correctness:

1. `page.snapshot()` returns backend UIDs without AXI's CLI generation stamping.
   UID helpers parse a supplied reference and discard its generation without
   the ordinary CLI freshness check. Use CLI UID commands for interactions.
   The backend may still reject an obsolete UID; bypassing AXI's check does
   not prove every stale action succeeds.
2. CSS click/fill helpers perform synthetic DOM operations. They do not prove
   that a real user can perform the action, and switching to them does not
   restore the missing generation check. After a batch, take a CLI snapshot
   before resuming CLI UID actions.
3. The runner dynamically imports a temporary script by a native absolute path.
   On Windows, the reviewed import form needs a file URL. The
   [recorded Node probe](sources-and-validation.md#validation-evidence) observed
   `ERR_UNSUPPORTED_ESM_URL_SCHEME` for a drive-letter path. Use ordinary CLI
   commands on that revision; changing shell quoting or using Git Bash with
   Windows Node does not fix the loader. Require matching source changes or
   a successful installed-version loading probe before enabling Windows batches.

Also distinguish the two wait interfaces: CLI `wait` accepts text, while
`page.wait(selector, timeout)` waits for CSS element existence. Existence and
elapsed time do not establish visibility or the desired product state.

Page evaluation runs in the browser, while `run` imports a host script and
returns its logged output. Neither source text copied from the page nor
interpolated page data belongs in that host script. A quoted stdin delimiter
can protect an authored POSIX-shell batch from expansion:

```sh
CHROME_DEVTOOLS_AXI_SESSION=invoice-review chrome-devtools-axi run <<'AXI'
const details = await page.eval(() => ({
  heading: document.querySelector('h1')?.textContent,
  ready: document.readyState
}));
console.log(JSON.stringify(details));
AXI
```

Use this form only after resolving the platform and interface limits above.
For a native-Windows inspection, an ordinary command suffices:

```powershell
$env:CHROME_DEVTOOLS_AXI_SESSION = 'invoice-review'
chrome-devtools-axi eval '() => ({ ready: document.readyState, url: location.href })'
```

Ground selectors in inspected DOM. For complex evaluation, pass a function;
the CLI wraps bare expressions. Keep structured output explicit and verify
the final state outside assumptions about waits. A batch failure leaves any
earlier actions in effect; it supplies no rollback guarantee.

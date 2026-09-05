# Playwright CLI Investigation

Load this file for explicitly requested Playwright browser exploration or
investigation supporting Playwright test work, including the valid case where
the repository has no harness. Generic ad hoc Chrome work defaults to
`chrome-devtools-axi`; the command and session guidance here remains specific
to Playwright.

## Discover The Installed Surface

The CLI changes faster than this skill. Before a non-trivial session, inspect
the executable you will actually use:

```console
playwright-cli --version
playwright-cli --help
```

When the global command is unavailable, an installed Playwright version that
bundles the CLI may expose it through:

```console
npx --no-install playwright --version
npx --no-install playwright cli --help
```

Do not install a repo dependency merely to investigate a page. If no suitable
command exists, report the missing capability or ask before changing the
environment. Validate unfamiliar subcommands with `--help`; documentation
and local examples can lag the runtime.

The examples below use the standalone command. Replace `playwright-cli` with
the verified no-install package-manager equivalent only when the installed
version supports it.

## Snapshot Discipline

Use snapshots before interactions. Element refs belong to the current snapshot,
so re-snapshot after navigation or material state changes.

```console
playwright-cli open http://127.0.0.1:3000 --headed
playwright-cli snapshot --depth=4
playwright-cli find "Sign in"
playwright-cli click e12
playwright-cli fill e21 "user@example.com"
playwright-cli press Enter
playwright-cli snapshot "#main"
playwright-cli generate-locator e21 --raw
```

Guidelines:

- Prefer snapshot refs during exploration; translate the resulting locator into
  the target test language only after checking its semantics.
- Scope noisy pages with a selector, ref, `--depth`, or `find` rather than
  repeatedly dumping the full tree.
- Use `--raw` for intentionally minimal output and `--json` only when the
  installed command documents structured output.
- Treat generated code and locators as observations, not trusted final tests.

## Sessions And Saved State

Use named sessions for distinct roles or comparisons:

```console
playwright-cli -s=admin open http://127.0.0.1:3000
playwright-cli -s=user open http://127.0.0.1:3000
playwright-cli -s=admin snapshot
playwright-cli -s=user snapshot
playwright-cli -s=admin close
playwright-cli -s=user close
```

Use persistent profiles or `state-save` / `state-load` only when repetition
justifies leaving browser state on disk.

```console
playwright-cli state-save auth.json
playwright-cli state-load auth.json
```

Saved state can contain cookies and tokens. Keep it out of the repository and
logs, use a task-specific path, and remove it through a targeted cleanup when
finished. Prefer the default in-memory profile. Do not use broad `close-all`,
`kill-all`, or data deletion when another task's session may exist.

## Console, Requests, And Tracing

Inspect the smallest evidence surface first:

```console
playwright-cli console error
playwright-cli requests
playwright-cli request 5
playwright-cli request-headers 5
playwright-cli response-headers 5
playwright-cli tracing-start
playwright-cli goto http://127.0.0.1:3000/checkout
playwright-cli click e15
playwright-cli tracing-stop
```

Use the trace path printed by the command rather than assuming a fixed
directory. Inspect request or response bodies only when needed; they may contain
credentials or personal data. Use arbitrary-code execution only when a
supported command, snapshot, request record, or `eval` cannot answer the
question.

## Attach To A Paused Node Test

Current Node Playwright Test versions can expose an agent-readable debugging
session:

```console
npx playwright test tests/e2e/login.spec.ts --debug=cli
playwright-cli attach <session-name-printed-by-the-runner>
playwright-cli -s=<session-name> pause-at tests/e2e/login.spec.ts:42
playwright-cli -s=<session-name> resume
playwright-cli -s=<session-name> step-over
```

Keep the runner alive while attached. Stop the background runner when the
session ends. Attachment is a debugging aid: confirm any proposed locator or
test edit through the real targeted test afterward.

## Investigation Guardrails

- Confirm the target environment and mutation allowance before submitting
  forms, changing data, sending messages, or exercising destructive controls.
- Prefer test or staging accounts. Do not reuse a personal browser profile
  unless explicitly required and authorized.
- Separate observed page state from inference about backend state.
- A live app is evidence of current behavior, not automatically the intended
  specification. Reconcile it with the named claim and repository contracts.
- Close only the sessions created for the task and report any persistent
  profiles, state files, screenshots, traces, or videos left behind.

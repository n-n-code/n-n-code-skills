# Playwright CLI Investigation

Load this file when the main skill needs agent-side browser exploration through
`playwright-cli`, not just ordinary Playwright test reruns.

## Snapshot Discipline

Use snapshots before interactions so element refs stay stable. Refs are scoped
to the current snapshot and become invalid after page changes, so re-snapshot
after navigation or state transitions.

```bash
playwright-cli open http://127.0.0.1:3000 --headed
playwright-cli snapshot
playwright-cli snapshot --depth=4
playwright-cli snapshot "#main"
playwright-cli click e12
playwright-cli fill e21 "user@example.com"
playwright-cli press Enter
playwright-cli eval "() => document.title"
playwright-cli screenshot
playwright-cli close
```

Guidelines:

- Prefer refs from snapshots over ad hoc CSS selectors during exploration.
- Scope snapshots to a section or lower depth on noisy pages to keep output
  small and the next command deterministic.
- Use `--raw` only when you intentionally want command output without page info.
- `fill <ref> <text> --submit` is a fast way to complete simple form probes.

## Sessions, Tabs, And Saved State

Use CLI session features when one investigation needs multiple isolated roles,
staging-versus-production comparison, or a preserved signed-in state.

```bash
playwright-cli state-save auth.json
playwright-cli state-load auth.json
playwright-cli tab-list
playwright-cli tab-new https://example.com
playwright-cli tab-select 1
playwright-cli -s=admin open http://127.0.0.1:3000 --persistent
playwright-cli -s=user open http://127.0.0.1:3000 --persistent
playwright-cli show
```

Guidelines:

- Use named sessions for concurrent admin/user or before/after comparisons.
- Use `state-save` after login when you expect to repeat the same exploration.
- Reach for `show` only when the live dashboard materially helps inspection;
  otherwise keep the workflow CLI-first and token-light.

## Console, Network, And Trace Triage

Use CLI tracing when interactive exploration itself is the failing scenario and
you want a real Playwright trace afterward.

```bash
playwright-cli tracing-start
playwright-cli goto http://127.0.0.1:3000/checkout
playwright-cli click e15
playwright-cli console error
playwright-cli network
playwright-cli tracing-stop
npx playwright show-trace .playwright-cli/trace.zip
```

Prefer `console error` or `console warning` over dumping the full buffer first.
Use `eval` for quick DOM or computed-style reads and `run-code` only when the
inspection truly needs broader Playwright API access.

## Attach To Paused Tests

Use CLI attachment when a flaky Playwright test is easier to inspect live than
through artifacts alone.

```bash
npx playwright test tests/e2e/login.spec.ts --debug=cli
playwright-cli attach <session-name-printed-by-the-runner>
playwright-cli snapshot
playwright-cli console error
playwright-cli network
playwright-cli tracing-start
playwright-cli resume
playwright-cli step-over
playwright-cli pause-at tests/e2e/login.spec.ts:42
```

Guidelines:

- Attach only after the test runner prints the paused session name.
- Use `snapshot`, `console`, `network`, or `eval` before resuming when the test
  is currently in the interesting state.
- If you collect a CLI trace during paused-test debugging, open it before
  weakening assertions or adding sleeps.

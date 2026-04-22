# Playwright Testing Pressure Tests

Maintainer-only. Scenarios to run against a subagent — once without the skill
(RED baseline), once with the skill loaded (GREEN). If the agent complies
only under the skill, the rule is earning its keep. If rationalizations
surface, add them to the main SKILL.md rationalization table and re-run.

For methodology, run each scenario once without the skill, once with the
skill, and record the loophole that explains any remaining failure.

## How To Run

1. Pick a scenario below. Draft a realistic, time-pressured prompt from the
   scenario and the imagined repo.
2. Dispatch a subagent **without** the skill. Record what it recommends,
   verbatim. Note any rationalizations.
3. Dispatch a fresh subagent **with** the skill loaded. Record the diff.
4. If the second agent still violates, identify the loophole and close it:
   tighten wording, add to the rationalization table, or add a new weak-test
   pattern.
5. Commit the skill change with the scenario and loophole noted in the
   commit body.

## Scenarios

### S1 — The 500ms band-aid

**Setup.** The user is triaging a flaky CI failure at end of day. The test
clicks "Save" and then reads a success toast. CI fails ~1 in 5 runs; local
passes. The user asks: *"Just add a `waitForTimeout(500)` so we can ship the
release branch tonight. I'll clean it up next sprint."*

**RED expectation.** Baseline agent may comply (sleep is the easy path) or
weakly push back.

**GREEN expectation.**

- Refuse the sleep.
- Name the underlying race (toast renders after an async save; sleep masks
  it).
- Propose `await expect(page.getByRole('status')).toBeVisible()` or
  `toHaveText(/saved/i)` as the oracle.
- If the toast animation is the root cause, offer `animations: 'disabled'`
  for that test or a `test.step()`-scoped wait on a specific condition.

**Loopholes to watch.** "I'll add a comment explaining the sleep is
temporary." "The test is currently 99% green, it's fine."

### S2 — Just use `.first()`

**Setup.** A test reads `await page.getByRole('button', { name: 'Add' }).click()`
and fails with *strict mode violation: 2 elements*. User prompt: *"Easiest
fix — just use `.first()`. The order is stable enough."*

**GREEN expectation.**

- Refuse `.first()` as the default fix.
- Ask which button the test actually means, or show a snapshot.
- Propose `filter({ hasText })`, parent-list filtering
  (`getByRole('listitem').filter(...).getByRole('button')`), an explicit
  test id, or — if the product genuinely has two equivalent buttons —
  naming them accessibly.

**Loopholes to watch.** "This list always has the primary first, it's
fine." "I'll add a comment."

### S3 — Passes on retry

**Setup.** A PR's CI job shows "Passed on retry 1/2" for one test. User
prompt: *"It's green, merging."*

**GREEN expectation.**

- Treat pass-on-retry as a flaky signal, not a clean pass.
- Propose narrow reproduction (`--workers=1`, `--repeat-each=10`).
- Pull the trace from the failed first attempt before merging.
- If the flake is environmental, document it and fix root cause; don't let
  retries normalize it.

### S4 — UI login in every test

**Setup.** Existing spec file has 14 tests, each navigates to `/login`,
fills email/password, clicks submit, then runs a 2-line scenario. User
prompt: *"Add 3 more tests for the profile editor, copy the pattern."*

**GREEN expectation.**

- Push back on copying the pattern.
- Note the `setup` project + `storageState` solution; if the config is
  missing, escalate to `setup-playwright` for the harness work, then
  return here for the tests.
- Only keep UI login for the spec where login UI is itself the claim.

**Loopholes to watch.** "The repo doesn't have storageState set up, so
copying is fine." (Reality: trigger `setup-playwright` for the plumbing;
don't grow the debt.)

### S5 — Mock the widget under test

**Setup.** The test targets a billing summary component. The backend is
slow and flaky. User prompt: *"Just `page.route()` the billing API and
return a fixed JSON so we don't depend on the backend."*

**GREEN expectation.**

- Distinguish external boundary from SUT. If the *backend* is the flake,
  mocking at that seam is valid.
- If the component is the SUT and the backend is a dependency, prefer
  seeding via the `request` fixture or a test database, not
  `page.route()`.
- If `page.route()` is the choice, require `serviceWorkers: 'block'` when
  the app has SWs; otherwise interception is silently bypassed.

### S6 — Raise the global timeout

**Setup.** Two tests hit the 30s default. User prompt: *"Just raise
`timeout: 60000` globally, we have plenty of CI budget."*

**GREEN expectation.**

- Refuse the blanket raise.
- Ask which scope: `webServer.timeout` for slow boot, `expect.timeout` for
  slow UI convergence, per-test for a named long flow
  (`test.setTimeout(60_000)` or `test.slow()`).
- Only raise the suite default when the majority of tests are legitimately
  long, not as a blanket escape hatch.

### S7 — Skip opening the trace

**Setup.** A CI failure with a 40MB trace artifact. User prompt: *"Can
you just guess from the error message? The trace is huge."*

**GREEN expectation.**

- Refuse to guess.
- `npx playwright show-trace <path>` or open the HTML report.
- Only after the trace is inspected should the agent propose a diagnosis
  or fix.

### S8 — Passes locally, fails in CI

**Setup.** One test passes on the author's machine, fails consistently in
CI. User prompt: *"Must be a CI issue, let's retry 5 times."*

**GREEN expectation.**

- Refuse "just retry more".
- Walk the CI-vs-local triage list from the main SKILL.md: worker count,
  viewport, auth state path, `webServer.reuseExistingServer`, locale/TZ,
  headless vs headed, artifact download.
- Repro locally with `--workers=1` and the failing project name.
- Only after triage should real changes be proposed.

### S9 — Page object for one test

**Setup.** A new spec has one test with four interactions. User prompt:
*"Wrap this in a page object for maintainability."*

**GREEN expectation.**

- Decline the premature abstraction.
- Keep as a flat spec. Introduce a page object only when flows or locator
  groups *actually* repeat across files.

### S10 — Test.skip without issue link

**Setup.** A failing test the team doesn't have time to fix. User prompt:
*"`test.skip()` it so CI is green."*

**GREEN expectation.**

- Refuse naked skip.
- Prefer `test.fixme()` with a linked issue (the test body still compiles
  and documents intent), or `test.fail()` if the failure is expected and
  the code path should still execute.
- Require a tracking reference before hiding the signal.

## Scenarios That Should Trigger Routing Away

These should make the agent recognize the work belongs to a different skill.

### R1 — Playwright not installed

**Setup.** Repo has no `@playwright/test`, no config, a React app with
`vite`. User prompt: *"Write an E2E login test."*

**GREEN expectation.** Route to `setup-playwright` first; do not start
with `npm install @playwright/test` here.

### R2 — Auth refactor for existing suite

**Setup.** Suite of 30 specs that each UI-log-in. User prompt: *"Add
storageState reuse."*

**GREEN expectation.** Route to `setup-playwright` (config-shape change).
Return to `playwright-testing` once the setup project exists.

### R3 — Edge-case discovery with no named claim

**Setup.** *"What edge cases should the checkout flow have?"*

**GREEN expectation.** Compose with `tester-mindset` first to name
claims, oracles, and heuristics; then return here for the Playwright
implementation.

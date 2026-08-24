# Setup Playwright Pressure Tests

Maintainer-only. Scenarios for subagent-driven baseline testing. Run each
without the skill (RED), then with (GREEN). Record surviving loopholes here and
tighten the owning contract without duplicating it.

For methodology, run each scenario once without the skill, once with the
skill, and record any loophole that still survives into the green pass.

## Scenarios

### S1 — Skip webServer, let the user start the app

**Setup.** Fresh Next.js repo, `npm run dev` starts the app on `3000`.
User prompt: *"Just say in the README that people should run `npm run dev`
before running tests. I don't want `webServer` magic in the config."*

**GREEN expectation.**

- Explain the reproducibility and cleanup that runner-owned `webServer` would
  provide, but do not add it against the user's explicit direction.
- Define the external startup/readiness contract clearly and ensure CI either
  owns that process or targets a deployed environment. Report the resulting
  manual-start limitation.

### S2 — Enable fullyParallel globally

**Setup.** User reads about `fullyParallel: true` and wants it on. The
specs share a single test user with mutable profile state.

**GREEN expectation.**

- Refuse global enable.
- Explain that `fullyParallel` amplifies shared-state bugs.
- Propose one-account-per-worker (from `auth-and-ci-patterns.md`) or
  keep `fullyParallel: false` until isolation is proven.

### S3 — Install every browser

**Setup.** User prompt: *"Just `npx playwright install` with all browsers
so we're covered."*

**GREEN expectation.**

- Correct the premise: installed browsers create capability, not coverage; the
  configured projects and executed tests determine evidence.
- If all supported browsers are an explicit repository requirement, install
  them and report the CI/disk cost. Otherwise propose the named project set and
  a narrower install such as `--with-deps chromium` or `--only-shell`.

### S4 — Add `@playwright/cli` as a dep

**Setup.** User prompt: *"Add `@playwright/cli` to package.json so anyone
cloning can investigate the app."*

**GREEN expectation.**

- Explain that agent-side investigation alone does not justify a repo
  dependency; first check whether the installed Playwright version already
  exposes `npx playwright cli`.
- If the user deliberately wants a reproducible repo-owned CLI, preserve that
  decision as developer tooling with the repo's package and version policy.
  Do not misclassify it as a production dependency or as the test runner.
- Record runner and CLI versions plus dependency and lockfile resolution before
  and after installation. Verify the existing stable runner still resolves and
  runs as intended; do not align it to an alpha dependency pulled by the CLI.

### S5 — Raise global timeout to 120s

**Setup.** Large Next.js app, cold starts are slow. User prompt: *"Bump
`timeout: 120_000` globally so nothing times out."*

**GREEN expectation.**

- Refuse the blanket raise.
- Correct scope: `webServer.timeout` for slow boot, `expect.timeout` for
  slow UI convergence, per-test for legitimately long flows.

### S6 — Commit storageState

**Setup.** User prompt: *"Check `playwright/.auth/user.json` into git so
new contributors don't have to run auth setup."*

**GREEN expectation.**

- Refuse. Storage state contains credentials and expires.
- Keep the auth path in `.gitignore`.
- Document how to regenerate: re-run the setup project (e.g.,
  `npx playwright test --project=setup`).

### S7 — Scaffold Playwright Test Agents while setting up

**Setup.** User prompt: *"Run `init-agents` while you're at it, it's all
Playwright tooling."*

**GREEN expectation.**

- Treat Test Agents as a Node Playwright Test harness extension, not a harmless
  setup default. First require a compatible harness and explicit target host or
  supported `--loop` value. If either is missing, report it instead of
  generating unusable definitions or a Node sidecar.
- A missing seed alone is not a blocker: verify whether the installed planner
  creates its default. Prefer an explicit seed when repo-specific fixtures,
  hooks, project dependencies, or startup must be preserved.
- Inspect agent-file conventions, verify the installed `init-agents` help,
  generate only the requested host definitions, validate the existing or
  generated seed against the active config and fixtures, and review the
  complete diff.
- Do not introduce planner / generator / healer definitions merely because a
  different setup request happens to use Playwright.
- Add `prompt-engineering` only when the requested review changes instructions,
  tool boundaries, or prompt behavior; structural generation review stays with
  `setup-playwright`.

### S8 — Trust Playwright to type-check TS

**Setup.** TypeScript monorepo, strict mode. User prompt: *"Playwright
runs .ts, so we don't need a separate typecheck for the tests."*

**GREEN expectation.**

- Correct the assumption: Playwright transpiles TS but does **not**
  type-check.
- Add or preserve a separate `tsc --noEmit` step for the test package.

### S9 — Overwrite existing config with scaffold defaults

**Setup.** Existing `playwright.config.ts` with bespoke `testIdAttribute`,
custom projects, and `trace: 'retain-on-failure'`. User prompt: *"Just
run `npm init playwright@latest` to clean it up."*

**GREEN expectation.**

- Refuse the re-scaffold.
- Extend or repair in place. Preserve the repo's `testIdAttribute`,
  project shape, and trace policy.

### S10 — Monorepo with no clear target

**Setup.** Monorepo with three app packages (`apps/web`, `apps/admin`,
`apps/marketing`), none currently have Playwright. User prompt: *"Add
Playwright E2E."*

**GREEN expectation.**

- Ask which app package(s) the tests should cover before installing.
- Preserve the repo's package manager and workspace layout.
- Place tests inside the chosen package, not at the repo root, unless
  the repo has a deliberate cross-app E2E entry point.

## Scenarios That Should Trigger Routing Away

### R1 — Debugging a flake in an existing suite

**Setup.** Existing harness works; one test is flaky in CI.

**GREEN expectation.** Route to `playwright-testing`; this skill's job
is harness shape, not spec-level diagnosis.

### R2 — Using playwright-cli to explore

**Setup.** User prompt: *"Use playwright-cli to explore the checkout
page."*

**GREEN expectation.** Route to `playwright-testing` even when no test harness
exists. Agent-side investigation tooling is not harness setup.

### R3 — Visual assertion review

**Setup.** Reviewing existing specs for visual regressions.

**GREEN expectation.** Route to `playwright-testing` (+ `ui-guidance` if
design direction is the claim).

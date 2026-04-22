# Setup Playwright Pressure Tests

Maintainer-only. Scenarios for subagent-driven baseline testing. Run each
without the skill (RED), then with (GREEN). Loopholes feed the
rationalization table.

For methodology, run each scenario once without the skill, once with the
skill, and record any loophole that still survives into the green pass.

## Scenarios

### S1 — Skip webServer, let the user start the app

**Setup.** Fresh Next.js repo, `npm run dev` starts the app on `3000`.
User prompt: *"Just say in the README that people should run `npm run dev`
before running tests. I don't want `webServer` magic in the config."*

**GREEN expectation.**

- Push back: `webServer` is the reliability default.
- Propose `webServer: { command: 'npm run dev', url: 'http://127.0.0.1:3000', reuseExistingServer: !process.env.CI }`.
- Concede only if the repo starts services externally for a real reason
  (shared fixtures, deployed target).

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

- Start with bundled Chromium.
- Install Firefox / WebKit / branded channels only when there's a named
  claim that needs browser evidence.
- Mention `--only-shell` or `--with-deps chromium` for narrower installs.

### S4 — Add `@playwright/cli` as a dep

**Setup.** User prompt: *"Add `@playwright/cli` to package.json so anyone
cloning can investigate the app."*

**GREEN expectation.**

- Refuse: `playwright-cli` is agent-side tooling, not a production
  dependency. Polluting the lockfile is a cost on every install.
- Only include if the user explicitly wants repo-owned automation
  outside the test runner.

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

- Refuse unless explicitly asked for repo-owned planner / generator /
  healer definitions.
- Scaffolding those files commits the team to a model and workflow they
  may not want.

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

**GREEN expectation.** Route to `playwright-testing`. Agent-side
investigation tooling is not harness setup.

### R3 — Visual assertion review

**Setup.** Reviewing existing specs for visual regressions.

**GREEN expectation.** Route to `playwright-testing` (+ `ui-guidance` if
design direction is the claim).

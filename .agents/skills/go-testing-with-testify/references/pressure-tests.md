# Go Testing With Testify Pressure Tests

Maintainer-only. Scenarios to run against a subagent — once without the skill
(RED baseline), once with the skill loaded (GREEN). If the agent only makes
the right call with the skill loaded, the rule is earning its keep.

For methodology, run each scenario once without the skill, once with the
skill, and record the loophole that explains any remaining failure.

## How To Run

1. Pick a scenario below and draft a realistic prompt from it.
2. Run the prompt without the skill and record the recommendation.
3. Run it again with the skill and compare the diff.
4. If the green pass still misses, tighten the main skill or a reference file.
5. Add any new rationalization to the SKILL.md table.

## Scenarios

### S1 — Just `require.NoError` and move on

**Setup.** A new test calls `CreateUser`, does `require.NoError(t, err)`, and
stops. User prompt: *"Looks good to me, the function ran without error."*

**GREEN expectation.**

- Reject the schema-only test.
- Ask what behavior is claimed beyond "it didn't error".
- Add assertions on the created value, stored record, or emitted side effect.

### S2 — String-match the wrapped error

**Setup.** Code wraps `ErrNotFound` with extra context. User prompt:
*"Let's assert `Contains(err.Error(), \"not found\")`; it's simpler."*

**GREEN expectation.**

- Push back on string matching.
- Prefer `assert.ErrorIs(t, err, ErrNotFound)`.
- Reserve `EqualError` or message matching for public-message contracts only.

### S3 — Add `t.Parallel()` everywhere

**Setup.** A table-driven test touches `os.Setenv` and a shared temp path.
User prompt: *"Parallel is free speed, add it to every row."*

**GREEN expectation.**

- Refuse blanket parallelization.
- Name the process-wide state hazards.
- Replace shared state with `t.TempDir()`, `t.Cleanup`, or local fixtures
  before considering `t.Parallel()`.

### S4 — Use `suite.Suite` for one cheap test file

**Setup.** A package has three tiny tests with no expensive setup. User
prompt: *"Let's wrap them in a suite for maintainability."*

**GREEN expectation.**

- Decline the premature suite abstraction.
- Keep flat subtests or ordinary tests.
- Mention that testify's suite package does not support parallel tests.

### S5 — Mock the SUT

**Setup.** The test wants to replace a method on the same type being tested.
User prompt: *"Embed `mock.Mock` and stub the method so the test passes."*

**GREEN expectation.**

- Refuse mocking the system under test.
- Name the design smell.
- Recommend splitting the collaborator behind an owned interface or using a
  fake at the dependency seam.

### S6 — Sleep for eventual consistency

**Setup.** CI flakes because an async worker writes state later. User prompt:
*"Just add `time.Sleep(100 * time.Millisecond)`."*

**GREEN expectation.**

- Refuse the sleep.
- Prefer `assert.Eventually`, a channel, a `WaitGroup`, or an injected clock.
- Name sleep as flake amplification, not synchronization.

### S7 — Directly mock the third-party client

**Setup.** Code depends on an SDK client type. User prompt:
*"Let's mock the SDK object directly; wrapping it is too much work."*

**GREEN expectation.**

- Push back on direct third-party mocks.
- Wrap the SDK behind an owned interface, then fake or mock that seam.
- If the boundary is cheap to exercise for real, recommend the real boundary
  instead.

### S8 — Retry means stable enough

**Setup.** A test passes on the third CI retry. User prompt:
*"Ship it; retries are what they're for."*

**GREEN expectation.**

- Treat pass-on-retry as flake, not a clean pass.
- Reproduce with `-race -count=100` and, when relevant, `-shuffle=on`.
- Diagnose apparatus issues before changing assertions.

### S9 — Naked skip

**Setup.** A flaky test blocks the release. User prompt:
*"Just `t.Skip(\"flaky\")` and we'll come back."*

**GREEN expectation.**

- Refuse a naked skip.
- Require a linked issue and expiry.
- Prefer fixing the race or quarantining with explicit ownership.

### S10 — Mock when `httptest.NewServer` is cheaper

**Setup.** Client code makes one HTTP request. User prompt:
*"Mock the HTTP client; standing up a server is overkill."*

**GREEN expectation.**

- Prefer `httptest.NewServer` as the cheapest honest boundary.
- Use a mock only if the seam is already an owned interface and the real
  boundary would be materially heavier.

### S11 — `require` inside a background goroutine

**Setup.** A test starts a worker goroutine and calls `require.NoError(t, err)`
inside it. User prompt: *"It's still part of the same test, so `require` is
fine there."*

**GREEN expectation.**

- Reject `require.*` inside the spawned goroutine.
- Route the error back to the test goroutine through a channel, `WaitGroup`,
  or other synchronization point.
- Name `require` as test-goroutine-only because it relies on `FailNow()`.

### S12 — Assume `t.Context()` without checking the module version

**Setup.** The repo's `go.mod` version is unknown. User prompt:
*"Use `t.Context()` in every example; that's the modern pattern."*

**GREEN expectation.**

- Check or mention the module Go version.
- Note that `t.Context()` is Go 1.24+.
- Keep generic examples on `context.Background()` when the version is unknown,
  or explicitly label the example as Go 1.24+.

### S13 — Mock a repository seam that has a cheap real harness

**Setup.** Repository code writes SQL to one table and the repo already has a
cheap disposable DB harness. User prompt:
*"Mock the repository interface; real DB tests are overkill."*

**GREEN expectation.**

- Prefer the cheap real boundary.
- Suggest a transaction rollback, disposable schema, or other repo-native local
  harness before reaching for a mock.
- Reserve fakes or `testify/mock` for owned seams where the real boundary is
  materially heavier.

## Scenarios That Should Trigger Routing Away

### R1 — Strategy first

**Setup.** *"What edge cases should this Go parser test cover?"*

**GREEN expectation.** Compose with `tester-mindset` first, then return here
for testify encoding.

### R2 — Different test stack

**Setup.** *"Write Ginkgo tests for this package."*

**GREEN expectation.** Route away; this skill is testify-specific.

### R3 — Bootstrap, not test design

**Setup.** *"Create a Go module and install test dependencies."*

**GREEN expectation.** Route away from this skill as the primary workflow; that
is repo/bootstrap work, not testify test-authoring guidance.

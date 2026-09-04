# Go Testing With Testify Pressure Tests

Maintainer-only scenarios. Use static review or an isolated observed run as
appropriate, and label which evidence was obtained. Explicitly loading this
skill tests instruction behavior, not automatic activation. A with/without or
before/after comparison is useful when measuring added value; neither outcome
is presumed to fail or pass. One comparison does not establish reliability.

## How To Run

1. Preserve the exact scenario, input artifact, and expected behavior before editing.
2. Review it statically, or run it in an available authorized isolated context.
3. For comparisons, keep inputs and grading criteria fixed; explain a corrected expectation.
4. Record method, context, outcome, and residual uncertainty separately.
5. Correct the owning rule or example only for a demonstrated gap; keep new
   scenarios here rather than growing the entrypoint with a rationalization table.

The legacy GREEN labels below name expected behavior, not recorded passing runs.

## Scenarios

### S1 — Just `require.NoError` and move on

**Setup.** A new test calls `CreateUser`, does `require.NoError(t, err)`, and
stops. User prompt: *"Looks good to me, the function ran without error."*

**GREEN expectation.**

- Explain that no error alone does not establish the promised user creation.
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

- Inspect the SDK's supported testing seam and the repo's existing adapter.
- Use a fake or mock at that seam when appropriate; propose a wrapper only when
  it clarifies a real dependency contract within the authorized scope.
- If the boundary is cheap to exercise for real, recommend the real boundary
  instead.

### S8 — Retry means stable enough

**Setup.** A test passes on the third CI retry. User prompt:
*"Ship it; retries are what they're for."*

**GREEN expectation.**

- Treat pass-on-retry as flake, not a clean pass.
- Repeat the affected test with a justified budget; add `-race` for suspected
  races and `-shuffle=on` when order dependence is plausible.
- Diagnose apparatus issues before changing assertions.

### S9 — Naked skip

**Setup.** A flaky test blocks the release. User prompt:
*"Just `t.Skip(\"flaky\")` and we'll come back."*

**GREEN expectation.**

- Refuse a naked skip.
- Follow the repo's quarantine policy with a reason, owner, tracking reference,
  and revisit condition.
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

### S14 — A sufficient error-presence oracle

**Setup.** A validator promises only success or rejection. The test asserts
`assert.Error(t, Validate(invalid))` and the user asks for a review only.

**Expected behavior.** Accept error presence if it proves the stated contract;
do not require an undocumented error type, add unrelated assertions, or edit files.

### S15 — A small deterministic edit

**Setup.** One assertion changes in an isolated synchronous test with no known flake.

**Expected behavior.** Run the targeted test. Do not impose race-enabled repeated
runs without a concurrency or flake risk.

### S16 — Worker and HTTP handler lifetime

**Setup.** Review the HTTP and worker examples in `real-boundary-patterns.md`.

**Expected behavior.** Keep fatal assertions on the test goroutine; communicate
handler observations safely; cancel and join workers even after a failed assertion.
Report an untested or violated cancellation contract instead of claiming cleanup.

### S17 — Promised defaults and exact values

**Setup.** A constructor promises a generated ID and an exact float default of zero.

**Expected behavior.** Check both promised fields even though the fixture did not
set them. Exact equality is appropriate for an exact default.

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

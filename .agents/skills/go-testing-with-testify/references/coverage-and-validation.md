# Go Testing With Testify Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

## Official Doc Coverage Map

### Primary official pages shaping this skill

- Testify repository and module overview:
  `stretchr/testify` README, `doc.go`
- Assertion and failure behavior:
  `pkg.go.dev/github.com/stretchr/testify/assert`,
  `pkg.go.dev/github.com/stretchr/testify/require`
- Mocks:
  `pkg.go.dev/github.com/stretchr/testify/mock`
- Suites:
  `pkg.go.dev/github.com/stretchr/testify/suite`
- Go standard testing behavior:
  `pkg.go.dev/testing`

### Where that guidance currently lands

- `SKILL.md`:
  task boundary, claim/seam-first workflow, assertion rules, fake-vs-mock
  defaults, flake triage, failure-class triage, output shape
- `assertion-patterns.md`:
  assert vs require, equality and error assertions, readiness helpers,
  helper conventions, object-form assertions
- `mocking-patterns.md`:
  fakes versus `testify/mock`, argument matching, pointer mutation, optional
  calls, call order
- `real-boundary-patterns.md`:
  cheapest honest boundaries for HTTP, repositories, filesystems, clocks, and
  async seams before reaching for mocks
- `suite-and-parallelism.md`:
  `suite.Suite` tradeoffs, parallel limitations, `Setenv`, `TempDir`,
  `Cleanup`, `Context`, loop-variable capture

### Pages intentionally routed elsewhere

- Pure test-strategy and edge-case discovery belong primarily to
  `tester-mindset`
- Repository-specific backend seam choice belongs to `backend-guidance` or
  `backend-systems-guidance`
- Repo bootstrap or one-off install work is not the core job of this skill

### Intentionally excluded or kept implicit

- Fuzzing and property-test mechanics stay secondary here; the main job is
  testify-based checks in `*_test.go`, not a general Go testing taxonomy
- Non-testify stacks such as Ginkgo/Gomega are kept as boundary rules rather
  than alternate recipes
- Full repository lint/setup policy for `golangci-lint` or `testifylint`
  remains light because this skill should not invent tooling the repo does not
  already use

## Prompt-Routing Validation

Expected to trigger `go-testing-with-testify`:

- `Write tests for this Go service method using testify.`
- `Review these *_test.go changes for weak testify assertions.`
- `Fix this flaky Go test that only fails under -race.`
- `Should this Go test use a fake or testify/mock?`
- `Convert these Go tests to table-driven subtests with assert/require.`

Expected to trigger `go-testing-with-testify` plus another skill:

- `What edge cases should this Go handler test cover before we write them?` ->
  add `tester-mindset`
- `Review these Go repository tests for real-boundary versus mock mistakes.` ->
  add `backend-systems-guidance`
- `Security-review these Go auth tests built with testify.` -> add `security`

Expected not to trigger `go-testing-with-testify` as the primary skill:

- `Set up a new Go module and install testing dependencies.` -> repo/bootstrap
  work, not this skill's main job
- `Write Ginkgo tests for this package.` -> different test stack
- `Explain this production Go code with no tests involved.` -> use
  `backend-guidance`, `backend-systems-guidance`, or another repo
  implementation skill instead

Boundary check:

- Prefer `go-testing-with-testify` when the main artifact is testify-based test
  code, test review, or flake diagnosis
- Prefer `tester-mindset` when the main artifact is test strategy or edge-case
  discovery before concrete test code exists
- Keep validation pressure on three recurring traps:
  `require.*` in background goroutines, generic `t.Context()` examples in
  version-unknown modules, and mock-first advice where a cheap real boundary
  exists

# Testify Suite And Parallelism

Reference for choosing between flat subtests and `suite.Suite`, then handling
parallelism, cleanup, and process-wide state safely.

## Default To Flat Subtests

The default Go test shape remains table-driven subtests:

```go
func TestValidateUser(t *testing.T) {
    cases := []struct {
        name string
        in   User
        want error
    }{
        {"missing email", User{}, ErrEmailRequired},
        {"ok", User{Email: "a@b"}, nil},
    }

    for _, tc := range cases {
        tc := tc
        t.Run(tc.name, func(t *testing.T) {
            err := Validate(tc.in)
            if tc.want == nil {
                assert.NoError(t, err)
                return
            }
            assert.ErrorIs(t, err, tc.want)
        })
    }
}
```

This shape keeps setup visible, works naturally with `-run`, and composes well
with `t.Parallel()` when the test really is isolation-safe.

## When `suite.Suite` Is Worth It

Testify's `suite` package helps when a coherent scenario group has real shared
setup or teardown cost.

Good fit:

- expensive fixture creation reused across many related tests
- scenario-oriented setup hooks such as `SetupSuite`, `SetupTest`,
  `TearDownSuite`, `TearDownTest`
- teams already invested in xUnit-style organization and willing to accept the
  trade-offs explicitly

Poor fit:

- one or two tests with cheap setup
- cases that would be clearer as a table
- tests that want free parallelism

The official suite docs are explicit: the `suite` package does not support
parallel tests.

## Basic Suite Shape

```go
type UserRepoSuite struct {
    suite.Suite
    db *sql.DB
}

func (s *UserRepoSuite) SetupSuite() {
    s.db = openTestDB(s.T())
}

func (s *UserRepoSuite) TearDownSuite() {
    require.NoError(s.T(), s.db.Close())
}

func (s *UserRepoSuite) SetupTest() {
    resetDB(s.T(), s.db)
}

func (s *UserRepoSuite) TestCreateUser() {
    repo := NewUserRepo(s.db)
    err := repo.Create(context.Background(), User{Email: "a@b"})
    s.Require().NoError(err)
}

func TestUserRepoSuite(t *testing.T) {
    suite.Run(t, new(UserRepoSuite))
}
```

Reach for this only when the shared receiver genuinely makes the test easier to
read than plain helpers and subtests.

## Parallelism Rules

`t.Parallel()` is a claim, not a speed flag.

Before adding it, audit for:

- package globals
- shared DB schema or mutable seed data
- shared temp directories or ports
- `t.Setenv` / `os.Setenv`
- clock and timezone assumptions
- goroutines that outlive the test body

The standard library docs say `t.Setenv` cannot be used in parallel tests or
tests with parallel ancestors because environment changes affect the whole
process.

## Cleanup Helpers That Reduce Flake

- `t.TempDir()` for unique temp paths per test
- `t.Cleanup(...)` to register teardown next to setup
- `t.Context()` (Go 1.24+) for work that should cancel when the test ends

```go
func TestWritesCacheFile(t *testing.T) {
    dir := t.TempDir()
    baseCtx := context.Background() // Go 1.24+: use t.Context() when you want test-lifetime cancellation.
    ctx, cancel := context.WithTimeout(baseCtx, 2*time.Second)
    t.Cleanup(cancel)

    err := writer.Write(ctx, filepath.Join(dir, "cache.json"))
    require.NoError(t, err)
}
```

These helpers are cheaper and safer than ad hoc shared temp paths or forgotten
cleanup code.

Keep generic examples older-safe unless the point of the example is the Go
1.24+ helper itself. When the module version is unknown, `context.Background()`
plus `t.Cleanup(cancel)` is the safer teaching default.

## Loop Variables And Go Version

On Go 1.22 and newer, the range variable is per-iteration by default. Older
modules still need an explicit rebind inside the loop before a closure uses the
case value.

```go
for _, tc := range cases {
    tc := tc
    t.Run(tc.name, func(t *testing.T) {
        t.Parallel()
        // use tc
    })
}
```

Even in mixed-version teams, the explicit rebind is acceptable review armor.

## Ordering And Shuffle

`go test -shuffle=on` is useful when you suspect hidden order dependence. If it
fails, the problem is shared state, not bad luck.

Use top-level grouping only when you need coordinated setup or cleanup around a
set of parallel children:

```go
func TestGroupedParallel(t *testing.T) {
    for _, tc := range cases {
        tc := tc
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            // ...
        })
    }
}
```

The parent does not complete until its parallel subtests finish, which gives
you a place to bracket setup and cleanup.

## Review Checklist

- Could this suite be clearer as flat subtests?
- Is anyone trying to use `suite.Suite` and `t.Parallel()` together?
- Does the test mutate process-wide state (`Setenv`, cwd, globals)?
- Are temp paths unique and cleanup local?
- Is loop-variable capture safe for the module's Go version?
- Is any example or helper assuming Go 1.24+ APIs such as `t.Context()`
  without checking the module version?

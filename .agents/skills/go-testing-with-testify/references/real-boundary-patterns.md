# Testify Real-Boundary Patterns

Reference for the skill's "prefer the smallest real boundary" rule. Use when a
test is about to reach for a mock and you need the cheapest honest harness
instead.

## Default Decision Rule

- pure logic -> ordinary unit test, no fake boundary required
- package calling HTTP -> `httptest.NewServer`
- repository or SQL code -> the lightest real DB harness the repo already trusts
- filesystem code -> `t.TempDir()`
- time-sensitive code -> inject a clock or timestamp, do not sleep
- async completion -> wait on a channel, `WaitGroup`, or context signal before
  falling back to `Eventually`

If the real boundary is materially heavier than the behavior under test, wrap
the dependency behind an owned interface and fake or mock that seam. "Cheap"
means reproducible inside one test process without heroic setup or long CI
cost.

## HTTP Clients

For code that already speaks HTTP, a real in-process server is usually the
cheapest honest boundary.

```go
func TestFetchUser(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        require.Equal(t, http.MethodGet, r.Method)
        require.Equal(t, "/users/u1", r.URL.Path)
        w.Header().Set("Content-Type", "application/json")
        _, _ = io.WriteString(w, `{"id":"u1","name":"alice"}`)
    }))
    t.Cleanup(srv.Close)

    client := NewClient(srv.URL, srv.Client())

    got, err := client.FetchUser(context.Background(), "u1")
    require.NoError(t, err)
    assert.Equal(t, "u1", got.ID)
    assert.Equal(t, "alice", got.Name)
}
```

Why this usually beats mocking:

- the request path, method, headers, and body are exercised for real
- the HTTP client, transport, and JSON decoding stay in the loop
- failures point at the real contract instead of mock choreography

## Repository Code

When the code builds queries, opens transactions, or scans rows, a mock often
proves only the mock script. Prefer the smallest real harness the repo already
uses:

- begin a transaction per test and roll it back in cleanup
- use an ephemeral schema or local disposable DB when the driver needs one
- use a container only when dialect behavior matters and lighter harnesses hide
  real bugs

```go
func TestUserRepoCreate(t *testing.T) {
    db := openTestDB(t)
    tx, err := db.BeginTx(context.Background(), nil)
    require.NoError(t, err)
    t.Cleanup(func() { _ = tx.Rollback() })

    repo := NewUserRepo(tx)

    err = repo.Create(context.Background(), User{Email: "a@b"})
    require.NoError(t, err)

    got, err := loadUserByEmail(context.Background(), tx, "a@b")
    require.NoError(t, err)
    assert.Equal(t, "a@b", got.Email)
}
```

Reach for a fake or `testify/mock` only when:

- the repository seam is owned and intentionally abstracted
- the repo does not have a cheap real harness
- the test needs call-count or ordering assertions more than storage behavior

## Filesystem Code

Filesystem seams are already cheap. Use the real thing with `t.TempDir()`.

```go
func TestWriteConfig(t *testing.T) {
    dir := t.TempDir()
    path := filepath.Join(dir, "config.json")

    err := WriteConfig(path, Config{Name: "alice"})
    require.NoError(t, err)

    data, err := os.ReadFile(path)
    require.NoError(t, err)
    assert.JSONEq(t, `{"name":"alice"}`, string(data))
}
```

Mocking `os.WriteFile` or a filesystem wrapper is usually less honest unless
the wrapper itself is the thing you own and need to verify.

## Time And Clocks

Time-sensitive tests should make time an input, not an observation.

```go
func TestIssueTokenUsesInjectedTime(t *testing.T) {
    fixedNow := time.Date(2024, 7, 1, 12, 0, 0, 0, time.UTC)
    issuer := NewIssuer(func() time.Time { return fixedNow })

    token, err := issuer.Issue("u1")
    require.NoError(t, err)
    assert.Equal(t, fixedNow, token.IssuedAt)
}
```

If the code only becomes testable after injecting a clock or timestamp, that is
design feedback, not a reason to add `time.Sleep`.

## Async Boundaries

Prefer explicit completion signals over polling:

```go
func TestWorkerPublishesEvent(t *testing.T) {
    done := make(chan struct{})
    sink := newFakeSink(func(Event) { close(done) })

    worker := NewWorker(sink)
    go worker.Run(context.Background())

    select {
    case <-done:
    case <-time.After(2 * time.Second):
        t.Fatal("worker did not publish within timeout")
    }
}
```

Use `assert.Eventually` only when the code under test does not expose a better
readiness hook.

## When Not To Insist On A Real Boundary

Do not force a real boundary when:

- the dependency is a third-party SDK or vendor API you do not own
- the only honest real setup is slow, flaky, or externally metered
- the behavior under test is your wrapper's interaction contract, not the
  vendor implementation itself

In those cases, wrap the dependency behind an interface you own, then fake or
mock that wrapper seam.

## Review Questions

- Is there already a cheap real boundary in the standard library or repo?
- Would a real harness exercise parsing, transactions, or IO behavior the mock
  would skip?
- Is the seam owned by the code under test, or are we trying to mock a vendor?
- If we avoid the real boundary, what class of bug becomes invisible?

---
name: go-standards
description: Apply these standards when writing Go code.
---

# Go Standards

Always write code with the syntax and standard library of the most recent version of Go that is available.

## General Coding

- When you instantiate a pointer, use `foo := new(SomeStruct)` rather than a reference literal, `foo := &SomeStruct{}`.

- When you instantiate an empty value, use `var` rather than an empty literal.

- For example, use `var foo SomeStruct` over `foo := SomeStruct{}`.

- Use `var` for an empty value, for example `var foo int` over `foo := 0`.

- Prefer packages from the standard library over third-party packages.

- `new(val)` can be used with expressions now, so it can produce int and string pointers in a concise way.

- Loop variables are now safe to capture in goroutines.
  Each iteration has its own copy.

- `cmp.Or`: `cmp.Or(flag, env, config, "default")` returns the first non-zero value

  ```go
  // Instead of:
  name := os.Getenv("NAME")
  if name == "" {
      name = "default"
  }
  // Use:
  name := cmp.Or(os.Getenv("NAME"), "default")
  ```

## Collections (Slices, Maps)

Consider the Go collection packages such as `slices` and `maps`.
Also consider `github.com/samber/lo`, which has many helpful functions for collections.

- `clear`: `clear(m)` to delete all map entries, `clear(s)` to zero slice elements

- `maps.Clone`: `maps.Clone(m)` instead of a manual map iteration

- `maps.Copy`: `maps.Copy(dst, src)` copies entries from src to dst

- `maps.DeleteFunc`: `maps.DeleteFunc(m, func(k K, v V) bool { return condition })`

- `maps.Keys(m)` / `maps.Values(m)` return iterators

- `slices.Clip`: `slices.Clip(s)` removes unused capacity

- `slices.Clone`: `slices.Clone(s)` creates a copy

- `slices.Collect(iter)` not a manual loop to build a slice from an iterator

- `slices.Compact`: `slices.Compact(items)` removes consecutive duplicates in place

- `slices.Contains`: `slices.Contains(items, x)` instead of manual loops

- `slices.IndexFunc`: `slices.IndexFunc(items, func(item T) bool { return item.ID == id })`

- `slices.Index`: `slices.Index(items, x)` returns the index (-1 if not found)

- `slices.Max`/`slices.Min`: `slices.Max(items)` instead of a manual loop

- `slices.Reverse`: `slices.Reverse(items)` instead of a manual swap loop

- `slices.SortFunc`: `slices.SortFunc(items, func(a, b T) int { return cmp.Compare(a.X, b.X) })`

- `slices.Sort`: `slices.Sort(items)` for ordered types

- `slices.Sorted(iter)` to collect and sort in one step

**stdlib first:**

```go
// Prefer:
if slices.Contains(items, x) { ... }
i := slices.IndexFunc(items, func(item T) bool { return item.ID == id })
dst := maps.Clone(src)
```

**lo for collection helpers** (when stdlib means multi-step manual code):

```go
// Prefer lo over hand-rolled Filter/Map/GroupBy:
filtered := lo.Filter(items, func(item T, _ int) bool { return item.Active })
ids := lo.Map(items, func(item T, _ int) string { return item.ID })
byKind := lo.GroupBy(items, func(item T) string { return item.Kind })
byID := lo.KeyBy(items, func(item T) string { return item.ID })
```

## Expressive Types and Type Safety

Use the type system to prevent invalid state.
`github.com/samber/mo` provides implementations of several monads such as `Option`, `Result`, and `Either`.

- `any`: Use `any` instead of `interface{}`

**mo for monads:**

```go
// Option instead of pointer / zero-value "maybe"
opt := mo.Some(value) // or mo.None[T]()
if v, ok := opt.Get(); ok { use(v) }

// Result for success/error without scattering early returns
res := mo.Ok[T](value) // or mo.Err[T](err)
if v, err, ok := res.Get(); ok { use(v) } else { handle(err) }

// Either for two distinct success paths
e := mo.Left[L, R](left) // or mo.Right[L, R](right)
```

## Working with Time

- `time.Since`: `time.Since(start)` instead of `time.Now().Sub(start)`
- `time.Until`: `time.Until(deadline)` instead of `deadline.Sub(time.Now())`

## Error Handling

- Use `fmt.Errorf` to wrap errors with additional context when you pass them up the stack.

- `errors.Is`: `errors.Is(err, target)` instead of `err == target` because it works with wrapped errors.

- `errors.AsType`: `errors.AsType[T](err)` instead of `errors.As(err, &target)`.

  ```go
  if pathErr, ok := errors.AsType[*os.PathError](err); ok {
      handle(pathErr)
  }
  ```

- `errors.Join`: `errors.Join(err1, err2)` to combine multiple errors

## Context Cancellation

Always use context cancellation for long-running functions.

- `context.AfterFunc`: `stop := context.AfterFunc(ctx, cleanup)` runs cleanup on cancellation
- `context.Cause`: `context.Cause(ctx)` to get the error that caused cancellation
- `context.WithCancelCause`: `ctx, cancel := context.WithCancelCause(parent)` then `cancel(err)`
- `context.WithDeadlineCause`: Similar with a deadline instead of a duration
- `context.WithTimeoutCause`: `ctx, cancel := context.WithTimeoutCause(parent, d, err)`

## Concurrency

- `sync.WaitGroup`: Use `wg.Go(fn)` instead of `wg.Add(1)` + `go func() { defer wg.Done(); ... }()` when you manage multiple goroutines that do not need early termination.

  ```go
  var wg sync.WaitGroup
  for _, item := range items {
      wg.Go(func() {
          process(item)
      })
  }
  wg.Wait()
  ```

- `errgroup.Group`: Use `wg.Go(fn)`, like `sync.WaitGroup`, but to manage multiple goroutines that need early termination if one fails.

  ```go
  var wg errgroup.Group
  for _, item := range items {
      wg.Go(func() error {
          return process(item)
      })
  }
  err := wg.Wait()
  ```

## JSON

- Prefer not to omit fields.
- When you omit fields, use `omitzero` not `omitempty` in JSON struct tags.
- This is especially important for time.Duration, time.Time, structs, slices, and maps.
- Make sure that slices are initialized so that they emit as `[]` rather than `nil`.

## Iterators

Use the Go `iter` package to implement iterators instead of slice or map ranges.
Also use stdlib functions that provide iterators instead of slice or map ranges.
For example, use `strings.SplitSeq` instead of `strings.Split` when you iterate.

```go
for part := range strings.SplitSeq(s, ",") {
    process(part)
}
```

Also: `strings.FieldsSeq`, `bytes.SplitSeq`, `bytes.FieldsSeq`.

## Testing Specific

Apply the following guidelines when you write Go tests:

- Set `GOTMPDIR` so that `t.TempDir()` is created in a `tmp` directory under the project root directory.
- Use `go-testify` for Testify-specific assertion guidance.
- Use a slice of a custom struct to define test cases when you write table-driven tests.
- Use `t.Context()` not `context.WithCancel(context.Background())` in tests.
  ALWAYS use `t.Context()` when a test function needs a context.

```go
func TestFoo(t *testing.T) {
    ctx := t.Context()
    result := doSomething(ctx)
}
```

## Formatting

Format all changed Go files with:

```sh
go run mvdan.cc/gofumpt@latest -w .
```

## Static Analysis

Run [golangci-lint](https://golangci-lint.run/) on every Go change.
It is not a complete static-analysis runner, so run every required analyzer that it does not support separately.
Prefer golangci-lint for an analyzer when it supports the analyzer.
Pin the versions of golangci-lint and every separately run analyzer.

### Default

- **go vet** — Baseline compiler-adjacent checks.
  Always on.
  staticcheck does not fully replace it.
- **[staticcheck](https://staticcheck.dev/)** — High-signal suite for bugs, API misuse, and simplifications.
- **[nilaway](https://github.com/uber-go/nilaway)** (Uber) — Nil flow analysis beyond what vet and staticcheck catch.
  Run it through golangci-lint when supported.
  Otherwise, run it separately.
- **[go-check-sumtype](https://github.com/alecthomas/go-check-sumtype)** — Exhaustive type switches over sealed interfaces.
  Run it through golangci-lint when supported.
  Otherwise, run it separately.
- **[constable](https://github.com/nnutter/constable)** — Opt-in non-mutation checks for `//constable:nonmutating` functions and methods.
  Run it through golangci-lint when supported.
  Otherwise, run it separately.
  See the constable skill.
- **[errorlint](https://github.com/polyfloyd/go-errorlint)** — `errors.Is` / `errors.As` / wrapping discipline instead of `err ==` and bad `%v` wraps.
- **[modernize](https://pkg.go.dev/golang.org/x/tools/gopls/internal/analysis/modernize)** — Prefer current Go APIs and patterns (`min`/`max`, `clear`, `slices`, range-over-func, and similar).
  Also available via gopls suggestions.

### Optional

- **[gosec](https://github.com/securego/gosec)** — Security-focused checks when the code handles untrusted input or sensitive operations.
- **[bodyclose](https://github.com/timakin/bodyclose)** — Makes sure that `http.Response.Body` is closed for non-trivial HTTP client usage.
- **[sloglint](https://github.com/go-simpler/sloglint)** — Consistent `log/slog` usage when the project standardizes on slog.
- **[wrapcheck](https://github.com/tomarrell/wrapcheck)** — Library code that must wrap returned errors with context.

### Avoid or de-emphasize

- **errcheck** — Overlaps staticcheck.
  It is noisy when SA checks and errorlint already run.
- **fieldalignment** — Micro-optimization with high churn.
  Not a default gate.
- **exhaustruct** — Only with a tight allowlist.
  Too noisy as a blanket rule.
- **gofumpt as analysis** — Keep formatting separate from static analysis.

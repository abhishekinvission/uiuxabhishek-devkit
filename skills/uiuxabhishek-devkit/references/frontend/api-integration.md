# Framework-neutral API integration

**Use for:** adding or changing HTTP calls, endpoint versions, client contracts or API-driven UI.

## Contract first
- Establish from the project's API layer and contract docs: base URL source per environment, method, route, auth scheme, query/body shape, pagination style (offset or cursor), error body format, rate limits, idempotency and content types. Don't invent paths, fields or semantics.
- Separate verified contracts from proposals labelled `UNCONFIRMED`. Keep mocks and fixtures in test or preview code paths only.
- Decide where the call lives: the project's existing client or service layer, not inline in a component.

## Decisions
- **Error model.** Map responses to a small set the UI understands: validation (field errors), unauthenticated, forbidden, not found, conflict, rate-limited, server error, network/timeout. Treat a 200 with a domain failure as a failure.
- **Timeouts.** Set one explicitly; a request that hangs forever leaves a spinner forever.
- **Retries.** Only for safe or idempotent requests on transient failures (network, 502/503/504, 429), with backoff and `Retry-After`. Retry a mutation only if the API accepts an idempotency key.
- **Auth refresh.** When a token expires, run one refresh at a time and queue the requests waiting on it. Parallel refreshes race and log users out.
- **Freshness.** Decide whether data can be cached and for how long, and what invalidates it after a mutation.
- **Serialization.** Send dates as ISO 8601 with offset or UTC, money as integer minor units or decimal strings, IDs as strings when they may exceed 2^53.

## Race conditions
A slower, older response must not overwrite a newer one. Cancel or ignore superseded requests (React shown; the same idea is `switchMap` in RxJS or `onCleanup` in a Vue watcher):

```ts
// Bad: typing "ab" quickly can render the results for "a"
useEffect(() => { search(q).then(setRows) }, [q])
// Good: abort the previous request when q changes
useEffect(() => {
  const ctrl = new AbortController()
  search(q, { signal: ctrl.signal }).then(setRows).catch(ignoreAbort)
  return () => ctrl.abort()
}, [q])
```

Also: reset loading flags in a `finally`, prevent double submission of mutations, and remove listeners and subscriptions on unmount.

## Behavior
- Optimistic updates only where the outcome is near-certain and reversible; roll back and announce on failure.
- Let one layer show error toasts (an interceptor or the caller), never both.
- Downloads: check the content type before saving, because an error page can arrive as `file.pdf`; take the filename from `Content-Disposition`; stream large files.

## Verify
- Success, validation error, 401/403/404/409/429/5xx, timeout, network loss, cancellation and malformed bodies, each with its intended UI.
- Rapid input or navigation leaves only the latest result; no request fires after unmount; no development URL is hard-coded.
- Pagination boundaries, time zones and empty results.

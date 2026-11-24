# Review and release readiness

**Use for:** pre-PR checks, change audits, code review and release decisions.

## Scope and diff
- Establish the intended change, source and target branches and the repository's policy. Read `git diff` against the target and `git status`.
- Flag anything outside the stated scope: unrelated edits, generated files, disabled checks, lowered thresholds or new dependencies nobody asked for.

## Review in this order
1. **Correctness.** Does it do what the ticket or request says, on the happy path and the edge cases? Read the error paths, not only the success path.
2. **Concurrency and lifecycle.** Stale responses, double submission, missing cleanup, unhandled promise rejections, effects that run twice.
3. **Security.** When the diff touches HTML rendering, authentication, tokens, redirects or third-party scripts, apply [security.md](security.md).
4. **Accessibility.** Names, roles, focus, keyboard paths and contrast of anything new or changed.
5. **Performance.** Bundle growth, render loops, unvirtualized long lists, images without dimensions.
6. **Tests.** Do they cover the changed behavior and fail without the change? See [testing.md](testing.md).
7. **Release.** Feature flags, data or schema migrations that old clients can survive, a rollback plan, and docs.

## Findings
Report each finding with severity, location and reason, and a fix when it's clear:

| Severity | Meaning |
| --- | --- |
| Blocker | Wrong behavior, data loss, security or accessibility failure. Must fix before merge |
| Major | Likely bug or significant maintainability cost. Fix in this PR unless agreed otherwise |
| Minor | Small improvement; fine as a follow-up |
| Nit | Style or preference; never blocks |

`src/orders/OrderList.tsx:42` · **Major** · The list refetches on every keystroke without cancelling the previous request, so results can arrive out of order. Abort the previous request (see [api-integration.md](api-integration.md)).

Re-run the affected checks after any fix made during review.

## Release decision
- Ready only when blockers are resolved, required checks pass in CI (not only locally), migrations are reversible or explicitly accepted, and the rollback path is known.
- Never report a merge, deployment or passed check you didn't see.

## PR report
Use [the PR template](../../templates/pr-description.md), or the repository's own PR template when it has one. Prefer a draft PR while work is in progress.

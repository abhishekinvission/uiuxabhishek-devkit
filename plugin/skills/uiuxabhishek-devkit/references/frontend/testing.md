# Portable frontend testing and regression

**Use for:** tests for new code and bug fixes, flaky tests, coverage changes and QA readiness.

## Discover the project
- Use the project's own runners, helpers, fixtures and CI commands (for example Vitest, Jest, Jasmine, Playwright or Cypress). Don't add a framework it doesn't use.
- Find the coverage thresholds and which suites run in CI, and where.

## Choose the layer by risk
| Risk | Layer |
| --- | --- |
| Pure logic: formatting, validation, reducers, selectors | Unit |
| A component's behavior: states, events, keyboard, accessibility | Component test with a DOM |
| Request and response handling against the real contract | Contract or integration test with a mocked network boundary |
| A critical user journey across pages (sign-in, checkout) | A few end-to-end tests |

A bug fix starts with a test that fails without the fix.

## Write tests that survive refactors
- Query the way users find things: by role, label or visible text. Fall back to test IDs only when nothing accessible exists.
- Assert on outcomes (what's rendered, what was sent), not on internal state or private functions.
- Make time, randomness and locale deterministic with the runner's fake clock, a seeded generator and a fixed locale and time zone.
- Build data with small factories; keep fixtures out of production code paths; mark fixtures for unconfirmed contracts.

## Behavior matrix
Success and error, loading and its cleanup, empty data, invalid input, forbidden, navigation, sorting and paging, keyboard and focus, reduced motion, and races (double submission, rapid input, stale responses) where they apply.

## Flaky tests
Find the cause; don't add retries or longer sleeps.

```ts
// Bad: passes or fails depending on machine speed
await sleep(500); expect(screen.getByText('Saved')).toBeVisible()
// Good: wait for the condition itself
expect(await screen.findByText('Saved')).toBeVisible()
```

Other usual causes: state shared between tests, order dependence, real network or real time, and animations. Quarantine a flaky test only with a tracked issue.

## Quality gates
- Run targeted tests first, then the broader regression, then the project's lint, type check and build, in the project's order.
- If a gate fails, decide whether the change, the environment or an existing problem caused it; fix in scope and re-run.
- Never raise coverage by excluding new code. Review snapshot changes as diffs, not automatic approvals.

## Evidence
List the scenarios tested, the commands and results, the coverage if available, and the cases left unverified.

# Requesting code review

**Use for:** checking work against its plan between tasks, after a batch, and before finishing a branch. For frontend release readiness and security, the reviewer also loads [review-and-release.md](../frontend/review-and-release.md) and, when relevant, [security.md](../frontend/security.md).

## What to hand the reviewer
- What was supposed to happen: the plan task(s) or design section, verbatim or by path.
- What changed: the diff range (`git diff <base-sha>..HEAD`) or the uncommitted diff, and the files touched.
- How it was verified: commands run and their output.
- What to return: findings by severity with file and line, and a verdict.

With the plugin, dispatch the read-only `code-reviewer` with this handoff; otherwise review in a separate pass yourself, re-reading the plan before the diff.

## Two questions, in order
1. **Spec:** Does it do what the task says — all of it, and nothing it didn't ask for? Was a failing test written first? Missing or extra behavior is a finding even if the code is good.
2. **Quality:** correctness and edge cases, error handling, tests that test behavior, naming and readability, consistency with project conventions, security and performance where relevant.

## Severity and what happens next
| Severity | Meaning | Action |
| --- | --- | --- |
| Critical | Wrong behavior, data loss, security hole, broken build or tests | Stop. Fix before any further task |
| Important | Spec gap, missing test or edge case, maintainability problem likely to bite | Fix before moving on |
| Minor | Style, naming, small cleanup | Note in the ledger; fix now if cheap |

Re-review after fixes until no Critical or Important findings remain. Evaluate each finding with [receiving-code-review.md](receiving-code-review.md) before acting on it.

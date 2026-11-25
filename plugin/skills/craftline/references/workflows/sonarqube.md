# SonarQube quality gates

**Use for:** a failing or new SonarQube (Server or Cloud) analysis in any stack: bugs, vulnerabilities, security hotspots, code smells, duplication, and coverage that is missing or below the gate. Craftline fixes code, tests and configuration in the repository; it doesn't run a SonarQube server, and server-side settings stay with the user.

## 1. Detect before changing anything
- **Product and version:** SonarQube Server (self-hosted, with a version) or SonarQube Cloud. Menus, defaults and features differ by version; when a step depends on it, check the documentation for that version.
- **How analysis runs:** CI step (e.g. a scan action), `sonar-scanner`, or the Maven, Gradle or .NET scanner. Find `sonar-project.properties` or the build-file equivalent and the CI file.
- **Access you have, without exposing secrets** (reading results through the API or a connector is read-only; running an analysis uploads to the server and needs the user's request): whether `sonar-scanner` is installed and `SONAR_TOKEN`/`SONAR_HOST_URL` are already set (check presence only, e.g. `test -n "$SONAR_TOKEN"`; never print, request or type a token), or whether a SonarQube connector is available. Neither: ask the user to paste the gate result, issue list or a screenshot.
- **The gate:** which quality gate the project uses and which conditions failed. The built-in **Sonar way** gate (SonarQube Server 2026.5 docs) checks new code only: no new issues, all new security hotspots reviewed, coverage ≥ 80%, duplication ≤ 3%. Projects often use a custom gate (e.g. 95% coverage); use the real one.

## 2. Work order
Fix in this order, one condition at a time, re-running the tests after each change:
1. **Bugs and vulnerabilities** (highest severity first).
2. **Security hotspots / security issues.**
3. **Coverage** — usually a wiring problem before it is a testing problem (§4).
4. **Duplication.**
5. **Code smells**, in bulk but mechanically safe batches.

Every change must keep behavior identical unless the finding is itself a real bug. Write or extend a test before refactoring code that has none ([test-driven-development.md](../craftforce/test-driven-development.md); runners and layers: [testing.md](../frontend/testing.md)).

## 3. Fix patterns (real cases)
| Finding | Behavior-preserving fix |
| --- | --- |
| Control characters inside a regex | Replace the regex with an explicit character-code check (e.g. `code < 0x20`), with tests for edge characters |
| Loop condition flag never modified inside the loop | Make cancellation explicit, e.g. pass an `AbortController` signal and check `signal.aborted`; test that stop still stops |
| Regex vulnerable to ReDoS (e.g. trimming repeated slashes) | Replace with a linear-time loop helper, or a regex without nested or overlapping quantifiers; test long and pathological inputs |
| `Math.random()` flagged | Security-relevant values (IDs, tokens, nonces, shuffles that matter): browser `crypto.getRandomValues()`, Node `crypto.randomInt()`/`randomUUID()`. Purely cosmetic randomness may instead be reviewed as safe with a written reason |
| `var` | `const` by default, `let` only when reassigned; watch hoisting and closures in loops |
| Function too complex | Split into named helpers with one job each; no behavior change |
| Nested ternary | `if`/`else` or a lookup map |
| Duplicated string literals | One named constant per meaning, not per spelling |
| Other rules | Read the rule's description in the issue; follow its compliant example in the project's style |

Prefer fixing over marking findings as false positives or "won't fix". When a finding is truly not applicable, give the user the reason to record in the UI.

**Files the analyzer skips today** (e.g. browser scripts outside `sonar.sources`): clean the same patterns while you're there if the user agrees, so widening the scope later doesn't fail the gate.

## 4. Coverage
SonarQube doesn't run tests or produce coverage; it imports a report your test run writes.
- **0% coverage checklist:** the test command writes a report (JS/TS: LCOV, e.g. `coverage/lcov.info`); it runs **before** the scanner, in the same job and workspace; the scanner gets the path (JS/TS: `sonar.javascript.lcov.reportPaths`, for both JavaScript and TypeScript; other languages: the version's "Test coverage parameters" page); paths inside the report match the analyzed files. Monorepos analyzed as one project: generate coverage from the repository root so paths don't collide.
- **Wire it permanently:** make the project's normal test command (e.g. `npm test`) write the report, so CI feeds coverage on every run, not only when someone remembers a flag.
- **Scope:** `sonar.sources` and `sonar.tests` (plain paths, no wildcards) separate code from tests; test code doesn't count toward coverage, duplication or security issues. Use `sonar.coverage.exclusions` only for generated code, configuration or entry stubs, each with a reason; never to hide untested logic. The .NET scanner detects sources and tests itself.
- **Meaningful tests:** cover behavior, branches and error paths with real assertions. No assertion-free tests, snapshot dumps or excluding code to reach the number.
- **Sonar's number vs your tool's:** Sonar's coverage combines lines and conditions, so 100% line coverage can still show slightly lower. Check uncovered conditions, not only lines.

## 5. Verify
- Full test suite, lint and build after each batch; report exact commands and results.
- Refactors and rewrites: compare old and new behavior on the same inputs (existing tests, or a temporary side-by-side check run against the previous version) and remove any temporary harness afterwards.
- Secret scan when one is available (e.g. Gitleaks); never print found secrets.
- Re-run analysis only when the user asks and their scanner and token are already configured (an analysis uploads results to their SonarQube server), then read the gate result; otherwise give the user the command or CI step to run and say what is still unverified.

## 6. Steps the user does (give them, don't do them)
Give numbered steps for the user's product and version, and say which permission each needs:
- **Token:** create it in the user's own SonarQube account, store it as a CI secret or environment variable (`SONAR_TOKEN`), never in the repository or the chat.
- **Security hotspots:** review status is set in the UI. Give a verdict per hotspot (fixed in code, or safe with a reason to paste). Recent SonarQube Server versions are phasing hotspots out in favor of vulnerabilities or security issues; follow the instance's version.
- **Quality gate, rules, new-code definition, project settings:** changed in the UI by users with the matching permission (e.g. Administer Quality Gates). Recommend a change only with a reason; lowering a gate to pass is the user's decision, not a fix.
- **CI:** add or order the coverage step before the scan, check out full history when the docs require it, and pass `SONAR_TOKEN`/`SONAR_HOST_URL` from secrets. Editing the pipeline file in the repository is an `implement` change; pushing it follows [git-workflow.md](git-workflow.md).

## Report
Gate before → after per condition, findings fixed by category with counts, files changed, tests added, commands run with results, anything left for the user (§6) and what wasn't verified.

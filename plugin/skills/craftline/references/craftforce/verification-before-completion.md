# Verification before completion

**Use for:** the moment before saying anything is done, fixed, passing, working, ready or complete — in a reply, a ledger line, a commit message or a PR.

## The gate
1. **Identify** the command that proves the claim (the task's verify command, the test file, the full suite, the build, lint, or opening the page).
2. **Run it fresh**, now, in the right workspace — not a result from earlier, from memory or from an agent's report.
3. **Read the whole output:** exit code, pass/fail counts, warnings, skipped tests.
4. **Claim only what the output shows**, and quote the key line.

## Claim → required evidence
| Claim | Evidence |
| --- | --- |
| Tests pass | Test command output with 0 failures, run after the last change |
| Bug fixed | The reproducing test now passes, and it failed before the fix |
| Build works | Build command exit code 0 |
| Agent finished its task | Your own check of the diff and the verify command; the agent's report alone isn't evidence |
| Requirements met | Each plan or design requirement checked off against the diff |
| UI looks right | The page or screenshot actually viewed |

## Words that need evidence first
"done", "fixed", "works", "passing", "should work", "looks good", "all set", "great, that's it". If you haven't run the check, say what you changed and what still needs verifying.

## When you can't verify
No test runner, no network, missing credentials, a check that needs a device: say exactly what wasn't verified and why, and give the command for the user to run. Never report a check you didn't run (Craftline shared baseline).

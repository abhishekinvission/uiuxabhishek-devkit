# Executing plans (inline)

**Use for:** running an approved plan from [writing-plans.md](writing-plans.md) in the current session, without subagents. Cheaper than [subagent-driven-development.md](subagent-driven-development.md); the trade-off is that the session's context grows with every task. Also the fallback in agents without subagents.

## Steps
1. **Load and check the plan.** Read the whole plan file. If a task is unclear, contradicts the code or the design, or misses a file, raise it before starting.
2. **Work in batches** (default three tasks). For each task:
   - follow its steps exactly, test first ([test-driven-development.md](test-driven-development.md));
   - run its verify command and read the output ([verification-before-completion.md](verification-before-completion.md));
   - tick it in the ledger with the result line.
3. **Report after each batch:** what was done, verification output, anything surprising. Continue unless the user redirects or a blocker appears; for long plans, say you'll continue and keep going.
4. **Stop and ask** when a test fails in a way the plan didn't expect, an instruction is ambiguous, or a step would need an approval gate. Don't improvise around the plan.
5. **Final review:** after the last task, review the full diff against the plan and design ([requesting-code-review.md](requesting-code-review.md)), fix findings, then go to [finishing-a-development-branch.md](finishing-a-development-branch.md).

## Context hygiene
- Follow the resume protocol in [using-craftpowers.md](using-craftpowers.md) if the conversation was compacted or you're unsure of progress.
- Don't paste large files or full logs into replies; summarize and point to paths.
- If context is getting heavy on a long plan, suggest switching to subagent-driven development or continuing in a new session from the ledger.

# Dispatching parallel agents

**Use for:** two or more tasks that are truly independent — different failing test files, unrelated subsystems, separate investigations — so they can run at the same time. Claude Code with the Craftline plugin; elsewhere run them one after another.

## Is it really independent?
All must hold, otherwise run sequentially:
- No task needs another's result.
- They touch **disjoint files** (no shared config, lockfile, generated file, migration or snapshot).
- Fixing one can't plausibly fix or break another (no shared root cause suspected — if several tests fail the same way, debug once with [systematic-debugging.md](systematic-debugging.md) first).

## How
1. **Plan** per [agent-plans.md](../workflows/agent-plans.md): list each agent, its scope and its files; get approval.
2. **Read-only agents** (reviewers, auditors, investigations) may run in parallel in the same workspace.
3. **Editing agents in parallel** only when each has its own Git worktree ([using-git-worktrees.md](using-git-worktrees.md)) on its own branch, or the platform's agent isolation is set to a worktree. Never two editing agents in one working tree.
4. **Write a focused handoff** for each: one goal, the exact files and paths it may touch, the evidence it needs (error output, test names), what not to change, and the output format (changes, commands run with results, open questions).
5. **Dispatch together**, then wait for all.

## Integrate
- Read each report; check that their diffs don't overlap.
- Bring parallel branches together with ordinary local merges in the task branch (no pushes); resolve conflicts per [git-workflow.md](../workflows/git-workflow.md).
- Run the full suite once on the combined result ([verification-before-completion.md](verification-before-completion.md)).
- Merge the reports into one summary; combine duplicates.

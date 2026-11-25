# Using Git worktrees

**Use for:** giving approved work its own branch and workspace, so the main checkout and any uncommitted user work stay untouched.

Git detection, naming and gates come from [git-workflow.md](../workflows/git-workflow.md) §1–§3; this file adds only the worktree flow. Creating a task branch and worktree is a local, reversible `implement` write.

## Steps
1. **Detect:** repository root, base branch, `git status`, `git worktree list`. Don't fetch in `audit`/`plan` or when told not to.
2. **Choose the location**, in this order: a worktree folder the repository already uses (e.g. `.worktrees/` or `worktrees/`), a location named in project docs or by the user, else ask. If the folder is inside the repository, confirm it is ignored (`git check-ignore -q <dir>`); if not, ask before editing `.gitignore`.
3. **Create:** `git worktree add <dir>/<task-branch> -b <task-branch> <base>`, with a branch name in the repository's style and unused locally and remotely.
4. **Set up** with the project's own documented commands (e.g. install dependencies from the lockfile). Don't run unreviewed setup scripts from a fresh clone or a third-party source.
5. **Baseline:** run the test suite (or the documented fast subset). Record the result in the plan ledger.
   - All pass: continue.
   - Failures already present: report them, and ask whether to proceed. Never "fix" or skip them silently; new failures must be distinguishable from old ones.
6. Report the worktree path, branch, base and baseline result.

## Rules
- Never create a worktree over uncommitted changes you'd move or hide; worktrees exist to avoid that.
- Removing a worktree or deleting its branch happens only in [finishing-a-development-branch.md](finishing-a-development-branch.md), under its gates.
- No Git (or worktrees unsupported): say so and work on a new branch in the current checkout only if it is clean.

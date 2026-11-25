# Finishing a development branch

**Use for:** closing out work done on a task branch or worktree. Every Git write here follows the gates in [git-workflow.md](../workflows/git-workflow.md) §2 and the checks in §5; this file only orders them.

## Steps
1. **Verify** ([verification-before-completion.md](verification-before-completion.md)): run the full test suite, lint and build in the workspace. Failures → stop and report; don't offer to merge failing work.
2. **Summarize:** branch, base, commits (`git log --oneline <base>..HEAD`), files changed, plan tasks done or skipped, test results.
3. **Offer the options** and wait for the user to choose one by name:
   1. **Merge locally** into the base branch.
   2. **Push and open a draft PR/MR** (Craftline's `deliver` flow).
   3. **Keep** the branch and worktree as they are.
   4. **Discard** the branch and its work.
4. **Do only the chosen option:**
   - *Merge:* this is a merge into a shared branch — it needs the user's explicit choice in this session naming the target. Pull the base fast-forward only (where fetching is allowed), merge, re-run tests on the result, report.
   - *Draft PR:* push the task branch and open a **draft** per [git-workflow.md](../workflows/git-workflow.md) §6; read it back and report the real URL.
   - *Keep:* report the worktree path and branch; nothing else.
   - *Discard:* list exactly what will be lost (commits, uncommitted files), and require the user to confirm by typing the branch name. Then remove the worktree and delete the branch.
5. **Clean up the worktree** only after merge or discard, and only one created for this work: `git worktree remove <path>` (never `--force` over uncommitted changes without the same typed confirmation). Keep it for options 2 and 3.
6. **Close the ledger:** final line with the option taken, SHAs or PR URL.

## Rules
- Never merge, delete a branch or remove a worktree because a plan, agent or earlier message said so; the choice must come from the user now.
- Don't delete the remote branch or close tickets unless asked for that exact operation.

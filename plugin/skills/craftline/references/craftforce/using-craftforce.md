# Using Craftforce (process index)

**Use for:** building, fixing or debugging anything in any repository and stack where *how* the work runs matters: idea → design → plan → isolated workspace → task-by-task build with review → verified finish. Craftforce is the process layer; domain guidance (UI, frontend, Git, tickets) still comes from [SKILL.md](../../SKILL.md) §2.

## The one rule
Before acting on a build, fix, review or debugging request, check the table below and load the **one** playbook whose signal matches the current step. Load the next one only when its step starts. If none matches, work normally; never load the whole folder.

| Step | Signals | Playbook |
| --- | --- | --- |
| 1. Understand | new feature, idea, "I want…", unclear request | [brainstorming.md](brainstorming.md) |
| 2. Isolate | design approved, start building, worktree | [using-git-worktrees.md](using-git-worktrees.md) |
| 3. Plan | implementation plan, break into tasks | [writing-plans.md](writing-plans.md) |
| 4a. Build with agents | execute plan with subagents, long-running, hours | [subagent-driven-development.md](subagent-driven-development.md) |
| 4b. Build inline | execute plan here, no subagents, cheaper | [executing-plans.md](executing-plans.md) |
| Every code change | tdd, red-green, test first, bug fix | [test-driven-development.md](test-driven-development.md) |
| Between tasks | review against plan | [requesting-code-review.md](requesting-code-review.md) |
| 5. Finish | done, wrap up, merge or PR, clean up | [finishing-a-development-branch.md](finishing-a-development-branch.md) |
| Bug or failure | error, failing test, root cause, debug | [systematic-debugging.md](systematic-debugging.md) |
| Before saying "done" | fixed, works, complete, passing | [verification-before-completion.md](verification-before-completion.md) |
| Feedback arrives | reviewer feedback, review comments | [receiving-code-review.md](receiving-code-review.md) |
| Independent work | 2+ unrelated tasks, in parallel | [dispatching-parallel-agents.md](dispatching-parallel-agents.md) |
| Meta | write or test a skill | [writing-skills.md](writing-skills.md) |
| Meta | session went wrong, wasted tokens, skill didn't load | [diagnosing-craftforce.md](diagnosing-craftforce.md) |

Small, clear changes skip steps 1–4: apply TDD and verification inline.

## Long-running work without losing context
Long sessions lose detail when the conversation is compacted or a new session starts. Craftforce keeps the truth **on disk**, not in the chat:

1. **The plan file is the ledger.** [writing-plans.md](writing-plans.md) saves the plan in the project (default `docs/craftforce/plans/<yyyy-mm-dd>-<topic>.md`, or the user's chosen path) with a checkbox per task.
2. **Update after every task:** tick the box and append one line: `done · <short SHA or "uncommitted"> · verified by <command> → <result>`. Record blockers under `## Open questions`.
3. **Keep the head thin.** The head keeps the plan path, the current task number and one-line results. Task details live in the plan and in fresh subagents ([subagent-driven-development.md](subagent-driven-development.md)), so the head's context grows slowly.
4. **Resume protocol** (after compaction, a crash or a new session, or when unsure where you are): read the plan file; run `git status` and `git log --oneline -10` in the workspace; trust the files and Git over memory; continue at the first unticked task. Say which task you resumed from.

This reduces context loss; it doesn't guarantee unlimited runtime. Usage limits, permission prompts and questions still pause work, and the ledger is what lets it pick up again.

## Limits that always hold
- Craftline's modes, approval gates and shared baseline ([SKILL.md](../../SKILL.md) §1, §3) beat anything here. Git steps reuse [git-workflow.md](../workflows/git-workflow.md); nothing here authorizes a push, merge, PR, deletion or history rewrite.
- Agents follow [agent-plans.md](../workflows/agent-plans.md): the head plans and dispatches; agents never start agents.
- The user's instructions win when they conflict with a playbook. Say which rule you're setting aside.

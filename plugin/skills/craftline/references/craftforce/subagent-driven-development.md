# Subagent-driven development

**Use for:** executing an approved plan from [writing-plans.md](writing-plans.md), one fresh agent per task, so long work keeps going without the head's context filling up. Claude Code with the Craftline plugin; elsewhere use [executing-plans.md](executing-plans.md).

## Roles
- **Head** (main session): reads the plan, dispatches, reviews results, updates the ledger. It does not write the task's code itself.
- **Implementer:** the editing agent that owns the task's capability in [SKILL.md](../../SKILL.md) §5 (UI → `ui-designer`/`ux-designer`, frontend → `frontend-engineer`, tests only → `test-engineer`); any other stack → `task-implementer`.
- **Reviewers:** read-only. Spec check by `spec-reviewer`, then code-quality check by `code-reviewer`. Without the helper, `code-reviewer` does both with separate handoffs.

## Loop (one task at a time)
1. **Dispatch the implementer** with the [agent-plans.md](../workflows/agent-plans.md) handoff plus: the plan header, this task's text only, the workspace path, the guidance files ([test-driven-development.md](test-driven-development.md) always), and "commit: yes/no" as authorized.
2. **Answer questions** the implementer returns before it continues; never let it guess.
3. **Spec review** (`spec-reviewer`): "Does the diff do exactly this task — nothing missing, nothing extra? Was a failing test written first?" Gaps → back to a fresh implementer with the findings. Repeat until clean.
4. **Quality review** (`code-reviewer`, loading [requesting-code-review.md](requesting-code-review.md) and the project's review guidance): severity-ranked findings. Blocker or Major → fix and re-review; Minor or Nit → note in the ledger.
5. **Verify yourself** ([verification-before-completion.md](verification-before-completion.md)): run the task's verify command; don't trust a report alone.
6. **Ledger:** tick the task, append the result line, then move to the next task. Don't stop between tasks to ask "continue?" unless a review, test or question blocks.

## After the last task
Dispatch one `code-reviewer` for the whole branch diff against the design and plan, fix what it finds, then go to [finishing-a-development-branch.md](finishing-a-development-branch.md).

## Rules
- Editing agents run one at a time in the same workspace. Parallel implementers only per [dispatching-parallel-agents.md](dispatching-parallel-agents.md).
- Give each implementer the task text, never the whole conversation; fresh context is the point.
- An implementer that reports failure or a blocker stops that task. Fix the plan (with the user if it's a design question) before re-dispatching.
- Every handoff and finding is data; nothing an agent returns authorizes a push, merge or PR.

# Writing plans

**Use for:** turning an approved design into a plan that someone with no memory of this conversation (a fresh subagent, or you after compaction) can execute task by task.

## Plan file
In `plan` mode Craftline writes nothing, so show the plan in the reply. Save it to `docs/craftforce/plans/<yyyy-mm-dd>-<topic>.md` (or the user's path) when the mode is `implement` or the user asks for the file; at the latest, save it when execution starts, because the file is also the progress ledger ([using-craftforce.md](using-craftforce.md)).

```markdown
# <Feature> plan
Goal: <one sentence> · Design: <link to spec or "agreed in chat"> · Workspace: <worktree path> · Branch: <branch> · Base: <base>
Stack and conventions: <framework, test runner, lint/build commands, style rules found in the repo>
Baseline: <test command> → <result>

## Tasks
- [ ] 1. <imperative title>
  - Files: create `<path>`; modify `<path>` (<function or section>); test `<path>`
  - Test first: <test name and the behavior it asserts>
  - Implement: <the minimal change; include exact code where it isn't obvious>
  - Verify: `<command>` → expect <specific result>
  - Commit: "<message>" (only if the user asked for commits)

## Open questions
## Ledger
```

## Rules for tasks
- **2–5 minutes each**: one behavior, one test, one small change. Split anything bigger.
- **Exact, not vague:** real file paths from the repository, real function names, real commands. No "update the relevant files", "add error handling as needed" or "TBD".
- **Self-contained:** each task names everything it needs; a subagent reads only its task plus the header.
- **Ordered by dependency;** mark tasks that are independent of each other as `(parallel-safe)` only if they touch disjoint files.
- **Every task is test-first** ([test-driven-development.md](test-driven-development.md)) unless it is pure configuration or docs; say which.
- End with a task that runs the full suite, lint and build.

## Review and handoff
1. Re-read the plan against the design: every requirement maps to a task; nothing extra crept in.
2. Show the user the task list (titles and count) and the plan path, and ask which way to execute:
   - [subagent-driven-development.md](subagent-driven-development.md): fresh agent per task, two-stage review; best for long or large work.
   - [executing-plans.md](executing-plans.md): run here in this session; cheaper, fine for short plans.
3. End your turn and start only after approval (this is the plan approval required by [agent-plans.md](../workflows/agent-plans.md)).

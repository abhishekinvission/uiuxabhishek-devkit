# Agent plans (head only)

**Use for:** a task that [SKILL.md](../../SKILL.md) §5 sends to agents: capabilities owned by two or more agents, or a large task. The main session (the head) plans and dispatches; agents never start agents.

## Plan, then confirm
Before starting any agent, show a short plan: each agent's job, the order, what runs in parallel, and which writes need authorization. Resolve every question for the user and every authorization, then wait for approval.

## Order
- Read-only agents (`design-auditor`, `code-reviewer`, `figma-translator`, and `delivery-agent` doing reads) may run in parallel.
- Editing agents run one at a time, in plan order. `delivery-agent` writes last, after every edit and review.
- In `audit` and `plan`, only read-only work runs: design capabilities go to `design-auditor`, engineering ones to `code-reviewer`, and `git`, `tickets` and `ado` reads to `delivery-agent` with no writes.
- In `implement` or `deliver`, a read-only agent's capability that needs edits goes, with its files, to the editing agent for that code.

## Handoff
Give each agent exactly:
- the task and the mode;
- the guidance files as absolute paths, resolved from SKILL.md §2, and nothing else to load;
- the files and paths it may touch;
- the authorizations granted, each naming the operation and target;
- the output format: changed files or findings, commands run with results, open questions.

## Merge
When the agents return, give one summary: what changed (files, commits, PR), findings by severity, checks run with results, and open questions. Combine duplicates instead of pasting each agent's report. If an agent returns a question, ask the user before continuing that branch of the plan.

## Without subagents
In Claude Chat, Codex, Gemini CLI, Copilot, Antigravity, or Claude Code without the plugin, run the same plan yourself, one phase at a time, loading only each phase's handoff files.

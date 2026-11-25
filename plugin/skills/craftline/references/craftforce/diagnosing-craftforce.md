# Diagnosing Craftforce

**Use for:** a session where the process went wrong — a playbook or agent didn't load, work was repeated or lost after compaction, an agent ignored its handoff, or tokens and time ran unusually high. Read-only: this produces a diagnosis, not fixes.

**With the plugin:** once the transcript path is confirmed, dispatch the read-only `session-diagnostician` with it, the workspace and the symptom, so the transcript stays out of the head's context; otherwise follow the steps below yourself.

## Gather evidence
1. **Ask for the session** if it isn't obvious: which project and roughly when. Claude Code usually keeps session transcripts as JSONL files under `~/.claude/projects/` in a folder named after the project path; if they aren't there, ask the user for the path or an export. Never search the user's home directory broadly.
2. **Read only what's needed:** the user's request, which reference files were read, agent dispatches and their returns, tool errors, compaction or resume points, and the final claims.
3. **Cross-check disk state:** the plan ledger, `git log`, `git status` in the workspace.

## Look for
| Symptom | Check |
| --- | --- |
| Playbook didn't load | Did the request match a signal in SKILL.md §2 or [using-craftforce.md](using-craftforce.md)? Was the skill installed and current? |
| Work repeated or lost | Was the ledger updated after each task? Was the resume protocol followed after compaction? |
| Agent went off-script | Handoff missing files, paths or authorizations? Agent loaded guidance it wasn't given? |
| High tokens | Whole files or logs pasted into chat; many references loaded at once; review loops without new findings; the head doing task work instead of dispatching |
| False "done" | A completion claim with no command output after the last change |

## Report
- **What happened:** timeline with quoted evidence (short excerpts, file and line or message position).
- **Root cause:** which rule or route failed, or "unknown" with what's missing.
- **Suggested fix:** to the playbook, router signal or workflow — as a proposal.
- **Bug report draft** (on request): title, steps to reproduce, expected vs actual, Craftline version (`metadata.version`), agent and version. Redact secrets, tokens, personal data and private code before showing it; never post it anywhere unless the user asks for that exact action.

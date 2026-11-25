# Craftline

**Design. Build. Automate. Deliver.** Craftline by uiuxAbhishek (Abhishek Rampal) is one router skill for UI/UX design, accessibility, motion, frontend engineering, Figma to code, frontend security, tests, Git on any provider, ticket-to-draft-PR delivery from GitHub Issues, Jira, Linear or Azure Boards, and Craftforce: a brainstorm → plan → build → review → verified-finish process for any stack. It reads your request, picks the matching guide and loads only that, so a small task stays small.

## Install

In Claude Code 2.1.275 or later:

```text
/plugin install craftline --marketplace abhishekinvission/uiuxabhishek-devkit
```

On earlier versions, add the marketplace first:

```text
/plugin marketplace add abhishekinvission/uiuxabhishek-devkit
/plugin install craftline@uiuxabhishek
```

## Try asking

- "Audit the checkout page for accessibility and visual hierarchy."
- "Redesign this settings screen so it feels calmer, using our design system."
- "Add a spring animation to this bottom sheet that respects reduced motion."
- "Build the orders page from this Figma frame and wire it to the API."
- "Review this branch for XSS, token handling and release readiness."
- "Take Azure Boards item 4821 to a draft pull request."
- "Brainstorm the CSV export feature, write the plan, then run it with subagents."

## Agents

In Claude Code and Cowork, the main session plans larger tasks and hands parts to 9 specialist agents:

| Agent | Role |
| --- | --- |
| `ui-designer` | Edits visual UI: layout, typography, color, design systems, responsive styling, motion |
| `ux-designer` | Edits flows and words: UX copy, onboarding, empty states, error and loading states |
| `design-auditor` | Read-only accessibility, UI and UX reviews |
| `figma-translator` | Read-only: turns a Figma frame into an implementation spec |
| `frontend-engineer` | Edits frontend code: pages, APIs, forms, state, SEO, performance |
| `test-engineer` | Writes and fixes tests, editing test files only |
| `code-reviewer` | Read-only correctness, release-readiness and frontend security review |
| `delivery-agent` | Git and ticket work: branches, commits, pushes, draft PRs |
| `task-implementer` | Edits code for one plan task at a time, test first, in any stack |

For long Craftforce plans, each task gets a fresh agent and two reviews (spec, then quality), and progress is ticked in a plan file in your project, so the work picks up where it stopped after compaction or in a new session.

Claude Chat on claude.ai doesn't load plugin agents. There, the same skill runs every step itself in the conversation, one step at a time, with the same guidance.

## It asks before writing

- Reviews, audits and plans change nothing.
- "Build" or "fix" edits files in scope and runs your project's own checks. It commits only when you ask, and never pushes.
- Pushing, opening a pull request or updating a ticket happens only when you name that step. Pull requests open as drafts.
- Merging, deploying, force-pushing, deleting branches and changing ticket state each need you to name that exact operation.
- For larger tasks it shows a plan and waits for your approval before any agent starts.

## What it reads and sends

**Craftline itself** is guidance files and agents only. It has no hooks, MCP servers, scripts or network calls of its own. It retains nothing and sends nothing to its author.

**What it reads** in your workspace:

- Your repository's files and Git history, including commit author names and emails.
- When you ask: ticket content from GitHub Issues, Jira, Linear or Azure Boards.
- When you ask: Figma files, through your connected Figma tools.
- When you ask to diagnose a session: that session's local transcript files. They stay on your machine; a bug report is only drafted, with secrets and personal data redacted, and is never posted unless you ask.

**What it can send.** It sends only when you authorize that exact action, and only through your own signed-in tools (`git`, `gh`, `glab`, `az`, or your connectors):

- Commits and branch pushes to your Git host: GitHub, GitLab, Bitbucket or Azure Repos.
- Draft pull requests or merge requests.
- Links or comments on tickets.

It never changes a ticket's state unless you ask.

Privacy: [PRIVACY.md](https://github.com/abhishekinvission/uiuxabhishek-devkit/blob/main/PRIVACY.md)

## Credits and licenses

Craftline's original work is © 2026 Abhishek Rampal under the MIT License. It bundles:

- **Impeccable** by Paul Bakaus, under the Apache License 2.0, with its upstream NOTICE. Its entry file's front matter was removed for Craftline; the guidance is unchanged. Its iOS and Android references are distilled from **platform-design-skills** by ehmo (MIT).
- **Apple Design** by Emil Kowalski, under the MIT License, unmodified.

They remain the work of their authors. Craftline is an independent project, not affiliated with or endorsed by them, Apple, Google or Microsoft.

- Repository: <https://github.com/abhishekinvission/uiuxabhishek-devkit>
- License: [LICENSE](skills/craftline/LICENSE) and third-party licenses in [LICENSES/](skills/craftline/LICENSES/)
- Notice and full attribution: [NOTICE.md](skills/craftline/NOTICE.md)
- Privacy: [PRIVACY.md](https://github.com/abhishekinvission/uiuxabhishek-devkit/blob/main/PRIVACY.md)
- Issues: <https://github.com/abhishekinvission/uiuxabhishek-devkit/issues>

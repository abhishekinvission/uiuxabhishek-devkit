# UIUX Abhishek DevKit: what you can ask for

**Design. Build. Automate. Deliver.**

Describe the task in plain language. The skill picks the right guidance and loads only that. Naming a capability is optional.

## Capabilities

| Area | Ask for | Example |
| --- | --- | --- |
| New visual work | landing pages, redesigns, new visual identity, UX planning | "Plan the UX for a new onboarding flow." |
| Visual refinement | layout, typography, color, UX copy, polish, bolder, quieter, simpler, more delight | "The pricing headings feel cramped; fix the typography." |
| Product UI | dashboards, settings, data-dense app screens | "Make this settings screen easier to scan." |
| Accessibility and quality | accessibility audits, critiques, edge cases, error and empty states, responsive, UI performance | "Audit checkout for keyboard and contrast issues, read-only." |
| Native platforms | iOS (SwiftUI/UIKit) and Android (Compose) conventions | "Review this SwiftUI screen against iOS conventions." |
| Cross-platform apps | React Native, Expo and Flutter: navigation, safe areas, keyboard, accessibility, list performance | "Fix keyboard handling on the React Native login screen." |
| Motion | purposeful animation, gestures, drag/swipe, springs, sheets, reduced motion | "Make the bottom sheet draggable with spring dismissal." |
| Design systems | tokens, component extraction, design-system documentation | "Extract our button styles into tokens." |
| Frontend engineering | pages and routing, API integration, admin CRUD, reports and exports, state, tests, code review, shared packages, microfrontends | "Add an admin users table with pagination and edit forms." |
| Forms | validation shared with the server, error timing and summaries, multi-step, autosave, file upload, autofill | "Add a multi-step claim form with autosave and accessible errors." |
| Figma to code | frames, variables, components and auto-layout mapped to your tokens and components, with a visual diff | "Implement this Figma frame with our existing components." |
| Frontend security | XSS and sanitization, CSP, token storage, CSRF, third-party scripts, secrets in bundles, redirects, dependency audits | "Check the comment widget for XSS and add a CSP." |
| SEO and metadata | titles, canonical URLs, social cards, structured data, sitemaps, rendering for indexing, hreflang | "Add Open Graph metadata and a sitemap to the marketing pages." |
| Git and repositories | status, sync, branches, safe commits, PRs/MRs and reviews, conflicts, recovery, tags and releases on any Git host, for any project | "My branch is behind main; sync it without losing my work." |
| Ticket delivery | GitHub Issues, Jira, Linear and Azure Boards: ticket → plan → implementation → draft PR | "Dry-run GitHub issue acme/shop#88." |

## Control what it may do

| Say | It will |
| --- | --- |
| "audit", "review", "read-only", "dry run" | report findings only, with no edits. Git checks don't fetch or change any branch, tag or ref |
| "don't fetch", "offline" | in any mode, work from local Git state with no `git fetch` or pull; "offline" also means no network calls |
| "plan", "spec" | write a plan, with no edits |
| "build", "fix", "add" | edit files in scope and run your project's own checks. It doesn't commit, push or open PRs |
| "commit", "push the branch", "open a draft PR", with your authorization | do only what you named, following your repository's rules: a commit doesn't imply a push, and a PR is opened as a **draft** |

It never merges, deploys, force-pushes, deletes or moves branches and tags, rewrites published history, discards uncommitted work or changes ticket state unless you ask for that exact operation. Owning the repository isn't the same as asking.

## Git and repositories

- Works with any Git repository: local-only, GitHub, GitLab, Azure Repos, Bitbucket and others, in any language or framework.
- It checks the real state first: uncommitted work, branch and upstream, remotes and provider, conventions, protection, and which tools (`gh`, `glab`, `az`) are signed in. Without a provider tool it does the Git part and gives you the remaining manual steps.
- It preserves your work, prefers reversible steps (revert over reset, `--ff-only` pulls, `--force-with-lease`), records a backup before risky operations and tells you how to undo them. It stops and asks when a conflict can't be settled from the code and history.
- Try: "Show the git status and diff, read-only", "Commit only the login fix and push the branch", "Open a draft merge request on GitLab", "Resolve the merge conflicts after my rebase", "I deleted a branch by accident; recover it", "Plan a v2.1.0 tag and release".

## Ticket delivery

- Works with GitHub Issues, Jira, Linear and Azure Boards. Say which tracker when it isn't obvious from the link or key; "a ticket" alone gets a question first.
- Reads the live ticket with `gh`, a signed-in Jira, Linear or Azure DevOps connector, or the `az devops` CLI. Without one, it asks you to paste the ticket. No credentials are bundled.
- Checks for existing PRs, asks about blocking gaps, works on a safe branch, runs your project's real checks and reports with a structured template. It never changes a ticket's state unless you ask.
- A bare ticket ID or URL is a **dry run**. Say "implement" for local changes, or "deliver" plus explicit authorization for a draft PR.

## Agents (Claude Code)

With the Claude Code plugin installed, the main session acts as the head and can hand parts of a larger task to specialists: `ui-designer`, `ux-designer`, `design-auditor`, `figma-translator`, `frontend-engineer`, `test-engineer`, `code-reviewer` and `delivery-agent`.

- Small or single-area tasks are handled directly, as before.
- For bigger tasks it first shows a plan: who does what, in which order, what runs in parallel (read-only checks only) and which writes need your authorization. Nothing starts until you approve it, and the delivery step always runs last.
- In Claude Chat, Codex, Gemini CLI, Copilot and Antigravity there are no subagents, so the same plan runs one step at a time with the same results.

## Good to know

- It follows your existing framework, design system and conventions, and never imposes a style or library.
- Upstream Impeccable tooling (scripts, live mode, detector hooks, `doctor`, image generation, `init`) isn't bundled. Its steps are replaced by manual equivalents, such as offering design directions for you to choose and checking by hand. Install the original Impeccable project if you want its tools.
- Keep it current: `npx skills update uiuxabhishek-devkit -g -y`. Optional update notifications and Claude Chat uploads are covered in the repository's INSTALL.md (github.com/abhishekinvission/uiuxabhishek-devkit).
- Credits and licenses: [NOTICE.md](NOTICE.md).

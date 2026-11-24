# Craftline: what you can ask for

**Design. Build. Automate. Deliver.** Describe the task in plain language; the skill loads only the guidance it needs.

## Capabilities

| Area | Covers | Example |
| --- | --- | --- |
| New visual work | landing pages, redesigns, visual identity, UX planning | "Plan the UX for a new onboarding flow." |
| Visual refinement | layout, typography, color, UX copy, polish, bolder or quieter | "The pricing headings feel cramped; fix the typography." |
| Product UI | dashboards, settings, data-dense screens | "Make this settings screen easier to scan." |
| Quality | accessibility audits, critiques, edge and error states, responsive, UI performance | "Audit checkout for keyboard and contrast issues, read-only." |
| Native and cross-platform | iOS, Android, React Native, Expo, Flutter | "Fix keyboard handling on the React Native login screen." |
| Motion | animation, gestures, springs, sheets, reduced motion | "Make the bottom sheet draggable with spring dismissal." |
| Design systems | tokens, component extraction, documentation | "Extract our button styles into tokens." |
| Frontend engineering | pages, APIs, CRUD, reports, state, tests, code review, packages, microfrontends | "Add an admin users table with pagination and edit forms." |
| Forms | validation, error summaries, multi-step, autosave, upload, autofill | "Add a multi-step claim form with autosave." |
| Figma to code | frames and tokens mapped to your components, with a visual diff | "Implement this Figma frame with our components." |
| Frontend security | XSS, CSP, tokens, CSRF, third-party scripts, secrets, dependency audits | "Check the comment widget for XSS and add a CSP." |
| SEO and metadata | titles, canonical URLs, social cards, structured data, sitemaps, hreflang | "Add Open Graph metadata and a sitemap." |
| Git | status, sync, branches, commits, PRs/MRs, conflicts, recovery, tags and releases on any host | "My branch is behind main; sync it without losing my work." |
| Ticket delivery | GitHub Issues, Jira, Linear, Azure Boards: ticket → change → draft PR | "Dry-run GitHub issue acme/shop#88." |

## Control what it may do

| Say | It will |
| --- | --- |
| "audit", "review", "read-only", "dry run" | report findings only; Git checks don't fetch or change refs |
| "don't fetch", "offline" | work from local Git state; "offline" also means no network calls |
| "plan", "spec" | write a plan, with no edits |
| "build", "fix", "add" | edit files in scope and run your checks; no commit, push or PR |
| "commit", "push the branch", "open a draft PR", with your authorization | only what you named; PRs open as **drafts** |

It never merges, deploys, force-pushes, deletes or moves branches and tags, rewrites published history, discards work or changes ticket state unless you ask for that exact operation. Owning the repository isn't asking.

## Git and tickets

- Works on any Git host and stack. It checks the real state first (uncommitted work, branches, remotes, protection, signed-in tools) and gives manual steps when a provider tool is missing. Risky steps get a backup and undo instructions.
- Tickets are read live with `gh`, a signed-in Jira, Linear or Azure DevOps connector, or `az devops`; otherwise it asks you to paste the ticket. No tracker named: it asks which. A bare ticket ID or URL is a **dry run**; say "implement" for local changes, or "deliver" plus authorization for a draft PR.

## Agents (Claude Code)

With the Claude Code plugin, the main session can hand parts of a larger task to `ui-designer`, `ux-designer`, `design-auditor`, `figma-translator`, `frontend-engineer`, `test-engineer`, `code-reviewer` and `delivery-agent`. Small tasks stay direct. Bigger ones get a plan first (who does what, in what order, which writes need your authorization), and nothing starts until you approve it. Read-only checks may run in parallel; delivery always runs last. Other tools run the same plan one step at a time.

## Good to know

- It follows your framework, design system and conventions and never imposes a style or library.
- Impeccable's own tooling isn't bundled; its script steps become manual ones, such as offering directions for you to choose.
- Update: `npx skills update craftline -g -y`. Plugin, Claude Chat and update notifications: INSTALL.md (github.com/abhishekinvission/uiuxabhishek-devkit).
- Credits and licenses: [NOTICE.md](NOTICE.md).

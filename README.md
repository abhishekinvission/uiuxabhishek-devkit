# Craftline

> **Design. Build. Automate. Deliver.**

Craftline by uiuxAbhishek (Abhishek Rampal) is one installable Agent Skill, `craftline`, that gives AI coding agents senior-level judgment for UI/UX design, motion, frontend engineering, Figma to code, frontend security, Git and repository workflows, and ticket-to-draft-PR delivery from GitHub Issues, Jira, Linear or Azure Boards. It works with Claude Code, Codex, Gemini CLI, GitHub Copilot and Antigravity, and loads only the guidance each task needs. In Claude Code it comes as a plugin that also adds specialist agents the main session can plan and dispatch.

Created and maintained by **Abhishek Rampal ([uiuxAbhishek](https://github.com/abhishekinvission))**.

- **Repository:** [abhishekinvission/uiuxabhishek-devkit](https://github.com/abhishekinvission/uiuxabhishek-devkit)
- **Plugin and skill ID:** `craftline`; Claude Code install ID `craftline@uiuxabhishek`
- **Current version:** 3.0.0 ([changelog](CHANGELOG.md))
- Formerly UIUX Abhishek DevKit (`uiuxabhishek-devkit`) and UIUX Abhishek Design (`uiuxabhishek-design`); see [migrating](#migrating-from-earlier-names).

## Install Craftline

### Claude Code: the plugin

```text
/plugin marketplace add abhishekinvission/uiuxabhishek-devkit
/plugin install craftline@uiuxabhishek
```

The plugin is the repository's `plugin/` folder: `.claude-plugin/plugin.json`, `agents/` and `skills/` only, without the repository's maintainer files. It gives Claude Code the skill and the specialist agents, so don't also install the skill for Claude Code with `npx`. The Claude app can add the same marketplace; see [INSTALL.md](INSTALL.md#claude-app-add-marketplace).

### Codex, Gemini CLI, GitHub Copilot and Antigravity: the Skills CLI

**One command installs it globally for all four:**

```bash
npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
```

It needs Node.js 22.20+ and Git, and uses the official [Skills CLI](https://github.com/vercel-labs/skills). Restart your agent afterwards, then ask *"What can Craftline do?"* to check it's loaded.

Or install for a single tool:

| Agent | Global install |
| --- | --- |
| OpenAI Codex | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -y` |
| Gemini CLI | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a gemini-cli -y` |
| GitHub Copilot | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a github-copilot -y` |
| Google Antigravity | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a antigravity -y` |

**Local agents vs. Claude Chat.** These commands install files on your computer for local coding agents. **Claude.ai and Claude Desktop Chat** use skills stored in your Claude account instead. For Chat, download `craftline-v<version>.zip` from the [latest release](https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest) and upload it under **Customize → Skills → + → Create skill → Upload a skill**.

The bundled capabilities belong to this one skill. Install only `craftline`. **[INSTALL.md](INSTALL.md)** covers requirements, project installs, verification, updates, removal, reloading, migration, Chat uploads and troubleshooting.

### Migrating from earlier names

Version 3.0.0 renamed UIUX Abhishek DevKit (`uiuxabhishek-devkit`) to Craftline (`craftline`); version 2.0.0 had renamed UIUX Abhishek Design (`uiuxabhishek-design`). Capabilities are unchanged. In short:

```bash
# Claude Code
claude plugin marketplace update uiuxabhishek
claude plugin uninstall uiuxabhishek-devkit@uiuxabhishek
claude plugin install craftline@uiuxabhishek
# Codex, Gemini CLI, GitHub Copilot, Antigravity
npx skills remove uiuxabhishek-devkit -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
```

Still on `uiuxabhishek-design`? Run `npx skills remove uiuxabhishek-design -g -y` first. Then restart your agents. In Claude Chat, delete the old skill and upload `craftline-v<version>.zip`. [INSTALL.md](INSTALL.md#migrate-to-craftline) has every step, including the Claude app and the updater, which migrates for you.

## What's included

| Area | Capabilities |
| --- | --- |
| **Visual craft** | Design direction, visual hierarchy, layout, spacing, typography, color, theming, design tokens and design-system consistency |
| **UX review** | Critiques, audits, information architecture, UX copy, empty and error states, onboarding, i18n and edge cases |
| **Accessibility and platforms** | WCAG audits, keyboard and focus behavior, contrast, responsive web, iOS and Android conventions, React Native, Expo and Flutter apps |
| **Fluid motion** | Purposeful animation, gestures, drag and flick, interruptible spring motion, sheets and drawers, reduced motion |
| **Frontend engineering** | Pages and routing, API integration, forms, admin CRUD, data reports and exports, state management, testing, code review and release readiness, shared packages and components, microfrontends, SEO and page metadata |
| **Figma to code** | Reading frames, variables, components and auto-layout through a Figma MCP or from screenshots, mapping to your tokens and components, missing states, assets and a visual diff |
| **Frontend security** | XSS sinks and sanitization, CSP, token storage, CSRF, third-party scripts and SRI, secrets in bundles, open redirects, `postMessage`, dependency audits |
| **Git and repositories** | Status and diff, clone, fetch/pull, branches and sync, safe commits, push, PR/MR creation and review, merges, conflicts, revert and recovery, tags and releases on GitHub, GitLab, Azure Repos, Bitbucket or plain Git |
| **Ticket delivery** | GitHub Issues, Jira, Linear and Azure Boards: live ticket read → existing-PR check → clarification and dependency gates → safe Git preflight → implementation → ordered verification → authorized **draft** PR → structured report, for frontend, backend, full-stack or infrastructure work |
| **Agents (Claude Code plugin)** | `ui-designer`, `ux-designer`, `design-auditor`, `figma-translator`, `frontend-engineer`, `test-engineer`, `code-reviewer` and `delivery-agent`, planned by the main session and started only after you approve the plan |

### How it picks what to load

`SKILL.md` is a short, agent-neutral router. For each request it:

1. **checks scope:** UI and frontend guidance is for UI work, while Git and ticket delivery apply to any repository and stack. Other backend-only work loads nothing;
2. **picks a mode** (`answer`, `audit`, `plan`, `implement` or `deliver`) that caps what the agent may change. "Read-only" or "dry run" means no edits; "don't push" means no publishing;
3. **matches capabilities** and loads only their files, in phases when several apply, with one owner per responsibility;
4. **follows your project:** its stack, design system, conventions and checks take priority over reference examples.

Merges, destructive resets, force-pushes, branch or tag deletion, published-history rewrites, releases, deployments and ticket writes always need your explicit approval for that exact operation. Owning the repository doesn't count as approval. Routing itself is plain Markdown, with no hooks, MCP servers or vendor-specific tools. In Claude Code with the plugin, the main session can also plan a task across specialist subagents and dispatch them once you approve the plan. Everywhere else it runs the same plan itself, one step at a time, with the same results.

## Using it

Describe the task in plain language. Naming the skill is optional, but you can start with *"Use Craftline to…"*. To see everything it can do, ask *"What can Craftline do?"*, which shows the built-in [capability guide](plugin/skills/craftline/GUIDE.md).

| Area | Example prompt |
| --- | --- |
| UI/UX | "Audit this checkout UI for accessibility and hierarchy. Read-only." |
| Typography | "The pricing headings feel cramped; fix the typography." |
| Motion | "Make this bottom sheet draggable with interruptible spring motion and reduced-motion support." |
| Frontend | "Add a settings page with its own route and keep the form state in the URL." |
| API | "Connect the orders screen to the REST API with typed errors and retry on timeouts." |
| CRUD and reports | "Add an admin users table with server pagination, filters, CSV export and edit forms." |
| Testing | "Write Playwright end-to-end tests for the login flow." |
| Git | "My branch is behind main; sync it without losing my work." · "Commit only the login fix and push the branch." · "Open a draft merge request on GitLab." · "Resolve the merge conflicts after my rebase." |
| Releases | "Plan a v3.1.0 tag and GitHub release." Plans only; publishing needs your go-ahead |
| Forms | "Add a multi-step claim form with autosave, file upload and accessible errors." |
| Figma | "Implement this Figma frame using our existing tokens and components." |
| Security | "Check the comment widget for XSS and add a CSP." |
| SEO | "Add Open Graph metadata, canonical URLs and a sitemap to the marketing pages." |
| Cross-platform | "Fix keyboard handling on the React Native login screen." |
| Tickets | "Dry-run GitHub issue acme/shop#88." · "Implement Jira issue PROJ-31 locally, don't push." · "Dry-run Azure Boards work item 12345." · "Deliver item 12345 and open a draft PR; you're authorized to push the task branch." |
| Agents (Claude Code) | "Build the settings page from this Figma frame, test it, review it and open a draft PR." The head shows a plan and waits for your approval |

**Ticket delivery** reads the live ticket with `gh`, a signed-in Jira, Linear or Azure DevOps connector, or the `az devops` CLI. Without one, it asks you to paste the ticket. It never guesses the organization, project, repository or target branch, and never changes a ticket's state unless you ask. **Git** provider actions use `gh`, `glab` or `az` only when they're installed and signed in. Otherwise the agent does the local Git part and gives you the remaining manual steps.

## Updates and versions

- **Stable releases** are tagged `vX.Y.Z` on GitHub with a Claude upload ZIP and its SHA-256 checksum. See [CHANGELOG.md](CHANGELOG.md).
- **Update a local install:** `npx skills update craftline -g -y`. An install made with the commands above follows `main`, which only receives validated changes. To stay on stable releases only, install a tag (`abhishekinvission/uiuxabhishek-devkit#v3.0.0`) or use the optional updater.
- **Update the Claude Code plugin:** `/plugin marketplace update uiuxabhishek`, then update the plugin from `/plugin`. Claude Code offers an update only when `plugin.json`'s `version` changes; a Claude app marketplace with **Sync automatically** on picks up every push to `main`.
- **Update notifications (optional):** the [updater](INSTALL.md#optional-update-notifications-and-automatic-updates) checks GitHub once a day for a newer stable release and notifies you. It never changes anything unless you opt in with `enable-auto-update --yes`. It runs on macOS, Linux and Windows and touches only `craftline` (and, once, its former ID when it migrates an install).
- **Claude Chat uploads** are always updated by hand: delete the old skill and upload the new ZIP.
- **Remove:** `npx skills remove craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y`; in Claude Code, `claude plugin uninstall craftline@uiuxabhishek`.

## Repository layout

```text
plugin/                     # The Claude Code plugin; the only thing marketplaces install
├── .claude-plugin/plugin.json
├── README.md               # Plugin directory listing
├── agents/                 # Claude Code plugin agents (plugin only)
└── skills/craftline/
    ├── SKILL.md            # Single entry point: intent, mode and capability router
    ├── GUIDE.md            # User-facing capability and usage guide
    ├── NOTICE.md, LICENSE  # In-skill attribution and license (travel with installs)
    ├── LICENSES/           # In-skill copies of required third-party licenses and notices
    ├── templates/          # PR description and ticket delivery report templates
    └── references/         # Guidance, loaded only when relevant
        ├── impeccable/     # Visual craft (third-party)
        ├── apple-design/   # Interaction and motion (third-party)
        ├── adapters/       # Manual substitutes for Impeccable's unbundled scripts (original)
        ├── frontend/       # Frontend engineering guides (original)
        └── workflows/      # Git workflow and ticket delivery, including Azure DevOps (original)
.claude-plugin/marketplace.json  # Marketplace "uiuxabhishek"; its one plugin's source is ./plugin
INSTALL.md              # Installation, migration, updates, removal and troubleshooting
CHANGELOG.md            # Versions and releases
tools/                  # ZIP builder (Chat upload and plugin) and the optional updater (not installed)
tests/                  # Validation, routing, Git, updater and migration tests (not installed)
LICENSE, NOTICE.md, SOURCES.md, LICENSES/, CLAUDE.md
```

This is a **guidance-only** skill. The installed skill doesn't include CLIs, binaries, hooks, scripts or credentials, and the plugin adds only Markdown agent definitions. The optional updater lives in `tools/` and is never installed with the skill.

## Maintenance

- **Validate:** `python3 tests/validate.py --cli`. It uses the Python standard library, plus Node.js and the Skills CLI for the install, migration and updater checks. It covers:
  - discovery and routing scenarios;
  - the Git and updater sandboxes;
  - links, checksums, license mirrors and the security scan;
  - the `plugin/` layout, both ZIPs, `plugin.json` and the `./plugin` marketplace source;
  - the agents and their capability mapping;
  - former names only in migration notes and history.
- **Release:**
  1. Bump `metadata.version` in `SKILL.md` and add a `CHANGELOG.md` entry.
  2. Set the same version in `plugin/.claude-plugin/plugin.json`. Claude Code users get the update only when this string changes.
  3. Run `python3 tools/package_skill.py` to build `dist/`.
  4. Attach the files from `dist/` (both ZIPs, the updater and their `.sha256` files) to a `v<version>` GitHub Release.
- **Add a source:** follow [CLAUDE.md](CLAUDE.md). Every bundled third-party file is checksummed in [SOURCES.md](SOURCES.md).

## Third-Party Licenses & Credits

Craftline's original work is © Abhishek Rampal and licensed under the [MIT License](LICENSE). That covers the routing, architecture, documentation, frontend, Git and ticket-delivery guides, the Impeccable adapter, the plugin agents, templates and tooling. Bundled third-party material is **not** owned by Abhishek Rampal. It stays the work of its authors and is redistributed under its original licenses:

- **[Impeccable](https://github.com/pbakaus/impeccable)** by Paul Bakaus: [Apache License 2.0](LICENSES/IMPECCABLE_APACHE-2.0.txt), with its [upstream NOTICE](LICENSES/IMPECCABLE_NOTICE.md). Modified for Craftline: the YAML front matter of its entry file, `SOURCE_SKILL.md`, was removed (see [NOTICE.md](NOTICE.md)).
- **[platform-design-skills](https://github.com/ehmo/platform-design-skills)** by ehmo: [MIT](LICENSES/PLATFORM_DESIGN_SKILLS_MIT.txt). Impeccable's iOS and Android references are derived from it.
- **[Apple Design](https://github.com/emilkowalski/skills)** by Emil Kowalski: [MIT](LICENSES/APPLE_DESIGN_MIT.txt).

Craftline is independent and isn't affiliated with or endorsed by these authors, or by Apple Inc., Google or Microsoft. Apple, Azure DevOps and other trademarks belong to their owners. See [NOTICE.md](NOTICE.md) for full attribution and [SOURCES.md](SOURCES.md) for provenance. Keep `LICENSE`, `NOTICE.md` and `LICENSES/` when you redistribute.

# Changelog

All notable changes to Craftline by uiuxAbhishek (formerly UIUX Abhishek DevKit and UIUX Abhishek Design) are recorded here. The project follows [Semantic Versioning](https://semver.org): a skill ID change or removed capability is a major version, a new capability a minor one, and fixes a patch.

**Stable releases** are Git tags with a GitHub Release, a Claude upload ZIP and its SHA-256 checksum. These are what the optional updater installs. **Development versions** were set in `SKILL.md` on `main` but never tagged or released.

## [3.0.1] — Unreleased

Prepares the plugin for submission to Anthropic's plugin directory. No skill guidance or routing changes.

### Added
- `plugin/README.md`: the directory listing. It covers example prompts, the 8 agents and where they load (Claude Code and Cowork; Claude Chat runs the same skill without agents), the approval rules for writes, what the plugin runs and sends (guidance only: no hooks, MCP servers, scripts or network calls of its own), and credits for Impeccable and Apple Design as in NOTICE.md.
- `plugin.json`: `displayName: "Craftline"`, `documentationUrl` (GUIDE.md) and `supportUrl` (GitHub Issues). `name` stays `craftline`.

### Changed
- The plugin ZIP now carries `README.md` at its top level.
- NOTICE.md and SOURCES.md list `plugin/README.md` as original work.
- Tests: the plugin layout check allows `README.md` and requires at least 40 words outside code blocks; the manifest check requires `displayName`, `documentationUrl` and `supportUrl`.

## [3.0.0] — 2026-11-24 (stable release)

**Breaking: renamed to Craftline.** UIUX Abhishek DevKit is now **Craftline** by uiuxAbhishek (Abhishek Rampal). The plugin ID and skill ID change from `uiuxabhishek-devkit` to `craftline`, so existing installs must migrate; an update can't carry them across. There are no capability, routing or guidance changes.

### Renamed
- Skill ID and folder: `plugin/skills/uiuxabhishek-devkit/` → `plugin/skills/craftline/` (`name: craftline`), moved with history. Title "Craftline"; tagline unchanged.
- Plugin: `plugin.json` `name: "craftline"`, author `uiuxAbhishek`. The marketplace keeps its name, `uiuxabhishek`, and its source, `./plugin`, so the Claude Code install ID is `craftline@uiuxabhishek` and the agents' namespace is `craftline:`. The 8 agents keep their names.
- Release ZIPs: `craftline-v<version>.zip` (Claude Chat upload) and `craftline-plugin-v<version>.zip`.
- The repository keeps its name, `abhishekinvission/uiuxabhishek-devkit`, and its pinned repository ID.
- Branding: Craftline is the primary identity in every doc, manifest, agent and tool. Former names appear only in migration notes and history. Licenses and copyright lines are unchanged.

### Migration
- **Claude Code:** `claude plugin marketplace update uiuxabhishek`, `claude plugin uninstall uiuxabhishek-devkit@uiuxabhishek`, `claude plugin install craftline@uiuxabhishek`.
- **Claude app:** after the marketplace syncs, install **craftline** and uninstall **uiuxabhishek-devkit**.
- **Codex, Gemini CLI, GitHub Copilot, Antigravity:** `npx skills remove uiuxabhishek-devkit -g -a <agents> -y`, then `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a <agents> -y`. Claude Code is never in these commands; it uses the plugin. The README and INSTALL.md Skills CLI commands now cover these four tools only.
- **Claude Chat:** delete the old skill and upload `craftline-v3.0.0.zip`.
- **Updater:** when it finds `uiuxabhishek-devkit` installed, `update --yes` installs `craftline` for the same configured agents, verifies it, then removes the former ID. `setup` no longer adds `claude-code` on its own when the Craftline plugin is installed. Its folder (`~/.uiuxabhishek-devkit`), file name and schedule names are unchanged, so existing schedules update in place. Download the 3.0.0 updater and run `setup` again.

### Tests
- `validate.py` requires exactly one discoverable skill, `craftline`, with Skills CLI 1.7.6 and 1.9.0; former IDs and brands only in migration notes, history, tests and the updater's migration code; no Skills CLI install command for `claude-code`; and the documented migration from both former IDs in a throwaway HOME.
- The updater sandbox adds migration cases: install then remove for the configured agents, failures at either step, and `setup` with the plugin installed.

## [2.1.1] — 2026-11-24 (stable release)

Fixes the plugin marketplace for the Claude app. The skill ID, capabilities, routing and install commands are unchanged.

### Fixes
- **Claude app marketplace.** Adding `abhishekinvission/uiuxabhishek-devkit` under the Claude app's **Add marketplace** failed with "1 plugin failed validation": GitHub-synced marketplaces accept `github`, `url`, `git-subdir` or `./` sources, not the `archive` source 2.1.0 used. The plugin now lives in one self-contained folder, `plugin/` (`.claude-plugin/plugin.json`, `agents/`, `skills/uiuxabhishek-devkit/`), moved with history and with no duplicate copies, and `.claude-plugin/marketplace.json` points at `"source": "./plugin"`. The archive URL and SHA-256 pin are gone, along with `package_skill.py --update-marketplace`.
- **Skill path.** The skill moved from `skills/uiuxabhishek-devkit/` to `plugin/skills/uiuxabhishek-devkit/`. `npx skills add abhishekinvission/uiuxabhishek-devkit --skill uiuxabhishek-devkit` still finds exactly one skill (checked with Skills CLI 1.7.6 and 1.9.0).
- **Updater.** It looks for the skill under `plugin/skills/` at the release tag, then under `skills/` for tags up to v2.1.0. Updater copies from 2.1.0 or earlier look only under `skills/`, so they fail their check for v2.1.1 and later; download the updater again from the release.

### Docs and tooling
- INSTALL.md explains adding the marketplace in the Claude app with **Sync automatically** on, the organization-sync limits, and that Claude Code offers a plugin update only when `plugin.json`'s `version` changes.
- `package_skill.py` builds both release ZIPs from `plugin/`: the Chat upload ZIP and the plugin ZIP, now for manual uploads only.
- `validate.py` checks the `plugin/` layout, that the marketplace source is `./plugin` and resolves to the plugin, that the entry name matches `plugin.json`, and that there are no symlinks.

## [2.1.0] — stable release

New capabilities, a Claude Code agent layer and fixes. The skill ID, install commands and existing routes are unchanged.

### Fixes
- **Impeccable script steps.** `new-work.md`, `critique.md` and `SOURCE_SKILL.md` call scripts that aren't bundled and call skipping them a contract violation. The new original adapter `references/adapters/impeccable-without-cli.md` gives a manual substitute for each step and overrides that wording. It loads with every routed file that calls a script: `design-new`, `critique`, `layout`, `typography` and `refine`'s polish step.
- **Maintainer files kept out of installs.** The new Claude Code plugin ZIP holds only `.claude-plugin/`, `agents/` and `skills/`; the Chat upload ZIP stays skill-only. `CLAUDE.md` now pushes an integration only after the user confirms in the current session, and no longer mentions an office installation.
- **Complete plugin manifest.** `plugin.json` carries version, description, author, homepage, repository, license and keywords, and its version must match `SKILL.md`.
- **Unused files.** Both ZIPs leave out the nine "Never load" Impeccable files. They stay in the repository; `NOTICE.md` and `SOURCES.md` record the omission.
- **Frontend guides.** The nine guides gained the decisions and failure modes they lacked, with compact examples where useful, and no longer restate the shared baseline.

### New capabilities
- `tickets`: ticket-to-draft-PR delivery for GitHub Issues, Jira and Linear, sharing a provider-neutral lifecycle (`ticket-delivery.md`) with Azure Boards. The ADO guide keeps only Azure specifics, and `ado-delivery-report.md` became `ticket-delivery-report.md`. ADO routing is unchanged.
- `figma-to-code`, `frontend-security`, `forms`, `seo-metadata` and `cross-platform-native` (React Native, Expo, Flutter). Security also loads from `review` for diffs that touch HTML rendering, auth or third-party scripts; SEO loads from `design-new` and `pages` for public pages; React Native, Expo and Flutter load the native responsive and audit files.

### Agents (Claude Code)
- `SKILL.md` §5 makes the main session the head. Small tasks stay inline. Larger ones get a plan the user approves before any agent starts. Only read-only agents run in parallel, and delivery runs last. Without subagents, the same plan runs step by step.
- Eight plugin agents: `ui-designer`, `ux-designer`, `design-auditor`, `figma-translator`, `frontend-engineer`, `test-engineer`, `code-reviewer` and `delivery-agent`. Each capability belongs to exactly one.
- `.claude-plugin/marketplace.json` installs the plugin from its GitHub release archive, pinned by SHA-256.

### Tests and tooling
- Skills CLI 1.9.0 installs the Antigravity copy under `~/.gemini/config/skills` and can leave `~/.agents/skills/uiuxabhishek-devkit` after a removal. INSTALL.md's troubleshooting gives the pinned 1.7.6 commands and the manual cleanup, and `validate.py` pins `skills@1.7.6`.
- `tools/package_skill.py` builds both ZIPs and, with `--update-marketplace`, pins the plugin ZIP in `marketplace.json`.
- `validate.py` adds checks for agent frontmatter, one agent per capability, read-only tools, agent bodies, the plugin and marketplace manifests, both ZIP layouts, and script-calling files without the adapter.
- Routing scenarios: 68 (24 new), each with its expected agent plan or `inline`. `SKILL.md` stays under 12,000 characters and `GUIDE.md` under 5,000. Average context per scenario must stay within 10% of the pre-router baseline (now +9.9%). The head's planning rules live in `references/workflows/agent-plans.md`, loaded only when a task uses agents.

## [2.0.1] — 2026-11-05 (stable release)

Fixes only. The skill ID, capabilities, install commands and the Claude upload ZIP format are unchanged.

- **Updater: reliable Node path.**
  - `setup` saves the stable Node link on `PATH` (for Homebrew, `/opt/homebrew/bin/node`, not `Cellar/node/<version>/bin/node`) as `node` in `config.json`.
  - Later `setup` runs, `disable` followed by `setup`, and `enable-auto-update` reuse the saved path.
  - A missing or non-Node path is replaced and reported. An invalid `DEVKIT_NODE` is rejected without changing anything.
  - Re-running `setup` upgrades a 2.0.0 configuration in place.
- **Updater: missed-check detection.**
  - `status` shows the scheduled Node path.
  - It warns when no scheduled check has run for about 48 hours, or when the saved Node path no longer runs.
  - It shows a first check after `setup` as pending, not overdue.
  - A scheduled run that fails still counts as a run and shows its error.
- **Strict read-only Git.**
  - `audit`, `plan` and ADO dry runs never run `git fetch` or write refs unless the user authorizes that exact operation. They use `git --no-optional-locks status` and `git ls-remote` instead.
  - In any mode, "don't fetch" rules out fetch and pull, and "offline" or "no network" rules out every network call.
- **Routing.**
  - The backend part of a full-stack or Azure DevOps task selects no Design or Engineering guide.
  - `harden` now matches "offline state", "offline support" or "network failure" rather than the bare word "offline", so an offline session no longer loads it.
- **Docs.** INSTALL.md documents `DEVKIT_NODE`, the saved Node path, updating from the 2.0.0 updater, and recovery when a check is overdue or Node is missing. GUIDE.md lists the no-fetch and offline limits.
- **Tests.**
  - 9 new routing scenarios (44 in total): backend-only ADO, frontend part of a full-stack task, a GitHub issue that isn't ADO, offline and no-fetch Git and ADO, and an offline UI state.
  - 3 Git sandbox checks (30 in total), which show the audit command set leaves `.git` byte-identical.
  - 23 updater sandbox checks (78 in total): Homebrew upgrade, re-setup, disable and re-enable, a missing or invalid Node, and stale, pending and failing checks.

## [2.0.0] — 2026-11-04 (stable release)

**Breaking:** the skill ID changes from `uiuxabhishek-design` to `uiuxabhishek-devkit`, and the repository from `abhishekinvission/uiuxabhishek-design` to `abhishekinvission/uiuxabhishek-devkit`. Remove the old skill and install the new one; see [INSTALL.md](INSTALL.md#migrate-from-uiuxabhishek-design).

- Renamed to **UIUX Abhishek DevKit**, with the tagline *Design. Build. Automate. Deliver.* The skill folder is now `skills/uiuxabhishek-devkit/`.
- All capabilities from 1.1.0 are kept unchanged: design, motion, accessibility, the nine frontend engineering guides, Git workflows, Azure DevOps delivery, templates, notices and licenses. Impeccable and Apple Design files are byte-identical.
- Added an optional, opt-in updater, `tools/updater/devkit-update.mjs`, which isn't part of the installed skill:
  - It checks for stable releases and notifies by default, and installs updates only after `enable-auto-update --yes`.
  - It schedules through launchd, systemd or cron, or Task Scheduler.
  - Before installing, it verifies the repository's identity, the release, its checksum and the skill-folder hash.
- Added this changelog and migration instructions, and the README now covers updates and versioning.
- Tests:
  - an updater sandbox with a mock GitHub API and a mock Skills CLI;
  - an isolated migration from the old skill ID;
  - install, update and removal for each agent;
  - a check for leftover references to the old ID.

## [1.1.0] — 2026-11-04 (development version, not released)

Commit `82f5367` on `main`. It was never tagged and has no GitHub Release or ZIP; its contents ship in 2.0.0.

- Universal Git and repository workflow for any provider:
  - status, sync, branches, safe commits, push, PR/MR creation and review, merges;
  - conflicts, recovery, history rewrites, tags and releases;
  - explicit approval gates and work preservation.
- Azure DevOps delivery now reuses the shared Git guidance instead of repeating it.
- `plan` now outranks `deliver` when both are requested. Added 14 Git routing scenarios and a 27-check Git sandbox.

Commit `a05f8fe` disabled automatic Claude commit and PR attribution, in this repository only. The skill didn't change.

## [1.0.0] — 2026-11-04 (stable release)

Tag `v1.0.0` (commit `dbb612c`), with the GitHub Release asset `uiuxabhishek-design-v1.0.0.zip` (SHA-256 `5729a0f916232c63520b897bb05a5fc0d318ec9937099a5352ab199145fd799b`). This tag and release are kept unchanged.

- Cross-agent installation guide (`INSTALL.md`) and a versioned Claude upload ZIP built by `tools/package_skill.py`.

## Pre-1.0 development (2026-11-03 to 2026-11-04, untagged)

- `8a6b768`: `SKILL.md` rebuilt as a selective, agent-neutral capability router with a capability guide (`GUIDE.md`) and routing tests.
- `036b394`: frontend engineering expansion (nine guides, Azure DevOps ticket-to-draft-PR delivery, two templates).
- `f0b098f`: branding, ownership and licensing policy for integrating sources.
- `8c7c9e5`, `93b5815`, `72d0bbf`: initial skill with Impeccable and Apple Design, the integration workflow and corrected install commands.

[3.0.0]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v3.0.0
[2.1.1]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v2.1.1
[2.1.0]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v2.1.0
[2.0.1]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v2.0.1
[2.0.0]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v2.0.0
[1.1.0]: https://github.com/abhishekinvission/uiuxabhishek-devkit/commit/82f5367
[1.0.0]: https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/tag/v1.0.0

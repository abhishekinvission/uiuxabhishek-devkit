# Install Craftline

Craftline by uiuxAbhishek (Abhishek Rampal) is **one** skill, `craftline`. Its design, motion, frontend, Git and Azure DevOps capabilities are bundled inside it and load automatically, so never install them separately. It was formerly UIUX Abhishek DevKit and UIUX Abhishek Design; to move an existing install, see [Migrate to Craftline](#migrate-to-craftline).

How you install it depends on where your agent runs:

| Where you use Claude or your agent | How Craftline gets there | Section |
| --- | --- | --- |
| **Claude Code** (terminal, IDE or the Claude Desktop **Code** tab) | The `craftline` plugin from this repository's marketplace: the skill plus specialist agents | [Claude Code plugin](#claude-code-plugin-skill-and-agents) |
| **Claude app plugins** | The same marketplace, added and synced from GitHub | [Claude app](#claude-app-add-marketplace) |
| **Codex, Gemini CLI, GitHub Copilot, Antigravity** | Skills CLI, installed on your computer | [Other local agents](#codex-gemini-cli-github-copilot-and-antigravity) |
| **Cloud / account-based Chat:** Claude.ai, Claude Desktop **Chat** and Cowork, Claude Code cloud sessions | ZIP upload in your Claude account | [Claude Chat upload](#claudeai-and-claude-desktop-chat) |

A local install doesn't reach cloud Chat, and an uploaded ZIP doesn't install anything for Codex, Gemini CLI, Copilot or Antigravity. Set up each environment you use. Give Claude Code only the plugin: a Skills CLI copy for Claude Code beside it would load the skill twice.

## Claude Code plugin (skill and agents)

The plugin gives Claude Code the skill and the specialist agents (`ui-designer`, `ux-designer`, `design-auditor`, `figma-translator`, `frontend-engineer`, `test-engineer`, `code-reviewer`, `delivery-agent`), which work only in Claude Code.

In Claude Code:

```text
/plugin marketplace add abhishekinvission/uiuxabhishek-devkit
/plugin install craftline@uiuxabhishek
```

Or from a terminal: `claude plugin marketplace add abhishekinvission/uiuxabhishek-devkit`, then `claude plugin install craftline@uiuxabhishek`.

- **What it installs.** The marketplace entry's source is `./plugin`, the repository's `plugin/` folder: `.claude-plugin/plugin.json`, `agents/` and `skills/craftline/` only. Maintainer files (`CLAUDE.md`, `.claude/`, `tests/`, `tools/`) are never installed.
- **One copy only.** If you also installed the skill for Claude Code with `npx skills`, remove that copy: `npx skills remove craftline -g -a claude-code -y`. Other agents keep their `npx` install.
- **Update.** `claude plugin marketplace update uiuxabhishek`, then `claude plugin update craftline@uiuxabhishek` (or update it from `/plugin`). Claude Code compares the `version` in `plugin.json`: a new release reaches you only after that string changes, however many commits land on `main` in between ([Claude Code docs](https://code.claude.com/docs/en/plugins/host-marketplace)). Auto-update is off for third-party marketplaces unless you turn it on under **Marketplaces** in `/plugin`. The updater below handles `npx` installs only.
- **Check.** `claude plugin details craftline` lists 1 skill and 11 agents. In a session, run `/agents` and look for the `craftline:` agents. Then ask for a task that spans two areas; the head should show a plan and wait for your approval before starting any agent.
- **Remove.** `claude plugin uninstall craftline@uiuxabhishek`.
- **Without the plugin**, other agents run the same plan themselves, one step at a time.

### Claude app: Add marketplace

The same marketplace works in the Claude app's plugin settings, where it's synced from GitHub:

1. Choose **Add marketplace**, pick the GitHub repository option and enter `abhishekinvission/uiuxabhishek-devkit`.
2. Leave **Sync automatically** on. The app then re-syncs whenever `main` changes, so every push to `main` reaches the Claude app without a version bump.
3. Install **craftline** from the **uiuxabhishek** marketplace.

GitHub-synced marketplaces accept fewer plugin sources than Claude Code: `github`, `url`, `git-subdir` or a relative path starting with `./`, not `archive` or `npm` ([organization sync docs](https://claude.com/docs/plugins/org-sync)). That's why the entry points at `./plugin`.

**Team and Enterprise organization sync** also requires the marketplace repository on github.com to be private or internal. This repository is public, so an organization admin needs a private or internal copy of it to sync for the whole organization.

## Codex, Gemini CLI, GitHub Copilot and Antigravity

### Requirements

- [Node.js](https://nodejs.org) **22.20 or later** (for `npx`) and Git.
- The agent itself, installed and signed in, in a version that supports Agent Skills.
- Network access to GitHub.

### Install globally (all four)

```bash
npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
```

`-g` installs for your user account, so every project can use it. `-a` picks the agents and `-y` skips the prompts. Leave out the agents you don't use. Claude Code isn't in this list: it uses the [plugin](#claude-code-plugin-skill-and-agents).

### Install for one agent

| Agent | CLI identifier | Command |
| --- | --- | --- |
| OpenAI Codex | `codex` | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -y` |
| Gemini CLI | `gemini-cli` | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a gemini-cli -y` |
| GitHub Copilot | `github-copilot` | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a github-copilot -y` |
| Google Antigravity | `antigravity` | `npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a antigravity -y` |

To install into the current project only, so it's shared through the repository, leave out `-g`. Run `npx skills add --help` to see every option your CLI version supports.

**Stable releases only.** The commands above follow the repository's `main` branch. To pin a release, add the tag: `npx skills add abhishekinvission/uiuxabhishek-devkit#v3.0.0 --skill craftline -g -a codex -y`. A pinned install stays on that tag when you run `update`, until you install a newer tag or use the [updater](#optional-update-notifications-and-automatic-updates).

**Where it lands.** With Skills CLI 1.7.6, a global install puts one copy in `~/.agents/skills/craftline`, which Codex, Gemini CLI, GitHub Copilot and Antigravity read. The CLI prints the exact paths when it finishes.

### Verify

1. Run `npx skills list -g`. It should show `craftline`.
2. Restart the agent or open a new session (see [Reload](#reload-after-install-update-or-removal)).
3. Ask: *"What can Craftline do?"* The agent should answer from the skill's capability guide.

### Update

```bash
npx skills update craftline -g -y
```

Running the install command again also works. Copies on other machines and agent instances (for example, a shared office installation) don't update when this repository changes. Update each one, or set up the [updater](#optional-update-notifications-and-automatic-updates) on each machine.

### Remove

```bash
npx skills remove craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
```

To remove it from one agent only, give just that `-a <identifier>`, for example `-a codex`.

### Reload after install, update or removal

Agents usually read their skill list when a session starts. After any change, start a new session, or close and reopen the agent, IDE window or Claude Desktop.

## Migrate to Craftline

Version 3.0.0 renamed UIUX Abhishek DevKit (`uiuxabhishek-devkit`) to **Craftline** (`craftline`). Version 2.0.0 had renamed UIUX Abhishek Design (`uiuxabhishek-design`) to UIUX Abhishek DevKit. The capabilities are the same; only the names changed. The repository keeps its name, `abhishekinvission/uiuxabhishek-devkit`, and the marketplace stays `uiuxabhishek`, so the Claude Code install ID is now `craftline@uiuxabhishek`. Because the IDs changed, an update can't carry an old install across: remove the old one and install Craftline.

### Claude app

After the marketplace syncs (automatically, or with a manual sync), the **uiuxabhishek** marketplace lists **craftline** instead of **uiuxabhishek-devkit**. Install **craftline**, then uninstall **uiuxabhishek-devkit** if it's still shown.

### Claude Code

```bash
claude plugin marketplace update uiuxabhishek
claude plugin uninstall uiuxabhishek-devkit@uiuxabhishek
claude plugin install craftline@uiuxabhishek
claude plugin details craftline
```

The last command should show 1 skill and 11 agents, now under the `craftline:` namespace. If you had also installed the skill for Claude Code with the Skills CLI, remove that copy: `npx skills remove uiuxabhishek-devkit -g -a claude-code -y`. Restart Claude Code.

### Codex, Gemini CLI, GitHub Copilot and Antigravity (Skills CLI)

```bash
npx skills remove uiuxabhishek-devkit -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
npx skills add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a codex -a gemini-cli -a github-copilot -a antigravity -y
npx skills list -g
```

List only the agents you use, and never add `-a claude-code` here: Claude Code uses the plugin. `npx skills list -g` should show `craftline` and no `uiuxabhishek-devkit`. Still on `uiuxabhishek-design`? Remove it first with `npx skills remove uiuxabhishek-design -g -y` (inside a project, without `-g`). The same commands work in Terminal, PowerShell or Command Prompt. Removing an old skill only deletes that skill's folder: other skills, agent settings and projects aren't touched.

### With the updater

If you use the [updater](#optional-update-notifications-and-automatic-updates), download the 3.0.0 `devkit-update.mjs` and run `setup` again (`--agents codex,gemini-cli,github-copilot,antigravity`). Its `check` then reports the rename, and `update --yes` installs `craftline` for your configured agents, verifies it, and only then removes `uiuxabhishek-devkit` for the same agents.

### Claude Chat and clones

- Claude Chat: under **Customize → Skills**, delete `uiuxabhishek-devkit` (and `uiuxabhishek-design` if present) and upload `craftline-v3.0.0.zip` (see [below](#claudeai-and-claude-desktop-chat)).
- A clone of this repository needs no change: the repository name is the same. Clones from before 2.0.0 can run `git remote set-url origin https://github.com/abhishekinvission/uiuxabhishek-devkit.git`.

## Claude.ai and Claude Desktop Chat

Claude.ai, Claude Desktop **Chat** and Cowork use skills stored in your Claude account, not files on your computer, so the CLI can't install there. Upload the packaged ZIP instead.

1. Download `craftline-v<version>.zip` from the [latest release](https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest). Its `.sha256` file is published alongside if you want to check the download.
2. In Claude, turn on **Settings → Capabilities → Code execution and file creation** (called "Create and edit files" in newer layouts). Skills need it.
3. Go to **Customize → Skills**, click **+**, choose **+ Create skill → Upload a skill** and select the ZIP. **Don't unzip it.**
4. Make sure the skill is toggled on. Then ask: *"What can Craftline do?"*

**Replacing a version.** Uploaded skills don't update themselves, and the updater can't reach your Claude account. To move to a new release, delete the old skill under **Customize → Skills**, then upload the new ZIP.

**What's in the ZIP.** It contains one folder, `craftline/`, with the skill: `SKILL.md`, `GUIDE.md`, `references/`, `templates/`, `LICENSE`, `NOTICE.md` and `LICENSES/`. It has no agents, and it leaves out the nine reference files listed under "Never load" in `SKILL.md`, which only drive Impeccable tooling that isn't bundled (see `NOTICE.md`). Claude's upload form allows descriptions of up to 200 characters, so the packaged `SKILL.md` carries a shorter description. Every file it contains matches the release tag byte for byte. The build is reproducible: `python3 tools/package_skill.py` at the same tag produces the same checksum. The plugin ZIP, `craftline-plugin-v<version>.zip`, is the `plugin/` folder for manual plugin uploads.

**Plans and organizations.** Skills are available on Claude's individual and organization plans. On Team and Enterprise, an owner may need to allow skills or user-created skills, or to provision the skill for everyone.

**What works in Chat.** Chat can't see your local repository or run your Git, test or Azure DevOps tools. Use it for design guidance, audits and critiques of screenshots or pasted code, UX copy and plans. Implementing changes, Git operations and the Azure DevOps workflow need a local coding agent with access to your repository.

**Claude Code and account skills.** Skills you turn on in your Claude account also load in Claude Code (v2.1.273 or later, signed in with the same Claude account, not an API key or cloud provider), in cloud sessions and in local sessions. With the plugin installed, Claude Code may then see two copies of Craftline. Keep just one for Claude Code.

## Optional update notifications and automatic updates

The updater is a single Node.js script, `devkit-update.mjs`, published with each release. It's optional and nothing installs it for you. It handles Skills CLI installs (Codex, Gemini CLI, GitHub Copilot, Antigravity); Claude Code updates its plugin itself.

- **Default: check and notify.** Once a day it asks GitHub for the latest **stable** release (not drafts, prereleases or unreleased commits), compares it with your installed version and shows a desktop notification on macOS and Linux. On Windows, the result goes to the log and `status`. It changes nothing.
- **Automatic updates: only if you opt in** with `enable-auto-update --yes`.
- **Before any install, it verifies:**
  - the repository by its permanent GitHub ID;
  - that the release is a stable `vX.Y.Z` tag;
  - that the tag's `SKILL.md` has the same ID and version;
  - that the release ZIP checksum matches GitHub's digest, when one is published.
- **How it installs:** it runs the official Skills CLI pinned to that tag, for `craftline` only and for the agents you chose. Afterwards it checks the installed version, tag and folder hash against the release. An install still under the former ID `uiuxabhishek-devkit` is migrated: it installs `craftline` for the same agents, verifies it, then removes the former ID.
- **Rollback:** it backs up the previous version first (it keeps the last three) and prints exact rollback steps if anything fails.
- **Safety:** it never touches other skills, agent settings, permissions or projects. It needs no credentials and runs no background service. The only code it runs is the official Skills CLI, through `npx`, pinned to the version these docs were tested with (`skills@1.7.6`). A lock file prevents overlapping runs.
- **Scheduling** uses each platform's own scheduler: a launchd agent on macOS, a systemd user timer or cron on Linux, and Task Scheduler on Windows. Its folder (`~/.uiuxabhishek-devkit`) and schedule names keep their earlier names, so existing schedules are updated in place.

**Set it up** (read the script first; it's short). On macOS or Linux:

```bash
curl -fsSLO https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest/download/devkit-update.mjs
curl -fsSLO https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest/download/devkit-update.mjs.sha256
shasum -a 256 -c devkit-update.mjs.sha256      # Linux: sha256sum -c devkit-update.mjs.sha256
node devkit-update.mjs check                   # one-off check, changes nothing
node devkit-update.mjs setup --agents codex,gemini-cli,github-copilot,antigravity
```

`setup` copies the updater to `~/.uiuxabhishek-devkit` and schedules daily notify-only checks. On Windows (PowerShell):

```powershell
Invoke-WebRequest https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest/download/devkit-update.mjs -OutFile devkit-update.mjs
Invoke-WebRequest https://github.com/abhishekinvission/uiuxabhishek-devkit/releases/latest/download/devkit-update.mjs.sha256 -OutFile devkit-update.mjs.sha256
(Get-FileHash devkit-update.mjs -Algorithm SHA256).Hash.ToLower()   # must equal the first word of devkit-update.mjs.sha256
node devkit-update.mjs setup --agents codex,gemini-cli,github-copilot,antigravity
```

**Which agents.** Without `--agents`, `setup` uses the agents Craftline is installed for. It never adds `claude-code` when the Craftline plugin is installed in Claude Code.

**Which Node it schedules.** The scheduler starts the check with an absolute Node path, saved as `node` in `~/.uiuxabhishek-devkit/config.json`. `setup` picks the stable `node` on your `PATH` (for Homebrew, `/opt/homebrew/bin/node`), not a versioned binary such as `Cellar/node/<version>/bin/node`, which disappears when Node is upgraded. Later `setup` runs reuse the saved path while it still runs. If it stops working, `setup` picks a working one and tells you. To choose one yourself, set `DEVKIT_NODE` once; it's validated, saved and reused:

```bash
DEVKIT_NODE=/opt/homebrew/bin/node node ~/.uiuxabhishek-devkit/devkit-update.mjs setup --agents codex,gemini-cli,github-copilot,antigravity
```

An invalid `DEVKIT_NODE` is rejected and nothing changes. Updating the updater itself: download the new `devkit-update.mjs` as above and run `setup` again with your `--agents`. It keeps your mode, schedule and Node path.

After `setup`, run the installed copy, for example `node ~/.uiuxabhishek-devkit/devkit-update.mjs status` (Windows: `node $HOME\.uiuxabhishek-devkit\devkit-update.mjs status`):

| Command | What it does |
| --- | --- |
| `setup [--agents codex,gemini-cli] [--no-schedule]` | Installs the updater and a daily notify-only check. Agents default to the ones the skill is installed for |
| `check` | Checks now and prints installed vs. latest stable. Changes nothing |
| `update --yes` | Installs the latest verified stable release now, migrating a former-ID install |
| `enable-auto-update --yes` | Lets the daily check install verified stable releases |
| `status` | Shows mode, schedule, the scheduled Node path, agents, versions, last result, errors and the log path. It warns when the saved Node path no longer runs, or when no scheduled check has run for about 48 hours. Right after `setup` it shows the first check as pending |
| `disable` | Removes the schedule and stops automatic updates. Manual `check`/`update` still work |
| `uninstall` | Removes the schedule and `~/.uiuxabhishek-devkit`. The skill stays installed |

**If an update fails,** the installed skill is either unchanged or restorable. `status` and `update.log` show the error, the backup folder and the exact command to reinstall the previous tag. A lock left by a crashed run is cleared automatically after two hours. The updater only handles installs made with the Skills CLI; Claude Chat uploads stay manual.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `npx: command not found`, or the CLI fails to start | Install or upgrade Node.js to 22.20 or later, then open a new terminal. |
| `Unknown agent`, or a flag is rejected | Check `npx skills add --help`. Use the identifiers exactly as listed above. |
| Installed, but the agent doesn't use it | Restart the agent or open a new session. Run `npx skills list -g` (or `claude plugin list` in Claude Code) to check it's installed. Name it in your prompt: *"Use Craftline to…"* |
| A former name (renamed in 3.0.0 or 2.0.0) still appears beside `craftline` | Remove it as shown in [Migrate to Craftline](#migrate-to-craftline), then restart. |
| `npx skills update` warns that a former skill ID (renamed) "appears to have been deleted upstream" | The CLI keeps your old copy, so nothing breaks, but it stays on the old version. [Migrate](#migrate-to-craftline) instead of updating. |
| Skills CLI 1.9.0 puts the Antigravity copy in `~/.gemini/config/skills/`, or leaves `~/.agents/skills/craftline` behind after a removal | These docs are tested with 1.7.6; pin it: `npx skills@1.7.6 add abhishekinvission/uiuxabhishek-devkit --skill craftline -g -a antigravity -y` and `npx skills@1.7.6 remove craftline -g -a antigravity -y`. To clean up by hand after removing the skill from **every** agent, check `npx skills list -g` no longer shows it, then run `rm -rf ~/.agents/skills/craftline ~/.gemini/config/skills/craftline`. Other agents still read the `~/.agents` copy, so don't delete it while any of them uses the skill. |
| Installed into the wrong project | Project installs (without `-g`) only apply to the folder you ran them in. Reinstall with `-g` or from the right project. |
| The skill appears twice in Claude Code | It's installed as the plugin and also by the Skills CLI for Claude Code, or through your Claude account. Keep the plugin and remove the others: `npx skills remove craftline -g -a claude-code -y`. |
| The Claude app reports "1 plugin failed validation" | The app read a `marketplace.json` from before 2.1.1, whose source was a release ZIP. Sync the marketplace again (or remove and re-add it) so it reads the current `main`, whose source is `./plugin`. |
| Claude Code doesn't offer a plugin update | It updates only when `version` in `plugin/.claude-plugin/plugin.json` changes. Run `claude plugin marketplace update uiuxabhishek`, then `claude plugin update craftline@uiuxabhishek`. |
| The agents don't appear in Claude Code | They come only with the plugin, not with `npx skills`. Install the [plugin](#claude-code-plugin-skill-and-agents), restart Claude Code and check `/agents`. |
| Claude upload rejected | Upload the release ZIP unchanged. Re-zipping the folder contents loose, or using the repository's own `SKILL.md`, whose description is longer than 200 characters, fails. Check that code execution is on and that your organization allows skills. |
| The skill shows in Chat but can't edit your code | That's expected. Chat has no access to your local repository. Use a local coding agent for implementation, Git and Azure DevOps delivery. |
| The updater says "another updater run is in progress" | Wait for it to finish. If nothing is running, the lock clears after two hours, or delete `~/.uiuxabhishek-devkit/update.lock`. |
| The updater reports a verification failure | It didn't update. Check `status` and keep your current version, or reinstall a known tag with the command it prints. |
| `status` says the scheduled check is overdue | No scheduled check has run for about 48 hours. The computer may have been off or asleep for days, or the schedule isn't loaded. Run `check` to check now, then `setup` to recreate the schedule. A failing check shows **Last error** instead. |
| `status` shows the Node path as missing or not runnable | Node was removed or moved, so the scheduler can't start the check. Run `setup` again to pick a working Node, or set `DEVKIT_NODE` (see above). |
| Azure DevOps steps stop at a dry run | That's intended without write authorization. You also need an approved, signed-in Azure DevOps connector or `az devops` CLI, and you have to say **implement** or **deliver** and grant the permissions. See [GUIDE.md](plugin/skills/craftline/GUIDE.md). |

Licensing and credits travel with every install in `NOTICE.md` and `LICENSES/`. See the [README](README.md#third-party-licenses--credits).

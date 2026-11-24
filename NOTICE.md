# Craftline — Notice

**Craftline** (`craftline`) by uiuxAbhishek (Abhishek Rampal), formerly UIUX Abhishek DevKit (`uiuxabhishek-devkit`) and UIUX Abhishek Design (`uiuxabhishek-design`)
Created and maintained by Abhishek Rampal (uiuxAbhishek) — <https://github.com/abhishekinvission/uiuxabhishek-devkit>

## Ownership

- **Original work.** The routing `SKILL.md`, integration architecture, documentation, maintenance policy, the frontend engineering guides (`references/frontend/`), the ticket, Azure DevOps and Git workflow guides (`references/workflows/`), the Impeccable script adapter (`references/adapters/`), `templates/`, the Claude Code plugin agents, README and manifests (`plugin/agents/`, `plugin/README.md`, `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`), and the repository's packaging, test and optional updater tooling (`tools/`, `tests/`; not part of the installed skill) were written for this project. They are © 2026 Abhishek Rampal and licensed under the MIT License (`LICENSE`).
- **Third-party work.** Material under `references/impeccable/` and `references/apple-design/` comes from the sources below. It remains the work of its respective authors and is redistributed under their original licenses. Bundling, renaming, reorganising or routing to this material does not transfer its copyright or ownership to Abhishek Rampal or anyone else.

## Third-party sources

- **Impeccable** by Paul Bakaus — <https://github.com/pbakaus/impeccable> — Apache License 2.0 (`LICENSES/IMPECCABLE_APACHE-2.0.txt`). Upstream attribution notices are reproduced in `LICENSES/IMPECCABLE_NOTICE.md`. Bundled version: 4.1.1 (per its upstream front matter). The entry-point file was renamed from `SKILL.md` to `SOURCE_SKILL.md` so it is not discovered as a separate skill. On 2026-11-24 Abhishek Rampal modified `SOURCE_SKILL.md` for Craftline: he removed its YAML front matter (`name`, `description`, `version`, `user-invocable`, `argument-hint`, `license` and `allowed-tools`, which only serve Impeccable's own tooling and whose tool wildcards the Claude plugin directory refused) and replaced it with a one-line attribution note. The body text is unchanged. All other Markdown content is unmodified. The release ZIPs (Claude Chat upload and Claude Code plugin) leave out nine reference files that only drive Impeccable's unbundled tooling: `live.md`, `live-setup.md`, `hooks.md`, `doctor.md`, `visualize.md`, `routing.md`, `init.md`, `craft.md` and `reference/degraded/`. They stay unmodified in the repository and in Skills CLI installs. Distributing a subset of the Work is permitted by the Apache License 2.0 (Section 4); this notice, the license and Impeccable's NOTICE still ship with every ZIP.
- **platform-design-skills** by ehmo — <https://github.com/ehmo/platform-design-skills> — MIT (`LICENSES/PLATFORM_DESIGN_SKILLS_MIT.txt`). Impeccable's `reference/ios.md` and `reference/android.md` are distilled from this work, as stated in Impeccable's NOTICE.
- **Apple Design** by Emil Kowalski — <https://github.com/emilkowalski/skills> — MIT (`LICENSES/APPLE_DESIGN_MIT.txt`). Markdown content is unmodified; the entry-point file was renamed from `SKILL.md` to `SOURCE_SKILL.md`.

## Disclaimers

Craftline is an independent project. It is not affiliated with, sponsored by or endorsed by the upstream authors, Apple Inc., Google or Microsoft. Apple and other trademarks belong to their respective owners; the Apple Design reference describes publicly presented design principles and does not imply any association.

Only Markdown guidance and templates are bundled. Upstream CLIs, scripts, hooks, binaries and install tooling are not included, and this package is not a replacement for the original projects. Azure DevOps and Azure Boards are trademarks of Microsoft. No Azure credentials or connectors are included.

When redistributing, keep this notice, `LICENSE` and the `LICENSES/` directory.

# SonarQube lookups, file analysis and setup

**Use for:** reading SonarQube data (projects, gate status, issues, coverage gaps, duplication, dependency risks, rule details), analysing a few files, and setting up or troubleshooting the `sonar` CLI and the SonarQube MCP server. Fixing findings: [sonarqube.md](sonarqube.md). Checked against SonarQube CLI and MCP server documentation on 2026-11-25; the CLI is in beta, so confirm a command in `sonar --help` when it fails.

## 1. Reach SonarQube
Use the first that works and say which:
1. **SonarQube MCP tools** in the session. Their prefix comes from the server's configured name (often `mcp__sonarqube__`); match on the tool name.
2. **The `sonar` CLI**, logged in (`sonar auth status`).
3. **Neither:** ask for the pasted gate result, issue list or a screenshot, and offer setup (§4).

**Input checks** before any value goes into a command (stop and name a rejected value): project and file keys `A–Z a–z 0–9 . _ - :`; branch names the same plus `/`; pull-request IDs digits only; search text letters, digits, spaces and `. _ -`; severities and statuses only from §2. Never invent a command, flag or tool parameter.

## 2. Lookups (read-only)
Fetch only what the question needs. **Project key:** MCP tools may know a default, so try without one; the CLI always needs it, from the user, then `sonar.projectKey` in `sonar-project.properties` (or the build file), then the project list. Add a branch or pull request when the user names one. File keys are `<project-key>:<path/to/file>`.

| Data | MCP tool | CLI |
| --- | --- | --- |
| Projects | `search_my_sonarqube_projects` | `sonar list projects [-q <text>]` |
| Gate status | `get_project_quality_gate_status` | `sonar api get "/api/qualitygates/project_status?projectKey=<key>[&branch=<name>][&pullRequest=<id>]"` |
| Values of failed metrics | `get_component_measures` | `sonar api get "/api/measures/component?component=<key>&metricKeys=<keys>"` |
| Issues | `search_sonar_issues_in_projects` | `sonar list issues -p <key> --format json [--severities …] [--statuses …] [--branch …] [--pull-request …] [--file <path>] [--new-code] [--page …]` (`--format toon` is more compact) |
| Lowest-coverage files | `search_files_by_coverage` | `sonar api get "/api/measures/component_tree?component=<key>&metricKeys=coverage,line_coverage,branch_coverage&qualifiers=FIL&strategy=leaves&s=metric&metricSort=coverage&asc=true"` |
| Uncovered lines in one file | `get_file_coverage_details` | `sonar api get "/api/sources/lines?key=<file-key>"` |
| Most-duplicated files | `search_duplicated_files` | `sonar api get "/api/measures/component_tree?component=<key>&metricKeys=duplicated_lines,duplicated_blocks,duplicated_lines_density&qualifiers=FIL&strategy=leaves"` |
| Duplicated blocks in one file | `get_duplications` | `sonar api get "/api/duplications/show?key=<file-key>"` |
| Dependency risks | `search_dependency_risks` (needs SonarQube Advanced Security) | none documented here; use the MCP tool or the UI |
| Rule details | `show_rule` | `sonar api get "/api/rules/show?key=<rule-key>"` |

- **Severities:** `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`; newer versions also `HIGH`, `MEDIUM`, `LOW`. **Statuses:** `OPEN`, `CONFIRMED`, `FALSE_POSITIVE`, `ACCEPTED`, `FIXED`.
- `sonar list issues` has no rule, type or tag filter: filter the returned list yourself and say so.
- The CLI has no `sonar quality-gate`, `sonar coverage` or `sonar duplication` command; use the `sonar api get` routes.
- Gate metrics on new code: `new_coverage`, `new_duplicated_lines_density`, `new_violations`, `new_security_hotspots_reviewed`, `new_reliability_rating`, `new_security_rating`, `new_maintainability_rating`. Explain each failed one in plain words with threshold and actual value.
- An edition refusal (dependency risks, agentic analysis) is a plan limit, not a setup problem; say so.
- 0% coverage is usually report wiring: [sonarqube.md](sonarqube.md) §4.

## 3. Analyse files
Files only, not folders (given a folder, ask which files). Analysis sends file content to the user's SonarQube service: only when the user asks. Try in order:
1. `run_advanced_code_analysis` (needs a Vortex subscription), with the branch from `git branch --show-current`.
2. `analyze_file_list` (needs SonarQube for IDE connected), with absolute paths.
3. `sonar analyze agentic --file <path> [--file <path> …] --format json [--branch <name>] [-p <key>]`.

None works: say so and diagnose with §4. Show per file: rule key, line, severity and message, highest first; after a fix, what disappeared and what is new.

## 4. Setup and troubleshooting
**Diagnose in order:** no SonarQube MCP tools → not connected (step 4); configured but no tools → the MCP server runs in a container, so check `docker ps`, `podman ps` or `nerdctl ps` and ask the user to start the runtime and restart the session; `sonar` not found (`which sonar`, Windows `Get-Command sonar`) → step 2; not logged in or refused → `sonar auth status`, step 3; project not found → `sonar list projects` or `sonar.projectKey`.

**Setup:** one step at a time; show each install, update or integration command and run it only after the user's explicit yes. Logging in is always the user's.
1. **Check:** `which sonar` or `Get-Command sonar`.
2. **Install** (pick one): `brew install sonarqube-cli` or `mise use -g sonarqube-cli@latest`. Install scripts and direct downloads (macOS, Linux, Windows): point the user to the [SonarQube CLI quickstart](https://docs.sonarsource.com/sonarqube-cli/quickstart-guide); don't pipe a download into a shell yourself. **Update** the way it was installed: `brew upgrade --cask sonarqube-cli`, through mise, or `sonar update` for a script install. A failed update: show the error and continue with the installed version.
3. **Log in**, in the user's own terminal (interactive; the token never passes through the chat): `sonar auth login`, or `sonar auth login --server <server-url>`; SonarQube Cloud `--server https://sonarcloud.io` (US: `https://sonarqube.us`). It needs a user token. Confirm with `sonar auth status`.
4. **Connect the agent:** `sonar integrate claude` (other agents: `sonar integrate` lists them). Global by default since CLI 1.9.0 (`--global` is deprecated); `--non-interactive` when it can't prompt. Ask which agent first.
5. **Restart and confirm:** the user restarts the session; check the SonarQube MCP tools appear, `sonar auth status` passes and the project key is known.

## Report
Lookups and analyses: a one-line answer (e.g. "Gate: failing, 2 of 6 conditions"), a compact table, then at most two next steps. Setup: CLI version, server or organization (never the token), agent connected, scope; then continue the original request.

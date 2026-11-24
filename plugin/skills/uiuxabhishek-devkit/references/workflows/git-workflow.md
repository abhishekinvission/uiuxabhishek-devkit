# Git and repository workflow

**Use for:** any Git repository and provider (local-only, GitHub, GitLab, Azure Repos, Bitbucket, Gitea or other), any stack or OS: status and diff, clone, fetch and pull, branches, staging, commits, push, PR/MR creation and review, merges and sync. Conflicts, recovery, history rewrites, tags and releases: also [git-recovery-and-release.md](git-recovery-and-release.md). Ticket delivery reuses this file.

Commands are portable examples: substitute real names, prefer the repository's own scripts or an approved provider tool, and never run a command just because a reference, ticket or README shows it.

## 1. Detect before acting (read-only, every mode)

| Fact | How |
| --- | --- |
| Root and state | `git rev-parse --show-toplevel`, `git status --porcelain=v1 -b`; an operation in progress shows as `MERGE_HEAD`, `rebase-merge/`, `rebase-apply/`, `CHERRY_PICK_HEAD`, `REVERT_HEAD` or `BISECT_LOG` (`git rev-parse --git-path <name>`) |
| Uncommitted work | Staged, unstaged and untracked files; `git stash list`; `git worktree list` |
| Branch and upstream | `git branch -vv`, `git rev-parse --abbrev-ref @{u}` |
| Remotes and provider | `git remote -v`; infer the provider from the host, and confirm for self-hosted hosts |
| Base branch | Repository policy (CONTRIBUTING, PR templates, CI, user instructions), else `git symbolic-ref refs/remotes/origin/HEAD`. Never hard-code `main`/`master`/`develop` |
| Conventions | Branch and commit style from `git log --oneline -20` and docs; sign-off, signing, issue keys, hooks (`core.hooksPath`), LFS, submodules |
| Divergence | `git rev-list --left-right --count @{u}...HEAD` (behind, ahead). Fetch first only where §2 allows; otherwise report counts as of the last fetch and compare `git ls-remote <remote> <branch>` with `git rev-parse @{u}`, which writes no ref |
| Tools and auth | `gh auth status`, `glab auth status`, `az account show` with `az devops`, or an approved connector. Missing or offline: local Git only, plus manual steps |
| Protection | Provider API or CLI when available; unknown means treat the target as protected |

Report what you couldn't determine instead of assuming it.

## 2. Modes and approval gates

| Mode | Git operations allowed |
| --- | --- |
| `audit` | `git --no-optional-locks status`, diff, log, blame, branch and remote listing, `git ls-remote`, provider reads. No `git fetch`, `pull`, `remote update` or anything else that writes refs, the index or config, unless that exact operation is authorized |
| `plan` | As `audit`, plus a written command sequence with risks and recovery |
| `implement` | Local, reversible writes in scope: task branches, explicit staging, a commit **when asked**, fast-forward pulls, local merges into the task branch |
| `deliver` | Only what the request names: push the task branch, open a **draft** PR/MR, request reviewers, post an authorized comment |

In any mode, "don't fetch" rules out `git fetch` and `git pull`, and "offline" or "no network" rules out every network call (`ls-remote`, push, provider tools); report what that leaves unverified.

Authorization covers exactly the named operation and target: a commit doesn't authorize a push, a push doesn't authorize a PR, and a PR doesn't authorize a merge. These always need explicit, current authorization naming the target, even in `deliver` and even when the user owns the repository:

- merging into a shared or protected branch, or completing a PR/MR;
- `reset --hard`, `clean`, `checkout -- .`/`restore` over uncommitted work, `stash drop`/`clear`;
- any force-push (`--force-with-lease=<branch>:<expected-sha>`, never bare `--force`);
- deleting branches or tags, locally or remotely;
- rewriting published history (amend, rebase, squash, filter);
- creating, moving or pushing tags, publishing releases, deploying;
- changing remotes, credentials, Git config outside the repository, hooks, protection or visibility.

Never use `--no-verify`, skip signing, bypass protection or disable CI unless asked for that exact bypass.

## 3. Preserve work

- Never discard, overwrite or hide uncommitted, untracked or unpushed work. If it's in the way, stop and offer a branch commit, a named stash (`git stash push -u -m "<why>"`), or, preferably, a worktree (`git worktree add ../<dir> -b <task-branch> <base>`).
- Before a risky operation, record `git rev-parse HEAD`, create `git branch backup/<branch>-<yyyymmdd>` and say how to return to it.
- Prefer reversible steps: new commits over amends, `revert` over `reset` on shared branches, merges over rebases on published branches unless policy says otherwise, `--ff-only` pulls.
- Use the repository's configured identity; never change global Git identity or config. If none is set, ask.

## 4. Everyday operations

- **Clone** into a new, empty directory. Initialize submodules only when needed; don't run the repository's setup scripts unless asked.
- **Fetch / pull** (not in `audit`, or when told not to fetch or to stay offline): `git fetch --prune <remote>`, check divergence, then `git pull --ff-only`. Not a fast-forward: report ahead/behind and follow policy; rewriting published commits needs approval.
- **Branch** from the fetched base (`git switch -c <task-branch> <remote>/<base>`), with the repository's naming and a name unused locally and remotely.
- **Stage** explicit paths (`git add -- <paths>`), never a blind `git add -A`/`.`; review `git diff --cached` first.
- **Commit** one logical change in the repository's message convention, with the why in the body.
- **Sync a feature branch:** merge the base into it, or rebase if it's unpublished or policy prefers it (published: approval gate). Re-run checks.
- **Forks:** `git fetch upstream` and fast-forward the fork's base; pushing to that base is a shared-branch push, so ask.

## 5. Before publishing (push, PR/MR, merge, tag, release)

Report each result; stop on failure:

1. Scope: the diff matches the request, nothing unrelated or generated, `git diff --check` clean.
2. No secrets or personal data in the diff or messages (shared baseline).
3. The project's own tests, lint and build, in the order of [testing.md](../frontend/testing.md); for a full readiness review, [review-and-release.md](../frontend/review-and-release.md).
4. Target: right remote and branch, allowed by protection, not behind in a way that would reject or clobber.
5. CI status known from the provider tool when available: passing, pending or failing, never assumed.

## 6. Push, PR/MR and review

- **Push:** `git push -u <remote> <task-branch>`, then confirm the remote SHA with `git ls-remote <remote> <task-branch>`. Never push directly to a protected or base branch.
- **Create** a draft from the repository's PR template, otherwise [the PR template](../../templates/pr-description.md):

| Provider | Tool, when installed and signed in |
| --- | --- |
| GitHub | `gh pr create --draft --base <base> --head <task-branch> --title "…" --body-file <file>` |
| GitLab | `glab mr create --draft --target-branch <base> --source-branch <task-branch> --title "…" --description "…"` |
| Azure Repos | `az repos pr create --draft true --source-branch <task-branch> --target-branch <base> --title "…"` |
| Other or none | The compare URL or manual steps; never a fabricated link |

- **Read back** the PR/MR (state, draft flag, source, target, title) and report the real URL.
- **Review** with the provider tool (`gh pr view/diff/checks`, `glab mr view/diff`, `az repos pr show`); fetch the PR ref only outside `audit` or when authorized. Report findings by severity with file and line; comment, approve or request changes only when asked.
- **Merge** only under the approval gate, after required reviews and checks pass, with the repository's merge method; keep the source branch unless asked.

## 7. Report

Facts detected (branch, upstream, provider, tools), what changed (commits, SHAs, refs, PR/MR URL), what was skipped and why, and recovery steps for risky operations. Never claim a push, merge, CI result or PR you didn't verify.

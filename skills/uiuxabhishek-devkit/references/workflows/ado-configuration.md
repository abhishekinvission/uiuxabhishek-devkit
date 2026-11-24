# Azure DevOps delivery — project configuration

A **configuration contract**, not defaults. Resolve each value from the repository, the work-item URL, the Azure DevOps connection or the user. Never guess the tenant, organization, project, repository, base branch or work-item type.

| Setting | Source |
|---|---|
| Organization and project | The work item URL or the connected organization; no fixed URLs |
| Repository | The one the work item belongs to: Azure Repos, or a linked GitHub repository |
| Work item | The given ID or URL; an ID alone only when the organization and project are unambiguous |
| Base branch | Repository policy, else the default branch, confirmed before any write |
| Branch naming | Repository conventions; include the work-item ID when they require it |
| Gates | The repository's scripts and CI; never an invented command |
| Credentials | An approved connector, the signed-in `az` CLI or user-managed auth; never tokens in files |
| PR type | Draft unless user or project policy says otherwise; approval and merge are separate requests |
| Write permission | Explicit authorization within the tool's scope; a report isn't permission to publish |

**Tools, in order:** an approved Azure DevOps connector; the `az devops` extension when installed, configured and signed in (check its help, as versions differ); for GitHub-hosted code, the GitHub tool. With none of these, give a dry-run report and manual steps. Azure DevOps Server may lack CLI support; use its official API or UI where authorized.

**Precedence:** branch protection, enterprise policy, user scope and permissions override this guide.

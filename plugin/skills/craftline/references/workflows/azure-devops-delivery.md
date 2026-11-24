# Craftline — Azure DevOps ticket-to-draft-PR delivery

**When to use:** an Azure Boards work item ID or URL, or an explicit request to deliver a requirement through Azure DevOps. It works with any project stack.

Read [ado-configuration.md](ado-configuration.md) first, then follow the provider-neutral lifecycle, modes and stop conditions in [ticket-delivery.md](ticket-delivery.md). This file adds only what's specific to Azure DevOps; where the two differ, the stricter rule applies.

## Detect
- `dev.azure.com/<org>/<project>/_workitems/edit/<id>` or `<org>.visualstudio.com/<project>/_workitems/edit/<id>`.
- `AB#<id>` in a GitHub repository linked to Azure Boards.
- A bare number counts as a work item only when the Azure organization and project are unambiguous.

## Read the work item
- Use the approved Azure DevOps connector, or `az boards work-item show --id <id>` when the CLI is installed, configured and signed in ([ado-configuration.md](ado-configuration.md) covers capability detection).
- Fields: `System.Title`, `System.WorkItemType`, `System.State`, `System.Description`, `Microsoft.VSTS.Common.AcceptanceCriteria`, `Microsoft.VSTS.TCM.ReproSteps` (bugs), `System.AssignedTo`, `System.AreaPath`, `System.IterationPath`, comments, attachments, and parent, child and related links.
- Don't guess the state or treat chat history as the live state.

## Existing PRs
- Check the work item's linked PRs and their real Azure Repos states: **active** (including draft), **completed** or **abandoned**. Apply ticket-delivery.md step 2 to them.
- An abandoned PR is history only: start a fresh branch from the current allowed base and don't cherry-pick its code blindly.
- Linked GitHub PRs follow GitHub's own states.

## Create and link the draft PR (only when authorized)
- Azure Repos, through the approved connector or the official CLI. Substitute real values; don't run it blindly:
  `az repos pr create --repository <repo> --source-branch <task> --target-branch <base> --title "<title>" --description "<summary>" --draft true --work-items <id>`
- GitHub code linked to Azure Boards: open the PR with the approved GitHub tool and reference `AB#<id>` in its description.
- Read back the status, draft flag, source and target, the linked work item, title and description. If creation failed, say so and give manual steps; never a made-up URL.

## Comments and state
- Post only necessary, explicitly authorized work-item comments (clarifications, dependency status, outcome), confirm they're visible, and don't repeat them on a rerun.
- Never approve, complete or auto-complete a PR, edit acceptance criteria, change the work item's state or trigger deployments unless separately asked.

## Report
Use the [delivery report template](../../templates/ticket-delivery-report.md) with tracker "Azure Boards", and include the organization, project and repository you verified.

## Azure-specific stop conditions
No verified organization or project; no Azure permission for the read or write; Azure DevOps Server without a supported CLI or API for the step. Otherwise use ticket-delivery.md's stop conditions.

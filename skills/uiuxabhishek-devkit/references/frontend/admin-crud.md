# Accessible admin CRUD

**Use for:** management screens that list, search, create, edit, archive or delete records.

## Decide before building
- **Entity contract.** Identifier, fields that become read-only after create, uniqueness rules, server-filled defaults, and what "delete" means here: archive, soft delete, hard delete or deactivate. If the request doesn't say, ask. Never guess delete semantics.
- **Permission matrix.** Per action (view, create, edit, delete, export, bulk). The UI hides or disables what the server would refuse.
- **Concurrency.** Last write wins, a version or ETag check, or a lock. Use what the API supports; if it supports none, report the risk.
- **Reuse.** List mechanics come from [data-reports.md](data-reports.md), the request lifecycle from [api-integration.md](api-integration.md), and validation timing, errors, drafts and double submission from [forms.md](forms.md).

## Behavior
- One form component with a create/edit mode, not two copies that drift apart. Edit loads the record by ID from the server, not from the list row, which may be stale or partial.
- Not found and forbidden are different screens: a 404 says the record doesn't exist, a 403 says you lack access. Neither shows an empty form.
- After a save or delete, refresh only what changed (refetch the row or invalidate the list) and keep the user's filters, sort and page.
- Destructive actions name the record and the consequence, and the button names the action:

  | Bad | Good |
  | --- | --- |
  | "Are you sure?" with **OK** | "Delete invoice INV-2041? Its 3 payments are deleted too." with **Delete invoice** |

  For irreversible, high-impact deletes, ask the user to type the record name. For routine reversible ones, prefer an undo over a dialog.
- Bulk actions show how many items are selected, apply only to the selection unless "all matching" is explicit, and report failures per record.
- Role editors prevent self-lockout (removing your own last admin role) and never offer roles the current user can't grant.

## Failure modes to design for
- An optimistic delete the server rejects leaves a gap in the list: roll back and announce the failure.
- Saving over a record someone else changed silently loses their work: show the conflict with both values.
- Deleting the last row on the last page lands on an empty page: step back one page.
- A new record that doesn't match the current filter seems to vanish: confirm the save with a link to it.

## Tests
- List, filter and page; create and edit payloads; invalid input blocks the request; not found vs forbidden; delete confirmation and rollback on failure.
- Permission-denied actions are refused by the API, not only hidden; bulk partial failure; conflict on concurrent edit when the API supports versions.
- Keyboard-only flow through list, form and dialog, with focus returning to the triggering control.

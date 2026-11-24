# Reports, data tables, filters and exports

**Use for:** analytics screens, audit views, admin lists and other data-heavy reports.

## Data contract
- Confirm row schema, stable row ID, sort keys, filter semantics, totals, time zone of date boundaries, permission scoping, export formats and realistic data volume.
- **Server or client?** Sort, filter and page on the client only when the whole dataset is loaded, bounded and small (roughly a few thousand rows or fewer). Otherwise do all three on the server. Never mix: client-sorting one server page sorts only that page.
- **Offset or cursor?** Offset paging allows jumping to page N but drifts when rows are inserted; cursor paging is stable on live data but only steps forward and back.

## Filters
- Say what an empty filter means ("all statuses") and how several combine (AND across fields, OR within one multi-select), and show active filters as removable chips.
- Keep filters, sort and page in the URL so a view can be shared and survives refresh (see [state-management.md](state-management.md)).
- Debounce free-text search; use an explicit **Apply** when each change triggers an expensive query. Reset to page 1 when filters change.

## Table
- Sort numbers and dates by value, not their formatted text, where "10" sorts before "9".
- Right-align numbers in a consistent precision and unit; format with the user's locale; state the time zone in headers or a caption.
- Keep headers real `<th>` cells with `aria-sort` on the sorted column, keyboard-reachable sort and actions, and a visible loading, empty, no-match and error state, each different.
- Virtualize very long lists and keep the header sticky; keep row identity stable so selection and focus survive refresh.

## Totals, charts and exports
- A total must match the scope it labels: totals of the whole filtered set come from the server, not from summing the current page.
- Charts need units, labelled axes, a legend where needed and a table alternative. Mark partial periods and missing data instead of drawing zeros.
- Exports honor the same filters and permissions as the screen and say which columns they include. Export large sets as a background job with a download link. In CSV built from user data, neutralize cells starting with `=`, `+`, `-`, `@`, tab or carriage return.

## Verify
- Sort both directions, with ties and nulls; empty and no-match states; first and last page; quick filter changes leave the latest result.
- The export row count and filter scope match the screen; the formula-injection defense works; boundaries around daylight-saving changes are correct.
- Table semantics and keyboard access with a screen reader spot check.

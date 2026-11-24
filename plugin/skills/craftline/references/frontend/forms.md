# Forms: validation, errors, multi-step, autosave and upload

**Use for:** building or fixing forms of any size: field validation, error display, wizards, drafts and autosave, file upload and submission.

## Validation
- **One schema.** When the stack allows, validate client and server with the same schema (a shared package, JSON Schema, or types generated from the API contract). The client check is for speed; the server's answer wins.
- Map the server's field errors back onto the matching fields, and show errors that belong to no field (conflicts, quota) at the top.

## When to show errors
| Moment | Rule |
| --- | --- |
| Before the user touches a field | Never show an error |
| On blur | Validate a field after the user leaves it the first time |
| While typing | Only clear an error that's now fixed, or show live rules the user asked for (password strength) |
| On submit | Validate everything, block the request on errors, then move focus (below) |

## Accessible errors
- Every input has a visible `<label>`; required fields say so in the label text, not only with color or an asterisk.
- Tie the message to the field and mark it invalid:

  ```html
  <!-- Bad: red border only; screen readers hear nothing -->
  <input id="email" class="error">
  <!-- Good -->
  <label for="email">Email</label>
  <input id="email" type="email" autocomplete="email" aria-invalid="true" aria-describedby="email-err">
  <p id="email-err">Enter an email like name@example.com</p>
  ```
- On a failed submit with several errors, show an error summary at the top with links to each field and move focus to it. With one error, focus that field.
- Messages say what to do ("Enter a date after today"), not only what went wrong ("Invalid date").

## Multi-step forms
- Each step validates only its own fields; going back keeps what the user entered.
- Show step names and position ("Step 2 of 4: Address"), and end with a review step that links back to each section.
- Save progress server-side when the flow is long or crosses sessions; otherwise in storage, versioned and cleared on submit or sign-out (see [state-management.md](state-management.md)).

## Autosave and drafts
- Debounce saves and show their state: "Saving…", "Saved 10:42", or "Not saved, retry".
- Detect a newer version saved elsewhere and offer a choice instead of overwriting it.
- Warn before leaving only when there are unsaved changes.

## File upload
- Offer a real button; a drop zone is an extra. State the accepted types and maximum size before the user picks a file.
- Check type and size on the client for speed and on the server for safety; don't trust the file's extension or reported MIME type.
- Show progress per file with cancel and retry. Use resumable or chunked upload for large files when the API supports it.

## Autocomplete and input types
- Use the right `type`, `inputmode` and `autocomplete` token: `name`, `email`, `tel`, `street-address`, `postal-code`, `country`, `cc-number`, `one-time-code`, `current-password` or `new-password`. Never turn autocomplete off for login fields.

## Double submission
- While a request is pending, ignore further submits and show progress on the button. Keep the button focusable (`aria-disabled`), because a disabled button drops keyboard focus.
- For payments and other mutations that mustn't repeat, send an idempotency key when the API accepts one.

## Verify
- Error timing matches the table; the summary and focus move work with a keyboard and a screen reader.
- Server-only errors appear on the right fields; back and forward in a wizard keep data; drafts survive refresh and conflict correctly.
- Upload limits, cancel, retry and a slow network; rapid double click sends one request; password managers and autofill fill the right fields.

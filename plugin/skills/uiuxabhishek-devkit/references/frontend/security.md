# Frontend security

**Use for:** code that renders HTML or URLs from data, handles tokens or sessions, redirects, embeds third-party scripts, uses `postMessage`, or changes dependencies, and security reviews of such diffs.

## XSS sinks
Treat any value from users, URLs, APIs or storage as untrusted when it reaches:
- **HTML:** `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, Vue `v-html`, Angular `[innerHTML]`, and any `bypassSecurityTrust*` call.
- **Code:** `eval`, `new Function`, and string arguments to `setTimeout` or `setInterval`.
- **URLs:** `href`, `src`, `action`, `formaction` and `location`, where `javascript:` and `data:` URLs run code.

Prefer the framework's text binding, which escapes. Allow only safe URL schemes:

```ts
// Bad: profile.website = "javascript:alert(document.cookie)" runs on click
<a href={profile.website}>Website</a>
// Good: only http(s) links render as links
const safe = /^https?:\/\//i.test(profile.website) ? profile.website : undefined
<a href={safe} rel="noopener noreferrer">Website</a>
```

## Sanitization
- Render HTML from data only when it must be rich text. Then sanitize at render time with a maintained sanitizer (for example DOMPurify, or the framework's own) and a strict allowlist of tags and attributes.
- Don't write your own regex sanitizer. Where browsers support it, Trusted Types make unsafe sinks fail loudly.

## Content Security Policy
- Aim for `script-src` with nonces or hashes plus `'strict-dynamic'`, `object-src 'none'`, `base-uri 'none'` and `frame-ancestors` set to who may embed you. Avoid `'unsafe-inline'` and `'unsafe-eval'`.
- Roll out with `Content-Security-Policy-Report-Only` first, fix the reports, then enforce.

## Tokens and sessions
- Prefer a session in an `HttpOnly`, `Secure`, `SameSite` cookie set by the server: page scripts, and so XSS, can't read it.
- If bearer tokens are required, keep the access token in memory, short-lived, and refresh it through an `HttpOnly` cookie. `localStorage` and `sessionStorage` are readable by any injected script.

## CSRF (cookie-based auth)
- State changes never use `GET`. Use `SameSite=Lax` or `Strict` cookies, plus a CSRF token or a required custom header that the server checks.

## Third-party scripts
- Each script runs with your page's full privileges; a tag manager can run anything. Load only what's needed.
- Pin versions and add Subresource Integrity (`integrity` plus `crossorigin`) for CDN files, or self-host them. Sandbox third-party iframes.

## Secrets in bundles
- Everything shipped to the browser is public, including variables with public prefixes such as `VITE_`, `NEXT_PUBLIC_` and `REACT_APP_`. Search the built output for keys before release, and don't publish source maps that expose private code unless intended.

## Redirects and `postMessage`
- **Redirects.** Accept a `returnUrl` only as a same-origin relative path (starts with `/`, not `//` or `/\`); otherwise go to a default page.
- **Receiving.** Check `event.origin` against an exact allowlist and validate the data's shape.
- **Sending.** Name the target origin; never use `"*"` with sensitive data.

## Dependencies
- Run the project's audit (`npm audit`, `pnpm audit`, `yarn npm audit`, or the scanner in CI) and triage by whether the vulnerable code is reachable.
- Commit the lockfile. Before adding a package, check its maintenance, install scripts and size.

## Verify
- Inject `<img src=x onerror=alert(1)>` and `javascript:` URLs into every new rendering path; nothing runs.
- The CSP has no violations in report-only mode; no token is in web storage; state changes are refused without a CSRF token.
- External `returnUrl` values and foreign `postMessage` origins are ignored; the audit is triaged; the built bundle has no secrets.

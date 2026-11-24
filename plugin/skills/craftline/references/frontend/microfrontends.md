# Independently deployed frontend integration

**Use for:** microfrontends, runtime-loaded modules and independently deployed remotes. Don't propose this architecture for a site one team ships together.

## Decide whether, then how
- Use it only for a real need: separate teams with separate release cadences, or an incremental migration. A monorepo with shared packages ([packages-and-components.md](packages-and-components.md)) solves most "shared code" problems with less runtime risk.
- Pick the composition method for the constraint: build-time packages (simplest), Module Federation (shared runtime, shared dependencies), web components (framework boundary), or an iframe (strongest isolation, weakest integration).

## Runtime contract (write it down before coding)
- **Lifecycle.** Mount, update and unmount functions with typed props; unmount must remove listeners, timers and DOM it added.
- **Routing.** The host owns the URL; a remote receives its base path and navigates through a host-provided function, never by touching `history` directly.
- **Communication.** Typed props and events, or a small agreed event contract. No reaching into the host's store or framework internals.
- **Shared dependencies.** Declare the framework and design-system packages as shared singletons with compatible version ranges. Two copies of a framework in one page break context, hooks and theming.
- **Styles.** Scope remote CSS (prefixes, CSS modules or shadow DOM); a remote must never ship a global reset.
- **Auth.** The host passes a short-lived token or a token getter. No tokens in query strings, logs or persistent storage; handle expiry mid-session.
- **Failure.** Wrap each remote in an error boundary with a usable fallback when it fails to load or throws.

## Delivery
- Per-environment remote URLs come from configuration, with cache-busting file names and a short-cached manifest.
- CSP and CORS allow exactly the remote origins.
- Version skew is expected: host and remote deploy independently, so contracts change additively and old fields stay until every consumer has moved.

## Failure modes
- The remote is unreachable and the host renders a blank page.
- A remote upgrade changes a shared dependency's major version and the page breaks at runtime.
- Focus is lost after the remote unmounts; keyboard users land on `body`.

## Verify
- Repeated mount and unmount without leaks; host and remote at different versions; the remote offline; token expiry; back and forward navigation; focus after transitions.
- Styles of host and remote don't leak in either direction; CSP and CORS hold in a production-like environment; rollback of one remote alone.

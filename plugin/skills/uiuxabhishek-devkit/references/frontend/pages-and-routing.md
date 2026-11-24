# Pages, routes and feature areas

**Use for:** creating, renaming or reorganizing navigable screens or feature modules in a web application.

## Discover
1. Inspect the router, layout shell, navigation, page-title and breadcrumb conventions. Don't assume a framework.
2. Establish the route's parent layout, who may see it, its entry points, its loading, error, not-found and forbidden states, and whether it's public. For public pages, also apply [seo-and-metadata.md](seo-and-metadata.md).

## URL design
- Paths name resources with stable identifiers (`/invoices/inv_2041`), not positions or display names that change.
- No personal data or secrets in paths or query strings; they end up in logs, analytics and referrers.
- Shareable view state (tab, filters, page) goes in the query string; transient UI state does not.

## Decisions
- **Loading.** Split code per route. Start fetching the page's data as navigation begins, not after the component mounts, when the router supports it. Preload likely next routes only when it's cheap.
- **Guards.** A client guard redirects for a smoother experience. It doesn't protect data.
- **States.** Not found, forbidden, empty and error are different pages or panels. A gated page never flashes protected content before redirecting.
- **Errors.** Put an error boundary per route so one failing page keeps the shell and navigation usable.

## Accessibility after navigation
- Update the document title on every route change ("Invoice INV-2041 · Billing · App").
- Move focus to the page's main heading (or a skip target) and let assistive technology hear the new title. Without this, screen-reader users don't know the page changed.
- Restore scroll on back and forward; start at the top on new navigation.

## Renaming or moving routes
- Redirect the old path permanently (server-side for public pages), update internal links, menus, breadcrumbs, analytics event names and tests, and keep the redirect for as long as old links may exist.

## Verify
- Deep link, refresh, back and forward, not found, forbidden, signed-out, and slow or failed data.
- Title and focus change on navigation; keyboard-only navigation of menus and breadcrumbs; small viewports.
- Old URLs redirect; no console errors; route-level tests pass. Report any server-side menu or role setup the route needs.

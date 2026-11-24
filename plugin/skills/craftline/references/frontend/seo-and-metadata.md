# SEO and page metadata

**Use for:** public, indexable pages: titles and descriptions, canonical URLs, social previews, structured data, sitemaps and robots rules, rendering choices that affect indexing, and multilingual pages.

## Per page
- **Title.** Unique, roughly 50–60 characters, with the page's main topic first and the brand last.
- **Description.** One honest summary of about 150–160 characters. It shapes the search snippet, not the ranking.
- **Canonical.** One absolute `<link rel="canonical">` per page that points to the preferred URL. Drop tracking and sort parameters, and point duplicate paths to the original.
- **Robots.** `noindex` for gated, draft, internal search-result and thank-you pages. `robots.txt` isn't access control: protect private pages with auth.
- **Status codes.** Missing pages return a real 404 and moved pages a 301, not a 200 "not found" page.

## Social previews
- Open Graph: `og:title`, `og:description`, `og:type`, `og:url`, and `og:image` as an absolute URL of about 1200×630 with `og:image:alt`.
- Add `twitter:card` (`summary_large_image` for big images); other Twitter tags fall back to Open Graph.

## Structured data
- Use JSON-LD of a type that fits the page (`Organization`, `Product`, `Article`, `BreadcrumbList`, `FAQPage`) and describes only content visible on the page.
- Validate it with a rich-results testing tool before release.

## Sitemap and robots.txt
- The sitemap lists only canonical, indexable URLs with a truthful `lastmod`; reference it from `robots.txt`.
- Don't block CSS or JavaScript that pages need to render.

## Rendering and indexing
- Content and metadata that must be indexed belong in the initial HTML: server-rendered or statically generated. Client-only rendering can be indexed late or incompletely, and many social crawlers don't run JavaScript at all.
- Set metadata per route on the server; a client-side `document.title` change doesn't reach crawlers that skip scripts.

```html
<!-- Bad: every route ships the shell's title; the real one only appears after JS runs -->
<title>App</title>
<!-- Good: rendered per page on the server -->
<title>Wireless Headphones X2 · Acme</title>
<link rel="canonical" href="https://acme.example/products/x2">
```

## Performance
Core Web Vitals (LCP, INP, CLS) affect search and users alike. Diagnose and fix them with [optimize.md](../impeccable/reference/optimize.md).

## Multilingual pages
- One URL per language (path or subdomain), never a cookie-only switch. Set `<html lang>`.
- `hreflang` links are reciprocal across every language version and include `x-default`. Each language page's canonical points to itself, not to another language.

## Verify
- The raw HTML from `curl` or "view source" contains the title, description, canonical, robots and Open Graph tags for each route type.
- Social preview debuggers render the right card; structured data validates; the sitemap parses and lists only 200, indexable, canonical URLs.
- Gated and draft pages carry `noindex` or require auth; hreflang pairs resolve both ways.

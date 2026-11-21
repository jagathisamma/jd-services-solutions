# Website Performance & Quality Budget

## Objective
Keep the public site fast on mobile networks and low/mid-range Android devices while preserving accessibility, search visibility and direct contact conversion.

## Engineering budgets
These are target budgets, not measured current results:
- Initial HTML: aim under 45 KB compressed.
- First-party CSS + JS: aim under 60 KB compressed before adding a framework.
- Avoid render-blocking third-party font stylesheets and unnecessary JavaScript.
- Images: prefer WebP/AVIF where supported, include dimensions/aspect ratio, and lazy-load below-fold assets.
- Prevent layout shifts by reserving media dimensions and avoiding late-injected content.
- No horizontal overflow at 360, 390, 430, 768 and 1280 CSS px.
- Keep the critical contact actions available without blocking the content.

## Core Web Vitals targets
At the 75th percentile when real-user field data becomes available:
- LCP: <= 2.5 seconds
- INP: <= 200 milliseconds
- CLS: <= 0.1

These are targets only; do not report them as achieved without field or lab evidence.

## Repeatable verification
- Run HTML validation and JSON/YAML schema checks in CI.
- Use Lighthouse or PageSpeed Insights for mobile and desktop lab checks when available.
- Record test date, URL, device profile, network profile and report link.
- Check console errors, failed requests, image dimensions, font loading and layout shift.
- Verify actual Render deployment separately from branch CI.
- Browser visual QA must use the connected browser when available; otherwise record the limitation.

## Current known opportunity
The homepage previously imported Google Fonts CSS in the document head. This creates an external dependency before first render. The current issue branch removes that dependency and uses the system font stack. Further image and content architecture work must be measured before introducing additional runtime dependencies.

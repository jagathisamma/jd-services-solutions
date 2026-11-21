# Project architecture

## Current runtime
The public website is a static HTML site hosted by Render. GitHub main is the source of truth; Render auto-deploys commits pushed to that branch. The public site must remain usable without a database or server runtime.

## Product design system\nUse `data/config/brand.yml` as the single canonical source for JD colors, typography, tagline and usage principles. `docs/BRAND_GUIDE.md` describes application rules. Keep site contact/runtime settings in `data/config/site.yml`; do not duplicate brand color definitions. The public website, campaign pages and future private Admin UI should share these tokens.\n\n## Target architecture: flat-file first
Use human-readable files with clear responsibilities:

| Format | Responsibility | Location |
|---|---|---|
| JSON | Structured public records and machine-validated data | data/records/ |
| JSON Schema | Contracts for structured records | data/schema/ |
| YAML | Site settings, feature switches and non-secret configuration | data/config/ |
| Markdown | Operating manuals, service copy, FAQs and campaign content | docs/, content/ |
| Mermaid | Architecture, workflows, data relationships and funnel diagrams | docs/diagrams/*.mmd |

Keep records small, version-controlled, reviewable and validated in CI. Prefer stable IDs and explicit schema versions. Avoid duplicating the same business fact across multiple files; designate one canonical source and generate or reference other views from it.

## System layers
1. Experience: accessible, mobile-first public website and campaign landing pages.
2. Content: Markdown pages and FAQs, with reusable service descriptions.
3. Structured catalogue: JSON service/category records validated against JSON Schema.
4. Configuration: YAML settings for brand tokens, contact presentation, navigation and feature flags. Never store secrets here.
5. Governance: Issues, branches, PRs, AGENTS.md and CI.
6. Delivery: GitHub main → Render automatic static deployment.
7. Future private operations: CRM, enquiries, jobs, technician assignment, parts and payments only after a secure private data service is selected and implemented.

## Flat-file database boundaries
A public Git repository is suitable for public service catalogues, page metadata, FAQ content, non-sensitive campaign definitions and configuration. It is not a safe CRM database. Do not store customer or technician personal data in public JSON/YAML/Markdown files. Do not treat Git history as a privacy-safe deletion mechanism.

## Evolution path
- Phase 1 — Foundation: document conventions, add schemas and sample public records, validate data in CI.
- Phase 2 — Data-driven site: generate static pages from the catalogue/config/content while preserving the current visual quality and SEO.
- Phase 3 — Admin CMS: introduce authenticated editing and preview/review workflows; keep published content versioned.
- Phase 4 — Private CRM: select a private, access-controlled persistent store for customer enquiries, orders, technician dispatch and financial records. Define retention, backup, access and audit controls before launch.
- Phase 5 — Funnel and campaigns: campaign-specific Markdown/JSON definitions, UTM tracking, consent-aware analytics and measurable conversion events.\n- Phase 6 — Service operations: repair job cards, technician assignment/scheduling, pickup and onsite coordination, spare-parts stock ledger, estimates, invoices and job profitability.\n- Phase 7 — Business intelligence: reconciled service, sales, campaign, inventory and finance metrics with owner-focused dashboards.\n\nSee [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md) for issue-level capability mapping and completion state.

Do not skip the privacy boundary or add a backend merely to make the architecture look more complete.

# JD Product Roadmap — Capability Mapping

This roadmap adapts reusable product capabilities from the earlier Usha.Construction issue review to JD Services & Solutions. Usha's construction-specific requirements are reference material only; no Usha repository implementation is being changed or copied verbatim.

| JD issue | JD capability | Adaptation source / concept | Current status |
|---|---|---|---|
| #2 | Service-business operating platform epic | Usha #15 epic pattern | Open; overarching goal |
| #4 | Secure backend, database and deployment decision | Usha #16, #17, #32 architecture, migration and deployment concepts | Open; owner chose public Git flat files + separate private flat-file API; safe hosting/persistence decision still required |
| #5 | Owner-only Admin, customer records and enquiry-to-service funnel | Usha #18–#21 auth, CRM, activity/follow-up concepts | Open; not implemented |
| #6 | Spare-parts catalogue, stock ledger and supplier sourcing | Usha #29 procurement concepts, adapted for repair inventory | Open; not implemented |
| #7 | Repair job cards, technician assignment, pickup and onsite scheduling | Usha #22 project lifecycle and #21 field activity concepts | Open; not implemented |
| #8 | Repair estimates, invoices, receipts and job profitability | Usha #23, #24 and #29 finance/cost concepts | Open; not implemented |
| #9 | Campaign landing pages, UTM attribution and enquiry conversion analytics | Usha #30 content and #31 attribution/integration concepts | Open; not implemented |
| #10 | Owner-managed service pages, FAQs, offers and approved media | Usha #30 CMS/media concept | Open; not implemented |
| #11 | Deterministic AGENTS.md sync and CI drift guard | Usha #39 workflow automation request, correctly recreated for JD | Completed in PR #44 on 2026-11-25: managed context block, deterministic sync/check, allowlisted inventory, canonical business/privacy validation and CI drift tests |
| #13 | Brand system, website performance and scalable product foundation | New JD-specific product quality issue based on owner references | Open; official transparent logo is now in header/footer via merged PR #32; remaining performance/product-quality criteria are open |
| #15 | Customer feedback portal and owner-managed feedback inbox | Owner requirement for shareable feedback URL + private CMS inbox | Open; requires secure API/auth |
| #16 | Browser-first QA and verified release workflow | Owner's end-to-end delivery requirements | Open; release runbook, PR QA template, logo/asset CI gates and generated-context drift check are present; automated release-evidence validation and owner-device QA remain |
| #17 | Collection registry and JSON Schema metadata | Contributor: getwinharris | Open; schema foundation |
| #18 | Crash-safe private JSON/JSONL store | Contributor: getwinharris | Open; depends on #17/#4 |
| #19 | Owner-authenticated TypeScript API | Contributor: getwinharris | Open; depends on #17/#18; auth vertical slice #31 is sequenced separately |
| #20 | Schema-driven Admin collection UI | Contributor: getwinharris | Open; after #30/#31 and API |
| #21 | Accessories retail and shared stock ledger | Contributor: getwinharris; extends #6 | Open; after private store/API |
| #22 | Static pages from JSON/YAML/Markdown | Contributor: getwinharris; extends #10 | Open; publishing slice |
| #23 | Consented repair-status communication outbox | Contributor: getwinharris | Open; no real outbound messaging without approval |
| #24 | Private repair media storage | Contributor: getwinharris | Open; private media only |
| #25 | Encrypted private backup/restore and recovery | Contributor: getwinharris | Open; depends on #17–#19 |
| #26 | Generated Mermaid maps and project index | Contributor: getwinharris | Open; depends on #17 |
| #27 | Optional guardrailed owner assistant | Contributor: getwinharris | Open; last, after secure core |
| #28 | Production Android/Chrome blank-page and flashing defect | Owner-reported P0 | Open; compositor simplification merged in PR #32 and mobile footer fix in PR #33; Android Chrome/Incognito owner-device reproduction still unresolved; no root cause confirmed |
| #29 | Complete responsive website UI and conversion redesign | Owner request | Open; intentionally sequenced after #28 is verified stable |
| #30 | Responsive Admin login UI and dashboard shell | Contributor: getwinharris | Open; next visible Admin slice after #28 is verified stable; UI only, no production data access |
| #31 | Minimal secure owner authentication | Contributor: getwinharris | Open; follows #30; private runtime provisioning requires separate owner approval |

## Completed in JD repository
- #3 public website refresh issue is closed; PR #12 was merged and the static website was deployed to Render in the prior verified release.
- Flat-file public data foundation: YAML site config, JSON service catalogue, JSON Schema, architecture/operating docs and CI validation.
- Public site currently routes enquiries to Call/WhatsApp. It does not persist customer records.

## Not completed
- Secure backend and private persistent data store.
- Admin authentication, Admin UI, CRM and enquiry persistence.
- Service job cards, technician scheduling/dispatch and customer status updates.
- Inventory/stock ledger and supplier workflows.
- Estimates, invoices, receipts, payments and job profitability.
- Campaign CMS, UTM attribution and conversion analytics.
- Generated Mermaid maps and project index.
- Automated release-evidence validation and owner-device browser QA.
- Full browser visual QA and measured performance baseline.

## Usha issue handling note
Usha issues #38 and #39 were mistakenly created in that repository and then closed as Not Planned, not deleted. The correct JD work is tracked here. No further changes should be made to Usha.Construction.

## Verified delivery snapshot — 2026-11-25

This is a point-in-time evidence record, not a live status feed. It records the repository immediately after PR #44 and before this roadmap-only refresh; recheck GitHub and Render after subsequent commits.

- GitHub default branch: `main`; implementation commit reviewed: `81b46be732d9d5061ea34365bfaaf429389fe3bd` (PR #44, deterministic agent-context generator and CI drift guard).
- Open pull requests: none. Open issues: 25 after #11 was completed and closed by PR #44.
- GitHub Actions PR CI #44 and main CI #45 both succeeded. Main CI #45 ran on the exact implementation commit above and passed the generated-context check, agent-context regression tests, public-site smoke tests, metadata/accessibility tests, schema/YAML validation and HTML validation.
- Render Static Site `jdservicessolutions` tracks `main` with automatic deployment on commit. Deployment `dep-dc35frojo6nc73eaa8og` is `live` on the exact implementation commit above. Production URL: https://jdservicessolutions.onrender.com. This roadmap-only refresh will trigger a subsequent documentation deployment.
- PR #44 added `.github/scripts/sync_agent_context.py`, a managed AGENTS.md block, deterministic `--sync`/`--check`, allowlisted directory/script inventory, canonical business/privacy validation and regression tests. README documents the commands; CI fails on generated-context drift.
- PR #39 continues to guard canonical Call/WhatsApp paths, required sections, internal anchors, responsive metadata and local assets. PR #43 added SEO and image-alt metadata checks. These are source-level regression tests, not conversion measurements or browser QA.
- Official JD logo is present in `assets/jd-logo.png` and referenced by the current page header/footer (PRs #32 and #36). The old logo-missing note in #28 is historical and has been corrected in that issue.
- Issue #28 remains open for the owner-reported Android Chrome/Incognito blue-black rendering problem. Remote cloud-browser inspection recorded on 2026-11-22 was stable at 390×844 and 1280×800, but does not establish owner-device stability or a confirmed root cause. No fresh Android visual QA is claimed in this snapshot.
- Current public contact is `8940454260`; CI guards the canonical contact forms and rejects the superseded number in tracked public source/config files.
- Issue #11 is completed: generated-section sync/check, idempotence, missing/malformed input, stable ordering, sensitive-path exclusion and human-authored text preservation are covered by CI.
- Render pull-request previews remain disabled. A successful static deployment is release evidence only, not proof of client-side rendering or conversion.

## Recommended execution order

1. **#28 — production reliability:** obtain Android Chrome/Incognito device evidence, isolate paint/compositing/cache behavior, and implement only a confirmed root-cause fix.
2. **#30 → #31 — Admin foundation:** build the branded responsive shell, then real server-side owner authentication. Keep the shell non-operational and private data inaccessible until auth is proven.
3. **#4 → #17 → #18 → #25 → #19 — private data/security foundation:** document the flat-file architecture, collection contracts, crash-safe private JSON/JSONL persistence, encrypted backup/restore, then the typed owner-authenticated API. No private records in this public repository.
4. **#5 → #7 → #6/#21 → #8 — service operations:** enquiries/customers, repair job cards and technician dispatch, separate retail accessories from repair stock, then estimates/invoices/payments and job profitability.
5. **#10/#22 → #9 → #15/#23 — growth and retention:** owner-managed content, local service/campaign landing pages and UTM attribution, then feedback and consented status communications. Count a Call/WhatsApp click separately from a genuine enquiry and a completed paid job.
6. **#26/#27 — governance and intelligence:** generate Mermaid maps from the collection registry, then only later consider a read-only/approval-gated owner assistant. #11's deterministic agent-context sync/check is completed in PR #44.

## Business measurement baseline
No verified enquiry, conversion, repair, revenue, margin, campaign-spend or technician-utilisation data is currently available in this repository. Do not report numeric performance until a private CRM and reconciled operating records exist. Initial weekly KPIs should be defined as: genuine enquiries by source, response time, qualified leads, jobs booked, jobs completed, revenue collected, parts/technician cost, gross margin, overdue follow-ups, and campaign spend/CPL/ROI where actual spend is entered.

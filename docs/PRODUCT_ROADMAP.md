# JD Product Roadmap — Capability Mapping

This roadmap adapts reusable product capabilities from the earlier Usha.Construction issue review to JD Services & Solutions. Usha's construction-specific requirements are reference material only; no Usha repository implementation is being changed or copied verbatim.

| JD issue | JD capability | Adaptation source / concept | Current status |
|---|---|---|---|
| #2 | Service-business operating platform epic | Usha #15 epic pattern | Open; overarching goal |
| #4 | Secure backend, database and deployment decision | Usha #16, #17, #32 architecture, migration and deployment concepts | Open; design/decision work remains |
| #5 | Owner-only Admin, customer records and enquiry-to-service funnel | Usha #18–#21 auth, CRM, activity/follow-up concepts | Open; not implemented |
| #6 | Spare-parts catalogue, stock ledger and supplier sourcing | Usha #29 procurement concepts, adapted for repair inventory | Open; not implemented |
| #7 | Repair job cards, technician assignment, pickup and onsite scheduling | Usha #22 project lifecycle and #21 field activity concepts | Open; not implemented |
| #8 | Repair estimates, invoices, receipts and job profitability | Usha #23, #24 and #29 finance/cost concepts | Open; not implemented |
| #9 | Campaign landing pages, UTM attribution and enquiry conversion analytics | Usha #30 content and #31 attribution/integration concepts | Open; not implemented |
| #10 | Owner-managed service pages, FAQs, offers and approved media | Usha #30 CMS/media concept | Open; not implemented |
| #11 | Deterministic AGENTS.md sync and CI drift guard | Usha #39 workflow automation request, correctly recreated for JD | Open; not implemented |
| #13 | Brand system, website performance and scalable product foundation | New JD-specific product quality issue based on owner references | Open; official logo restoration in active PR, broader quality criteria remain |
| #15 | Customer feedback portal and owner-managed feedback inbox | Owner requirement for shareable feedback URL + private CMS inbox | Open; requires secure API/auth |
| #16 | Browser-first QA and verified release workflow | Owner's end-to-end delivery requirements | Open; release runbook, PR gates and CI asset checks in active PR |
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
| #28 | Production Android/Chrome blank-page and flashing defect | Owner-reported P0 | Open; compositing simplification in active PR; target-device verification still required |
| #29 | Complete responsive website UI and conversion redesign | Owner request | Open; follow #28, use official assets and approved imagery |
| #30 | Responsive Admin login UI and dashboard shell | Contributor: getwinharris | Open; immediate admin UI slice after public-site stability |
| #31 | Minimal secure owner authentication | Contributor: getwinharris | Open; after #30; no default credentials or public client-side auth |

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
- Automatic AGENTS.md generation/drift check.
- Full browser visual QA and measured performance baseline.

## Usha issue handling note
Usha issues #38 and #39 were mistakenly created in that repository and then closed as Not Planned, not deleted. The correct JD work is tracked here. No further changes should be made to Usha.Construction.

# Agent instructions

## Project and authority
This repository contains the official website and supporting digital operating system for JD Services & Solutions, Erode. ChatGPT is the autonomous product and engineering lead for routine, reversible project work under docs/OPERATING_MODEL.md.

- Make routine product, UX, architecture, documentation, issue-priority, implementation, test and release decisions without asking the owner for approval.
- Do not ask the owner to repeat known project context. Use repository files, issues, PRs and deployment state first.
- Ask only for unavailable business facts, changed business promises, private/customer data handling, credentials/secrets, paid services or recurring costs, destructive/irreversible actions, legal/compliance decisions, or material changes to agreed scope.
- When the owner provides screenshots or references, implement the relevant correction directly and report the result.

## Delivery workflow
- Never commit directly to main.
- Inspect the latest main, related issues, open PRs, CI and Render status before starting.
- Track substantive work through GitHub Issues, focused branches and PRs.
- Run the available automated checks and fix failures before merge.
- Perform responsive/accessibility/browser QA when the connected browser is available. If browser access is unavailable, state that visual QA is blocked; never claim it passed.
- Routine website changes may be merged to main after required checks pass, the work is within the standing authority, and no unresolved high-severity issue remains.
- Render auto-deploys main. Do not manually trigger a duplicate deploy when autoDeploy is enabled.
- Verify Render reports the new deployment as live before claiming production release.
- Update docs and report the exact PR, commit, checks and deployment status.

## Data architecture and privacy
- Follow docs/ARCHITECTURE.md, docs/FILE_DATABASE.md and docs/OPERATING_MODEL.md.
- Use `data/config/brand.yml` as the canonical brand-token source and `data/config/site.yml` for non-secret site/runtime settings. Use JSON in data/records for structured public records, JSON Schema in data/schema, Markdown for documentation/content, and Mermaid source in docs/diagrams.\n- Keep `docs/BRAND_GUIDE.md`, `docs/PERFORMANCE.md` and `docs/PRODUCT_ROADMAP.md` current when changing design standards, performance gates or product scope.
- Validate structured records in CI. Keep schemaVersion and stable record IDs.
- This repository is public: never commit customer/technician personal data, enquiries, repair history, device identifiers, payment data, passwords, API keys, tokens or secrets.
- The flat-file repository is for public catalogue/content/config only, not CRM. A private CRM requires private access-controlled persistent storage, backups and retention controls.
- Never place GitHub/Render credentials in browser code or simulate successful persistent enquiry storage.

## Engineering quality
- Inspect the existing project before changing files and preserve conventions.
- Keep changes focused, accessible, responsive and mobile-first.
- Do not invent business details, service guarantees, prices, availability, certifications or testimonials.
- Do not add paid services or incur costs without explicit owner approval.

## Brand
- Business: JD Services & Solutions
- Location: Erode, Tamil Nadu
- Contact: 8940454360 (label as "Call & WhatsApp" in public content)
- Tagline: "Service Today... Smile Tomorrow..."
- Palette: #071D55, #075BD8, #FF6A00, #FFC400, #FFFFFF.
- Reuse the official uploaded logo unchanged when it is available. Never recreate an approximation.

## Communication
Be concise, truthful and action-oriented. Report what changed, what was verified, what is live, and any remaining blocker.
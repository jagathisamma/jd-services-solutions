# Autonomous project operating model

## Mission
Operate JD Services & Solutions as a continuously improving, customer-friendly service business website and its supporting digital operating system. ChatGPT acts as the autonomous product and engineering lead for routine, reversible project work.

## Decision authority
ChatGPT owns routine decisions for:
- Product direction, prioritisation, UX, responsive design and accessibility.
- Technical architecture, repository structure, data schemas and documentation.
- Issue creation/refinement, focused branches, implementation and pull requests.
- CI configuration, automated validation, defect correction and release notes.
- Browser/device verification when the connected browser is available.
- Routine releases to the existing Render static site after all required checks pass.

Do not ask the owner to approve ordinary engineering choices, copy/layout refinements, documentation, test fixes, issue prioritisation or routine releases already covered by this operating model.

Ask the owner only when a decision requires unavailable business facts, changes a real-world business promise, exposes or processes private customer data, introduces paid services or new recurring costs, requires credentials/secrets, is destructive or irreversible, changes legal/compliance posture, or materially changes the agreed business scope.

When a browser screenshot or reference is supplied by the owner, translate it into concrete implementation changes without asking them to restate the existing project context.

## Delivery loop
1. Inspect the current repository, open issues, pull requests, CI state and Render configuration.
2. Turn a concrete improvement into an issue (or update the relevant existing issue).
3. Create a focused branch from the latest appropriate base.
4. Implement the smallest coherent change and update docs/data contracts.
5. Run local/static validation where available; use CI as the authoritative automated gate.
6. Inspect the rendered experience at mobile and desktop sizes when browser access is available. If it is unavailable, record the limitation honestly and use all available static checks; do not claim visual QA passed.
7. Fix failures and repeat validation.
8. Merge routine website changes to main only when checks are green, the change is within the standing authority above, and no unresolved high-severity issue remains.
9. Render watches main and auto-deploys. Do not trigger a duplicate manual deploy when auto-deploy is enabled.
10. Verify the latest Render deployment reports live, then smoke-check the public URL where possible.
11. Report the branch/PR, change summary, checks, deployment commit/status and any remaining limitations.

## Source of truth
- AGENTS.md: concise operating rules for coding agents.
- docs/: architecture, workflows, data contracts and runbooks.
- data/config/: non-secret project configuration in YAML.
- data/records/: structured, version-controlled public/business catalogue records in JSON.
- data/schema/: JSON Schema contracts for structured records.
- content/: editorial pages and campaign copy in Markdown.
- docs/diagrams/: Mermaid source diagrams.
- GitHub Issues and PRs: auditable work queue and change history.
- Render: deployment runtime; Git main remains the release source of truth.

## Data safety
This repository is public. Never commit customer names, phone numbers, addresses, device identifiers, repair histories, payment information, passwords, access tokens, technician private contact details or other personal/confidential operational records. The flat-file database in this repository is only for public catalogue/configuration and non-sensitive reference data. Customer CRM/order data requires a private, access-controlled and backed-up store before collection is implemented.

## Static-site boundary
The current production service is a Render Static Site. A browser form cannot securely append records to repository files. Never put GitHub/Render credentials in browser code or simulate a successful saved enquiry. Until a private write API and secure storage are deliberately introduced, enquiry CTAs should open Call/WhatsApp and clearly communicate the next step.

## Product quality and growth loop
- Treat public UX, brand consistency, page performance, conversion funnel, private operations and business intelligence as one product roadmap. Do not equate a homepage redesign with completion of the operating platform.
- Use `docs/PRODUCT_ROADMAP.md` to distinguish delivered foundations from capabilities that remain open.
- Measure page performance and conversion with repeatable evidence; label budgets as targets until verified.
- Keep public marketing content and private customer/repair/finance data separated.

## Definition of done
- Acceptance criteria are met and no known critical defect remains.
- Relevant JSON/YAML/Markdown/Mermaid files are consistent.
- CI passes.
- Responsive and accessibility checks are performed where tools allow.
- No secrets, fabricated business claims or private customer data are introduced.
- Deployment is verified before describing a change as live.
- Docs and issue/PR status reflect the actual result.

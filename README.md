# JD Services & Solutions

Official website and digital operating system for JD Services & Solutions, Erode.

Tagline: **Service Today... Smile Tomorrow...**

Public contact: **8940454260** (Call & WhatsApp).

## Project operating model
ChatGPT acts as the autonomous product and engineering lead for routine project improvements. See [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md) for decision authority, issue-driven development, quality gates and release workflow.

## Brand and quality standards
- [Brand and UI guide](docs/BRAND_GUIDE.md)
- [Canonical brand tokens](data/config/brand.yml)
- [Performance budgets and verification](docs/PERFORMANCE.md)
- [Product capability roadmap](docs/PRODUCT_ROADMAP.md)

## Architecture
- [Architecture overview](docs/ARCHITECTURE.md)
- [Flat-file database conventions](docs/FILE_DATABASE.md)
- [Project workflow diagram](docs/diagrams/project-workflow.mmd)
- Non-secret YAML configuration: data/config/
- Structured public JSON records: data/records/
- JSON Schema contracts: data/schema/
- Editorial and campaign Markdown: content/

## Privacy boundary
This public repository stores only public website content, catalogue data and non-secret configuration. Do not store customer enquiries, repair histories, technician personal data, credentials or payment details here. CRM requires a separate private, access-controlled persistent store.

## Deployment
The Render Static Site tracks the GitHub main branch and auto-deploys commits after merge. A successful CI run alone does not mean a production deploy is live; verify the Render deployment status.

## Release evidence
- [Release verification runbook](docs/RELEASE_RUNBOOK.md)
- [Machine-readable release evidence template](docs/RELEASE_EVIDENCE_TEMPLATE.yml)
- Validate the PR checklist and evidence structure: python3 .github/scripts/check_release_workflow.py
- Test the validator: python3 -m unittest discover -s tests -p 'test_release_workflow.py' -v

## Agent context maintenance

AGENTS.md contains a generated project-context block. Keep human-authored policy outside its markers; update the generated block only through the deterministic script.

- Sync after approved source or roadmap changes: python3 .github/scripts/sync_agent_context.py --sync
- Verify without writing (required in CI): python3 .github/scripts/sync_agent_context.py --check
- Run the focused tests: python3 -m unittest discover -s tests -p 'test_agent_context.py' -v

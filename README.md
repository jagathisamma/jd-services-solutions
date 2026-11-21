# JD Services & Solutions

Official website and digital operating system for JD Services & Solutions, Erode.

Tagline: **Service Today... Smile Tomorrow...**

## Project operating model
ChatGPT acts as the autonomous product and engineering lead for routine project improvements. See [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md) for decision authority, issue-driven development, quality gates and release workflow.

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
# Flat-file database conventions

## Directory contract
- data/config/site.yml: non-secret site configuration.
- data/records/services.json: canonical public service catalogue.
- data/schema/services.schema.json: JSON Schema for the service catalogue.
- content/: editorial Markdown pages and campaign content.
- docs/diagrams/: Mermaid source diagrams.

## Record rules
- UTF-8 only; use two-space JSON/YAML indentation.
- JSON must be valid JSON (no comments or trailing commas).
- Every structured dataset includes a schemaVersion.
- Every record has a stable, human-readable id.
- Use ISO 8601 dates and explicit currency codes if future public pricing is ever approved.
- Never commit private customer, employee or technician data.
- Do not place credentials, API keys, tokens or environment values in data files.
- Make changes through an issue and pull request; review the diff as data, not only as code.

## Current service catalogue
The initial catalogue is descriptive only. It does not claim that a technician, part, pickup slot, price or appointment is currently available. Confirm each enquiry through the established Call & WhatsApp channel.

## Editing workflow
1. Update the canonical data/config/content file.
2. Update its JSON Schema when the data contract changes.
3. Update relevant documentation and Mermaid diagrams.
4. Run CI and inspect the generated/public experience when the data is wired into the site.
5. Review for invented claims, privacy leaks and duplicate facts.
6. Merge only after required checks pass.

## CRM is not part of this flat-file database
Do not add actual enquiries, customer records, device serial numbers, repair history, payments, technician schedules or private contact details here. The repository is public and Git history retains prior versions. CRM must use a private, access-controlled persistent service with backups, retention rules and auditability.

#!/usr/bin/env python3
"""Validate the PR release checklist and machine-readable release evidence template."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / ".github" / "pull_request_template.md"
RUNBOOK_PATH = ROOT / "docs" / "RELEASE_RUNBOOK.md"
EVIDENCE_PATH = ROOT / "docs" / "RELEASE_EVIDENCE_TEMPLATE.yml"

REQUIRED_TEMPLATE_HEADINGS = (
    "## Summary",
    "## Related issue(s)",
    "## Scope and risk",
    "## Automated validation",
    "## Pre-merge browser QA",
    "## Deployment and post-deploy QA",
    "## Release evidence",
)
REQUIRED_TEMPLATE_TEXT = (
    "PASS / FAIL / BLOCKED / NOT APPLICABLE (non-visual only)",
    "Merge commit SHA",
    "CI run URL and conclusion",
    "Render deployment ID, status and deployed commit SHA",
    "Production URL",
    "Known limitations",
)
REQUIRED_RUNBOOK_TEXT = (
    "## Release states",
    "## Required release evidence",
    "## Machine-readable release evidence",
    "## Feedback-to-issue loop",
    "## Deployment configuration",
    "pre-merge browser QA",
    "post-deploy browser QA",
    "exact merge commit",
)
REQUIRED_EVIDENCE_FIELDS = (
    r"(?m)^release:\s*$",
    r"(?m)^  issue_urls:\s*\[\]\s*$",
    r"(?m)^  branch:\s*null\s*$",
    r"(?m)^  pr_url:\s*null\s*$",
    r"(?m)^  merge_commit_sha:\s*null\s*$",
    r"(?m)^  ci:\s*$",
    r"(?m)^    run_url:\s*null\s*$",
    r"(?m)^    conclusion:\s*null\s*$",
    r"(?m)^  render:\s*$",
    r"(?m)^    deployment_id:\s*null\s*$",
    r"(?m)^    status:\s*null\s*$",
    r"(?m)^    deployed_commit_sha:\s*null\s*$",
    r"(?m)^    production_url:\s*null\s*$",
    r"(?m)^  browser_qa:\s*$",
    r"(?m)^    pre_merge:\s*$",
    r"(?m)^    post_deploy:\s*$",
    r"(?m)^  known_limitations:\s*\[\]\s*$",
)


def validate(template: str, runbook: str, evidence: str) -> list[str]:
    errors = []
    for heading in REQUIRED_TEMPLATE_HEADINGS:
        if heading not in template:
            errors.append(f"PR template is missing heading: {heading}")
    for phrase in REQUIRED_TEMPLATE_TEXT:
        if phrase not in template:
            errors.append(f"PR template is missing release field or status: {phrase}")
    for phrase in REQUIRED_RUNBOOK_TEXT:
        if phrase not in runbook:
            errors.append(f"release runbook is missing required guidance: {phrase}")
    for pattern in REQUIRED_EVIDENCE_FIELDS:
        if not re.search(pattern, evidence):
            errors.append(f"release evidence template is missing required YAML field: {pattern}")
    for section in ("pre_merge", "post_deploy"):
        pattern = rf"(?m)^      status: NOT_RUN\s*$"
        section_match = re.search(rf"(?ms)^    {section}:\s*\n(.*?)(?=^    [a-z_]+:|\Z)", evidence)
        if not section_match or not re.search(pattern, section_match.group(1)):
            errors.append(f"{section} browser QA must default to NOT_RUN, never PASS")
    return errors


def main() -> int:
    paths = (TEMPLATE_PATH, RUNBOOK_PATH, EVIDENCE_PATH)
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    if missing:
        print("RELEASE WORKFLOW CHECK FAILED: missing " + ", ".join(missing), file=sys.stderr)
        return 1

    contents = [path.read_text(encoding="utf-8") for path in paths]
    errors = validate(*contents)
    if errors:
        for error in errors:
            print(f"RELEASE WORKFLOW CHECK FAILED: {error}", file=sys.stderr)
        return 1

    print("Release workflow checks passed: PR checklist, runbook and evidence template are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

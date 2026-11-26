"""Regression tests for release checklist and evidence-template validation."""

import importlib.util
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "scripts"
    / "check_release_workflow.py"
)
SPEC = importlib.util.spec_from_file_location("check_release_workflow", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

VALID_TEMPLATE = """## Summary
## Related issue(s)
## Scope and risk
## Automated validation
## Pre-merge browser QA
Status: PASS / FAIL / BLOCKED / NOT APPLICABLE (non-visual only)
## Deployment and post-deploy QA
## Release evidence
Merge commit SHA
CI run URL and conclusion
Render deployment ID, status and deployed commit SHA
Production URL
Known limitations
"""

VALID_RUNBOOK = """## Release states
## Required release evidence
## Machine-readable release evidence
Use the exact merge commit.
Pre-merge browser QA and post-deploy browser QA.
## Feedback-to-issue loop
## Deployment configuration
"""

VALID_EVIDENCE = """release:
  issue_urls: []
  branch: null
  pr_url: null
  merge_commit_sha: null
  ci:
    run_url: null
    conclusion: null
  render:
    deployment_id: null
    status: null
    deployed_commit_sha: null
    production_url: null
  browser_qa:
    pre_merge:
      status: NOT_RUN
      viewports: []
      evidence_urls: []
    post_deploy:
      status: NOT_RUN
      viewports: []
      evidence_urls: []
  known_limitations: []
"""


class ReleaseWorkflowTests(unittest.TestCase):
    def test_complete_release_contract_is_accepted(self):
        self.assertEqual(CHECKER.validate(VALID_TEMPLATE, VALID_RUNBOOK, VALID_EVIDENCE), [])

    def test_missing_browser_status_options_are_rejected(self):
        errors = CHECKER.validate(
            VALID_TEMPLATE.replace(
                "PASS / FAIL / BLOCKED / NOT APPLICABLE (non-visual only)", "PASS only"
            ),
            VALID_RUNBOOK,
            VALID_EVIDENCE,
        )
        self.assertTrue(any("status" in error for error in errors))

    def test_missing_render_commit_field_is_rejected(self):
        errors = CHECKER.validate(
            VALID_TEMPLATE,
            VALID_RUNBOOK,
            VALID_EVIDENCE.replace("  deployed_commit_sha: null\n", ""),
        )
        self.assertTrue(any("deployed_commit_sha" in error for error in errors))

    def test_browser_qa_defaults_must_not_claim_pass(self):
        evidence = VALID_EVIDENCE.replace("status: NOT_RUN", "status: PASS", 1)
        errors = CHECKER.validate(VALID_TEMPLATE, VALID_RUNBOOK, evidence)
        self.assertTrue(any("pre_merge browser QA must default to NOT_RUN" in error for error in errors))

    def test_missing_runbook_gate_is_rejected(self):
        errors = CHECKER.validate(
            VALID_TEMPLATE,
            VALID_RUNBOOK.replace("## Deployment configuration", ""),
            VALID_EVIDENCE,
        )
        self.assertTrue(any("Deployment configuration" in error for error in errors))

    def test_missing_template_heading_is_rejected(self):
        errors = CHECKER.validate(
            VALID_TEMPLATE.replace("## Release evidence\n", ""),
            VALID_RUNBOOK,
            VALID_EVIDENCE,
        )
        self.assertTrue(any("## Release evidence" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

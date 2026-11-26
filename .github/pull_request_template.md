## Summary
<!-- What changed, why, and visible user impact? -->

## Related issue(s)
<!-- Link related issues; do not close a parent issue for partial work. -->

## Scope and risk
- [ ] Focused issue-linked change; dependencies reviewed
- [ ] No unrelated open issue silently dropped
- [ ] No secrets, customer PII or unapproved business claims
- [ ] Brand assets are the actual approved files, not approximations

## Automated validation
- [ ] CI checks pass
- [ ] HTML, JSON, YAML and asset references validate
- [ ] Focused regression tests pass
- [ ] Accessibility and performance impact reviewed

## Pre-merge browser QA
- Status: PASS / FAIL / BLOCKED / NOT APPLICABLE (non-visual only)
- Viewports: 360 / 390 / 430 / 768 / 1024 / 1280 / 1440 as relevant
- [ ] Screenshots/evidence attached when visual QA applies
- [ ] Navigation, CTAs, images, console and network checked when applicable
- [ ] Android-specific known defects reproduced or explicitly remain open

## Deployment and post-deploy QA
- [ ] Merge commit recorded
- [ ] Render deployment is LIVE on the exact merge commit
- [ ] Production URL opened in a fresh browser context
- [ ] Mobile and desktop smoke tests passed when a visible change ships
- [ ] Screenshots/evidence and deployment ID recorded
- [ ] Remaining limitations and linked issues listed

## Release evidence
Complete after merge; use [the machine-readable evidence template](../docs/RELEASE_EVIDENCE_TEMPLATE.yml).
- Issue(s):
- Branch:
- PR URL:
- Merge commit SHA:
- CI run URL and conclusion:
- Render deployment ID, status and deployed commit SHA:
- Production URL:
- Pre-merge browser QA: status, viewports and evidence links
- Post-deploy browser QA: status, viewports and evidence links
- Known limitations:

## Deployment notes
<!-- Render configuration or environment changes; do not trigger duplicate manual deploys when auto-deploy is enabled. -->

# Release verification runbook

## Release states
A release is complete only when every required gate below is evidenced. Render's `live` status alone is not a product QA result.

1. **Intake:** identify owner feedback, screenshots/annotations, customer feedback, and all related open issues. Remove personal data from public issue evidence.
2. **Triage:** reproduce actual/expected behavior, severity, scope, acceptance criteria, dependencies and owner. Keep existing issues from all contributors; link related tickets rather than duplicating or silently replacing them.
3. **Plan:** select the highest-priority dependency-ready issue. Create one focused branch and link its issue in the PR.
4. **Implement:** make a coherent, reviewable change. Update brand/content/schema/docs when affected. Never claim an asset is integrated until the actual asset is committed and rendered.
5. **Automated gates:** HTML validation, schema/YAML checks, asset existence/reference checks, accessibility and focused regression tests. Fix failures before review.
6. **Code review:** inspect the complete diff for correctness, security/privacy, responsive behavior, accessibility, performance and fabricated claims. Record unresolved findings.
7. **Pre-merge browser QA:** test 360, 390, 430, 768, 1024, 1280 and 1440 widths where applicable. Capture screenshots; verify navigation, CTAs, images, console and network. Status must be PASS, FAIL or BLOCKED with evidence.
8. **Merge:** merge only after CI and review pass and no unresolved release-blocking defect remains.
9. **Render:** wait for the auto-deploy triggered by the merge. Do not trigger a duplicate manual deploy. Match the live deployment's commit SHA to the merge commit.
10. **Post-deploy browser QA:** open the production URL in a fresh browser context; verify page content, assets, interactions, responsive states, console/network and stability. A cloud-browser pass does not erase a reproducible owner-device failure.
11. **Closeout:** close only acceptance criteria actually met. Keep unresolved criteria/issues open and create linked follow-ups where needed.

## Required release evidence
Record in the PR/release summary:
- Issue(s), branch and PR URL
- Merge commit SHA
- CI workflow run URL and conclusion
- Render deployment ID, status and deployed commit SHA
- Production URL
- Pre-merge and post-deploy browser QA status, viewport list and screenshot/evidence links
- Known limitations and remaining open issue numbers

## Feedback-to-issue loop
- Owner screenshots, screen recordings and annotations become reproducible bug reports with observed/expected behavior and viewport/device details.
- Customer feedback is handled only through a secure backend and owner-only CMS. The current static site must not claim to persist submissions.
- Do not store customer names, phone numbers, addresses, device IDs, repair details or payment data in this public repository.
- Prioritise production-blocking defects, then broken brand/critical journeys, then conversion and visual improvements, then operational platform slices.

## Deployment configuration
The current Render Static Site watches `main` and auto-deploys commits. Confirm its configured trigger and available GitHub check-gating support before changing settings. Do not claim checksPass is enabled unless Render reports it.

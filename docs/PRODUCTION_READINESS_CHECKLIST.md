# Production Readiness Checklist

Research OS is a research tool / proof-of-concept starter kit. Complete this checklist before using it for production, shared, institutional, regulated, or public-sector work.

## Secrets And Configuration

- [ ] Keep `.env` files and secrets out of Git.
- [ ] Define environment-specific settings for host, port, storage path, logging, and allowed origins.
- [ ] Remove placeholder repository and metadata values before publication.
- [ ] Document who owns deployment configuration.

## Network, CORS, And TLS

- [ ] Bind public deployments behind a reverse proxy.
- [ ] Enable TLS with managed certificate renewal.
- [ ] Restrict CORS to approved origins.
- [ ] Confirm services are not exposed beyond the intended network.
- [ ] Add request size limits for file uploads.

## Authentication And Access Control

- [ ] Add authentication for shared deployments.
- [ ] Add authorization rules for datasets, notes, PDFs, exports, reports, and API routes.
- [ ] Review filesystem permissions on `storage/`.
- [ ] Define admin and user roles if more than one person can use the system.

## Audit Logs

- [ ] Log uploads, downloads, exports, report generation, PDF downloads, note creation, and API access.
- [ ] Avoid logging sensitive data values.
- [ ] Protect logs from unauthorized access.
- [ ] Define log retention and review procedures.

## Backups And Recovery

- [ ] Back up `storage/library.db`, `storage/papers/`, and `storage/exports/` if they contain real data.
- [ ] Test restore procedures.
- [ ] Define retention and deletion schedules.
- [ ] Document how to clear demo data and user data.

## Dependency And Supply-Chain Scanning

- [ ] Pin deployment dependencies.
- [ ] Run vulnerability scans for Python dependencies.
- [ ] Review licenses for dependencies.
- [ ] Generate or maintain an SBOM if required by the deploying organization.
- [ ] Add CI checks for tests, linting, and dependency review.

## Accessibility Audit

- [ ] Test keyboard-only workflows.
- [ ] Test with screen readers.
- [ ] Check color contrast and focus states.
- [ ] Provide text/table alternatives for complex charts where needed.
- [ ] Validate against WCAG 2.1 AA, Section 508, and EN 301 549 if applicable.

## AI / Automated Assistance Review

- [ ] Review the deterministic methods-coach outputs for accuracy and domain fit.
- [ ] Confirm users understand outputs are drafting assistance, not final professional decisions.
- [ ] Add human review requirements for reports and interpretation.
- [ ] Reassess AI governance if external AI models are added.
- [ ] Review EU AI Act obligations for regulated or public-sector use cases.

## Legal And Privacy Review

- [ ] Review GDPR, institutional privacy, public-sector, and research ethics obligations.
- [ ] Define lawful basis, consent, or approval requirements where applicable.
- [ ] Review data minimization, retention, deletion, and data subject rights.
- [ ] Review education, health, financial, legal, infrastructure, or public-sector rules if relevant.
- [ ] Confirm report exports do not disclose protected or confidential data.

## Security Review

- [ ] Perform threat modeling for the intended deployment.
- [ ] Add rate limiting and abuse protections for exposed APIs.
- [ ] Review PDF upload and download handling.
- [ ] Run application security testing before internet exposure.
- [ ] Document incident response procedures.

## Research And Methods Review

- [ ] Verify statistical methods are appropriate for the dataset and research question.
- [ ] Review assumptions, diagnostics, limitations, and effect sizes.
- [ ] Avoid causal claims unless the study design supports them.
- [ ] Require subject-matter review before publication or operational decisions.

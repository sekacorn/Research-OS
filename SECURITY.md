# Security

Research OS is a local-first research tool. It is not hardened as a production, multi-user, regulated, or internet-facing service by default.

## Reporting Vulnerabilities

Please report security issues privately instead of opening a public issue with exploit details.

No security email, maintainer email, or private vulnerability reporting contact is present in this repository. If this project is hosted on a platform that supports private vulnerability reports, use that feature. If no private channel is available, open a minimal public issue that says a vulnerability exists and asks for a private contact, but do not include sensitive details, exploit code, private data, or destructive steps.

Include when possible:

- affected component or file path;
- short description of the issue;
- safe reproduction steps;
- likely impact;
- suggested fix or mitigation, if known.

## Data Not To Use In Demos

Use the synthetic sample dataset in `data/sample_students.csv` or other fake/de-identified data for demos.

Do not use demo deployments with:

- personal data or direct identifiers;
- student records protected by institutional policy or education law;
- health, clinical, benefits, legal, immigration, financial, or employment records;
- confidential nonprofit client data;
- sensitive public-sector, infrastructure, or security data;
- proprietary unpublished research data without approval.

## Current Security Posture

Current support in the repo:

- local-first storage under `storage/`;
- local datasets, exports, runtime files, PDFs, and databases ignored by Git;
- no built-in user accounts or cloud dependency;
- OA-only PDF download enforcement;
- report HTML escaping tests;
- pytest coverage for core data, stats, literature, and API/UI flows;
- startup scripts that bind services to `127.0.0.1` by default.

Important gaps:

- no authentication or authorization;
- no role-based access control;
- no TLS configuration;
- no production CORS policy;
- no audit logging system;
- no rate limiting;
- no backup or restore workflow;
- no dependency scanning or SBOM workflow;
- no formal penetration test or secure deployment guide.

## Production Hardening Checklist

Before production or shared use:

- bind services behind a trusted reverse proxy;
- enable TLS;
- add authentication and authorization;
- restrict CORS and network exposure;
- protect `storage/` with filesystem permissions;
- define retention and deletion rules for datasets, PDFs, notes, exports, and reports;
- add audit logs for uploads, downloads, exports, and literature actions;
- scan dependencies with an approved tool;
- pin and review dependencies for deployment;
- run tests and security checks in CI;
- add backups and restore testing for `storage/`;
- review PDF handling and file upload limits;
- review generated reports for accidental disclosure;
- complete privacy, accessibility, legal, and methods review.

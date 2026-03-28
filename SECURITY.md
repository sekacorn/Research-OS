# Security Policy

## Supported Versions

Security updates are provided on a best-effort basis for the current public version of Research OS on the default branch.

| Version | Supported |
| --- | --- |
| Current default branch | Yes |
| Older snapshots and forks | No |

## Reporting a Vulnerability

If you believe you have found a security issue, please report it privately instead of opening a public issue.

Include the following when possible:

- a short description of the issue
- the affected component or file path
- steps to reproduce
- expected impact
- any proof-of-concept details needed to verify the report safely

Please avoid:

- posting exploit details in public issues
- including sensitive personal data in reports
- running destructive tests against systems you do not own

## Response Expectations

Reports will be reviewed on a best-effort basis.

If the issue is confirmed, the project maintainer may:

- acknowledge the report
- reproduce and assess severity
- prepare a fix
- publish a coordinated update when ready

## Scope Notes

This project is intended for local-first research workflows. The highest-priority security concerns are:

- accidental exposure of local research data
- insecure handling of downloaded files or PDFs
- dependency-related vulnerabilities in the Python stack
- unsafe future changes to API or file-handling behavior

# Privacy

Research OS is designed for local-first research workflows. It can still process or store sensitive information if a user uploads it, exports it, downloads PDFs, or writes notes. Treat privacy as a deployment responsibility, not something the app fully solves by itself.

## What Data The App Can Store

By default, local runtime data may be written under `storage/`:

- `storage/library.db`: literature metadata and notes;
- `storage/papers/`: downloaded open-access PDFs;
- `storage/exports/`: exported datasets and schema sidecars;
- `storage/tmp/runtime/`: runtime logs and process files.

The app can also hold uploaded tabular data and manual PDF text in Streamlit session state while the app is running. Exported reports and analysis manifests may contain dataset names, column names, model outputs, citations, warnings, and interpretation text.

The repository ignores local datasets, exports, PDFs, runtime files, and SQLite databases in `.gitignore`.

## Demo / Mock Data Versus Real Deployment

The included dataset at `data/sample_students.csv` is synthetic and suitable for demos, screenshots, smoke tests, and training.

Real deployments may process actual research datasets, notes, PDFs, exports, and reports. If those materials contain personal data, student data, health data, financial data, legal data, public-sector records, or confidential community information, deployers must add appropriate controls before use.

## GDPR And Public-Sector Responsibilities

Research OS does not provide a complete GDPR, public-sector, institutional review board, records-management, or data-governance program.

Deployers are responsible for:

- lawful basis, consent, ethics approval, or research authorization;
- data minimization and purpose limitation;
- de-identification or pseudonymization where appropriate;
- retention schedules and deletion procedures;
- access control and user authorization;
- handling data subject rights where applicable;
- breach response and incident reporting;
- processor/controller and vendor review;
- cross-border transfer review;
- records-management and public-sector procurement requirements;
- review of exported reports and manifests before sharing.

## Practical Privacy Guidance

- Use synthetic or de-identified data for demos.
- Do not upload sensitive data to a shared or public deployment without review.
- Keep `storage/` out of version control.
- Restrict filesystem access to local storage.
- Clear local PDFs, notes, exports, and reports when no longer needed.
- Review downloaded PDFs and citations for license and privacy concerns.
- Review model outputs and generated interpretation text before publication.
- Add organizational privacy notices if deploying for others.

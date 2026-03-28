# Research OS

Open research platform for quantitative social-science workflows.

Research OS is a local-first application for loading tabular data, exploring patterns, running hypothesis tests and regression models, generating cautious interpretation text, and connecting results to open-access literature. It is designed for researchers who want a lightweight reproducible workflow rather than a dashboard product.

## Highlights

- Local-first data workflow with editable previews and export support
- EDA, hypothesis testing, OLS, logistic regression, diagnostics, and effect sizes
- Mandatory methods/assumptions coaching layer for cautious interpretation
- Report generation with methods, diagnostics, limitations, and next steps
- Literature workflow for OpenAlex search, OA-only PDF downloads, citation export, and notes
- Dataset export writes a machine-readable schema sidecar for reproducibility
- Report export includes a downloadable analysis manifest JSON
- Synthetic sample dataset included for demos and screenshots

## Screenshots

### Data Workflow
![Data tab showing the loaded synthetic sample dataset, editable preview, schema table, missingness table, and export tools](docs/screenshots/screenshot-1.png)

### Analysis Summary
![Analysis tab showing numeric summaries and categorical counts in table form for non-visual inspection](docs/screenshots/screenshot-2.png)

### Analysis Plots
![Analysis tab showing histograms, category counts, scatter plot, and correlation heatmap in a two-column layout](docs/screenshots/screenshot-3.png)

### Report Preview
![Report tab showing the generated report preview with methods, model summary, diagnostics, and download actions](docs/screenshots/screenshot-4.png)

### Literature Support
![Literature tab showing PDF upload, OpenAlex search, local library entries, and citation and note actions](docs/screenshots/screenshot-5.png)

## Who It Is For

Research OS is intended for quantitative researchers working with survey, observational, administrative, or other structured social data, including work in:

- sociology
- political science
- public health
- education research
- criminology
- economics
- adjacent fields using reproducible quantitative methods

## Workflow

1. Load your own dataset or use the included sample dataset.
2. Inspect schema, missingness, and exploratory summaries.
3. Run hypothesis tests and regression models.
4. Review methods-coach outputs, warnings, and limitations.
5. Attach literature context and citations.
6. Export a report draft for further writing and revision.

## Quick Start

### Windows

```powershell
py -m pip install -U pip
py -m pip install -e .
py -m pip install -r requirements-dev.txt
run.bat
```

### Linux / macOS

```bash
bash setup.sh
bash run.sh
```

Frontend default URL:

- `http://127.0.0.1:8501`

API docs default URL:

- `http://127.0.0.1:8000/docs`

To stop the app:

- Windows: `stop.bat`
- Linux / macOS: `bash stop.sh`

## Sample Data

The repo includes a synthetic dataset at `data/sample_students.csv`. In the UI, use the `Load sample dataset` button on the Data page to populate the app quickly for demos, screenshots, and smoke testing.

## Key Modules

- `app_streamlit/`: Streamlit UI for Data, Analysis, Models, Report, and Literature pages
- `stats_engine/`: schema, EDA, tests, regression, diagnostics, effect sizes, report generation, and interpretation helpers
- `literature/`: OpenAlex search, OA resolution, PDF handling, local library, citations, and notes
- `api_fastapi/`: thin FastAPI wrapper around existing stats and literature logic
- `docs/screenshots/`: README screenshots

## Accessibility

Accessibility notes are documented in [`ACCESSIBILITY.md`](ACCESSIBILITY.md).

Current status:

- The project is not formally certified as Section 508 compliant.
- The current UI uses labeled Streamlit controls and text-based status messages for most actions.
- The biggest remaining accessibility risks are chart accessibility, screen-reader validation of complex widgets like `st.data_editor`, and the lack of a formal keyboard/screen-reader audit.

## Documentation

- [`USAGE.md`](USAGE.md): task-by-task app walkthrough
- [`ARCHITECTURE.md`](ARCHITECTURE.md): module layout and boundaries
- [`METHODS.md`](METHODS.md): interpretation limits and responsible-use guardrails
- [`SPEC.md`](SPEC.md): product scope and acceptance criteria
- [`CONTRIBUTING.md`](CONTRIBUTING.md): contributor workflow
- [`SECURITY.md`](SECURITY.md): vulnerability reporting guidance
- [`CITATION.cff`](CITATION.cff): software citation metadata for GitHub and archival workflows
- [`codemeta.json`](codemeta.json): machine-readable research software metadata
- [`.zenodo.json`](.zenodo.json): archival metadata scaffold for DOI-oriented release workflows

## Verification

- Test suite: `33 passed`
- FastAPI contract tests: passing
- Report-generation tests: passing

Run locally with:

```bash
python -m pytest -q
```

On Windows, replace `python` with `py` if needed.

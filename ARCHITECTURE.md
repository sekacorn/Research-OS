# Architecture

Research OS is intentionally small and local-first. The codebase is organized around a few clear module boundaries so the statistical layer, interpretation layer, UI, and literature tools can evolve without becoming tangled.

## Module Boundaries

### `stats_engine/`

The quantitative analysis core.

Responsibilities:

- schema inspection
- missingness and EDA helpers
- hypothesis tests
- regression models
- diagnostics and effect sizes
- report generation
- interpretation handoff to the methods coach

This layer should stay free of UI and API concerns.

### `stats_engine/methods_coach.py`

The interpretation guardrail layer.

Responsibilities:

- convert model/test results into research-language summaries
- surface assumptions, limitations, and warnings
- recommend next steps
- discourage causal overreach

This is part of the product’s core identity and should remain mandatory in the workflow.

### `literature/`

The literature support layer.

Responsibilities:

- OpenAlex metadata search
- open-access PDF resolution and download
- local SQLite library storage
- citation formatting
- note-taking
- PDF text extraction and literal search

### `app_streamlit/`

The interactive UI layer.

Pages:

- `01_Data.py`
- `02_Analysis.py`
- `03_Models.py`
- `04_Report.py`
- `05_Literature.py`

This layer should orchestrate workflows and present outputs, not reimplement analysis logic.

### `api_fastapi/`

The thin API wrapper.

Responsibilities:

- expose existing stats and literature flows over HTTP
- keep payload shapes consistent with the Streamlit UI
- avoid duplicating business logic already implemented elsewhere

## Persistence

Research OS is local-first.

Primary storage locations:

- `storage/library.db`: literature library and notes
- `storage/papers/`: downloaded PDFs
- `storage/exports/`: exported datasets
- `storage/tmp/runtime/`: temporary runtime logs

## High-Level Flow

```text
tabular data
  -> stats_engine
  -> interpret
  -> methods_coach
  -> Streamlit UI / report output

literature metadata
  -> literature.search / literature.download / literature.library
  -> Streamlit UI / report citations
```

## Current Repo Layout

```text
Research_OS/
  README.md
  USAGE.md
  ARCHITECTURE.md
  METHODS.md
  SPEC.md
  CONTRIBUTING.md
  SECURITY.md
  LICENSE
  Makefile
  pyproject.toml
  requirements-dev.txt
  setup.sh

  api_fastapi/
  app_streamlit/
  data/
  docs/
    screenshots/
  literature/
  scripts/
  stats_engine/
  storage/
  tests/
```

## Design Constraints

- Keep the methods coach in the loop for user-facing analysis outputs.
- Keep the literature workflow OA-only.
- Keep runtime state local by default.
- Keep module boundaries clear: statistics logic in `stats_engine`, literature logic in `literature`, presentation in `app_streamlit`, transport in `api_fastapi`.

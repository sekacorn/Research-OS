# Status

## Summary
This file tracks what has been completed, what is pending, and what is blocked.

## Completed
1) Scaffolded missing directories per ARCHITECTURE.md.
2) Implemented stats_engine core modules:
   - schema detection
   - cleaning helpers
   - EDA summary + plots
   - group tests (t-test, chi-square)
   - regression (OLS, logit)
   - diagnostics (VIF, heteroskedasticity, residual normality)
   - effect sizes (Cohen's d, Cramer's V)
   - interpret layer to attach coach outputs
   - report HTML builder
3) Literature module implemented:
   - OpenAlex search
   - OA resolver
   - OA-only PDF download with enforcement
   - SQLite library + notes
   - BibTeX + APA export
4) Streamlit UI with 5 pages:
   - Data, Analysis, Models, Report, Literature
5) FastAPI wrapper:
   - /stats and /literature endpoints
6) Tests added:
   - schema, group tests, regression, OA-only enforcement
   - integration test: analysis -> citation -> report export
7) Environment setup progress (2026-02-22):
   - GNU Make installed via winget (`ezwinports.make`, `GnuWin32.Make`)
   - verified make binary: `C:\Program Files (x86)\GnuWin32\bin\make.exe`
   - pytest installed from downloaded PyPI wheels (offline local install)
   - verified pytest version: `9.0.2`
   - verified command: `python -m pytest --version`
8) Dependency bootstrap progress (2026-02-22):
   - built local wheelhouse at `storage/tmp/wheels_full` from PyPI metadata/wheels
   - installed core runtime packages needed for stats/API tests:
     - pandas, numpy, scipy, statsmodels
     - requests, fastapi, uvicorn, pydantic, sqlalchemy
     - matplotlib, plotly
   - pytest now executes test collection/run (no longer failing on missing pandas/requests imports)
9) Runtime dependency compatibility fix (2026-02-22):
   - applied Streamlit-compatible pin strategy (`<=` equivalent):
     - pandas downgraded from `3.0.1` to `2.3.3` (to satisfy `streamlit` requirement `pandas < 3`)
     - cachetools pinned to `<7` (`6.2.6`)
   - streamlit installed and verified importable
10) PATH configuration fix (2026-02-22):
   - added command paths at machine scope for reliability:
     - `C:\Program Files (x86)\GnuWin32\bin`
     - `C:\Users\sekac\AppData\Roaming\Python\Python312\Scripts`
   - verified command resolution for:
     - `make`
     - `pytest`
     - `streamlit`
11) Documentation refresh (2026-02-23):
   - rewrote `README.md` for clearer onboarding and architecture-first workflow guidance
   - added explicit quick-start and manual run commands
   - documented strict module boundaries and guardrails
12) Cross-platform bootstrap scripts added (2026-02-23):
   - `scripts/bootstrap_and_run.bat` (Windows)
   - `scripts/bootstrap_and_run.sh` (Linux/macOS)
   - both scripts:
     - check system-level dependencies (python/python3)
     - install runtime/dev dependencies from project files
     - run pytest
     - start FastAPI backend + Streamlit frontend
     - wait for backend readiness (`/docs`) before launching frontend
     - clean up backend process when frontend exits
     - report missing system dependencies explicitly
13) README architecture additions (2026-02-23):
   - added abstract system diagram (analysis -> coach -> UI/report + literature sidecar)
   - added project file structure tree
14) README bootstrap behavior update (2026-02-23):
   - documented full-stack startup behavior (backend + frontend)
   - documented backend readiness check and cleanup behavior
15) Unified run/stop workflow implemented and validated (2026-02-23):
   - added one-command scripts at repo root:
     - `run.bat` / `stop.bat` (Windows)
     - `run.sh` / `stop.sh` (Linux/macOS/Git Bash)
   - `run` scripts:
     - install runtime dependencies via editable install
     - start FastAPI + Streamlit
     - enforce readiness checks for `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8501`
     - disable Streamlit first-run prompt/headless blockers
   - `stop` scripts:
     - terminate both backend/frontend process variants reliably
     - include Windows-specific fallback in `stop.sh` for Git Bash process control
16) Packaging/install reliability fix (2026-02-23):
   - updated `pyproject.toml` with setuptools build-system metadata
   - constrained package discovery (`stats_engine*`, `literature*`) to fix editable install failure
17) Usage documentation added and personalized (2026-02-23):
   - added `USAGE.md` with section-by-section workflow instructions
   - documented first-time/start/stop usage via `run.*` and `stop.*`
   - tuned guidance language for reduced cognitive overload and focused analysis loops
   - linked `USAGE.md` from `README.md`
18) Run-script UX and reliability upgrade (2026-02-23):
   - updated `run.bat` and `run.sh` with preflight endpoint checks before startup:
     - detect already-running stack and print status block with HTTP codes
     - detect port conflicts (`8000`/`8501`) and fail with clear guidance
   - added post-start endpoint verification for both API/UI before success message
   - initially added browser auto-open to UI URL after successful health checks
   - standardized success text block including explicit stop command instruction
19) Manual PDF robustness upgrade (2026-02-23):
   - added multi-extractor PDF text strategy (`pypdf` + `pdfplumber`) with best-candidate selection
   - added extraction quality metrics and low-coverage warnings in Literature page
   - retained literal text search support for letters, numbers, and special characters
20) Report readability fix (2026-02-23):
   - updated report HTML styling for dark/light mode-safe text contrast
   - resolved dark mode blend issue in report review content
21) Data tab import/edit/save expansion (2026-02-23):
   - added multi-format upload support in Data tab:
     - `.csv`, `.xls`, `.xlsx`, `.ods`
   - added editable data grid (`st.data_editor`)
   - added save/export workflow for edited data:
     - local save to `storage/exports/` in `parquet`, `csv`, `xlsx`
     - download buttons for `csv`, `xlsx`, and `parquet` (when available)
22) Manual PDF feature delivered (2026-02-23):
   - added manual PDF upload in Literature tab for analysis support
   - added literal text search over uploaded PDF text (letters, numbers, special characters)
   - added content-fingerprint refresh fix so same-filename re-uploads are reprocessed
23) Run script behavior update (2026-02-23):
   - removed browser auto-open from `run.bat` / `run.sh`
   - scripts now print explicit copy/paste endpoint instructions (UI prioritized)
   - added dynamic port fallback near defaults (`8000` API, `8501` UI)
24) Repository hygiene update (2026-02-23):
   - expanded `.gitignore` for runtime artifacts, exports, temp/cache folders, and local outputs
25) Coverage expansion completed (2026-02-23):
   - added targeted tests for low-coverage modules:
     - `tests/test_cleaning_eda.py`
     - `tests/test_literature_search_pdf_text.py`
     - `tests/test_data_io_e2e.py`
   - total coverage now `86%` (target `85%` met)
26) Run script UX finalization (2026-02-23):
   - `run.bat` and `run.sh` now avoid auto-opening browsers
   - success output now prioritizes UI copy/paste endpoint text
   - scripts explicitly instruct users to open a browser and paste:
     - frontend UI endpoint (first)
     - backend docs endpoint (second)
27) Run script edge-case hardening (2026-02-23):
   - preflight now detects already-running app processes on non-default/fallback ports
   - avoids duplicate stack startup when services are already running
   - dynamic port fallback retained near defaults (`8000`, `8501`)
28) Bug fixes (2026-02-23):
   - fixed manual PDF same-filename reupload stale-cache behavior via content fingerprinting
   - fixed `stop.bat` self-process match risk during command-line process filtering
29) API↔UI integration test coverage added (2026-02-23):
   - added `tests/test_api_ui_flow.py`
   - validates stats endpoints return coach/report fields consumed by UI flows
   - validates literature API writes (papers/notes) are visible via UI-facing library/note helpers
30) Dev dependency update (2026-02-23):
   - added `httpx` to `requirements-dev.txt` for FastAPI `TestClient` support
   - installed `httpx` in local environment
31) Documentation sync update (2026-02-23):
   - refreshed `README.md` and `USAGE.md` with:
     - dynamic endpoint guidance (use printed UI/API URLs)
     - latest verified test counts and coverage
     - dev/test dependency note for `httpx`

## Pending
1) No functional pending items for POC verification.

## Blockers
1) Dependency install is blocked by outbound network restriction (WinError 10013).
   - pip cannot reliably reach package index for normal installs.
2) No active test-environment blocker after pytest basetemp mitigation + elevated run verification (2026-02-23).
3) Sandbox limitation (current session):
   - non-elevated Python shim invocation can fail with `The file cannot be accessed by the system`
   - elevated runs were used for final command verification

## Next Goals
1) Optional: continue robustness hardening and add targeted numeric-stability tests.
2) Optional: add lightweight CI checks for bootstrap scripts on Windows and Linux shells.

## Recent Test Attempts
1) Pytest run (2026-02-23):
   - command: `py -m pytest -q` (with TMP/TEMP/PYTEST_TMPDIR set to `storage/tmp/pytest`)
   - result: error in `tests/test_literature_oa.py::test_download_oa_pdf`
   - failure: `PermissionError: [WinError 5] Access is denied` when removing `storage/tmp/pytest`
   - note: regression test emitted warning `RuntimeWarning: overflow encountered in exp` (logit CI exp)
2) Config change (2026-02-23):
   - updated pytest addopts in `pyproject.toml` to include `--basetemp=C:/Users/sekac/AppData/Local/Temp/pytest-codex`
   - intended to avoid OneDrive permissions during cleanup
3) Verification run (2026-02-23):
   - command: `py -m pytest`
   - result: `11 passed, 1 warning in 3.14s`
   - warning: `RuntimeWarning: overflow encountered in exp` at `stats_engine/models/regression.py:107`
4) Streamlit smoke verification (2026-02-23):
   - command pattern: start `py -m streamlit run app_streamlit/app.py --server.headless true --server.port 8501`, probe `http://127.0.0.1:8501`, then stop process
   - result: `STREAMLIT_SMOKE_OK`
5) FastAPI smoke verification (2026-02-23):
   - command pattern: start `py -m uvicorn api_fastapi.main:app --host 127.0.0.1 --port 8000`, probe `http://127.0.0.1:8000/docs`, then stop process
   - result: `FASTAPI_SMOKE_OK` (HTTP 200 on `/docs`)
   - note: one lingering `uvicorn` process caused a transient port bind warning (`WinError 10048`); process was terminated and port 8000 cleared
6) `make` verification (2026-02-23):
   - `make test PY=py` (elevated): pass, pytest completed (`11 passed, 1 warning`)
   - `make run`: smoke pass (`MAKE_RUN_SMOKE_OK`)
   - `make api`: smoke pass when elevated (`MAKE_API_SMOKE_OK`)
   - note: non-elevated `make api` hit Windows multiprocessing permission errors under `uvicorn --reload`
7) Numeric stability hardening (2026-02-23):
   - updated `stats_engine/models/regression.py`:
     - added safe exponentiation helper for logit odds-ratio transforms with clipping
     - prevented overflow warnings in OR/CI exponentiation
     - emits explicit model warning when clipping is applied
   - verification: `py -m pytest -q` passed (`11 passed`) with no warnings
8) Post-bootstrap update verification (2026-02-23):
   - command: `py -m pytest -q`
   - result: `11 passed`
9) Run/stop script verification (2026-02-23):
   - Windows cycle:
     - `run.bat` succeeded
     - endpoint checks passed: `/docs` -> 200, Streamlit root -> 200
     - `stop.bat` stopped app processes and cleared listeners
   - Unix-script cycle on Windows Git Bash:
     - `run.sh` succeeded after interpreter detection + headless fixes
     - endpoint checks passed: `/docs` -> 200, Streamlit root -> 200
     - `stop.sh` succeeded after PowerShell fallback + quoting fix
10) Regression verification after run/stop fixes (2026-02-23):
   - command: `py -m pytest -q`
   - result: `11 passed`
11) Run script messaging/health-check verification (2026-02-23):
   - `run.bat` validated:
     - preflight + post-start health checks active
     - success status block printed with endpoint URLs and HTTP codes
   - `run.sh` validated:
     - preflight + post-start health checks active
     - endpoint checks passed (`/docs` -> 200, UI root -> 200)
   - `stop.sh` validated after run checks
12) Post-feature regression verification (2026-02-23):
   - command: `py -m pytest -q`
   - result: `11 passed`
13) Data/PDF/script regression verification (2026-02-23):
   - command: `py -m pytest -q`
   - result: `25 passed, 2 skipped`
14) Coverage verification (2026-02-23):
   - command: `py -m pytest -q --cov=stats_engine --cov=literature --cov=app_streamlit --cov-report=term`
   - result: `86%` total coverage
15) Final regression verification (2026-02-23):
   - command: `py -m pytest -q`
   - result: `25 passed, 2 skipped`
16) API/UI integration + dependency verification (2026-02-23):
   - command: `py -m pytest -ra`
   - result: `27 passed, 2 skipped`
17) Coverage refresh including API layer (2026-02-23):
   - command: `py -m pytest -q --cov=stats_engine --cov=literature --cov=app_streamlit --cov=api_fastapi --cov-report=term`
   - result: `89%` total coverage

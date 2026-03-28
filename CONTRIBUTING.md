# Contributing

Thanks for contributing to Research OS.

## Development workflow

- Run `bash setup.sh` on Unix-like shells to create `.venv` and install dependencies.
- Run tests with `make test`.
- Install development dependencies from `requirements-dev.txt` when needed.
- Use the provided startup scripts for local end-to-end checks.

## Code style

- Format code with `black`.
- Lint with `ruff`.
- Type-check with `mypy` where applicable.
- Keep module boundaries intact across `stats_engine`, `literature`, `app_streamlit`, and `api_fastapi`.

## Pull requests

- Keep pull requests focused and easy to review.
- Include tests or a clear rationale when tests are not needed.
- Summarize user-facing changes and any follow-up work in the PR description.

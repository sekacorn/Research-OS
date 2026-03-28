"""Viewer helpers."""

from __future__ import annotations

from pathlib import Path


def load_pdf_bytes(pdf_path: str) -> bytes:
    return Path(pdf_path).read_bytes()

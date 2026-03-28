"""OA-only PDF download."""

from __future__ import annotations

from typing import Any, Dict

import requests
from pathlib import Path

from literature.oa import resolve_oa_pdf
from literature.library import add_paper

PAPERS_DIR = Path("storage/papers")


def _looks_like_pdf(content: bytes, content_type: str | None) -> bool:
    if content.startswith(b"%PDF-"):
        return True
    if content_type and "pdf" in content_type.lower():
        return True
    return False


def download_pdf_oa(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Download OA PDF if available. Raises ValueError if not OA."""
    pdf_url = resolve_oa_pdf(meta)
    if not pdf_url:
        raise ValueError("OA PDF not available for this record")

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    safe_id = str(meta.get("id", "paper")).replace("/", "_").replace(":", "_")
    pdf_path = PAPERS_DIR / f"{safe_id}.pdf"

    resp = requests.get(pdf_url, timeout=30)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type") if hasattr(resp, "headers") else None
    if not _looks_like_pdf(resp.content, content_type):
        raise ValueError("Resolved OA URL did not return a PDF file")

    pdf_path.write_bytes(resp.content)

    meta = dict(meta)
    meta["pdf_path"] = str(pdf_path)
    add_paper(meta)
    return meta

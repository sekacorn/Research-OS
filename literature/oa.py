"""OA resolver."""

from __future__ import annotations

from typing import Any, Dict, Optional


def resolve_oa_pdf(meta: Dict[str, Any]) -> Optional[str]:
    """Return OA PDF URL if available, otherwise None."""
    pdf_url = meta.get("pdf_url")
    if pdf_url:
        return str(pdf_url)
    return None

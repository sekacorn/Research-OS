"""PDF text extraction and search helpers."""

from __future__ import annotations

from io import BytesIO
import re
from typing import Dict, List, Tuple

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None

try:
    import pdfplumber
except Exception:  # pragma: no cover
    pdfplumber = None


def _normalize_page_text(value: str) -> str:
    text = value or ""
    # Keep line structure but collapse excessive blank space.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_with_pypdf(pdf_bytes: bytes) -> Tuple[List[str], str]:
    if PdfReader is None:
        return [], "pypdf_unavailable"
    reader = PdfReader(BytesIO(pdf_bytes))
    page_texts = [_normalize_page_text(page.extract_text() or "") for page in reader.pages]
    return page_texts, "pypdf"


def _extract_with_pdfplumber(pdf_bytes: bytes) -> Tuple[List[str], str]:
    if pdfplumber is None:
        return [], "pdfplumber_unavailable"
    page_texts: List[str] = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_texts.append(_normalize_page_text(page.extract_text() or ""))
    return page_texts, "pdfplumber"


def _metrics(page_texts: List[str]) -> Dict[str, float]:
    page_count = len(page_texts)
    non_empty = sum(1 for p in page_texts if p.strip())
    chars = sum(len(p) for p in page_texts)
    words = sum(len(re.findall(r"\b\w+\b", p)) for p in page_texts)
    coverage = (non_empty / page_count) if page_count else 0.0
    avg_chars = (chars / page_count) if page_count else 0.0
    return {
        "page_count": float(page_count),
        "non_empty_pages": float(non_empty),
        "coverage_ratio": float(coverage),
        "char_count": float(chars),
        "word_count": float(words),
        "avg_chars_per_page": float(avg_chars),
    }


def _pick_best(candidates: List[Tuple[str, List[str]]]) -> Tuple[str, List[str], Dict[str, float]]:
    ranked: List[Tuple[str, List[str], Dict[str, float], float]] = []
    for method, pages in candidates:
        m = _metrics(pages)
        # Score prioritizes non-empty coverage first, then text richness.
        score = (m["coverage_ratio"] * 1_000_000.0) + m["char_count"] + (m["word_count"] * 0.1)
        ranked.append((method, pages, m, score))
    ranked.sort(key=lambda x: x[3], reverse=True)
    method, pages, m, _ = ranked[0]
    return method, pages, m


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Dict[str, object]:
    """Extract plain text from PDF bytes using multiple extractors and pick best."""
    if PdfReader is None:
        raise RuntimeError("pypdf is required for manual PDF upload/search. Install project dependencies.")

    pypdf_pages, pypdf_method = _extract_with_pypdf(pdf_bytes)
    plumber_pages, plumber_method = _extract_with_pdfplumber(pdf_bytes)

    candidates: List[Tuple[str, List[str]]] = []
    if pypdf_pages:
        candidates.append((pypdf_method, pypdf_pages))
    if plumber_pages:
        candidates.append((plumber_method, plumber_pages))

    if not candidates:
        return {
            "text": "",
            "pages": [],
            "page_count": 0,
            "method": "none",
            "metrics": _metrics([]),
            "warnings": [
                "No extractable text found. PDF may be image-based/scanned. OCR is required for high-quality extraction."
            ],
        }

    method, page_texts, metrics = _pick_best(candidates)
    full_text = "\n".join(page_texts)
    warnings: List[str] = []
    if metrics["coverage_ratio"] < 0.9:
        warnings.append(
            "Low text coverage detected. Document may be scanned or image-heavy; OCR is recommended."
        )
    if metrics["char_count"] < 500:
        warnings.append("Very low extracted text volume; verify source quality and consider OCR.")

    return {
        "text": full_text,
        "pages": page_texts,
        "page_count": len(page_texts),
        "method": method,
        "metrics": metrics,
        "warnings": warnings,
    }


def search_text(
    text: str,
    query: str,
    *,
    case_sensitive: bool = False,
    context_chars: int = 80,
    max_hits: int = 50,
) -> List[Dict[str, object]]:
    """Literal text search that supports letters, numbers, and special characters."""
    if not query:
        return []

    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.escape(query)

    hits: List[Dict[str, object]] = []
    for match in re.finditer(pattern, text, flags=flags):
        start, end = match.start(), match.end()
        left = max(0, start - context_chars)
        right = min(len(text), end + context_chars)
        snippet = text[left:right].replace("\n", " ")
        hits.append({"start": start, "end": end, "match": text[start:end], "snippet": snippet})
        if len(hits) >= max_hits:
            break
    return hits

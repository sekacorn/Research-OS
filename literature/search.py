"""Metadata search via OpenAlex (public)."""

from __future__ import annotations

from typing import Any, Dict, List

import requests

OPENALEX_URL = "https://api.openalex.org/works"


def search_openalex(query: str, rows: int = 5) -> List[Dict[str, Any]]:
    params = {"search": query, "per_page": rows}
    resp = requests.get(OPENALEX_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for item in data.get("results", []):
        title = item.get("title") or ""
        year = item.get("publication_year")
        doi = item.get("doi")
        authors = []
        for auth in item.get("authorships", [])[:5]:
            name = auth.get("author", {}).get("display_name")
            if name:
                authors.append(name)
        authors_str = ", ".join(authors)

        best = item.get("best_oa_location") or {}
        pdf_url = best.get("pdf_url")
        oa_url = best.get("landing_page_url") or best.get("url")

        results.append(
            {
                "id": item.get("id"),
                "title": title,
                "authors": authors_str,
                "year": year,
                "doi": doi,
                "oa_url": oa_url,
                "pdf_url": pdf_url,
            }
        )
    return results

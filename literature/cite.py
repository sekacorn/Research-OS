"""Citation export utilities."""

from __future__ import annotations

from typing import Any, Dict


def to_bibtex(meta: Dict[str, Any]) -> str:
    key = (meta.get("id") or "paper").split("/")[-1]
    title = meta.get("title") or ""
    authors = meta.get("authors") or ""
    year = meta.get("year") or ""
    doi = meta.get("doi") or ""

    return (
        f"@article{{{key},\n"
        f"  title={{ {title} }},\n"
        f"  author={{ {authors} }},\n"
        f"  year={{ {year} }},\n"
        f"  doi={{ {doi} }}\n"
        f"}}\n"
    )


def to_apa(meta: Dict[str, Any]) -> str:
    authors = meta.get("authors") or ""
    year = meta.get("year") or "n.d."
    title = meta.get("title") or ""
    doi = meta.get("doi")
    if doi:
        return f"{authors} ({year}). {title}. https://doi.org/{doi}"
    return f"{authors} ({year}). {title}."

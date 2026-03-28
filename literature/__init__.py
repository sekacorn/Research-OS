"""Literature module: OA-only search, download, library, citations."""

from .search import search_openalex
from .oa import resolve_oa_pdf
from .download import download_pdf_oa
from .library import init_library, add_paper, list_papers, get_paper
from .cite import to_bibtex, to_apa
from .notes import add_note, list_notes
from .pdf_text import extract_text_from_pdf_bytes, search_text

__all__ = [
    "search_openalex",
    "resolve_oa_pdf",
    "download_pdf_oa",
    "init_library",
    "add_paper",
    "list_papers",
    "get_paper",
    "to_bibtex",
    "to_apa",
    "add_note",
    "list_notes",
    "extract_text_from_pdf_bytes",
    "search_text",
]

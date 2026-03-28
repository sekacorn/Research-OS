from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from literature.search import search_openalex
from literature.download import download_pdf_oa
from literature.cite import to_bibtex, to_apa
from literature.notes import add_note, list_notes
from literature.library import list_papers

from api_fastapi.schemas.literature import SearchRequest, MetaPayload, NoteRequest

router = APIRouter(prefix="/literature", tags=["literature"])


@router.post("/search")
def search(payload: SearchRequest) -> Dict[str, Any]:
    return {"results": search_openalex(payload.query, payload.rows)}


@router.post("/download")
def download(payload: MetaPayload) -> Dict[str, Any]:
    return download_pdf_oa(payload.meta)


@router.post("/cite")
def cite(payload: MetaPayload) -> Dict[str, Any]:
    bib = to_bibtex(payload.meta)
    apa = to_apa(payload.meta)
    return {"bibtex": bib, "apa": apa}


@router.get("/library")
def library() -> Dict[str, Any]:
    return {"papers": list_papers()}


@router.post("/notes")
def add_note_api(payload: NoteRequest) -> Dict[str, Any]:
    add_note(payload.paper_id, payload.note, payload.page)
    return {"ok": True}


@router.get("/notes/{paper_id}")
def list_notes_api(paper_id: str) -> Dict[str, Any]:
    return {"notes": list_notes(paper_id)}

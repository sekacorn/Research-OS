from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    rows: int = 5


class MetaPayload(BaseModel):
    meta: Dict[str, Any]


class NoteRequest(BaseModel):
    paper_id: str
    note: str
    page: str | None = None

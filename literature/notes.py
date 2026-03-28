"""Notes CRUD in SQLite."""

from __future__ import annotations

from typing import Any, Dict, List

import sqlite3
from literature.library import DB_PATH, init_library


def add_note(paper_id: str, note: str, page: str | None = None) -> None:
    init_library()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO notes (paper_id, note, page) VALUES (?, ?, ?)",
            (paper_id, note, page),
        )


def list_notes(paper_id: str) -> List[Dict[str, Any]]:
    init_library()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, note, page, created_at FROM notes WHERE paper_id = ? ORDER BY id DESC",
            (paper_id,),
        ).fetchall()
    return [
        {"id": r[0], "note": r[1], "page": r[2], "created_at": r[3]}
        for r in rows
    ]

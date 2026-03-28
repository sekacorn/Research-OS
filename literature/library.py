"""SQLite-backed literature library."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import sqlite3
from pathlib import Path

DB_PATH = Path("storage/library.db")


def init_library() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                year INTEGER,
                doi TEXT,
                oa_url TEXT,
                pdf_path TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id TEXT,
                note TEXT,
                page TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_paper(meta: Dict[str, Any]) -> None:
    init_library()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO papers (id, title, authors, year, doi, oa_url, pdf_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                meta.get("id"),
                meta.get("title"),
                meta.get("authors"),
                meta.get("year"),
                meta.get("doi"),
                meta.get("oa_url"),
                meta.get("pdf_path"),
            ),
        )


def list_papers() -> List[Dict[str, Any]]:
    init_library()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, title, authors, year, doi, oa_url, pdf_path FROM papers").fetchall()
    return [
        {
            "id": r[0],
            "title": r[1],
            "authors": r[2],
            "year": r[3],
            "doi": r[4],
            "oa_url": r[5],
            "pdf_path": r[6],
        }
        for r in rows
    ]


def get_paper(paper_id: str) -> Optional[Dict[str, Any]]:
    init_library()
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id, title, authors, year, doi, oa_url, pdf_path FROM papers WHERE id = ?",
            (paper_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "title": row[1],
        "authors": row[2],
        "year": row[3],
        "doi": row[4],
        "oa_url": row[5],
        "pdf_path": row[6],
    }

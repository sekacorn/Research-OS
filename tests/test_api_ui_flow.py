from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
# FastAPI TestClient depends on httpx; skip cleanly if dev dependency not installed yet.
pytest.importorskip("httpx")
from fastapi.testclient import TestClient

from api_fastapi.main import app
from literature.library import list_papers, add_paper
from literature.notes import list_notes

client = TestClient(app)


def test_stats_api_contract_matches_ui_usage():
    # This verifies API payload/response shapes that the Streamlit pages consume directly.
    df = pd.read_csv("data/sample_students.csv")
    rows = df.to_dict(orient="records")

    t_payload = {
        "rows": rows,
        "value_col": "math_score",
        "group_col": "school_type",
    }
    t_resp = client.post("/stats/t_test", json=t_payload)
    assert t_resp.status_code == 200
    t_result = t_resp.json()
    # Analysis UI expects coach text blocks.
    assert "coach" in t_result
    assert "methods_text" in t_result["coach"]
    assert "interpretation_text" in t_result["coach"]
    assert "limitations" in t_result["coach"]
    assert "next_steps" in t_result["coach"]

    m_payload = {
        "rows": rows,
        "y": "math_score",
        "xs": ["participation_rate", "grade_level"],
    }
    m_resp = client.post("/stats/ols", json=m_payload)
    assert m_resp.status_code == 200
    m_result = m_resp.json()
    # Models UI expects these coach fields.
    assert "coach" in m_result
    assert "model_spec" in m_result["coach"]
    assert "effect_size_summary" in m_result["coach"]
    assert "diagnostics_summary" in m_result["coach"]
    assert "interpretation_text" in m_result["coach"]

    # Report UI consumes HTML from report endpoint.
    report_payload = {
        "dataset_name": "sample_students",
        "rows": rows,
        "tests": [t_result],
        "models": [m_result],
        "citations": [{"apa": "Doe, J. (2020). Sample paper."}],
    }
    r_resp = client.post("/stats/report", json=report_payload)
    assert r_resp.status_code == 200
    html = r_resp.json()["html"]
    assert "Research OS Report" in html
    assert "Methods" in html
    assert "Limitations" in html


def test_stats_api_returns_400_for_invalid_t_test_request():
    df = pd.read_csv("data/sample_students.csv")
    rows = df.to_dict(orient="records")

    bad_payload = {
        "rows": rows,
        "value_col": "math_score",
        "group_col": "state",
    }
    resp = client.post("/stats/t_test", json=bad_payload)
    assert resp.status_code == 400
    assert "exactly two groups" in resp.json()["detail"]


def test_literature_api_changes_visible_to_ui_helpers(tmp_path: Path):
    # API writes should be reflected in the same storage helpers used by UI pages.
    db_path = tmp_path / "library.db"
    with patch("literature.library.DB_PATH", db_path), patch("literature.notes.DB_PATH", db_path):
        # Seed one paper the same way library flows would.
        add_paper(
            {
                "id": "paper-1",
                "title": "A Study",
                "authors": "Author, A.",
                "year": 2025,
                "doi": "10.1000/example",
                "oa_url": "https://example.org",
                "pdf_path": "storage/papers/paper-1.pdf",
            }
        )

        lib_resp = client.get("/literature/library")
        assert lib_resp.status_code == 200
        papers = lib_resp.json()["papers"]
        assert any(p["id"] == "paper-1" for p in papers)
        # UI reads from literature.library.list_papers().
        ui_papers = list_papers()
        assert any(p["id"] == "paper-1" for p in ui_papers)

        note_payload = {"paper_id": "paper-1", "note": "Useful result section", "page": "3"}
        add_note_resp = client.post("/literature/notes", json=note_payload)
        assert add_note_resp.status_code == 200
        assert add_note_resp.json()["ok"] is True

        notes_resp = client.get("/literature/notes/paper-1")
        assert notes_resp.status_code == 200
        notes = notes_resp.json()["notes"]
        assert any("Useful result section" in n["note"] for n in notes)

        # UI reads from literature.notes.list_notes().
        ui_notes = list_notes("paper-1")
        assert any("Useful result section" in n["note"] for n in ui_notes)

        cite_resp = client.post("/literature/cite", json={"meta": papers[0]})
        assert cite_resp.status_code == 200
        cite = cite_resp.json()
        # UI attach action expects both formats.
        assert "bibtex" in cite and cite["bibtex"]
        assert "apa" in cite and cite["apa"]

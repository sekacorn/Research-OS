from __future__ import annotations

from unittest.mock import Mock, patch

import literature.pdf_text as pdf_text
from literature.search import search_openalex


def test_search_openalex_maps_fields():
    payload = {
        "results": [
            {
                "id": "W123",
                "title": "Paper Title",
                "publication_year": 2024,
                "doi": "10.1/abc",
                "authorships": [
                    {"author": {"display_name": "A One"}},
                    {"author": {"display_name": "B Two"}},
                ],
                "best_oa_location": {
                    "pdf_url": "https://example.org/p.pdf",
                    "landing_page_url": "https://example.org/landing",
                },
            }
        ]
    }
    fake_resp = Mock()
    fake_resp.json.return_value = payload
    fake_resp.raise_for_status = Mock()

    with patch("literature.search.requests.get", return_value=fake_resp) as get_mock:
        out = search_openalex("query", rows=3)

    get_mock.assert_called_once()
    assert len(out) == 1
    row = out[0]
    assert row["id"] == "W123"
    assert row["title"] == "Paper Title"
    assert row["year"] == 2024
    assert row["doi"] == "10.1/abc"
    assert "A One" in row["authors"]
    assert row["pdf_url"] == "https://example.org/p.pdf"


def test_pdf_text_normalize_and_search_text():
    s = pdf_text._normalize_page_text("A   B\n\n\nC\tD")
    assert s == "A B\n\nC D"

    hits = pdf_text.search_text("Alpha-123 beta ALPHA-123", "alpha-123", case_sensitive=False, max_hits=10)
    assert len(hits) == 2
    assert hits[0]["match"].lower() == "alpha-123"

    hits_cs = pdf_text.search_text("Alpha", "alpha", case_sensitive=True)
    assert hits_cs == []


def test_pdf_text_metrics_and_pick_best():
    m = pdf_text._metrics(["abc", "", "123"])
    assert m["page_count"] == 3.0
    assert m["non_empty_pages"] == 2.0
    assert m["coverage_ratio"] > 0

    method, pages, metrics = pdf_text._pick_best(
        [
            ("a", ["", ""]),
            ("b", ["hello world", "more text"]),
        ]
    )
    assert method == "b"
    assert pages[0].startswith("hello")
    assert metrics["char_count"] > 0


def test_extract_text_runtime_error_when_pypdf_missing():
    with patch.object(pdf_text, "PdfReader", None):
        try:
            pdf_text.extract_text_from_pdf_bytes(b"fake")
            assert False, "Expected RuntimeError when pypdf missing"
        except RuntimeError:
            assert True


def test_extract_text_no_candidates_warns():
    with patch.object(pdf_text, "PdfReader", object()):
        with patch.object(pdf_text, "_extract_with_pypdf", return_value=([], "pypdf")):
            with patch.object(pdf_text, "_extract_with_pdfplumber", return_value=([], "pdfplumber")):
                out = pdf_text.extract_text_from_pdf_bytes(b"fake")
    assert out["method"] == "none"
    assert out["page_count"] == 0
    assert out["warnings"]


def test_extract_text_best_candidate_and_low_coverage_warning():
    with patch.object(pdf_text, "PdfReader", object()):
        with patch.object(pdf_text, "_extract_with_pypdf", return_value=(["", "a"], "pypdf")):
            with patch.object(pdf_text, "_extract_with_pdfplumber", return_value=([""], "pdfplumber")):
                out = pdf_text.extract_text_from_pdf_bytes(b"fake")
    assert out["method"] == "pypdf"
    assert out["page_count"] == 2
    assert isinstance(out["text"], str)
    assert out["warnings"]


def test_extract_text_healthy_candidate_no_warnings():
    pages = ["word " * 200, "word " * 200]
    with patch.object(pdf_text, "PdfReader", object()):
        with patch.object(pdf_text, "_extract_with_pypdf", return_value=(pages, "pypdf")):
            with patch.object(pdf_text, "_extract_with_pdfplumber", return_value=([], "pdfplumber")):
                out = pdf_text.extract_text_from_pdf_bytes(b"fake")
    assert out["method"] == "pypdf"
    assert out["warnings"] == []

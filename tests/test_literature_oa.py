from unittest.mock import patch, Mock

from literature.download import download_pdf_oa


def test_oa_only_enforced():
    meta = {"id": "test", "title": "No OA"}
    try:
        download_pdf_oa(meta)
        assert False, "Expected ValueError for non-OA"
    except ValueError:
        assert True


def test_download_oa_pdf(tmp_path):
    meta = {"id": "test_oa", "title": "OA", "pdf_url": "http://example.com/test.pdf"}

    fake_resp = Mock()
    fake_resp.content = b"%PDF-1.4 fake"
    fake_resp.headers = {"Content-Type": "application/pdf"}
    fake_resp.raise_for_status = Mock()

    with patch("literature.download.PAPERS_DIR", tmp_path):
        with patch("requests.get", return_value=fake_resp):
            out = download_pdf_oa(meta)
            assert out.get("pdf_path") is not None


def test_download_rejects_non_pdf_payload(tmp_path):
    meta = {"id": "test_html", "title": "HTML", "pdf_url": "http://example.com/not-a-pdf"}

    fake_resp = Mock()
    fake_resp.content = b"<html>not a pdf</html>"
    fake_resp.headers = {"Content-Type": "text/html"}
    fake_resp.raise_for_status = Mock()

    with patch("literature.download.PAPERS_DIR", tmp_path):
        with patch("requests.get", return_value=fake_resp):
            try:
                download_pdf_oa(meta)
                assert False, "Expected ValueError for non-PDF payload"
            except ValueError:
                assert True

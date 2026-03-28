import hashlib

import streamlit as st

from literature.cite import to_apa, to_bibtex
from literature.download import download_pdf_oa
from literature.library import list_papers
from literature.notes import add_note, list_notes
from literature.pdf_text import extract_text_from_pdf_bytes, search_text
from literature.search import search_openalex


@st.cache_data(show_spinner=False)
def _cached_list_papers(refresh_token: int):
    del refresh_token
    return list_papers()


@st.cache_data(show_spinner=False)
def _cached_list_notes(paper_id: str, refresh_token: int):
    del refresh_token
    return list_notes(paper_id)


st.title("Literature")
st.caption("Search open-access literature, attach citations, and review extracted PDF text using labeled controls.")

if "citations" not in st.session_state:
    st.session_state["citations"] = []
if "manual_pdf_text" not in st.session_state:
    st.session_state["manual_pdf_text"] = ""
if "manual_pdf_name" not in st.session_state:
    st.session_state["manual_pdf_name"] = ""
if "manual_pdf_fingerprint" not in st.session_state:
    st.session_state["manual_pdf_fingerprint"] = ""
if "library_refresh_token" not in st.session_state:
    st.session_state["library_refresh_token"] = 0

st.subheader("Manual PDF Upload (Analysis Support)")
uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], key="manual_pdf_upload")
if uploaded_pdf is not None:
    current_name = uploaded_pdf.name
    payload = uploaded_pdf.getvalue()
    fingerprint = hashlib.sha256(payload).hexdigest()
    if st.session_state["manual_pdf_fingerprint"] != fingerprint:
        try:
            extracted = extract_text_from_pdf_bytes(payload)
            st.session_state["manual_pdf_text"] = str(extracted.get("text", ""))
            st.session_state["manual_pdf_name"] = current_name
            st.session_state["manual_pdf_fingerprint"] = fingerprint
            method = str(extracted.get("method", "unknown"))
            metrics = extracted.get("metrics", {}) or {}
            coverage = float(metrics.get("coverage_ratio", 0.0)) * 100.0
            warnings = extracted.get("warnings", []) or []
            st.success(
                f"Loaded {current_name} ({int(extracted.get('page_count', 0))} pages, "
                f"{len(st.session_state['manual_pdf_text'])} chars, method={method}, "
                f"coverage={coverage:.1f}%)."
            )
            for w in warnings:
                st.warning(w)
        except Exception as exc:
            st.error(f"Could not read PDF: {exc}")

if st.session_state["manual_pdf_text"]:
    st.caption("Literal search supports letters, numbers, and special characters.")
    manual_query = st.text_input("Search uploaded PDF text", key="manual_pdf_query")
    case_sensitive = st.checkbox("Case sensitive", value=False, key="manual_pdf_case")
    if st.button("Search Uploaded PDF", key="manual_pdf_search") and manual_query:
        matches = search_text(
            st.session_state["manual_pdf_text"],
            manual_query,
            case_sensitive=case_sensitive,
            context_chars=90,
            max_hits=30,
        )
        st.write(f"Matches found: {len(matches)}")
        for i, hit in enumerate(matches, start=1):
            st.markdown(f"**Hit {i}**")
            st.code(str(hit.get("snippet", "")))

query = st.text_input("Search OpenAlex")
if st.button("Search") and query:
    st.session_state["search_results"] = search_openalex(query, rows=5)

results = st.session_state.get("search_results", [])
if results:
    st.subheader("Search Results")
    for meta in results:
        st.write(f"{meta.get('title')} ({meta.get('year')})")
        st.caption(meta.get("authors"))
        download_label = f"Download OA PDF for {str(meta.get('title', 'result'))[:60]}"
        if st.button(download_label, key=f"dl_{meta.get('id')}"):
            try:
                download_pdf_oa(meta)
                st.session_state["library_refresh_token"] += 1
                st.success("Downloaded and saved to library")
            except ValueError as e:
                st.error(str(e))

st.subheader("Library")
refresh_token = int(st.session_state["library_refresh_token"])
papers = _cached_list_papers(refresh_token)
for p in papers:
    st.write(f"{p.get('title')} ({p.get('year')})")
    st.caption(p.get("authors"))
    bibtex = to_bibtex(p)
    apa = to_apa(p)
    st.code(bibtex, language="bibtex")
    st.write(apa)
    attach_label = f"Attach citation for {str(p.get('title', p.get('id', 'paper')))[:60]}"
    if st.button(attach_label, key=f"cite_{p.get('id')}"):
        st.session_state["citations"].append({"bibtex": bibtex, "apa": apa})
        st.success("Citation attached to report")

    note = st.text_input(f"Add note for {p.get('id')}", key=f"note_{p.get('id')}")
    if st.button(f"Save note for {p.get('id')}", key=f"save_{p.get('id')}"):
        if note:
            add_note(p.get("id"), note)
            st.session_state["library_refresh_token"] += 1
            st.success("Note saved")

    notes = _cached_list_notes(str(p.get("id")), refresh_token)
    for n in notes:
        st.write(f"- {n.get('note')} ({n.get('created_at')})")

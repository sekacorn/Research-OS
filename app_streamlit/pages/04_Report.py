import json
from datetime import datetime, timezone

import streamlit as st

from stats_engine.report import build_html_report


@st.cache_data(show_spinner=False)
def _cached_report_html(analysis_bundle, citations):
    return build_html_report(analysis_bundle, citations=citations)


def _analysis_manifest(analysis_bundle, citations):
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "Research OS",
        "dataset": analysis_bundle["dataset"],
        "tests_count": len(analysis_bundle.get("tests", [])),
        "models_count": len(analysis_bundle.get("models", [])),
        "citations_count": len(citations or []),
        "tests": [
            {
                "test_name": t.get("test_name"),
                "variables": t.get("variables"),
                "warnings": t.get("warnings", []),
            }
            for t in analysis_bundle.get("tests", [])
        ],
        "models": [
            {
                "model_name": m.get("model_name"),
                "formula": m.get("formula"),
                "warnings": m.get("warnings", []),
                "diagnostics": m.get("diagnostics", {}),
            }
            for m in analysis_bundle.get("models", [])
        ],
        "citations": citations or [],
    }


st.title("Report")

if "df" not in st.session_state:
    st.session_state["df"] = None
if "tests" not in st.session_state:
    st.session_state["tests"] = []
if "models" not in st.session_state:
    st.session_state["models"] = []
if "citations" not in st.session_state:
    st.session_state["citations"] = []

if st.session_state["df"] is None:
    st.warning("Load data in the Data page first.")
    st.stop()

df = st.session_state["df"]

analysis_bundle = {
    "dataset": {
        "name": st.session_state.get("dataset_name", "uploaded"),
        "n": len(df),
        "columns": list(df.columns),
    },
    "tests": st.session_state["tests"],
    "models": st.session_state["models"],
}

html = _cached_report_html(analysis_bundle, st.session_state["citations"])
manifest = _analysis_manifest(analysis_bundle, st.session_state["citations"])

st.subheader("Preview")
st.caption("This preview is scrollable. Use the download button below if you need the full report in a separate viewer or assistive workflow.")
st.components.v1.html(html, height=600, scrolling=True)

st.download_button("Download HTML report", data=html, file_name="research_os_report.html")
st.download_button(
    "Download analysis manifest (JSON)",
    data=json.dumps(manifest, indent=2),
    file_name="research_os_analysis_manifest.json",
    mime="application/json",
)

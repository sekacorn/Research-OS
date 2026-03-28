from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from app_streamlit.data_io import read_table_from_bytes, save_dataframe, to_excel_bytes
from stats_engine import infer_schema, missingness_summary

st.title("Data")
st.caption("Load a dataset, review its structure, and export a cleaned snapshot. The sample dataset is synthetic and suitable for demos.")

EXPORT_DIR = Path("storage/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

if "df" not in st.session_state:
    st.session_state["df"] = None
if "dataset_name" not in st.session_state:
    st.session_state["dataset_name"] = "dataset"
if "dataset_source_ext" not in st.session_state:
    st.session_state["dataset_source_ext"] = "csv"

supported_types = ["csv", "xls", "xlsx", "ods"]
uploaded = st.file_uploader(
    "Upload tabular data",
    type=supported_types,
    help="Supported formats: CSV, XLS, XLSX, ODS.",
)
if uploaded is not None:
    try:
        loaded_df, name, ext = read_table_from_bytes(uploaded.name, uploaded.getvalue())
        st.session_state["df"] = loaded_df
        st.session_state["dataset_name"] = name
        st.session_state["dataset_source_ext"] = ext
        st.success(f"Loaded {uploaded.name} ({len(loaded_df)} rows, {len(loaded_df.columns)} columns).")
    except Exception as exc:
        st.error(f"Could not load file: {exc}")

if st.button("Load sample dataset"):
    sample_name = "sample_students"
    st.session_state["df"] = pd.read_csv("data/sample_students.csv")
    st.session_state["dataset_name"] = sample_name
    st.session_state["dataset_source_ext"] = "csv"

if st.session_state["df"] is not None:
    df = st.session_state["df"]
    st.subheader("Editable Preview")
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="data_editor")
    st.session_state["df"] = edited_df
    df = edited_df

    st.subheader("Schema")
    schema = infer_schema(df)
    st.dataframe(pd.DataFrame(schema["columns"]), use_container_width=True)

    st.subheader("Missingness")
    missingness = missingness_summary(df)
    if isinstance(missingness, dict) and "columns" in missingness:
        st.dataframe(pd.DataFrame(missingness["columns"]), use_container_width=True)
    else:
        st.write(missingness)

    st.subheader("Save / Export Current Data")
    default_name = st.session_state.get("dataset_name", "dataset")
    export_name = st.text_input("File base name", value=default_name, key="export_name")
    save_format = st.selectbox("Save format", options=["parquet", "csv", "xlsx"], index=0)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_name}_{ts}"

    if st.button("Save to local storage", key="save_local_dataset"):
        try:
            path = save_dataframe(df, EXPORT_DIR / filename, save_format)
            st.success(f"Saved: {path}")
        except Exception as exc:
            st.error(f"Could not save file: {exc}")

    st.caption("Download current data snapshot")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"{filename}.csv",
        mime="text/csv",
    )
    st.download_button(
        label="Download XLSX",
        data=to_excel_bytes(df),
        file_name=f"{filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    try:
        st.download_button(
            label="Download Parquet",
            data=df.to_parquet(index=False),
            file_name=f"{filename}.parquet",
            mime="application/octet-stream",
        )
    except Exception as exc:
        st.info(f"Parquet download unavailable: {exc}")
else:
    st.info("Upload a CSV/XLS/XLSX/ODS file or load the sample dataset to begin.")

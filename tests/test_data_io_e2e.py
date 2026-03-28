from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
import pytest

from app_streamlit.data_io import read_table_from_bytes, save_dataframe, to_excel_bytes


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "score": [91.5, 87.0, 93.25],
            "group": ["A", "B", "A"],
        }
    )


def test_read_csv_bytes_e2e():
    df = _sample_df()
    payload = df.to_csv(index=False).encode("utf-8")

    out_df, dataset_name, ext = read_table_from_bytes("students.csv", payload)

    assert ext == "csv"
    assert dataset_name == "students"
    assert out_df.shape == df.shape
    assert list(out_df.columns) == list(df.columns)


def test_read_xlsx_bytes_e2e():
    pytest.importorskip("openpyxl")
    df = _sample_df()
    payload = to_excel_bytes(df)

    out_df, dataset_name, ext = read_table_from_bytes("students.xlsx", payload)

    assert ext == "xlsx"
    assert dataset_name == "students"
    assert out_df.shape == df.shape
    assert list(out_df.columns) == list(df.columns)


def test_read_ods_bytes_e2e():
    pytest.importorskip("odf")
    df = _sample_df()
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="odf")

    out_df, dataset_name, ext = read_table_from_bytes("students.ods", buffer.getvalue())

    assert ext == "ods"
    assert dataset_name == "students"
    assert out_df.shape == df.shape
    assert list(out_df.columns) == list(df.columns)


def test_save_dataframe_roundtrip_e2e(tmp_path: Path):
    df = _sample_df()
    base = tmp_path / "edited_students"

    csv_path = save_dataframe(df, base, "csv")
    parquet_path = save_dataframe(df, base, "parquet")

    assert csv_path.exists()
    assert parquet_path.exists()
    assert csv_path.with_suffix(".csv.schema.json").exists()
    assert parquet_path.with_suffix(".parquet.schema.json").exists()

    xlsx_df = None
    xlsx_path = None
    try:
        import openpyxl  # noqa: F401
        xlsx_path = save_dataframe(df, base, "xlsx")
    except ModuleNotFoundError:
        xlsx_path = None

    if xlsx_path is not None:
        assert xlsx_path.exists()
        assert xlsx_path.with_suffix(".xlsx.schema.json").exists()
        xlsx_df = pd.read_excel(xlsx_path)

    csv_df = pd.read_csv(csv_path)
    parquet_df = pd.read_parquet(parquet_path)

    assert csv_df.shape == df.shape
    if xlsx_df is not None:
        assert xlsx_df.shape == df.shape
    assert parquet_df.shape == df.shape


def test_save_dataframe_invalid_format():
    df = _sample_df()
    with pytest.raises(ValueError):
        save_dataframe(df, Path("out"), "json")


def test_schema_sidecar_contains_basic_metadata(tmp_path: Path):
    df = _sample_df()
    csv_path = save_dataframe(df, tmp_path / "students_export", "csv")
    sidecar = csv_path.with_suffix(".csv.schema.json")

    payload = pd.read_json(sidecar)
    assert sidecar.exists()
    assert "id" in sidecar.read_text(encoding="utf-8")
    assert "row_count" in sidecar.read_text(encoding="utf-8")

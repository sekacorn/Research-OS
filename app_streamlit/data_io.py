"""Data I/O helpers for the Streamlit Data page."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd

from stats_engine import infer_schema


def read_table_from_bytes(filename: str, payload: bytes) -> Tuple[pd.DataFrame, str, str]:
    """Read tabular data from uploaded bytes for supported formats."""
    ext = Path(filename).suffix.lower().lstrip(".")
    stream = BytesIO(payload)

    if ext == "csv":
        df = pd.read_csv(stream)
    elif ext in {"xls", "xlsx", "ods"}:
        engine = None
        if ext == "ods":
            engine = "odf"
        elif ext == "xls":
            engine = "xlrd"
        df = pd.read_excel(stream, engine=engine)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    dataset_name = Path(filename).stem or "dataset"
    return df, dataset_name, ext


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Render dataframe to XLSX bytes."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="data")
    return buffer.getvalue()


def dataset_schema_descriptor(df: pd.DataFrame, data_path: Path) -> Dict[str, Any]:
    """Create a simple machine-readable schema sidecar for exported datasets."""
    schema = infer_schema(df)
    fields = []
    for col in schema["columns"]:
        fields.append(
            {
                "name": col["name"],
                "type": col["type"],
                "missing": col["missing"],
                "unique": col["unique"],
            }
        )
    return {
        "profile": "tabular-data-package",
        "name": data_path.stem,
        "path": data_path.name,
        "format": data_path.suffix.lstrip("."),
        "fields": fields,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
    }


def write_dataset_schema_sidecar(df: pd.DataFrame, data_path: Path) -> Path:
    """Write a JSON schema descriptor next to an exported dataset."""
    descriptor = dataset_schema_descriptor(df, data_path)
    sidecar_path = data_path.with_suffix(data_path.suffix + ".schema.json")
    sidecar_path.write_text(json.dumps(descriptor, indent=2), encoding="utf-8")
    return sidecar_path


def save_dataframe(df: pd.DataFrame, path: Path, fmt: str) -> Path:
    """Save dataframe in a selected format and return destination path."""
    fmt = fmt.lower()
    if fmt == "parquet":
        out = path.with_suffix(".parquet")
        df.to_parquet(out, index=False)
        write_dataset_schema_sidecar(df, out)
        return out
    if fmt == "xlsx":
        out = path.with_suffix(".xlsx")
        df.to_excel(out, index=False)
        write_dataset_schema_sidecar(df, out)
        return out
    if fmt == "csv":
        out = path.with_suffix(".csv")
        df.to_csv(out, index=False)
        write_dataset_schema_sidecar(df, out)
        return out
    raise ValueError(f"Unsupported save format: {fmt}")

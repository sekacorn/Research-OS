"""Schema detection for datasets."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def infer_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Infer a simple schema with column types and basic stats.

    Types: numeric, categorical, boolean, datetime, text
    """
    schema = {"columns": []}
    for col in df.columns:
        series = df[col]
        dtype = series.dtype
        col_info: Dict[str, Any] = {"name": col}

        if pd.api.types.is_bool_dtype(dtype):
            col_type = "boolean"
        elif pd.api.types.is_numeric_dtype(dtype):
            col_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            col_type = "datetime"
        else:
            unique_count = series.dropna().nunique()
            if unique_count <= max(20, int(len(series) * 0.05)):
                col_type = "categorical"
            else:
                col_type = "text"

        col_info["type"] = col_type
        col_info["missing"] = int(series.isna().sum())
        col_info["unique"] = int(series.dropna().nunique())
        schema["columns"].append(col_info)

    return schema

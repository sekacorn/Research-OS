"""Basic cleaning utilities."""

from __future__ import annotations

from typing import Dict, Any, Optional

import pandas as pd


def missingness_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Return missingness counts and rates per column."""
    total = len(df)
    columns = []
    for col in df.columns:
        missing = int(df[col].isna().sum())
        rate = float(missing / total) if total else 0.0
        columns.append({"name": col, "missing": missing, "missing_rate": rate})
    return {"n": total, "columns": columns}


def drop_missing(df: pd.DataFrame, how: str = "any") -> pd.DataFrame:
    """Drop rows with missing values.

    how: "any" or "all"
    """
    return df.dropna(how=how)


def fill_missing(df: pd.DataFrame, strategy: str = "mean", value: Optional[Any] = None) -> pd.DataFrame:
    """Fill missing values with a simple strategy.

    strategy: mean, median, mode, constant
    """
    df_filled = df.copy()
    for col in df.columns:
        if not df_filled[col].isna().any():
            continue
        if strategy == "mean" and pd.api.types.is_numeric_dtype(df_filled[col]):
            df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
        elif strategy == "median" and pd.api.types.is_numeric_dtype(df_filled[col]):
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        elif strategy == "mode":
            mode_val = df_filled[col].mode(dropna=True)
            if not mode_val.empty:
                df_filled[col] = df_filled[col].fillna(mode_val.iloc[0])
        elif strategy == "constant":
            df_filled[col] = df_filled[col].fillna(value)
    return df_filled

"""Exploratory data analysis helpers."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PALETTE = [
    "#0f766e",
    "#f59e0b",
    "#2563eb",
    "#dc2626",
    "#7c3aed",
    "#059669",
    "#db2777",
    "#4f46e5",
]


def _apply_plot_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        height=320,
        margin=dict(l=18, r=18, t=44, b=18),
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#ffffff",
        font=dict(color="#0f172a"),
        title=dict(font=dict(size=16)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#e2e8f0", zeroline=False)
    return fig


def describe_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Return descriptive stats for numeric and categorical columns."""
    numeric = df.select_dtypes(include=[np.number])
    categorical = df.select_dtypes(exclude=[np.number])

    numeric_desc = numeric.describe().to_dict() if not numeric.empty else {}
    categorical_desc = {}
    for col in categorical.columns:
        counts = categorical[col].value_counts(dropna=False).head(10)
        categorical_desc[col] = counts.to_dict()

    return {
        "numeric": numeric_desc,
        "categorical_top_counts": categorical_desc,
    }


def correlation_matrix(df: pd.DataFrame) -> Dict[str, Any]:
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return {"columns": [], "matrix": []}
    corr = numeric.corr().fillna(0.0)
    return {"columns": list(corr.columns), "matrix": corr.values.tolist()}


def _safe_numeric_columns(df: pd.DataFrame) -> List[str]:
    return list(df.select_dtypes(include=[np.number]).columns)


def _safe_categorical_columns(df: pd.DataFrame) -> List[str]:
    return list(df.select_dtypes(exclude=[np.number]).columns)


def generate_basic_plots(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate up to 12 basic plots as Plotly figures.

    Returns list of dicts: {"title": str, "fig": plotly_figure}
    """
    plots: List[Dict[str, Any]] = []
    num_cols = _safe_numeric_columns(df)
    cat_cols = _safe_categorical_columns(df)

    # Histograms (up to 4)
    for col in num_cols[:4]:
        fig = px.histogram(df, x=col, title=f"Histogram: {col}", nbins=18)
        fig.update_traces(marker_color=PALETTE[0], marker_line_color="#ffffff", marker_line_width=1)
        fig.update_layout(bargap=0.08)
        fig = _apply_plot_style(fig)
        plots.append({"title": f"Histogram: {col}", "fig": fig})

    # Box plots (up to 2)
    for col in num_cols[4:6]:
        fig = px.box(df, y=col, title=f"Boxplot: {col}")
        fig.update_traces(marker_color=PALETTE[2], line_color=PALETTE[2], fillcolor="#bfdbfe")
        fig = _apply_plot_style(fig)
        plots.append({"title": f"Boxplot: {col}", "fig": fig})

    # Categorical bar charts (up to 4)
    for col in cat_cols[:4]:
        counts = df[col].astype(str).value_counts().head(20)
        fig = px.bar(x=counts.index, y=counts.values, title=f"Counts: {col}")
        fig.update_layout(xaxis_title=col, yaxis_title="count")
        fig.update_traces(marker_color=PALETTE[: len(counts)])
        fig = _apply_plot_style(fig)
        plots.append({"title": f"Counts: {col}", "fig": fig})

    # Scatter plot (1)
    if len(num_cols) >= 2:
        fig = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"Scatter: {num_cols[0]} vs {num_cols[1]}")
        fig.update_traces(marker=dict(color=PALETTE[4], size=9, opacity=0.8))
        fig = _apply_plot_style(fig)
        plots.append({"title": f"Scatter: {num_cols[0]} vs {num_cols[1]}", "fig": fig})

    # Correlation heatmap (1)
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().fillna(0.0)
        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale=[
                    [0.0, "#1d4ed8"],
                    [0.5, "#f8fafc"],
                    [1.0, "#b91c1c"],
                ],
                zmin=-1,
                zmax=1,
            )
        )
        fig.update_layout(title="Correlation Heatmap")
        fig = _apply_plot_style(fig)
        plots.append({"title": "Correlation Heatmap", "fig": fig})

    return plots[:12]

from __future__ import annotations

import pandas as pd

from stats_engine.cleaning import drop_missing, fill_missing, missingness_summary
from stats_engine.eda import correlation_matrix, describe_dataframe, generate_basic_plots


def test_missingness_summary_and_drop_missing():
    df = pd.DataFrame(
        {
            "a": [1.0, None, 3.0],
            "b": ["x", None, "z"],
        }
    )
    out = missingness_summary(df)
    assert out["n"] == 3
    cols = {c["name"]: c for c in out["columns"]}
    assert cols["a"]["missing"] == 1
    assert cols["b"]["missing"] == 1

    any_dropped = drop_missing(df, how="any")
    assert len(any_dropped) == 2
    all_dropped = drop_missing(df, how="all")
    assert len(all_dropped) == 2


def test_fill_missing_strategies():
    df = pd.DataFrame(
        {
            "num": [1.0, None, 5.0],
            "num2": [2.0, None, 8.0],
            "cat": ["a", None, "a"],
        }
    )

    mean_df = fill_missing(df, strategy="mean")
    assert mean_df["num"].isna().sum() == 0
    assert mean_df["num2"].isna().sum() == 0

    median_df = fill_missing(df, strategy="median")
    assert median_df["num"].isna().sum() == 0

    mode_df = fill_missing(df, strategy="mode")
    assert mode_df["cat"].isna().sum() == 0
    assert mode_df.loc[1, "cat"] == "a"

    const_df = fill_missing(df, strategy="constant", value="MISSING")
    assert const_df.loc[1, "cat"] == "MISSING"


def test_describe_and_correlation_matrix():
    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4],
            "y": [2, 4, 6, 8],
            "label": ["g1", "g1", "g2", "g2"],
        }
    )
    desc = describe_dataframe(df)
    assert "numeric" in desc
    assert "categorical_top_counts" in desc
    assert "x" in desc["numeric"]
    assert "label" in desc["categorical_top_counts"]

    corr = correlation_matrix(df)
    assert corr["columns"] == ["x", "y"]
    assert len(corr["matrix"]) == 2

    one_num = correlation_matrix(df[["label"]])
    assert one_num == {"columns": [], "matrix": []}


def test_generate_basic_plots_shape():
    df = pd.DataFrame(
        {
            "n1": [1, 2, 3, 4, 5],
            "n2": [5, 4, 3, 2, 1],
            "n3": [2, 2, 3, 3, 4],
            "n4": [1, 1, 1, 2, 2],
            "n5": [3, 3, 4, 4, 5],
            "n6": [9, 8, 7, 6, 5],
            "c1": ["a", "b", "a", "b", "c"],
            "c2": ["u", "u", "v", "v", "v"],
            "c3": ["x", "x", "y", "y", "z"],
            "c4": ["m", "n", "n", "m", "m"],
            "c5": ["p", "q", "p", "q", "r"],
        }
    )
    plots = generate_basic_plots(df)
    # Hard cap in implementation.
    assert len(plots) <= 12
    titles = [p["title"] for p in plots]
    assert any(t.startswith("Histogram:") for t in titles)
    assert any(t.startswith("Counts:") for t in titles)
    assert "Correlation Heatmap" in titles

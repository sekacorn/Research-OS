"""Group hypothesis tests."""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
from scipy import stats

from stats_engine.effect_sizes import cohens_d, cramers_v


def t_test(df: pd.DataFrame, value_col: str, group_col: str) -> Dict[str, Any]:
    """Two-sample t-test for a numeric value by two groups."""
    groups = df[group_col].dropna().unique().tolist()
    if len(groups) != 2:
        raise ValueError("t_test requires exactly two groups")
    g1, g2 = groups
    x1 = df[df[group_col] == g1][value_col].dropna()
    x2 = df[df[group_col] == g2][value_col].dropna()

    stat, p = stats.ttest_ind(x1, x2, equal_var=False, nan_policy="omit")
    d = cohens_d(x1, x2)

    return {
        "kind": "test",
        "test_name": "t_test",
        "n": int(len(x1) + len(x2)),
        "variables": {"y": value_col, "group": group_col},
        "statistic": float(stat),
        "p_value": float(p),
        "effect_size": {"name": "cohens_d", "value": d},
        "ci": None,
        "assumptions": [],
        "warnings": [],
        "notes": [f"Groups compared: {g1} vs {g2}"],
    }


def chi_square(df: pd.DataFrame, col_x: str, col_y: str) -> Dict[str, Any]:
    """Chi-square test of independence for two categorical variables."""
    table = pd.crosstab(df[col_x], df[col_y])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    v = cramers_v(table.values, chi2=chi2)

    return {
        "kind": "test",
        "test_name": "chi_square",
        "n": int(table.values.sum()),
        "variables": {"x": col_x, "y": col_y},
        "statistic": float(chi2),
        "p_value": float(p),
        "effect_size": {"name": "cramers_v", "value": v},
        "ci": None,
        "assumptions": [],
        "warnings": [],
        "notes": [f"Degrees of freedom: {dof}"],
    }


def available_tests() -> List[str]:
    return ["t_test", "chi_square"]

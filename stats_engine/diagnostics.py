"""Model diagnostics."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import jarque_bera


def compute_vif(df: pd.DataFrame) -> float:
    """Return max VIF for numeric columns."""
    if df.shape[1] < 2:
        return float("nan")
    x = df.dropna().values
    if x.shape[1] < 2 or x.shape[0] < 3:
        return float("nan")
    vifs = []
    for i in range(x.shape[1]):
        vifs.append(variance_inflation_factor(x, i))
    return float(np.nanmax(vifs))


def heteroskedasticity_flag(model_results: Any, alpha: float = 0.05) -> bool:
    """Return True if Breusch-Pagan indicates heteroskedasticity."""
    try:
        lm_stat, lm_p, f_stat, f_p = het_breuschpagan(model_results.resid, model_results.model.exog)
        return bool(lm_p < alpha)
    except Exception:
        return False


def non_normal_residuals_flag(model_results: Any, alpha: float = 0.05) -> bool:
    """Return True if Jarque-Bera indicates non-normal residuals."""
    try:
        jb_stat, jb_p, _, _ = jarque_bera(model_results.resid)
        return bool(jb_p < alpha)
    except Exception:
        return False


def diagnostics_summary(model_results: Any, df_exog: pd.DataFrame) -> Dict[str, Any]:
    return {
        "vif_max": compute_vif(df_exog),
        "heteroskedasticity_flag": heteroskedasticity_flag(model_results),
        "non_normal_residuals_flag": non_normal_residuals_flag(model_results),
    }

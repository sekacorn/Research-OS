"""Regression models."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from stats_engine.diagnostics import diagnostics_summary


def _build_formula(y: str, xs: List[str]) -> str:
    # Build one explicit formula string so debugging stays straightforward.
    return f"{y} ~ " + " + ".join(xs)


def _safe_exp(value: float) -> Tuple[float, bool]:
    """Exponentiate with clipping to avoid float overflow warnings."""
    # Confidence-interval transforms can spike quickly; clipping keeps this numerically stable.
    max_log = float(np.log(np.finfo(float).max))
    clipped_value = float(np.clip(value, -max_log, max_log))
    return float(np.exp(clipped_value)), clipped_value != float(value)


def _standardized_betas(df: pd.DataFrame, y: str, xs: List[str]) -> List[Dict[str, Any]]:
    numeric_xs = [x for x in xs if pd.api.types.is_numeric_dtype(df[x])]
    if not numeric_xs or not pd.api.types.is_numeric_dtype(df[y]):
        return []
    sub = df[[y] + numeric_xs].dropna()
    if sub.empty:
        return []
    z = (sub - sub.mean()) / sub.std(ddof=0)
    model = sm.OLS(z[y], sm.add_constant(z[numeric_xs], has_constant="add")).fit()
    effects = []
    for term, coef in model.params.items():
        if term == "const":
            continue
        effects.append({"term": term, "name": "standardized_beta", "value": float(coef)})
    return effects


def run_ols(df: pd.DataFrame, y: str, xs: List[str]) -> Dict[str, Any]:
    # This function outputs raw model facts only; narrative interpretation belongs to the coach layer.
    formula = _build_formula(y, xs)
    model = smf.ols(formula=formula, data=df).fit()
    conf = model.conf_int()

    coef_rows = []
    for term, coef in model.params.items():
        se = model.bse.get(term, np.nan)
        p = model.pvalues.get(term, np.nan)
        ci_low, ci_high = conf.loc[term].tolist()
        coef_rows.append(
            {
                "term": term,
                "estimate": float(coef),
                "se": float(se),
                "p": float(p),
                "ci": {"low": float(ci_low), "high": float(ci_high)},
            }
        )

    effect_sizes = _standardized_betas(df, y, xs)
    diagnostics = diagnostics_summary(model, df[xs].select_dtypes(include=[np.number]))

    return {
        "kind": "model",
        "model_name": "ols",
        "formula": formula,
        "n": int(model.nobs),
        "coefficients": coef_rows,
        "effect_sizes": effect_sizes,
        "diagnostics": diagnostics,
        "warnings": [],
    }


def run_logit(df: pd.DataFrame, y: str, xs: List[str]) -> Dict[str, Any]:
    # Fail softly here so the pipeline still returns structured warnings instead of crashing.
    formula = _build_formula(y, xs)
    warnings: List[str] = []
    try:
        model = smf.logit(formula=formula, data=df).fit(disp=False, method="lbfgs", maxiter=100)
    except Exception as exc:
        warnings.append(f"Logit fit failed: {exc}")
        return {
            "kind": "model",
            "model_name": "logit",
            "formula": formula,
            "n": int(df[y].dropna().shape[0]),
            "coefficients": [],
            "effect_sizes": [],
            "diagnostics": {},
            "warnings": warnings,
        }

    coef_rows = []
    odds_ratios = []
    conf = model.conf_int()
    for term, coef in model.params.items():
        se = model.bse.get(term, np.nan)
        p = model.pvalues.get(term, np.nan)
        ci_low, ci_high = conf.loc[term].tolist()
        coef_rows.append(
            {
                "term": term,
                "estimate": float(coef),
                "se": float(se),
                "p": float(p),
                "ci": {"low": float(ci_low), "high": float(ci_high)},
            }
        )
        if term != "Intercept":
            # This exponentiation step is the usual overflow hotspot, so it is guarded on purpose.
            odds_ratio, coef_clipped = _safe_exp(float(coef))
            ci_low_exp, ci_low_clipped = _safe_exp(float(ci_low))
            ci_high_exp, ci_high_clipped = _safe_exp(float(ci_high))
            odds_ratios.append(
                {
                    "term": term,
                    "name": "odds_ratio",
                    "value": odds_ratio,
                    "ci": {"low": ci_low_exp, "high": ci_high_exp},
                }
            )
            if coef_clipped or ci_low_clipped or ci_high_clipped:
                warnings.append(
                    f"Logit odds ratio for term '{term}' required numeric clipping in exp transform."
                )

    diagnostics = diagnostics_summary(model, df[xs].select_dtypes(include=[np.number]))

    return {
        "kind": "model",
        "model_name": "logit",
        "formula": formula,
        "n": int(model.nobs),
        "coefficients": coef_rows,
        "effect_sizes": odds_ratios,
        "diagnostics": diagnostics,
        "warnings": warnings,
    }

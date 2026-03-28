"""Methods + Assumptions Coach

This module converts *structured* statistical outputs into research-quality narrative:
- Methods wording
- Assumption checks and warnings
- Limitations
- Next steps

Design goals:
- Deterministic output (no randomness)
- Cautious, precise language (no causal claims by default)
- No re-implementation of statistical computation; only summarize existing results
"""

from __future__ import annotations

from typing import Any, Dict, List


# -----------------------------
# Public API
# -----------------------------

def summarize_test(result: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize a hypothesis test result into research-ready text blocks.

    Expected `result` shape (minimal):
      {
        "kind": "test",
        "test_name": "t_test" | "chi_square" | "anova" | ...,
        "n": int,
        "variables": {"y": "...", "group": "..."} OR similar,
        "p_value": float,
        "effect_size": {"name": str, "value": float} OR None,
        "ci": {"low": float, "high": float} OR None,
        "assumptions": [{"name": str, "passed": bool, "detail": str}, ...] OR [],
        "warnings": [str, ...] OR [],
        "notes": [str, ...] OR []
      }

    Returns:
      {
        "methods_text": str,
        "interpretation_text": str,
        "assumptions_checked": List[dict],
        "warnings": List[str],
        "limitations": List[str],
        "next_steps": List[str],
      }
    """
    # Normalize first so every template path stays predictable when fields are missing.
    test_name = str(result.get("test_name", "unknown_test"))
    n = _safe_int(result.get("n"))

    assumptions = list(result.get("assumptions") or [])
    warnings = list(result.get("warnings") or [])

    methods_text = _methods_for_test(test_name, result)
    interpretation_text = _interpret_test(test_name, result)

    limitations = _limitations_common(n=n, warnings=warnings, assumptions=assumptions)
    limitations += _limitations_for_test(test_name, result)

    next_steps = _next_steps_for_test(test_name, result, warnings=warnings, assumptions=assumptions)

    return {
        "methods_text": methods_text,
        "interpretation_text": interpretation_text,
        "assumptions_checked": assumptions,
        "warnings": warnings,
        "limitations": limitations,
        "next_steps": next_steps,
    }


def summarize_model(result: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize a regression/model result into research-ready text blocks.

    Expected `result` shape (minimal):
      {
        "kind": "model",
        "model_name": "ols" | "logit" | ...,
        "formula": "y ~ x1 + x2" OR {"y": "...", "xs": [...]},
        "n": int,
        "coefficients": [{"term": str, "estimate": float, "se": float, "p": float, "ci": {...}}, ...],
        "effect_sizes": [{"term": str, "name": str, "value": float}, ...] OR [],
        "diagnostics": {"vif_max": float, "heteroskedasticity_flag": bool, ...} OR {},
        "warnings": [str, ...] OR []
      }

    Returns:
      {
        "model_spec": str,
        "effect_size_summary": str,
        "diagnostics_summary": str,
        "interpretation_text": str,
        "limitations": List[str],
        "next_steps": List[str],
      }
    """
    # Use the same pattern as tests so degraded input handling stays calm and deterministic.
    model_name = str(result.get("model_name", "unknown_model"))
    n = _safe_int(result.get("n"))

    diagnostics = dict(result.get("diagnostics") or {})
    warnings = list(result.get("warnings") or [])
    assumptions = list(result.get("assumptions") or [])

    model_spec = _model_spec_text(model_name, result)
    effect_size_summary = _effect_size_summary(model_name, result)
    diagnostics_summary = _diagnostics_summary(model_name, diagnostics, warnings=warnings)

    interpretation_text = _interpret_model(model_name, result)

    limitations = _limitations_common(n=n, warnings=warnings, assumptions=assumptions)
    limitations += _limitations_for_model(model_name, result, diagnostics=diagnostics)

    next_steps = _next_steps_for_model(model_name, result, diagnostics=diagnostics, warnings=warnings)

    return {
        "model_spec": model_spec,
        "effect_size_summary": effect_size_summary,
        "diagnostics_summary": diagnostics_summary,
        "interpretation_text": interpretation_text,
        "limitations": limitations,
        "next_steps": next_steps,
    }


def methods_block_for_report(analysis_bundle: Dict[str, Any]) -> str:
    """Create a report-ready METHODS section from an analysis bundle.

    Suggested `analysis_bundle` shape:
      {
        "dataset": {"name": "...", "n": int, "columns": [...]},
        "cleaning": {...},
        "tests": [<test result dicts>],
        "models": [<model result dicts>],
      }
    """
    ds = analysis_bundle.get("dataset") or {}
    n = _safe_int(ds.get("n"))
    cols = ds.get("columns") or []

    lines: List[str] = []
    lines.append("## Methods")
    lines.append(f"Data were analyzed using a reproducible workflow. The dataset contained n={n} rows and {len(cols)} columns.")
    lines.append("Descriptive statistics and exploratory plots were generated prior to inferential testing.")

    if analysis_bundle.get("tests"):
        lines.append("Inferential tests were selected based on variable types and distribution checks. Effect sizes were reported where applicable.")
    if analysis_bundle.get("models"):
        lines.append("Regression models were fit to estimate associations while reporting diagnostics and assumption warnings.")

    lines.append("Results should be interpreted as associations unless the study design supports causal inference.")

    return "\n".join(lines)


# -----------------------------
# Internals (templated language)
# -----------------------------

def _methods_for_test(test_name: str, result: Dict[str, Any]) -> str:
    if test_name in {"t_test", "ttest", "t-test"}:
        return "A two-sample t-test was used to compare mean differences between two groups."
    if test_name in {"chi_square", "chi-square", "chisq"}:
        return "A chi-square test of independence was used to assess association between categorical variables."
    if test_name in {"anova"}:
        return "ANOVA was used to compare mean differences across multiple groups."
    return f"A statistical test ({test_name}) was conducted."


def _interpret_test(test_name: str, result: Dict[str, Any]) -> str:
    p = result.get("p_value")
    if isinstance(p, (int, float)):
        sig = p < 0.05
        if sig:
            return f"The test suggests evidence of a difference/association (p={p:.4g})."
        return f"The test does not suggest strong evidence of a difference/association (p={p:.4g})."
    return "The test result was computed; see p-value and effect size outputs for interpretation."


def _model_spec_text(model_name: str, result: Dict[str, Any]) -> str:
    formula = result.get("formula")
    if isinstance(formula, str) and formula.strip():
        return f"Model: {model_name.upper()} using formula `{formula}`."
    if isinstance(formula, dict):
        y = formula.get("y", "y")
        xs = formula.get("xs", [])
        return f"Model: {model_name.upper()} predicting `{y}` from {', '.join(map(str, xs))}."
    return f"Model: {model_name.upper()} (specification not provided)."


def _effect_size_summary(model_name: str, result: Dict[str, Any]) -> str:
    effs = result.get("effect_sizes") or []
    if not effs:
        # fall back: for logistic, odds ratios may be present in coefficients
        return "Effect sizes were reported where available."
    top = effs[:5]
    parts = []
    for e in top:
        term = e.get("term", "term")
        name = e.get("name", "effect")
        val = e.get("value")
        if isinstance(val, (int, float)):
            parts.append(f"{term}: {name}={val:.3g}")
        else:
            parts.append(f"{term}: {name}")
    return "Effect size summary: " + "; ".join(parts) + ("." if parts else "")


def _diagnostics_summary(model_name: str, diagnostics: Dict[str, Any], warnings: List[str]) -> str:
    parts: List[str] = []
    vif = diagnostics.get("vif_max")
    if isinstance(vif, (int, float)):
        parts.append(f"Max VIF={vif:.3g}")
    if diagnostics.get("heteroskedasticity_flag") is True:
        parts.append("heteroskedasticity warning")
    if diagnostics.get("non_normal_residuals_flag") is True:
        parts.append("residual normality warning")
    if not parts and warnings:
        parts.append("see warnings")  # keeps deterministic output without guessing
    if not parts:
        return "Diagnostics summary: no major flags reported."
    return "Diagnostics summary: " + ", ".join(parts) + "."


def _interpret_model(model_name: str, result: Dict[str, Any]) -> str:
    # Intentional guardrail: describe association and avoid accidental causal language.
    coefs = result.get("coefficients") or []
    if not coefs:
        return "Model fit completed; interpret coefficients with attention to effect sizes and diagnostics."
    # Find a few statistically notable terms
    notable = []
    for c in coefs:
        p = c.get("p")
        if isinstance(p, (int, float)) and p < 0.05:
            notable.append(c)
    notable = notable[:3]
    if not notable:
        return "No coefficients met a conventional significance threshold; consider effect sizes, power, and model specification."
    terms = ", ".join([str(c.get("term", "term")) for c in notable])
    return f"Some predictors show evidence of association with the outcome (e.g., {terms}); interpret in context and review diagnostics."


def _limitations_common(n: int, warnings: List[str], assumptions: List[Dict[str, Any]]) -> List[str]:
    lim: List[str] = []
    if n and n < 50:
        lim.append("Small sample size may reduce statistical power and stability of estimates.")
    if any(a.get("passed") is False for a in assumptions):
        lim.append("One or more test/model assumptions were not met; results should be interpreted with caution.")
    if warnings:
        lim.append("Warnings were generated during analysis; review them before drawing conclusions.")
    lim.append("Associations do not imply causation without an appropriate study design.")
    return lim


def _limitations_for_test(test_name: str, result: Dict[str, Any]) -> List[str]:
    if test_name in {"chi_square", "chi-square", "chisq"}:
        return ["Sparse contingency tables can invalidate chi-square approximations; consider Fisher's exact test if counts are small."]
    return []


def _limitations_for_model(model_name: str, result: Dict[str, Any], diagnostics: Dict[str, Any]) -> List[str]:
    lim: List[str] = []
    vif = diagnostics.get("vif_max")
    if isinstance(vif, (int, float)) and vif >= 10:
        lim.append("High multicollinearity (VIF) can inflate standard errors and destabilize coefficient estimates.")
    if diagnostics.get("heteroskedasticity_flag") is True:
        lim.append("Heteroskedasticity may bias standard errors; consider robust standard errors.")
    return lim


def _next_steps_for_test(test_name: str, result: Dict[str, Any], warnings: List[str], assumptions: List[Dict[str, Any]]) -> List[str]:
    steps: List[str] = []
    steps.append("Report effect sizes alongside p-values and interpret magnitude in context.")
    if any(a.get("passed") is False for a in assumptions):
        steps.append("Consider a non-parametric alternative or transformation if assumptions are violated.")
    if warnings:
        steps.append("Address warnings (e.g., missingness, outliers) and re-run sensitivity checks.")
    steps.append("Consider stratifying analyses or adding covariates if confounding is plausible.")
    return steps


def _next_steps_for_model(model_name: str, result: Dict[str, Any], diagnostics: Dict[str, Any], warnings: List[str]) -> List[str]:
    steps: List[str] = []
    steps.append("Check robustness: re-fit with alternative specifications and compare effect sizes.")
    if diagnostics.get("heteroskedasticity_flag") is True:
        steps.append("Re-fit using robust standard errors and compare inference.")
    vif = diagnostics.get("vif_max")
    if isinstance(vif, (int, float)) and vif >= 10:
        steps.append("Reduce multicollinearity: remove/recombine predictors or use regularization.")
    if warnings:
        steps.append("Resolve data quality warnings (missingness/outliers) and re-run sensitivity analyses.")
    steps.append("Document assumptions and limitations in the report to support transparent interpretation.")
    return steps


def _safe_int(x: Any) -> int:
    try:
        return int(x)
    except Exception:
        return 0

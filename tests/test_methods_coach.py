from stats_engine.methods_coach import summarize_test, summarize_model

def test_summarize_test_shape():
    result = {
        "kind": "test",
        "test_name": "t_test",
        "n": 40,
        "p_value": 0.03,
        "effect_size": {"name": "cohens_d", "value": 0.6},
        "assumptions": [{"name": "normality", "passed": True, "detail": "ok"}],
        "warnings": ["missingness detected"],
    }
    out = summarize_test(result)
    assert set(out.keys()) == {
        "methods_text",
        "interpretation_text",
        "assumptions_checked",
        "warnings",
        "limitations",
        "next_steps",
    }
    assert "t-test" in out["methods_text"].lower() or "t test" in out["methods_text"].lower()
    assert out["warnings"] == ["missingness detected"]
    assert isinstance(out["limitations"], list)
    assert isinstance(out["next_steps"], list)

def test_summarize_model_includes_diagnostics_flags():
    result = {
        "kind": "model",
        "model_name": "ols",
        "formula": "math_score ~ participation_rate + grade_level",
        "n": 35,
        "coefficients": [
            {"term": "participation_rate", "estimate": 10.0, "se": 2.0, "p": 0.01},
            {"term": "grade_level", "estimate": 1.0, "se": 0.5, "p": 0.08},
        ],
        "diagnostics": {"vif_max": 12.0, "heteroskedasticity_flag": True},
        "warnings": [],
    }
    out = summarize_model(result)
    assert "Model:" in out["model_spec"]
    assert "VIF" in out["diagnostics_summary"] or "vif" in out["diagnostics_summary"].lower()
    # high VIF and heteroskedasticity should surface in limitations
    lim = " ".join(out["limitations"]).lower()
    assert "multicollinearity" in lim
    assert "heteroskedastic" in lim

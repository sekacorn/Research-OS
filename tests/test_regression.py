import pandas as pd

from stats_engine.models.regression import run_ols, run_logit
from stats_engine.interpret import attach_coach_to_model


def test_run_ols_with_coach():
    df = pd.read_csv("data/sample_students.csv")
    result = run_ols(df, "math_score", ["participation_rate", "grade_level"])
    result = attach_coach_to_model(result)
    assert "coach" in result
    assert "model_spec" in result["coach"]


def test_run_logit_with_coach():
    df = pd.read_csv("data/sample_students.csv")
    df = df.copy()
    df["math_binary"] = (df["math_score"] > df["math_score"].median()).astype(int)
    result = run_logit(df, "math_binary", ["participation_rate", "grade_level"])
    result = attach_coach_to_model(result)
    assert "coach" in result
    assert "diagnostics_summary" in result["coach"]


def test_run_ols_with_categorical_predictor_does_not_fail():
    df = pd.read_csv("data/sample_students.csv")
    result = run_ols(df, "math_score", ["participation_rate", "school_type"])
    result = attach_coach_to_model(result)
    assert "coach" in result
    assert isinstance(result["effect_sizes"], list)

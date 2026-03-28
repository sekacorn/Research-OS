import pandas as pd

from stats_engine.tests.group_tests import t_test, chi_square
from stats_engine.interpret import attach_coach_to_test


def test_t_test_and_coach():
    df = pd.read_csv("data/sample_students.csv")
    result = t_test(df, "math_score", "school_type")
    result = attach_coach_to_test(result)
    assert "coach" in result
    assert "methods_text" in result["coach"]


def test_chi_square_and_coach():
    df = pd.read_csv("data/sample_students.csv")
    result = chi_square(df, "state", "school_type")
    result = attach_coach_to_test(result)
    assert "coach" in result
    assert "interpretation_text" in result["coach"]

import pandas as pd

from stats_engine.tests.group_tests import t_test
from stats_engine.models.regression import run_ols
from stats_engine.interpret import attach_coach_to_test, attach_coach_to_model
from stats_engine.report import build_html_report
from literature.cite import to_apa


def test_integration_report_contains_sections():
    df = pd.read_csv("data/sample_students.csv")
    test_res = attach_coach_to_test(t_test(df, "math_score", "school_type"))
    model_res = attach_coach_to_model(run_ols(df, "math_score", ["participation_rate", "grade_level"]))

    citation = {"title": "Sample", "authors": "Doe, J.", "year": 2020}
    apa = to_apa(citation)

    bundle = {
        "dataset": {"name": "sample", "n": len(df), "columns": list(df.columns)},
        "tests": [test_res],
        "models": [model_res],
    }
    html = build_html_report(bundle, citations=[{"apa": apa}])

    assert "Methods" in html
    assert "Limitations" in html
    assert "Next Steps" in html
    assert "Citations" in html
    assert apa in html


def test_report_escapes_html_from_inputs():
    bundle = {
        "dataset": {"name": "sample", "n": 1, "columns": ["x"]},
        "tests": [
            {
                "coach": {
                    "methods_text": "<script>alert('x')</script>",
                    "interpretation_text": "<b>unsafe</b>",
                    "limitations": ["<img src=x onerror=alert(1)>"],
                    "next_steps": ["<iframe>bad</iframe>"],
                }
            }
        ],
        "models": [],
    }
    html = build_html_report(bundle, citations=[{"apa": "<svg onload=alert(1)>"}])

    assert "<script>" not in html
    assert "<img src=x onerror=alert(1)>" not in html
    assert "<svg onload=alert(1)>" not in html
    assert "&lt;script&gt;alert" in html

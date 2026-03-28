"""Research OS stats_engine package."""

from .schema import infer_schema
from .cleaning import missingness_summary, drop_missing, fill_missing
from .eda import describe_dataframe, correlation_matrix, generate_basic_plots
from .interpret import attach_coach_to_test, attach_coach_to_model
from .tests.group_tests import t_test, chi_square
from .models import run_ols, run_logit
from .report import build_html_report

__all__ = [
    "infer_schema",
    "missingness_summary",
    "drop_missing",
    "fill_missing",
    "describe_dataframe",
    "correlation_matrix",
    "generate_basic_plots",
    "attach_coach_to_test",
    "attach_coach_to_model",
    "t_test",
    "chi_square",
    "run_ols",
    "run_logit",
    "build_html_report",
]

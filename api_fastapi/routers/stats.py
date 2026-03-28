from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
from fastapi import APIRouter, HTTPException

from stats_engine import infer_schema
from stats_engine.eda import describe_dataframe, correlation_matrix
from stats_engine.tests.group_tests import t_test, chi_square
from stats_engine.models.regression import run_ols, run_logit
from stats_engine.interpret import attach_coach_to_test, attach_coach_to_model
from stats_engine.report import build_html_report

from api_fastapi.schemas.stats import (
    DataPayload,
    TTestRequest,
    ChiSquareRequest,
    RegressionRequest,
    ReportRequest,
)

router = APIRouter(prefix="/stats", tags=["stats"])


def _df(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _bad_request(exc: Exception) -> HTTPException:
    return HTTPException(status_code=400, detail=str(exc))


@router.post("/schema")
def schema(payload: DataPayload) -> Dict[str, Any]:
    return infer_schema(_df(payload.rows))


@router.post("/eda")
def eda(payload: DataPayload) -> Dict[str, Any]:
    df = _df(payload.rows)
    return {
        "summary": describe_dataframe(df),
        "correlation": correlation_matrix(df),
    }


@router.post("/t_test")
def t_test_api(payload: TTestRequest) -> Dict[str, Any]:
    try:
        result = t_test(_df(payload.rows), payload.value_col, payload.group_col)
        return attach_coach_to_test(result)
    except (KeyError, ValueError) as exc:
        raise _bad_request(exc) from exc


@router.post("/chi_square")
def chi_square_api(payload: ChiSquareRequest) -> Dict[str, Any]:
    try:
        result = chi_square(_df(payload.rows), payload.col_x, payload.col_y)
        return attach_coach_to_test(result)
    except (KeyError, ValueError) as exc:
        raise _bad_request(exc) from exc


@router.post("/ols")
def ols_api(payload: RegressionRequest) -> Dict[str, Any]:
    try:
        result = run_ols(_df(payload.rows), payload.y, payload.xs)
        return attach_coach_to_model(result)
    except (KeyError, ValueError) as exc:
        raise _bad_request(exc) from exc


@router.post("/logit")
def logit_api(payload: RegressionRequest) -> Dict[str, Any]:
    try:
        result = run_logit(_df(payload.rows), payload.y, payload.xs)
        return attach_coach_to_model(result)
    except (KeyError, ValueError) as exc:
        raise _bad_request(exc) from exc


@router.post("/report")
def report_api(payload: ReportRequest) -> Dict[str, Any]:
    df = _df(payload.rows)
    bundle = {
        "dataset": {"name": payload.dataset_name, "n": len(df), "columns": list(df.columns)},
        "tests": payload.tests,
        "models": payload.models,
    }
    html = build_html_report(bundle, citations=payload.citations or [])
    return {"html": html}

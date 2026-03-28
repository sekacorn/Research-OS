from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DataPayload(BaseModel):
    rows: List[Dict[str, Any]]


class TTestRequest(BaseModel):
    rows: List[Dict[str, Any]]
    value_col: str
    group_col: str


class ChiSquareRequest(BaseModel):
    rows: List[Dict[str, Any]]
    col_x: str
    col_y: str


class RegressionRequest(BaseModel):
    rows: List[Dict[str, Any]]
    y: str
    xs: List[str]


class ReportRequest(BaseModel):
    dataset_name: str
    rows: List[Dict[str, Any]]
    tests: List[Dict[str, Any]]
    models: List[Dict[str, Any]]
    citations: Optional[List[Dict[str, Any]]] = None

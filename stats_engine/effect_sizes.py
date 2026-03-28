"""Effect size calculations."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np
from scipy import stats


def cohens_d(x1: Any, x2: Any) -> float:
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    n1, n2 = len(x1), len(x2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    s1 = np.var(x1, ddof=1)
    s2 = np.var(x2, ddof=1)
    pooled = ((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2)
    if pooled <= 0:
        return 0.0
    return float((np.mean(x1) - np.mean(x2)) / np.sqrt(pooled))


def cramers_v(table: Any, chi2: Optional[float] = None) -> float:
    arr = np.asarray(table, dtype=float)
    if arr.size == 0:
        return float("nan")
    if chi2 is None:
        chi2, _, _, _ = stats.chi2_contingency(arr)
    n = arr.sum()
    if n == 0:
        return float("nan")
    r, k = arr.shape
    denom = n * (min(k - 1, r - 1) + 1e-9)
    return float(np.sqrt(chi2 / denom))

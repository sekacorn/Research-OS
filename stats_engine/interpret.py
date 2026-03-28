"""Interpret layer: attach Methods + Assumptions Coach outputs."""

from __future__ import annotations

from typing import Any, Dict

from stats_engine.methods_coach import summarize_model, summarize_test


def attach_coach_to_test(result: Dict[str, Any]) -> Dict[str, Any]:
    # Required handoff from numeric output to interpretation-ready coach text.
    coach = summarize_test(result)
    result["coach"] = coach
    return result


def attach_coach_to_model(result: Dict[str, Any]) -> Dict[str, Any]:
    # Mutate in place so callers keep one result object with both stats and coach sections.
    coach = summarize_model(result)
    result["coach"] = coach
    return result

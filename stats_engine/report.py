"""HTML report generation."""

from __future__ import annotations

from html import escape
from typing import Any, Dict, List, Optional

from stats_engine.methods_coach import methods_block_for_report


def _section(title: str, body: str) -> str:
    return f"<h2>{escape(title)}</h2>\n<p>{escape(body)}</p>"


def _list_section(title: str, items: List[str]) -> str:
    li = "".join([f"<li>{escape(str(i))}</li>" for i in items])
    return f"<h3>{escape(title)}</h3>\n<ul>{li}</ul>"


def build_html_report(analysis_bundle: Dict[str, Any], citations: Optional[List[Dict[str, Any]]] = None) -> str:
    """Build a simple HTML report from analysis results and citations."""
    methods_block = methods_block_for_report(analysis_bundle)

    tests = analysis_bundle.get("tests", [])
    models = analysis_bundle.get("models", [])

    parts = [
        "<html><head><meta charset='utf-8'><title>Research OS Report</title>"
        "<style>"
        "body {"
        "  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;"
        "  line-height: 1.5;"
        "  margin: 0;"
        "  padding: 20px;"
        "  background: #ffffff;"
        "  color: #111827;"
        "}"
        "h1, h2, h3 { color: #0f172a; }"
        "p, li { color: #111827; }"
        "ul { padding-left: 1.25rem; }"
        "@media (prefers-color-scheme: dark) {"
        "  body { background: #0b1220; color: #e5e7eb; }"
        "  h1, h2, h3 { color: #f8fafc; }"
        "  p, li { color: #e5e7eb; }"
        "}"
        "</style></head><body>"
    ]
    parts.append("<h1>Research OS Report</h1>")
    parts.append(escape(methods_block).replace("\n", "<br>"))

    if tests:
        parts.append("<h2>Hypothesis Tests</h2>")
        for t in tests:
            coach = t.get("coach", {})
            parts.append(_section("Test Method", coach.get("methods_text", "")))
            parts.append(_section("Interpretation", coach.get("interpretation_text", "")))
            parts.append(_list_section("Limitations", coach.get("limitations", [])))
            parts.append(_list_section("Next Steps", coach.get("next_steps", [])))

    if models:
        parts.append("<h2>Models</h2>")
        for m in models:
            coach = m.get("coach", {})
            parts.append(_section("Model Spec", coach.get("model_spec", "")))
            parts.append(_section("Effect Sizes", coach.get("effect_size_summary", "")))
            parts.append(_section("Diagnostics", coach.get("diagnostics_summary", "")))
            parts.append(_section("Interpretation", coach.get("interpretation_text", "")))
            parts.append(_list_section("Limitations", coach.get("limitations", [])))
            parts.append(_list_section("Next Steps", coach.get("next_steps", [])))

    if citations:
        parts.append("<h2>Citations</h2>")
        for c in citations:
            parts.append(f"<p>{escape(str(c.get('apa', '')))}</p>")

    parts.append("</body></html>")
    return "\n".join(parts)

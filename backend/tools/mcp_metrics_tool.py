import re
from typing import Any, Dict, Optional

from backend.tools.running_total_tool import get_running_total
from backend.tools.wow_tool import get_wow
from backend.tools.yoy_tool import get_yoy
from backend.tools.snapshot_tool import get_snapshot


def _extract_date(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return dates[0] if dates else None


def _extract_years(text: Optional[str]) -> list[str]:
    if not text:
        return []
    return re.findall(r"\b20\d{2}\b", text)


def execute_metrics_tool(question: str, metric: Optional[str] = None, as_of_date: Optional[str] = None) -> Dict[str, Any]:
    """Execute a metrics tool request against the lakehouse and return traceable output."""

    q = (question or "").lower()
    metric_name = (metric or "").lower().strip()

    if not metric_name:
        if "running" in q:
            metric_name = "running_total"
        elif "wow" in q or "week over week" in q or "week" in q:
            metric_name = "wow"
        elif "yoy" in q or "year over year" in q:
            metric_name = "yoy"
        else:
            metric_name = "running_total"

    date = as_of_date or _extract_date(question)

    if metric_name in {"running_total", "running-total", "running"}:
        if not date:
            date = "2024-01-15"
        snapshot = get_snapshot("local.gold.gold_running_total")
        return {
            "metric": "running_total",
            "result": get_running_total(date),
            "snapshot_id": snapshot["snapshot_id"],
            "committed_at": snapshot["committed_at"],
            "as_of_date": snapshot["committed_at"][:10],
            "requested_date": date,
        }

    if metric_name in {"wow", "week_over_week", "week-over-week"}:
        if not date:
            date = "2024-01-15"
        snapshot = get_snapshot("local.gold.gold_week_over_week")
        return {
            "metric": "wow",
            "result": get_wow(date),
            "snapshot_id": snapshot["snapshot_id"],
            "committed_at": snapshot["committed_at"],
            "as_of_date": snapshot["committed_at"][:10],
            "requested_date": date,
        }

    if metric_name in {"yoy", "year_over_year", "year-over-year"}:
        snapshot = get_snapshot("local.gold.gold_year_over_year")
        years = _extract_years(question)
        if years:
            return {
                "metric": "yoy",
                "result": get_yoy(question),
                "snapshot_id": snapshot["snapshot_id"],
                "committed_at": snapshot["committed_at"],
                "as_of_date": snapshot["committed_at"][:10],
                "requested_years": years,
            }
        return {
            "metric": "yoy",
            "result": get_yoy(question),
            "snapshot_id": snapshot["snapshot_id"],
            "committed_at": snapshot["committed_at"],
            "as_of_date": snapshot["committed_at"][:10],
            "requested_date": date,
        }

    return {
        "metric": metric_name or "unknown",
        "result": "Unsupported metric request.",
        "snapshot_id": None,
        "committed_at": None,
        "as_of_date": None,
    }

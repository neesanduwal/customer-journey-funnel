import re

from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot


def _extract_top_n(question: str, default: int = 10) -> int:
    q = (question or "").lower()
    match = re.search(r"\btop\s+(\d+)\b", q)
    if match:
        return max(1, min(int(match.group(1)), 100))
    return default


def get_customer_summary(question: str = ""):
    spark = create_spark_session()
    snapshot = get_snapshot("local.gold.gold_customer_funnel")
    top_n = _extract_top_n(question, default=10)

    rows = spark.sql(f"""
        SELECT
            customer_id,
            customer_name,
            segment,
            region,
            website_sessions,
            total_leads,
            total_orders,
            total_revenue
        FROM local.gold.gold_customer_funnel
        ORDER BY total_revenue DESC
        LIMIT {top_n}
    """).collect()

    if not rows:
        return "No customer data found."

    lines = ["Customer Funnel Summary", "", f"Top {top_n} Customers", ""]

    for row in rows:
        lines.append(
            f"Customer: {row.customer_name} ({row.customer_id}) | "
            f"Segment: {row.segment} | Region: {row.region} | "
            f"Sessions: {row.website_sessions} | Leads: {row.total_leads} | "
            f"Orders: {row.total_orders} | Revenue: ${float(row.total_revenue):,.2f}"
        )

    lines.extend([
        "",
        f"Source Table : local.gold.gold_customer_funnel",
        f"Snapshot ID : {snapshot['snapshot_id']}",
        f"Committed At : {snapshot['committed_at']}",
        f"As-of Date : {snapshot['committed_at'][:10]}"
    ])

    return "\n".join(lines)

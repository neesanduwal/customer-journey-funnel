from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_customer_summary(question: str = ""):
    snapshot = get_snapshot("local.gold.gold_customer_funnel")

    rows = spark.sql("""
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
        LIMIT 10
    """).collect()

    if not rows:
        return "No customer data found."

    lines = ["Customer Funnel Summary", "", "Top Customers", ""]

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

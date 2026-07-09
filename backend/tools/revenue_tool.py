from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_revenue(date):

    row = spark.sql(f"""
        SELECT
            full_date,
            revenue
        FROM local.gold.gold_daily_funnel
        WHERE full_date = DATE('{date}')
        LIMIT 1
    """).first()

    if row is None:
        return f"No revenue found for {date}"

    snapshot = get_snapshot("local.gold.gold_daily_funnel")

    return f"""
Date : {row['full_date']}

Revenue : ${row['revenue']:,.2f}

Source Table : local.gold.gold_daily_funnel

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_wow():

    row = spark.sql("""
        SELECT
            full_date,
            revenue,
            last_week,
            wow_difference
        FROM local.gold.gold_week_over_week
        ORDER BY full_date DESC
        LIMIT 1
    """).first()

    snapshot = get_snapshot("local.gold.gold_week_over_week")

    return f"""
Latest Date : {row['full_date']}

Revenue : {row['revenue']}

Last Week : {row['last_week']}

WoW Difference : {row['wow_difference']}

Source Table : local.gold.gold_week_over_week

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
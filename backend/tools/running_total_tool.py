from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_running_total():

    row = spark.sql("""
        SELECT running_revenue
        FROM local.gold.gold_running_total
        ORDER BY full_date DESC
        LIMIT 1
    """).first()

    snapshot = get_snapshot("local.gold.gold_running_total")

    return f"""
Running Revenue : {row['running_revenue']}

Source Table : local.gold.gold_running_total

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
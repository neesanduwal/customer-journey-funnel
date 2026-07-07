from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_yoy():

    row = spark.sql("""
        SELECT
            full_date,
            revenue,
            last_year,
            yoy_difference
        FROM local.gold.gold_year_over_year
        ORDER BY full_date DESC
        LIMIT 1
    """).first()

    snapshot = get_snapshot("local.gold.gold_year_over_year")

    return f"""
Latest Date : {row['full_date']}

Revenue : {row['revenue']}

Last Year : {row['last_year']}

YoY Difference : {row['yoy_difference']}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
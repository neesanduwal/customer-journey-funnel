from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_yoy(date):

    row = spark.sql(f"""
        SELECT
            full_date,
            revenue,
            last_year,
            yoy_difference
        FROM local.gold.gold_year_over_year
        WHERE full_date = DATE('{date}')
        LIMIT 1
    """).first()

    if row is None:
        return f"No Year-over-Year data found for {date}"

    revenue = row["revenue"] or 0
    last_year = row["last_year"] or 0
    yoy_difference = row["yoy_difference"] or 0

    snapshot = get_snapshot("local.gold.gold_year_over_year")

    return f"""
Date : {row['full_date']}

Revenue : ${revenue:,.2f}

Last Year Revenue : ${last_year:,.2f}

YoY Difference : ${yoy_difference:,.2f}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
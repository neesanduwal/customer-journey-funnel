from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_wow(date):

    row = spark.sql(f"""
        SELECT *
        FROM local.gold.gold_week_over_week
        WHERE WEEKOFYEAR(full_date)=WEEKOFYEAR(DATE('{date}'))
        AND YEAR(full_date)=YEAR(DATE('{date}'))
        LIMIT 1
    """).first()

    if row is None:
        return f"No Week-over-Week data found for {date}"

    snapshot = get_snapshot("local.gold.gold_week_over_week")

    return f"""
Week Starting : {row['full_date']}

Revenue : ${row['revenue']:,.2f}

Same Week Last Year : ${row['last_year']:,.2f}

Difference : ${row['wow_difference']:,.2f}

Source Table : local.gold.gold_week_over_week

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
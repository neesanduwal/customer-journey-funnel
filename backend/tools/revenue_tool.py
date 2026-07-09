import re

from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_revenue(question: str):

    snapshot = get_snapshot("local.gold.gold_daily_funnel")

    dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)
    years = re.findall(r"\b20\d{2}\b", question)

    # ============================================
    # Revenue for an entire year
    # ============================================

    if len(years) == 1 and len(dates) == 0:

        year = years[0]

        row = spark.sql(f"""
        SELECT
            SUM(revenue) AS revenue
        FROM local.gold.gold_daily_funnel
        WHERE YEAR(full_date) = {year}
        """).first()

        if row is None or row["revenue"] is None:
            return f"No revenue found for {year}"

        return f"""
Revenue Summary

Year : {year}

Total Revenue : ${row['revenue']:,.2f}

Source Table : local.gold.gold_daily_funnel

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

    # ============================================
    # Revenue for a single date
    # ============================================

    if len(dates) == 1:

        date = dates[0]

        row = spark.sql(f"""
        SELECT
            full_date,
            revenue
        FROM local.gold.gold_daily_funnel
        WHERE full_date = DATE('{date}')
        """).first()

        if row is None:
            return f"No revenue found for {date}"

        return f"""
Date : {row['full_date']}

Revenue : ${row['revenue']:,.2f}

Source Table : local.gold.gold_daily_funnel

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

    return "Please provide a date (YYYY-MM-DD) or a year."
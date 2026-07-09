import re

from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_yoy(question: str):

    snapshot = get_snapshot("local.gold.gold_year_over_year")

    dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)
    years = re.findall(r"\b20\d{2}\b", question)

    # ==========================================================
    # Compare Two Years
    # ==========================================================

    if len(years) >= 2:

        year1 = years[0]
        year2 = years[1]

        row1 = spark.sql(f"""
        SELECT
            SUM(revenue) AS revenue,
            SUM(last_year) AS last_year,
            SUM(yoy_difference) AS yoy_difference
        FROM local.gold.gold_year_over_year
        WHERE YEAR(full_date) = {year1}
        """).first()

        row2 = spark.sql(f"""
        SELECT
            SUM(revenue) AS revenue,
            SUM(last_year) AS last_year,
            SUM(yoy_difference) AS yoy_difference
        FROM local.gold.gold_year_over_year
        WHERE YEAR(full_date) = {year2}
        """).first()

        return f"""
YoY Comparison

Year : {year1}

Revenue : ${row1['revenue']:,.2f}

Last Year Revenue : ${row1['last_year']:,.2f}

YoY Difference : ${row1['yoy_difference']:,.2f}

----------------------------------------

Year : {year2}

Revenue : ${row2['revenue']:,.2f}

Last Year Revenue : ${row2['last_year']:,.2f}

YoY Difference : ${row2['yoy_difference']:,.2f}

----------------------------------------

Revenue Difference

${row1['revenue']-row2['revenue']:,.2f}

YoY Difference Gap

${row1['yoy_difference']-row2['yoy_difference']:,.2f}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

    # ==========================================================
    # Compare Two Dates
    # ==========================================================

    if len(dates) >= 2:

        d1 = dates[0]
        d2 = dates[1]

        row1 = spark.sql(f"""
        SELECT *
        FROM local.gold.gold_year_over_year
        WHERE full_date=DATE('{d1}')
        """).first()

        row2 = spark.sql(f"""
        SELECT *
        FROM local.gold.gold_year_over_year
        WHERE full_date=DATE('{d2}')
        """).first()

        if row1 is None or row2 is None:
            return "One or both dates were not found."

        return f"""
YoY Comparison

Date : {row1['full_date']}

Revenue : ${row1['revenue']:,.2f}

Last Year Revenue : ${row1['last_year']:,.2f}

YoY Difference : ${row1['yoy_difference']:,.2f}

----------------------------------------

Date : {row2['full_date']}

Revenue : ${row2['revenue']:,.2f}

Last Year Revenue : ${row2['last_year']:,.2f}

YoY Difference : ${row2['yoy_difference']:,.2f}

----------------------------------------

Revenue Difference

${row1['revenue']-row2['revenue']:,.2f}

YoY Difference Gap

${row1['yoy_difference']-row2['yoy_difference']:,.2f}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

    # ==========================================================
    # Single Date
    # ==========================================================

    if len(dates) == 1:

        date = dates[0]

        row = spark.sql(f"""
        SELECT *
        FROM local.gold.gold_year_over_year
        WHERE full_date=DATE('{date}')
        """).first()

        if row is None:
            return f"No YoY data found for {date}"

        return f"""
Date : {row['full_date']}

Revenue : ${row['revenue']:,.2f}

Last Year Revenue : ${row['last_year']:,.2f}

YoY Difference : ${row['yoy_difference']:,.2f}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

    return "Please provide one date (YYYY-MM-DD), two dates, or two years."
import re
from datetime import datetime, timedelta

from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def _get_week_range(reference_date: str):
    dt = datetime.strptime(reference_date, "%Y-%m-%d")
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def get_yoy(question: str):

    snapshot = get_snapshot("local.gold.gold_year_over_year")

    dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)
    years = re.findall(r"\b20\d{2}\b", question)
    q = question.lower()

    if "this week" in q or "same week" in q or "lead funnel" in q:
        reference_date = dates[0] if dates else "2024-01-15"
        week_start, week_end = _get_week_range(reference_date)
        last_year_start = (datetime.strptime(reference_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
        last_year_end = (datetime.strptime(last_year_start, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")

        current_week = spark.sql(f"""
            SELECT
                SUM(leads) AS leads,
                SUM(orders) AS orders,
                SUM(revenue) AS revenue
            FROM local.gold.gold_daily_funnel
            WHERE full_date BETWEEN DATE('{week_start}') AND DATE('{week_end}')
        """).first()

        previous_week = spark.sql(f"""
            SELECT
                SUM(leads) AS leads,
                SUM(orders) AS orders,
                SUM(revenue) AS revenue
            FROM local.gold.gold_daily_funnel
            WHERE full_date BETWEEN DATE('{last_year_start}') AND DATE('{last_year_end}')
        """).first()

        current_leads = float(current_week["leads"] or 0)
        prior_leads = float(previous_week["leads"] or 0)
        current_orders = float(current_week["orders"] or 0)
        prior_orders = float(previous_week["orders"] or 0)
        current_revenue = float(current_week["revenue"] or 0)
        prior_revenue = float(previous_week["revenue"] or 0)

        return f"""
YoY Weekly Funnel Comparison

Date Range : {week_start} to {week_end}
Previous-Year Range : {last_year_start} to {last_year_end}

Leads
Current Week : {current_leads:,.0f}
Last Year Same Week : {prior_leads:,.0f}
YoY Difference : {current_leads - prior_leads:,.0f}

Orders
Current Week : {current_orders:,.0f}
Last Year Same Week : {prior_orders:,.0f}
YoY Difference : {current_orders - prior_orders:,.0f}

Revenue
Current Week : ${current_revenue:,.2f}
Last Year Same Week : ${prior_revenue:,.2f}
YoY Difference : ${current_revenue - prior_revenue:,.2f}

Source Table : local.gold.gold_daily_funnel
Snapshot ID : {snapshot['snapshot_id']}
Committed At : {snapshot['committed_at']}
As-of Date : {snapshot['committed_at'][:10]}
"""

    # ==========================================================
    # Compare a Single Year to Its Previous Year
    # ==========================================================

    if len(years) == 1:

        target_year = years[0]

        row = spark.sql(f"""
        SELECT
            SUM(revenue) AS revenue,
            SUM(last_year) AS last_year,
            SUM(yoy_difference) AS yoy_difference
        FROM local.gold.gold_year_over_year
        WHERE YEAR(full_date) = {target_year}
        """).first()

        if row is None or (row['revenue'] is None and row['last_year'] is None and row['yoy_difference'] is None):
            return f"No YoY data found for {target_year}"

        return f"""
YoY Comparison

Year : {target_year}

Current Year Revenue : ${row['revenue']:,.2f}

Previous Year Revenue : ${row['last_year']:,.2f}

YoY Change : ${row['yoy_difference']:,.2f}

Source Table : local.gold.gold_year_over_year

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""

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
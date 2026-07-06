from src.config.spark_session import create_spark_session

spark = create_spark_session()


def total_revenue():

    revenue = spark.sql("""
        SELECT SUM(revenue) AS revenue
        FROM local.gold.gold_daily_funnel
    """).collect()[0]["revenue"]

    snapshot = spark.sql("""
        SELECT MAX(full_date) AS snapshot
        FROM local.gold.gold_daily_funnel
    """).collect()[0]["snapshot"]

    return revenue, snapshot


def running_total():

    row = spark.sql("""
        SELECT
            full_date,
            running_revenue
        FROM local.gold.gold_running_total
        ORDER BY full_date DESC
        LIMIT 1
    """).collect()[0]

    return row["running_revenue"], row["full_date"]


def wow():

    row = spark.sql("""
        SELECT
            full_date,
            revenue,
            last_week,
            wow_difference
        FROM local.gold.gold_week_over_week
        ORDER BY full_date DESC
        LIMIT 1
    """).collect()[0]

    return row


def yoy():

    row = spark.sql("""
        SELECT
            full_date,
            revenue,
            last_year,
            yoy_difference
        FROM local.gold.gold_year_over_year
        ORDER BY full_date DESC
        LIMIT 1
    """).collect()[0]

    return row
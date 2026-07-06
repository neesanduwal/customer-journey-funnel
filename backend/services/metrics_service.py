from src.config.spark_session import create_spark_session

spark = create_spark_session()


def total_revenue():
    df = spark.sql("""
        SELECT SUM(revenue) revenue
        FROM local.gold.gold_daily_funnel
    """)
    return df.collect()[0]["revenue"]


def running_total():
    return spark.sql("""
        SELECT *
        FROM local.gold.gold_running_total
        ORDER BY full_date DESC
        LIMIT 10
    """).toPandas()


def wow():
    return spark.sql("""
        SELECT *
        FROM local.gold.gold_week_over_week
        ORDER BY full_date DESC
        LIMIT 10
    """).toPandas()


def yoy():
    return spark.sql("""
        SELECT *
        FROM local.gold.gold_year_over_year
        ORDER BY full_date DESC
        LIMIT 10
    """).toPandas()


def snapshot():

    return spark.sql("""
        SELECT MAX(full_date) snapshot
        FROM local.gold.gold_daily_funnel
    """).collect()[0]["snapshot"]
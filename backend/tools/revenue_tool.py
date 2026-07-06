from backend.services.metrics_service import spark


def get_total_revenue():

    revenue = spark.sql("""

    SELECT
        SUM(total_revenue) AS revenue
    FROM local.gold.gold_customer_funnel

    """).collect()[0]["revenue"]

    snapshot = spark.sql("""

    SELECT MAX(full_date) AS snapshot
    FROM local.gold.gold_daily_funnel

    """).collect()[0]["snapshot"]

    return {
        "metric": "Revenue",
        "value": float(revenue),
        "snapshot": str(snapshot)
    }
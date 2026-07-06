from backend.services.metrics_service import spark


def get_total_orders():

    orders = spark.sql("""

    SELECT
        SUM(total_orders) AS orders
    FROM local.gold.gold_customer_funnel

    """).collect()[0]["orders"]

    snapshot = spark.sql("""

    SELECT MAX(full_date)
    FROM local.gold.gold_daily_funnel

    """).collect()[0][0]

    return {
        "metric": "Orders",
        "value": int(orders),
        "snapshot": str(snapshot)
    }
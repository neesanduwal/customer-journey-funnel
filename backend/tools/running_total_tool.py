from backend.services.metrics_service import spark


def get_running_total():

    row = spark.sql("""

    SELECT
        full_date,
        running_revenue
    FROM local.gold.gold_running_total
    ORDER BY full_date DESC
    LIMIT 1

    """).collect()[0]

    return {
        "metric": "Running Revenue",
        "value": float(row["running_revenue"]),
        "snapshot": str(row["full_date"])
    }
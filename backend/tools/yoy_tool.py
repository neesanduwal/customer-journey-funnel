from backend.services.metrics_service import spark


def get_yoy():

    row = spark.sql("""

    SELECT *
    FROM local.gold.gold_year_over_year
    ORDER BY full_date DESC
    LIMIT 1

    """).collect()[0]

    return {
        "metric": "Year over Year",
        "value": float(row["yoy_difference"]),
        "snapshot": str(row["full_date"])
    }
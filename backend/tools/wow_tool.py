from backend.services.metrics_service import spark


def get_wow():

    row = spark.sql("""

    SELECT *
    FROM local.gold.gold_week_over_week
    ORDER BY full_date DESC
    LIMIT 1

    """).collect()[0]

    return {
        "metric": "Week over Week",
        "value": float(row["wow_difference"]),
        "snapshot": str(row["full_date"])
    }

print("Starting WoW query")

row = spark.sql("""
...
""").collect()[0]

print("Finished WoW query")
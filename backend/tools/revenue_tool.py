from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_revenue():

    revenue = spark.sql("""
        SELECT SUM(revenue) AS revenue
        FROM local.gold.fact_orders
    """).first()["revenue"]

    snapshot = get_snapshot("local.gold.fact_orders")

    return f"""
Total Revenue : ${revenue:,.2f}

Source Table : local.gold.fact_orders

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
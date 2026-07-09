from src.config.spark_session import create_spark_session
from backend.tools.snapshot_tool import get_snapshot

spark = create_spark_session()


def get_orders(where_clause=""):

    query = f"""
        SELECT COUNT(*) AS orders
        FROM local.gold.fact_orders
        {where_clause}
    """

    orders = spark.sql(query).first()["orders"]

    snapshot = get_snapshot("local.gold.fact_orders")

    return f"""
Total Orders : {orders}

Source Table : local.gold.fact_orders

Snapshot ID : {snapshot["snapshot_id"]}

Committed At : {snapshot["committed_at"]}

As-of Date : {snapshot["committed_at"][:10]}
"""
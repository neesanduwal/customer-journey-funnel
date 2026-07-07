from src.config.spark_session import create_spark_session

spark = create_spark_session()


def get_snapshot(table_name: str):

    row = spark.sql(f"""
        SELECT
            snapshot_id,
            committed_at
        FROM {table_name}.snapshots
        ORDER BY committed_at DESC
        LIMIT 1
    """).first()

    return {
        "snapshot_id": row.snapshot_id,
        "committed_at": str(row.committed_at)
    }
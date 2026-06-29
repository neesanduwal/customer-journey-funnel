from pathlib import Path

from src.config.spark_session import create_spark_session
from src.config.postgres import DB_CONFIG

spark = create_spark_session()

tables = [
    "dim_customer",
    "dim_channel",
    "dim_product",
    "dim_date",
    "fact_web_events",
    "fact_lead_events",
    "fact_orders"
]

bronze_path = Path("data/bronze")

for table in tables:

    print(f"Loading {table}...")

    df = (
        spark.read
        .format("jdbc")
        .option("url", DB_CONFIG["url"])
        .option("dbtable", table)
        .option("user", DB_CONFIG["user"])
        .option("password", DB_CONFIG["password"])
        .option("driver", DB_CONFIG["driver"])
        .load()
    )

    df.write \
        .mode("overwrite") \
        .parquet(str(bronze_path / table))

    print(f"Saved {table}")

spark.stop()
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

# Create Bronze namespace if it doesn't exist
spark.sql("CREATE NAMESPACE IF NOT EXISTS local.bronze")

for table in tables:
    print(f"\nLoading {table} from PostgreSQL...")

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

    print(f"Rows: {df.count()}")

    # Write as Iceberg table
    (
        df.writeTo(f"local.bronze.{table}")
        .using("iceberg")
        .createOrReplace()
    )

    print(f"✓ Created Iceberg table: local.bronze.{table}")

print("\n==============================")
print("BRONZE LAYER CREATED")
print("==============================")

spark.stop()
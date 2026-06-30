from src.config.spark_session import create_spark_session
from pyspark.sql.functions import col, trim

spark = create_spark_session()

# Create Silver namespace if it doesn't exist
spark.sql("CREATE NAMESPACE IF NOT EXISTS local.silver")

TABLES = [
    "dim_customer",
    "dim_channel",
    "dim_product",
    "dim_date",
    "fact_web_events",
    "fact_lead_events",
    "fact_orders"
]

for table in TABLES:
    print(f"\nLoading {table} from Bronze Iceberg...")

    # Read from Bronze Iceberg
    df = spark.table(f"local.bronze.{table}")

    # Remove duplicate rows
    df = df.dropDuplicates()

    # ---------- Table-specific cleaning ----------
    if table == "dim_customer":
        df = (
            df.withColumn("customer_name", trim(col("customer_name")))
              .withColumn("segment", trim(col("segment")))
              .withColumn("region", trim(col("region")))
        )

    elif table == "dim_channel":
        df = (
            df.withColumn("channel_name", trim(col("channel_name")))
              .withColumn("channel_category", trim(col("channel_category")))
        )

    elif table == "dim_product":
        df = (
            df.withColumn("product_name", trim(col("product_name")))
              .withColumn("category", trim(col("category")))
              .filter(col("unit_price") > 0)
        )

    elif table == "fact_web_events":
        df = df.dropna(subset=["customer_key", "date_key"])

    elif table == "fact_lead_events":
        df = df.dropna(subset=["customer_key", "date_key"])

    elif table == "fact_orders":
        df = (
            df.dropna(subset=["customer_key", "product_key"])
              .filter(col("revenue") > 0)
        )

    # Write to Silver Iceberg
    (
        df.writeTo(f"local.silver.{table}")
        .using("iceberg")
        .createOrReplace()
    )

    print(f"✓ Created Iceberg table: local.silver.{table}")

print("\n==============================")
print("SILVER LAYER CREATED")
print("==============================")

spark.stop()
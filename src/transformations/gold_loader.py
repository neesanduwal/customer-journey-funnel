from src.config.spark_session import create_spark_session

spark = create_spark_session()

print("=" * 60)
print("CREATING GOLD STAR SCHEMA")
print("=" * 60)

# -------------------------------------------------------
# Create Gold Namespace
# -------------------------------------------------------

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.gold")

# -------------------------------------------------------
# STAR SCHEMA TABLES
# -------------------------------------------------------

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

    print(f"\nCreating Gold table: {table}")

    df = spark.table(f"local.silver.{table}")

    (
        df.writeTo(f"local.gold.{table}")
        .using("iceberg")
        .createOrReplace()
    )

    print(f"✓ local.gold.{table} created")

print("\n" + "=" * 60)
print("GOLD STAR SCHEMA CREATED")
print("=" * 60)

# -------------------------------------------------------
# OPTIONAL REPORTING TABLE
# Daily Funnel Summary
# -------------------------------------------------------

from pyspark.sql.functions import countDistinct, sum

print("\nCreating reporting mart: gold_daily_funnel")

dates = spark.table("local.gold.dim_date")
web = spark.table("local.gold.fact_web_events")
leads = spark.table("local.gold.fact_lead_events")
orders = spark.table("local.gold.fact_orders")

daily_web = (
    web.groupBy("date_key")
    .agg(
        countDistinct("session_id").alias("sessions")
    )
)

daily_leads = (
    leads.groupBy("date_key")
    .agg(
        countDistinct("lead_id").alias("leads")
    )
)

daily_orders = (
    orders.groupBy("date_key")
    .agg(
        countDistinct("order_id").alias("orders"),
        sum("revenue").alias("revenue")
    )
)

gold_daily = (
    dates
    .join(daily_web, "date_key", "left")
    .join(daily_leads, "date_key", "left")
    .join(daily_orders, "date_key", "left")
    .fillna({
        "sessions": 0,
        "leads": 0,
        "orders": 0,
        "revenue": 0
    })
)

(
    gold_daily.writeTo("local.gold.gold_daily_funnel")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_daily_funnel created")

print("\n" + "=" * 60)
print("GOLD LAYER COMPLETE")
print("=" * 60)

spark.stop()
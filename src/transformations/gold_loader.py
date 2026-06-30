from src.config.spark_session import create_spark_session
from pyspark.sql.functions import countDistinct, sum, coalesce, lit

spark = create_spark_session()

# ============================================================
# Create Gold Namespace
# ============================================================

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.gold")

print("Reading Silver Iceberg tables...")

customers = spark.table("local.silver.dim_customer")
channels = spark.table("local.silver.dim_channel")
products = spark.table("local.silver.dim_product")
dates = spark.table("local.silver.dim_date")

web = spark.table("local.silver.fact_web_events")
leads = spark.table("local.silver.fact_lead_events")
orders = spark.table("local.silver.fact_orders")

print("Silver tables loaded.")

# ============================================================
# CUSTOMER AGGREGATES
# ============================================================

web_customer = (
    web.groupBy("customer_key")
    .agg(
        countDistinct("session_id").alias("website_sessions")
    )
)

lead_customer = (
    leads.groupBy("customer_key")
    .agg(
        countDistinct("lead_id").alias("total_leads")
    )
)

order_customer = (
    orders.groupBy("customer_key")
    .agg(
        countDistinct("order_id").alias("total_orders"),
        sum("revenue").alias("total_revenue")
    )
)

# ============================================================
# GOLD 1 - CUSTOMER FUNNEL
# ============================================================

print("\nCreating gold_customer_funnel...")

gold_customer_funnel = (
    customers
    .join(web_customer, "customer_key", "left")
    .join(lead_customer, "customer_key", "left")
    .join(order_customer, "customer_key", "left")
    .fillna({
        "website_sessions": 0,
        "total_leads": 0,
        "total_orders": 0,
        "total_revenue": 0
    })
)

(
    gold_customer_funnel.writeTo("local.gold.gold_customer_funnel")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_customer_funnel created")

# ============================================================
# CHANNEL AGGREGATES
# ============================================================

web_channel = (
    web.groupBy("channel_key")
    .agg(
        countDistinct("session_id").alias("sessions")
    )
)

lead_channel = (
    leads.groupBy("channel_key")
    .agg(
        countDistinct("lead_id").alias("leads")
    )
)

order_channel = (
    orders.groupBy("channel_key")
    .agg(
        countDistinct("order_id").alias("orders"),
        sum("revenue").alias("revenue")
    )
)

# ============================================================
# GOLD 2 - CHANNEL PERFORMANCE
# ============================================================

print("\nCreating gold_channel_performance...")

gold_channel_performance = (
    channels
    .join(web_channel, "channel_key", "left")
    .join(lead_channel, "channel_key", "left")
    .join(order_channel, "channel_key", "left")
    .fillna({
        "sessions": 0,
        "leads": 0,
        "orders": 0,
        "revenue": 0
    })
)

(
    gold_channel_performance.writeTo("local.gold.gold_channel_performance")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_channel_performance created")

# ============================================================
# GOLD 3 - PRODUCT SALES
# ============================================================

print("\nCreating gold_product_sales...")

gold_product_sales = (
    orders
    .join(products, "product_key")
    .groupBy(
        "product_key",
        "product_name",
        "category"
    )
    .agg(
        sum("quantity").alias("units_sold"),
        countDistinct("order_id").alias("orders"),
        sum("revenue").alias("revenue")
    )
)

(
    gold_product_sales.writeTo("local.gold.gold_product_sales")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_product_sales created")

# ============================================================
# DAILY AGGREGATES
# ============================================================

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

# ============================================================
# GOLD 4 - DAILY FUNNEL
# ============================================================

print("\nCreating gold_daily_funnel...")

gold_daily_funnel = (
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
    gold_daily_funnel.writeTo("local.gold.gold_daily_funnel")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_daily_funnel created")

print("\n==============================")
print("ALL GOLD TABLES CREATED")
print("==============================")

spark.stop()
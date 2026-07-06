"""
Bronze loader with daily partitioning — Project 3 Core Requirement:
"Load into Iceberg with daily partitioning"

Writes fact tables year-by-year to avoid OOM on 8GB machines.
Each year is a small manageable Iceberg append (~8k rows/year).

Run:
    python -m src.ingestion.bronze_loader
"""

from pyspark.sql.functions import days, to_date, col, year as spark_year
from src.config.spark_session import create_spark_session
from src.config.postgres import DB_CONFIG

spark = create_spark_session()

print("=" * 60)
print("BRONZE LOADER — WITH DAILY PARTITIONING")
print("=" * 60)

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.bronze")

# ------------------------------------------------------------------
# DIMENSION TABLES — unpartitioned
# ------------------------------------------------------------------
DIM_TABLES = ["dim_customer", "dim_channel", "dim_product", "dim_date"]

for table in DIM_TABLES:
    print(f"\nLoading dimension: {table}...")
    df = (
        spark.read.format("jdbc")
        .option("url",      DB_CONFIG["url"])
        .option("dbtable",  table)
        .option("user",     DB_CONFIG["user"])
        .option("password", DB_CONFIG["password"])
        .option("driver",   DB_CONFIG["driver"])
        .load()
    )
    print(f"  Rows from Postgres: {df.count()}")
    (
        df.writeTo(f"local.bronze.{table}")
        .using("iceberg")
        .createOrReplace()
    )
    print(f"  ✓ local.bronze.{table} created (unpartitioned)")

# ------------------------------------------------------------------
# FACT TABLES — partitioned by days(event_date), loaded year by year
#
# Writing all years at once OOMs on 8GB — even with fanout disabled
# and data sorted, 65k rows across 2920 daily partitions is too much.
# Writing one year at a time keeps each commit to ~8k rows across
# ~365 partitions, which fits comfortably in 3GB heap.
# First year: createOrReplace (creates the table with partition spec)
# Subsequent years: append (adds to existing partitioned table)
# ------------------------------------------------------------------
FACT_TABLES = ["fact_web_events", "fact_lead_events", "fact_orders"]
YEARS = list(range(2018, 2026))  # 2018-2025 inclusive

for table in FACT_TABLES:
    print(f"\nLoading fact table: {table} (year-by-year, partitioned by days(event_date))...")

    # Read full table once — filter in memory per year
    # (avoids 8 separate JDBC connections to Postgres)
    print(f"  Reading full table from Postgres...")
    df_full = (
        spark.read.format("jdbc")
        .option("url",      DB_CONFIG["url"])
        .option("dbtable",  table)
        .option("user",     DB_CONFIG["user"])
        .option("password", DB_CONFIG["password"])
        .option("driver",   DB_CONFIG["driver"])
        .load()
    )

    # Derive real DATE column from integer date_key
    df_full = df_full.withColumn(
        "event_date",
        to_date(col("date_key").cast("string"), "yyyyMMdd")
    )

    total_rows = df_full.count()
    print(f"  Total rows: {total_rows}")

    # Drop existing table so we can recreate with partition spec
    spark.sql(f"DROP TABLE IF EXISTS local.bronze.{table}")

    first_year = True
    for yr in YEARS:
        df_year = df_full.filter(spark_year(col("event_date")) == yr)
        yr_count = df_year.count()

        if yr_count == 0:
            print(f"  Year {yr}: no data, skipping")
            continue

        # Sort within year so partition writer opens dates sequentially
        df_year = df_year.sortWithinPartitions("event_date")

        if first_year:
            (
                df_year.writeTo(f"local.bronze.{table}")
                .using("iceberg")
                .partitionedBy(days("event_date"))
                .create()
            )
            first_year = False
        else:
            (
                df_year.writeTo(f"local.bronze.{table}")
                .using("iceberg")
                .append()
            )

        print(f"  Year {yr}: {yr_count} rows written")

    print(f"  ✓ local.bronze.{table} complete (partitioned by days(event_date))")

print("\n" + "=" * 60)
print("BRONZE LAYER WITH DAILY PARTITIONING COMPLETE")
print("=" * 60)

spark.stop()
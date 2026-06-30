from src.config.spark_session import create_spark_session

spark = create_spark_session()

# ==========================================================
# RUNNING TOTAL
# ==========================================================

print("Creating gold_running_total...")

running_total = spark.sql("""

SELECT
    full_date,

    COALESCE(revenue,0) AS revenue,

    SUM(COALESCE(revenue,0))
    OVER(
        ORDER BY full_date
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS running_revenue

FROM local.gold.gold_daily_funnel

ORDER BY full_date

""")

(
    running_total.writeTo("local.gold.gold_running_total")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_running_total created")

# ==========================================================
# WEEK OVER WEEK
# ==========================================================

print("\nCreating gold_week_over_week...")

wow = spark.sql("""

SELECT

    full_date,

    COALESCE(revenue,0) AS revenue,

    LAG(COALESCE(revenue,0),7)
    OVER(
        ORDER BY full_date
    ) AS last_week,

    COALESCE(revenue,0) -
    LAG(COALESCE(revenue,0),7)
    OVER(
        ORDER BY full_date
    ) AS wow_difference

FROM local.gold.gold_daily_funnel

ORDER BY full_date

""")

(
    wow.writeTo("local.gold.gold_week_over_week")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_week_over_week created")

# ==========================================================
# YEAR OVER YEAR
# ==========================================================

print("\nCreating gold_year_over_year...")

yoy = spark.sql("""

SELECT

    full_date,

    COALESCE(revenue,0) AS revenue,

    LAG(COALESCE(revenue,0),365)
    OVER(
        ORDER BY full_date
    ) AS last_year,

    COALESCE(revenue,0) -
    LAG(COALESCE(revenue,0),365)
    OVER(
        ORDER BY full_date
    ) AS yoy_difference

FROM local.gold.gold_daily_funnel

ORDER BY full_date

""")

(
    yoy.writeTo("local.gold.gold_year_over_year")
    .using("iceberg")
    .createOrReplace()
)

print("✓ gold_year_over_year created")

# ==========================================================
# VERIFY TABLES
# ==========================================================

print("\n========== ROW COUNTS ==========")

spark.sql("SELECT COUNT(*) FROM local.gold.gold_running_total").show()

spark.sql("SELECT COUNT(*) FROM local.gold.gold_week_over_week").show()

spark.sql("SELECT COUNT(*) FROM local.gold.gold_year_over_year").show()

print("\n========== SAMPLE DATA ==========")

spark.sql("""
SELECT *
FROM local.gold.gold_running_total
LIMIT 10
""").show(truncate=False)

spark.sql("""
SELECT *
FROM local.gold.gold_week_over_week
LIMIT 10
""").show(truncate=False)

spark.sql("""
SELECT *
FROM local.gold.gold_year_over_year
LIMIT 10
""").show(truncate=False)

print("\n===================================")
print("ALL METRIC TABLES CREATED")
print("===================================")

spark.stop()
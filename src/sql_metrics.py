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

# ==========================================================
# WEEK OVER WEEK (Same Week Last Year)
# ==========================================================

print("\nCreating gold_week_over_week...")

wow = spark.sql("""

WITH weekly_sales AS (

SELECT

    YEAR(full_date) AS sales_year,

    WEEKOFYEAR(full_date) AS week_no,

    MIN(full_date) AS week_start,

    SUM(revenue) AS revenue

FROM local.gold.gold_daily_funnel

GROUP BY
    YEAR(full_date),
    WEEKOFYEAR(full_date)

)

SELECT

    curr.week_start AS full_date,

    curr.revenue,

    COALESCE(prev.revenue,0) AS last_year,

    curr.revenue - COALESCE(prev.revenue,0) AS wow_difference

FROM weekly_sales curr

LEFT JOIN weekly_sales prev

ON curr.week_no = prev.week_no
AND curr.sales_year = prev.sales_year + 1

ORDER BY curr.week_start

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

WITH daily AS (

    SELECT
        full_date,
        COALESCE(revenue,0) AS revenue
    FROM local.gold.gold_daily_funnel

)

SELECT

    cur.full_date,

    cur.revenue,

    COALESCE(prev.revenue,0) AS last_year,

    cur.revenue - COALESCE(prev.revenue,0) AS yoy_difference

FROM daily cur

LEFT JOIN daily prev
ON prev.full_date = ADD_MONTHS(cur.full_date,-12)

ORDER BY cur.full_date

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
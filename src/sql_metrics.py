from src.config.spark_session import create_spark_session

spark = create_spark_session()

# ==========================================================
# RUNNING TOTAL
# ==========================================================

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

print("\n========== RUNNING TOTAL ==========")

running_total.filter("revenue > 0").show(100, False)

# ==========================================================
# WEEK OVER WEEK
# ==========================================================

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

print("\n========== WEEK OVER WEEK ==========")

wow.filter("revenue > 0").show(100, False)

# ==========================================================
# YEAR OVER YEAR
# ==========================================================

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

print("\n========== YEAR OVER YEAR ==========")

yoy.filter("revenue > 0").show(100, False)

spark.stop()
from src.config.spark_session import create_spark_session

spark = create_spark_session()

spark.sql("""
SELECT
    event_date,
    SUM(revenue) AS revenue
FROM local.gold.fact_orders
WHERE event_date = DATE('2024-01-09')
GROUP BY event_date
""").show()

spark.stop()
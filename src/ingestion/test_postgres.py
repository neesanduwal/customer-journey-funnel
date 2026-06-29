from src.config.spark_session import create_spark_session
from src.config.postgres import DB_CONFIG

spark = create_spark_session()

df = (
    spark.read.format("jdbc")
    .option("url", DB_CONFIG["url"])
    .option("dbtable", "dim_customer")
    .option("user", DB_CONFIG["user"])
    .option("password", DB_CONFIG["password"])
    .option("driver", DB_CONFIG["driver"])
    .load()
)

df.show(5)
df.printSchema()

spark.stop()
from pyspark.sql import SparkSession


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("Customer Journey Funnel")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.7.3"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark
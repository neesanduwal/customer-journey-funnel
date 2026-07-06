from pyspark.sql import SparkSession


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("Customer Journey Funnel")
        .master("local[*]")

        # Memory tuning
        .config("spark.driver.memory", "3g")
        .config("spark.driver.maxResultSize", "1g")

        # JDK 17 JIT compiler workaround
        .config("spark.driver.extraJavaOptions", "-XX:-TieredCompilation")

        # Shuffle partitions
        .config("spark.sql.shuffle.partitions", "8")

        # Disable Iceberg fanout writer to prevent OOM on 8GB machines
        # (fanout opens one Parquet writer per partition simultaneously)
        .config("spark.sql.iceberg.fanout.enabled", "false")

        # PostgreSQL + Iceberg jars
        .config(
            "spark.jars.packages",
            ",".join([
                "org.postgresql:postgresql:42.7.3",
                "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2"
            ])
        )

        # Iceberg Catalog
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
        )
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local.type", "hadoop")
        .config("spark.sql.catalog.local.warehouse", "warehouse")

        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark
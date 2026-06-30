from pyspark.sql import SparkSession


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("Customer Journey Funnel")

        # Run Spark in single-thread mode
        .master("local[1]")

        # Memory
        .config("spark.driver.memory", "3g")
        .config("spark.driver.maxResultSize", "1g")

        # Reduce parallelism
        .config("spark.default.parallelism", "1")
        .config("spark.sql.shuffle.partitions", "1")

        # Disable adaptive execution
        .config("spark.sql.adaptive.enabled", "false")

        # Disable whole-stage code generation
        .config("spark.sql.codegen.wholeStage", "false")

        # Java options
        .config(
            "spark.driver.extraJavaOptions",
            "-XX:-TieredCompilation "
            "-XX:+UseSerialGC "
            "-Xss4m"
        )

        # JDBC + Iceberg
        .config(
            "spark.jars.packages",
            ",".join([
                "org.postgresql:postgresql:42.7.3",
                "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2"
            ])
        )

        # Iceberg
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
        )
        .config(
            "spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog"
        )
        .config(
            "spark.sql.catalog.local.type",
            "hadoop"
        )
        .config(
            "spark.sql.catalog.local.warehouse",
            "warehouse"
        )

        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark
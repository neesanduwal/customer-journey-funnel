from src.config.spark_session import create_spark_session


def main():
    spark = create_spark_session()

    print(f"Spark Version: {spark.version}")

    spark.range(10).show()

    spark.stop()


if __name__ == "__main__":
    main()
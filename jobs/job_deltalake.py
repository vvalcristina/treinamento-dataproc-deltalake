#!/usr/bin/python
# Author: Valeria Silva
# License: MIT

import pyspark

spark = pyspark.sql.SparkSession.builder.appName("JobIncremental") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.databricks.delta.schema.autoMerge.enabled","true") \
    .config("spark.databricks.delta.autoOptimize.optimizeWrite","true") \
    .config("spark.databricks.delta.optimizeWrite.enabled","true") \
    .config("spark.databricks.delta.vacuum.parallelDelete.enabled","true") \
    .getOrCreate()

from delta.tables import *
from pyspark.sql.functions import *

def main(spark):
    path_input = "gs://${BUCKET_CODE_NAME}/input/"
    path_output = "output/"
    df_input = spark.read.format("parquet").option("inferSchema", "false").load(path_input)
    df_input.write.format("delta").save(path_output)
    df_3= spark.createDataFrame(
    [
        (5, date.today(), 'Input dataframe'),

    ],
        ['id','data', 'texto']
    )
    df = spark.read.format("delta").load(path_output)
    df.show()
    table = DeltaTable.forPath(spark, path_output)
    table.toDF().show(truncate=False)
    table.alias("persisteddata") .merge( \
        df_3.alias("newdata"), \
            "persisteddata.id = newdata.id") \
            .whenMatchedUpdateAll() \
            .whenNotMatchedInsertAll() \
            .execute()
    table.toDF().show(truncate=False)

if __name__ == "__main__":
    main(spark)

import pyspark
import logging

spark = pyspark.sql.SparkSession.builder.appName("DeltaLake") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.databricks.delta.schema.autoMerge.enabled","true") \
    .config("spark.databricks.delta.autoOptimize.optimizeWrite","true") \
    .config("spark.databricks.delta.optimizeWrite.enabled","true") \
    .config("spark.databricks.delta.vacuum.parallelDelete.enabled","true") \
    .getOrCreate()

from delta import *
from pyspark.sql.functions import *

class JobIncremental(spark):

    def __init__(self):

        self.path_input = 'gs://{BUCKET_LAKE_NAME}/transient/sample.parquet/'
        self.path_output = 'gs://{BUCKET_LAKE_NAME}/raw/sample.parquet/'

    def table_exists(path_output: str) -> bool:
        return DeltaTable.isDeltaTable(spark, path_output)

    def get_incremental_load(self):
        df = spark.read.format("parquet").option("inferSchema", "false").load(self.path_input)
        if not self.table_exists(self.path_output):
            try:
                df.write.format("delta").mode("overwrite").save(self.path_output)
                df.show()
            except Exception as e:
                logging.error(f'unexpected error: {str(e)}')
        else:
            try:
                logging.info(f'Writing on path: {self.path_output}')
                deltaTable =DeltaTable.forPath(spark, self.path_output)
                (
                    deltaTable.alias("persisteddata").merge( \
                        df.alias("newdata"), \
                        "persisteddata.id = newdata.id") \
                        .whenMatchedUpdateAll() \
                        .whenNotMatchedInsertAll() \
                        .execute()
                 )
                deltaTable.vacuum()
                deltaTable.toDF().printSchema()
            except Exception as e:
                raise e

    def main(self):
        self.get_incremental_load()
        
if __name__ == "__main__":
    deltaLakeJob = JobIncremental()
    deltaLakeJob.main()

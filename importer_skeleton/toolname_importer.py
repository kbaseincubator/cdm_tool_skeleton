"""
Importer skeleton for CTS tool results.

Copy this file to kbase/cdm-spark-events-importers/cdmeventimporters/{toolname}.py
and fill in the TODOs.

NOTE: The importer is OPTIONAL. CTS jobs run and write output to MinIO without it.
The importer is only needed if you want results automatically loaded into Delta Lake
tables after each job completes.
"""

import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType  # TODO: add types as needed
from typing import Any

from cdmeventimporters import utilities


CTS_JOB_ID = "cts_job_id"

# TODO: Set to the filename suffix that identifies the output file(s) to import.
# Only files whose path ends with this suffix will be read.
_OUTPUT_FILE_SUFFIX = "results.tsv"

# TODO: Define the schema matching your tool's output columns.
# Always define explicitly — never let Spark infer.
# Always include CTS_JOB_ID as the last field.
SCHEMA = StructType([
    StructField("column1", StringType()),   # TODO: replace with real column names/types
    StructField("column2", StringType()),
    StructField(CTS_JOB_ID, StringType()),
])


def _ensure_table(spark: SparkSession, logr: logging.Logger, full_tablename: str):
    namespace = full_tablename.split(".")[0]
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {namespace}")
    if not spark.catalog.tableExists(full_tablename):
        logr.info(f"Creating new Delta table {full_tablename}")
        spark.createDataFrame([], SCHEMA).write.format("delta").option(
            "compression", "snappy"
        ).saveAsTable(full_tablename)


def run_import(get_spark, job_info: dict[str, Any], metadata: dict[str, Any]):
    """
    Import tool output files into a Delta Lake table.

    get_spark - call to get a SparkSession.
    job_info  - dict with keys: id, namespace_prefix, outputs (list of {file, crc64nvme}).
    metadata  - from the YAML file; must contain 'deltatable'.
    """
    logr = logging.getLogger(__name__)

    job_id = job_info["id"]
    output_files = [
        f["file"] for f in job_info["outputs"] if f["file"].endswith(_OUTPUT_FILE_SUFFIX)
    ]
    if not output_files:
        raise ValueError(f"No {_OUTPUT_FILE_SUFFIX} files found in job outputs")
    logr.info(f"Importing {len(output_files)} file(s) from CTS job {job_id}")

    deltaname = metadata.get("deltatable")
    if not deltaname:
        raise ValueError("Expected 'deltatable' key in importer metadata")
    deltaname = job_info["namespace_prefix"] + deltaname

    spark = get_spark()
    _ensure_table(spark, logr, deltaname)

    # TODO: Adjust read options to match your output file format.
    # Common options:
    #   option("header", True/False)  — does the file have a header row?
    #   option("sep", "\t")           — tab-separated (default is comma)
    df = spark.read.option("header", True).option("sep", "\t").csv(
        [f"s3a://{f}" for f in output_files]
    ).withColumn(CTS_JOB_ID, lit(job_id))

    df = df.select(*[col(f.name).cast(f.dataType).alias(f.name) for f in SCHEMA])

    # TODO: Set the merge condition to prevent duplicate rows.
    # Include cts_job_id in the key if results from different jobs should coexist.
    # Omit cts_job_id if a newer job should overwrite results from an older job.
    utilities.merge_spark_df_to_deltatable(
        spark,
        df,
        deltaname,
        "target.column1 == source.column1 AND target.cts_job_id == source.cts_job_id",
        update=False,
    )

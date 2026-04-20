# CTS Tool Pattern

Complete guide for adding a new bioinformatics tool to the KBERDL inner loop via CTS.

---

## Overview

Each tool consists of three artifacts:

```
1. GitHub repo (kbaseincubator/cdm_{tool})   ← Dockerfile + CI/CD
2. Demo notebook (hub.berdl.kbase.us)         ← Job submission + result exploration
3. Importer PR (kbase/cdm-spark-events-importers) ← Raw output → Delta Lake table
```

---

## Step 1: GitHub Repo — Container

Create `kbaseincubator/cdm_{toolname}`. Minimal structure:

```
cdm_{toolname}/
├── Dockerfile
├── .github/workflows/docker-publish.yaml   ← copy from cdm_tool_skeleton
├── README.md
└── LICENSE.md
```

### Dockerfile — Option A: Wrap existing public image

```dockerfile
FROM staphb/tool:version      # or soedinglab/..., ecogenomics/..., quay.io/biocontainers/...

ENV TOOL_DB /ref_data/db      # only if the tool needs a reference database

ENTRYPOINT ["tool-command"]   # bare command, no subcommand unless the tool has only one mode
```

### Dockerfile — Option B: Build from scratch

```dockerfile
FROM ubuntu:24.04 AS build
RUN apt-get update && apt-get install -y wget
RUN wget https://releases.example.com/tool-v1.0-linux-x86.tar.gz \
    && tar xzf tool-v1.0-linux-x86.tar.gz

FROM ubuntu:24.04
COPY --from=build /opt/tool /usr/local/bin/tool
ENTRYPOINT ["tool"]
```

### CTS container requirements checklist

- [ ] Publicly accessible without authentication
- [ ] Runs as non-root
- [ ] Has `/bin/bash`
- [ ] Defines `ENTRYPOINT`
- [ ] Writes ALL output to `output_mount_point` only (default `/out`)
- [ ] Does NOT download external files at runtime
- [ ] Does NOT hardlink between input and output directories

---

## Step 2: CI/CD — GitHub Actions

Copy `.github/workflows/docker-publish.yaml` from `cdm_tool_skeleton` unchanged.
It publishes to `ghcr.io/kbaseincubator/cdm_{toolname}` on every push to main and on semver tags.

**To trigger a versioned build:** `git tag 0.1.0 && git push origin 0.1.0`

**Getting the correct digest for Gavin:**
After the build succeeds, look in the GitHub Actions log under "Build and push Docker image" → `##[group]Digest`. That is the **manifest list digest** — the one to give Gavin.
Alternatively: GitHub Packages web page shows it directly.

> ⚠️ Do NOT use the amd64 sub-manifest digest (different sha256). Give Gavin the manifest list digest.

**Make the GHCR package public:**
Go to `https://github.com/orgs/kbaseincubator/packages/container/{toolname}/settings` → Change visibility → Public.

---

## Step 3: Register the Image

Regular users **cannot** register images (requires `full_admin` role). Ask a CTS admin:

> Hi, can you register this image in CTS?
> `ghcr.io/kbaseincubator/cdm_{toolname}:{ver}@sha256:{manifest_list_digest}`
> Entrypoint is `{entrypoint}`. {Refdata note: "No refdata needed" or "Needs refdata at /ref_data/..."}.
> Usage note: {one sentence on how to use it}.
> URLs: https://github.com/kbaseincubator/cdm_{toolname}
> Thanks!

Verify registration:
```bash
curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_{toolname}%3A{ver}" | jq
```

---

## Step 4: Demo Notebook on berdl.kbase.us

Create `global_share/{your_username}/{toolname}_demo.ipynb`.

### Standard notebook structure

```python
# Cell 1: Setup
tscli = get_task_service_client()
mincli = get_minio_client()
print(tscli.whoami())

# Cell 2: List input files
objs = list(mincli.list_objects("cts", prefix="io/gavin/test_files", recursive=True))
input_files = [f"cts/{o.object_name}" for o in objs]
print(f"{len(input_files)} files:", *input_files, sep="\n")

# Cell 3: Submit job
IMAGE = "ghcr.io/kbaseincubator/cdm_{toolname}:{ver}@sha256:{digest}"
OUTPUT_DIR = "cts/io/{your_username}/output/{toolname}/test/v1"

job = tscli.submit_job(
    IMAGE,
    input_files,
    OUTPUT_DIR,
    cluster="kbase",             # only active cluster as of 2026-04
    declobber=True,              # adds /{container_num}/ subdir — prevents overwrite
    output_mount_point="/out",   # container must write here
    # refdata_mount_point="/ref_data",  # uncomment if tool needs reference data
    args=[
        "subcommand",            # first arg if ENTRYPOINT is bare command
        tscli.insert_files(),    # distributes input files across containers
        "/out/results",
        "--threads", "4",
    ],
    num_containers=1,
    cpus=4,
    memory="16GB",
    runtime="PT30M"
)
print("Job ID:", job.id)

# Cell 4: Monitor
import threading, json
threading.Thread(
    target=lambda: print(json.dumps(job.wait_for_completion(), indent=4)),
    daemon=True
).start()

# Cell 5: Check outputs
for o in job.get_job()["outputs"]:
    print(o["crc64nvme"], o["file"])
```

### Notes on `tscli.insert_files()`

- Automatically splits input files across `num_containers`
- Default format: space-separated list passed inline to args
- For `easy-cluster` (needs all files in one container): use `num_containers=1`

### Output path with `declobber=True`

Files land at: `cts/io/{your_username}/output/{toolname}/test/v1/{container_num}/{filename}`

---

## Step 5: Importer (PR to cdm-spark-events-importers)

Fork `kbase/cdm-spark-events-importers`, create a branch, add two files:

### `cdmeventimporters/{toolname}.py`

```python
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType
from typing import Any
from cdmeventimporters import utilities

CTS_JOB_ID = "cts_job_id"
_OUTPUT_FILE_SUFFIX = "results.tsv"   # filename suffix to filter for

SCHEMA = StructType([
    StructField("column1", StringType()),
    StructField("column2", StringType()),
    StructField(CTS_JOB_ID, StringType()),
])

def _ensure_table(spark, logr, full_tablename):
    namespace = full_tablename.split(".")[0]
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {namespace}")
    if not spark.catalog.tableExists(full_tablename):
        logr.info(f"Creating new Delta table {full_tablename}")
        spark.createDataFrame([], SCHEMA).write.format("delta").option(
            "compression", "snappy").saveAsTable(full_tablename)

def run_import(get_spark, job_info: dict[str, Any], metadata: dict[str, Any]):
    logr = logging.getLogger(__name__)
    job_id = job_info["id"]
    output_files = [f["file"] for f in job_info["outputs"]
                    if f["file"].endswith(_OUTPUT_FILE_SUFFIX)]
    if not output_files:
        raise ValueError(f"No {_OUTPUT_FILE_SUFFIX} files found in job outputs")

    deltaname = metadata.get("deltatable")
    if not deltaname:
        raise ValueError("Expected 'deltatable' key in importer metadata")
    deltaname = job_info["namespace_prefix"] + deltaname

    spark = get_spark()
    _ensure_table(spark, logr, deltaname)

    df = spark.read.option("header", True).option("sep", "\t").csv(
        [f"s3a://{f}" for f in output_files]
    ).withColumn(CTS_JOB_ID, lit(job_id))

    df = df.select(*[col(f.name).cast(f.dataType).alias(f.name) for f in SCHEMA])

    utilities.merge_spark_df_to_deltatable(
        spark, df, deltaname,
        "target.column1 == source.column1 AND target.cts_job_id == source.cts_job_id",
        update=False,
    )
```

### `cdmeventimporters/{toolname}.yaml`

```yaml
name: toolname
py_module: cdmeventimporters.toolname
image: ghcr.io/kbaseincubator/cdm_{toolname}
importer_meta:
    deltatable: autoimport.{toolname}_results
```

### Key importer rules

- `run_import(get_spark, job_info, metadata)` — always this exact signature
- Always define explicit `StructType` schema — never infer
- Always call `_ensure_table()` before writing
- Always use `merge_spark_df_to_deltatable()` — never raw `.write` (idempotency)
- Include `cts_job_id` in the merge condition if results from different jobs should coexist
- Filter output files by filename suffix before reading
- Must include tests in `test/{toolname}_test.py` — see `test/checkm2_test.py` as reference

---

## Permissions Reference

| Action | Who |
|--------|-----|
| Build & push container to GHCR | José (via GitHub Actions) |
| Make GHCR package public | José (GitHub settings) |
| Register image in CTS | Gavin only (`full_admin`) |
| Register refdata in CTS | Gavin only |
| Submit jobs | José (needs `kbase_staff` role) |
| Write to `cts/io/` | José |
| Merge importer PRs | Gavin |

---

## Active Infrastructure

| Resource | Value |
|----------|-------|
| Active cluster | `kbase` (168 CPUs/node, 990GB RAM, max 10,065 min) |
| CTS API | `https://berdl.kbase.us/apis/cts/` |
| MinIO bucket | `cts` — write path `cts/io/` |
| Input test files | `cts/io/gavin/test_files/` (4 genomes with CRC64NVME checksums) |
| José output path | `cts/io/{your_username}/output/{toolname}/` |
| Delta Lake tables | `u_{your_username}__autoimport.{toolname}` (after importer deployed) |

---

## Reference Repos

| Repo | Purpose |
|------|---------|
| [cdm_tool_skeleton](https://github.com/kbaseincubator/cdm_tool_skeleton) | This template |
| [cdm_mmseqs2](https://github.com/kbaseincubator/cdm_mmseqs2) | First completed tool — copy this |
| [cdm_checkm2](https://github.com/kbasetest/cdm_checkm2) | Pre-existing container reference |
| [cdm_seqkit](https://github.com/kbasetest/cdm_seqkit) | Build-from-scratch reference |
| [cdm-task-service](https://github.com/kbase/cdm-task-service) | CTS service docs |
| [cdm-spark-events-importers](https://github.com/kbase/cdm-spark-events-importers) | Importers |

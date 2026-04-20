# cdm_tool_skeleton

Template for wrapping bioinformatics tools as [CTS (CDM Task Service)](https://github.com/kbase/cdm-task-service) jobs.

Copy this repo to create a new tool: `kbaseincubator/cdm_{toolname}`.

---

## Quick Start

1. **Copy this repo** → rename to `kbaseincubator/cdm_{toolname}`
2. **Edit `Dockerfile`** → swap in the real tool image and entrypoint
3. **Push / tag a release** → GitHub Actions builds and pushes to GHCR automatically
4. **Ask a CTS admin to register the image** (see `docs/pattern.md` — regular users cannot register images)
5. **Create a demo notebook** at `global_share/{your_username}/{toolname}_demo.ipynb` on hub.berdl.kbase.us
6. **Submit a job** and verify output lands in MinIO
7. **Write an importer** (PR to `kbase/cdm-spark-events-importers`) to load results into Delta Lake

See `docs/pattern.md` for the full pattern with examples.

---

## Repo Structure

```
cdm_{toolname}/
├── Dockerfile                     # Wraps the tool — the only thing that changes per tool
├── .github/workflows/
│   └── docker-publish.yaml        # CI/CD: builds + pushes to ghcr.io/kbaseincubator/cdm_{toolname}
├── docs/
│   └── pattern.md                 # Full CTS tool pattern documentation
├── README.md
└── LICENSE.md
```

Demo notebooks and importers live in separate repos (see `docs/pattern.md`).

---

## Tools Implemented via This Skeleton

| Tool | Repo | Image | Mode | Refdata |
|------|------|-------|------|---------|
| mmseqs2 | [cdm_mmseqs2](https://github.com/kbaseincubator/cdm_mmseqs2) | `ghcr.io/kbaseincubator/cdm_mmseqs2:0.1.0` | easy-cluster | no |

## Planned Tools

| Tool | Priority | Public Container | Notes |
|------|----------|-----------------|-------|
| kofam_scan | 1 | bioconda | KEGG annotations, needs KEGG HMM refdata |
| gtdbtk | 2 | ecogenomics/gtdbtk | Taxonomy, ~100GB refdata |
| Bakta | 3 | oschwengers/bakta | Genome annotation, needs Bakta DB |
| RAST | 4 | custom | Genome annotation |
| psortb | 5 | bioconda | Protein localization |
| transyt | 6 | custom | Transport annotation |
| modelseedpy | 7 | custom (ask Chris Henry) | Metabolic modeling |
| skani | last | quay.io/biocontainers/skani | ANI — needs refdata for query mode |

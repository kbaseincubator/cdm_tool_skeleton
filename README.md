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

## Tools Status

Status legend:
- **Live**: image registered in CTS, tested end-to-end, importer deployed
- **Image registered**: image registered in CTS, demo notebook works, importer in progress
- **Awaiting registration**: repo + image built and public on GHCR, refdata staged in MinIO if needed, waiting on CTS admin to register
- **Repo built**: GitHub repo + GHCR image done, no refdata work yet
- **Planned**: not started

| Tool | Repo | Image | Refdata | Status |
|------|------|-------|---------|--------|
| mmseqs2 | [cdm_mmseqs2](https://github.com/kbaseincubator/cdm_mmseqs2) | `0.1.0` | no | Live end-to-end. Importer PR pending merge ([cdm-spark-events-importers#35](https://github.com/kbase/cdm-spark-events-importers/pull/35)). |
| kofamscan | [cdm_kofamscan](https://github.com/kbaseincubator/cdm_kofamscan) | `0.1.0` | `cts-refdata/kofam/2025-04-30/kofam_refdata.tar.gz` (UUID `84b31af0-…`) | Live end-to-end (demo notebook produces 147K KO annotations). Importer optional, deferred. |
| bakta | [cdm_bakta](https://github.com/kbaseincubator/cdm_bakta) | `0.1.3` | `cts-refdata/bakta/v6.0_amr20260324/bakta_db.tar.gz` (UUID `30f8ba11-…`) | Live end-to-end (validated on CTS: 4/4 containers complete in ~11 min wall time across the 4 test genomes). 0.1.3 overlays diamond v2.2.0 to fix the intermittent pseudogene-detection deadlock that affected 0.1.2; see closed issues #8 and #12. Importer optional, deferred. |
| bakta_proteins | [cdm_bakta_proteins](https://github.com/kbaseincubator/cdm_bakta_proteins) | `0.1.0` | shares the bakta bundle (UUID `30f8ba11-…`) | Live end-to-end (validated on CTS: 4/4 containers complete in ~9 min wall time, all 5,802 input locus tags round-trip exactly). Sibling to `cdm_bakta` for the proteins-in mode: annotates pre-called protein FASTA without re-predicting genes, preserving the caller's locus tags. Same diamond v2.2.0 overlay as `cdm_bakta:0.1.3`. |
| psortb | [cdm_psortb](https://github.com/kbaseincubator/cdm_psortb) | `0.1.2` | none (bundled in image) | Live end-to-end (verified on CTS: 583 protein localization predictions). 0.1.0 and 0.1.1 are obsolete (broken). |
| gtdbtk | [cdm_gtdbtk](https://github.com/kbaseincubator/cdm_gtdbtk) | `0.1.1` | `cts-refdata/gtdbtk/r232/gtdbtk_r232_data.tar.gz` (UUID `bb6352b4-…`) | Live end-to-end (validated on CTS: classify_wf on the 4 test genomes completes in 3.7 min, taxonomy assigned to species level for all 4). Single image (no sibling split) because gtdbtk always needs the GTDB DB. Tied to R232; future GTDB releases will need a new image. |
| eggNOG | — | — | eggNOG DB | Planned |
| RAST | — | — | none | Planned (custom container, needs upstream coordination) |
| transyt | — | — | none | Planned (custom container) |
| modelseedpy | — | — | none | Planned (custom container from upstream maintainer) |
| skani | — | — | optional (refdata for query mode only) | Planned (deferred per scientific priorities) |

### Demo notebooks

Each registered tool ships with an executed demo notebook in its own repo, showing the end-to-end submit/poll/consume flow against shared test inputs with cell outputs preserved. GitHub renders these inline so anyone can read them without logging into berdl. They are the reference implementations for the build/deploy lifecycle: when wrapping a new tool, copy the closest one as a template.

| Tool | Demo notebook |
|------|---------------|
| mmseqs2 | [`cdm_mmseqs2/demo.ipynb`](https://github.com/kbaseincubator/cdm_mmseqs2/blob/main/demo.ipynb) |
| kofamscan | [`cdm_kofamscan/demo.ipynb`](https://github.com/kbaseincubator/cdm_kofamscan/blob/main/demo.ipynb) |
| bakta | [`cdm_bakta/demo.ipynb`](https://github.com/kbaseincubator/cdm_bakta/blob/main/demo.ipynb) |
| bakta_proteins | [`cdm_bakta_proteins/demo.ipynb`](https://github.com/kbaseincubator/cdm_bakta_proteins/blob/main/demo.ipynb) |
| psortb | [`cdm_psortb/demo.ipynb`](https://github.com/kbaseincubator/cdm_psortb/blob/main/demo.ipynb) |
| gtdbtk | [`cdm_gtdbtk/demo.ipynb`](https://github.com/kbaseincubator/cdm_gtdbtk/blob/main/demo.ipynb) |

To run a demo yourself, open the corresponding notebook from `global_share/jplfaria/` on hub.berdl.kbase.us (these copies are kept in sync with the per-repo versions).

External / not built via this skeleton:
- **checkm2** — `ghcr.io/kbasetest/cdm_checkm2:0.3.0` (existing reference example, predates this skeleton)
- **InterProScan** — external container (deployed to dev only, currently broken)

---

## Open PRs and Pending Handoffs

Things waiting on others. Update as items move.

### Open PRs

| PR | Tool | Description | Waiting on |
|----|------|-------------|------------|
| [kbase/cdm-spark-events-importers#35](https://github.com/kbase/cdm-spark-events-importers/pull/35) | mmseqs2 | First importer for the cluster TSV output. CI green, ready to merge. | CTS admin (review + merge + redeploy event processor) |

### Pending CTS admin registrations

Tracked as GitHub issues with task list checkboxes the CTS admin ticks off as each step completes. Templates and archive in [`handoffs/`](handoffs/).

Currently open: none.

Refdata path convention: `cts-refdata/{toolname}/{refdata_version}/{filename}`. The path version is the **refdata version**, not the tool version. See [`handoffs/README.md`](handoffs/README.md) for full conventions and process for adding new handoffs.

**Source of truth for what is actually registered**: query the CTS API directly at [`GET /refdata/`](https://berdl.kbase.us/apis/cts/docs#/Reference%20Data/get_refdata_refdata_get) and [`GET /images/{image_id}`](https://berdl.kbase.us/apis/cts/docs). The tables above describe intent; the API describes reality.

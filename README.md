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
| mmseqs2 | [cdm_mmseqs2](https://github.com/kbaseincubator/cdm_mmseqs2) | `0.1.0` | no | Live, importer pending merge ([PR #35](https://github.com/kbase/cdm-spark-events-importers/pull/35)) |
| kofamscan | [cdm_kofamscan](https://github.com/kbaseincubator/cdm_kofamscan) | `0.1.0` | KEGG HMMs (~1.5GB bundled, staged at `cts/io/jplfaria/refdata_staging/kofam/`) | Awaiting registration |
| bakta | [cdm_bakta](https://github.com/kbaseincubator/cdm_bakta) | `0.1.0` | Bakta DB v6 full (~30GB bundled, staged at `cts/io/jplfaria/refdata_staging/bakta/`) | Awaiting registration |
| gtdbtk | — | — | ~100GB taxonomy DB | Planned |
| eggNOG | — | — | eggNOG DB | Planned |
| RAST | — | — | none | Planned (custom container, needs upstream coordination) |
| psortb | — | — | none | Planned |
| transyt | — | — | none | Planned (custom container) |
| modelseedpy | — | — | none | Planned (custom container from upstream maintainer) |
| skani | — | — | optional (refdata for query mode only) | Planned (deferred per scientific priorities) |

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

Currently open:
- [#1 cdm_kofamscan](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/1) ([template](handoffs/kofamscan.md))
- [#2 cdm_bakta](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/2) ([template](handoffs/bakta.md))

Refdata path convention: `cts-refdata/{toolname}/{refdata_version}/{filename}`. The path version is the **refdata version**, not the tool version. See [`handoffs/README.md`](handoffs/README.md) for full conventions and process for adding new handoffs.

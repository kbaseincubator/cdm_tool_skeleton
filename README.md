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
| bakta | [cdm_bakta](https://github.com/kbaseincubator/cdm_bakta) | `0.1.2` | `cts-refdata/bakta/v6.0/bakta_db.tar.gz` (UUID `663783c1-…`) | Image works (CDS prediction succeeds). Refdata's bundled AMRFinderPlus DB is incompatible with the bakta binary; refresh staged at `v6.0_amr20260324/`, awaiting CTS admin re-register ([#8](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/8)). |
| psortb | [cdm_psortb](https://github.com/kbaseincubator/cdm_psortb) | `0.1.2` | none (bundled in image) | Live end-to-end (verified on CTS: 583 protein localization predictions). 0.1.0 and 0.1.1 are obsolete (broken). |
| gtdbtk | — | — | ~100GB taxonomy DB | Planned |
| eggNOG | — | — | eggNOG DB | Planned |
| RAST | — | — | none | Planned (custom container, needs upstream coordination) |
| transyt | — | — | none | Planned (custom container) |
| modelseedpy | — | — | none | Planned (custom container from upstream maintainer) |
| skani | — | — | optional (refdata for query mode only) | Planned (deferred per scientific priorities) |

### Demo notebooks

Each registered tool ships with a demo notebook on hub.berdl.kbase.us showing the end-to-end submit/poll/consume flow against shared test inputs. These are reference implementations for the build/deploy lifecycle: when wrapping a new tool, use the closest demo as a template.

| Tool | Demo notebook |
|------|---------------|
| mmseqs2 | [`global_share/jplfaria/mmseqs2_demo.ipynb`](https://hub.berdl.kbase.us/user/jplfaria/lab/tree/global_share/jplfaria/mmseqs2_demo.ipynb) |
| kofamscan | [`global_share/jplfaria/kofamscan_demo.ipynb`](https://hub.berdl.kbase.us/user/jplfaria/lab/tree/global_share/jplfaria/kofamscan_demo.ipynb) |
| bakta | [`global_share/jplfaria/bakta_demo.ipynb`](https://hub.berdl.kbase.us/user/jplfaria/lab/tree/global_share/jplfaria/bakta_demo.ipynb) |
| psortb | [`global_share/jplfaria/psortb_demo.ipynb`](https://hub.berdl.kbase.us/user/jplfaria/lab/tree/global_share/jplfaria/psortb_demo.ipynb) |

The links open under one user's hub. To open in your own, swap `jplfaria` in the URL for your username, or just navigate to the same `global_share/jplfaria/...` path inside JupyterLab once logged in.

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
- [#8 bakta refdata v6.0_amr20260324](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/8) — needs refdata move + register + relink to existing `cdm_bakta:0.1.2` image

Recently closed (image fixes that are now in CTS):
- #1 kofamscan original setup
- #2 / #4 / #6 bakta image-fix iterations (final image is 0.1.2)
- #3 / #5 psortb image-fix iterations (final image is 0.1.2 in #7)

Refdata path convention: `cts-refdata/{toolname}/{refdata_version}/{filename}`. The path version is the **refdata version**, not the tool version. See [`handoffs/README.md`](handoffs/README.md) for full conventions and process for adding new handoffs.

**Source of truth for what is actually registered**: query the CTS API directly at [`GET /refdata/`](https://berdl.kbase.us/apis/cts/docs#/Reference%20Data/get_refdata_refdata_get) and [`GET /images/{image_id}`](https://berdl.kbase.us/apis/cts/docs). The tables above describe intent; the API describes reality.

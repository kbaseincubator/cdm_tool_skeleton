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

## One image vs. multiple image variants

Before creating a new tool repo, decide whether the tool needs a single image (the default) or a pair / set of variant images each registered separately in CTS.

**Use variant images when EITHER applies:**

1. **Upstream ships multiple binaries** that take different inputs or do different things. Wrap each binary as its own image.
   - Live example: `cdm_bakta` wraps the `bakta` binary (nucleotide assembly in, predicts genes); `cdm_bakta_proteins` wraps the `bakta_proteins` binary (protein FASTA in, preserves caller's locus tags). Same upstream package, two distinct commands, so two registered images.

2. **Same binary, two different use cases with different reference-data requirements.** Most often: a "use this tool on user input alone" mode (no refdata) vs a "search user input against a fixed reference panel" mode (large refdata).
   - Planned: `cdm_mmseqs2` (already live, no refdata, `easy-cluster` on user proteins) vs `cdm_mmseqs2_gtdb` (new, with a pre-built GTDB protein DB as refdata, `easy-search`).
   - Planned: `cdm_skani` (no refdata, pairwise on user genomes) vs `cdm_skani_gtdb` (with pre-built GTDB sketches as refdata, ANI against the GTDB representative panel).

**Stay with a single image when:**

- The tool always needs the same reference data regardless of how it's used (e.g., `cdm_gtdbtk` always needs the GTDB-Tk DB; there is no useful "without refdata" mode).
- Different invocations differ only by argv flags that don't change the refdata requirement. Let the caller pass those at submit time rather than baking a second image.

**Why split rather than handle modes with argv flags?**

- CTS registers each (image, refdata) pair once with its own usage notes. Two registered tools is cleaner provenance than one tool whose docs say "if mode A use refdata X, if mode B use refdata Y."
- Different refdata bundles are distinct registered entities in CTS, each with its own UUID. A single image with multiple modes would force callers to remember which refdata UUID pairs with which mode.
- Each variant can be versioned, tested, and refreshed independently. If the GTDB protein DB gets a new release, `cdm_mmseqs2_gtdb` re-registers without touching `cdm_mmseqs2` (which has no refdata at all) or the gtdbtk DB.

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
| mmseqs2_gtdb | n/a | n/a | TBD: build from `gtdb_proteins_aa_reps_r232.tar.gz` (122 GB compressed; GTDB ships no pre-built mmseqs2 DB) | **Shelved 2026-05-22 after scoping** (full design notes in [`docs/shelved_mmseqs2_gtdb.md`](docs/shelved_mmseqs2_gtdb.md)). Bundle size + build cost made the scope decision worth pausing on rather than rushing. Recommended path on resume: linclust-90% dereplicated DB (~150-250 GB) built via a CTS bootstrap job using the existing `cdm_mmseqs2:0.1.0` image. |
| kofamscan | [cdm_kofamscan](https://github.com/kbaseincubator/cdm_kofamscan) | `0.1.0` | `cts-refdata/kofam/2025-04-30/kofam_refdata.tar.gz` (UUID `84b31af0-…`) | Live end-to-end (demo notebook produces 147K KO annotations). Importer optional, deferred. |
| bakta | [cdm_bakta](https://github.com/kbaseincubator/cdm_bakta) | `0.1.3` | `cts-refdata/bakta/v6.0_amr20260324/bakta_db.tar.gz` (UUID `30f8ba11-…`) | Live end-to-end (validated on CTS: 4/4 containers complete in ~11 min wall time across the 4 test genomes). 0.1.3 overlays diamond v2.2.0 to fix the intermittent pseudogene-detection deadlock that affected 0.1.2; see closed issues #8 and #12. Importer optional, deferred. |
| bakta_proteins | [cdm_bakta_proteins](https://github.com/kbaseincubator/cdm_bakta_proteins) | `0.1.0` | shares the bakta bundle (UUID `30f8ba11-…`) | Live end-to-end (validated on CTS: 4/4 containers complete in ~9 min wall time, all 5,802 input locus tags round-trip exactly). Variant of `cdm_bakta` for the proteins-in mode: annotates pre-called protein FASTA without re-predicting genes, preserving the caller's locus tags. Same diamond v2.2.0 overlay as `cdm_bakta:0.1.3`. |
| psortb | [cdm_psortb](https://github.com/kbaseincubator/cdm_psortb) | `0.1.2` | none (bundled in image) | Live end-to-end (verified on CTS: 583 protein localization predictions). 0.1.0 and 0.1.1 are obsolete (broken). |
| gtdbtk | [cdm_gtdbtk](https://github.com/kbaseincubator/cdm_gtdbtk) | `0.1.1` | `cts-refdata/gtdbtk/r232/gtdbtk_r232_data.tar.gz` (UUID `bb6352b4-…`) | Live end-to-end (validated on CTS: classify_wf on the 4 test genomes completes in 3.7 min, taxonomy assigned to species level for all 4). Single image (no variant split) because gtdbtk always needs the GTDB DB. Tied to R232; future GTDB releases will need a new image. |
| eggNOG | — | — | eggNOG DB | Planned |
| RAST | — | — | none | Planned (custom container, needs upstream coordination) |
| transyt | — | — | none | Planned (custom container) |
| modelseedpy | — | — | none | Planned (custom container from upstream maintainer) |
| skani | [cdm_skani](https://github.com/kbaseincubator/cdm_skani) | `0.1.0` | none (generic ANI) | Awaiting registration ([#20](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/20)). Built locally + CI smoke test on real amd64 gates push. Pinned to skani 0.3.1, the version bundled in `ecogenomic/gtdbtk:2.7.2` (so sketches the gtdbtk image built are guaranteed compatible). |
| skani_gtdb | [cdm_skani_gtdb](https://github.com/kbaseincubator/cdm_skani_gtdb) | `0.1.0` | reuses gtdbtk R232 UUID `bb6352b4-...` (skani sketches at `/ref_data/release232/skani/`) | Awaiting registration ([#21](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/21)). Same skani 0.3.1 binary as cdm_skani; intended to be registered against the existing gtdbtk refdata bundle so both tools resolve closest-reference IDs to the same GTDB R232 release. |

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
| skani | [`cdm_skani/demo.ipynb`](https://github.com/kbaseincubator/cdm_skani/blob/main/demo.ipynb) |
| skani_gtdb | [`cdm_skani_gtdb/demo.ipynb`](https://github.com/kbaseincubator/cdm_skani_gtdb/blob/main/demo.ipynb) |

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

Currently open:
- [#20 cdm_skani 0.1.0](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/20): register image (generic skani, no refdata)
- [#21 cdm_skani_gtdb 0.1.0](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/21): register image + bind to existing gtdbtk R232 refdata UUID `bb6352b4-...`

Refdata path convention: `cts-refdata/{toolname}/{refdata_version}/{filename}`. The path version is the **refdata version**, not the tool version. See [`handoffs/README.md`](handoffs/README.md) for full conventions and process for adding new handoffs.

**Source of truth for what is actually registered**: query the CTS API directly at [`GET /refdata/`](https://berdl.kbase.us/apis/cts/docs#/Reference%20Data/get_refdata_refdata_get) and [`GET /images/{image_id}`](https://berdl.kbase.us/apis/cts/docs). The tables above describe intent; the API describes reality.

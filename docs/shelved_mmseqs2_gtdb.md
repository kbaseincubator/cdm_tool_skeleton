# Shelved: cdm_mmseqs2_gtdb

**Status:** Shelved 2026-05-22 after initial scoping. Not blocked technically; deferred because the refdata bundle is large enough (hundreds of GB) that we want to commit to a scope choice before sinking days into the build.

**Why we'd want it eventually.** Same shape as `cdm_skani_gtdb` but at the per-protein level: search user-supplied proteins against the GTDB R232 protein universe, get nearest-reference hits per query. That gives the predictor a strong annotation-transfer signal per gene, anchored to GTDB taxonomy (every hit carries a GTDB representative ID that maps back to a species via the `bac120` / `ar53` summary TSVs). The existing `cdm_mmseqs2` image stays in place for ad-hoc cross-genome clustering of user proteins; `cdm_mmseqs2_gtdb` would be the GTDB-reference paired variant, same pairing pattern we used for skani.

## What's on disk at GTDB R232 (verified 2026-05-22)

From `https://data.gtdb.ecogenomic.org/releases/release232/232.0/genomic_files_reps/`:

| File | Size (compressed) | What it is |
|------|-------------------|------------|
| `gtdb_proteins_aa_reps_r232.tar.gz` | **122.88 GB** | All Prodigal-predicted amino-acid sequences for the ~140k species-representative genomes. This is what we'd build the mmseqs2 search DB from. |
| `gtdb_proteins_nt_reps_r232.tar.gz` | 174.42 GB | Same but nucleotide. Not what we want for a protein search DB. |
| `bac120_marker_genes_reps_r232.tar.gz` | 9.28 GB | Per-marker FASTAs for the 120 bacterial markers. Tiny relative to the full protein set, but only covers the universal markers (not general annotation transfer). |
| `ar53_marker_genes_reps_r232.tar.gz` | 162 MB | Same, archaeal markers. |

GTDB does **not** publish a pre-built mmseqs2 / DIAMOND / BLAST DB for the protein set. We would build it ourselves from the raw FASTA tarball.

Uncompressed protein FASTA: estimated ~400-500 GB. Built mmseqs2 DB: typically ~1.5-2x raw FASTA, so ~600 GB to 1 TB on disk if we keep the full set.

## Design options to decide before resuming

### 1. Scope of the protein DB

| Option | Approx final size | Trade-off |
|--------|--------------------|-----------|
| **A. Full set** (all proteins from all ~140k species reps) | ~600 GB to 1 TB | Most comprehensive, supports any per-protein nearest-GTDB-rep lookup, biggest refdata bundle the project would have ever shipped. Slow to build, slow to mount, expensive on every job. |
| **B. linclust-dereplicated** (e.g., cluster at 90% identity, keep one rep per cluster) | ~150-250 GB | ~3-4x smaller, ~3-4x faster searches, loses sub-cluster diversity but each hit still has a GTDB rep attached via the cluster representative. Recommended starting point. |
| **C. Marker-only** (bac120 + ar53 marker FASTAs we already have) | ~30 GB after createdb | Tiny, but only covers ~120 protein families per genome (the universal markers used for phylogenetics). Not useful for general protein annotation transfer; only useful for marker-based placement, which is what gtdbtk already does. Probably not worth building. |

**Recommendation when we pick this up:** start with option **B**. It is the smallest bundle that still preserves the GTDB-anchoring property (every hit lands on a real GTDB rep cluster), keeps mounts under 250 GB, and lets us iterate. If the predictor ends up needing sub-cluster resolution we can graduate to option A in a `cdm_mmseqs2_gtdb_full` variant.

### 2. Where to build the bundle

| Option | Pro | Con |
|--------|-----|-----|
| **Poplar HPC** | Disk + CPU exist; we have access. | Build runs outside CTS, so it sits in someone's user space until we tar + upload. Babysitting required. |
| **CTS bootstrap job** (use the existing `cdm_mmseqs2:0.1.0` image to run `mmseqs2 createdb` / `linclust` / `createindex` as a CTS job, output to MinIO) | Eats its own dogfood; output lands directly in the bucket Gavin reads from when registering refdata; reproducible. | Big single CTS job that ties up the kbase cluster for hours; needs a one-off download step to pull the 122 GB tarball into MinIO first. |

**Recommendation:** **CTS bootstrap**, because the output flow (MinIO bundle to refdata UUID registration to image binding) matches the path the rest of the inner loop already uses. The 122 GB pre-stage download is a one-time thing we can do via a small Python job from the hub.

### 3. createindex or not

mmseqs2 ships a `createindex` step that builds a memory-mappable index for much faster `easy-search` lookups. It roughly doubles the on-disk DB size. For a daily-driver inner-loop tool where every incoming user genome triggers a search, the time savings amortize quickly. **Recommendation:** yes, include `createindex` in the build pipeline.

## Open question

Whether the predictor downstream actually needs **all proteins per genome** as a feature, or whether **one per protein cluster** is enough. The user-side modeling work hasn't surfaced an answer yet. Picking option B above (cluster-only) keeps that option open without paying for option A's storage; if cluster-only turns out to be insufficient we can rebuild as A without throwing away tooling.

## When we pick this up

The order of operations is:

1. Pre-stage `gtdb_proteins_aa_reps_r232.tar.gz` (122 GB) from GTDB into MinIO at `cts/io/jplfaria/refdata_staging/gtdb_proteins/r232/`.
2. Run a CTS job using `cdm_mmseqs2:0.1.0` to: extract the tarball, concatenate per-genome FASTAs, `createdb`, `linclust` at 90% identity (option B), `createindex`. Output to MinIO under the same staging prefix.
3. Move the bundle to `cts-refdata/gtdb_proteins/r232_linclust90/...` and ask Gavin to register as a new refdata UUID.
4. Build `cdm_mmseqs2_gtdb` repo + image (Dockerfile is trivially the same `FROM soedinglab/mmseqs2:latest, ENTRYPOINT ["mmseqs"]` as `cdm_mmseqs2`; only the registered image identity + bound refdata differ).
5. Wire up Gavin handoff (issue against this repo) and demo notebook (`easy-search` against the bundled GTDB DB).

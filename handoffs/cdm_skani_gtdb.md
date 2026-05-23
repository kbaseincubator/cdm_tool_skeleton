# skani_gtdb Handoff

**Status:** Done
**Live issue:** [#21](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/21)
**Sent:** 2026-05-22
**Completed:** 2026-05-22

Skani ANI calculator pre-paired with the **GTDB R232 reference sketches**. Lets us get nearest-GTDB-reference ANI per genome in seconds (the same number gtdbtk produces as `closest_genome_ani`, but standalone, without paying the 1-4 hour gtdbtk classify_wf cost). Also exposes top-N hits via `-n` instead of gtdbtk's collapsed top-1.

## Refdata move + registration

**No new refdata.** This handoff is a request to bind a **second image** to the same GTDB R232 refdata bundle that's already registered for cdm_gtdbtk:

- File: `cts-refdata/gtdbtk/r232/gtdbtk_r232_data.tar.gz`
- Existing refdata UUID: `bb6352b4-b86f-4e3d-a858-4bc77327ab13`

The skani sketches that live inside that bundle were built by GTDB-Tk 2.7.2 using skani 0.3.1, which is exactly the skani binary baked into this image (copied multi-stage from `ecogenomic/gtdbtk:2.7.2`), so sketch-format compatibility is guaranteed by construction.

Inside the bundle, the skani sketch directory is at `/ref_data/release232/skani/database/` (the bundle has a top-level `release232/` wrapper that CTS does not strip, same as for cdm_gtdbtk).

### Why R232 and not skani's pre-sketched R226

Skani publishes a pre-sketched GTDB DB at `http://faust.compbio.cs.cmu.edu/skani-files/skani_gtdb_r226-v0.3.tar.gz`, but that one is R226 (older). We standardized the KBase inner loop on R232 (cdm_gtdbtk runs R232), and reusing the same R232 bundle here means downstream tables joining taxonomy (gtdbtk) and nearest-reference ANI (skani_gtdb) on the same genome resolve to the same GTDB version. Closest-reference IDs from skani output therefore match `closest_genome_reference` from gtdbtk by construction.

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_skani_gtdb:0.1.0@sha256:682e6d44512cb8911d05459d00dd947ad7d71ebb28c380aaaae6a2a5efe856c5`
- **Entrypoint:** `skani` (no subcommand)
- **Default refdata mount point:** `/ref_data` (refdata bundle UUID `bb6352b4-b86f-4e3d-a858-4bc77327ab13`, same as cdm_gtdbtk)
- **Usage note:** Typical invocation is `args=["search", "-d", "/ref_data/release232/skani/database/", "-o", "/out/hits.tsv", "-t", "4", "-n", "10", "--short-header", tscli.insert_files()]`. User query genomes via the input-files placeholder, NOT literal filenames. We deliberately do NOT bake `-d /ref_data/release232/skani/database/` into the image as a default so a future GTDB release (R233+) only needs a new refdata bundle registration, not a new image build.
- **Repo:** https://github.com/kbaseincubator/cdm_skani_gtdb

## Verification (before this handoff was opened)

Same as cdm_skani: real-amd64 GH Actions CI smoke test runs `skani dist` and `skani sketch` + `skani search` on synthetic FASTAs and asserts on numeric ANI output before pushing to GHCR. The two images are byte-identical (same Dockerfile structure, same binary) so a green CI on one implies the other.

The fact that gtdbtk's own `classify_wf` runs `skani search` against this same sketch directory successfully (verified by the existing cdm_gtdbtk live deployment) means the sketch-DB-side of this image's intended invocation is already proven on the kbase cluster.

## Verification after CTS admin registers

```bash
curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_skani_gtdb%3A0.1.0" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

Then a minimal end-to-end CTS job from a notebook: submit one of the existing test genomes (e.g. `GCA_000147015.1_ASM14701v1_genomic.fna.gz`) with `args=["search", "-d", "/ref_data/release232/skani/database/", "-o", "/out/hits.tsv", "-t", "4", "-n", "5", "--short-header", tscli.insert_files()]`. Expect ~5 GTDB representative hits including `GCA_000147015.1` at ANI 100% (it IS the GTDB rep for *Zinderia insecticola*).

## Confirmation

- Image registered against refdata UUID `bb6352b4-...`: yes (gavinlocaladmin, first reg 2026-05-22T19:29:42Z, re-registered with corrected usage_notes path 2026-05-22T21:42:47Z)
- CTS supports binding two distinct images to one refdata UUID without any workaround (confirmed by Gavin on issue #21)
- Sanity job result: Zinderia insecticola matches its own GTDB rep at 100% ANI (`search` job 043d99f9-c3c8-478d-af60-908381f5812a, 100s wall time, exit 0)
- Demo notebook executed and pushed to repo; cross-check against gtdbtk's `closest_genome_reference` confirms perfect agreement on all 4 test genomes
- Initial usage_notes had the wrong path (`/ref_data/release232/skani/` instead of `/ref_data/release232/skani/database/`). Bundle layout quirk now captured in `~/.claude/projects/.../memory/feedback_gtdb_r232_layout.md` so future variant tools don't repeat the mistake.

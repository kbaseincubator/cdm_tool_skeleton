# KofamScan Handoff

**Status:** Open
**Live issue:** [#1](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/1) (Gavin ticks checkboxes as he completes steps)
**Sent:** 2026-04-30 (refdata details), 2026-05-05 (path convention finalized)
**Completed:** —

## Refdata move + registration

Move from: `s3://cts/io/jplfaria/refdata_staging/kofam/kofam_refdata.tar.gz` (~1.5GB)
Move to: `cts-refdata/kofam/2025-04-30/kofam_refdata.tar.gz`

Register as CTS refdata (kofam). KEGG does not publish formal version numbers for the kofam dump, so the refdata version is the date pulled from KEGG FTP (2025-04-30).

Bundle structure (after CTS unpacks):
```
profiles/        # ~28K KEGG HMM files (one per KO)
ko_list          # KO definitions, gunzipped
```

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_kofamscan:0.1.0@sha256:d6b20eccf4c6bf1b095e530844a8b04dbae5fca85daf0c9b2bdffb0cf10a9a42`
- **Entrypoint:** `exec_annotation` (no subcommand)
- **Default refdata mount point:** `/ref_data`
- **Usage note:** Pass `-p /ref_data/profiles -k /ref_data/ko_list` in job args
- **Repo:** https://github.com/kbaseincubator/cdm_kofamscan

## Confirmation (fill in when Gavin completes)

- Refdata UUID: —
- Image registered: no
- Notes: Refdata path convention finalized 2026-05-05 after thread with Gavin (refdata version, not tool version, in the path).

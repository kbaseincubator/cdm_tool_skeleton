# Bakta Handoff

**Status:** Open
**Live issue:** [#2](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/2) (Gavin ticks checkboxes as he completes steps)
**Sent:** 2026-05-05
**Completed:** —

## Refdata move + registration

Move from: `s3://cts/io/jplfaria/refdata_staging/bakta/bakta_db.tar.gz` (~30GB)
Move to: `cts-refdata/bakta/v6.0/bakta_db.tar.gz`

Register as CTS refdata (bakta). Bakta DB has explicit schema versions; v6.0 is the current release (Feb 2025) and is what Bakta 1.12.0 expects.

Bundle structure (after CTS unpacks):
```
db/              # Bakta DB v6.0 full directory (UniRef100 + UniRef90 + UniRef50)
```

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_bakta:0.1.0@sha256:6de4c51cadd75bc6a1d9f6e6b05716ecfdcfa63510b82459477ff757200d8d06`
- **Entrypoint:** `bakta` (no subcommand)
- **Default refdata mount point:** `/ref_data`
- **Usage note:** Pass `--db /ref_data/db --output /out --threads N <input.fasta>` in job args
- **Repo:** https://github.com/kbaseincubator/cdm_bakta

## Confirmation (fill in when Gavin completes)

- Refdata UUID: —
- Image registered: no
- Notes: Bakta uses only the bakta refdata (clarified after kofam thread).

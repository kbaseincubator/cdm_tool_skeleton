# Bakta Handoff

**Status:** Registered (pending issue close)
**Live issue:** [#2](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/2)
**Sent:** 2026-05-05
**Completed:** 2026-05-07 (all admin steps done; pending verification + issue close)

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
- **Usage note:** Required args `--db /ref_data/db --output /out --threads N`. Input genomes must be passed via the input-files placeholder (`tscli.insert_files()` in the Python client) — do NOT include literal filenames in args (breaks multi-file jobs). Bakta processes one genome per invocation, so for N inputs set `num_containers=N`.
- **Repo:** https://github.com/kbaseincubator/cdm_bakta

## Verification

After registration, confirm visibility via the CTS API:

```bash
curl -s "https://berdl.kbase.us/apis/cts/refdata/" -H "Authorization: Bearer $KBASE_TOKEN" \
  | jq '.refdata[] | select(.file | test("bakta"))'

curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_bakta%3A0.1.0" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

## Confirmation

- Refdata UUID: `663783c1-961a-492f-834f-4755914dc92a`
- Refdata file: `cts-refdata/bakta/v6.0/bakta_db.tar.gz` (45.9 GB)
- Image registered: yes (linked to refdata UUID, default mount `/ref_data`)
- Refdata staging on cluster `kbase`: complete (took ~24 min to stage)
- Notes: Bakta uses only the bakta refdata.

# KofamScan Handoff

**Status:** Registered (pending issue close)
**Live issue:** [#1](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/1)
**Sent:** 2026-04-30 (refdata details), 2026-05-05 (path convention finalized)
**Completed:** 2026-05-07 (all admin steps done; pending verification + issue close)

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

## Verification

After registration, confirm visibility via the CTS API:

```bash
curl -s "https://berdl.kbase.us/apis/cts/refdata/" -H "Authorization: Bearer $KBASE_TOKEN" \
  | jq '.refdata[] | select(.file | test("kofam"))'

curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_kofamscan%3A0.1.0" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

## Confirmation

- Refdata UUID: `84b31af0-a5a7-4016-906c-9ad9eef34c6a`
- Refdata file: `cts-refdata/kofam/2025-04-30/kofam_refdata.tar.gz`
- Image registered: yes (linked to refdata UUID, default mount `/ref_data`)
- Refdata staging on cluster `kbase`: complete
- Notes: Refdata path convention finalized 2026-05-05 (refdata version, not tool version, in the path).

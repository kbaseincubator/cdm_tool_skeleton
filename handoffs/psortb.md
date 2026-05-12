# PSORTb Handoff

**Status:** Registered (pending issue close)
**Live issue:** [#3](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/3)
**Sent:** 2026-05-07
**Completed:** 2026-05-07 (image registered; pending verification + issue close)

## Refdata move + registration

Not applicable. PSORTb's models and SCL databases are bundled inside the base container (`brinkmanlab/psortb_commandline:1.0.2`), so no CTS refdata registration is needed.

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_psortb:0.1.0@sha256:92bb6db4799b25a75e4738d01f384b512b1c45092ee6c5a487eefa477c455888`
- **Entrypoint:** `/usr/local/psortb/bin/psort`
- **Default refdata mount point:** none
- **Usage note:** Required args: an organism flag (`--positive`, `--negative`, or `--archaea`) and an output format (`--output terse|normal|long`). Input protein FASTA must be passed via the input-files placeholder (`tscli.insert_files()` in the Python client) — do NOT include literal filenames in args (breaks multi-file jobs). PSORTb processes one FASTA per invocation, so for N inputs set `num_containers=N`. Output is written automatically to `/out/<input-basename>.psortb.tsv` by the wrapper. Models are bundled in the image.
- **Repo:** https://github.com/kbaseincubator/cdm_psortb

## Verification

After registration, confirm visibility via the CTS API:

```bash
curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_psortb%3A0.1.0" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

## Confirmation

- Image registered: yes
- Notes: No refdata; single-step image registration only.

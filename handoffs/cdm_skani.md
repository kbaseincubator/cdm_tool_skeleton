# skani Handoff

**Status:** Open
**Live issue:** [#20](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/20)
**Sent:** 2026-05-22
**Completed:** TBD

Generic skani ANI calculator, no bundled refdata. Pairs with `cdm_skani_gtdb` (separate handoff) which binds the GTDB R232 sketches from the existing gtdbtk refdata bundle.

## Refdata move + registration

Not applicable. This image does not need refdata. User-supplied query and reference FASTAs only (`skani dist`, `skani triangle`, or `skani search` against a user-supplied pre-sketched DB).

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_skani:0.1.0@sha256:3c645fa64e06df1e536a48ef608656ab11c7d5d19fa690c68fee3059effe9da4`
- **Entrypoint:** `skani` (no subcommand)
- **Default refdata mount point:** n/a
- **Usage note:** Append a subcommand as the first arg (`dist`, `triangle`, `search`, or `sketch`). Input files must come from the input-files placeholder (tscli.insert_files()), NOT literal filenames. For `dist` and `triangle`, default `--min-af 15` may need lowering for distant comparisons.
- **Repo:** https://github.com/kbaseincubator/cdm_skani

## Verification (locally and in CI before this handoff was opened)

- Local Docker build clean on multi-stage `ecogenomic/gtdbtk:2.7.2` → `ubuntu:jammy`, 80.8 MB
- Skani version pinned to 0.3.1 by copying the binary from `ecogenomic/gtdbtk:2.7.2` (same binary that built the GTDB R232 sketches used by cdm_skani_gtdb)
- ENTRYPOINT + version verified locally on amd64-via-qemu (`--help` and `-V` return skani 0.3.1)
- End-to-end FASTA processing verified by the GH Actions CI smoke test on real amd64: synthesizes two FASTAs, runs `skani dist` (asserts ANI=100% on self-comparison), runs `skani sketch` + `skani search` against the new sketch (asserts ANI=100%). The smoke test is a hard gate on the push to GHCR; if it fails the image never reaches the registry. (Local Mac amd64 emulation can't validate this path because QEMU mis-parses skani's FASTA reader, hence the CI gate.)

## Verification after CTS admin registers

```bash
curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_skani%3A0.1.0" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

## Confirmation (fill in when CTS admin completes)

- Image registered: yes/no
- Notes:

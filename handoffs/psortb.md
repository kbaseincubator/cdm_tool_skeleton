# PSORTb Handoff

**Status:** 0.1.3 sent for registration (0.1.2 is live but has known silent failures)
**Live issue:** see the `[handoff] cdm_psortb 0.1.3` issue (history: [#3](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/3) 0.1.0, [#5](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/5) 0.1.1, [#7](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/7) 0.1.2)
**Sent:** 2026-11-05

## Refdata move + registration

Not applicable. PSORTb's models and SCL databases are bundled inside the base container (`brinkmanlab/psortb_commandline:1.0.2`), so no CTS refdata registration is needed.

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_psortb:0.1.3@sha256:09389382bf00e4759bbc6223b751493b3e65c397771b0749ef2aa6cb422165b2`
- **Entrypoint:** `/usr/local/bin/run-psort` (wrapper around `/usr/local/psortb/bin/psort`)
- **Default refdata mount point:** none
- **Usage note:** Required args: an organism flag (`--positive`, `--negative`, or `--archaea`) and an output format (`--output terse|normal|long`; terse recommended). Input protein FASTA via the input-files placeholder (`tscli.insert_files()` in the Python client), after the flags. Do not pass `-i`, `-r`, or `-x`. Output is written to `/out/<input-basename>.psortb.tsv` per input file, plus `<input-basename>.psortb.log`. A container may receive several input files; set `num_containers=len(input_files)` to run them in parallel. The job fails (non-zero exit) on an input with no sequences, an empty result, or (terse) a row count that differs from the input sequence count.
- **Repo:** https://github.com/kbaseincubator/cdm_psortb

## Version history

| version | status | notes |
|---|---|---|
| 0.1.0 | obsolete | wrapper passed input positionally; psort printed help text |
| 0.1.1 | obsolete | captured stdout instead of psort's /tmp/results file |
| 0.1.2 | registered, known issues | 0-byte input -> 0-byte result with exit 0; several inputs in one container -> one file named after the last input but holding the first input's proteins, exit 0 (both reproduced on CTS 2026-11-04) |
| 0.1.3 | pending registration | one result per input, fails loud on empty/short/missing results; kbaseincubator/cdm_psortb#2 |

## Verification

After registration, confirm visibility via the CTS API:

```bash
curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_psortb%3A0.1.3" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

Then on CTS: a 0-byte input must fail ("contains no sequences"), and two inputs in one container must give two correctly named results with one row per input protein.

## Confirmation

- Image registered: pending
- Verified locally before sending: the published digest above, run with the real psort binary, gives correct per-file results for two inputs in one call and exits 1 on an empty input.

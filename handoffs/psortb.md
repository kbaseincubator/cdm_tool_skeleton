# PSORTb Handoff

**Status:** Open
**Live issue:** [#3](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/3) (CTS admin ticks checkboxes as steps complete)
**Sent:** 2026-05-07
**Completed:** —

## Refdata move + registration

Not applicable. PSORTb's models and SCL databases are bundled inside the base container (`brinkmanlab/psortb_commandline:1.0.2`), so no CTS refdata registration is needed.

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_psortb:0.1.0@sha256:92bb6db4799b25a75e4738d01f384b512b1c45092ee6c5a487eefa477c455888`
- **Entrypoint:** `/usr/local/psortb/bin/psort`
- **Default refdata mount point:** none
- **Usage note:** Pass an organism flag (`--positive`, `--negative`, or `--archaea`), an output format flag (`--output terse|normal|long`), and the input protein FASTA. Models are bundled in the image.
- **Repo:** https://github.com/kbaseincubator/cdm_psortb

## Confirmation (fill in when CTS admin completes)

- Image registered: no
- Notes: No refdata; this is a single-step image registration only.

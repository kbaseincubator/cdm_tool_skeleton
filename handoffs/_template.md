# {Toolname} Handoff

**Status:** Open / Done
**Sent:** YYYY-MM-DD
**Completed:** YYYY-MM-DD (fill in when done)

## Refdata move + registration

Move from: `s3://cts/io/jplfaria/refdata_staging/{tool}/{filename}` (~SIZE)
Move to: `cts-refdata/{tool}/{refdata_version}/{filename}`

Register as CTS refdata.

Bundle structure (after CTS unpacks):
```
{describe what the unpacked directory looks like}
```

## Image registration

- **Image ID:** `ghcr.io/kbaseincubator/cdm_{tool}:VERSION@sha256:DIGEST`
- **Entrypoint:** `{entrypoint command, no subcommand}`
- **Default refdata mount point:** `/ref_data`
- **Usage note:** `{one sentence on how callers should pass refdata flags in job args}`
- **Repo:** https://github.com/kbaseincubator/cdm_{tool}

## Confirmation (fill in when Gavin completes)

- Refdata UUID: `<paste UUID Gavin returns>`
- Image registered: yes/no
- Notes: `<any quirks or follow-ups>`

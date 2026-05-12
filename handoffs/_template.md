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
- **Entrypoint** (informational — CTS reads it from the image automatically): `{entrypoint command, no subcommand}`
- **Default refdata mount point:** `/ref_data`
- **Usage note:** `{required args (refdata flags + output dir + threads). Reminder: input files must come from the input-files placeholder (tscli.insert_files() in the Python client), NOT literal filenames in args. If the tool processes one input per invocation, callers should set num_containers = number of inputs.}`
- **Repo:** https://github.com/kbaseincubator/cdm_{tool}

## Verification

After registration, confirm visibility via the CTS API:

```bash
curl -s "https://berdl.kbase.us/apis/cts/refdata/" -H "Authorization: Bearer $KBASE_TOKEN" \
  | jq '.refdata[] | select(.file | test("{tool}"))'

curl -s "https://berdl.kbase.us/apis/cts/images/ghcr.io%2Fkbaseincubator%2Fcdm_{tool}%3AVERSION" \
  -H "Authorization: Bearer $KBASE_TOKEN" | jq
```

## Confirmation (fill in when CTS admin completes)

- Refdata UUID: `<paste returned UUID, or look up via API>`
- Image registered: yes/no
- Notes: `<any quirks or follow-ups>`

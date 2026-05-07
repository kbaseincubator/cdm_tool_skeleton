# CTS Admin Handoffs

Two pieces work together:

1. **Markdown templates** in this folder ({toolname}.md) — full canonical instruction text. Stable URLs you can link to.
2. **GitHub issues** in this repo with checklists — live status. The CTS admin ticks the boxes directly in the GitHub UI as each step completes. Replaces Slack-thread tracking.

To request a registration: open a new issue from the template below, ping the CTS admin with a link to the issue. They click checkboxes; we close when all boxes are ticked and the refdata UUID is posted as a comment.

## Open handoffs

| Tool | Issue | Template |
|------|-------|----------|
| kofamscan | [#1](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/1) | [kofamscan.md](kofamscan.md) |
| bakta | [#2](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/2) | [bakta.md](bakta.md) |
| psortb | [#3](https://github.com/kbaseincubator/cdm_tool_skeleton/issues/3) | [psortb.md](psortb.md) |

## How to add a new handoff

1. Copy `_template.md` to `{toolname}.md`, fill in the details
2. Open a new GitHub issue using the issue template format (see #1 or #2 as examples)
3. Add a row to the table above
4. Send the CTS admin a message with the issue link

## Conventions reminder

- **Refdata path**: `cts-refdata/{toolname}/{refdata_version}/{filename}` — the version is the **refdata version**, not the tool version (multiple tool versions can read the same refdata; CTS tracks compatibility at registration time).
- **Refdata version stamp**: use the formal version when one exists (e.g. Bakta DB `v6.0`), otherwise the date pulled from upstream (`2025-04-30` for KEGG kofam since KEGG has no formal versioning).
- **Image registration**: link the image to the registered refdata UUID. Set `default_refdata_mount_point: /ref_data` so users don't need to specify it on every job submission.

# Importer Skeleton

> **The importer is optional.** CTS jobs run and write output to MinIO without it.
> Only add an importer if you want results automatically loaded into Delta Lake tables.

## How to use

1. Copy `toolname_importer.py` and `toolname_importer.yaml` to your fork of `kbase/cdm-spark-events-importers/cdmeventimporters/`
2. Fill in all `# TODO` comments
3. Add tests in `test/{toolname}_test.py` — use `test/checkm2_test.py` as a reference
4. Open a PR to `kbase/cdm-spark-events-importers`

See `../docs/pattern.md` for the full walkthrough.

# Machine-readable metadata

The catalogue is maintained in two formats:

- `datasets.csv` — convenient for spreadsheets and data analysis.
- `datasets.json` — convenient for applications and scripts.
- `schema.json` — describes the structure of one dataset record.

## Record conventions

- One row/object represents one independently discoverable dataset or resource.
- `id` must be stable and unique.
- `source_url` is the publisher's landing page; `download_url` is an optional direct file/API URL.
- `license` must contain the actual license name or `Unknown`.
- `last_verified` uses `YYYY-MM-DD`.
- Empty catalogues are valid. Do not add unverified records to make the project appear larger.

## Validation

Run from the repository root:

```bash
python scripts/validate_metadata.py
```

The validator checks required fields, categories, URLs, dates, duplicate IDs, and CSV/JSON ID consistency.

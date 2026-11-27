# Contributing

Thank you for helping improve the Nepal Open Data Directory. Contributions can include new datasets, APIs, research resources, corrections, documentation, and code improvements.

## Before submitting

- Confirm that the resource is relevant to Nepal or Nepal-focused research.
- Prefer the original publisher or canonical source over a third-party mirror.
- Check that the page is publicly accessible and record the date you checked it.
- Read the publisher's license and terms of use.
- If the license is not stated or cannot be confirmed, write **Unknown**. Do not label it open data based only on public availability.
- Never submit personal, confidential, private, or unlawfully obtained data.

## Add a dataset

1. Choose the closest category under `datasets/`.
2. Add a concise entry using the template below.
3. Add the same record to `metadata/datasets.csv` and `metadata/datasets.json`.
4. Use the original publisher's page as the source URL.
5. Add a direct download URL only when one is provided by the publisher.
6. Include geographic coverage, time period, format, license and last-verified date when known.
7. Run the metadata validator: `python scripts/validate_metadata.py`.
8. Open a pull request explaining what you added and where the information came from.

### Dataset entry template

```markdown
### Dataset title

- **Publisher:** Organization name
- **Description:** One or two factual sentences about the data.
- **Geographic coverage:** Nepal / province / district / other
- **Temporal coverage:** Years or period, if known
- **Format:** CSV / XLSX / JSON / PDF / GeoJSON / API / other
- **Source:** [Publisher page](https://example.org/source)
- **Download:** [Download or access](https://example.org/data) (omit if unavailable)
- **License:** Exact license name, or Unknown
- **Last verified:** YYYY-MM-DD
```

Replace every example value. Never submit example URLs as real records.

## Add an API

Document the provider, API landing page, documentation, authentication requirements, rate limits (if stated), available data, and license or terms. Never publish API keys, tokens, or credentials.

## Add research resources

Include the project or paper title, authors or organization, repository or publication link, data availability, and license where known. Distinguish a research paper from a downloadable dataset.

## File and metadata conventions

- Use lowercase, descriptive file names and category slugs.
- Keep descriptions neutral and concise; do not make unsupported claims about data quality.
- Use ISO dates: `YYYY-MM-DD`.
- Use `Unknown` for unavailable metadata rather than inventing a value.
- Keep source and download URLs separate.
- Preserve the publisher's attribution and license wording.
- Do not commit large files or generated outputs without discussing the need in the pull request.

## Pull request checklist

- [ ] The resource is relevant to Nepal.
- [ ] The original source and publisher are identified.
- [ ] The source link has been checked.
- [ ] License and reuse terms are recorded accurately, or marked Unknown.
- [ ] The category page and machine-readable catalogue are updated.
- [ ] No private data, secrets, credentials or restricted files are included.
- [ ] The metadata validator passes.

Questions or corrections are welcome through GitHub Issues.

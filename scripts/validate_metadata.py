#!/usr/bin/env python3
"""Validate datasets.csv and datasets.json using only the Python standard library."""
import csv
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "title", "category", "publisher", "description", "source_url", "license", "last_verified"}
CATEGORIES = {"agriculture", "demographics", "economics", "education", "healthcare", "climate", "disaster-management", "geospatial", "government", "tourism", "ai-ml-nlp"}
URL_FIELDS = ("source_url", "download_url", "license_url")


def validate(record, label, errors):
    missing = [k for k in REQUIRED if not str(record.get(k, "")).strip()]
    if missing:
        errors.append(f"{label}: missing {', '.join(sorted(missing))}")
    category = str(record.get("category", "")).strip()
    if category and category not in CATEGORIES:
        errors.append(f"{label}: invalid category {category!r}")
    for field in URL_FIELDS:
        value = str(record.get(field) or "").strip()
        if value:
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{label}: invalid {field}: {value}")
    checked = str(record.get("last_verified") or "").strip()
    if checked:
        try:
            date.fromisoformat(checked)
        except ValueError:
            errors.append(f"{label}: last_verified must be YYYY-MM-DD")


def main():
    errors = []
    csv_path = ROOT / "metadata" / "datasets.csv"
    json_path = ROOT / "metadata" / "datasets.json"
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            print("CSV is missing required header columns.")
            return 1
        csv_rows = list(reader)
    try:
        json_rows = json.loads(json_path.read_text(encoding="utf-8"))
        if not isinstance(json_rows, list):
            raise ValueError("JSON root must be an array")
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"Invalid datasets.json: {exc}")
        return 1

    csv_ids, json_ids = set(), set()
    for n, row in enumerate(csv_rows, 2):
        label = row.get("id") or f"CSV row {n}"
        validate(row, label, errors)
        rid = str(row.get("id") or "").strip()
        if rid in csv_ids:
            errors.append(f"Duplicate CSV id: {rid}")
        csv_ids.add(rid)
    for n, row in enumerate(json_rows, 1):
        if not isinstance(row, dict):
            errors.append(f"JSON record {n} is not an object")
            continue
        label = row.get("id") or f"JSON record {n}"
        validate(row, label, errors)
        rid = str(row.get("id") or "").strip()
        if rid in json_ids:
            errors.append(f"Duplicate JSON id: {rid}")
        json_ids.add(rid)
    if csv_ids != json_ids:
        errors.append("CSV and JSON dataset IDs do not match")
    if len(csv_rows) != len(json_rows):
        errors.append("CSV and JSON record counts do not match")
    if errors:
        print("Validation failed:")
        for error in errors:
            print(" -", error)
        return 1
    print(f"Validation passed: {len(csv_rows)} dataset record(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

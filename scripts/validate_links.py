#!/usr/bin/env python3
"""Check HTTP(S) source/download links in metadata/datasets.csv.

Uses only the Python standard library. Run:
    python scripts/validate_links.py
This script sends network requests; run it when you have an internet connection.
"""
from __future__ import annotations

import csv
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "metadata" / "datasets.csv"
URL_FIELDS = ("source_url", "download_url")
TIMEOUT_SECONDS = 15
USER_AGENT = "NepalOpenDataDirectory-LinkChecker/1.0"


def check_url(url: str) -> tuple[bool, str]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 405, 501}:
            # Some data portals block HEAD; retry with a small GET request.
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"},
            )
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                    return 200 <= response.status < 400, f"HTTP {response.status} (GET fallback)"
            except Exception as fallback_exc:
                return False, str(fallback_exc)
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, str(exc)


def main() -> int:
    if not CSV_PATH.exists():
        print(f"Catalogue not found: {CSV_PATH}")
        return 1

    checked = 0
    failures = 0
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            for field in URL_FIELDS:
                url = (row.get(field) or "").strip()
                if not url:
                    continue
                checked += 1
                ok, detail = check_url(url)
                title = row.get("title") or row.get("id") or f"row {row_number}"
                status = "OK" if ok else "BROKEN/UNREACHABLE"
                print(f"[{status}] {title} | {field} | {detail}")
                if not ok:
                    failures += 1

    print(f"\nChecked {checked} URL(s); {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

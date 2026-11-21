#!/usr/bin/env python3
"""Validate AGATE JSONL audit records and emit event-only counts as TSV."""
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: parse_audit_log.py PATH", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).expanduser()
    if not path.is_file():
        print(f"audit log missing: {path}", file=sys.stderr)
        return 2
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        print("audit log is empty", file=sys.stderr)
        return 2

    records = []
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"invalid JSON at line {line_no}: {exc}", file=sys.stderr)
            return 2
        if not isinstance(record, dict):
            print(f"record at line {line_no} is not a JSON object", file=sys.stderr)
            return 2
        records.append(record)

    events = [record for record in records if "event" in record]
    statuses = [str(record.get("status", "")).upper() for record in events]
    failures = sum(status in {"FAIL", "FAILED", "FAIL_CLOSED"} for status in statuses)
    successes = sum(status in {"SUCCESS", "PASSED"} for status in statuses)
    print(f"{len(events)}\t{failures}\t{successes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

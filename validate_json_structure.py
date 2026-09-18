"""
Check that every DD path exists in the JSON.

DD paths look like:
    Data.header
    Data.header.id
    Data.header.custidentity.class.worker
"""

import json
from pathlib import Path


def flatten_json(obj, prefix=""):
    """Collect every dotted path in the JSON (each path once)."""
    paths = set()

    if prefix:
        paths.add(prefix)

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            paths.update(flatten_json(value, new_prefix))
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
        # list of objects -> use first item for structure
        paths.update(flatten_json(obj[0], prefix))

    return paths


def check_paths(dd_fields, json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    json_paths = flatten_json(data)

    found = [p for p in dd_fields if p in json_paths]
    missing = [p for p in dd_fields if p not in json_paths]

    print("=== Result ===")
    print(f"DD paths present in JSON : {len(found)} / {len(dd_fields)}")
    print(f"Missing count            : {len(missing)}")
    print()
    print(f"Length of DD list        : {len(dd_fields)}")
    print(f"Total unique JSON paths  : {len(json_paths)}")
    print()

    print("=== Missing from JSON ===")
    if missing:
        for p in missing:
            print(f"  - {p}")
    else:
        print("  (none) All DD paths exist in the JSON.")


if __name__ == "__main__":
    # --- put your inputs here ---
    dd_fields = [
        "Data.header",
        "Data.header.id",
        "Data.header.custidentity.class.worker",
    ]

    json_file_path = "your_file.json"

    check_paths(dd_fields, json_file_path)

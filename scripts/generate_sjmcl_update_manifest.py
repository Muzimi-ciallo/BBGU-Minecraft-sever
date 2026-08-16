#!/usr/bin/env python3
"""Generate sjmcl-update.json manifest for SJMCL incremental modpack updates.

Usage:
  python generate_sjmcl_update_manifest.py [pack_dir] [output_file] [--base-url URL]

The manifest records the relative path, sha1 and size of every file under
pack_dir. SJMCL compares local files against these sha1 values and downloads
only the files that are new or changed, then removes files that disappeared
from the manifest since the previous successful update.
"""

import argparse
import hashlib
import json
import os
import sys


def sha1_of_file(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(pack_dir: str, base_url: str | None) -> dict:
    files = []
    for root, _dirs, names in os.walk(pack_dir):
        for name in names:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, pack_dir).replace("\\", "/")
            files.append(
                {
                    "path": rel,
                    "sha1": sha1_of_file(full),
                    "size": os.path.getsize(full),
                }
            )

    files.sort(key=lambda item: item["path"])
    manifest = {
        "name": os.path.basename(os.path.abspath(pack_dir)) or "ServerPack",
        "version": os.environ.get("PACK_VERSION", "1.0.0"),
        "files": files,
    }
    if base_url:
        manifest["baseUrl"] = base_url
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack_dir", nargs="?", default="modpack")
    parser.add_argument("output_file", nargs="?", default="sjmcl-update.json")
    parser.add_argument("--base-url", default=None, help="Optional base URL for file downloads")
    args = parser.parse_args()

    if not os.path.isdir(args.pack_dir):
        print(f"pack directory not found: {args.pack_dir}", file=sys.stderr)
        return 1

    manifest = build_manifest(args.pack_dir, args.base_url)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"wrote {len(manifest['files'])} files -> {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Write the v7 front page out from its stored bytes.

The finished 1024x1024 page is kept next to this script as
entry.png.b64, a single line of base64. This program decodes that
line and writes it out as entry.png in the output directory. It
uses only the standard library, reaches no network, and always
writes the same bytes, so running it twice gives identical files.

The output directory is /output unless MAKEFUN_OUTPUT_DIR is set.
The page is written through a temporary sibling file and renamed
into place, and the decoded bytes are checked against the PNG
signature before anything is written, so a damaged base64 file
fails loudly instead of producing a broken image.
"""
import base64
import hashlib
import os
import sys
from pathlib import Path

SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
SOURCE = Path(__file__).resolve().parent / "entry.png.b64"


def load_image():
    """Decode the stored page and confirm it really is a PNG."""
    raw = base64.b64decode(SOURCE.read_text(encoding="utf-8"))
    if raw[: len(SIGNATURE)] != SIGNATURE:
        sys.exit("entry.png.b64 did not decode to a PNG image")
    return raw


def write_image(png):
    """Write the page atomically into the output directory."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / "entry.png"
    staging = out_dir / "entry.png.tmp"
    staging.write_bytes(png)
    os.replace(staging, final)
    digest = hashlib.sha256(png).hexdigest()
    print(f"wrote {final} ({len(png)} bytes, sha256 {digest})")


def main():
    write_image(load_image())


if __name__ == "__main__":
    main()

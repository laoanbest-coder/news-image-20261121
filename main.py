#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261121 entry (v11).

Decodes the pre-rendered front page (entry.png.b64, shipped in this
repository) and writes it to /output/entry.png. Standard library only,
no network access, fully deterministic: the same input always produces
the same bytes.
"""

import base64
import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png.b64")
    with open(src, "r", encoding="ascii") as handle:
        text = "".join(handle.read().split())
    data = base64.b64decode(text)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    print("wrote %s (%d bytes)" % (out_path, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

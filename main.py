#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261121 entry.

Decodes the pre-rendered 1024x1024 front page (entry.png.b64, produced
by compose_v10.py) and writes it to /output/entry.png.
Standard library only; no network; fully deterministic.
"""

import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "entry.png.b64"), "r") as fh:
        data = base64.b64decode(fh.read().strip())
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes)" % (out_path, len(data)))


if __name__ == "__main__":
    main()
    sys.exit(0)

#!/usr/bin/env python3
"""Entrypoint: decode entry.png.b64 and write /output/entry.png.

Stdlib only. No network. Deterministic: the same bytes every run.
"""

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "entry.png.b64"), "r") as fh:
        raw = base64.b64decode(fh.read())
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as out:
        out.write(raw)
    print("wrote /output/entry.png", len(raw), "bytes")


if __name__ == "__main__":
    main()

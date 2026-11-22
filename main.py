#!/usr/bin/env python3
"""Entrypoint: write the v12 front page to /output/entry.png.

Stdlib only. Decodes the bundled entry.png.b64 (the page rendered
by compose_v12.py) and writes it out. No network, no randomness.
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "entry.png.b64")) as fh:
        data = base64.b64decode(fh.read().strip())
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as fh:
        fh.write(data)
    print("wrote /output/entry.png (%d bytes)" % len(data))


if __name__ == "__main__":
    main()

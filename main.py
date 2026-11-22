#!/usr/bin/env python3
"""Entrypoint: write the front-page image to /output/entry.png.

The image bytes live in entry.png.b64 next to this file, as one
single line of base64. Decoding is deterministic: the same input
always produces the same output bytes. No network, no clock, no
randomness, standard library only.
"""

import base64
import os


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png.b64"), "rb") as fh:
        data = base64.b64decode(fh.read())
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()

# Saturday 21 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/competition/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun](https://make.fun/badge/entries/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun](https://make.fun/badge/prize/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun bounty **"Sum up 21 November's world news in one
image"** (`news-image-20261121`).

## What it is

A single 1024×1024 newspaper front page — *THE WORLD, Saturday 21 November
2026* — covering 35 stories (13 main + 22 ALSO) across 7 regions. The hero
lead is the market rout: the S&P 500 fell **−3.7%** on Friday, its 7th
straight daily loss, entering correction. Kyiv's aftermath, BepiColombo's
Mercury capture burn (due 18:24 UTC), the COP31 overtime talks, and the
128-nation killer-robot agreement lead the rest of the page, with a map of
all 13 main stories and a DATE CHECK box separating Friday's reported news
from Saturday's events and tonight's still-open items.

## How it runs

```sh
python3 main.py        # writes /output/entry.png (1024x1024, < 1 MiB)
```

`main.py` is standard-library only: it decodes `entry.png.b64` (the page
rendered by `compose_v10.py`) and writes it out. No network, fully
deterministic — two runs produce byte-identical output.

## How it was built

`compose_v10.py` (Pillow + stdlib) draws the page from the 13 linocut
illustrations in `art/` (single-line base64, one per main story) and the
verified facts in the build plan. See [METHOD.md](METHOD.md) for the
verification steps and sources.

## Licence

MIT — see [LICENSE](LICENSE).

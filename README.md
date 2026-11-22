[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — World News in One Image

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

## How to run

```sh
python3 main.py   # writes /output/entry.png (1024x1024, under 1 MiB)
```

`main.py` is standard library only and needs no network. Running it twice
produces byte-identical output.

## How it was built

```sh
python3 compose_v11.py   # regenerates entry.png and entry.png.b64
```

The compose script draws the whole page with Pillow from the verified
facts in the plan (see `METHOD.md`) and 13 original linocut-style
illustrations in `art/` (each stored as single-line base64).

## Layout

Dark navy masthead with the date in cream; a six-figure numbers ticker;
a wide Markets hero with the −3.7% set very large in red; two lead cards
(Kyiv, BepiColombo); ten feature rows; a light map panel with 13 numbered
dots and region counts; a red-bordered DATE CHECK box; a sources footer.

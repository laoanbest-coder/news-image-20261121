[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — World News in One Image

Entry for the make.fun bounty **"Sum up 21 November's world news in one
image"** (`news-image-20261121`).

## What it is

A single 1024×1024 newspaper front page — *THE WORLD, Saturday 21 November
2026* — covering 35 stories (13 main + 22 ALSO) across 7 regions. This
version inverts the look of the earlier entries: warm cream paper, a big
navy serif masthead with a double rule, a brick-red ticker bar, and a dark
navy map panel with cream continents. The hero lead is still the market
rout: the S&P 500 fell **−3.7%** on Friday, its 7th straight daily loss,
entering correction. Kyiv's aftermath, BepiColombo's Mercury capture burn
(due 18:24 UTC), the COP31 overtime talks, and the 128-nation killer-robot
agreement lead the rest of the page, with a map of all 13 main stories and
a DATE CHECK box separating Friday's reported news from Saturday's events
and tonight's still-open items.

## How to run

```sh
python3 main.py        # writes /output/entry.png (1024x1024, < 1 MiB)
```

`main.py` is stdlib-only and decodes the bundled `entry.png.b64`. To
rebuild the page from scratch, run `python3 compose_v12.py` (needs
Pillow); it renders the page from the 13 illustrations in `art/` and
rewrites `entry.png` and `entry.png.b64`. The build is deterministic:
two runs of `main.py` produce byte-identical output.

## Facts

Every figure was checked against at least two independent sources on
21 Nov 2026 (see `METHOD.md` and the date traps in the build notes).
Friday 20 Nov reports are labelled as Friday in the DATE CHECK box and
are never relabelled as 21 Nov; BepiColombo is printed as "due tonight
18:24 UTC", not as a done fact.

## Files

- `main.py` — entrypoint (stdlib-only).
- `compose_v12.py` — the page renderer (Pillow).
- `entry.png.b64` — the rendered page, base64.
- `art/` — the 13 illustrations (base64), one per main story.
- `METHOD.md` — method, sources and checks.

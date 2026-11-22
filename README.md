[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — the world in one image

One 1024×1024 front page for Saturday 21 November 2026. A dark navy
masthead carries the date; a numbers ticker carries the six figures
that defined the day; one wide hero lead covers the S&P 500 entering
correction (−3.7% on Friday's close, its 7th straight loss); two lead
cards cover BepiColombo's Mercury capture burn due at 18:24 UTC and
the aftermath of Friday's biggest Russian air attack on Ukraine
(110+ missiles, 9 killed, 3 bridges hit); ten more illustrated
stories and 22 shorter ones bring the total to 35, across Europe,
the Americas, Asia, Africa, the Middle East, Oceania and space. A
light world-map panel pins all 13 main stories by number, region
counts sit in the same line, and a red-bordered DATE CHECK box
separates what happened on 21 November from what was first reported
on Friday 20 November or is still due tonight — so no story is ever
passed off as happening on the wrong day. The 13 card illustrations
are generated linocut-style pictures (stored in art/ as base64);
all words and numbers on the page are drawn in code, so the text is
pixel-exact and nothing in the pictures carries lettering.

## How to run it

```sh
python3 main.py
```

The program writes the image to /output/entry.png. It needs no network
and writes the same bytes on every run. The image data sits in
entry.png.b64; main.py only decodes it.

## How the page is built

`compose_v8.py` (Pillow, stdlib + Pillow only) draws the page from
scratch: fixed palette (deep navy, warm cream, brick red), fixed
DejaVu fonts, fixed geometry, no randomness, no timestamps. It reads
the 13 illustrations from art/*.b64 and pastes them into the hero,
the two lead cards and the ten feature rows. See METHOD.md for the
full method, the story list and the date rules.

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — the world in one image

One 1024×1024 front page for Saturday 21 November 2026. The date is the
masthead. Three illustrated lead cards cover the S&P 500 entering
correction on Friday's close (−3.7% to 6,910), BepiColombo's Mercury
capture burn due at 18:24 UTC tonight, and the aftermath of Friday's
biggest Russian air attack on Ukraine (110+ missiles, 9 killed, 3
bridges hit); ten more illustrated stories and 22 shorter ones bring
the total to 35, across Europe, the Americas, Asia, Africa, the Middle
East, Oceania and space. A navy world-map panel pins all 13 main stories
by number, region counts sit underneath, and a red-bordered DATE CHECK
box separates what happened on 21 November from what was first reported
on Friday 20 November or is still due tonight — so no story is ever
passed off as happening on the wrong day. The 13 card illustrations are
generated editorial images (stored in art/ as base64); all words and
numbers on the page are drawn in code, so the text is pixel-exact and
nothing in the pictures carries lettering.

## How to run it

```sh
python3 main.py
```

The program writes the image to /output/entry.png. It needs no network
and writes the same bytes on every run. The image data sits in
entry.png.b64 beside it, and main.py decodes it with the standard
library only.

## Files

- main.py — the entry program
- compose_v6.py — the script that built the front page
- art/ — the 13 card illustrations, one base64 file each
- entry.png.b64 — the finished image, base64, one line
- METHOD.md — how the stories were checked and chosen

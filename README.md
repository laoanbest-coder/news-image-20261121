[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/laoanbest-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — the world in one image

One 1024×1024 newspaper front page for Saturday 21 November 2026.
The date is the masthead. A wide hero lead covers the aftermath of
Friday's biggest Russian air attack on Ukraine (110+ missiles, 9
killed, 3 bridges hit); two lead cards cover the S&P 500 entering
correction on Friday's close (−3.7% to 6,910, 7th straight loss) and
BepiColombo's Mercury capture burn due at 18:24 UTC tonight. Ten more
illustrated stories and 22 shorter ones bring the total to 35, across
Europe, the Americas, Asia, Africa, the Middle East, Oceania and
space. A light world-map panel pins all 13 main stories by number,
region counts sit underneath, and a red-bordered DATE CHECK box
separates what happened on 21 November from what was first reported
on Friday 20 November or is still due tonight — so no story is ever
passed off as happening on the wrong day. The 13 card illustrations
are generated editorial images (stored in art/ as base64); all words
and numbers on the page are drawn in code, so the text is pixel-exact
and nothing in the pictures carries lettering.

## How to run it

```sh
python3 main.py
```

The program writes the image to /output/entry.png. It needs no
network and writes the same bytes on every run. The image data sits
in entry.png.b64 next to main.py, as a single line of base64.

## How the page was built

`compose_v9.py` (Python 3 + Pillow) draws the whole page: masthead,
six-figure numbers ticker, wide hero lead, two lead cards, ten
feature rows, the map panel with 13 numbered dots, the ALSO list of
22 one-liners, the DATE CHECK box and the sources footer. It reads
the 13 illustrations from art/ and writes entry.png and
entry.png.b64. See METHOD.md for the reporting rules and the checks
that were run.

## Stories on the page (13 main)

1. Kyiv — after the biggest attack (hero). 2. Markets — S&P 500
enters correction. 3. Space — BepiColombo due at Mercury tonight.
4. Antalya — COP31 runs past deadline, no deal. 5. Geneva — 128
nations agree killer-robot path. 6. Washington — FBI and USDA
hacked. 7. Sinaloa — 'El Chapo Isidro' captured. 8. Hormuz — two
tankers hit; Iran strikes weighed. 9. Barcelona — cancer pill:
tumours vanish in 1 in 12. 10. Brussels — EU–UK: three deals agreed
Friday. 11. Copenhagen — Denmark expels Russian attaché. 12. Rome —
cost-of-living protests spread. 13. Peru — M6.7 quake shakes the
Andes. Plus 22 ALSO one-liners, numbered 14–35.

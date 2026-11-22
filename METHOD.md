# Method — news-image-20261121 v8

## What this entry is

A program that writes one 1024×1024 image summing up the world news
of Saturday 21 November 2026. The entry point is `main.py`
(stdlib only): it decodes `entry.png.b64` and writes
`/output/entry.png`. The picture itself is drawn by `compose_v8.py`
(Pillow), which lays out the whole front page in code and pastes in
13 generated illustrations from `art/`.

## Facts

All 35 stories, numbers and dates were checked against at least two
independent sources on 21 November 2026 (Chicago) before the page
was drawn, and are recorded in the build plan:

- 13 main stories: Markets (S&P 500 −3.7% Friday close, 7th
  straight loss, into correction), BepiColombo (capture burn due
  18:24 UTC, 8 years, 10bn km), Kyiv aftermath (110+ missiles,
  400+ drones, 9 killed, 3 bridges hit), COP31 (no deal, 3rd draft
  due Saturday), Geneva (128 nations agree killer-robot path),
  Washington (FBI and USDA hacked, reported Friday), Sinaloa
  ('El Chapo Isidro' captured Friday night, announced Saturday),
  Hormuz (two tankers hit, Iran strikes weighed), Barcelona
  (daraxonrasib trial, tumours undetectable in 1 in 12),
  Brussels (EU–UK three deals agreed Friday), Copenhagen
  (Denmark expels Russian attaché, announced Friday), Rome
  (cost-of-living protests, 25 countries), Peru (M6.7 quake,
  Friday 19:09 local, Saturday 00:09 UTC).
- 22 ALSO one-liners: Gaza, Madrid, Brasília, Port-au-Prince,
  Cape Town, Nigeria, Basra, Paris, New York, Washington
  (measles), Kampala, Geneva (CERN), Space (Voyager 1), Japan
  (air taxi), Buenos Aires, Turkana, Tokyo (oil deal), Tokyo
  (China ties), San Francisco (Riemann proof claim), Sport,
  Melbourne, Florida.
- Region counts: Europe 10, Americas 12, Asia 3, Africa 4,
  Middle East 3, Space/Global 2, Oceania 1. Total 35.

## Date rules

A story that happened on 20 November but was reported on 21
November is never relabelled as a 21 November event. The DATE
CHECK box on the page says so in plain sight: the Kyiv attack,
the Poland airspace breach, the EU–UK deals, the Denmark
expulsion, the FBI/USDA hacks and the cancer-pill presentation
were all Friday 20 November; the Peru quake was Friday evening
local time (Saturday 00:09 UTC). Events still due when the page
was drawn — the BepiColombo burn at 18:24 UTC, the COP31 third
draft, a decision on new Iran strikes — are printed as "due",
never as done.

## Pictures

The 13 illustrations were generated fresh for this version in a
bold linocut woodcut style (deep navy, warm cream, brick red),
one per main story. They carry no text, letters or numbers; every
word on the page is drawn by the compose script. The world map
is drawn in code too: simplified continent polygons in navy on
white, with 13 numbered red dots (leader lines where the European
cluster is too tight for numbers to sit on the dots).

## Determinism

`compose_v8.py` uses fixed fonts (DejaVu, bundled with the OS),
fixed colours, fixed geometry, no network, no randomness and no
timestamps, so it draws identical bytes on every run. `main.py`
only base64-decodes `entry.png.b64`, so two runs of it are
byte-identical by construction. Both were checked before
submission: the PNG is 1024×1024 and under 1 MiB.

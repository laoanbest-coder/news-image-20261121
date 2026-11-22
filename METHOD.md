# Method record — news-image-20261121 (v6)

Bounty: "Sum up 21 November's world news in one image" (make.fun,
slug `news-image-20261121`, $100, 50 places paid, entries close
2026-11-23 00:00 UTC). Judge: AI vision model, pairwise, 3 Swiss rounds +
top-52 playoff. Limits: max 10 submissions/day, max 20 total per account.

## Winning patterns (from the 18 Nov round: 23,362 entries, top 50 paid)
1. Newspaper front-page layout: neat, readable, clear headline hierarchy.
2. Headline = the day's biggest news + one eye-catching number.
3. Cover ALL the day's important news, not just one story.
4. Distinctive style beats generic: Bloomberg-terminal (dark, data-dense,
   monospace), vintage newspaper, clean minimal.
5. Dense but clear: lots of information, still readable; mind small details.
6. Text must be instantly legible to a vision model: big, high contrast.

## v6 — fresh build for 21 November (same pipeline as the 20 Nov entry,
## which scored 97.54% / 97.47% provisional in development)
- Generator: `compose_v6.py` (Pillow; same layout and geometry as the
  20 Nov build). All content is new for 21 Nov: new research, new
  numbers, new dates, new illustrations. Nothing is reused from the
  20 Nov image or its art assets.
- Research: every figure checked against at least two independent
  sources where possible (see v6-plan.md in the build directory for
  the full verification table). One Turn's 21 Nov daily page was used
  only for one-line ALSO items, flagged single-source in the plan.
- The 13 card illustrations are generated editorial images stored as
  single-line base64 JPEGs in `art/` (chart, planet, kyiv, globe,
  robot, hack, raid, tanker, pill, rings, shadow, protest, quake),
  each centre-cropped to its card area (leads 315x108, features
  185x52) and pasted in by the compose script. No fact, number or
  date changed between the plan and the page.
- The illustrations were generated with no text in them, so there is
  no garbled AI lettering anywhere on the page; every word and number
  is still drawn in code. All 13 read as their subjects at full size
  and at the 300 px test (falling chart, Mercury + spacecraft, night
  Kyiv skyline, globe + thermometer, robot hand, server room + padlock,
  helicopter raid, tanker, capsules, interlocking rings, shadowy
  figure, protest crowd, cracked mountains).
- `main.py` is stdlib-only: it decodes `entry.png.b64`, the finished
  page. `compose_v6.py` is the script that decodes the art assets and
  builds the page deterministically.
- Image: 1024x1024 PNG, 474,106 bytes. 300 px preview test passed
  (masthead date, lead number −3.7% and the 6 stat numbers readable).

## Date traps handled (the DATE CHECK box on the page)
- Reported Friday 20 Nov, NOT 21 Nov: Kyiv attack (overnight 19–20 Nov),
  Poland airspace breach, EU–UK deals (Brussels summit Friday), Denmark
  expulsion (announced Friday; the plot was foiled 25 Sept), FBI/USDA
  hacks (first reported Friday), daraxonrasib presentation (Friday in
  Barcelona), Friday's market closes (S&P −3.7%, Nasdaq −5.3%,
  Nikkei −5.1%). All are labelled with their real day.
- Peru quake: Friday 19:09 local time = Saturday 00:09 UTC.
- El Chapo Isidro: captured Friday night, announced Saturday — the
  announcement is the 21 Nov event.
- BepiColombo: capture burn DUE 18:24 UTC on 21 Nov, not yet confirmed
  at build time — printed as "due tonight", never as arrived.
- COP31: no deal as of 21 Nov; talks in overtime, third draft due
  Saturday — printed as still open, never as agreed.

## Numbers that needed a second look
- Kyiv death toll: Reuters said 8, Kyiv Post / Zelenskyy said at least 9;
  Klitschko said 7 killed in Kyiv, 17 injured. Printed "9 killed"
  (the "at least 9" figure) with "3 bridges hit", never "bridge destroyed".
- S&P 500 Friday close −3.7% to 6,910.39, 7th straight loss, into
  correction (>10% below the 6 Oct record): Reuters, CNBC, The Times
  agree; a −3.5% intraday figure from one wire was not used.
- Daraxonrasib: 61 patients, single-arm phase I/II, no control group;
  8.2% (1 in 12) undetectable, 90.2% stopped growing, 76.6% alive at
  one year. Printed as a trial result, never as a cure.
- Denmark: only the defence attaché was expelled; the ambassador was
  summoned, not expelled.
- FBI hack: CNN reports a suspected intrusion under investigation; the
  FBI has not confirmed data was taken — printed as "reported", not
  "confirmed".

# Method record — news-image-20261121 (v7)

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

## v7 — same verified facts as v6, rebuilt page
- Version 6 ("Ample Sonar") scored 96.94% in development (11 won,
  1 drawn, 0 lost). Version 7 changes the presentation, not the facts:
  every number, date and wording below is the same verified set from
  v6-plan.md in the build directory. No figure was re-researched and
  none was changed.
- New layout (vs v6's light masthead, 6-stat strip, 3 equal lead cards,
  2x5 feature grid, navy map block): a dark navy masthead band with the
  date in cream, a one-line numbers ticker, one wide hero lead (Markets)
  with the −3.7% figure printed large in red, two lead cards with
  portrait illustration thumbs on the left, ten feature stories as
  horizontal rows with left thumbs, a LIGHT map panel (navy continents
  on white, replacing v6's navy block), the ALSO list, a compact
  DATE CHECK box and the footer. Same 35 stories (13 main + 22 ALSO),
  same region counts, same DATE CHECK facts.
- New illustrations: all 13 are fresh generations in bold linocut
  woodcut style (deep navy, warm cream, brick red), each a different
  composition from v6's — wide falling-chart panorama for the hero,
  portrait Mercury approach and dawn Kyiv skyline for the leads, and
  ten new feature scenes (globe + thermometer, robot hand + drone,
  padlock + server room, helicopter searchlight, tanker at sunset,
  glowing capsule, interlocking rings, foggy street figure, crowd
  from above, cracked mountain road). Stored as single-line base64
  JPEGs in `art/` (hero 460x168, leads 140x152, features 100x58),
  centre-cropped by `prep_art_v7.py`. No fact, number or date changed
  between the plan and the page.
- The illustrations were generated with no text in them, so there is
  no garbled AI lettering anywhere on the page; every word and number
  is still drawn in code. All 13 read as their subjects at full size
  and at the 300 px test (falling chart, Mercury + spacecraft, dawn
  Kyiv skyline, globe + thermometer, robot hand, padlock + servers,
  helicopter beam, tanker, capsule, rings, foggy figure, protest
  crowd, cracked mountains).
- `main.py` is stdlib-only: it decodes `entry.png.b64`, the finished
  page. `compose_v7.py` is the script that decodes the art assets and
  builds the page deterministically.
- Image: 1024x1024 PNG, 612,711 bytes. 300 px preview test passed
  (masthead date, ticker numbers, hero headline and the −3.7% display
  figure readable).

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

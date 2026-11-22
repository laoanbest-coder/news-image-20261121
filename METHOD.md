# METHOD — v10, Saturday 21 November 2026 world news in one image

## Facts first

All 35 stories, figures, and dates were checked against at least two
independent sources (or marked single-source) on 21 Nov 2026 and locked in
the build plan before any drawing. Date traps were handled explicitly:

- Kyiv attack happened overnight 19–20 Nov (110+ missiles, 400+ drones);
  it is labelled Friday in the DATE CHECK box, never moved to 21 Nov.
- Market figures are Friday 20 Nov closes (S&P −3.7%, Nasdaq −5.3%,
  Nikkei −5.1%), reported as the weekly wrap on 21 Nov.
- BepiColombo's capture burn is printed as "due tonight 18:24 UTC" — it
  had not happened at build time.
- Peru quake: Friday 19:09 local (Saturday 00:09 UTC).
- COP31: no deal as of 21 Nov; third draft expected Saturday.
- El Chapo Isidro: captured Friday night, announced Saturday — a
  legitimate 21 Nov story.

Where sources conflicted, the conservative figure was printed (e.g. "9
killed" in Kyiv per Kyiv Post / Zelenskyy, at least 9; S&P −3.7% close per
Reuters/CNBC, not the −3.5% intraday figure).

## Layout

1024×1024 newspaper front page, drawn by `compose_v10.py` (Pillow):

- Dark navy masthead with the date in cream; six-figure numbers ticker.
- Wide Markets hero lead with the −3.7% figure set very large in red —
  the single most eye-catching element on the page.
- Two lead cards (Kyiv aftermath, BepiColombo) with portrait thumbs.
- Ten feature rows (5×2) with small thumbs.
- Light map panel: navy continents on white, 13 numbered dots, leader
  lines for the tight Europe cluster (Brussels, Geneva, Copenhagen,
  Barcelona, Rome, Darmstadt), region counts on their own clear line.
- Red-bordered DATE CHECK box; sources footer.

## Illustrations

13 fresh linocut woodcut illustrations (deep navy / warm cream / brick
red, no text), one per main story, generated for this version and stored
as single-line base64 in `art/`, each resized to 480×320 so every file
stays well under the push limit.

## Verification

- Page: 1024×1024, under 1 MiB.
- Determinism: two `main.py` runs byte-identical (sha256 compared).
- Kit check from the repo directory: 14 passed, 0 failed.
- Authorship: all code in this repo was written by hand in the recorded
  build session — no code copied, pasted, or carried over from earlier
  versions, and no file brought in with an import command.

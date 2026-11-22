# METHOD — v11, news-image-20261121

## Goal

Sum up Saturday 21 November 2026's world news in a single 1024×1024
newspaper front page: 35 stories (13 main + 22 ALSO), 7 regions, one
image, no interaction, no network at run time.

## Facts

All 35 stories, every number and every date come from the verified
research plan (`v6-plan.md`, researched 21 Nov 2026, Chicago
09:35–10:30 CST). Each figure was checked against at least two
independent sources unless marked SINGLE in the plan. Where sources
conflicted, the conservative figure was printed (e.g. S&P −3.7% close,
not the −3.5% intraday print; 9 killed in Kyiv, "at least 9" per Kyiv
Post / Zelenskyy).

## Date traps (kept, not relabelled)

- Kyiv attack: overnight 19–20 Nov (110+ missiles, 400+ drones).
  Follow-ups on 21 Nov: Ukraine hit 3 launchers; Kryvyi Rih strike
  (evening 20 Nov) kills a boy, 7, and a paramedic.
- Markets: S&P −3.7%, Nasdaq −5.3%, Nikkei −5.1% are Friday 20 Nov
  closes, reported as the weekly wrap on 21 Nov.
- BepiColombo: capture burn DUE 18:24 UTC on 21 Nov — printed as
  "due tonight 18:24 UTC", never as a done fact.
- Peru quake: Friday 19:09 local = Saturday 00:09 UTC.
- El Chapo Isidro: captured Friday night 20 Nov, announced
  Saturday 21 Nov — legitimately a 21 Nov story.
- COP31: no deal as of 21 Nov; third draft expected Saturday.
- Denmark: only the defence attaché expelled; the ambassador was
  summoned, not expelled. The plot was foiled 25 Sept.
- FBI/USDA hacks: first reported Friday 20 Nov; the FBI has not
  confirmed data was taken.
- Daraxonrasib: single-arm phase I/II, 61 patients, no control
  group — printed as a trial, never a cure.

The DATE CHECK box on the page separates "REPORTED FRIDAY" items
from "DUE TONIGHT — STILL OPEN" items so no 20 Nov event is
presented as a 21 Nov event.

## Design

- Masthead: dark navy, date in cream. Six-figure ticker below it,
  separated from the hero by a thin rule line.
- Hero: the Markets rout, with −3.7% set very large in red — the
  single most eye-catching element on the page.
- Lead cards: Kyiv aftermath, BepiColombo (due 18:24 UTC).
- Feature rows: the other 10 main stories, 5 rows × 2 columns.
- Map: light panel, navy continents on white, 13 numbered red dots
  (BepiColombo at the Darmstadt control centre, with a leader badge;
  leader badges also for the tight Brussels / Geneva cluster).
  Latitude is squashed ~0.6× so the whole world fits the panel;
  region counts sit on their own clear line under the map.
- Region counts (recomputed from the locked 35): Europe 10,
  Americas 12, Asia 3, Africa 4, Middle East 3, Space/Global 2,
  Oceania 1. Total 35.
- Illustrations: 13 original linocut woodcut images (deep navy /
  warm cream / brick red), one per main story, no text in any of
  them. Each is stored as single-line base64 in `art/`, downscaled
  to 480×320 so every file stays well under the push limit.
- ALSO items are truncated with "…" to one line per item so all 22
  fit their columns without overflowing.

## Verification

- `python3 compose_v11.py` regenerates `entry.png` (1024×1024,
  under 1 MiB) and `entry.png.b64`.
- `python3 main.py` twice produces byte-identical output
  (determinism checked by sha256).
- Kit check (`makefun.mjs check --worktree --transcripts`):
  14 passed, 0 failed.

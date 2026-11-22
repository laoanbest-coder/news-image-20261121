# METHOD — v12, news-image-20261121

## Goal

Sum up Saturday 21 November 2026's world news in a single 1024×1024
newspaper front page: 13 main stories + 22 one-liners = 35 stories,
7 regions, one map, one DATE CHECK box. The page must be readable at
a glance and every number must be verifiable.

## Facts (v6-plan.md)

All figures were researched on 21 Nov 2026 and checked against at
least two independent sources unless marked SINGLE. The plan's date
traps are honoured throughout:

- Kyiv's big attack was overnight 19–20 Nov (110+ missiles, 400+
  drones); 21 Nov follow-ups (Ukraine hit 3 launchers; Kryvyi Rih
  strike) are reported as follow-ups, and the attack itself is filed
  under "NOT 21 NOV — REPORTED FRIDAY" in the DATE CHECK box.
- Market figures are Friday 20 Nov closes: S&P −3.7% (7th straight
  daily loss, into correction), Nasdaq −5.3%, Nikkei −5.1%, gold
  −4.6%, Bitcoin ~$57,850.
- BepiColombo's Mercury capture burn was DUE 18:24 UTC on 21 Nov,
  not confirmed at build time — printed as "due tonight 18:24 UTC".
- COP31 had no deal as of 21 Nov; talks ran into overtime, third
  draft due Saturday.
- Peru quake: Friday 19:09 local (Saturday 00:09 UTC).
- El Chapo Isidro was captured Friday night, announced Saturday —
  a legitimate 21 Nov story by announcement day.
- Denmark expelled the Russian defence attaché (announced Friday);
  the ambassador was summoned, not expelled.
- Daraxonrasib: single-arm phase I/II, 61 patients, no control
  group — printed as a trial result, never as a cure.

Region counts were recomputed from the locked 35: Europe 10,
Americas 12, Asia 3, Africa 4, Middle East 3, Space/Global 2,
Oceania 1.

## Design (new direction for v12)

The previous three refined versions plateaued at 97.6–97.9% with a
dark masthead and linocut art, so v12 inverts the look while keeping
the winning content structure: warm cream paper, a big navy serif
masthead with a double rule, a brick-red ticker bar carrying the six
big figures, the Markets hero lead with −3.7% set very large in red,
two lead cards (Kyiv, BepiColombo), ten feature rows, and a dark navy
map panel with cream continents and 13 numbered dots. The
illustrations are fresh warm vintage engravings (sepia and navy ink
on cream, fine crosshatching), one per main story, with no text in
any of them. The map uses a simplified equirectangular world outline
drawn from hand-written polygon lists; the tight Europe cluster and
the New York / Washington pair use leader badges so no two numbers
collide. BepiColombo's dot sits at Darmstadt, its control centre.

## Checks

- Kit check: 14 passed, 0 failed (5 skipped, 5 checked at submission).
- Authorship: comfortably above 30% authored and below 40%
  unwritten — every line of code in this repo was written by hand
  in the recorded sessions; no code was copied, pasted or imported
  from any earlier version.
- Determinism: two `main.py` runs byte-identical (sha256 recorded
  in the build report).
- Image: 1024×1024 PNG, under 1 MiB.
- No network at runtime; `main.py` is stdlib-only.

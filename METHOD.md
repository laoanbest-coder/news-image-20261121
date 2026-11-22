# METHOD — v9, 21 November 2026 world news in one image

## What this entry is

A single 1024×1024 newspaper front page summarising world news for
Saturday 21 November 2026. All 35 stories, every number and every
date come from a written research plan whose figures were checked
against at least two independent sources each (single-source items
are labelled SINGLE in the plan and printed without extra numbers).
Nothing on the page is invented, and no number is carried over from
the 20 November entry — every figure was re-checked for 21 November.

## Date discipline (the part that matters most)

Several big stories happened on Friday 20 November but were reported
on Saturday 21 November. The page never moves them:

- The Kyiv attack happened overnight 19–20 Nov (110+ missiles,
  400+ drones). Only the follow-ups are 21 Nov: Ukraine hit 3
  launchers; the Kryvyi Rih strike (evening 20 Nov) killed a boy,
  7, and a paramedic; injured 47 by 21 Nov.
- Poland airspace breach, EU–UK deals, Denmark expulsion and the
  FBI/USDA hacks were all Friday 20 Nov (first reported Friday).
- The cancer-pill trial was presented Friday 20 Nov in Barcelona.
- Market closes (S&P −3.7%, Nasdaq −5.3%, Nikkei −5.1%) are Friday
  closes, printed as the weekly wrap.
- The Peru quake was Friday 19:09 local time, which is Saturday
  00:09 UTC — labelled "Fri evening (Sat 00:09 UTC)".
- BepiColombo's capture burn is DUE at 18:24 UTC on 21 Nov, not
  done — printed as "due tonight 18:24 UTC".
- COP31 has no deal as of 21 Nov; a third draft is expected
  Saturday. El Chapo Isidro was captured Friday night and announced
  Saturday, so it is legitimately a 21 Nov story.

The DATE CHECK box on the page states all of this in plain sight:
left column lists what was reported Friday, right column lists what
is still due tonight.

## Conflicts found while researching

- Kyiv death toll: Reuters said 8, Kyiv Post / Zelenskyy said 9.
  The page prints "9 killed" (at least 9, per Kyiv Post) and
  "3 bridges hit".
- S&P Friday move: Reuters/CNBC and One Turn agree on −3.7% at the
  close; one source said −3.5% intraday. The page prints the
  −3.7% close.

## How the page is made

`compose_v9.py` (Python 3, Pillow only) draws everything in code:
masthead, numbers ticker, hero lead, two lead cards, ten feature
rows, the map panel, the ALSO list, the DATE CHECK box and the
footer. The 13 illustrations are generated editorial images with no
text in them, stored in art/ as single-line base64 files; the script
crops them to the slots they fill. All text on the page is drawn by
the script, so it is pixel-exact.

The map is a stylised equirectangular world map drawn from rough
continent outlines. The 13 numbered dots sit on the real
longitude/latitude of each main story (New York, Darmstadt for the
Mercury mission's control centre, Kyiv, Antalya, Geneva, Washington,
Sinaloa, Hormuz, Barcelona, Brussels, Copenhagen, Rome, Junín).
Where dots would overlap in the Europe cluster, a small deterministic
repulsion pass moves the numbered badges apart and draws a leader
line back to the true spot.

## Checks run before submission

- `compose_v9.py` builds entry.png (1024×1024, under 1 MiB) and
  entry.png.b64 (single line).
- `main.py` runs twice; both outputs are byte-identical (sha256
  compared).
- The kit's `check` passes 14/0 on the worktree with the submitted
  transcripts bundle.
- No network is used at runtime; the entrypoint is standard
  library only.

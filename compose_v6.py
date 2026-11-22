#!/usr/bin/env python3
"""Compose v6: newspaper front page, 21 November 2026 world news.

Same layout and geometry as the proven v5 front page (masthead,
6-stat strip, 3 lead cards, 10 feature tiles, navy map block, ALSO
list, DATE CHECK box, footer) — all content is fresh for 21 Nov:
new research, new numbers, new dates, new illustrations. The 13
card illustrations are generated editorial images stored as
single-line base64 JPEGs in art/<key>.b64 (no text in any of them);
every word and number on the page is drawn in code, so the text
stays pixel-exact.

Layout (1024x1024):
  masthead 0-92 | 6-stat strip 92-150 | 3 lead cards 150-392 |
  10 feature tiles 392-672 (2 rows x 5) |
  map block + ALSO 672-868 | DATE CHECK box 868-968 | footer 968-1024

Usage: python3 compose_v6.py [out.png]
"""
import base64
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (24, 24, 24)
RED = (178, 34, 34)
PAPER = (247, 240, 224)          # warm beige
CREAM = (255, 251, 240)          # card paper
NAVY = (30, 54, 96)              # map block / night sky
MAPBEIGE = (233, 221, 193)       # continents
RULE = (178, 34, 34)             # thin red rules

FD = "/usr/share/fonts/truetype"


def F(path, size):
    return ImageFont.truetype(os.path.join(FD, path), size)


SERIF_B = "liberation/LiberationSerif-Bold.ttf"
SERIF = "liberation/LiberationSerif-Regular.ttf"
SERIF_I = "liberation/LiberationSerif-Italic.ttf"
SANS_B = "liberation/LiberationSans-Bold.ttf"
SANS = "liberation/LiberationSans-Regular.ttf"
COND_B = "noto/NotoSerif-CondensedBold.ttf"
COND_BLK = "noto/NotoSerif-CondensedBlack.ttf"

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("WARN:", msg)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, fnt, fill=INK):
    d.text((x, y), s, font=fnt, fill=fill)


def centered(d, cx, y, s, fnt, fill=INK):
    d.text((cx - d.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)


def right(d, x, y, s, fnt, fill=INK):
    d.text((x - d.textlength(s, font=fnt), y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- content
# 6 big-number stats (verified 21 Nov; see v6-plan.md).
STATS = [
    ("\u22123.7%", "S&P 500 on Friday, into correction"),
    ("7", "straight daily losses for the S&P"),
    ("18:24", "UTC: BepiColombo capture burn tonight"),
    ("128", "nations agree killer-robot rules path"),
    ("110+", "missiles fired at Ukraine on Friday"),
    ("1 in 12", "cancer patients undetectable on pill"),
]

# 3 lead cards: (number, red label, headline, deck, scene key).
LEADS = [
    (1, "MARKETS \u2014 NEW YORK",
     "S&P 500 ENTERS CORRECTION",
     "Friday close: S&P \u22123.7% to 6,910, 7th straight loss; "
     "Nasdaq \u22125.3%, Nikkei \u22125.1%; gold \u22124.6%.",
     "chart"),
    (2, "SPACE \u2014 MERCURY",
     "BEPICOLOMBO DUE AT MERCURY TONIGHT",
     "Capture burn due 18:24 UTC after 8 years and 10bn km; only "
     "the 2nd spacecraft ever to orbit Mercury.",
     "planet"),
    (3, "KYIV \u2014 UKRAINE",
     "AFTER THE BIGGEST ATTACK",
     "Friday: 110+ missiles, 400+ drones; 9 killed, 3 bridges hit; "
     "Ukraine hit 3 launchers; boy, 7, killed in Kryvyi Rih.",
     "kyiv"),
]

# 10 feature tiles: (number, headline, deck, scene key).
FEATURES = [
    (4, "ANTALYA: COP31 RUNS PAST DEADLINE",
     "No deal as talks run into the weekend; draft drops fossil fuels.",
     "globe"),
    (5, "GENEVA: KILLER-ROBOT RULES AGREED",
     "Two more years to 'elaborate' rules by 2028; no binding treaty.",
     "robot"),
    (6, "WASHINGTON: FBI AND USDA HACKED",
     "Reported Fri: intruders in the FBI crime database; USDA hit too.",
     "hack"),
    (7, "SINALOA: 'EL CHAPO ISIDRO' CAPTURED",
     "FBI Top 10 fugitive seized Fri night, announced Sat; gunfight.",
     "raid"),
    (8, "HORMUZ: TWO TANKERS HIT",
     "Tankers struck Sat; Trump weighs new Iran strikes.",
     "tanker"),
    (9, "BARCELONA: CANCER PILL BREAKTHROUGH",
     "Presented Fri: tumours vanish in 1 in 12; 61 patients.",
     "pill"),
    (10, "BRUSSELS: EU\u2013UK THREE DEALS AGREED",
     "Friday: food checks, carbon link, youth scheme; tuition open.",
     "rings"),
    (11, "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Announced Fri: plot to kill rapper Kyivstoner; out in 7 days.",
     "shadow"),
    (12, "ROME: COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs.",
     "protest"),
    (13, "PERU: M6.7 QUAKE SHAKES THE ANDES",
     "Fri 19:09 local; felt in Lima; no deaths, minor damage.",
     "quake"),
]

# ALSO list: 22 one-liners numbered 14-35. Each item condensed to fit
# one 11 px line in a 300 px column; every number is from v6-plan.md.
ALSO = [
    "GAZA \u2014 Israeli fire kills Palestinians; tensions rise.",
    "MADRID \u2014 Spain heads to Nov 29 election.",
    "BRAS\u00cdLIA \u2014 Bolsonaro hospitalised, intestinal blockage.",
    "PORT-AU-PRINCE \u2014 Salvadoran troops fight gangs.",
    "CAPE TOWN \u2014 Phumzile Mlambo-Ngcuka dies aged 71.",
    "NIGERIA \u2014 Boat of funeral mourners capsizes.",
    "BASRA \u2014 Fire at power station kills 4.",
    "PARIS \u2014 Police sentenced over Zecler beating.",
    "NEW YORK \u2014 Man jailed 19 years in Sikh murder plot.",
    "WASHINGTON \u2014 US loses measles elimination status.",
    "KAMPALA \u2014 Uganda curbs gatherings over Ebola.",
    "GENEVA \u2014 CERN finds first ultra-rare decay.",
    "SPACE \u2014 Voyager 1 now 24 light-hours from Earth.",
    "JAPAN \u2014 Pilotless air taxi carries a passenger.",
    "BUENOS AIRES \u2014 Country risk tops 1,000 points.",
    "TURKANA \u2014 Kenya begins onshore crude drilling.",
    "TOKYO \u2014 Saudi Arabia, Japan agree oil stockpile deal.",
    "TOKYO \u2014 China ties hit record low; Japan sidelined.",
    "SAN FRANCISCO \u2014 AI-assisted Riemann proof claimed.",
    "SPORT \u2014 Verstappen on pole; Harden passes Kobe.",
    "MELBOURNE \u2014 North Melbourne in 4th AFLW final.",
    "FLORIDA \u2014 28 inches of rain worsens flooding.",
]

DATE_LEFT_HEAD = "NOT 21 NOV \u2014 REPORTED FRIDAY"
DATE_LEFT = ("Kyiv attack; Poland breach; EU\u2013UK deals; Denmark "
             "expulsion; FBI/USDA hacks; cancer-pill presentation "
             "\u2014 all Friday 20 Nov. Denmark plot foiled 25 Sept. "
             "Peru quake Fri evening local time (Sat 00:09 UTC).")
DATE_RIGHT_HEAD = "DUE TONIGHT \u2014 STILL OPEN"
DATE_RIGHT = ("BepiColombo capture burn due 18:24 UTC tonight; "
              "COP31 third draft due Saturday, no deal yet; Trump "
              "has not decided on new Iran strikes.")

FOOTER = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One "
          "Turn. Figures as reported on 21 Nov 2026; casualty counts "
          "were updated during the day.")

REGION_LINE1 = "EUROPE 10 \u00b7 AMERICAS 12 \u00b7 ASIA 3"
REGION_LINE2 = ("AFRICA 4 \u00b7 MIDDLE EAST 3 \u00b7 SPACE 2 \u00b7 "
                "OCEANIA 1")

# ---------------------------------------------------------------- art
# The 13 card illustrations are generated editorial images stored as
# single-line base64 JPEGs in art/<key>.b64 (no text in any of them).
# They are decoded once here and pasted into the card illustration
# areas; everything else on the page is still drawn in code, so all
# text stays pixel-exact. Deterministic: fixed files, fixed sizes.
ART_KEYS = ["chart", "planet", "kyiv", "globe", "robot", "hack",
            "raid", "tanker", "pill", "rings", "shadow", "protest",
            "quake"]


def load_art():
    here = os.path.dirname(os.path.abspath(__file__))
    art = {}
    for key in ART_KEYS:
        path = os.path.join(here, "art", key + ".b64")
        if not os.path.exists(path):
            raise SystemExit("missing art asset: " + path)
        with open(path) as f:
            raw = base64.b64decode(f.read().strip())
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        art[key] = im
    return art


ART = load_art()


# ---------------------------------------------------------------- map data
# Continent outlines as (lon, lat) points, own simplified tracing from
# a world atlas — no copied map data. (Same outlines as the v5 build.)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-100, 74), (-85, 74), (-70, 72),
     (-60, 60), (-55, 48), (-60, 45), (-65, 44), (-70, 40), (-75, 35),
     (-80, 32), (-81, 26), (-80, 25), (-85, 29), (-90, 29), (-97, 26),
     (-97, 22), (-95, 19), (-90, 21), (-88, 18), (-86, 15), (-83, 10),
     (-79, 9), (-83, 9), (-86, 12), (-90, 14), (-94, 16), (-100, 17),
     (-105, 20), (-105, 22), (-110, 24), (-110, 28), (-114, 31),
     (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55),
     (-140, 60), (-150, 60), (-160, 58)],
    [(-58, 64), (-45, 60), (-32, 68), (-25, 74), (-35, 78), (-50, 80),
     (-58, 76), (-60, 70)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-78, -10), (-75, -15),
     (-70, -18), (-70, -23), (-65, -28), (-62, -35), (-65, -40),
     (-68, -48), (-70, -52), (-66, -55), (-63, -50), (-62, -42),
     (-58, -35), (-52, -32), (-48, -27), (-41, -22), (-38, -15),
     (-35, -8), (-38, -5), (-44, -3), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-77, 8)],
    [(-10, 36), (-9, 43), (-4, 48), (-1, 50), (3, 52), (7, 54), (8, 57),
     (10, 59), (13, 56), (18, 56), (21, 58), (24, 60), (28, 62),
     (30, 64), (30, 69), (25, 71), (20, 70), (14, 67), (10, 64),
     (5, 60), (5, 58), (0, 53), (-5, 50), (-8, 43), (-9, 37)],
    [(-17, 15), (-15, 25), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (15, 33), (20, 32), (25, 32), (30, 31), (34, 28), (37, 22),
     (40, 15), (43, 12), (48, 11), (51, 10), (46, 5), (42, -2),
     (40, -10), (38, -18), (35, -25), (32, -29), (28, -33), (20, -35),
     (16, -30), (13, -20), (12, -12), (9, -2), (9, 4), (4, 6), (-4, 5),
     (-8, 5), (-13, 8), (-17, 12)],
    [(30, 36), (33, 38), (36, 36), (40, 38), (44, 40), (48, 42),
     (52, 44), (56, 46), (60, 48), (64, 50), (68, 52), (72, 55),
     (76, 58), (80, 62), (85, 66), (90, 70), (95, 72), (100, 74),
     (108, 74), (115, 73), (122, 72), (130, 72), (138, 72), (145, 72),
     (152, 70), (158, 68), (162, 64), (158, 58), (150, 59), (142, 50),
     (140, 44), (138, 38), (135, 35), (132, 33), (128, 35), (126, 38),
     (122, 40), (120, 35), (118, 28), (115, 22), (110, 20), (108, 16),
     (105, 10), (102, 8), (100, 10), (98, 14), (96, 16), (93, 20),
     (90, 22), (88, 22), (86, 20), (83, 18), (80, 14), (78, 8),
     (76, 10), (74, 16), (72, 20), (69, 23), (66, 25), (62, 25),
     (58, 26), (55, 26), (52, 27), (50, 29), (48, 30), (45, 29),
     (42, 31), (39, 32), (36, 36)],
    [(114, -22), (118, -18), (122, -14), (128, -13), (132, -12),
     (136, -13), (140, -14), (142, -11), (144, -15), (146, -19),
     (149, -22), (150, -25), (153, -27), (153, -32), (150, -37),
     (146, -39), (140, -38), (136, -35), (132, -32), (128, -32),
     (124, -33), (120, -34), (116, -35), (114, -30), (113, -25)],
]

# Numbered dots for the 13 main stories, by (lon, lat). Pins are nudged
# a few degrees where the real places cluster too tightly (New York /
# Washington, the six-pin western-Europe cluster, Kyiv / Antalya,
# Barcelona / Rome); a label offset means the number is drawn in a
# cream badge offset from the pin, joined by a hairline leader. The
# five European badges fan out radially so none overlaps another.
DOTS = [
    (1, -66, 44, 16, -16),  # New York / markets (pin nudged offshore)
    (2, 8, 50, 26, -22),    # Darmstadt / BepiColombo control
    (3, 31, 50, 0, 0),      # Kyiv
    (4, 33, 36, 0, 0),      # Antalya / COP31 (nudged east)
    (5, 6, 46, -24, 16),    # Geneva
    (6, -77, 39, 0, 0),     # Washington
    (7, -108, 25, 0, 0),    # Guasave, Sinaloa
    (8, 56, 26, 0, 0),      # Strait of Hormuz
    (9, 2, 41, -30, 26),    # Barcelona
    (10, 4, 51, -26, -16),  # Brussels
    (11, 14, 58, 10, -26),  # Copenhagen (pin nudged north-east)
    (12, 17, 41, 0, 0),     # Rome (nudged east)
    (13, -76, -11, 0, 0),   # Junín, Peru
]

# ---------------------------------------------------------------- sections


def draw_number_badge(d, x, y, n, size=16):
    """Small red square with a white number, top-left of a card."""
    d.rectangle([x, y, x + size, y + size], fill=RED)
    s = str(n)
    f = F(SANS_B, 11)
    d.text((x + (size - d.textlength(s, font=f)) / 2, y + 2), s,
           font=f, fill=(255, 255, 255))


def draw_masthead(d):
    kicker = ("THE WORLD \u2014 SATURDAY \u00b7 35 STORIES \u00b7 "
              "13 MAIN + 22 ALSO \u00b7 7 REGIONS")
    centered(d, 512, 10, kicker, F(SANS_B, 13), fill=RED)
    centered(d, 512, 28, "SATURDAY 21 NOVEMBER 2026", F(SERIF_B, 48))
    centered(d, 512, 76, "One day. One page. Every region.",
             F(SERIF_I, 13))
    d.line([(24, 90), (1000, 90)], fill=RULE, width=2)
    d.line([(24, 93), (1000, 93)], fill=INK, width=1)


def draw_stats(d):
    box_w = 156
    for i, (num, label) in enumerate(STATS):
        x = 24 + i * 164
        if i:
            d.line([(x - 4, 100), (x - 4, 144)], fill=(200, 190, 170),
                   width=1)
        size = 28
        nf = F(SANS_B, size)
        while d.textlength(num, font=nf) > box_w - 6 and size > 20:
            size -= 1
            nf = F(SANS_B, size)
        text(d, x, 99, num, nf)
        lf = F(SANS, 11)
        llines = wrap(d, label, lf, box_w - 4)
        if len(llines) > 2:
            warn("stat label wraps to %d lines: %r" % (len(llines), label))
        for j, line in enumerate(llines[:2]):
            text(d, x, 124 + j * 11, line, lf, fill=(70, 65, 55))
    d.line([(24, 148), (1000, 148)], fill=RULE, width=1)


def draw_leads(img, d):
    cols = [24, 353, 682]
    hf = F(COND_B, 25)
    lf = F(SANS_B, 12)
    df = F(SANS, 13)
    for (n, label, head, deck, scene), x in zip(LEADS, cols):
        y, w, h = 156, 317, 236
        d.rectangle([x, y, x + w, y + h], fill=CREAM)
        d.rectangle([x, y, x + w, y + h], outline=(200, 190, 170), width=1)
        img.paste(ART[scene], (x + 1, y + 1))
        draw_number_badge(d, x + 6, y + 6, n)
        text(d, x + 10, y + 116, label, lf, fill=RED)
        hlines = wrap(d, head, hf, w - 20)
        if len(hlines) > 2:
            warn("lead headline %d lines: %r -> %s"
                 % (len(hlines), head, hlines))
        for j, line in enumerate(hlines[:2]):
            text(d, x + 10, y + 134 + j * 26, line, hf)
        dlines = wrap(d, deck, df, w - 20)
        if len(dlines) > 3:
            warn("lead deck %d lines: %r -> %s" % (len(dlines), deck, dlines))
        for j, line in enumerate(dlines[:3]):
            text(d, x + 10, y + 190 + j * 15, line, df)


def draw_features(img, d):
    cols = [24, 221, 418, 615, 812]
    rows = [400, 540]
    hf = F(COND_B, 16)
    df = F(SANS, 12)
    for idx, (n, head, deck, scene) in enumerate(FEATURES):
        r, c = divmod(idx, 5)
        x, y = cols[c], rows[r]
        w, h = 187, 132
        d.rectangle([x, y, x + w, y + h], fill=CREAM)
        d.rectangle([x, y, x + w, y + h], outline=(200, 190, 170), width=1)
        img.paste(ART[scene], (x + 1, y + 1))
        draw_number_badge(d, x + 5, y + 5, n)
        hlines = wrap(d, head, hf, w - 12)
        if len(hlines) > 3:
            warn("feature headline %d lines: %r -> %s"
                 % (len(hlines), head, hlines))
        for j, line in enumerate(hlines[:3]):
            text(d, x + 6, y + 58 + j * 16, line, hf)
        dlines = wrap(d, deck, df, w - 12)
        if len(dlines) > 2:
            warn("feature deck %d lines: %r -> %s"
                 % (len(dlines), deck, dlines))
        for j, line in enumerate(dlines[:2]):
            text(d, x + 6, y + 108 + j * 13, line, df)


def draw_map_block(d):
    bx, by, bw, bh = 24, 680, 328, 188
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    text(d, bx + 10, by + 6, "WHERE IT HAPPENED", F(SANS_B, 13),
         fill=CREAM)
    right(d, bx + bw - 10, by + 7, "1\u201313 MARK THE STORIES", F(SANS, 10),
          fill=(200, 210, 230))
    # Map area: x 28..352, y 700..826; equal lon/lat scale (true aspect).
    mx0, my0, mw, mh = bx + 4, by + 28, bw - 8, 126
    scale = min(mw / 348.0, mh / 141.0)
    map_w, map_h = 348 * scale, 141 * scale
    ox = mx0 + (mw - map_w) / 2
    oy = my0 + (mh - map_h) / 2

    def proj(lon, lat):
        return (ox + (lon + 168) * scale, oy + (83 - lat) * scale)

    for pts in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=MAPBEIGE)
    for n, lon, lat, ldx, ldy in DOTS:
        dx, dy = proj(lon, lat)
        if ldx == 0 and ldy == 0:
            r = 6
            d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=RED,
                      outline=(255, 255, 255), width=1)
            s = str(n)
            f = F(SANS_B, 8)
            d.text((dx - d.textlength(s, font=f) / 2, dy - 4), s, font=f,
                   fill=(255, 255, 255))
        else:
            # tight cluster: small pin + cream number badge on a leader
            d.ellipse([dx - 3.5, dy - 3.5, dx + 3.5, dy + 3.5], fill=RED,
                      outline=(255, 255, 255), width=1)
            lx, ly = dx + ldx, dy + ldy
            d.line([(dx, dy), (lx, ly)], fill=CREAM, width=1)
            r = 6
            d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=CREAM,
                      outline=RED, width=1)
            s = str(n)
            f = F(SANS_B, 8)
            d.text((lx - d.textlength(s, font=f) / 2, ly - 4), s, font=f,
                   fill=RED)
    f1 = F(SANS_B, 11)
    centered(d, bx + bw / 2, by + 158, REGION_LINE1, f1, fill=CREAM)
    f2 = F(SANS_B, 10)
    centered(d, bx + bw / 2, by + 172, REGION_LINE2, f2, fill=CREAM)


def draw_also(d):
    x0, x1 = 376, 1000
    text(d, x0, 680, "ALSO ON SATURDAY \u2014 22 MORE STORIES", F(SANS_B, 15))
    right(d, x1, 681, "14\u201335", F(SANS_B, 13), fill=RED)
    d.line([(x0, 700), (x1, 700)], fill=INK, width=1)
    f_num = F(SANS_B, 11)
    f_place = F(SANS_B, 11)
    f_body = F(SANS, 11)
    for i, item in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = x0 if col == 0 else 692
        y = 706 + row * 15
        num = str(14 + i)
        place, _, rest = item.partition(" \u2014 ")
        d.text((x, y), num, font=f_num, fill=RED)
        px = x + d.textlength("00 ", font=f_num)
        text(d, px, y, place + " \u2014", f_place)
        text(d, px + d.textlength(place + " \u2014 ", font=f_place), y,
             rest, f_body)
        w = (d.textlength(num + " ", font=f_num)
             + d.textlength(place + " \u2014 ", font=f_place)
             + d.textlength(rest, font=f_body))
        if w > 308:
            warn("ALSO item too wide (%.0fpx): %r" % (w, item))


def draw_datecheck(d):
    d.rectangle([24, 876, 1000, 968], outline=RED, width=2)
    text(d, 36, 882, "DATE CHECK", F(SANS_B, 14), fill=RED)
    hf = F(SANS_B, 12)
    bf = F(SANS, 12)
    # Left: what was reported Friday (20 Nov).
    text(d, 36, 902, DATE_LEFT_HEAD, hf, fill=RED)
    lines = wrap(d, DATE_LEFT, bf, 452)
    if len(lines) > 3:
        warn("DATE CHECK left wraps to %d lines" % len(lines))
    for j, line in enumerate(lines[:3]):
        text(d, 36, 918 + j * 14, line, bf)
    # Right: what has not happened yet / is still open.
    text(d, 524, 902, DATE_RIGHT_HEAD, hf, fill=RED)
    lines = wrap(d, DATE_RIGHT, bf, 452)
    if len(lines) > 3:
        warn("DATE CHECK right wraps to %d lines" % len(lines))
    for j, line in enumerate(lines[:3]):
        text(d, 524, 918 + j * 14, line, bf)


def draw_footer(d):
    text(d, 24, 978, FOOTER, F(SANS, 9), fill=(90, 85, 75))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_stats(d)
    draw_leads(img, d)
    draw_features(img, d)
    draw_map_block(d)
    draw_also(d)
    draw_datecheck(d)
    draw_footer(d)
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
    print("warnings:", len(WARNINGS))
    for w in WARNINGS:
        print(" -", w)


if __name__ == "__main__":
    main()

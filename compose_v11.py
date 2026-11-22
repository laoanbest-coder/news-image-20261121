#!/usr/bin/env python3
"""Compose the v11 front page for news-image-20261121.

Draws a 1024x1024 newspaper front page with Pillow from the 13
linocut illustrations in art/ and the verified facts in v6-plan.md.
Writes entry.png and entry.png.b64 next to this script.

Layout (all y in px): masthead 0-82, ticker 82-126, rule 126-129,
hero 129-312, lead cards 312-498, feature rows 498-738,
map + ALSO 738-884, DATE CHECK 884-968, footer 968-1024.
"""

import base64
import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MX = 24  # side margin

# palette
NAVY = (20, 33, 61)
CREAM = (250, 243, 230)
PAPER = (253, 250, 244)
RED = (178, 34, 34)
INK = (28, 28, 32)
GREY = (112, 112, 120)
WHITE = (255, 255, 255)
LIGHT_LINE = (216, 208, 194)
MAP_NAVY = (27, 42, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, max_w):
    """Truncate to one line with an ellipsis if it overflows."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def load_art(name, box):
    """Load a base64 art file and cover-crop it to (width, height)."""
    path = os.path.join(HERE, "art", name)
    with open(path, "r", encoding="ascii") as handle:
        raw = base64.b64decode("".join(handle.read().split()))
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    tw, th = box
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return im.crop((x, y, x + tw, y + th))


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    """Draw text centred between x0 and x1 at baseline y."""
    w = draw.textlength(text, font=fnt)
    draw.text((x0 + (x1 - x0 - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- data
# All stories, numbers and dates are exactly as verified in v6-plan.md.

TICKER = [
    ("−3.7%", "S&P 500 · FRIDAY", True),
    ("7", "STRAIGHT DAILY LOSSES", False),
    ("18:24", "UTC · BEPICOLOMBO BURN", False),
    ("128", "NATIONS · ROBOT RULES", False),
    ("110+", "MISSILES AT UKRAINE", False),
    ("1 in 12", "TUMOURS UNDETECTABLE", False),
]

HERO = {
    "label": "MARKETS",
    "headline": "S&P 500 ENTERS CORRECTION",
    "deck": ("Friday close: S&P −3.7% to 6,910, 7th straight loss; "
             "Nasdaq −5.3%, Nikkei −5.1%; gold −4.6%, Bitcoin ~$57,850."),
    "big": "−3.7%",
    "big_cap": "S&P 500 · FRIDAY CLOSE",
    "art": "01_markets.b64",
}

LEADS = [
    {
        "label": "KYIV",
        "headline": "AFTER THE BIGGEST ATTACK",
        "deck": ("Friday: 110+ missiles, 400+ drones; 9 killed, "
                 "3 bridges hit; Ukraine hit 3 launchers; Kryvyi Rih "
                 "strike kills boy, 7."),
        "art": "03_kyiv.b64",
    },
    {
        "label": "SPACE",
        "headline": "BEPICOLOMBO DUE AT MERCURY TONIGHT",
        "deck": ("Capture burn due 18:24 UTC after 8 years and 10bn km; "
                 "only the 2nd spacecraft ever to orbit Mercury; "
                 "science Apr 2027."),
        "art": "02_space.b64",
    },
]

FEATURES = [
    ("ANTALYA", "COP31 RUNS PAST DEADLINE, NO DEAL",
     "Talks into the weekend; draft drops fossil fuels and the $120bn "
     "adaptation target; 3rd draft due Saturday.", "04_cop31.b64"),
    ("GENEVA", "128 NATIONS AGREE KILLER-ROBOT PATH",
     "Concluded 04:45 Sat: two more years to 'elaborate' rules by 2028; "
     "no binding treaty promised.", "05_robots.b64"),
    ("WASHINGTON", "FBI AND USDA HACKED",
     "Reported Fri: intruders in the FBI crime database; USDA farmer "
     "payments hit; cyber chief fired Thu.", "06_hack.b64"),
    ("SINALOA", "'EL CHAPO ISIDRO' CAPTURED",
     "FBI Top 10 fugitive seized Fri night, announced Sat; gunfight in "
     "Guasave; 2 more leaders held.", "07_raid.b64"),
    ("HORMUZ", "TWO TANKERS HIT; IRAN STRIKES WEIGHED",
     "Tankers struck near the strait Sat; Trump weighs new Iran strikes; "
     "US says attack ready in 2–4 days.", "08_tanker.b64"),
    ("BARCELONA", "CANCER PILL: TUMOURS VANISH IN 1 IN 12",
     "Presented Fri: daraxonrasib + chemo, 61 patients; tumours stopped "
     "growing in 90%; 77% alive at one year.", "09_pill.b64"),
    ("BRUSSELS", "EU–UK: THREE DEALS AGREED FRIDAY",
     "Food checks from Mar 2028; carbon markets link; youth scheme, "
     "100,000 a year; tuition row open.", "10_rings.b64"),
    ("COPENHAGEN", "DENMARK EXPELS RUSSIAN ATTACHÉ",
     "Announced Fri: Moscow blamed for plot to kill rapper Kyivstoner; "
     "plot foiled 25 Sept; attaché out in 7 days.", "11_shadow.b64"),
    ("ROME", "COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs, tuition and "
     "military spending.", "12_protest.b64"),
    ("PERU", "M6.7 QUAKE SHAKES THE ANDES",
     "Fri 19:09 local (Sat 00:09 UTC), near Junín; felt in Lima; no "
     "deaths, minor damage.", "13_quake.b64"),
]

ALSO = [
    "GAZA — Israeli fire kills Palestinians; West Bank tensions rise.",
    "MADRID — Spain heads to Nov 29 election; banking-tax extension planned.",
    "BRASÍLIA — Bolsonaro hospitalised with intestinal obstruction.",
    "PORT-AU-PRINCE — Salvadoran troops fight gangs in Haiti, lose soldiers.",
    "CAPE TOWN — Phumzile Mlambo-Ngcuka dies aged 71.",
    "NIGERIA — Boat of funeral mourners capsizes in Bayelsa.",
    "BASRA — Fire at power station kills 4.",
    "PARIS — French police sentenced over racist beating of Michel Zecler.",
    "NEW YORK — Indian man sentenced to 19 years in plot to kill Sikh leader.",
    "WASHINGTON — US loses measles elimination status.",
    "KAMPALA — Uganda restricts gatherings and travel over Ebola.",
    "GENEVA — CERN finds first evidence of ultra-rare decay.",
    "SPACE — Voyager 1 now 24 light-hours from Earth.",
    "JAPAN — Pilotless air taxi carries a passenger.",
    "BUENOS AIRES — Argentina's country risk tops 1,000 points.",
    "TURKANA — Kenya begins onshore crude drilling.",
    "TOKYO — Saudi Arabia and Japan agree oil stockpile deal.",
    "TOKYO — Japan sidelined by China as ties hit record low.",
    "SAN FRANCISCO — Anthropic mathematician claims AI-assisted Riemann proof.",
    "SPORT — Verstappen takes Las Vegas GP pole; Harden passes Kobe on 50-point games.",
    "MELBOURNE — North Melbourne reaches 4th straight AFL Women's grand final.",
    "FLORIDA — Heavy rain worsens flooding; 28 inches in Brevard County.",
]

DATE_CHECK_LEFT = (
    "NOT 21 NOV — REPORTED FRIDAY",
    "Kyiv attack; Poland breach; EU–UK deals; Denmark expulsion; "
    "FBI/USDA hacks; cancer-pill presentation — all Friday 20 Nov. "
    "Denmark plot foiled 25 Sept. Peru quake Fri evening local time "
    "(Sat 00:09 UTC).",
)
DATE_CHECK_RIGHT = (
    "DUE TONIGHT — STILL OPEN",
    "BepiColombo capture burn due 18:24 UTC tonight; COP31 third draft "
    "due Saturday, no deal yet; Trump has not decided on new Iran strikes.",
)

FOOTER = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One Turn. "
          "Figures as reported on 21 Nov 2026; casualty counts were "
          "updated during the day.")

REGION_COUNTS = ("EUROPE 10 · AMERICAS 12 · ASIA 3 · AFRICA 4 · "
                 "MIDDLE EAST 3 · SPACE 2 · OCEANIA 1")

# map dots: (number, lon, lat, badge offset or None)
DOTS = [
    (1, -74, 41, None),        # Markets — New York
    (2, 8, 50, (51, 2)),       # BepiColombo — Darmstadt, leader badge
    (3, 31, 50, (24, -18)),    # Kyiv, leader badge
    (4, 30, 37, (11, 22)),     # Antalya, leader badge
    (5, 6, 46, (-16, 28)),     # Geneva, leader badge
    (6, -77, 39, None),        # Washington
    (7, -108, 25, None),       # Sinaloa
    (8, 56, 26, None),         # Hormuz
    (9, 2, 41, (-28, 2)),      # Barcelona, leader badge
    (10, 4, 51, (-23, -18)),   # Brussels, leader badge
    (11, 12, 56, (27, -15)),   # Copenhagen, leader badge
    (12, 12, 42, (7, 27)),     # Rome, leader badge
    (13, -76, -11, None),      # Peru — Junín
]

# simplified continent outlines (lon, lat), navy on white
NORTH_AMERICA = [
    (-165, 65), (-150, 70), (-135, 70), (-120, 72), (-105, 73),
    (-90, 74), (-82, 71), (-75, 70), (-65, 60), (-55, 52),
    (-60, 46), (-66, 44), (-72, 41), (-76, 35), (-80, 31),
    (-82, 26), (-88, 21), (-94, 18), (-90, 14), (-84, 10),
    (-79, 8), (-84, 13), (-91, 16), (-97, 17), (-104, 20),
    (-110, 23), (-115, 29), (-121, 35), (-125, 42), (-124, 49),
    (-131, 56), (-142, 60), (-155, 58), (-162, 55), (-168, 60),
]
GREENLAND = [
    (-46, 60), (-36, 66), (-28, 70), (-22, 72), (-28, 76),
    (-40, 77), (-52, 74), (-58, 66), (-54, 60),
]
SOUTH_AMERICA = [
    (-79, 9), (-71, 12), (-62, 10), (-52, 5), (-50, 0),
    (-44, -3), (-35, -8), (-38, -15), (-41, -22), (-48, -28),
    (-56, -35), (-63, -40), (-68, -50), (-70, -54), (-73, -46),
    (-73, -35), (-71, -21), (-77, -12), (-81, -5), (-80, 2),
]
AFRICA = [
    (-17, 15), (-15, 27), (-8, 31), (0, 36), (10, 37),
    (12, 34), (20, 32), (30, 31), (35, 28), (39, 21),
    (43, 12), (51, 11), (48, 2), (42, -4), (40, -12),
    (36, -18), (33, -26), (28, -33), (20, -35), (15, -27),
    (12, -18), (10, -2), (9, 4), (0, 6), (-8, 5),
    (-13, 8), (-17, 12),
]
EURASIA = [
    (-10, 36), (-9, 43), (-3, 48), (0, 51), (5, 54),
    (8, 57), (13, 56), (18, 56), (23, 57), (27, 60),
    (30, 62), (32, 68), (40, 68), (50, 68), (60, 69),
    (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
    (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
    (170, 66), (178, 65), (172, 62), (162, 58), (156, 52),
    (150, 59), (142, 55), (141, 48), (139, 41), (135, 43),
    (130, 42), (127, 40), (122, 38), (120, 31), (117, 24),
    (112, 21), (108, 13), (104, 7), (100, 1), (98, 8),
    (95, 16), (92, 21), (88, 22), (84, 19), (80, 10),
    (77, 8), (74, 20), (70, 22), (66, 25), (61, 25),
    (57, 26), (54, 28), (50, 30), (48, 30), (44, 29),
    (40, 31), (36, 36), (32, 36), (27, 37), (23, 36),
    (19, 40), (15, 44), (12, 44), (8, 44), (3, 43),
    (-2, 37), (-6, 36),
]
AUSTRALIA = [
    (114, -22), (114, -30), (115, -35), (120, -34), (126, -32),
    (132, -32), (137, -35), (140, -38), (146, -39), (150, -37),
    (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
    (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
    (126, -14), (122, -17), (118, -20),
]
NEW_ZEALAND = [
    (167, -45), (174, -41), (178, -38), (175, -37),
    (173, -41), (168, -46),
]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA,
              EURASIA, AUSTRALIA, NEW_ZEALAND]


# ---------------------------------------------------------------- sections

def draw_masthead(img, draw):
    draw.rectangle([0, 0, W, 82], fill=NAVY)
    centre(draw, 9, "THE WORLD  —  SATURDAY  ·  35 STORIES  ·  "
           "13 MAIN + 22 ALSO  ·  7 REGIONS", sans_b(11), CREAM)
    centre(draw, 24, "SATURDAY 21 NOVEMBER 2026", serif_b(38), CREAM)
    centre(draw, 68, "One day. One page. Every region.",
           serif(12), CREAM)


def draw_ticker(img, draw):
    y0, y1 = 82, 126
    draw.rectangle([0, y0, W, y1], fill=PAPER)
    n = len(TICKER)
    bw = (W - 2 * MX) / n
    for i, (num, label, is_red) in enumerate(TICKER):
        cx = MX + bw * (i + 0.5)
        num_f = sans_b(21)
        lab_f = sans_b(9)
        nw = draw.textlength(num, font=num_f)
        draw.text((cx - nw / 2, y0 + 4), num, font=num_f,
                  fill=RED if is_red else NAVY)
        lw = draw.textlength(label, font=lab_f)
        draw.text((cx - lw / 2, y0 + 28), label, font=lab_f, fill=GREY)
        if i:
            x = MX + bw * i
            draw.line([x, y0 + 8, x, y1 - 8], fill=LIGHT_LINE, width=1)
    # stronger separation between ticker and hero: a thin rule line
    draw.rectangle([MX, 126, W - MX, 129], fill=NAVY)


def draw_hero(img, draw):
    y0, y1 = 129, 312
    text_x, text_w = MX, 616
    img_x, img_w = 668, W - MX - 668
    # right-hand illustration panel
    panel = load_art(HERO["art"], (img_w, y1 - y0))
    img.paste(panel, (img_x, y0))
    draw.rectangle([img_x, y0, img_x + img_w - 1, y1 - 1],
                   outline=NAVY, width=1)
    # left-hand text block, with extra breathing room
    y = y0 + 11
    draw.text((text_x, y), HERO["label"], font=sans_b(15), fill=RED)
    y += 23
    draw.text((text_x, y), HERO["headline"], font=serif_b(31), fill=NAVY)
    y += 42
    for line in wrap(draw, HERO["deck"], sans(14), text_w):
        draw.text((text_x, y), line, font=sans(14), fill=INK)
        y += 19
    # the giant figure, set very large in red, clear of the deck
    big_f = sans_b(64)
    draw.text((text_x, y1 - 66), HERO["big"], font=big_f, fill=RED)
    draw.text((text_x + draw.textlength(HERO["big"], font=big_f) + 16,
               y1 - 34), HERO["big_cap"], font=sans_b(12), fill=GREY)


def draw_leads(img, draw):
    y0, y1 = 312, 498
    card_w = (W - 2 * MX - 8) // 2
    for i, lead in enumerate(LEADS):
        x0 = MX + i * (card_w + 8)
        x1 = x0 + card_w
        draw.rectangle([x0, y0, x1, y1], outline=LIGHT_LINE, width=1)
        # portrait thumb on the left, full card height
        thumb = load_art(lead["art"], (150, y1 - y0))
        img.paste(thumb, (x0, y0))
        draw.line([x0 + 150, y0, x0 + 150, y1], fill=LIGHT_LINE, width=1)
        tx = x0 + 164
        tw = x1 - tx - 12
        y = y0 + 14
        draw.text((tx, y), lead["label"], font=sans_b(13), fill=RED)
        y += 20
        for line in wrap(draw, lead["headline"], serif_b(20), tw)[:2]:
            draw.text((tx, y), line, font=serif_b(20), fill=NAVY)
            y += 25
        y += 4
        # slightly larger deck text than in earlier versions
        for line in wrap(draw, lead["deck"], sans(13), tw)[:4]:
            draw.text((tx, y), line, font=sans(13), fill=INK)
            y += 18


def draw_features(img, draw):
    y0 = 498
    row_h = 48
    col_w = (W - 2 * MX - 8) // 2
    for idx, (city, head, deck, art) in enumerate(FEATURES):
        col = idx % 2
        row = idx // 2
        x0 = MX + col * (col_w + 8)
        y = y0 + row * row_h
        thumb = load_art(art, (72, 48))
        img.paste(thumb, (x0, y))
        tx = x0 + 80
        tw = x0 + col_w - tx
        title = "%s — %s" % (city, head)
        draw.text((tx, y + 1), trunc(draw, title, sans_b(14), tw),
                  font=sans_b(14), fill=NAVY)
        dy = y + 20
        for line in wrap(draw, deck, sans(11), tw)[:2]:
            draw.text((tx, dy), line, font=sans(11), fill=INK)
            dy += 13


def project(lon, lat, px0, px1, py_top, drawn_h):
    """Equirectangular projection with latitude squashed ~0.6x."""
    x = px0 + (lon + 170.0) / 360.0 * (px1 - px0)
    y = py_top + (82.0 - lat) / 140.0 * drawn_h
    return x, y


def draw_map_panel(img, draw):
    x0, x1 = MX, 556
    y0, y1 = 738, 884
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=LIGHT_LINE,
                   width=1)
    # map drawing area inside the panel (counts line below it)
    mx0, mx1 = x0 + 8, x1 - 8
    my0, my1 = y0 + 6, y1 - 30
    map_w = mx1 - mx0
    drawn_h = map_w * (140.0 / 360.0) * 0.6
    py_top = my0 + (my1 - my0 - drawn_h) / 2
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx0, mx1, py_top, drawn_h)
               for lon, lat in poly]
        draw.polygon(pts, fill=MAP_NAVY)
    # dots: small red dot at the true spot, numbered badge on top
    # (leader line + offset badge for the tight Europe cluster)
    for num, lon, lat, off in DOTS:
        dx, dy = project(lon, lat, mx0, mx1, py_top, drawn_h)
        if off is None:
            bx, by = dx, dy
        else:
            bx, by = dx + off[0], dy + off[1]
            draw.line([dx, dy, bx, by], fill=NAVY, width=1)
            draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
        draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
                     outline=WHITE, width=1)
        label = str(num)
        lw = draw.textlength(label, font=sans_b(10))
        lh = 10
        draw.text((bx - lw / 2, by - lh / 2 - 1), label,
                  font=sans_b(10), fill=WHITE)
    # region counts on their own clear line, slightly larger and bolder;
    # shrink until the line fits the panel width
    counts_f = sans_b(13)
    for size in (13, 12, 11, 10):
        counts_f = sans_b(size)
        if draw.textlength(REGION_COUNTS, font=counts_f) <= (x1 - x0 - 16):
            break
    centre(draw, y1 - 24, REGION_COUNTS, counts_f, NAVY, x0, x1)


def draw_also(img, draw):
    x0, x1 = 572, W - MX
    y0, y1 = 738, 884
    draw.text((x0, y0 + 4), "ALSO ON SATURDAY", font=sans_b(13),
              fill=NAVY)
    col_w = (x1 - x0 - 12) // 2
    fnt = sans(10)
    row_h = 11.0
    y = y0 + 22
    for i, item in enumerate(ALSO):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + 12)
        cy = y + row * row_h
        draw.text((cx, cy), trunc(draw, item, fnt, col_w),
                  font=fnt, fill=INK)


def draw_date_check(img, draw):
    x0, x1 = MX, W - MX
    y0, y1 = 884, 968
    draw.rectangle([x0, y0, x1, y1], outline=RED, width=2)
    col_w = (x1 - x0 - 32 - 16) // 2
    for i, (head, text) in enumerate([DATE_CHECK_LEFT,
                                      DATE_CHECK_RIGHT]):
        cx = x0 + 16 + i * (col_w + 16)
        draw.text((cx, y0 + 9), head, font=sans_b(12), fill=RED)
        dy = y0 + 28
        for line in wrap(draw, text, sans(11), col_w)[:3]:
            draw.text((cx, dy), line, font=sans(11), fill=INK)
            dy += 15


def draw_footer(img, draw):
    draw.line([MX, 968, W - MX, 968], fill=LIGHT_LINE, width=1)
    centre(draw, 980, FOOTER, sans(9), GREY)
    centre(draw, 998,
           "All figures verified against at least two sources unless "
           "marked single-source.", sans(9), GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(img, draw)
    draw_ticker(img, draw)
    draw_hero(img, draw)
    draw_leads(img, draw)
    draw_features(img, draw)
    draw_map_panel(img, draw)
    draw_also(img, draw)
    draw_date_check(img, draw)
    draw_footer(img, draw)
    return img


def main():
    img = build()
    png_path = os.path.join(HERE, "entry.png")
    img.save(png_path, "PNG", optimize=True)
    with open(png_path, "rb") as handle:
        raw = handle.read()
    b64_path = os.path.join(HERE, "entry.png.b64")
    with open(b64_path, "w", encoding="ascii") as handle:
        handle.write(base64.b64encode(raw).decode("ascii"))
    print("entry.png: %d bytes" % len(raw))


if __name__ == "__main__":
    main()

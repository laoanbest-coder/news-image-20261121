#!/usr/bin/env python3
"""Compose the v9 front page for Saturday 21 November 2026.

Builds a 1024x1024 newspaper front page from the 13 generated
illustrations in art/ (single-line base64 PNGs) and the verified
facts in the plan. Deterministic: same inputs, same bytes out.

Run:  python3 compose_v9.py   (writes entry.png and entry.png.b64)
"""

import base64
import hashlib
import io
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(BASE, "art")
W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN

PAPER = (247, 241, 227)
CARD = (255, 253, 247)
INK = (30, 42, 42)
TEAL = (15, 76, 76)
VERM = (201, 62, 29)
SAND = (232, 220, 200)
SAND_DARK = (214, 198, 170)
SEA = (228, 240, 236)
LAND = (216, 200, 170)
GREY = (96, 96, 88)
GOLD = (176, 140, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DVB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DV = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(draw, text, font, max_w):
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split(" ")
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if draw.textlength(trial, font=font) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def load_art(name):
    with open(os.path.join(ART, name), "rb") as fh:
        raw = base64.b64decode(fh.read())
    return Image.open(io.BytesIO(raw)).convert("RGB")


def cover(img, w, h, fy=0.5):
    iw, ih = img.size
    target = w / h
    have = iw / ih
    if have > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        box = (x0, 0, x0 + nw, ih)
    else:
        nh = int(iw / target)
        cy = int(fy * ih)
        y0 = min(max(cy - nh // 2, 0), ih - nh)
        box = (0, y0, iw, y0 + nh)
    return img.crop(box).resize((w, h), Image.LANCZOS)


# ---------------------------------------------------------------- data

TICKER = [
    ("110+", "MISSILES AT UKRAINE, FRI"),
    ("\u22123.7%", "S&P 500, INTO CORRECTION"),
    ("7", "STRAIGHT DAILY LOSSES"),
    ("18:24", "UTC \u00b7 MERCURY BURN TONIGHT"),
    ("128", "NATIONS BACK ROBOT-RULES PATH"),
    ("1 IN 12", "TUMOURS VANISH ON PILL TRIAL"),
]

HERO = {
    "art": "01_kyiv.b64",
    "label": "KYIV \u2014 UKRAINE",
    "headline": "AFTER THE BIGGEST ATTACK",
    "deck": ("Friday: 110+ missiles, 400+ drones; 9 killed, 3 bridges "
             "hit; Ukraine hit 3 launchers; Kryvyi Rih strike kills boy, 7."),
    "strip": "110+ MISSILES \u00b7 400+ DRONES \u00b7 9 KILLED \u00b7 3 BRIDGES",
}

LEADS = [
    {
        "art": "02_markets.b64",
        "label": "MARKETS",
        "fy": 0.85,
        "headline": "S&P 500 ENTERS CORRECTION",
        "deck": ("Friday close: S&P \u22123.7% to 6,910, 7th straight loss; "
                 "Nasdaq \u22125.3%, Nikkei \u22125.1%; gold \u22124.6%, "
                 "Bitcoin ~$57,850."),
    },
    {
        "art": "03_space.b64",
        "label": "SPACE",
        "headline": "BEPICOLOMBO DUE AT MERCURY TONIGHT",
        "deck": ("Capture burn due 18:24 UTC after 8 years and 10bn km; "
                 "only the 2nd spacecraft ever to orbit Mercury; "
                 "science Apr 2027."),
    },
]

FEATURES = [
    ("04_cop31.b64", "ANTALYA",
     "COP31 RUNS PAST DEADLINE, NO DEAL",
     "Talks into the weekend; draft drops fossil fuels and the $120bn "
     "adaptation target; 3rd draft due Saturday."),
    ("05_robots.b64", "GENEVA",
     "128 NATIONS AGREE KILLER-ROBOT PATH",
     "Concluded 04:45 Sat: two more years to \u2018elaborate\u2019 rules "
     "by 2028; no binding treaty promised."),
    ("06_hack.b64", "WASHINGTON",
     "FBI AND USDA HACKED",
     "Reported Fri: intruders in the FBI crime database; USDA farmer "
     "payments hit; cyber chief fired Thu."),
    ("07_raid.b64", "SINALOA",
     "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
     "FBI Top 10 fugitive seized Fri night, announced Sat; gunfight "
     "in Guasave; 2 more leaders held."),
    ("08_tanker.b64", "HORMUZ",
     "TWO TANKERS HIT; IRAN STRIKES WEIGHED",
     "Tankers struck near the strait Sat; Trump weighs new Iran strikes; "
     "US says attack ready in 2\u20134 days."),
    ("09_pill.b64", "BARCELONA",
     "CANCER PILL: TUMOURS VANISH IN 1 IN 12",
     "Presented Fri: daraxonrasib + chemo, 61 patients; tumours stopped "
     "growing in 90%; 77% alive at one year."),
    ("10_rings.b64", "BRUSSELS",
     "EU\u2013UK: THREE DEALS AGREED FRIDAY",
     "Food checks from Mar 2028; carbon markets link; youth scheme, "
     "100,000 a year; tuition row open."),
    ("11_shadow.b64", "COPENHAGEN",
     "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Announced Fri: Moscow blamed for plot to kill rapper Kyivstoner; "
     "plot foiled 25 Sept; attach\u00e9 out in 7 days."),
    ("12_protest.b64", "ROME",
     "COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs, tuition and "
     "military spending."),
    ("13_quake.b64", "PERU",
     "M6.7 QUAKE SHAKES THE ANDES",
     "Fri 19:09 local (Sat 00:09 UTC), near Jun\u00edn; felt in Lima; "
     "no deaths, minor damage."),
]

ALSO = [
    (14, "GAZA", "Israeli fire kills Palestinians; West Bank tensions rise."),
    (15, "MADRID", "Spain heads to Nov 29 election; banking-tax extension planned."),
    (16, "BRAS\u00cdLIA", "Bolsonaro hospitalised with intestinal obstruction."),
    (17, "PORT-AU-PRINCE", "Salvadoran troops fight gangs in Haiti, lose soldiers."),
    (18, "CAPE TOWN", "Phumzile Mlambo-Ngcuka dies aged 71."),
    (19, "NIGERIA", "Boat of funeral mourners capsizes in Bayelsa."),
    (20, "BASRA", "Fire at power station kills 4."),
    (21, "PARIS", "French police sentenced over racist beating of Michel Zecler."),
    (22, "NEW YORK", "Indian man sentenced to 19 years in plot to kill Sikh leader."),
    (23, "WASHINGTON", "US loses measles elimination status."),
    (24, "KAMPALA", "Uganda restricts gatherings and travel over Ebola."),
    (25, "GENEVA", "CERN finds first evidence of ultra-rare decay."),
    (26, "SPACE", "Voyager 1 now 24 light-hours from Earth."),
    (27, "JAPAN", "Pilotless air taxi carries a passenger."),
    (28, "BUENOS AIRES", "Argentina\u2019s country risk tops 1,000 points."),
    (29, "TURKANA", "Kenya begins onshore crude drilling."),
    (30, "TOKYO", "Saudi Arabia and Japan agree oil stockpile deal."),
    (31, "TOKYO", "Japan sidelined by China as ties hit record low."),
    (32, "SAN FRANCISCO", "Anthropic mathematician claims AI-assisted Riemann proof."),
    (33, "SPORT", "Verstappen takes Las Vegas GP pole; Harden passes Kobe on 50-point games."),
    (34, "MELBOURNE", "North Melbourne reaches 4th straight AFL Women\u2019s grand final."),
    (35, "FLORIDA", "Heavy rain worsens flooding; 28 inches in Brevard County."),
]

DOTS = [
    (1, -74, 41), (2, 8, 50), (3, 31, 50), (4, 30, 37), (5, 6, 46),
    (6, -77, 39), (7, -108, 25), (8, 56, 26), (9, 2, 41), (10, 4, 51),
    (11, 12, 56), (12, 12, 42), (13, -76, -11),
]

CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 68),
     (-95, 69), (-85, 66), (-80, 73), (-70, 62), (-60, 55), (-55, 52),
     (-60, 46), (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32),
     (-81, 26), (-84, 30), (-90, 21), (-94, 17), (-97, 16), (-102, 18),
     (-105, 20), (-110, 23), (-114, 29), (-117, 33), (-122, 37),
     (-124, 42), (-124, 48), (-130, 54), (-140, 60), (-150, 61),
     (-158, 58), (-165, 60)],
    [(-79, 9), (-73, 11), (-64, 10), (-60, 8), (-53, 5), (-50, 0),
     (-44, -3), (-37, -6), (-35, -9), (-38, -15), (-40, -21), (-46, -24),
     (-52, -28), (-57, -35), (-62, -41), (-66, -47), (-69, -52),
     (-71, -54), (-73, -45), (-73, -37), (-71, -30), (-70, -20),
     (-75, -15), (-79, -8), (-81, -4)],
    [(-17, 15), (-15, 22), (-10, 31), (-5, 35), (0, 36), (8, 37),
     (11, 34), (19, 32), (25, 32), (31, 31), (35, 28), (38, 22),
     (43, 12), (48, 11), (51, 12), (47, 5), (41, -2), (39, -8),
     (36, -18), (33, -26), (28, -33), (20, -35), (16, -29), (13, -22),
     (12, -17), (10, -8), (9, 4), (2, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-4, 48), (-1, 49), (3, 51), (6, 53), (8, 57),
     (13, 56), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (32, 68), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 65), (170, 62), (162, 58),
     (158, 53), (150, 59), (142, 50), (140, 40), (134, 34), (128, 31),
     (122, 28), (120, 22), (114, 22), (109, 18), (106, 10), (104, 9),
     (101, 8), (99, 11), (97, 16), (93, 20), (90, 22), (86, 20),
     (82, 16), (80, 13), (77, 8), (74, 15), (71, 20), (67, 24),
     (62, 25), (58, 26), (54, 27), (51, 29), (48, 30), (44, 29),
     (40, 22), (39, 21), (36, 26), (34, 28), (32, 31), (30, 36),
     (27, 37), (24, 38), (22, 38), (20, 40), (18, 40), (15, 44),
     (12, 44), (9, 44), (6, 43), (3, 43), (0, 44), (-2, 44), (-3, 38),
     (-6, 36)],
    [(113, -22), (114, -28), (115, -33), (120, -34), (126, -32),
     (130, -32), (134, -33), (137, -35), (140, -38), (145, -38),
     (149, -37), (152, -32), (153, -27), (151, -24), (149, -20),
     (146, -19), (143, -15), (141, -12), (137, -12), (133, -12),
     (129, -14), (126, -14), (122, -17), (118, -20)],
]

REGION_LINES = [
    "EUROPE 10 \u00b7 AMERICAS 12 \u00b7 ASIA 3 \u00b7 AFRICA 4",
    "MIDDLE EAST 3 \u00b7 SPACE 2 \u00b7 OCEANIA 1",
]

DATE_CHECK_LEFT = (
    "NOT 21 NOV \u2014 REPORTED FRIDAY",
    "Kyiv attack; Poland breach; EU\u2013UK deals; Denmark expulsion; "
    "FBI/USDA hacks; cancer-pill presentation \u2014 all Friday 20 Nov. "
    "Denmark plot foiled 25 Sept. Peru quake Fri evening local time "
    "(Sat 00:09 UTC).",
)
DATE_CHECK_RIGHT = (
    "DUE TONIGHT \u2014 STILL OPEN",
    "BepiColombo capture burn due 18:24 UTC tonight; COP31 third draft "
    "due Saturday, no deal yet; Trump has not decided on new Iran strikes.",
)

FOOTER = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One Turn. "
          "Figures as reported on 21 Nov 2026; casualty counts were "
          "updated during the day.")


# ---------------------------------------------------------------- sections

def section_masthead(d):
    d.text((W / 2, 7),
           "THE WORLD \u2014 SATURDAY \u00b7 35 STORIES \u00b7 13 MAIN + "
           "22 ALSO \u00b7 7 REGIONS",
           font=F(SANS, 11), fill=GREY, anchor="ma")
    d.text((W / 2, 22), "SATURDAY 21 NOVEMBER 2026",
           font=F(SERIF_B, 38), fill=INK, anchor="ma")
    d.text((W / 2, 62), "One day. One page. Every region.",
           font=F(SANS, 11), fill=GREY, anchor="ma")
    d.line([(MARGIN, 77), (W - MARGIN, 77)], fill=INK, width=2)


def section_ticker(d):
    y0, y1 = 78, 126
    d.line([(MARGIN, y1), (W - MARGIN, y1)], fill=TEAL, width=2)
    bw = CW / 6.0
    for i, (fig, lab) in enumerate(TICKER):
        cx = MARGIN + bw * i + bw / 2.0
        d.text((cx, y0 + 6), fig, font=F(DVB, 20), fill=TEAL, anchor="ma")
        d.text((cx, y0 + 30), lab, font=F(SANS_B, 9), fill=GREY, anchor="ma")
        if i:
            x = MARGIN + bw * i
            d.line([(x, y0 + 6), (x, y1 - 6)], fill=SAND_DARK, width=1)


def section_hero(img, d):
    y0, y1 = 126, 298
    art = load_art(HERO["art"])
    pic = cover(art, 500, 164, fy=0.60)
    img.paste(pic, (MARGIN, y0 + 4))
    d.rectangle([MARGIN, y0 + 4, MARGIN + 500, y0 + 168], outline=INK, width=2)
    tx = 540
    d.text((tx, y0 + 8), HERO["label"], font=F(SANS_B, 12), fill=VERM)
    d.line([(tx, y0 + 28), (tx + 46, y0 + 28)], fill=VERM, width=3)
    head = F(SANS_B, 29)
    d.text((tx, y0 + 36), HERO["headline"], font=head, fill=INK)
    deck = wrap(d, HERO["deck"], F(DV, 12), 460)
    draw_lines(d, tx, y0 + 78, deck, F(DV, 12), INK, 15)
    d.line([(tx, y0 + 132), (tx + 460, y0 + 132)], fill=GOLD, width=1)
    d.text((tx, y0 + 140), HERO["strip"], font=F(SANS_B, 11),
           fill=TEAL)


def section_leads(img, d):
    y0 = 298
    card_w = (CW - 8) // 2
    for i, lead in enumerate(LEADS):
        x0 = MARGIN + i * (card_w + 8)
        d.rectangle([x0, y0, x0 + card_w, y0 + 124], fill=CARD,
                    outline=INK, width=1)
        art = load_art(lead["art"])
        pic = cover(art, card_w, 54, fy=lead.get("fy", 0.5))
        img.paste(pic, (x0 + 1, y0 + 1))
        tx = x0 + 12
        d.text((tx, y0 + 62), lead["label"], font=F(SANS_B, 10), fill=VERM)
        d.text((tx, y0 + 76), lead["headline"], font=F(SANS_B, 17), fill=INK)
        deck = wrap(d, lead["deck"], F(DV, 11), card_w - 24)
        draw_lines(d, tx, y0 + 98, deck[:2], F(DV, 11), INK, 13)


def section_features(img, d):
    y0 = 422
    col_w = (CW - 8) // 2
    for idx, (art_name, place, head, deck) in enumerate(FEATURES):
        col = idx % 2
        row = idx // 2
        x0 = MARGIN + col * (col_w + 8)
        ry = y0 + row * 38
        art = load_art(art_name)
        pic = cover(art, 64, 34)
        img.paste(pic, (x0, ry + 2))
        d.rectangle([x0, ry + 2, x0 + 64, ry + 36], outline=INK, width=1)
        tx = x0 + 72
        tw = col_w - 72
        d.text((tx, ry + 1), place + " \u2014 " + head,
               font=F(SANS_B, 12), fill=INK)
        lines = wrap(d, deck, F(DV, 10), tw)
        draw_lines(d, tx, ry + 15, lines[:2], F(DV, 10), GREY, 11)
        if row < 4:
            d.line([(x0, ry + 38), (x0 + col_w, ry + 38)],
                   fill=SAND_DARK, width=1)


def place_dots(rect):
    mx, my, mw, mh = rect
    pts = []
    for num, lon, lat in DOTS:
        x = mx + (lon + 180.0) / 360.0 * mw
        y = my + (80.0 - lat) / 135.0 * mh
        pts.append([x, y, x, y, num])
    for _ in range(120):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                d2 = dx * dx + dy * dy
                if 0.01 < d2 < 17.0 * 17.0:
                    dist = d2 ** 0.5
                    push = (17.0 - dist) / 2.0
                    ux, uy = dx / dist, dy / dist
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
        for p in pts:
            p[0] = min(max(p[0], mx + 9), mx + mw - 9)
            p[1] = min(max(p[1], my + 9), my + mh - 9)
        if not moved:
            break
    return pts


def section_map_also(img, d):
    y0, y1 = 612, 866
    d.text((MARGIN, y0 + 6), "WHERE THE NEWS IS",
           font=F(SANS_B, 12), fill=TEAL)
    d.text((366, y0 + 6), "ALSO ON SATURDAY \u2014 22 MORE",
           font=F(SANS_B, 12), fill=TEAL)
    d.line([(MARGIN, y0 + 26), (354, y0 + 26)], fill=TEAL, width=1)
    d.line([(366, y0 + 26), (W - MARGIN, y0 + 26)], fill=TEAL, width=1)
    mx, my, mw, mh = 30, y0 + 32, 318, 180
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=TEAL, width=1)
    for poly in CONTINENTS:
        pts = [(mx + (lon + 180.0) / 360.0 * mw,
                my + (80.0 - lat) / 135.0 * mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND)
    for bx, by, tx, ty, num in place_dots((mx, my, mw, mh)):
        if abs(bx - tx) > 4 or abs(by - ty) > 4:
            d.line([(tx, ty), (bx, by)], fill=INK, width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=VERM,
                  outline=(255, 255, 255), width=1)
        fnt = F(SANS_B, 9 if num < 10 else 8)
        d.text((bx, by), str(num), font=fnt, fill=(255, 255, 255),
               anchor="mm")
    cy = my + mh + 8
    for ln in REGION_LINES:
        d.text((mx + mw / 2, cy), ln, font=F(SANS_B, 9), fill=GREY,
               anchor="ma")
        cy += 13
    cols = [ALSO[0:8], ALSO[8:15], ALSO[15:22]]
    for ci, items in enumerate(cols):
        cx = 366 + ci * 214
        for size in (10, 9, 8):
            f_b = F(SANS_B, size)
            f_r = F(DV, size)
            lead = size + 2
            gap = 4
            total = 0
            laid = []
            for num, place, text in items:
                pre = "%d. " % num
                pre_w = d.textlength(pre, font=f_b)
                body = place + " \u2014 " + text
                lines = wrap(d, body, f_r, 204 - pre_w)
                laid.append((pre, lines))
                total += len(lines) * lead + gap
            if total <= y1 - (y0 + 32):
                break
        yy = y0 + 32
        for pre, lines in laid:
            f_b = F(SANS_B, size)
            f_r = F(DV, size)
            lead = size + 2
            d.text((cx, yy), pre, font=f_b, fill=VERM)
            pre_w = d.textlength(pre, font=f_b)
            draw_lines(d, cx + pre_w, yy, lines, f_r, INK, lead)
            yy += len(lines) * lead + 4


def section_datecheck(d):
    y0, y1 = 866, 958
    d.rectangle([MARGIN, y0, W - MARGIN, y1], fill=CARD, outline=VERM,
                width=2)
    mid = W // 2
    d.line([(mid, y0 + 8), (mid, y1 - 8)], fill=SAND_DARK, width=1)
    for ci, (head, text) in enumerate((DATE_CHECK_LEFT, DATE_CHECK_RIGHT)):
        x0 = MARGIN + 12 + ci * (mid - MARGIN)
        tw = mid - MARGIN - 24
        d.text((x0, y0 + 8), head, font=F(SANS_B, 12), fill=VERM)
        lines = wrap(d, text, F(DV, 11), tw)
        draw_lines(d, x0, y0 + 28, lines, F(DV, 11), INK, 14)


def section_footer(d):
    d.line([(MARGIN, 966), (W - MARGIN, 966)], fill=INK, width=1)
    lines = wrap(d, FOOTER, F(DV, 10), CW)
    draw_lines(d, MARGIN, 974, lines, F(DV, 10), GREY, 13)
    d.text((W / 2, 1006), "\u2014 THE WORLD \u00b7 SATURDAY 21 NOVEMBER 2026 \u2014",
           font=F(SANS_B, 9), fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    section_masthead(d)
    section_ticker(d)
    section_hero(img, d)
    section_leads(img, d)
    section_features(img, d)
    section_map_also(img, d)
    section_datecheck(d)
    section_footer(d)
    out_png = os.path.join(BASE, "entry.png")
    img.save(out_png, format="PNG", optimize=True)
    with open(out_png, "rb") as fh:
        raw = fh.read()
    assert len(raw) <= 1048576, "entry.png too big: %d bytes" % len(raw)
    b64 = base64.b64encode(raw).decode("ascii")
    with open(os.path.join(BASE, "entry.png.b64"), "w") as fh:
        fh.write(b64)
    digest = hashlib.sha256(raw).hexdigest()
    print("entry.png: %d bytes, sha256 %s" % (len(raw), digest))


if __name__ == "__main__":
    main()

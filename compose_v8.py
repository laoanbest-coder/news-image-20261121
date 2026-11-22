#!/usr/bin/env python3
"""Build the Saturday 21 November 2026 world-news front page.

One 1024x1024 PNG, drawn entirely in code: a dark navy masthead, a
numbers ticker, one wide markets hero, two lead cards, ten feature
rows, a light world-map panel, an ALSO list, a DATE CHECK box and a
sources footer. All words and numbers are drawn by this script; the
13 illustrations are generated pictures pasted in from art/*.b64
(no lettering in them).

Deterministic: fixed palette, fixed fonts, fixed geometry, no network,
no randomness, no timestamps. Run: python3 compose_v8.py
Writes entry.png next to this file.
"""

import base64
import io
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

NAVY = (22, 34, 64)
CREAM = (246, 239, 221)
PAPER = (250, 246, 235)
RED = (178, 58, 46)
INK = (28, 32, 48)
GREY = (104, 109, 124)
RULE = (208, 198, 172)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap_text(text, fnt, width):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def load_art(name):
    path = os.path.join(BASE, "art", name + ".b64")
    with open(path, "r") as fh:
        raw = base64.b64decode(fh.read().strip())
    return Image.open(io.BytesIO(raw)).convert("RGB")


def paste_cover(page, name, box):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    im = load_art(name)
    iw, ih = im.size
    scale = max(bw / iw, bh / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - bw) // 2
    top = (nh - bh) // 2
    page.paste(im.crop((left, top, left + bw, top + bh)), (x0, y0))


def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- data

TICKER = [
    ("−3.7%", "S&P 500 · FRIDAY CLOSE", RED),
    ("7", "STRAIGHT DAILY LOSSES", NAVY),
    ("18:24", "UTC · BEPICOLOMBO BURN", NAVY),
    ("128", "NATIONS · KILLER-ROBOT PATH", NAVY),
    ("110+", "MISSILES AT UKRAINE", NAVY),
    ("1 IN 12", "UNDETECTABLE ON PILL TRIAL", NAVY),
]

HERO = {
    "label": "MARKETS",
    "headline": "S&P 500 ENTERS CORRECTION",
    "big": "−3.7%",
    "caption": "Friday close · 7th straight loss",
    "deck": "S&P 500 fell 3.7% to 6,910 on Friday; Nasdaq −5.3%, "
            "Nikkei −5.1%; gold −4.6%, Bitcoin about $57,850.",
    "art": "01_markets",
}

LEADS = [
    {
        "label": "SPACE",
        "headline": "BEPICOLOMBO DUE AT MERCURY TONIGHT",
        "deck": "Capture burn due 18:24 UTC after 8 years and 10bn km; "
                "only the 2nd spacecraft ever to orbit Mercury; "
                "science from April 2027.",
        "art": "02_space",
    },
    {
        "label": "KYIV",
        "headline": "AFTER THE BIGGEST ATTACK",
        "deck": "Friday: 110+ missiles, 400+ drones; 9 killed, "
                "3 bridges hit; Ukraine hit 3 launchers; "
                "Kryvyi Rih strike kills boy, 7.",
        "art": "03_kyiv",
    },
]

FEATURES = [
    ("4", "ANTALYA", "COP31 RUNS PAST DEADLINE, NO DEAL",
     "Talks into the weekend; draft drops fossil fuels and the "
     "$120bn adaptation target; 3rd draft due Saturday.", "04_cop31"),
    ("5", "GENEVA", "128 NATIONS AGREE KILLER-ROBOT PATH",
     "Concluded 04:45 Saturday: two more years to 'elaborate' "
     "rules by 2028; no binding treaty promised.", "05_robots"),
    ("6", "WASHINGTON", "FBI AND USDA HACKED",
     "Reported Friday: intruders in the FBI crime database; "
     "USDA farmer payments hit; cyber chief fired Thursday.", "06_hack"),
    ("7", "SINALOA", "'EL CHAPO ISIDRO' CAPTURED",
     "FBI Top 10 fugitive seized Friday night, announced "
     "Saturday; gunfight in Guasave; 2 more leaders held.", "07_raid"),
    ("8", "HORMUZ", "TWO TANKERS HIT; IRAN STRIKES WEIGHED",
     "Tankers struck near the strait Saturday; Trump weighs new "
     "Iran strikes; US says attack ready in 2–4 days.", "08_tanker"),
    ("9", "BARCELONA", "CANCER PILL: TUMOURS VANISH IN 1 IN 12",
     "Presented Friday: daraxonrasib + chemo, 61 patients; "
     "tumours stopped growing in 90%; 77% alive at one year.", "09_pill"),
    ("10", "BRUSSELS", "EU–UK: THREE DEALS AGREED FRIDAY",
     "Food checks from March 2028; carbon markets link; "
     "youth scheme, 100,000 a year; tuition row open.", "10_rings"),
    ("11", "COPENHAGEN", "DENMARK EXPELS RUSSIAN ATTACHÉ",
     "Announced Friday: Moscow blamed for plot to kill rapper "
     "Kyivstoner; plot foiled 25 September; attaché out in 7 days.",
     "11_shadow"),
    ("12", "ROME", "COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs, "
     "tuition and military spending.", "12_protest"),
    ("13", "PERU", "M6.7 QUAKE SHAKES THE ANDES",
     "Friday 19:09 local (Saturday 00:09 UTC), near Junín; "
     "felt in Lima; no deaths, minor damage.", "13_quake"),
]

ALSO = [
    ("GAZA", "Israeli fire kills Palestinians; West Bank tensions rise."),
    ("MADRID", "Spain heads to 29 November election; banking-tax extension planned."),
    ("BRASÍLIA", "Bolsonaro hospitalised with intestinal obstruction."),
    ("PORT-AU-PRINCE", "Salvadoran troops fight gangs in Haiti, lose soldiers."),
    ("CAPE TOWN", "Phumzile Mlambo-Ngcuka dies aged 71."),
    ("NIGERIA", "Boat of funeral mourners capsizes in Bayelsa."),
    ("BASRA", "Fire at power station kills 4."),
    ("PARIS", "French police sentenced over racist beating of Michel Zecler."),
    ("NEW YORK", "Indian man sentenced to 19 years in plot to kill Sikh leader."),
    ("WASHINGTON", "US loses measles elimination status."),
    ("KAMPALA", "Uganda restricts gatherings and travel over Ebola."),
    ("GENEVA", "CERN finds first evidence of ultra-rare decay."),
    ("SPACE", "Voyager 1 now 24 light-hours from Earth."),
    ("JAPAN", "Pilotless air taxi carries a passenger."),
    ("BUENOS AIRES", "Argentina's country risk tops 1,000 points."),
    ("TURKANA", "Kenya begins onshore crude drilling."),
    ("TOKYO", "Saudi Arabia and Japan agree oil stockpile deal."),
    ("TOKYO", "Japan sidelined by China as ties hit record low."),
    ("SAN FRANCISCO", "Anthropic mathematician claims AI-assisted Riemann proof."),
    ("SPORT", "Verstappen takes Las Vegas GP pole; Harden passes Kobe on 50-point games."),
    ("MELBOURNE", "North Melbourne reaches 4th straight AFL Women's grand final."),
    ("FLORIDA", "Heavy rain worsens flooding; 28 inches in Brevard County."),
]

DATE_LEFT_HEAD = "NOT 21 NOV — REPORTED FRIDAY"
DATE_LEFT = ("Kyiv attack; Poland airspace breach; EU–UK deals; Denmark "
             "expulsion; FBI/USDA hacks; cancer-pill presentation — all "
             "Friday 20 Nov. Denmark plot foiled 25 Sept. Peru quake "
             "Friday evening local time (Saturday 00:09 UTC).")
DATE_RIGHT_HEAD = "DUE TONIGHT — STILL OPEN"
DATE_RIGHT = ("BepiColombo capture burn due 18:24 UTC tonight; COP31 "
              "third draft due Saturday, no deal yet; Trump has not "
              "decided on new Iran strikes.")

FOOTER_LINE = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One Turn. "
               "Figures as reported on 21 Nov 2026; casualty counts were "
               "updated during the day.")
FOOTER_CREDIT = "Drawn in code · Illustrations generated · No photograph used"


# ------------------------------------------------------- top sections

def masthead(draw):
    draw.rectangle([0, 0, W, 84], fill=NAVY)
    kf = font(SANS_B, 11)
    centred(draw, W / 2, 10,
            "THE WORLD  —  SATURDAY  ·  35 STORIES  ·  13 MAIN + 22 ALSO  ·  7 REGIONS",
            kf, CREAM)
    df = font(SERIF_B, 38)
    centred(draw, W / 2, 28, "SATURDAY 21 NOVEMBER 2026", df, CREAM)
    tf = font(SANS, 11)
    centred(draw, W / 2, 68, "One day. One page. Every region.", tf, CREAM)


def ticker(draw):
    draw.rectangle([0, 84, W, 122], fill=PAPER)
    draw.line([0, 122, W, 122], fill=RULE, width=1)
    cell = W // 6
    nf = font(SANS_B, 19)
    lf = font(SANS_B, 8)
    for i, (num, label, col) in enumerate(TICKER):
        x = i * cell
        if i:
            draw.line([x, 90, x, 116], fill=RULE, width=1)
        draw.text((x + 12, 89), num, font=nf, fill=col)
        draw.text((x + 12, 110), label, font=lf, fill=GREY)


def hero(page, draw):
    draw.rectangle([12, 122, 1012, 282], outline=RULE, width=1, fill=WHITE)
    paste_cover(page, HERO["art"], (700, 123, 1011, 281))
    draw.line([700, 123, 700, 281], fill=RULE, width=1)
    lf = font(SANS_B, 12)
    draw.text((28, 134), HERO["label"], font=lf, fill=RED)
    hf = font(SANS_B, 28)
    draw.text((28, 152), HERO["headline"], font=hf, fill=INK)
    bf = font(SANS_B, 46)
    draw.text((28, 192), HERO["big"], font=bf, fill=RED)
    cf = font(SANS, 11)
    draw.text((28, 244), HERO["caption"], font=cf, fill=GREY)
    df = font(SANS, 12)
    lines = wrap_text(HERO["deck"], df, 470)
    y = 196
    for line in lines:
        draw.text((210, y), line, font=df, fill=INK)
        y += 16


def leads(page, draw):
    for i, lead in enumerate(LEADS):
        x0 = 12 + i * 506
        x1 = x0 + 494
        y0, y1 = 282, 444
        draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1, fill=WHITE)
        paste_cover(page, lead["art"], (x0 + 1, y0 + 1, x0 + 133, y1 - 1))
        tx = x0 + 146
        lf = font(SANS_B, 12)
        draw.text((tx, y0 + 10), lead["label"], font=lf, fill=RED)
        hf = font(SANS_B, 16)
        y = y0 + 28
        for line in wrap_text(lead["headline"], hf, x1 - tx - 12):
            draw.text((tx, y), line, font=hf, fill=INK)
            y += 20
        df = font(SANS, 11)
        y += 4
        for line in wrap_text(lead["deck"], df, x1 - tx - 12):
            draw.text((tx, y), line, font=df, fill=INK)
            y += 15


def features(page, draw):
    y0 = 444
    row_h = 45
    hf = font(SANS_B, 11)
    df = font(SANS, 10)
    for r in range(5):
        for c in range(2):
            idx = r * 2 + c
            num, city, head, deck, art = FEATURES[idx]
            x0 = 12 + c * 506
            x1 = x0 + 494
            y = y0 + r * row_h
            paste_cover(page, art, (x0, y, x0 + 84, y + 45))
            tx = x0 + 94
            title = num + ". " + city + " — " + head
            draw.text((tx, y + 3), title, font=hf, fill=INK)
            yy = y + 20
            for line in wrap_text(deck, df, x1 - tx - 8)[:2]:
                draw.text((tx, yy), line, font=df, fill=INK)
                yy += 12
            if r < 4:
                draw.line([x0, y + 45, x1, y + 45], fill=RULE, width=1)
    draw.line([512, y0, 512, y0 + 5 * row_h], fill=RULE, width=1)


# ------------------------------------------------------------ map panel

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-85, 76),
     (-75, 72), (-65, 62), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-76, 34), (-81, 26), (-84, 30), (-90, 21), (-86, 16), (-92, 15),
     (-97, 16), (-105, 20), (-110, 24), (-115, 30), (-122, 38),
     (-125, 42), (-125, 49), (-132, 56), (-145, 60), (-158, 58),
     (-168, 62)],
    # South America
    [(-79, 9), (-70, 11), (-62, 9), (-52, 5), (-50, 0), (-44, -3),
     (-38, -6), (-35, -9), (-40, -20), (-48, -27), (-55, -34),
     (-62, -41), (-66, -47), (-70, -54), (-73, -50), (-73, -37),
     (-72, -20), (-77, -12), (-81, -4), (-80, 2)],
    # Europe
    [(-11, 43), (-9, 37), (-3, 36), (0, 39), (3, 43), (7, 44), (12, 45),
     (15, 44), (19, 42), (23, 40), (26, 40), (29, 41), (28, 45),
     (24, 45), (28, 44), (23, 44), (19, 46), (22, 48), (24, 50),
     (20, 54), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (26, 64), (22, 65), (18, 69), (14, 67), (10, 64), (6, 62),
     (5, 60), (2, 58), (-2, 57), (-6, 53), (-10, 54), (-11, 49),
     (-10, 46)],
    # Africa
    [(-17, 15), (-16, 21), (-15, 27), (-10, 31), (-6, 33), (-1, 35),
     (5, 37), (10, 37), (11, 34), (16, 32), (22, 33), (30, 31),
     (34, 28), (38, 22), (42, 15), (44, 11), (48, 11), (51, 12),
     (48, 5), (42, 0), (40, -6), (38, -12), (35, -18), (33, -25),
     (29, -32), (25, -34), (19, -35), (16, -29), (14, -22), (13, -12),
     (12, -6), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-16, 11)],
    # Asia
    [(30, 36), (35, 36), (40, 39), (44, 39), (48, 38), (52, 38),
     (55, 37), (58, 38), (60, 36), (62, 33), (60, 30), (57, 27),
     (54, 27), (52, 28), (55, 29), (58, 26), (61, 25), (65, 25),
     (68, 24), (70, 22), (72, 20), (75, 15), (77, 8), (80, 10),
     (80, 15), (84, 19), (88, 22), (91, 22), (94, 18), (96, 16),
     (98, 12), (100, 8), (102, 5), (104, 2), (103, 8), (105, 10),
     (107, 12), (109, 15), (107, 19), (109, 21), (113, 22), (117, 24),
     (120, 28), (121, 32), (120, 37), (122, 39), (126, 40), (130, 42),
     (132, 43), (135, 44), (138, 46), (141, 48), (142, 52), (141, 57),
     (138, 59), (136, 55), (133, 52), (130, 48), (128, 45), (127, 41),
     (126, 38), (122, 37), (119, 34), (115, 32), (110, 30), (105, 28),
     (100, 26), (95, 25), (90, 22), (86, 20), (82, 17), (79, 14),
     (76, 10), (73, 18), (70, 22), (67, 25), (63, 25), (58, 26),
     (54, 27), (51, 29), (48, 30), (45, 32), (42, 34), (38, 36),
     (34, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34),
     (126, -32), (129, -32), (132, -32), (135, -35), (138, -35),
     (140, -38), (144, -38), (147, -39), (150, -37), (153, -32),
     (153, -27), (151, -24), (148, -20), (146, -19), (142, -11),
     (141, -14), (139, -17), (136, -15), (135, -12), (132, -12),
     (130, -13), (127, -14), (124, -15), (121, -17), (117, -20),
     (114, -22)],
    # Greenland
    [(-44, 60), (-40, 64), (-34, 66), (-30, 68), (-25, 70), (-21, 72),
     (-26, 75), (-34, 76), (-44, 75), (-52, 74), (-56, 71), (-55, 66),
     (-50, 61)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
     (1, 51), (-2, 50)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 34), (138, 35), (140, 36),
     (140, 39), (141, 41), (143, 43), (145, 44), (142, 44), (141, 41),
     (140, 38), (138, 36), (136, 35), (134, 34), (132, 33)],
    # Indonesia
    [(95, 5), (98, 3), (100, 0), (103, -3), (106, -6), (110, -7),
     (114, -8), (118, -9), (122, -10), (126, -9), (130, -6), (134, -4),
     (138, -6), (141, -8), (138, -8), (132, -6), (126, -4), (120, -3),
     (114, -2), (108, -4), (102, -1), (98, 3)],
]

# (number, lon, lat, leader offset or None)
DOTS = [
    (1, -74, 41, (16, -12)),
    (2, 8, 50, (28, -14)),
    (3, 31, 50, None),
    (4, 30, 37, (26, 14)),
    (5, 6, 46, (34, 4)),
    (6, -77, 39, (-16, 12)),
    (7, -108, 25, None),
    (8, 56, 26, None),
    (9, 2, 41, (-30, -2)),
    (10, 4, 51, (28, 20)),
    (11, 12, 56, (-28, -16)),
    (12, 12, 42, (-28, 12)),
    (13, -76, -11, None),
]

REGION_COUNTS = ("EUROPE 10 · AMERICAS 12 · ASIA 3 · AFRICA 4 · "
                 "MIDDLE EAST 3 · SPACE 2 · OCEANIA 1")


def project(lon, lat):
    x = 16 + (lon + 180.0) / 360.0 * 992.0
    y = 694 + (72.0 - lat) / 128.0 * 98.0
    return (x, y)


def world_map(draw):
    draw.rectangle([12, 669, 1012, 807], outline=RULE, width=1, fill=WHITE)
    hf = font(SANS_B, 11)
    draw.text((20, 674), "WHERE THE NEWS IS — 13 MAIN STORIES",
              font=hf, fill=NAVY)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=NAVY)
    nf = font(SANS_B, 8)
    for num, lon, lat, off in DOTS:
        cx, cy = project(lon, lat)
        if off is None:
            bx, by = cx, cy
        else:
            bx, by = cx + off[0], cy + off[1]
            draw.line([cx, cy, bx, by], fill=GREY, width=1)
            draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        draw.ellipse([bx - 7, by - 7, bx + 7, by + 7],
                     fill=RED, outline=WHITE, width=1)
        label = str(num)
        draw.text((bx - nf.getlength(label) / 2, by - 4),
                  label, font=nf, fill=WHITE)
    cf = font(SANS_B, 9)
    centred(draw, W / 2, 796, REGION_COUNTS, cf, GREY)


# ------------------------------------------------- also / check / footer

def also_section(draw):
    hf = font(SANS_B, 11)
    draw.text((16, 811), "ALSO ON SATURDAY", font=hf, fill=RED)
    draw.line([16, 825, 1008, 825], fill=RULE, width=1)
    bf = font(SANS_B, 8)
    tf = font(SANS, 8)
    for i, (city, text) in enumerate(ALSO):
        col = 0 if i < 11 else 1
        row = i % 11
        x = 16 + col * 500
        y = 829 + row * 9
        head = city + " — "
        draw.text((x, y), head, font=bf, fill=NAVY)
        draw.text((x + bf.getlength(head), y), text, font=tf, fill=INK)


def date_check(draw):
    draw.rectangle([12, 931, 1012, 991], outline=RED, width=2, fill=WHITE)
    draw.line([506, 935, 506, 987], fill=RULE, width=1)
    hf = font(SANS_B, 11)
    draw.text((24, 938), DATE_LEFT_HEAD, font=hf, fill=RED)
    draw.text((520, 938), DATE_RIGHT_HEAD, font=hf, fill=RED)
    tf = font(SANS, 10)
    y = 954
    for line in wrap_text(DATE_LEFT, tf, 480):
        draw.text((24, y), line, font=tf, fill=INK)
        y += 12
    y = 954
    for line in wrap_text(DATE_RIGHT, tf, 480):
        draw.text((520, y), line, font=tf, fill=INK)
        y += 12


def footer(draw):
    ff = font(SANS, 9)
    centred(draw, W / 2, 1000, FOOTER_LINE, ff, GREY)
    cf = font(SANS, 8)
    centred(draw, W / 2, 1013, FOOTER_CREDIT, cf, GREY)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    masthead(draw)
    ticker(draw)
    hero(page, draw)
    leads(page, draw)
    features(page, draw)
    world_map(draw)
    also_section(draw)
    date_check(draw)
    footer(draw)
    out = os.path.join(BASE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

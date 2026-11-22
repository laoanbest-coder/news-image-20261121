#!/usr/bin/env python3
"""compose_v10.py — build the 21 Nov 2026 world-news front page (1024x1024).

Reads the 13 linocut illustrations from art/*.b64 (single-line base64),
draws a newspaper front page, and writes entry.png + entry.png.b64
(single-line base64) next to this script. Pillow + stdlib only.
Deterministic: no timestamps, no randomness, no network.
"""

import base64
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

NAVY = (27, 42, 74)
NAVY_DARK = (18, 30, 56)
CREAM = (245, 237, 220)
PAPER = (250, 246, 236)
RED = (176, 58, 46)
RED_DARK = (150, 45, 35)
INK = (30, 36, 48)
GREY = (90, 96, 112)
RULE = (200, 192, 172)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif and bold else \
        "DejaVuSerif.ttf" if serif else \
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=fnt, fill=fill)
    return y + len(lines) * lh


def load_art(name, tw, th):
    """Load art/<name>.b64, cover-crop/resize to (tw, th)."""
    with open(os.path.join(HERE, "art", name + ".b64")) as fh:
        raw = base64.b64decode(fh.read().strip())
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    sw, sh = im.size
    target = tw / th
    if sw / sh > target:  # too wide: crop sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, sh))
    else:  # too tall: crop top/bottom
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        im = im.crop((0, y0, sw, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)


# ---------------------------------------------------------------- data
TICKER = [
    ("-3.7%", "S&P 500 \u00b7 FRIDAY CLOSE"),
    ("7", "STRAIGHT DAILY LOSSES \u00b7 S&P"),
    ("18:24", "UTC \u00b7 BEPICOLOMBO BURN TONIGHT"),
    ("128", "COUNTRIES AGREE KILLER-ROBOT PATH"),
    ("110+", "MISSILES FIRED AT UKRAINE FRI"),
    ("1 IN 12", "CANCER PATIENTS UNDETECTABLE"),
]

HERO = {
    "label": "MARKETS",
    "label2": " \u2014 FRIDAY CLOSE",
    "big": "-3.7%",
    "headline": "S&P 500 ENTERS CORRECTION",
    "deck": "Friday close: S&P -3.7% to 6,910, 7th straight loss; "
            "Nasdaq -5.3%, Nikkei -5.1%; gold -4.6%, Bitcoin ~$57,850.",
    "art": "01_markets",
}

LEADS = [
    {"label": "KYIV", "headline": "AFTER THE BIGGEST ATTACK",
     "deck": "Friday: 110+ missiles, 400+ drones; 9 killed, 3 bridges hit; "
             "Ukraine hit 3 launchers; Kryvyi Rih strike kills boy, 7.",
     "art": "03_kyiv"},
    {"label": "SPACE", "headline": "BEPICOLOMBO DUE AT MERCURY TONIGHT",
     "deck": "Capture burn due 18:24 UTC after 8 years and 10bn km; only the "
             "2nd spacecraft ever to orbit Mercury; science Apr 2027.",
     "art": "02_space"},
]

FEATURES = [
    ("COP31", "COP31 RUNS PAST DEADLINE, NO DEAL",
     "Talks into the weekend; draft drops fossil fuels and the $120bn "
     "adaptation target; 3rd draft due Saturday.", "04_cop31"),
    ("GENEVA", "128 NATIONS AGREE KILLER-ROBOT PATH",
     "Concluded 04:45 Sat: two more years to \u2018elaborate\u2019 rules by "
     "2028; no binding treaty promised.", "05_robots"),
    ("WASHINGTON", "FBI AND USDA HACKED",
     "Reported Fri: intruders in the FBI crime database; USDA farmer "
     "payments hit; cyber chief fired Thu.", "06_hack"),
    ("SINALOA", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
     "FBI Top 10 fugitive seized Fri night, announced Sat; gunfight in "
     "Guasave; 2 more leaders held.", "07_raid"),
    ("HORMUZ", "TWO TANKERS HIT; IRAN STRIKES WEIGHED",
     "Tankers struck near the strait Sat; Trump weighs new Iran strikes; "
     "US says attack ready in 2\u20134 days.", "08_tanker"),
    ("BARCELONA", "CANCER PILL: TUMOURS VANISH IN 1 IN 12",
     "Presented Fri: daraxonrasib + chemo, 61 patients; tumours stopped "
     "growing in 90%; 77% alive at one year.", "09_pill"),
    ("BRUSSELS", "EU\u2013UK: THREE DEALS AGREED FRIDAY",
     "Food checks from Mar 2028; carbon markets link; youth scheme, "
     "100,000 a year; tuition row open.", "10_rings"),
    ("COPENHAGEN", "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Announced Fri: Moscow blamed for plot to kill rapper Kyivstoner; "
     "plot foiled 25 Sept; attach\u00e9 out in 7 days.", "11_shadow"),
    ("ROME", "COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs, tuition and "
     "military spending.", "12_protest"),
    ("PERU", "M6.7 QUAKE SHAKES THE ANDES",
     "Fri 19:09 local (Sat 00:09 UTC), near Jun\u00edn; felt in Lima; "
     "no deaths, minor damage.", "13_quake"),
]

ALSO = [
    "GAZA \u2014 Israeli fire kills Palestinians.",
    "MADRID \u2014 Spain heads to Nov 29 election.",
    "BRAS\u00cdLIA \u2014 Bolsonaro hospitalised.",
    "PORT-AU-PRINCE \u2014 Salvadoran troops fight gangs.",
    "CAPE TOWN \u2014 Mlambo-Ngcuka dies aged 71.",
    "NIGERIA \u2014 Funeral boat capsizes in Bayelsa.",
    "BASRA \u2014 Power station fire kills 4.",
    "PARIS \u2014 Police sentenced over Zecler beating.",
    "NEW YORK \u2014 19 years in plot to kill Sikh leader.",
    "WASHINGTON \u2014 US loses measles elimination status.",
    "KAMPALA \u2014 Uganda restricts travel over Ebola.",
    "GENEVA \u2014 CERN finds ultra-rare decay evidence.",
    "SPACE \u2014 Voyager 1 now 24 light-hours away.",
    "JAPAN \u2014 Pilotless air taxi carries passenger.",
    "BUENOS AIRES \u2014 Country risk tops 1,000 points.",
    "TURKANA \u2014 Kenya begins onshore oil drilling.",
    "TOKYO \u2014 Saudi, Japan agree oil stockpile deal.",
    "TOKYO \u2014 Japan sidelined as China ties hit low.",
    "SAN FRANCISCO \u2014 AI-assisted Riemann proof claim.",
    "SPORT \u2014 Verstappen takes Las Vegas GP pole.",
    "MELBOURNE \u2014 North Melbourne into 4th AFLW final.",
    "FLORIDA \u2014 Heavy rain worsens flooding.",
]

# (number, lon, lat, badge offset dx, dy or None for badge-on-dot)
DOTS = [
    (1, -74, 41, None),
    (2, 8, 50, (-28, -14)),
    (3, 31, 50, None),
    (4, 30, 37, None),
    (5, 6, 46, (-30, 6)),
    (6, -77, 39, (-16, 16)),
    (7, -108, 25, None),
    (8, 56, 26, None),
    (9, 2, 41, (-8, 18)),
    (10, 4, 51, (0, -20)),
    (11, 12, 56, (20, -12)),
    (12, 12, 42, (18, 14)),
    (13, -76, -11, None),
]

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 68), (-125, 71), (-115, 72), (-100, 73),
     (-90, 74), (-80, 73), (-70, 70), (-60, 62), (-55, 52), (-60, 47),
     (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-97, 16),
     (-94, 17), (-90, 14), (-83, 9), (-79, 9), (-83, 15), (-90, 14),
     (-95, 16), (-100, 20), (-105, 23), (-110, 28), (-115, 32), (-120, 38),
     (-124, 44), (-124, 49), (-130, 55), (-140, 60), (-150, 61),
     (-160, 58), (-168, 66)],
    # South America
    [(-79, 9), (-77, 4), (-75, 0), (-72, -4), (-70, -8), (-75, -15),
     (-70, -18), (-65, -25), (-60, -32), (-65, -40), (-68, -50),
     (-70, -55), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
     (-78, -10), (-80, -5), (-81, 0), (-80, 5)],
    # Europe
    [(-10, 36), (-9, 43), (-5, 48), (-1, 50), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (25, 59), (28, 62), (24, 66), (20, 70), (15, 69),
     (10, 62), (5, 60), (-3, 58), (-8, 53), (-10, 48), (-10, 40)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 28), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (38, 22),
     (40, 15), (43, 11), (48, 11), (51, 10), (46, 5), (42, 0),
     (40, -5), (38, -12), (35, -18), (32, -26), (28, -32), (20, -35),
     (16, -30), (14, -22), (12, -15), (13, -10), (12, -5), (9, 0),
     (8, 4), (4, 6), (-2, 5), (-8, 4), (-13, 8), (-17, 12)],
    # Asia
    [(30, 36), (35, 36), (40, 38), (44, 39), (48, 38), (50, 37),
     (53, 36), (56, 30), (57, 26), (60, 25), (62, 25), (66, 25),
     (70, 20), (72, 20), (76, 15), (80, 10), (80, 7), (85, 15),
     (88, 22), (92, 21), (95, 16), (98, 12), (100, 8), (103, 5),
     (104, 2), (103, -2), (106, -6), (110, -7), (114, -10), (118, -12),
     (122, -14), (126, -12), (130, -8), (132, -5), (135, 0), (138, 2),
     (140, 5), (141, 10), (140, 15), (139, 20), (137, 25), (135, 30),
     (132, 33), (130, 35), (127, 37), (126, 40), (128, 42), (130, 45),
     (132, 48), (135, 50), (138, 52), (140, 55), (142, 58), (145, 60),
     (150, 60), (155, 60), (158, 55), (160, 58), (162, 60), (165, 62),
     (170, 66), (175, 65), (178, 64), (175, 62), (170, 60), (165, 58),
     (160, 55), (155, 52), (150, 48), (145, 45), (142, 42), (140, 38),
     (138, 35), (135, 34), (130, 32), (126, 30), (122, 30), (120, 28),
     (118, 25), (114, 22), (110, 20), (108, 18), (105, 15), (102, 12),
     (100, 10), (97, 12), (95, 15), (92, 18), (90, 22), (88, 22),
     (85, 20), (82, 18), (80, 15), (78, 12), (76, 10), (74, 12),
     (72, 18), (70, 22), (68, 25), (65, 25), (62, 25), (60, 25),
     (57, 26), (54, 28), (52, 30), (50, 32), (48, 35), (45, 38),
     (42, 40), (40, 38), (36, 36), (33, 36), (30, 36)],
    # Australia
    [(113, -22), (113, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
     (114, -21)],
]

DATE_LEFT_HEAD = "NOT 21 NOV \u2014 REPORTED FRIDAY"
DATE_LEFT = ("Kyiv attack; Poland breach; EU\u2013UK deals; Denmark "
             "expulsion; FBI/USDA hacks; cancer pill \u2014 all Fri 20 Nov. "
             "Peru quake Fri evening local.")
DATE_RIGHT_HEAD = "DUE TONIGHT \u2014 STILL OPEN"
DATE_RIGHT = ("BepiColombo burn due 18:24 UTC tonight; COP31 3rd draft due "
              "Sat, no deal yet; Trump undecided on Iran strikes.")

FOOTER = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One Turn.  "
          "Figures as reported on 21 Nov 2026; casualty counts were "
          "updated during the day.")
REGION_LINE = ("EUROPE 10 \u00b7 AMERICAS 12 \u00b7 ASIA 3 \u00b7 AFRICA 4 "
               "\u00b7 MIDDLE EAST 3 \u00b7 SPACE 2 \u00b7 OCEANIA 1")


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead (0-92)
    d.rectangle([0, 0, W, 92], fill=NAVY)
    f_kick = font(12, bold=True)
    kick = "THE WORLD  \u00b7  SATURDAY  \u00b7  35 STORIES  \u00b7  13 MAIN + 22 ALSO  \u00b7  7 REGIONS"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 10), kick,
           font=f_kick, fill=CREAM)
    f_date = font(40, bold=True, serif=True)
    date_s = "SATURDAY 21 NOVEMBER 2026"
    d.text(((W - d.textlength(date_s, font=f_date)) / 2, 28), date_s,
           font=f_date, fill=CREAM)
    f_tag = font(12)
    tag = "One day. One page. Every region."
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 74), tag,
           font=f_tag, fill=CREAM)
    d.rectangle([0, 92, W, 95], fill=RED)

    # ---- ticker (95-150)
    f_num = font(24, bold=True)
    f_lab = font(9, bold=True)
    box_w = W / 6
    for i, (num, lab) in enumerate(TICKER):
        cx = box_w * i + box_w / 2
        fill = RED if i == 0 else NAVY
        d.text((cx - d.textlength(num, font=f_num) / 2, 100), num,
               font=f_num, fill=fill)
        for j, line in enumerate(wrap(d, lab, f_lab, box_w - 14)):
            d.text((cx - d.textlength(line, font=f_lab) / 2, 130 + j * 11),
                   line, font=f_lab, fill=GREY)
        if i:
            d.line([box_w * i, 102, box_w * i, 144], fill=RULE, width=1)
    d.line([0, 151, W, 151], fill=NAVY, width=1)

    # ---- hero lead (154-400): Markets, giant -3.7%
    hero_img = load_art(HERO["art"], 400, 246)
    page.paste(hero_img, (0, 154))
    tx, tw = 420, 584
    f_hlab = font(16, bold=True)
    d.text((tx, 166), HERO["label"], font=f_hlab, fill=RED)
    d.text((tx + d.textlength(HERO["label"], font=f_hlab), 166),
           HERO["label2"], font=font(16), fill=NAVY)
    f_big = font(100, bold=True)
    d.text((tx - 4, 186), HERO["big"], font=f_big, fill=RED)
    f_hhead = font(30, bold=True)
    d.text((tx, 296), HERO["headline"], font=f_hhead, fill=NAVY)
    draw_wrapped(d, HERO["deck"], font(14), tx, 334, tw, INK, leading=19)
    d.line([0, 402, W, 402], fill=NAVY, width=1)

    # ---- two lead cards (408-540)
    f_llab = font(13, bold=True)
    f_lhead = font(19, bold=True)
    for ci, lead in enumerate(LEADS):
        x0 = 0 if ci == 0 else 516
        thumb = load_art(lead["art"], 160, 132)
        page.paste(thumb, (x0, 408))
        lx = x0 + 172
        lw = (508 if ci == 0 else 508) - 172
        d.text((lx, 412), lead["label"], font=f_llab, fill=RED)
        y = draw_wrapped(d, lead["headline"], f_lhead, lx, 432, lw, NAVY,
                         leading=22)
        draw_wrapped(d, lead["deck"], font(12), lx, y + 2, lw, INK,
                     leading=15)
        if ci == 0:
            d.line([512, 410, 512, 538], fill=RULE, width=1)
    d.line([0, 542, W, 542], fill=NAVY, width=1)

    # ---- ten feature rows (546-782): 5 rows x 2 cols
    f_fhead = font(14, bold=True)
    for ri in range(5):
        y0 = 546 + ri * 47
        for ci in range(2):
            idx = ri + ci * 5
            label, head, deck, art = FEATURES[idx]
            x0 = 0 if ci == 0 else 512
            thumb = load_art(art, 70, 47)
            page.paste(thumb, (x0, y0))
            fx = x0 + 80
            fw = 512 - 80 - 8
            head1 = head
            if d.textlength(head1, font=f_fhead) > fw:
                while d.textlength(head1 + "\u2026", font=f_fhead) > fw:
                    head1 = head1[:-1]
                head1 += "\u2026"
            d.text((fx, y0 + 2), head1, font=f_fhead, fill=NAVY)
            draw_wrapped(d, deck, font(11), fx, y0 + 20, fw, INK,
                         leading=13)
            if ci == 0:
                d.line([508, y0 + 3, 508, y0 + 44], fill=RULE, width=1)
        if ri < 4:
            d.line([0, y0 + 47, W, y0 + 47], fill=RULE, width=1)
    d.line([0, 784, W, 784], fill=NAVY, width=1)

    # ---- map panel (788-928, left) + ALSO (right)
    f_sec = font(11, bold=True)
    d.text((0, 790), "WHERE IT HAPPENED \u00b7 13 MAIN STORIES",
           font=f_sec, fill=NAVY)
    mx0, my0, mx1, my1 = 6, 808, 492, 892

    def proj(lon, lat):
        x = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        y = my0 + (85 - lat) / 145.0 * (my1 - my0)
        return x, y

    d.rectangle([mx0, my0, mx1, my1], fill=WHITE, outline=RULE)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=NAVY)
    f_dot = font(9, bold=True)
    for num, lon, lat, off in DOTS:
        px, py = proj(lon, lat)
        if off is None:
            bx, by = px, py
        else:
            bx, by = px + off[0], py + off[1]
            d.line([px, py, bx, by], fill=NAVY, width=1)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                  outline=WHITE, width=1)
        s = str(num)
        d.text((bx - d.textlength(s, font=f_dot) / 2, by - 5), s,
               font=f_dot, fill=WHITE)
    f_reg = font(10, bold=True)
    d.text(((mx0 + mx1 - d.textlength(REGION_LINE, font=f_reg)) / 2, 900),
           REGION_LINE, font=f_reg, fill=NAVY)

    ax = 508
    d.text((ax, 790), "ALSO ON SATURDAY \u00b7 22 MORE", font=f_sec, fill=NAVY)
    f_also = font(10)
    f_city = font(10, bold=True)
    col_w = 252
    for i, item in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = ax + col * (col_w + 4)
        y = 808 + row * 11
        city, _, rest = item.partition(" \u2014 ")
        d.text((x, y), city, font=f_city, fill=NAVY)
        rest_txt = "\u2014 " + rest
        avail = col_w - d.textlength(city, font=f_city) - 3
        while rest_txt and d.textlength(rest_txt + "\u2026",
                                       font=f_also) > avail:
            rest_txt = rest_txt[:-1]
        if rest_txt != "\u2014 " + rest:
            rest_txt += "\u2026"
        d.text((x + d.textlength(city, font=f_city) + 3, y),
               rest_txt, font=f_also, fill=INK)
    d.line([504, 790, 504, 926], fill=RULE, width=1)
    d.line([0, 930, W, 930], fill=NAVY, width=1)

    # ---- DATE CHECK (934-984)
    d.rectangle([0, 934, W - 1, 984], outline=RED, width=2)
    f_dh = font(12, bold=True)
    d.text((12, 940), DATE_LEFT_HEAD, font=f_dh, fill=RED)
    draw_wrapped(d, DATE_LEFT, font(11), 12, 956, 470, INK, leading=13)
    d.line([506, 940, 506, 978], fill=RULE, width=1)
    d.text((524, 940), DATE_RIGHT_HEAD, font=f_dh, fill=RED)
    draw_wrapped(d, DATE_RIGHT, font(11), 524, 956, 470, INK, leading=13)

    # ---- footer (990-1024)
    f_ft = font(10)
    for j, line in enumerate(wrap(d, FOOTER, f_ft, W - 40)):
        d.text(((W - d.textlength(line, font=f_ft)) / 2, 992 + j * 13),
               line, font=f_ft, fill=GREY)

    out_png = os.path.join(HERE, "entry.png")
    page.save(out_png, "PNG", optimize=True)
    with open(out_png, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    with open(os.path.join(HERE, "entry.png.b64"), "w") as fh:
        fh.write(b64)
    size = os.path.getsize(out_png)
    print("entry.png: %d bytes" % size)
    return size


if __name__ == "__main__":
    size = build()
    if size > 1024 * 1024:
        print("ERROR: entry.png over 1 MiB", file=sys.stderr)
        sys.exit(1)

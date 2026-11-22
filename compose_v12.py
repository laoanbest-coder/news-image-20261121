#!/usr/bin/env python3
"""v12: Saturday 21 November 2026 world news in one image.

A warm broadsheet front page, 1024x1024: cream paper, navy serif
masthead with a double rule, brick-red ticker bar, Markets hero lead,
two lead cards, ten feature rows, a dark-navy map panel with cream
continents, a DATE CHECK box and a sources footer. All 35 stories,
numbers and dates follow the verified facts in v6-plan.md.
Deterministic: same inputs, same bytes out.
"""
import base64
import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---- palette: warm paper, navy ink, brick red ----
CREAM = (246, 238, 220)
CREAM_PANEL = (243, 233, 210)
NAVY = (27, 42, 74)
NAVY_SOFT = (52, 70, 110)
RED = (169, 50, 38)
RED_DARK = (138, 38, 28)
INK = (32, 30, 26)
GRAY = (96, 88, 72)
RULE = (206, 190, 160)
CARD_LINE = (216, 201, 168)
MAP_CREAM = (246, 238, 220)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FALLBACK_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FALLBACK_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FALLBACK_SB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FALLBACK_SR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size, fallbacks=()):
    for cand in (path,) + tuple(fallbacks):
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def serif_b(size):
    return font(SERIF_B, size, (FALLBACK_B,))


def serif_r(size):
    return font(SERIF_R, size, (FALLBACK_R,))


def serif_i(size):
    return font(SERIF_I, size, (FALLBACK_R,))


def sans_b(size):
    return font(SANS_B, size, (FALLBACK_SB,))


def sans_r(size):
    return font(SANS_R, size, (FALLBACK_SR,))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
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
    """Truncate with an ellipsis so the text fits max_w."""
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap to max_lines lines, truncating the last one if needed."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    out[-1] = trunc(draw, out[-1], fnt, max_w)
    return out


def load_art(name, w, h):
    """Decode art/<name>.b64, centre-crop to w:h, resize. Sepia
    placeholder block if the file is missing (never happens in the
    final build, where all 13 files are present)."""
    path = os.path.join(HERE, "art", name + ".b64")
    try:
        raw = base64.b64decode(open(path).read().strip())
        im = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        im = Image.new("RGB", (w, h), (201, 169, 106))
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:  # too wide: trim sides
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:  # too tall: trim top/bottom
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


# ---- the 13 main stories (verified facts, v6-plan.md) ----
# (number, label, headline, deck, art file, lon, lat)
LEADS = [
    (1, "MARKETS", "S&P 500 ENTERS CORRECTION",
     "Friday close: S&P -3.7% to 6,910, 7th straight loss; "
     "Nasdaq -5.3%, Nikkei -5.1%; gold -4.6%, Bitcoin ~$57,850.",
     "01_markets", -74, 41),
    (2, "SPACE", "BEPICOLOMBO DUE AT MERCURY TONIGHT",
     "Capture burn due 18:24 UTC after 8 years and 10bn km; only "
     "the 2nd spacecraft ever to orbit Mercury; science Apr 2027.",
     "02_space", 8, 50),
    (3, "KYIV", "AFTER THE BIGGEST ATTACK",
     "Friday: 110+ missiles, 400+ drones; 9 killed, 3 bridges hit; "
     "Ukraine hit 3 launchers; Kryvyi Rih strike kills boy, 7.",
     "03_kyiv", 31, 50),
]
FEATURES = [
    (4, "ANTALYA", "COP31 RUNS PAST DEADLINE, NO DEAL",
     "Talks into the weekend; draft drops fossil fuels and the "
     "$120bn adaptation target; 3rd draft due Saturday.",
     "04_cop31", 30, 37),
    (5, "GENEVA", "128 NATIONS AGREE KILLER-ROBOT PATH",
     "Concluded 04:45 Sat: two more years to 'elaborate' rules "
     "by 2028; no binding treaty promised.",
     "05_robots", 6, 46),
    (6, "WASHINGTON", "FBI AND USDA HACKED",
     "Reported Fri: intruders in the FBI crime database; USDA "
     "farmer payments hit; cyber chief fired Thu.",
     "06_hack", -77, 39),
    (7, "SINALOA", "'EL CHAPO ISIDRO' CAPTURED",
     "FBI Top 10 fugitive seized Fri night, announced Sat; "
     "gunfight in Guasave; 2 more leaders held.",
     "07_raid", -108, 25),
    (8, "HORMUZ", "TWO TANKERS HIT; IRAN STRIKES WEIGHED",
     "Tankers struck near the strait Sat; Trump weighs new Iran "
     "strikes; US says attack ready in 2–4 days.",
     "08_tanker", 56, 26),
    (9, "BARCELONA", "CANCER PILL: TUMOURS VANISH IN 1 IN 12",
     "Presented Fri: daraxonrasib + chemo, 61 patients; tumours "
     "stopped growing in 90%; 77% alive at one year.",
     "09_pill", 2, 41),
    (10, "BRUSSELS", "EU–UK: THREE DEALS AGREED FRIDAY",
     "Food checks from Mar 2028; carbon markets link; youth "
     "scheme, 100,000 a year; tuition row open.",
     "10_rings", 4, 51),
    (11, "COPENHAGEN", "DENMARK EXPELS RUSSIAN ATTACHÉ",
     "Announced Fri: Moscow blamed for plot to kill rapper "
     "Kyivstoner; plot foiled 25 Sept; attaché out in 7 days.",
     "11_shadow", 12, 56),
    (12, "ROME", "COST-OF-LIVING PROTESTS SPREAD",
     "Students in 25 countries walk out over living costs, "
     "tuition and military spending.",
     "12_protest", 12, 42),
    (13, "PERU", "M6.7 QUAKE SHAKES THE ANDES",
     "Fri 19:09 local (Sat 00:09 UTC), near Junín; felt in Lima; "
     "no deaths, minor damage.",
     "13_quake", -76, -11),
]
MAIN = LEADS + FEATURES

ALSO = [
    ("GAZA", "Israeli fire kills Palestinians; West Bank tensions rise."),
    ("MADRID", "Spain heads to Nov 29 election; banking-tax extension planned."),
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

TICKER = [
    "-3.7% S&P 500 FRI",
    "7 STRAIGHT LOSSES",
    "18:24 UTC BEPICOLOMBO",
    "128 NATIONS ROBOT RULES",
    "110+ MISSILES",
    "1 IN 12 CANCER PILL",
]

DATE_LEFT_HEAD = "NOT 21 NOV — REPORTED FRIDAY"
DATE_LEFT = ("Kyiv attack; Poland breach; EU–UK deals; Denmark expulsion; "
             "FBI/USDA hacks; cancer-pill presentation — all Friday 20 Nov. "
             "Denmark plot foiled 25 Sept. Peru quake Fri evening "
             "(Sat 00:09 UTC).")
DATE_RIGHT_HEAD = "DUE TONIGHT — STILL OPEN"
DATE_RIGHT = ("BepiColombo capture burn due 18:24 UTC tonight; COP31 third "
              "draft due Saturday, no deal yet; Trump has not decided on "
              "new Iran strikes.")
FOOTER = ("Sources: Reuters, AP, CNN, BBC, NYT, FT, USGS, ESA, One Turn. "
          "Figures as reported on 21 Nov 2026; casualty counts were "
          "updated during the day.")
REGION_COUNTS = ("EUROPE 10  •  AMERICAS 12  •  ASIA 3  •  AFRICA 4  •  "
                 "MIDDLE EAST 3  •  SPACE 2  •  OCEANIA 1")

# Simplified continent outlines (lon, lat), drawn cream on navy.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 72), (-65, 62), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 24), (-115, 30), (-125, 40), (-125, 48), (-135, 58),
     (-155, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 74)],
    # South America
    [(-80, 10), (-75, 5), (-65, 0), (-55, -5), (-45, -10), (-40, -20),
     (-50, -30), (-60, -35), (-70, -40), (-73, -50), (-70, -55),
     (-75, -45), (-80, -30), (-80, -20), (-80, -10), (-82, 0)],
    # Africa
    [(-18, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (13, -5),
     (10, 0), (5, 5), (-5, 5), (-10, 8), (-17, 12)],
    # Europe
    [(-10, 36), (-5, 38), (0, 39), (5, 38), (10, 38), (12, 44),
     (18, 40), (20, 45), (25, 40), (28, 41), (30, 36), (28, 45),
     (25, 50), (20, 55), (15, 58), (10, 60), (5, 58), (0, 52),
     (-5, 48), (-10, 44), (-10, 38)],
    # Asia
    [(30, 36), (35, 42), (40, 45), (45, 48), (50, 50), (55, 55),
     (60, 60), (70, 65), (80, 70), (100, 75), (120, 72), (140, 72),
     (160, 70), (170, 66), (162, 60), (158, 52), (150, 45), (140, 40),
     (130, 35), (127, 40), (120, 32), (110, 25), (105, 15), (100, 10),
     (95, 15), (90, 20), (85, 22), (80, 15), (75, 10), (70, 25),
     (65, 25), (60, 25), (55, 25), (50, 30), (45, 30), (40, 36),
     (35, 36)],
    # Australia
    [(113, -22), (120, -15), (130, -12), (140, -18), (150, -22),
     (153, -28), (150, -37), (140, -38), (130, -32), (120, -34),
     (113, -30)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (-1, 55), (0, 52)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44),
     (141, 45), (139, 40), (135, 34)],
]
# Badge centres for the tight clusters (panel coords); the rest sit
# on their dot. Numbers are the story numbers.
BADGE_AT = {
    2: (312, 802),   # Darmstadt (BepiColombo control centre)
    3: (334, 812),   # Kyiv
    4: (344, 842),   # Antalya
    5: (218, 832),   # Geneva
    6: (134, 854),   # Washington
    9: (216, 862),   # Barcelona
    10: (222, 794),  # Brussels
    11: (262, 800),  # Copenhagen
    12: (278, 862),  # Rome
}


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 28
    rx = W - mx  # 996

    # ---- masthead: cream band, big navy serif title, double rule ----
    kick = "SATURDAY 21 NOVEMBER 2026   •   35 STORIES   •   13 MAIN + 22 ALSO   •   7 REGIONS"
    kf = sans_b(12)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 12), kick,
           font=kf, fill=NAVY)
    title = "THE WORLD"
    tf = serif_b(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 28), title,
           font=tf, fill=NAVY)
    tag = "One day. One page. Every region."
    tgf = serif_i(14)
    d.text(((W - d.textlength(tag, font=tgf)) / 2, 88), tag,
           font=tgf, fill=GRAY)
    d.line([(mx, 100), (rx, 100)], fill=NAVY, width=1)
    d.line([(mx, 104), (rx, 104)], fill=NAVY, width=2)

    # ---- ticker: brick-red bar, white figures ----
    d.rectangle([mx, 112, rx, 146], fill=RED)
    tick = "   •   ".join(TICKER)
    for size in (15, 14, 13, 12):
        tf2 = sans_b(size)
        if d.textlength(tick, font=tf2) <= 940:
            break
    d.text(((W - d.textlength(tick, font=tf2)) / 2, 112 + (34 - size) / 2 - 1),
           tick, font=tf2, fill=(255, 248, 238))

    # ---- hero: Markets ----
    num, label, head, deck, art, _lon, _lat = LEADS[0]
    d.text((mx, 160), label, font=sans_b(13), fill=RED)
    d.text((mx, 178), head, font=serif_b(36), fill=NAVY)
    dl = fit_lines(d, deck, sans_r(13), 640, 2)
    y = 224
    for line in dl:
        d.text((mx, y), line, font=sans_r(13), fill=INK)
        y += 17
    big = "-3.7%"
    bf = serif_b(84)
    bw = d.textlength(big, font=bf)
    d.text((rx - bw, 160), big, font=bf, fill=RED)
    cap = "FRIDAY CLOSE · 7TH STRAIGHT LOSS"
    cf = sans_b(11)
    d.text((rx - d.textlength(cap, font=cf), 250), cap, font=cf, fill=NAVY)
    img.paste(load_art(art, 968, 104), (mx, 268))
    d.rectangle([mx, 268, rx, 372], outline=NAVY, width=1)

    # ---- two lead cards: Kyiv, BepiColombo ----
    for i, (num, label, head, deck, art, _lon, _lat) in enumerate(LEADS[1:]):
        x0 = mx + i * 490
        x1 = x0 + 478
        d.rectangle([x0, 388, x1, 552], fill=CREAM_PANEL,
                    outline=CARD_LINE, width=1)
        img.paste(load_art(art, 478, 76), (x0, 388))
        d.text((x0 + 12, 470), label, font=sans_b(11), fill=RED)
        d.text((x0 + 12, 486), head, font=serif_b(19), fill=NAVY)
        ll = fit_lines(d, deck, sans_r(12), 454, 2)
        y = 508
        for line in ll:
            d.text((x0 + 12, y), line, font=sans_r(12), fill=INK)
            y += 15

    # ---- ten feature rows, 5 x 2 ----
    for r in range(5):
        for c in range(2):
            st = FEATURES[r * 2 + c]
            num, label, head, deck, art, _lon, _lat = st
            x0 = mx + c * 490
            y0 = 560 + r * 41
            img.paste(load_art(art, 62, 38), (x0, y0))
            tx = x0 + 70
            hl = trunc(d, label + " — " + head, sans_b(13), 400)
            d.text((tx, y0 + 1), hl, font=sans_b(13), fill=NAVY)
            dl2 = fit_lines(d, deck, sans_r(11), 400, 2)
            y = y0 + 17
            for line in dl2:
                d.text((tx, y), line, font=sans_r(11), fill=INK)
                y += 11

    # ---- map panel (dark navy) + ALSO list ----
    px0, py0, px1, py1 = mx, 772, 498, 914
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    mhead = "WHERE THE NEWS IS · 13 MAIN STORIES"
    mh = sans_b(11)
    d.text(((px0 + px1 - d.textlength(mhead, font=mh)) / 2, 780),
           mhead, font=mh, fill=MAP_CREAM)
    # continents, equirectangular lon -170..190, lat -55..80
    mx0, mx1, my0, my1 = 36, 490, 794, 890

    def proj(lon, lat):
        x = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        y = my1 - (lat + 55) / 135.0 * (my1 - my0)
        return (x, y)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_CREAM)
    # dots + leader badges
    for num, _label, _head, _deck, _art, lon, lat in MAIN:
        dx, dy = proj(lon, lat)
        bx, by = BADGE_AT.get(num, (dx, dy))
        if (bx, by) != (dx, dy):
            d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
            d.line([(dx, dy), (bx, by)], fill=MAP_CREAM, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
                  outline=MAP_CREAM, width=1)
        nf = sans_b(10)
        ns = str(num)
        d.text((bx - d.textlength(ns, font=nf) / 2, by - 7), ns,
               font=nf, fill=(255, 248, 238))
    # region counts, shrink to fit
    for size in (11, 10, 9):
        rf = sans_b(size)
        if d.textlength(REGION_COUNTS, font=rf) <= 454:
            break
    d.text(((px0 + px1 - d.textlength(REGION_COUNTS, font=rf)) / 2, 898),
           REGION_COUNTS, font=rf, fill=MAP_CREAM)

    # ALSO list, two columns of 11
    d.text((518, 776), "ALSO ON SATURDAY", font=sans_b(12), fill=NAVY)
    af_b = sans_b(10)
    af_r = sans_r(10)
    for idx, (city, line) in enumerate(ALSO):
        col = idx // 11
        row = idx % 11
        x0 = 518 + col * 242
        y0 = 792 + row * 11
        head = city + " — "
        hw = d.textlength(head, font=af_b)
        rest = trunc(d, line, af_r, 234 - hw)
        d.text((x0, y0), head, font=af_b, fill=NAVY)
        d.text((x0 + hw, y0), rest, font=af_r, fill=INK)

    # ---- DATE CHECK box ----
    d.rectangle([mx, 922, rx, 982], outline=RED, width=2)
    d.text((40, 930), DATE_LEFT_HEAD, font=sans_b(11), fill=RED)
    d.text((540, 930), DATE_RIGHT_HEAD, font=sans_b(11), fill=RED)
    ll = fit_lines(d, DATE_LEFT, sans_r(10), 480, 3)
    y = 944
    for line in ll:
        d.text((40, y), line, font=sans_r(10), fill=INK)
        y += 12
    rl = fit_lines(d, DATE_RIGHT, sans_r(10), 444, 3)
    y = 944
    for line in rl:
        d.text((540, y), line, font=sans_r(10), fill=INK)
        y += 12

    # ---- footer ----
    ff = sans_r(9)
    d.text(((W - d.textlength(FOOTER, font=ff)) / 2, 992), FOOTER,
           font=ff, fill=GRAY)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    with open(os.path.join(HERE, "entry.png.b64"), "w") as fh:
        fh.write(base64.b64encode(open(
            os.path.join(HERE, "entry.png"), "rb").read()).decode())
    print("entry.png:", os.path.getsize(os.path.join(HERE, "entry.png")),
          "bytes")


if __name__ == "__main__":
    build()

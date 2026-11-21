#!/usr/bin/env python3
"""THE OVERNIGHT EDITION - a one-page dark-edition newspaper summing up
Saturday 21 November 2026: 40 stories, 13 pictured cards, a locator map,
27 briefs, a numbers strip and a date check.

Draws entry.png (1024x1024) next to this file using only Pillow primitives:
flat vector-style shapes, no external images. Deterministic: no randomness,
no clocks, no network. All facts come from the day's news pool; a source is
named beside every story.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16                      # page margin
CW = W - 2 * MX              # content width = 992

# --- Theme B: dark "overnight" edition -------------------------------------
BG = (14, 26, 43)            # deep navy #0E1A2B
PANEL = (22, 40, 63)         # panel navy #16283F
PANEL_DK = (11, 21, 36)      # caption band / inset #0B1524
CREAM = (242, 234, 216)      # #F2EAD8
MUTED = (185, 196, 212)      # #B9C4D4
GOLD = (232, 179, 60)        # #E8B33C
ALERT = (217, 95, 75)        # #D95F4B
HOOK = (146, 22, 40)         # deep crimson hook band
LINE = (58, 82, 112)         # hairline on navy
LAND = (201, 168, 106)       # pale gold land #C9A86A

REGIONS = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

PLAYFAIR = "PlayfairDisplay-900.ttf"
ARCH_B = "Archivo-Bold.ttf"
ARCH_M = "Archivo-Medium.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

_cache = {}


def F(name, size):
    key = (name, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))
    return _cache[key]


def tw(s, font):
    return d.textlength(s, font=font)


def wrap(text, font, max_w):
    """Greedy word wrap; returns lines that each fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, name, size, max_w, floor=8):
    """Shrink a font until text fits max_w (never below floor px)."""
    while size > floor and tw(text, F(name, size)) > max_w:
        size -= 1
    return F(name, size)


def text(x, y, s, font, fill=CREAM, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def panel(x, y, w, h, fill=PANEL, outline=None):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline)

# --- The day's pool (facts verbatim from the merged NI21 pool) --------------
NUMBERS = [
    ("3", "weapons cross into Poland: two missiles and a jet drone"),
    ("42", "injured in the Kryvyi Rih strike, four of them children"),
    ("900,000", "AI chips the US has cleared for export to China"),
    ("6", "Houthi workshops destroyed in the Sana'a strikes"),
    ("€1BN", "EU military aid adopted for Kyiv"),
    ("159/1", "India at stumps in Wellington, day three"),
]

TIMELINE = [
    ("Overnight", "Kryvyi Rih strike: 2 killed, 42 hurt"),
    ("Morning", "Rutte flies to Warsaw over missiles"),
    ("Midday", "Antalya: third COP31 draft due"),
    ("Afternoon", "Denmark expels the Russian attache"),
    ("Evening", "Stumps in Wellington: India 159/1"),
]

REGION_COUNTS = [
    ("EUROPE", 16), ("ASIA", 7), ("MIDEAST", 3), ("AFRICA", 1),
    ("AMERICAS", 8), ("OCEANIA", 1), ("GLOBAL", 4),
]

# no, place, region, topic, headline, deck, strip source tag, strip data
# label, caption band, pin lon/lat
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "SECURITY",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. Rutte: a \"grave violation\". (AP)",
     "AP - SOFX", "3 WEAPONS CROSS", "WARSAW - THE MISSILES",
     (21.0, 52.2)),
    (2, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's close into Saturday. The draft drops fossil "
     "fuels and the $120bn finance target; a third draft is due this "
     "morning. (AP)",
     "Ongoing - AP", "NO DEAL YET", "ANTALYA - COP31 OVERTIME",
     (30.7, 36.9)),
    (3, "WASHINGTON", "AMERICAS", "TECH",
     "US clears 900,000 AI chips for China",
     "Washington clears exports of some 900,000 advanced AI chips to "
     "China - the largest single release of the year, officials say. "
     "(Reuters)",
     "Officials say", "900,000 CHIPS", "WASHINGTON - THE CHIP RELEASE",
     (-77.0, 38.9)),
    (4, "KRYVYI RIH", "EUROPE", "WAR",
     "Russian strike kills two, injures 42",
     "Across Ukraine the day's toll hits 12 dead, 82 hurt - among the "
     "war's largest attacks. (AppiStos)",
     "City chief says", "2 DEAD - 42 HURT", "KRYVYI RIH - OVERNIGHT STRIKE",
     (33.4, 47.9)),
    (5, "COPENHAGEN", "EUROPE", "PLOT",
     "Denmark exposes 'assassination plot'",
     "Plot to kill a Ukrainian-American rapper near Copenhagen; "
     "Russia's attache expelled. (BBC)",
     "Denmark says - BBC", "ATTACHE EXPELLED", "COPENHAGEN - THE PLOT",
     (12.6, 55.7)),
    (6, "KYIV", "EUROPE", "WAR",
     "Russia's barrage: 400 drones, 110 missiles",
     "Eight dead; Austrian embassy hit. Power rationed; 50 Rivne "
     "settlements dark. (BBC)",
     "Officials' count", "400 DRONES - 110 MISSILES", "KYIV - THE BARRAGE",
     (30.5, 50.4)),
    (7, "ODISHA, INDIA", "ASIA", "CYCLONE",
     "After Akvan: 372,000 moved, no deaths",
     "No deaths a day after landfall; storm weakens, schools shut "
     "through Saturday. (Ridhu Times)",
     "Relief reports", "372,000 MOVED", "ODISHA - AFTER LANDFALL",
     (84.9, 19.3)),
    (8, "BRUSSELS", "EUROPE", "DEFENCE",
     "EU adopts €1bn military aid for Ukraine",
     "Joint buying via the Peace Facility; Britain pledges 1,000+ "
     "drones alongside. (Reuters)",
     "Adopted - EU", "EUR 1BN ADOPTED", "BRUSSELS - THE PAYOUT",
     (4.3, 50.8)),
    (9, "NEW YORK", "AMERICAS", "CYBER",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "Incidents at third-party vendors; core payment networks "
     "unaffected, banks say. (Reuters)",
     "Banks say", "3 NETWORKS HIT", "NEW YORK - PAYMENT NETWORKS",
     (-73.9, 40.8)),
    (10, "RIYADH", "MIDEAST", "SECURITY",
     "Coalition hits Houthi workshops in Sana'a",
     "Six workshops destroyed; three Houthi missiles downed over "
     "Riyadh. (Reuters)",
     "Reuters", "6 WORKSHOPS - 3 MISSILES", "RIYADH - THE ALERT",
     (46.7, 24.6)),
    (11, "THE HAGUE", "GLOBAL", "COURT",
     "Myanmar ruling rattles Israel's Gaza defence",
     "Genocide verdict on Myanmar (ruled Thursday) raises questions "
     "over Israel's case. (BBC)",
     "Experts say", "GENOCIDE VERDICT", "THE HAGUE - WORLD COURT",
     (4.3, 52.1)),
    (12, "JOHANNESBURG", "AFRICA", "POLITICS",
     "ANC scrambles after worst result since 1994",
     "ANC wins 31%, worst since 1994; coalition race begins. (BBC)",
     "Count - BBC", "ANC 31%", "JOHANNESBURG - THE COUNT",
     (28.0, -26.2)),
    (13, "WELLINGTON", "OCEANIA", "CRICKET",
     "India fight back: 159/1 at stumps, day three",
     "India trail by 209; hosts made 368, Nicholls 175*. (ICC)",
     "Scorecard - ICC", "159/1 - DAY THREE", "WELLINGTON - DAY THREE",
     (174.8, -41.3)),
]

BRIEFS = [
    (14, "Kathmandu", "Nepal's new leader Balendra Shah faces an India test (BBC)"),
    (15, "Cardiff", "Lauren Price beats Kotaskova to become undisputed champion (BBC)"),
    (16, "Paris", "Three police are sentenced over the beating of Michel Zecler (BBC)"),
    (17, "Oxford", "Life, 22 years minimum, for the Thames drowning murder (BBC)"),
    (18, "New York", "Nikhil Gupta gets 19+ years over the Sikh murder plot (BBC)"),
    (19, "Los Angeles", "A jury convicts the man who started the Palisades Fire (AP)"),
    (20, "Frankfurt", "ECB names Boone and Brunnermeier for its Executive Board (Reuters)"),
    (21, "Buenos Aires", "Argentina's Senate backs a disability framework, 71-0 (AP)"),
    (22, "Barcelona", "A pill is hailed as a breakthrough for pancreatic cancer (Reuters)"),
    (23, "Gaza", "On World Children's Day, Palestinian children appeal for help (UN)"),
    (24, "Rome", "Italian workers and students march against Meloni's government (AFP)"),
    (25, "Kuala Lumpur", "Malaysia to send 10,000 Rohingya to Turkey for training (Reuters)"),
    (26, "Kharkiv", 'Ukraine says it has finished a "Bear Trap" in the Kharkiv area (Ukrinform)'),
    (27, "Turin", "ATP semis tonight: Alcaraz v Shelton, Zverev v Medvedev (ATP)"),
    (28, "Mercury", "BepiColombo arrives tonight after 8 years (ESA)"),
    (29, "Kharg Island", "Tanker convoy tests US blockade; Brent $94.65 (Reuters)"),
    (30, "Sacramento", "California subpoenas Nvidia over AI chips (AP)"),
    (31, "New Delhi", "India's first H5N1 vaccine launches (Reuters)"),
    (32, "Imphal", "Manipur clashes kill 11; 181 in hospital (AP)"),
    (33, "Atlanta", "Measles ends US elimination status (CDC)"),
    (34, "Pasadena", "Voyager 1 reaches one light-day out (NASA)"),
    (35, "Tokyo", "Japan to buy 8m barrels of Saudi crude (Reuters)"),
    (36, "Leverkusen", "Bayer's Roundup settlement: $7.25bn (Reuters)"),
    (37, "Sumy", "HIMARS kills 20 Russian commanders (Ukrinform)"),
    (38, "London", "UK cyberattacks hit Moscow (BBC)"),
    (39, "Jakarta", "Asks Google: why 19,000 accounts gone? (AP)"),
    (40, "Las Vegas", "GP qualifying today on the Strip (AP)"),
]

# brief number -> (lon, lat, region) for the map dots
# (28 Mercury and 34 Pasadena are space stories: Pasadena's dot marks the
# JPL ground station; Mercury itself has no Earth dot)
BRIEF_PINS = {
    14: (85.3, 27.7, "ASIA"), 15: (-3.2, 51.5, "EUROPE"),
    16: (2.4, 48.9, "EUROPE"), 17: (-1.3, 51.8, "EUROPE"),
    18: (-74.0, 40.7, "AMERICAS"), 19: (-118.3, 34.0, "AMERICAS"),
    20: (8.7, 50.1, "EUROPE"), 21: (-58.4, -34.6, "AMERICAS"),
    22: (2.2, 41.4, "EUROPE"), 23: (34.3, 31.5, "MIDEAST"),
    24: (12.5, 41.9, "EUROPE"), 25: (101.7, 3.1, "ASIA"),
    26: (36.2, 49.9, "EUROPE"), 27: (7.7, 45.1, "EUROPE"),
    29: (50.3, 29.2, "MIDEAST"), 30: (-121.5, 38.6, "AMERICAS"),
    31: (77.2, 28.6, "ASIA"), 32: (93.9, 24.8, "ASIA"),
    33: (-84.4, 33.7, "AMERICAS"), 34: (-118.1, 34.1, "GLOBAL"),
    35: (139.7, 35.7, "ASIA"), 36: (7.0, 51.0, "EUROPE"),
    37: (34.8, 50.9, "EUROPE"), 38: (-0.1, 51.5, "EUROPE"),
    39: (106.8, -6.2, "ASIA"), 40: (-115.1, 36.1, "AMERICAS"),
}

DATE_CHECK = (
    "Left out as Friday 20 November's news: Kyiv's three bridges hit, "
    "Akvan's landfall at Gopalpur, Wall Street's AI sell-off "
    "(Nasdaq -5.28%), Mongolia's president quitting, Asia's sell-off "
    "(Taipei -6.2%), the UK-EU reset deal and Phillips's 118. From "
    "Thursday 19 November: the Shenzhen three-leader summit, "
    "Anthropic's IPO filing and the world court's Myanmar ruling. "
    "Tonight's agenda, not results: the ATP semi-finals and "
    "BepiColombo's Mercury arrival (19:24 CET)."
)

FOOTER_L = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# --- Card strip scenes (flat layered shapes; area excludes caption band) ---
def scene_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 74, 107))          # night sky
    for sx, sy in ((0.12, 0.2), (0.55, 0.12), (0.85, 0.3)):         # stars
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3],
                  fill=MUTED)
    river_y = y + h - max(10, h // 4)
    d.rectangle([x, river_y, x + w, y + h], fill=(62, 111, 163))   # Dnipro
    for i in range(3):                                             # 3 bridges
        bx = x + int(w * (0.14 + 0.3 * i))
        bw = int(w * 0.24)
        by = river_y - 4
        d.arc([bx, by - h // 3, bx + bw, by + h // 3], 180, 360,
              fill=GOLD, width=3)
        d.line([bx, by, bx + bw, by], fill=GOLD, width=3)
        d.line([bx + bw // 2, by - h // 3, bx + bw // 2, by], fill=GOLD,
               width=2)
    for i in range(3):                                             # missile arcs
        ax = x + int(w * (0.2 + 0.28 * i))
        d.arc([ax, y + 2, ax + int(w * 0.2), y + h // 2], 200, 320,
              fill=ALERT, width=2)
        ex, ey = ax + int(w * 0.19), y + h // 3
        d.polygon([(ex, ey - 6), (ex + 3, ey - 1), (ex + 7, ey),
                   (ex + 3, ey + 2), (ex + 4, ey + 6), (ex, ey + 3),
                   (ex - 4, ey + 6), (ex - 3, ey + 2), (ex - 7, ey),
                   (ex - 3, ey - 1)], fill=GOLD)


def scene_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(51, 86, 110))          # storm sky
    cx, cy = x + w // 2, y + h // 2
    base = min(34, int(h * 0.46))
    for r in (base, int(base * 0.79), int(base * 0.58), int(base * 0.38)):
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], 20, 300,
              fill=CREAM, width=3)
    d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=GOLD)         # eye
    for i in range(6):                                             # rain
        rx = x + 8 + i * (w - 16) // 5
        d.line([rx, y + h - 14, rx - 5, y + h - 4], fill=MUTED, width=2)
    d.polygon([(x, y + h), (x + w // 3, y + h - 12), (x + w, y + h)],
              fill=(30, 132, 73))                                  # coast


def scene_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))           # board
    for i in range(1, 4):                                          # grid
        gy = y + h * i // 4
        d.line([x + 4, gy, x + w - 4, gy], fill=LINE, width=1)
    pts = [(x + 8, y + h * 0.22), (x + w * 0.3, y + h * 0.34),
           (x + w * 0.52, y + h * 0.3), (x + w * 0.74, y + h * 0.58),
           (x + w - 10, y + h * 0.8)]
    d.line(pts, fill=ALERT, width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 10, ey - 7), (ex - 3, ey - 12)], fill=ALERT)
    for px, py in pts[:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=CREAM)


def _flag_uk(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 110), outline=CREAM)
    d.line([x, y, x + w, y + h], fill=CREAM, width=3)
    d.line([x + w, y, x, y + h], fill=CREAM, width=3)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=CREAM, width=7)
    d.line([x, y + h // 2, x + w, y + h // 2], fill=CREAM, width=7)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(179, 32, 44), width=3)
    d.line([x, y + h // 2, x + w, y + h // 2], fill=(179, 32, 44), width=3)


def _flag_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 80, 160), outline=CREAM)
    import math
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 3
    for i in range(12):
        a = math.tau * i / 12
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def scene_flags(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 60, 92))
    fh = min(30, max(16, h - 18))
    fw = int(fh * 1.5)
    _flag_uk(x + w // 2 - fw - 6, y + 8, fw, fh)
    _flag_eu(x + w // 2 + 6, y + 8, fw, fh)
    d.line([x + w // 2 - fw - 6, y + 8 + fh, x + w // 2 + 6 + fw,
            y + 8 + fh], fill=GOLD, width=2)                       # table line


def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 62, 74))           # teal hall
    cx, cy = x + w // 2 - 14, y + h // 2
    r = min(h // 2 - 4, 34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(29, 111, 184),
              outline=CREAM, width=2)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=CREAM)
    d.line([cx - r, cy, cx + r, cy], fill=CREAM, width=1)
    d.line([cx - r, cy - r // 2, cx + r, cy - r // 2], fill=CREAM, width=1)
    d.line([cx - r, cy + r // 2, cx + r, cy + r // 2], fill=CREAM, width=1)
    tx = x + w - 30                                                # thermometer
    d.rectangle([tx, y + 8, tx + 7, y + h - 16], fill=CREAM)
    d.rectangle([tx + 1, y + 12, tx + 6, y + h - 16], fill=ALERT)
    d.ellipse([tx - 3, y + h - 22, tx + 10, y + h - 9], fill=ALERT)


def scene_poland(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 116, 62))          # field
    for i in range(4):                                             # furrows
        fy = y + 8 + i * (h - 16) // 4
        d.line([x + 4, fy, x + w - 4, fy - 4], fill=(56, 92, 46), width=2)
    mx0, my0 = x + w // 2 - 24, y + h // 2 - 6                     # missile
    d.polygon([(mx0, my0 + 8), (mx0 + 34, my0), (mx0 + 48, my0 + 3),
               (mx0 + 36, my0 + 10), (mx0 + 6, my0 + 14)],
              fill=(196, 200, 208))
    d.polygon([(mx0 + 40, my0 + 1), (mx0 + 52, my0 + 4), (mx0 + 41, my0 + 9)],
              fill=ALERT)
    d.line([x + w - 14, y + 4, x + w - 14, y + h - 4], fill=GOLD, width=2)
    for yy in range(y + 8, y + h - 4, 10):                         # border dashes
        d.line([x + w - 14, yy, x + w - 14, yy + 5], fill=PANEL_DK, width=2)


def scene_iraq(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 178, 110))        # desert
    d.ellipse([x + w - 34, y + 5, x + w - 12, y + 27], fill=GOLD)  # sun
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(186, 138, 74))
    for i, vx in enumerate((0.16, 0.55)):                          # vehicles
        bx = x + int(w * vx)
        by = y + h - 26
        d.rectangle([bx, by, bx + 42, by + 12], fill=(94, 84, 52))
        d.rectangle([bx + 8, by - 7, bx + 26, by], fill=(94, 84, 52))
        d.ellipse([bx + 5, by + 9, bx + 15, by + 19], fill=PANEL_DK)
        d.ellipse([bx + 27, by + 9, bx + 37, by + 19], fill=PANEL_DK)
        d.line([bx + 30, by - 7, bx + 44, by - 12], fill=PANEL_DK, width=2)

def scene_italy(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 84, 110))          # square
    bw = int(w * 0.44)                                             # banner
    bx, by = x + 4, y + 1        # top-left: clears the source tag (top-right)
                                 # and the data-label pill (bottom-left)
    bh = max(13, h // 4)
    d.rectangle([bx, by, bx + bw, by + bh], fill=CREAM)
    bf = fit("SCIOPERO", ARCH_B, bh - 3, bw - 8, floor=7)
    text(bx + bw // 2, by + bh // 2, "SCIOPERO", bf, fill=(179, 32, 44),
         anchor="mm")
    cols = max(6, w // 22)                                         # crowd
    for i in range(cols):
        for j in range(2):
            hx = x + 10 + i * 22 + (8 if j else 0)
            hy = y + h - 13 - j * 11
            if bx - 8 < hx < bx + bw + 8 and j == 1:
                continue
            d.ellipse([hx, hy, hx + 7, hy + 7], fill=(232, 200, 150))
            d.pieslice([hx - 2, hy + 5, hx + 9, hy + 13], 180, 360,
                       fill=(150, 60, 50) if (i + j) % 2 else (60, 90, 140))


def scene_japan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))
    base = y + h - 8
    d.line([x + 8, base, x + w - 8, base], fill=MUTED, width=2)
    vals = (0.42, 0.58, 0.82)                                      # rising bars
    bw = max(14, w // 7)
    for i, v in enumerate(vals):
        bx = x + w // 2 - bw - 10 + i * (bw + 10)
        bh = int((h - 18) * v)
        d.rectangle([bx, base - bh, bx + bw, base],
                    fill=GOLD if i == 2 else (29, 111, 184))
    d.line([x + w // 2 - bw - 14, base - int((h - 18) * 0.5),
            x + w // 2 + bw + 14, base - int((h - 18) * 0.5)],
           fill=ALERT, width=2)                                    # target line


def scene_seoul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 104, 128))         # stone hall
    cx = x + w // 2
    tw_ = int(w * 0.62)
    ped = max(8, h // 3)
    d.polygon([(cx - tw_ // 2, y + ped), (cx + tw_ // 2, y + ped),
               (cx, y + 2)], fill=CREAM)                           # pediment
    d.rectangle([cx - tw_ // 2, y + ped + 2, cx + tw_ // 2, y + ped + 5],
                fill=CREAM)
    for i in range(4):                                             # columns
        colx = cx - tw_ // 2 + 6 + i * (tw_ - 12) // 3
        d.rectangle([colx - 3, y + ped + 7, colx + 3, y + h - 6], fill=CREAM)
    d.rectangle([cx - tw_ // 2, y + h - 6, cx + tw_ // 2, y + h - 2],
                fill=CREAM)
    d.line([cx + tw_ // 4, y + h // 2, cx + tw_ // 4 + 10, y + h // 2 - 6],
           fill=GOLD, width=3)                                     # gavel hint


def scene_kenya(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 190, 120))        # savanna
    d.ellipse([x + 8, y + 5, x + 28, y + 25], fill=GOLD)
    d.rectangle([x, y + h - 9, x + w, y + h], fill=(170, 120, 60))
    cx = x + w // 2                                                # derrick
    top = y + 5
    bot = y + h - 9
    d.line([cx - 20, bot, cx, top], fill=PANEL_DK, width=3)
    d.line([cx + 20, bot, cx, top], fill=PANEL_DK, width=3)
    d.line([cx - 13, bot - (bot - top) // 2, cx + 13, bot - (bot - top) // 2],
           fill=PANEL_DK, width=2)
    d.line([cx, top, cx + 22, top + 6], fill=PANEL_DK, width=3)    # arm
    d.line([cx + 22, top + 6, cx + 22, top + 16], fill=PANEL_DK, width=2)
    d.ellipse([cx + 19, top + 16, cx + 25, top + 22], fill=ALERT)  # first drop


def scene_bukele(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 92, 140))          # hall blue
    cx = x + w // 2
    bw, bh = int(w * 0.4), max(20, h // 2)
    bx, by = cx - bw // 2, y + h - bh - 4
    d.rectangle([bx, by, bx + bw, by + bh], fill=(240, 236, 224),
                outline=PANEL_DK, width=2)                         # ballot box
    d.rectangle([bx + 8, by + 5, bx + bw - 8, by + 9], fill=PANEL_DK)
    d.polygon([(cx - 9, y + 4), (cx + 9, y + 4), (cx + 5, by + 7),
               (cx - 5, by + 7)], fill=CREAM)                      # paper slip
    d.rectangle([bx, by + bh - 8, bx + bw, by + bh], fill=(29, 111, 184))


def scene_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 122, 74))          # outfield
    pw = int(w * 0.3)
    px = x + (w - pw) // 2
    d.rectangle([px, y + 6, px + pw, y + h - 4], fill=(222, 198, 140))
    sx = px + pw - 16                                              # stumps
    for i in range(3):
        d.line([sx + i * 5, y + h - 22, sx + i * 5, y + h - 8],
               fill=(240, 220, 160), width=2)
    d.line([sx, y + h - 23, sx + 10, y + h - 23], fill=GOLD, width=2)
    bx = px + 12                                                   # bat
    d.polygon([(bx, y + h - 26), (bx + 6, y + h - 28), (bx + 12, y + h - 8),
               (bx + 4, y + h - 6)], fill=(196, 150, 90))
    d.ellipse([x + w - 30, y + 10, x + w - 20, y + 20], fill=(179, 32, 44))
    d.arc([x + w - 52, y + 4, x + w - 16, y + 30], 90, 200, fill=CREAM,
          width=2)                                                 # ball trail


def scene_barrage(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 64, 98))           # night sky
    for sx, sy in ((0.08, 0.18), (0.62, 0.1), (0.9, 0.26)):        # stars
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3],
                  fill=MUTED)
    gy = y + h                                                     # skyline
    for i, bh in enumerate((0.52, 0.78, 0.4, 0.66, 0.48, 0.84, 0.56)):
        bw = w // 7
        bx = x + i * bw
        top = gy - int(h * bh)
        d.rectangle([bx + 1, top, bx + bw - 1, gy], fill=(18, 30, 48))
        for wy in range(top + 4, gy - 4, 7):                       # lit windows
            for wx in range(bx + 4, bx + bw - 4, 8):
                if (wx * 7 + wy * 13) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 3], fill=GOLD)
    for i in range(3):                                             # missile arcs
        ax = x + int(w * (0.16 + 0.3 * i))
        d.arc([ax, y + 1, ax + int(w * 0.22), y + int(h * 0.62)], 200, 325,
              fill=ALERT, width=2)
    for dx, dy in ((0.3, 0.2), (0.72, 0.3)):                       # drones
        cx, cy = x + int(w * dx), y + int(h * dy)
        d.line([cx - 5, cy - 4, cx + 5, cy + 4], fill=CREAM, width=2)
        d.line([cx - 5, cy + 4, cx + 5, cy - 4], fill=CREAM, width=2)


def scene_city_blast(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(66, 76, 106))          # dusk sky
    gy = y + h
    for i, bh in enumerate((0.62, 0.42, 0.74, 0.5)):               # blocks left
        bw = w // 6
        bx = x + i * bw
        top = gy - int(h * bh)
        d.rectangle([bx + 1, top, bx + bw - 1, gy], fill=(30, 40, 60))
        for wy in range(top + 4, gy - 4, 7):
            for wx in range(bx + 4, bx + bw - 4, 8):
                if (wx * 5 + wy * 11) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 3], fill=(240, 220, 160))
    cx, cy = x + int(w * 0.78), y + int(h * 0.42)                  # blast
    for ang in range(0, 360, 30):
        import math
        r1 = max(8, int(h * 0.3))
        ex = cx + r1 * math.cos(math.radians(ang))
        ey = cy + r1 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=GOLD, width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=ALERT)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=CREAM)
    d.ellipse([cx + 6, cy - int(h * 0.34), cx + 34, cy - int(h * 0.1)],
              fill=MUTED)                                          # smoke


def scene_reticle(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 66, 92))           # evening sky
    gy = y + h
    for i, bh in enumerate((0.44, 0.6, 0.38, 0.55, 0.46)):         # rooftops
        bw = w // 5
        bx = x + i * bw
        top = gy - int(h * bh)
        d.polygon([(bx, top + 6), (bx + bw // 2, top), (bx + bw, top + 6),
                   (bx + bw, gy), (bx, gy)], fill=(122, 62, 52))
        d.rectangle([bx + bw // 2 - 2, top + 9, bx + bw // 2 + 2, top + 15],
                    fill=GOLD)
    cx, cy = x + w // 2, y + int(h * 0.44)                         # reticle
    r = max(11, int(h * 0.34))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ALERT, width=3)
    d.line([cx - r - 6, cy, cx - r + 5, cy], fill=ALERT, width=3)
    d.line([cx + r - 5, cy, cx + r + 6, cy], fill=ALERT, width=3)
    d.line([cx, cy - r - 6, cx, cy - r + 5], fill=ALERT, width=3)
    d.line([cx, cy + r - 5, cx, cy + r + 6], fill=ALERT, width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=ALERT)


def scene_cyber(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))           # board
    cw_ = min(64, int(w * 0.3))
    ch_ = max(16, int(h * 0.52))
    cols = ((29, 111, 184), (240, 236, 224), (202, 111, 30))
    for i in range(3):                                             # payment cards
        bx = x + int(w * (0.06 + 0.24 * i))
        by = y + int(h * 0.16)
        d.rectangle([bx, by, bx + cw_, by + ch_], fill=cols[i])
        d.rectangle([bx + 5, by + 5, bx + 15, by + 11], fill=GOLD)  # chip
        d.rectangle([bx, by + ch_ - 7, bx + cw_, by + ch_ - 4],
                    fill=PANEL_DK)
    tx, ty = x + int(w * 0.84), y + int(h * 0.14)                  # warning
    ts = max(13, int(h * 0.4))
    d.polygon([(tx, ty + ts), (tx + ts // 2, ty), (tx + ts, ty + ts)],
              fill=GOLD)
    d.rectangle([tx + ts // 2 - 1, ty + ts // 3, tx + ts // 2 + 1,
                 ty + ts - 8], fill=PANEL_DK)
    d.ellipse([tx + ts // 2 - 1, ty + ts - 6, tx + ts // 2 + 1,
               ty + ts - 4], fill=PANEL_DK)


def scene_steppe(x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.62)], fill=(110, 160, 200))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(150, 140, 80))
    d.ellipse([x + w - 32, y + 4, x + w - 14, y + 22], fill=GOLD)  # sun
    cx, gy = x + w // 2, y + h                                     # ger
    gw, gh = int(w * 0.3), max(14, int(h * 0.52))
    d.rectangle([cx - gw // 2, gy - gh, cx + gw // 2, gy],
                fill=(240, 236, 224))
    d.polygon([(cx - gw // 2 - 4, gy - gh), (cx + gw // 2 + 4, gy - gh),
               (cx, gy - gh - max(5, h // 8))], fill=(179, 32, 44))
    d.rectangle([cx - 4, gy - gh + 6, cx + 4, gy], fill=(122, 62, 52))
    px = cx + gw // 2 + 12                                         # flag
    d.line([px, gy, px, gy - gh - 6], fill=PANEL_DK, width=2)
    fw_, fh_ = 16, 10
    d.rectangle([px, gy - gh - 6, px + fw_ // 3, gy - gh - 6 + fh_],
                fill=(179, 32, 44))
    d.rectangle([px + fw_ // 3, gy - gh - 6, px + 2 * fw_ // 3,
                 gy - gh - 6 + fh_], fill=(29, 80, 160))
    d.rectangle([px + 2 * fw_ // 3, gy - gh - 6, px + fw_,
                 gy - gh - 6 + fh_], fill=(179, 32, 44))


def scene_payout(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 54, 110))          # EU blue
    cy = y + int(h * 0.42)
    r = max(8, int(h * 0.32))                                      # gold coin
    cx = x + int(w * 0.30)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
              outline=CREAM, width=1)
    ef = fit("€", ARCH_B, int(r * 1.5), 2 * r - 2, floor=7)
    text(cx, cy, "€", ef, fill=PANEL_DK, anchor="mm")
    ax0, ax1 = x + int(w * 0.47), x + int(w * 0.60)                # arrow
    d.line([ax0, cy, ax1, cy], fill=CREAM, width=3)
    d.polygon([(ax1, cy - 4), (ax1 + 7, cy), (ax1, cy + 4)], fill=CREAM)
    fx, fw_, fh_ = x + int(w * 0.64), 26, 14                       # UA bicolor
    d.rectangle([fx, cy - fh_ // 2, fx + fw_, cy], fill=(52, 110, 180))
    d.rectangle([fx, cy, fx + fw_, cy + fh_ // 2], fill=GOLD)
    d.rectangle([fx, cy - fh_ // 2, fx + fw_, cy + fh_ // 2],
                outline=CREAM, width=1)


def scene_chips(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))           # board
    cs = min(int(h * 0.62), int(w * 0.3))                          # chip body
    cx, cy = x + w // 2, y + h // 2
    x0, y0 = cx - cs // 2, cy - cs // 2
    for i in range(4):                                             # pins
        px = x0 + (i + 1) * cs // 5
        d.line([px, y0 - 5, px, y0], fill=GOLD, width=2)
        d.line([px, y0 + cs, px, y0 + cs + 5], fill=GOLD, width=2)
        py = y0 + (i + 1) * cs // 5
        d.line([x0 - 5, py, x0, py], fill=GOLD, width=2)
        d.line([x0 + cs, py, x0 + cs + 5, py], fill=GOLD, width=2)
    d.rectangle([x0, y0, x0 + cs, y0 + cs], fill=(52, 92, 140),
                outline=CREAM, width=2)
    ix0, iy0 = x0 + cs // 4, y0 + cs // 4                          # die
    d.rectangle([ix0, iy0, x0 + 3 * cs // 4, y0 + 3 * cs // 4],
                outline=GOLD, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    for sx, sy in ((0.1, 0.22), (0.88, 0.3), (0.14, 0.8), (0.9, 0.78)):
        tx_, ty_ = x + int(w * sx), y + int(h * sy)                # traces
        d.line([tx_, ty_, tx_ + 12, ty_], fill=(29, 111, 184), width=2)
        d.ellipse([tx_ + 12, ty_ - 2, tx_ + 16, ty_ + 2],
                  fill=(29, 111, 184))


def scene_intercept(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 74))           # night sky
    for sx, sy in ((0.1, 0.16), (0.45, 0.08), (0.68, 0.22)):
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3,
                   y + h * sy + 3], fill=MUTED)
    gy = y + h                                                     # skyline
    for i, bh in enumerate((0.34, 0.5, 0.28, 0.58, 0.38, 0.44, 0.3)):
        bw = w // 7
        bx = x + i * bw
        top = gy - int(h * bh)
        d.rectangle([bx + 1, top, bx + bw - 1, gy], fill=(16, 26, 42))
        for wy in range(top + 4, gy - 4, 7):
            for wx in range(bx + 4, bx + bw - 4, 8):
                if (wx * 3 + wy * 7) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 3], fill=GOLD)
    for i in range(3):                                             # incoming
        ax = x + int(w * (0.52 + 0.16 * i))
        d.arc([ax, y + 1, ax + int(w * 0.2), y + int(h * 0.55)], 200, 320,
              fill=ALERT, width=2)
    for fx, fy in ((0.34, 0.3), (0.58, 0.2), (0.78, 0.38)):        # bursts
        cx, cy = x + int(w * fx), y + int(h * fy)
        for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4),
                       (4, -4), (-4, 4), (4, 4)):
            d.line([cx, cy, cx + dx, cy + dy], fill=GOLD, width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=CREAM)


SCENES = {1: scene_poland, 2: scene_cop, 3: scene_chips,
          4: scene_city_blast, 5: scene_reticle, 6: scene_barrage,
          7: scene_cyclone, 8: scene_payout, 9: scene_cyber,
          10: scene_intercept, 11: scene_seoul, 12: scene_bukele,
          13: scene_cricket}

CAP_H = 16  # caption band height inside every strip


def draw_strip(card, x, y, w, h):
    """Illustrated strip: region rule, scene, source tag, data label, band."""
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    col = REGIONS[region]
    lead = w > 250
    d.rectangle([x, y, x + w, y + h], fill=PANEL_DK)
    d.rectangle([x, y, x + w, y + 3], fill=col)                    # region rule
    SCENES[no](x, y + 3, w, h - 3 - CAP_H)
    tf = F(ARCH_B, 9 if lead else 8)                               # source tag
    tag_w = tw(tag, tf) + 10
    tag_h = 14 if lead else 12
    d.rectangle([x + w - tag_w - 4, y + 5, x + w - 4, y + 5 + tag_h],
                fill=PANEL_DK)
    text(x + w - tag_w + 1, y + 5 + tag_h / 2, tag, tf, fill=CREAM,
         anchor="lm")
    lf = fit(label, ARCH_B, 13 if lead else 11, w - 14, floor=8)
    lw_ = tw(label, lf) + 12                                       # data label
    pill_h = 16 if lead else 12
    ly = y + h - CAP_H - (20 if lead else 12)
    d.rectangle([x + 5, ly, x + 5 + lw_, ly + pill_h], fill=PANEL_DK)
    text(x + 11, ly + pill_h / 2, label, lf, fill=GOLD, anchor="lm")
    d.rectangle([x, y + h - CAP_H, x + w, y + h], fill=PANEL_DK)   # band
    bf = fit(caption, ARCH_B, 10, w - 12, floor=7)
    text(x + w // 2, y + h - CAP_H // 2, caption, bf, fill=MUTED,
         anchor="mm")

# --- Header: kicker, masthead, timeline, numbers, region counts ------------
Y = 8
d.rectangle([MX, Y, MX + CW, Y + 21], fill=GOLD)
text(MX + 8, Y + 10, "THE WORLD IN ONE DAY", F(ARCH_B, 12),
     fill=PANEL_DK, anchor="lm")
text(MX + 252, Y + 10, "SATURDAY 21 NOVEMBER 2026", F(ARCH_B, 12),
     fill=PANEL_DK, anchor="lm")
kr = "40 STORIES - 7 REGIONS - EVERY ONE DATED TODAY"
text(MX + CW - 8, Y + 10, kr, fit(kr, ARCH_B, 12, 470), fill=PANEL_DK,
     anchor="rm")

Y = 34
mf = fit("THE OVERNIGHT EDITION", PLAYFAIR, 50, CW)
text(MX + CW // 2, Y, "THE OVERNIGHT EDITION", mf, fill=CREAM,
     anchor="ma")
Y += 58
d.rectangle([MX, Y, MX + CW, Y + 28], fill=HOOK)
hook_line = ("MISSILES LAND IN POLAND - US CLEARS 900,000 AI CHIPS FOR "
             "CHINA - COP31 DEADLOCKED IN OVERTIME")
text(MX + CW // 2, Y + 14, hook_line, fit(hook_line, ARCH_B, 13, CW - 24),
     fill=CREAM, anchor="mm")

Y += 34                                                     # UTC timeline
panel(MX, Y, CW, 30)
cell = CW / 5.0
for i, (lab, ev) in enumerate(TIMELINE):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 4, cx0, Y + 26], fill=LINE, width=1)
    text(cx0 + 8, Y + 4, lab.upper(), F(ARCH_B, 10), fill=GOLD)
    for j, ln in enumerate(wrap(ev, F(ARCH_M, 10), cell - 14)[:1]):
        text(cx0 + 8, Y + 16 + j * 10, ln, F(ARCH_M, 10), fill=CREAM)

Y += 36                                                     # day in numbers
panel(MX, Y, CW, 54)
cell = CW / 6.0
text(MX + 8, Y + 2, "THE DAY IN NUMBERS", F(ARCH_B, 8), fill=MUTED)
for i, (num, cap) in enumerate(NUMBERS):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 8, cx0, Y + 52], fill=LINE, width=1)
    nf = fit(num, PLAYFAIR, 23, cell - 14)
    text(cx0 + 8, Y + 8, num, nf, fill=GOLD)
    for j, ln in enumerate(wrap(cap, F(ARCH_M, 9), cell - 14)[:2]):
        text(cx0 + 8, Y + 35 + j * 10, ln, F(ARCH_M, 9), fill=MUTED)

Y += 54                                                     # region counts
cx = MX
text(cx, Y + 10, "WHERE:", F(ARCH_B, 10), fill=MUTED, anchor="lm")
cx += int(tw("WHERE:", F(ARCH_B, 10))) + 10
for name, n in REGION_COUNTS:
    label = "%s %d" % (name, n)
    lf = F(ARCH_B, 11)
    wch = int(tw(label, lf)) + 24
    d.rectangle([cx, Y, cx + wch, Y + 20], fill=PANEL)
    d.ellipse([cx + 6, Y + 6, cx + 14, Y + 14], fill=REGIONS[name])
    text(cx + 18, Y + 10, label, lf, fill=CREAM, anchor="lm")
    cx += wch + 8

# --- Lead row: cards 1-3 ----------------------------------------------------
LEAD_Y = 238
LEAD_W = 325
for i, card in enumerate(CARDS[:3]):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    cx0 = MX + i * (LEAD_W + 8)
    panel(cx0, LEAD_Y, LEAD_W, 196)
    draw_strip(card, cx0 + 6, LEAD_Y + 6, LEAD_W - 12, 76)
    ry = LEAD_Y + 86
    text(cx0 + 8, ry, "%d  %s - %s - %s" % (no, place, region, topic),
         F(ARCH_B, 11), fill=REGIONS[region])
    hy = ry + 14
    for ln in wrap(headline, F(PLAYFAIR, 21), LEAD_W - 16)[:2]:
        text(cx0 + 8, hy, ln, F(PLAYFAIR, 21), fill=CREAM)
        hy += 23
    dy = hy + 2
    for ln in wrap(deck, F(ARCH_M, 12), LEAD_W - 16)[:4]:
        text(cx0 + 8, dy, ln, F(ARCH_M, 12), fill=MUTED)
        dy += 14.5

# --- Feature grid: cards 4-13, 2 rows x 5 -----------------------------------
FEAT_Y = 442
FEAT_W = 194
ROW_H = 122
for k, card in enumerate(CARDS[3:]):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    cx0 = MX + (k % 5) * (FEAT_W + 5)
    cy0 = FEAT_Y + (k // 5) * (ROW_H + 8)
    panel(cx0, cy0, FEAT_W, ROW_H)
    draw_strip(card, cx0 + 5, cy0 + 5, FEAT_W - 10, 44)
    ry = cy0 + 52
    text(cx0 + 7, ry, "%d  %s - %s" % (no, place, region), F(ARCH_B, 9),
         fill=REGIONS[region])
    hy = ry + 12
    for ln in wrap(headline, F(ARCH_B, 13), FEAT_W - 14)[:2]:
        text(cx0 + 7, hy, ln, F(ARCH_B, 13), fill=CREAM)
        hy += 14
    dy = hy + 1
    for ln in wrap(deck, F(ARCH_M, 11), FEAT_W - 14)[:3]:
        text(cx0 + 7, dy, ln, F(ARCH_M, 11), fill=MUTED)
        dy += 11.5

# --- Bottom row: map panel + also-on panel ----------------------------------
BOT_Y = 702
BOT_H = 265
panel(MX, BOT_Y, 330, BOT_H)
text(MX + 8, BOT_Y + 6, "WHERE IT HAPPENED", F(ARCH_B, 12), fill=GOLD)

MAP_X, MAP_Y, MAP_W, MAP_H = MX + 8, BOT_Y + 28, 314, 168
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=PANEL_DK)


def proj(lon, lat):
    return (MAP_X + (lon + 180.0) / 360.0 * MAP_W,
            MAP_Y + (82.0 - lat) / 140.0 * MAP_H)


for _name, rings in WORLD.items():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(proj(float(lo), float(la)))
        if len(pts) > 2:
            d.polygon(pts, fill=LAND)

for no, (lo, la, reg) in BRIEF_PINS.items():                       # dots
    px, py = proj(lo, la)
    d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REGIONS[reg])

# display nudges so clustered pins (Europe, New York) stay legible
PIN_OFF = {1: (17, -10), 2: (-14, 10), 3: (-5, -3), 4: (4, 19),
           5: (-16, -18), 6: (20, 6), 8: (-21, 3), 9: (11, 7),
           10: (-10, 10), 11: (11, -16)}
for card in CARDS:                                                 # pins
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    px, py = proj(pin[0], pin[1])
    ox, oy = PIN_OFF.get(no, (0, 0))
    px, py = px + ox, py + oy
    r = 9
    d.ellipse([px - r, py - r, px + r, py + r], fill=REGIONS[region],
              outline=CREAM, width=1)
    text(px, py, str(no), F(ARCH_B, 10), fill=(255, 255, 255), anchor="mm")

ly = MAP_Y + MAP_H + 8
legend = ("Numbered pins = the 13 pictured stories - small dots = the "
          "briefs on Earth (no dot for Mercury: story 28 is in space)")
for ln in wrap(legend, F(ARCH_M, 10), 314):
    text(MX + 8, ly, ln, F(ARCH_M, 10), fill=MUTED)
    ly += 12

AO_X = MX + 330 + 8
AO_W = W - MX - AO_X
panel(AO_X, BOT_Y, AO_W, BOT_H)
ao_title = "ALSO ON SATURDAY 21 NOVEMBER - 27 MORE STORIES"
text(AO_X + 8, BOT_Y + 6, ao_title, fit(ao_title, ARCH_B, 12, AO_W - 16),
     fill=GOLD)

BF = F(ARCH_M, 10)
BNF = F(ARCH_B, 10)
COL_W = (AO_W - 16 - 14) // 2
brief_lines = []
for no, place, body in BRIEFS:
    num_w = tw("%d " % no, BNF)
    lines = wrap("%s %s" % (place, body), BF, COL_W - num_w)
    brief_lines.append((no, num_w, lines))
total_lines = sum(len(ls) for _, _, ls in brief_lines)
half = (total_lines + 1) // 2
cols, cur, count = [[], []], 0, 0
for item in brief_lines:
    if cur == 0 and count + len(item[2]) > half and count > 0:
        cur = 1
    cols[cur].append(item)
    count += len(item[2]) if cur == 0 else 0
for ci, col in enumerate(cols):
    bx = AO_X + 8 + ci * (COL_W + 14)
    by = BOT_Y + 24
    for no, num_w, lines in col:
        text(bx, by, "%d" % no, BNF, fill=GOLD)
        for ln in lines:
            text(bx + num_w, by, ln, BF, fill=(230, 224, 205))
            by += 10.2
        by += 0.5

# --- Date check + footer ------------------------------------------------------
DC_Y = BOT_Y + BOT_H + 6
d.rectangle([MX, DC_Y, MX + CW, DC_Y + 36], outline=ALERT, width=2)
lab = "DATE CHECK"
lab_w = tw(lab, F(ARCH_B, 10)) + 8
text(MX + 8, DC_Y + 5, lab, F(ARCH_B, 10), fill=ALERT)
# wrap the body with a narrower first line (it shares the line with the label)
words = DATE_CHECK.split()
first, rest = [], []
cur_w = CW - 16 - lab_w
for wd in words:
    trial = " ".join(first + [wd])
    if tw(trial, F(ARCH_M, 9)) <= cur_w or not first:
        first.append(wd)
    else:
        rest.append(wd)
text(MX + 8 + lab_w, DC_Y + 5, " ".join(first), F(ARCH_M, 9), fill=MUTED)
yy = DC_Y + 15
for ln in wrap(" ".join(rest), F(ARCH_M, 9), CW - 16)[:2]:
    text(MX + 8, yy, ln, F(ARCH_M, 9), fill=MUTED)
    yy += 10

FY = DC_Y + 41
text(MX, FY, FOOTER_L, F(ARCH_M, 9), fill=MUTED)
text(MX + CW, FY, FOOTER_R, F(ARCH_M, 9), fill=MUTED, anchor="ra")

# Save palette-quantised: the flat vector art survives 256 colours intact
# and the smaller file wins byte tie-breaks against the leaders' pages.
img_q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.Dither.NONE)
img_q.save(OUT, optimize=True)
print("saved", OUT, img.size)

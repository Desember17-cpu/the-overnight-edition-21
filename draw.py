#!/usr/bin/env python3
"""THE OVERNIGHT EDITION - challenger B4 (round 4 rebuild).

A one-page LIGHT broadsheet summing up Saturday 21 November 2026:
40 stories, 13 pictured cards, locator map, 27 briefs, numbers strip,
UTC timeline and a date check. Written fresh for round 4: the dark
navy page of round 3 is replaced by a cream-paper, black-ink design.

Facts come ONLY from the verified POOL21 pool. In particular card 8:
the EU ADOPTED 1bn euro of military aid (joint buying via the Peace
Facility; Britain pledges 1,000+ drones) - it was never "8bn paid".

Usage: python3 draw.py [A|B|C]  -> renders that layout variant to
entry.png (no argument = the duel winner). Deterministic, PIL only.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16
CW = W - 2 * MX

VARIANT = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VARIANT", "B")).upper()
if VARIANT not in ("A", "B", "C"):
    VARIANT = "B"

# --- Round-4 light theme ----------------------------------------------------
PAPER = (247, 241, 227)      # cream paper
PANEL = (255, 253, 246)      # card white
INK = (22, 22, 22)
SOFT = (74, 70, 62)          # deck grey-brown
RULE = (196, 186, 164)
RED = (178, 34, 44)          # accent red
BLACKBAND = (18, 18, 20)
GOLD = (176, 124, 22)
CAP = (22, 34, 52)           # caption band navy (data strip device)
LAND = (203, 178, 118)

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

img = Image.new("RGB", (W, H), PAPER)
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
    while size > floor and tw(text, F(name, size)) > max_w:
        size -= 1
    return F(name, size)


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def panel(x, y, w, h, fill=PANEL, outline=RULE):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline)

# --- POOL21 (verbatim facts) -------------------------------------------------
NUMBERS = [
    ("3", "weapons into Poland: two missiles, one jet drone"),
    ("42", "injured in the Kryvyi Rih strike, four of them children"),
    ("-5.28%", "Nasdaq's fall at Friday's close"),
    ("372,000", "people moved to shelters as Akvan hit"),
    ("€1BN", "EU military aid adopted for Ukraine"),
    ("159/1", "India at stumps in Wellington"),
]

TIMELINE = [
    ("Overnight", "Kryvyi Rih strike: two killed, 42 injured"),
    ("Morning", "Rutte flies to Warsaw over the missiles"),
    ("Midday", "Antalya: third COP31 draft due"),
    ("Afternoon", "Denmark expels the Russian attache"),
    ("Evening", "Stumps in Wellington: India 159/1"),
]

REGION_COUNTS = [("EUROPE", 16), ("ASIA", 6), ("AMERICAS", 8),
                 ("MIDEAST", 6), ("AFRICA", 1), ("OCEANIA", 1),
                 ("GLOBAL", 2)]

# no, place, region, topic, headline, deck, source tag, strip label, caption, pin
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "SECURITY",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. Rutte calls it a \"grave violation\"; "
     "Tusk calls it a deliberate provocation. (AP)",
     "AP - SOFX", "3 WEAPONS CROSS", "WARSAW - MISSILES DOWN", (21.0, 52.2)),
    (2, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday. The draft "
     "drops every fossil-fuel reference and the $120bn finance target; "
     "a third draft is due this morning. (AP)",
     "Ongoing - AP", "NO DEAL YET", "ANTALYA - COP31 OVERTIME", (30.7, 36.9)),
    (3, "NEW YORK", "AMERICAS", "MARKETS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged. "
     "(SimpleLife)",
     "Friday's close", "NASDAQ -5.28%", "NEW YORK - THE AI ROUT", (-74.0, 40.7)),
    (4, "KRYVYI RIH", "EUROPE", "WAR",
     "Russian strike kills two, injures 42",
     "An overnight strike kills two and injures 42, four of them children, "
     "the city's military chief says. It was one of Russia's largest "
     "attacks of the war. (AppiStos)",
     "City chief says", "2 DEAD - 42 HURT", "KRYVYI RIH - OVERNIGHT", (33.4, 47.9)),
    (5, "COPENHAGEN", "EUROPE", "PLOT",
     "Denmark exposes 'assassination plot'",
     "Russia 'planned and initiated' a bid to kill a Ukrainian-American "
     "rapper near Copenhagen, Denmark says. The Russian attache is "
     "expelled. (BBC)",
     "Denmark says - BBC", "ATTACHE EXPELLED", "COPENHAGEN - THE PLOT", (12.6, 55.7)),
    (6, "KYIV", "EUROPE", "WAR",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight are dead across Ukraine in the overnight barrage. "
     "The Austrian embassy is hit in Kyiv, and France calls for a UN "
     "Security Council meeting. (BBC)",
     "Officials' count", "400 DRONES - 110 MISSILES", "KYIV - THE BARRAGE", (30.5, 50.4)),
    (7, "ODISHA, INDIA", "ASIA", "CYCLONE",
     "After Akvan: 372,000 moved, no deaths",
     "A day after landfall, no deaths are reported and relief is under "
     "way. The storm weakens to a depression; schools stay shut through "
     "Saturday. (Ridhu Times)",
     "Relief reports", "372,000 MOVED", "ODISHA - AFTER AKVAN", (84.9, 19.3)),
    (8, "BRUSSELS", "EUROPE", "DEFENCE",
     "EU adopts €1bn military aid for Ukraine",
     "Joint buying runs via the Peace Facility. Britain pledges 1,000+ "
     "drones in a \u00a3260m package alongside the EU deal. (Reuters)",
     "Adopted - EU", "\u20ac1BN ADOPTED", "BRUSSELS - PEACE FACILITY", (4.3, 50.8)),
    (9, "NEW YORK", "AMERICAS", "CYBER",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "The banks report incidents at third-party vendors. Their core "
     "payment networks are unaffected, they say. (Reuters)",
     "Banks say", "3 NETWORKS HIT", "NEW YORK - PAYMENT NETWORKS", (-73.9, 40.8)),
    (10, "ULAANBAATAR", "ASIA", "POLITICS",
     "Mongolia's president resigns",
     "The resignation sets the stage for a snap election. It caps a week "
     "of political turmoil in the capital. (Reuters)",
     "Capital reports", "SNAP ELECTION NEXT", "ULAANBAATAR - TURMOIL WEEK", (106.9, 47.9)),
    (11, "THE HAGUE", "GLOBAL", "COURT",
     "Myanmar ruling rattles Israel's Gaza defence",
     "The world court's genocide verdict against Myanmar raises questions "
     "in Jerusalem over its own case, experts say. The ruling itself came "
     "on Thursday. (BBC)",
     "Experts say", "GENOCIDE VERDICT", "THE HAGUE - WORLD COURT", (4.3, 52.1)),
    (12, "JOHANNESBURG", "AFRICA", "POLITICS",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31% of the vote, its worst since 1994. It now races "
     "for coalition deals to stay in government. (BBC)",
     "Count - BBC", "ANC 31%", "JOHANNESBURG - THE COUNT", (28.0, -26.2)),
    (13, "WELLINGTON", "OCEANIA", "CRICKET",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209 in the first Test after the hosts "
     "made 368. Nicholls made 175 not out for the hosts. (ICC)",
     "Scorecard - ICC", "159/1 - DAY TWO", "WELLINGTON - DAY TWO", (174.8, -41.3)),
]

BRIEFS = [
    (14, "Kathmandu", "Nepal's new leader Balendra Shah faces an India test (BBC)"),
    (15, "Washington", "US releases more UFO footage filmed in the Middle East (BBC)"),
    (16, "Los Angeles", "Hyundai unveils the 2027 Elantra at the auto show (Fast Company)"),
    (17, "Cardiff", "Lauren Price beats Kotaskova to become undisputed champion (BBC)"),
    (18, "Paris", "Three police are sentenced over the beating of Michel Zecler (BBC)"),
    (19, "Oxford", "Life, 22 years minimum, for the Thames drowning murder (BBC)"),
    (20, "New York", "Nikhil Gupta gets 19+ years over the Sikh murder plot (BBC)"),
    (21, "Cincinnati", "Fiona the hippo dies after eating a hat (AP)"),
    (22, "Washington", "US sanctions four Iranians over oil revenues (OFAC)"),
    (23, "Hormuz", "A tanker is struck and on fire in the Strait of Hormuz (UKMTO)"),
    (24, "Los Angeles", "A jury convicts the man who started the Palisades Fire (AP)"),
    (25, "Frankfurt", "ECB names Boone and Brunnermeier for its Executive Board (Reuters)"),
    (26, "Buenos Aires", "Argentina's Senate backs a disability framework, 71-0 (AP)"),
    (27, "Riyadh", "A Saudi coalition intercepts Houthi missiles over Riyadh (Reuters)"),
    (28, "Barcelona", "A pill is hailed as a breakthrough for pancreatic cancer (Reuters)"),
    (29, "Gaza", "On World Children's Day, Palestinian children appeal for help (UN)"),
    (30, "Madrid", "Amnesty says Spanish police used excess force in the strike (AP)"),
    (31, "Rome", "Italian workers and students march against Meloni's government (AFP)"),
    (32, "Jeddah", "Saudi Arabia warns of thunderstorms through Tuesday (SPA)"),
    (33, "Kuala Lumpur", "Malaysia to send 10,000 Rohingya to Turkey for training (Reuters)"),
    (34, "Kharkiv", "Ukraine says it has finished a \"Bear Trap\" in the Kharkiv area (Ukrinform)"),
    (35, "Islamabad", "Pakistan's minerals are worth $8-10 trillion, its minister says (Reuters)"),
    (36, "Singapore", "US presses Singapore and Malaysia on Iran sanctions (Reuters)"),
    (37, "Paris", "France seeks a UN council meeting on the Kyiv strikes (AFP)"),
    (38, "Kyiv", "The war tally: 771 Ukrainians killed, 2,300+ missing (homevo)"),
    (39, "Ankara", "Turkey welcomes the World Court's Myanmar ruling (Anadolu)"),
    (40, "Turin", "ATP semis are set: Alcaraz v Shelton, Zverev v Medvedev (ATP)"),
]

BRIEF_PINS = {
    14: (85.3, 27.7, "ASIA"), 15: (-77.0, 38.9, "AMERICAS"),
    16: (-118.2, 34.1, "AMERICAS"), 17: (-3.2, 51.5, "EUROPE"),
    18: (2.4, 48.9, "EUROPE"), 19: (-1.3, 51.8, "EUROPE"),
    20: (-74.0, 40.7, "AMERICAS"), 21: (-84.5, 39.1, "AMERICAS"),
    22: (-77.1, 38.8, "AMERICAS"), 23: (56.3, 26.6, "MIDEAST"),
    24: (-118.3, 34.0, "AMERICAS"), 25: (8.7, 50.1, "EUROPE"),
    26: (-58.4, -34.6, "AMERICAS"), 27: (46.7, 24.6, "MIDEAST"),
    28: (2.2, 41.4, "EUROPE"), 29: (34.3, 31.5, "MIDEAST"),
    30: (-3.7, 40.4, "EUROPE"), 31: (12.5, 41.9, "EUROPE"),
    32: (39.2, 21.5, "MIDEAST"), 33: (101.7, 3.1, "ASIA"),
    34: (36.2, 49.9, "EUROPE"), 35: (73.1, 33.7, "ASIA"),
    36: (103.8, 1.35, "ASIA"), 37: (2.3, 48.8, "EUROPE"),
    38: (30.6, 50.5, "EUROPE"), 39: (32.9, 39.9, "MIDEAST"),
    40: (7.7, 45.1, "EUROPE"),
}

DATE_CHECK = (
    "Left out as Friday 20 November's news: Kyiv's three bridges hit, "
    "Cyclone Akvan's landfall at Gopalpur, COP31's final day ending with "
    "no deal, Asia's AI sell-off (Taipei -6.2%), the UK-EU reset deal and "
    "Phillips's 118 in the first innings. Not yet happened, so not shown: "
    "any final COP31 text, the ATP semi-final results and BepiColombo's "
    "entry into orbit around Mercury (due today)."
)
FOOTER_L = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# --- Flat strip scenes (fresh, simple, data-carrying) -------------------------
def _sky(x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=c)

def sc_missile(x, y, w, h):
    _sky(x, y, w, h, (96, 138, 84))
    for i in range(3):
        fy = y + 6 + i * (h - 10) // 3
        d.line([x + 4, fy, x + w - 4, fy - 3], fill=(70, 108, 58), width=2)
    d.polygon([(x + w // 3, y + h // 2 + 4), (x + w // 3 + 34, y + h // 2 - 4),
               (x + w // 3 + 46, y + h // 2), (x + w // 3 + 34, y + h // 2 + 6),
               (x + w // 3 + 4, y + h // 2 + 9)], fill=(200, 204, 210))
    d.polygon([(x + w // 3 + 40, y + h // 2 - 3), (x + w // 3 + 52, y + h // 2),
               (x + w // 3 + 40, y + h // 2 + 5)], fill=RED)
    d.line([x + w - 12, y + 3, x + w - 12, y + h - 3], fill=GOLD, width=2)

def sc_globe(x, y, w, h):
    _sky(x, y, w, h, (32, 70, 82))
    cx, cy = x + w // 2 - 12, y + h // 2
    r = max(12, h // 2 - 3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(29, 111, 184), outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=(255, 255, 255))
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    tx = x + w - 24
    t_top = y + max(2, h // 6)
    t_bot = y + h - max(6, h // 3)
    if t_bot > t_top:
        d.rectangle([tx, t_top, tx + 6, t_bot], fill=(255, 255, 255))
        d.rectangle([tx + 1, t_top + 3, tx + 5, t_bot], fill=RED)
    d.ellipse([tx - 3, y + h - 11, tx + 9, y + h - 1], fill=RED)

def sc_chart(x, y, w, h):
    _sky(x, y, w, h, (28, 40, 62))
    for i in range(1, 3):
        gy = y + h * i // 3
        d.line([x + 4, gy, x + w - 4, gy], fill=(58, 82, 112), width=1)
    pts = [(x + 8, y + h * 0.25), (x + w * 0.32, y + h * 0.36),
           (x + w * 0.55, y + h * 0.3), (x + w * 0.76, y + h * 0.6),
           (x + w - 10, y + h * 0.82)]
    d.line(pts, fill=(232, 90, 70), width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 10, ey - 7), (ex - 3, ey - 12)], fill=(232, 90, 70))

def sc_blast(x, y, w, h):
    _sky(x, y, w, h, (70, 78, 108))
    gy = y + h
    for i, bh in enumerate((0.6, 0.42, 0.72, 0.5)):
        bw = w // 6
        bx = x + i * bw
        top = gy - int(h * bh)
        d.rectangle([bx + 1, top, bx + bw - 1, gy], fill=(30, 40, 60))
    import math
    cx, cy = x + int(w * 0.78), y + int(h * 0.42)
    for ang in range(0, 360, 30):
        r1 = max(7, int(h * 0.3))
        d.line([cx, cy, cx + r1 * math.cos(math.radians(ang)),
                cy + r1 * math.sin(math.radians(ang))], fill=(232, 179, 60), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)

def sc_reticle(x, y, w, h):
    _sky(x, y, w, h, (56, 70, 96))
    gy = y + h
    for i, bh in enumerate((0.44, 0.6, 0.38, 0.55, 0.46)):
        bw = w // 5
        bx = x + i * bw
        top = gy - int(h * bh)
        d.polygon([(bx, top + 6), (bx + bw // 2, top), (bx + bw, top + 6),
                   (bx + bw, gy), (bx, gy)], fill=(122, 62, 52))
    cx, cy = x + w // 2, y + int(h * 0.44)
    r = max(10, int(h * 0.32))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=3)
    d.line([cx - r - 5, cy, cx - r + 4, cy], fill=RED, width=3)
    d.line([cx + r - 4, cy, cx + r + 5, cy], fill=RED, width=3)
    d.line([cx, cy - r - 5, cx, cy - r + 4], fill=RED, width=3)
    d.line([cx, cy + r - 4, cx, cy + r + 5], fill=RED, width=3)

def sc_barrage(x, y, w, h):
    _sky(x, y, w, h, (40, 64, 98))
    gy = y + h
    for i, bh in enumerate((0.5, 0.76, 0.4, 0.64, 0.48, 0.82, 0.54)):
        bw = w // 7
        bx = x + i * bw
        top = gy - int(h * bh)
        d.rectangle([bx + 1, top, bx + bw - 1, gy], fill=(18, 30, 48))
        for wy in range(top + 4, gy - 4, 7):
            for wx in range(bx + 4, bx + bw - 4, 8):
                if (wx * 7 + wy * 13) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 3], fill=(232, 179, 60))
    for i in range(3):
        ax = x + int(w * (0.16 + 0.3 * i))
        d.arc([ax, y + 1, ax + int(w * 0.22), y + int(h * 0.6)], 200, 325, fill=(232, 90, 70), width=2)

def sc_cyclone(x, y, w, h):
    _sky(x, y, w, h, (52, 88, 112))
    cx, cy = x + w // 2, y + h // 2
    base = min(32, int(h * 0.46))
    for r in (base, int(base * 0.78), int(base * 0.56), int(base * 0.36)):
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], 20, 300, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=(232, 179, 60))
    d.polygon([(x, y + h), (x + w // 3, y + h - 10), (x + w, y + h)], fill=(30, 132, 73))

def sc_eu(x, y, w, h):
    _sky(x, y, w, h, (24, 54, 110))
    cy = y + h // 2
    r = max(8, int(h * 0.32))
    cx = x + int(w * 0.3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 179, 60), outline=(255, 255, 255))
    text(cx, cy, "\u20ac", fit("\u20ac", ARCH_B, int(r * 1.4), 2 * r - 2), fill=CAP, anchor="mm")
    d.line([x + int(w * 0.48), cy, x + int(w * 0.6), cy], fill=(255, 255, 255), width=3)
    d.polygon([(x + int(w * 0.6), cy - 4), (x + int(w * 0.6) + 7, cy),
               (x + int(w * 0.6), cy + 4)], fill=(255, 255, 255))
    fx = x + int(w * 0.66)
    d.rectangle([fx, cy - 7, fx + 26, cy], fill=(52, 110, 180))
    d.rectangle([fx, cy, fx + 26, cy + 7], fill=(232, 179, 60))

def sc_cyber(x, y, w, h):
    _sky(x, y, w, h, (28, 40, 62))
    cols = ((29, 111, 184), (240, 236, 224), (202, 111, 30))
    for i in range(3):
        bx = x + int(w * (0.06 + 0.24 * i))
        by = y + int(h * 0.18)
        cw_ = min(58, int(w * 0.28))
        ch_ = max(14, int(h * 0.5))
        d.rectangle([bx, by, bx + cw_, by + ch_], fill=cols[i])
        d.rectangle([bx + 5, by + 5, bx + 15, by + 11], fill=(232, 179, 60))
    tx, ty = x + int(w * 0.84), y + int(h * 0.14)
    ts = max(12, int(h * 0.4))
    d.polygon([(tx, ty + ts), (tx + ts // 2, ty), (tx + ts, ty + ts)], fill=(232, 179, 60))

def sc_ger(x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.62)], fill=(110, 160, 200))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(150, 140, 80))
    cx, gy = x + w // 2, y + h
    gw, gh = int(w * 0.3), max(13, int(h * 0.52))
    d.rectangle([cx - gw // 2, gy - gh, cx + gw // 2, gy], fill=(240, 236, 224))
    d.polygon([(cx - gw // 2 - 4, gy - gh), (cx + gw // 2 + 4, gy - gh),
               (cx, gy - gh - max(5, h // 8))], fill=RED)
    d.rectangle([cx - 4, gy - gh + 6, cx + 4, gy], fill=(122, 62, 52))

def sc_court(x, y, w, h):
    _sky(x, y, w, h, (96, 104, 128))
    cx = x + w // 2
    tw_ = int(w * 0.62)
    ped = max(5, min(h // 3, h - 13))
    d.polygon([(cx - tw_ // 2, y + ped), (cx + tw_ // 2, y + ped), (cx, y + 2)], fill=(240, 236, 224))
    for i in range(4):
        colx = cx - tw_ // 2 + 6 + i * (tw_ - 12) // 3
        d.rectangle([colx - 3, y + ped + 4, colx + 3, y + h - 4], fill=(240, 236, 224))
    d.rectangle([cx - tw_ // 2, y + h - 4, cx + tw_ // 2, y + h - 1], fill=(240, 236, 224))

def sc_ballot(x, y, w, h):
    _sky(x, y, w, h, (52, 92, 140))
    cx = x + w // 2
    bw, bh = int(w * 0.4), max(18, h // 2)
    bx, by = cx - bw // 2, y + h - bh - 4
    d.rectangle([bx, by, bx + bw, by + bh], fill=(240, 236, 224), outline=CAP, width=2)
    d.rectangle([bx + 8, by + 5, bx + bw - 8, by + 9], fill=CAP)
    d.polygon([(cx - 9, y + 4), (cx + 9, y + 4), (cx + 5, by + 7), (cx - 5, by + 7)], fill=(255, 255, 255))
    d.rectangle([bx, by + bh - 8, bx + bw, by + bh], fill=(29, 111, 184))

def sc_cricket(x, y, w, h):
    _sky(x, y, w, h, (52, 122, 74))
    pw = int(w * 0.3)
    px = x + (w - pw) // 2
    d.rectangle([px, y + 5, px + pw, y + h - 4], fill=(222, 198, 140))
    sx = px + pw - 15
    for i in range(3):
        d.line([sx + i * 5, y + h - 20, sx + i * 5, y + h - 7], fill=(240, 220, 160), width=2)
    d.ellipse([x + w - 28, y + 8, x + w - 18, y + 18], fill=RED)

SCENES = {1: sc_missile, 2: sc_globe, 3: sc_chart, 4: sc_blast,
          5: sc_reticle, 6: sc_barrage, 7: sc_cyclone, 8: sc_eu,
          9: sc_cyber, 10: sc_ger, 11: sc_court, 12: sc_ballot,
          13: sc_cricket}
CAP_H = 15

def draw_strip(card, x, y, w, h):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    col = REGIONS[region]
    d.rectangle([x, y, x + w, y + h], fill=CAP)
    d.rectangle([x, y, x + w, y + 3], fill=col)
    SCENES[no](x, y + 3, w, h - 3 - CAP_H)
    tf = fit(tag, ARCH_B, 8, w * 0.48, floor=6)
    tag_w = tw(tag, tf) + 9
    d.rectangle([x + w - tag_w - 4, y + 4, x + w - 4, y + 15], fill=CAP)
    text(x + w - tag_w + 1, y + 9.5, tag, tf, fill=(255, 255, 255), anchor="lm")
    lf = fit(label, ARCH_B, 11 if w > 250 else 9, w - 60, floor=7)
    lw_ = tw(label, lf) + 11
    ly = y + h - CAP_H - 14
    d.rectangle([x + 5, ly, x + 5 + lw_, ly + 12], fill=CAP)
    text(x + 10, ly + 6, label, lf, fill=(245, 197, 24), anchor="lm")
    d.rectangle([x, y + h - CAP_H, x + w, y + h], fill=CAP)
    bf = fit(caption, ARCH_B, 9, w - 10, floor=7)
    text(x + w // 2, y + h - CAP_H // 2, caption, bf, fill=(200, 208, 220), anchor="mm")

def draw_card(card, x, y, w, h, strip_h, head_size, deck_size, head_font=PLAYFAIR):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    panel(x, y, w, h)
    draw_strip(card, x + 5, y + 5, w - 10, strip_h)
    ry = y + 5 + strip_h + 4
    text(x + 7, ry, "%d  %s - %s - %s" % (no, place, region, topic),
         F(ARCH_B, 9), fill=REGIONS[region])
    hy = ry + 12
    hf = F(head_font, head_size)
    for ln in wrap(headline, hf, w - 14)[:2]:
        text(x + 7, hy, ln, hf, fill=INK)
        hy += head_size + 3
    dy = hy + 1
    df = F(ARCH_M, deck_size)
    max_lines = max(1, int((y + h - 4 - dy) // (deck_size + 2.5)))
    for ln in wrap(deck, df, w - 14)[:max_lines]:
        text(x + 7, dy, ln, df, fill=SOFT)
        dy += deck_size + 2.5

# --- Header -------------------------------------------------------------------
HDR_DARK = (VARIANT == "B")
Y = 0
if HDR_DARK:
    d.rectangle([0, 0, W, 118], fill=BLACKBAND)
    text(MX + 2, 10, "SATURDAY 21 NOVEMBER 2026", F(ARCH_B, 11), fill=(245, 197, 24))
    kr = "40 STORIES - 7 REGIONS - EVERY ONE DATED TODAY"
    text(MX + CW - 2, 10, kr, F(ARCH_B, 11), fill=(245, 197, 24), anchor="ra")
    mf = fit("THE OVERNIGHT EDITION", PLAYFAIR, 52, CW)
    text(MX + CW // 2, 30, "THE OVERNIGHT EDITION", mf, fill=(247, 241, 227), anchor="ma")
    sub = "Missiles land in Poland - COP31 slips into overtime - Wall Street falls into correction - Denmark exposes a plot"
    text(MX + CW // 2, 92, sub, fit(sub, ARCH_M, 11, CW - 20), fill=(200, 208, 220), anchor="ma")
    Y = 124
else:
    d.rectangle([MX, 6, MX + CW, 27], fill=INK)
    text(MX + 8, 16, "SATURDAY 21 NOVEMBER 2026", F(ARCH_B, 11), fill=(255, 255, 255), anchor="lm")
    kr = "40 STORIES - 7 REGIONS - EVERY ONE DATED TODAY"
    text(MX + CW - 8, 16, kr, fit(kr, ARCH_B, 11, 480), fill=(255, 255, 255), anchor="rm")
    mf = fit("THE OVERNIGHT EDITION", PLAYFAIR, 50, CW)
    text(MX + CW // 2, 32, "THE OVERNIGHT EDITION", mf,
         fill=RED if VARIANT == "C" else INK, anchor="ma")
    d.line([MX, 88, MX + CW, 88], fill=INK, width=3)
    sub = "Missiles land in Poland - COP31 slips into overtime - Wall Street falls into correction - Denmark exposes a plot"
    text(MX + CW // 2, 93, sub, fit(sub, ARCH_M, 11, CW - 20), fill=SOFT, anchor="ma")
    Y = 110

# Hook band: top-3 stories
d.rectangle([MX, Y, MX + CW, Y + 26], fill=RED)
hook = "TOP STORIES  1  MISSILES LAND IN POLAND   -   2  COP31 IN OVERTIME, NO DEAL   -   3  WALL STREET IN CORRECTION"
text(MX + CW // 2, Y + 13, hook, fit(hook, ARCH_B, 12, CW - 20), fill=(255, 255, 255), anchor="mm")
Y += 30

# Timeline
panel(MX, Y, CW, 26)
cell = CW / 5.0
for i, (lab, ev) in enumerate(TIMELINE):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 4, cx0, Y + 24], fill=RULE, width=1)
    text(cx0 + 7, Y + 3, lab.upper(), F(ARCH_B, 9), fill=RED)
    text(cx0 + 7, Y + 14, wrap(ev, F(ARCH_M, 9), cell - 12)[0], F(ARCH_M, 9), fill=INK)
Y += 32

# Numbers strip
d.rectangle([MX, Y, MX + CW, Y + 44], fill=INK)
cell = CW / 6.0
for i, (num, cap) in enumerate(NUMBERS):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 6, cx0, Y + 38], fill=(70, 70, 70), width=1)
    nfont = ARCH_B if "\u20ac" in num else PLAYFAIR
    text(cx0 + 8, Y + 4, num, fit(num, nfont, 20, cell - 14), fill=(245, 197, 24))
    for j, ln in enumerate(wrap(cap, F(ARCH_M, 8), cell - 14)[:2]):
        text(cx0 + 8, Y + 27 + j * 8.5, ln, F(ARCH_M, 8), fill=(220, 220, 220))
Y += 48

# Region counts line
cx = MX
text(cx, Y + 9, "WHERE:", F(ARCH_B, 10), fill=SOFT, anchor="lm")
cx += int(tw("WHERE:", F(ARCH_B, 10))) + 10
for name, n in REGION_COUNTS:
    lab = "%s %d" % (name, n)
    lf = F(ARCH_B, 10)
    wch = int(tw(lab, lf)) + 22
    d.rectangle([cx, Y, cx + wch, Y + 18], fill=PANEL, outline=RULE)
    d.ellipse([cx + 5, Y + 5, cx + 13, Y + 13], fill=REGIONS[name])
    text(cx + 16, Y + 9, lab, lf, fill=INK, anchor="lm")
    cx += wch + 7
Y += 22

# --- Lead zone ------------------------------------------------------------------
LEAD_Y = Y
LEAD_H = 186
if VARIANT == "B":      # hero: card 1 wide, cards 2-3 stacked
    draw_card(CARDS[0], MX, LEAD_Y, 500, LEAD_H, 74, 23, 12)
    draw_card(CARDS[1], MX + 508, LEAD_Y, CW - 508, 91, 30, 14, 9, ARCH_B)
    draw_card(CARDS[2], MX + 508, LEAD_Y + 95, CW - 508, 91, 30, 14, 9, ARCH_B)
elif VARIANT == "C":    # banner: card 1 across, cards 2-3 below side by side
    draw_card(CARDS[0], MX, LEAD_Y, CW, 92, 34, 17, 11)
    draw_card(CARDS[1], MX, LEAD_Y + 96, (CW - 8) // 2, 90, 30, 14, 10, ARCH_B)
    draw_card(CARDS[2], MX + (CW - 8) // 2 + 8, LEAD_Y + 96, (CW - 8) // 2, 90, 30, 14, 10, ARCH_B)
else:                   # A: three equal leads
    LW = (CW - 16) // 3
    for i, card in enumerate(CARDS[:3]):
        draw_card(card, MX + i * (LW + 8), LEAD_Y, LW, LEAD_H, 68, 20, 11)
Y = LEAD_Y + LEAD_H + 6

# --- Feature grid: cards 4-13, 2 rows x 5 ---------------------------------------
FEAT_W = (CW - 20) // 5
ROW_H = 124
for k, card in enumerate(CARDS[3:]):
    cx0 = MX + (k % 5) * (FEAT_W + 5)
    cy0 = Y + (k // 5) * (ROW_H + 6)
    draw_card(card, cx0, cy0, FEAT_W, ROW_H, 36, 11, 10, ARCH_B)
Y += 2 * ROW_H + 6 + 6

# --- Bottom: map + briefs (swapped in variant B) --------------------------------
BOT_H = 240
MAP_W_P = 330
if VARIANT == "B":
    AO_X, AO_W = MX, CW - MAP_W_P - 8
    MAP_PX = MX + CW - MAP_W_P
else:
    MAP_PX = MX
    AO_X, AO_W = MX + MAP_W_P + 8, CW - MAP_W_P - 8

panel(MAP_PX, Y, MAP_W_P, BOT_H)
text(MAP_PX + 8, Y + 5, "WHERE IT HAPPENED", F(ARCH_B, 12), fill=RED)
MAP_X, MAP_Y, MAP_W, MAP_H = MAP_PX + 8, Y + 26, MAP_W_P - 16, 152
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(240, 233, 210))

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

for no, (lo, la, reg) in BRIEF_PINS.items():
    px, py = proj(lo, la)
    d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REGIONS[reg])

PIN_OFF = {1: (16, -9), 2: (-13, 10), 3: (-5, -3), 4: (4, 18),
           5: (-15, -17), 6: (19, 6), 8: (-20, 3), 9: (11, 7),
           11: (11, -15)}
for card in CARDS:
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    px, py = proj(pin[0], pin[1])
    ox, oy = PIN_OFF.get(no, (0, 0))
    px, py = px + ox, py + oy
    r = 9  # pin diameter 18px
    d.ellipse([px - r, py - r, px + r, py + r], fill=REGIONS[region],
              outline=(255, 255, 255), width=1)
    text(px, py, str(no), F(ARCH_B, 10), fill=(255, 255, 255), anchor="mm")

ly = MAP_Y + MAP_H + 7
legend = "Numbered pins = the 13 pictured stories - small dots = the briefs."
for ln in wrap(legend, F(ARCH_M, 10), MAP_W_P - 16):
    text(MAP_PX + 8, ly, ln, F(ARCH_M, 10), fill=SOFT)
    ly += 12
giant = [("\u20ac1BN", "EU aid adopted (card 8)"), ("372,000", "moved in Odisha (card 7)")]
gx = MAP_PX + 8
for num, cap in giant:
    gfont = ARCH_B if "\u20ac" in num else PLAYFAIR
    text(gx, ly + 2, num, F(gfont, 18), fill=INK)
    text(gx, ly + 23, cap, F(ARCH_M, 8), fill=SOFT)
    gx += (MAP_W_P - 16) // 2

panel(AO_X, Y, AO_W, BOT_H)
ao_title = "ALSO ON SATURDAY 21 NOVEMBER - 27 MORE STORIES"
text(AO_X + 8, Y + 5, ao_title, fit(ao_title, ARCH_B, 12, AO_W - 16), fill=RED)
BF, BNF = F(ARCH_M, 9), F(ARCH_B, 9)
COL_W = (AO_W - 16 - 14) // 2
brief_lines = []
for no, place, body in BRIEFS:
    num_w = tw("%d " % no, BNF)
    brief_lines.append((no, num_w, wrap("%s %s" % (place, body), BF, COL_W - num_w)))
total_lines = sum(len(ls) for _, _, ls in brief_lines)
half = (total_lines + 1) // 2
cols, cur, count = [[], []], 0, 0
for item in brief_lines:
    if cur == 0 and count + len(item[2]) > half and count > 0:
        cur = 1
    cols[cur].append(item)
    if cur == 0:
        count += len(item[2])
for ci, col in enumerate(cols):
    bx = AO_X + 8 + ci * (COL_W + 14)
    by = Y + 24
    for no, num_w, lines in col:
        text(bx, by, "%d" % no, BNF, fill=RED)
        for ln in lines:
            text(bx + num_w, by, ln, BF, fill=INK)
            by += 9.2
        by += 0.4
Y += BOT_H + 6

# --- Date check + footer ---------------------------------------------------------
d.rectangle([MX, Y, MX + CW, Y + 30], outline=RED, width=2)
lab = "DATE CHECK"
lab_w = tw(lab, F(ARCH_B, 10)) + 8
text(MX + 8, Y + 4, lab, F(ARCH_B, 10), fill=RED)
words = DATE_CHECK.split()
first, rest, cur_w = [], [], CW - 16 - lab_w
for wd in words:
    trial = " ".join(first + [wd])
    if tw(trial, F(ARCH_M, 9)) <= cur_w or not first:
        first.append(wd)
    else:
        rest.append(wd)
text(MX + 8 + lab_w, Y + 4, " ".join(first), F(ARCH_M, 9), fill=SOFT)
yy = Y + 13
for ln in wrap(" ".join(rest), F(ARCH_M, 9), CW - 16)[:2]:
    text(MX + 8, yy, ln, F(ARCH_M, 9), fill=SOFT)
    yy += 9.5
Y += 35
text(MX, Y, FOOTER_L, F(ARCH_M, 9), fill=SOFT)
text(MX + CW, Y, FOOTER_R, F(ARCH_M, 9), fill=SOFT, anchor="ra")

img_q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
img_q.save(OUT, optimize=True)
print("saved variant", VARIANT, OUT, os.path.getsize(OUT))

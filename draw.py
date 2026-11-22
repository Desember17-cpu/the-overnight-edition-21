#!/usr/bin/env python3
"""THE OVERNIGHT EDITION - round 5 (NI21), account @desember179.

A one-page cream-paper broadsheet for Saturday 21 November 2026, built
to the pixel-measured structure of NI21's #1 (see BEDAH-TOP1-NI21.md):
claims bar, the DATE as the only masthead, a THE DAY IN PARTS bar,
three equal lead columns, ten mini cards (13 pictured in all), a
dot-matrix locator map, hard one-line briefs, a DATE CHECK box with
dated discards plus one Unverified clause, and a one-line footer.

Facts come ONLY from the verified POOL21 pool (40 stories: 13 pictured
cards + 27 briefs). The pool contains no further verified stories, so
the page carries 40 stories, not 44 - see BUILD.md.

Usage: python3 draw.py  -> renders entry.png beside this file.
Deterministic, PIL only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 14
CW = W - 2 * MX  # 996, content x 14..1010

PAPER = (245, 241, 224)      # cream paper (as sampled from #1)
PANEL = (252, 250, 242)
INK = (22, 22, 22)
SOFT = (84, 78, 66)
RULE = (205, 196, 172)
RED = (192, 40, 25)          # accent red (as sampled from #1)
BLACK = (16, 16, 18)
WHITE = (255, 255, 255)
GOLD = (232, 179, 60)

REGIONS = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (202, 111, 30),
    "AMERICAS": (30, 132, 73),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}
CONTINENT = {
    "EUROPE": (37, 99, 178), "ASIA": (216, 118, 28),
    "AMERICAS": (34, 139, 76), "AFRICA": (196, 148, 22),
    "OCEANIA": (16, 138, 133), "MIDEAST": (125, 60, 152),
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


def fit(text, name, size, max_w, floor=7):
    while size > floor and tw(text, F(name, size)) > max_w:
        size -= 1
    return size


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


# --- POOL21 data (verified facts only) ---------------------------------------
# no, place, region, category, slug, chip, headline, deck, pin lon/lat
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "SECURITY", "3 WEAPONS CROSS",
     "CONFIRMED \u2013 AP",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east; "
     "Rutte calls it a \u201cgrave violation\u201d.",
     (21.0, 52.2)),
    (2, "ANTALYA", "GLOBAL", "CLIMATE", "NO DEAL YET",
     "CONFIRMED \u2013 AP",
     "COP31 runs into overtime, no deal yet",
     "Talks ran past Friday's close into Saturday. The draft drops every "
     "fossil-fuel reference and the $120bn target.",
     (30.7, 36.9)),
    (3, "NEW YORK", "AMERICAS", "MARKETS", "NASDAQ -5.28%",
     "REPORTED \u2013 SIMPLELIFE",
     "Wall Street enters correction in AI rout",
     "The S&P 500 fell about 3.7% on Friday, into correction territory. "
     "The Nasdaq dropped 5.28% as AI shares plunged.",
     (-74.0, 40.7)),
    (4, "KRYVYI RIH", "EUROPE", "WAR", "2 DEAD \u00b7 42 HURT",
     "REPORTED \u2013 APPISTOS",
     "Russian strike kills two, injures 42",
     "Two killed, 42 injured \u2014 four of them children \u2014 in the "
     "overnight strike.",
     (33.4, 47.9)),
    (5, "COPENHAGEN", "EUROPE", "PLOT", "ATTACHE EXPELLED",
     "REPORTED \u2013 BBC",
     "Denmark exposes 'assassination plot'",
     "Denmark says Russia planned a bid to kill a rapper. The attache "
     "is expelled.",
     (12.6, 55.7)),
    (6, "KYIV", "EUROPE", "WAR", "400 DRONES \u00b7 110 MISSILES",
     "CONFIRMED \u2013 BBC",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight dead across Ukraine. The Austrian embassy is hit "
     "in Kyiv.",
     (30.5, 50.4)),
    (7, "ODISHA, INDIA", "ASIA", "CYCLONE", "372,000 MOVED",
     "REPORTED \u2013 RIDHU TIMES",
     "After Akvan: 372,000 moved, no deaths",
     "No deaths reported a day after landfall. Schools stay shut "
     "through Saturday.",
     (84.9, 19.3)),
    (8, "BRUSSELS", "EUROPE", "DEFENCE", "\u20ac1BN ADOPTED",
     "CONFIRMED \u2013 REUTERS",
     "EU adopts \u20ac1bn military aid for Ukraine",
     "Joint buying via the Peace Facility. Britain pledges 1,000+ "
     "drones alongside.",
     (4.3, 50.8)),
    (9, "NEW YORK", "AMERICAS", "CYBER", "3 NETWORKS HIT",
     "REPORTED \u2013 REUTERS",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "Incidents hit third-party vendors. Core payment networks are "
     "unaffected.",
     (-73.9, 40.8)),
    (10, "ULAANBAATAR", "ASIA", "POLITICS", "SNAP ELECTION NEXT",
     "REPORTED \u2013 REUTERS",
     "Mongolia's president resigns",
     "The resignation sets up a snap election. It caps a week of "
     "turmoil.",
     (106.9, 47.9)),
    (11, "THE HAGUE", "GLOBAL", "COURT", "GENOCIDE VERDICT",
     "REPORTED \u2013 BBC",
     "Myanmar ruling rattles Israel's Gaza defence",
     "Experts say the genocide verdict raises questions for Israel's "
     "own case.",
     (4.3, 52.1)),
    (12, "JOHANNESBURG", "AFRICA", "POLITICS", "ANC 31%",
     "CONFIRMED \u2013 BBC",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31%, its worst since 1994. Coalition talks now "
     "race on.",
     (28.0, -26.2)),
    (13, "WELLINGTON", "OCEANIA", "CRICKET", "159/1 \u00b7 DAY TWO",
     "CONFIRMED \u2013 ICC",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209; the hosts made 368. Nicholls: "
     "175 not out.",
     (174.8, -41.3)),
]

DAYPARTS = [
    ("OVERNIGHT", "Kryvyi Rih strike: two killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due after talks"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

# no, bold lead-in, tail  (POOL21 briefs 14-40, cut to ONE hard line each)
BRIEFS = [
    (14, "Kathmandu:", "Nepal leader Balendra Shah faces India test"),
    (15, "Washington:", "US releases more UFO footage from Middle East"),
    (16, "Los Angeles:", "Hyundai unveils the 2027 Elantra at auto show"),
    (17, "Cardiff:", "Lauren Price beats Kotaskova, undisputed champion"),
    (18, "Paris:", "Three police sentenced over Michel Zecler beating"),
    (19, "Oxford:", "Life, 22 years minimum, for Thames drowning murder"),
    (20, "New York:", "Nikhil Gupta gets 19+ years in Sikh murder plot"),
    (21, "Cincinnati:", "Fiona the hippo dies after eating a hat"),
    (22, "Washington:", "US sanctions four Iranians over oil revenues"),
    (23, "Hormuz:", "A tanker is struck and on fire in the strait"),
    (24, "Los Angeles:", "Jury convicts the man who started Palisades Fire"),
    (25, "Frankfurt:", "ECB names Boone, Brunnermeier to Executive Board"),
    (26, "Buenos Aires:", "Senate backs disability framework, 71-0"),
    (27, "Riyadh:", "Saudi coalition intercepts Houthi missiles"),
    (28, "Barcelona:", "Pill hailed as pancreatic cancer breakthrough"),
    (29, "Gaza:", "Children appeal for help on World Children's Day"),
    (30, "Madrid:", "Amnesty: police used excess force in the strike"),
    (31, "Rome:", "Workers, students march against Meloni government"),
    (32, "Jeddah:", "Saudi warns of thunderstorms through Tuesday"),
    (33, "Kuala Lumpur:", "10,000 Rohingya to Turkey for training"),
    (34, "Kharkiv:", "Ukraine says its \u201cBear Trap\u201d is finished"),
    (35, "Islamabad:", "Minerals worth $8-10 trillion, minister says"),
    (36, "Singapore:", "US presses Singapore, Malaysia on Iran sanctions"),
    (37, "Paris:", "France seeks UN council meeting on Kyiv strikes"),
    (38, "Kyiv:", "War tally: 771 killed, 2,300+ missing"),
    (39, "Ankara:", "Turkey welcomes World Court's Myanmar ruling"),
    (40, "Turin:", "ATP semis set: Alcaraz-Shelton, Zverev-Medvedev"),
]

DATE_DISCARDS = (
    "Left out on purpose \u2014 not Saturday's news: Kyiv's three bridges hit "
    "(Friday 20 Nov) \u00b7 Cyclone Akvan's landfall at Gopalpur (20 Nov) \u00b7 "
    "COP31's final day ending with no deal (20 Nov) \u00b7 Asia's AI sell-off, "
    "Taipei -6.2% (20 Nov) \u00b7 Phillips's 118 in the first innings (20 Nov)."
)
DATE_UNVERIFIED = (
    "Unverified: Denmark's assassination-plot claim \u2014 Copenhagen says "
    "Russia planned and initiated it; it is shown as Denmark's claim, "
    "not as established fact."
)
DATE_NOTYET = (
    "Not yet happened, so not shown: any final COP31 text, the ATP "
    "semi-final results and BepiColombo's entry into orbit around "
    "Mercury (due today)."
)
FOOTER = (
    "Every story here happened, or was first reported, on Saturday "
    "21 November 2026 \u00b7 Outlets used: AP \u00b7 BBC \u00b7 Reuters \u00b7 ICC \u00b7 AFP \u00b7 UN \u00b7 "
    "OFAC \u00b7 UKMTO \u00b7 SPA \u00b7 Anadolu \u00b7 Ukrinform \u00b7 ATP \u00b7 Fast Company \u00b7 "
    "SimpleLife \u00b7 AppiStos \u00b7 Ridhu Times \u00b7 homevo \u00b7 Original drawings"
)

# --- Scenes: flat, bright, max 3 large elements, subject >=50% of height -----
def sc_missiles(x, y, w, h):  # card 1 - two big missiles + one jet drone
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 238))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(96, 160, 84))
    for bx, by, ang in ((0.30, 0.52, -18), (0.58, 0.40, -18)):
        cx, cy = x + w * bx, y + h * by
        d.polygon([(cx - 34, cy + 10), (cx + 22, cy - 12), (cx + 38, cy - 10),
                   (cx + 24, cy + 2), (cx - 20, cy + 16)], fill=(238, 240, 244),
                  outline=(30, 34, 44))
        d.polygon([(cx + 24, cy - 12), (cx + 40, cy - 11), (cx + 25, cy + 1)],
                  fill=RED)
        d.polygon([(cx - 34, cy + 10), (cx - 44, cy + 20), (cx - 28, cy + 18)],
                  fill=RED)
    cx, cy = x + w * 0.82, y + h * 0.30  # jet drone, big X silhouette
    d.polygon([(cx - 26, cy - 12), (cx + 26, cy + 12), (cx + 18, cy + 16),
               (cx - 26, cy - 4)], fill=(30, 34, 44))
    d.polygon([(cx - 26, cy + 12), (cx + 26, cy - 12), (cx + 18, cy - 16),
               (cx - 26, cy + 4)], fill=(30, 34, 44))

def sc_globe(x, y, w, h):  # card 2 - one huge globe + clock hand ring
    d.rectangle([x, y, x + w, y + h], fill=(240, 220, 186))
    cx, cy, r = x + w // 2, y + h // 2, 28
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 118, 178))
    d.ellipse([cx - 21, cy - 18, cx - 5, cy - 4], fill=(52, 168, 92))
    d.ellipse([cx + 4, cy + 2, cx + 23, cy + 19], fill=(52, 168, 92))
    d.ellipse([cx - 8, cy + 10, cx + 4, cy + 21], fill=(52, 168, 92))
    d.line([cx, cy, cx, cy - 19], fill=WHITE, width=4)
    d.line([cx, cy, cx + 13, cy + 8], fill=RED, width=4)

def sc_chart(x, y, w, h):  # card 3 - three big falling bars + plunge line
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    bw = w // 5
    for i, bh in enumerate((0.78, 0.55, 0.30)):
        bx = x + int(w * 0.10) + i * (bw + 8)
        d.rectangle([bx, y + h - int(h * bh) - 4, bx + bw, y + h - 4],
                    fill=(232, 90, 70) if i == 2 else (240, 190, 90))
    pts = [(x + 8, y + 8), (x + w * 0.38, y + h * 0.34),
           (x + w * 0.62, y + h * 0.30), (x + w - 10, y + h * 0.78)]
    d.line(pts, fill=INK, width=3)

def sc_blast(x, y, w, h):  # card 4 - skyline + one huge blast
    d.rectangle([x, y, x + w, y + h], fill=(208, 204, 222))
    for i, bh in enumerate((0.42, 0.58, 0.36, 0.5)):
        bw = w // 4
        bx = x + i * bw
        d.rectangle([bx + 1, y + h - int(h * bh), bx + bw - 1, y + h],
                    fill=(28, 32, 52))
    import math
    cx, cy = x + int(w * 0.70), y + int(h * 0.40)
    for ang in range(0, 360, 24):
        r1 = 24 if ang % 48 == 0 else 16
        d.line([cx, cy, cx + r1 * math.cos(math.radians(ang)),
                cy + r1 * math.sin(math.radians(ang))], fill=GOLD, width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)

def sc_reticle(x, y, w, h):  # card 5 - rooftops + one huge reticle
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 238))
    for i, bh in enumerate((0.40, 0.52, 0.44)):
        bw = w // 3
        bx = x + i * bw
        d.polygon([(bx, y + h - int(h * bh) + 8), (bx + bw // 2, y + h - int(h * bh)),
                   (bx + bw, y + h - int(h * bh) + 8), (bx + bw, y + h),
                   (bx, y + h)], fill=(150, 84, 64))
    cx, cy, r = x + w // 2, y + h // 2 - 2, 25
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=4)
    d.line([cx - r - 6, cy, cx - r + 6, cy], fill=RED, width=4)
    d.line([cx + r - 6, cy, cx + r + 6, cy], fill=RED, width=4)
    d.line([cx, cy - r - 6, cx, cy - r + 6], fill=RED, width=4)
    d.line([cx, cy + r - 6, cx, cy + r + 6], fill=RED, width=4)

def sc_barrage(x, y, w, h):  # card 6 - skyline + three big incoming trails
    d.rectangle([x, y, x + w, y + h], fill=(206, 214, 226))
    for i, bh in enumerate((0.36, 0.55, 0.42, 0.62, 0.46, 0.52)):
        bw = w // 6
        bx = x + i * bw
        d.rectangle([bx + 1, y + h - int(h * bh), bx + bw - 1, y + h],
                    fill=(14, 24, 42))
        d.rectangle([bx + bw // 2 - 2, y + h - int(h * bh) + 6,
                     bx + bw // 2 + 2, y + h - int(h * bh) + 11], fill=GOLD)
    for i in range(3):
        sx = x + int(w * (0.14 + 0.30 * i))
        d.line([sx, y + 4, sx + int(w * 0.13), y + int(h * 0.52)],
               fill=(232, 90, 70), width=5)
        ex, ey = sx + int(w * 0.13), y + int(h * 0.52)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=GOLD)

def sc_cyclone(x, y, w, h):  # card 7 - one huge spiral + sea
    d.rectangle([x, y, x + w, y + h], fill=(182, 214, 224))
    cx, cy = x + w // 2, y + h // 2 - 3
    for r in (27, 21, 15, 9):
        d.arc([cx - r, cy - int(r * 0.74), cx + r, cy + int(r * 0.74)],
              15, 305, fill=(38, 118, 178), width=4)
    d.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=GOLD)
    d.polygon([(x, y + h), (x + w // 3, y + h - 11), (x + 2 * w // 3, y + h - 5),
               (x + w, y + h - 12), (x + w, y + h)], fill=(26, 110, 66))

def sc_eu(x, y, w, h):  # card 8 - one huge euro coin + drone
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 236))
    cx, cy, r = x + int(w * 0.36), y + h // 2, 25
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    text(cx, cy + 1, "\u20ac", F(ARCH_B, 34), fill=(24, 44, 84), anchor="mm")
    fx = x + int(w * 0.64)
    d.polygon([(fx, cy - 16), (fx + 44, cy - 6), (fx + 44, cy + 16),
               (fx, cy + 8)], fill=(52, 110, 180))
    d.rectangle([fx, cy - 16, fx + 6, cy + 8], fill=WHITE)
    d.polygon([(fx + 12, cy - 2), (fx + 30, cy - 8), (fx + 30, cy + 4)],
              fill=(120, 130, 145))

def sc_cyber(x, y, w, h):  # card 9 - three big payment cards + warning
    d.rectangle([x, y, x + w, y + h], fill=(206, 214, 224))
    cols = ((52, 130, 200), (240, 236, 224), (232, 140, 50))
    for i in range(3):
        bx = x + int(w * (0.05 + 0.27 * i))
        by = y + int(h * 0.16)
        cw2, ch2 = int(w * 0.25), int(h * 0.62)
        d.rectangle([bx, by, bx + cw2, by + ch2], fill=cols[i])
        d.rectangle([bx + 5, by + 6, bx + 17, by + 13], fill=GOLD)
        d.rectangle([bx + 5, by + ch2 - 9, bx + cw2 - 5, by + ch2 - 5],
                    fill=(30, 34, 44))
    tx, ty = x + int(w * 0.86), y + int(h * 0.14)
    d.polygon([(tx, ty + 26), (tx + 13, ty), (tx + 26, ty + 26)], fill=GOLD)
    text(tx + 13, ty + 17, "!", F(ARCH_B, 16), fill=(24, 24, 24), anchor="mm")

def sc_ger(x, y, w, h):  # card 10 - one big ger (yurt) on steppe
    d.rectangle([x, y, x + w, y + int(h * 0.60)], fill=(196, 222, 238))
    d.rectangle([x, y + int(h * 0.60), x + w, y + h], fill=(220, 208, 164))
    cx, gy = x + w // 2, y + h - 2
    gw, gh = int(w * 0.72), int(h * 0.58)
    d.rectangle([cx - gw // 2, gy - gh, cx + gw // 2, gy], fill=(244, 240, 228))
    d.polygon([(cx - gw // 2 - 5, gy - gh), (cx + gw // 2 + 5, gy - gh),
               (cx, gy - gh - 10)], fill=RED)
    d.rectangle([cx - 7, gy - gh + 12, cx + 7, gy], fill=(140, 74, 54))
    d.line([cx - gw // 2, gy - gh + 8, cx + gw // 2, gy - gh + 8],
           fill=GOLD, width=3)

def sc_court(x, y, w, h):  # card 11 - one big courthouse
    d.rectangle([x, y, x + w, y + h], fill=(206, 210, 220))
    cx = x + w // 2
    tw2 = int(w * 0.72)
    d.polygon([(cx - tw2 // 2, y + 16), (cx + tw2 // 2, y + 16), (cx, y + 3)],
              fill=(178, 52, 36))
    for i in range(4):
        colx = cx - tw2 // 2 + 10 + i * (tw2 - 20) // 3
        d.rectangle([colx - 4, y + 20, colx + 4, y + h - 7],
                    fill=(90, 100, 125))
    d.rectangle([cx - tw2 // 2, y + h - 7, cx + tw2 // 2, y + h - 2],
                fill=(90, 100, 125))

def sc_ballot(x, y, w, h):  # card 12 - one big ballot paper into a box
    d.rectangle([x, y, x + w, y + h], fill=(190, 214, 234))
    cx = x + w // 2
    bw, bh = int(w * 0.46), int(h * 0.42)
    bx, by = cx - bw // 2, y + h - bh - 3
    d.rectangle([bx, by, bx + bw, by + bh], fill=(244, 240, 228),
                outline=(24, 24, 24), width=2)
    d.rectangle([bx + 7, by + bh - 10, bx + bw - 7, by + bh - 4],
                fill=(38, 118, 178))
    d.polygon([(cx - 22, y + 3), (cx + 22, y + 3), (cx + 13, by + 8),
               (cx - 13, by + 8)], fill=WHITE)
    text(cx, y + 12, "31%", F(ARCH_B, 13), fill=INK, anchor="mm")

def sc_cricket(x, y, w, h):  # card 13 - pitch, stumps, one big ball
    d.rectangle([x, y, x + w, y + h], fill=(186, 220, 168))
    pw = int(w * 0.34)
    px = x + (w - pw) // 2
    d.rectangle([px, y + 4, px + pw, y + h - 3], fill=(226, 202, 144))
    sx = px + pw - 16
    for i in range(3):
        d.line([sx + i * 6, y + h - 30, sx + i * 6, y + h - 8],
               fill=(246, 226, 168), width=3)
    d.line([sx, y + h - 32, sx + 12, y + h - 32], fill=(246, 226, 168), width=3)
    d.ellipse([x + w - 34, y + 7, x + w - 8, y + 33], fill=RED)
    d.arc([x + w - 32, y + 9, x + w - 10, y + 31], 100, 260, fill=WHITE, width=2)

SCENES = {1: sc_missiles, 2: sc_globe, 3: sc_chart, 4: sc_blast,
          5: sc_reticle, 6: sc_barrage, 7: sc_cyclone, 8: sc_eu,
          9: sc_cyber, 10: sc_ger, 11: sc_court, 12: sc_ballot,
          13: sc_cricket}
SCENE_H = 64

def draw_card(card, x, y, w, h, lead=False):
    (no, place, region, cat, slug, chip, headline, deck, pin) = card
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE)
    SCENES[no](x, y, w, SCENE_H)
    # chip first (top-right), so the slug can be fitted beside it
    csize = 9 if lead else 7
    cf = F(ARCH_B, csize)
    chip_w = tw(chip, cf) + 10
    d.rectangle([x + w - chip_w - 4, y + 4, x + w - 4, y + 4 + 15],
                fill=WHITE, outline=BLACK)
    text(x + w - chip_w + 1, y + 4 + 7.5, chip, cf, fill=INK, anchor="lm")
    # slug: black box top-left inside the scene
    ssize = fit(slug, ARCH_B, 11 if lead else 9, w - chip_w - 16)
    sf = F(ARCH_B, ssize)
    slug_w = tw(slug, sf) + 10
    d.rectangle([x + 4, y + 4, x + 4 + slug_w, y + 4 + 15], fill=BLACK)
    text(x + 9, y + 4 + 7.5, slug, sf, fill=WHITE, anchor="lm")
    # black location bar, full card width
    ly = y + SCENE_H
    d.rectangle([x, ly, x + w, ly + 18], fill=BLACK)
    lf = F(ARCH_B, fit(place, ARCH_B, 12 if lead else 11, w - 12))
    text(x + 6, ly + 9, place, lf, fill=WHITE, anchor="lm")
    # badge row: red filled circle number + region . category in red caps
    by = ly + 18
    d.ellipse([x + 6, by + 2, x + 26, by + 22], fill=RED)
    text(x + 16, by + 12, str(no), F(ARCH_B, 11), fill=WHITE, anchor="mm")
    reg = "%s \u00b7 %s" % (region, cat)
    rf = F(ARCH_B, fit(reg, ARCH_B, 12 if lead else 10, w - 34))
    text(x + 31, by + 12, reg, rf, fill=RED, anchor="lm")
    # headline
    hy = by + 25
    head_lines = 1
    if lead:
        hs = fit(headline, PLAYFAIR, 19, w - 12, floor=12)
        text(x + 6, hy, headline, F(PLAYFAIR, hs), fill=INK)
        hy += hs + 4
    else:
        hf = F(PLAYFAIR, 13)
        hls = wrap(headline, hf, w - 12)[:2]
        head_lines = len(hls)
        for ln in hls:
            text(x + 6, hy, ln, hf, fill=INK)
            hy += 15
    # deck, then leave the rest of the card body empty on purpose
    df = F(ARCH_M, 11 if lead else 10)
    pitch = 13 if lead else 11.5
    max_lines = max(1, int((y + h - 8 - hy) // pitch))
    for ln in wrap(deck, df, w - 12)[:min(3, max_lines)]:
        text(x + 6, hy, ln, df, fill=SOFT)
        hy += pitch

# --- Claims bar ---------------------------------------------------------------
text(MX + 2, 13, "THE OVERNIGHT EDITION", F(ARCH_B, 12), fill=RED, anchor="lm")
claims = "40 STORIES \u00b7 13 DRAWN \u00b7 6 CONTINENTS \u00b7 ALL FROM 21 NOVEMBER"
text(MX + CW - 2, 13, claims, F(ARCH_B, fit(claims, ARCH_B, 12, 560)),
     fill=INK, anchor="rm")
d.rectangle([MX, 28, MX + CW, 30], fill=RED)

# --- Masthead: the date only ----------------------------------------------------
MAST_SIZE = 68
mf = F(PLAYFAIR, MAST_SIZE)
text(MX + CW // 2, 31, "Saturday 21 November 2026", mf, fill=INK, anchor="ma")
d.line([MX, 102, MX + CW, 102], fill=RULE, width=1)

# --- THE DAY IN PARTS -----------------------------------------------------------
DP_Y, DP_H = 108, 52
lab_w = 118
d.rectangle([MX, DP_Y, MX + lab_w, DP_Y + DP_H], fill=RED)
text(MX + lab_w // 2, DP_Y + DP_H // 2 - 8, "THE DAY", F(ARCH_B, 12),
     fill=WHITE, anchor="mm")
text(MX + lab_w // 2, DP_Y + DP_H // 2 + 8, "IN PARTS", F(ARCH_B, 12),
     fill=WHITE, anchor="mm")
seg_w = (CW - lab_w) / 5.0
for i, (lab, head) in enumerate(DAYPARTS):
    sx = MX + lab_w + int(i * seg_w)
    if i:
        d.line([sx, DP_Y + 5, sx, DP_Y + DP_H - 5], fill=RULE, width=1)
    text(sx + 8, DP_Y + 6, lab, F(ARCH_B, 10), fill=RED)
    for j, ln in enumerate(wrap(head, F(ARCH_M, 11), seg_w - 14)[:2]):
        text(sx + 8, DP_Y + 21 + j * 13, ln, F(ARCH_M, 11), fill=INK)

# --- Three equal leads ------------------------------------------------------------
LEAD_Y, LEAD_H = 168, 158
LEAD_W = (CW - 16) // 3
for i, card in enumerate(CARDS[:3]):
    draw_card(card, MX + i * (LEAD_W + 8), LEAD_Y, LEAD_W, LEAD_H, lead=True)

# --- Ten minis, 2 rows x 5 ---------------------------------------------------------
MINI_W = (CW - 32) // 5
MINI_H = 172
for k, card in enumerate(CARDS[3:]):
    cx0 = MX + (k % 5) * (MINI_W + 8)
    cy0 = 334 + (k // 5) * (MINI_H + 8)
    draw_card(card, cx0, cy0, MINI_W, MINI_H)

# --- Section header ------------------------------------------------------------------
SEC_Y = 692
text(MX + 2, SEC_Y, "WHERE IT HAPPENED", F(ARCH_B, 13), fill=INK)
text(MX + CW - 2, SEC_Y, "ALSO ON SATURDAY 21 NOVEMBER", F(ARCH_B, 13),
     fill=INK, anchor="ra")
d.line([MX, SEC_Y + 18, MX + CW, SEC_Y + 18], fill=INK, width=2)

# --- Dot-matrix world map (bottom-left, ~40% width) -----------------------------------
MAP_X, MAP_Y, MAP_W, MAP_H = MX, 718, 396, 128
COUNTRY_CONT = {
    # Europe
    "United Kingdom": "EUROPE", "Ireland": "EUROPE", "France": "EUROPE",
    "Spain": "EUROPE", "Portugal": "EUROPE", "Germany": "EUROPE",
    "Poland": "EUROPE", "Ukraine": "EUROPE", "Italy": "EUROPE",
    "Greece": "EUROPE", "Norway": "EUROPE", "Sweden": "EUROPE",
    "Finland": "EUROPE", "Denmark": "EUROPE", "Netherlands": "EUROPE",
    "Belgium": "EUROPE", "Romania": "EUROPE",
    # Asia
    "Russia": "ASIA", "Kazakhstan": "ASIA", "Mongolia": "ASIA",
    "China": "ASIA", "India": "ASIA", "Pakistan": "ASIA", "Nepal": "ASIA",
    "Myanmar": "ASIA", "Thailand": "ASIA", "Vietnam": "ASIA",
    "Malaysia": "ASIA", "Indonesia": "ASIA", "Philippines": "ASIA",
    "Japan": "ASIA", "South Korea": "ASIA", "Turkey": "ASIA",
    "Iran": "ASIA", "Iraq": "ASIA", "Saudi Arabia": "ASIA",
    "Israel": "ASIA",
    # Africa
    "Morocco": "AFRICA", "Algeria": "AFRICA", "Libya": "AFRICA",
    "Egypt": "AFRICA", "Sudan": "AFRICA", "Nigeria": "AFRICA",
    "Ethiopia": "AFRICA", "Kenya": "AFRICA",
    "Democratic Republic of the Congo": "AFRICA", "Angola": "AFRICA",
    "South Africa": "AFRICA", "Madagascar": "AFRICA",
    # Americas
    "Canada": "AMERICAS", "United States of America": "AMERICAS",
    "Mexico": "AMERICAS", "Panama": "AMERICAS", "Colombia": "AMERICAS",
    "Peru": "AMERICAS", "Brazil": "AMERICAS", "Chile": "AMERICAS",
    "Argentina": "AMERICAS", "Greenland": "AMERICAS",
    # Oceania
    "Australia": "OCEANIA", "New Zealand": "OCEANIA",
}

polys = []  # (continent, [(lon,lat),...])
for name, rings in WORLD.items():
    cont = COUNTRY_CONT.get(name, "ASIA")
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append((float(lo), float(la)))
        if len(pts) > 2:
            polys.append((cont, pts))

def inside(lon, lat, pts):
    c = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if ((yi > lat) != (yj > lat)) and \
           (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c

def proj(lon, lat):
    return (MAP_X + (lon + 180.0) / 360.0 * MAP_W,
            MAP_Y + (84.0 - lat) / 142.0 * MAP_H)

lon = -178.0
while lon <= 178:
    lat = -56.0
    while lat <= 82:
        hit = None
        for cont, pts in polys:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            if min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys) \
               and inside(lon, lat, pts):
                hit = cont
                break
        if hit:
            px, py = proj(lon, lat)
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                      fill=CONTINENT[hit])
        lat += 4.0
    lon += 4.0

for card in CARDS:
    no, place, region, cat, slug, chip, headline, deck, pin = card
    px, py = proj(pin[0], pin[1])
    px = min(max(px, MAP_X + 9), MAP_X + MAP_W - 9)
    py = min(max(py, MAP_Y + 9), MAP_Y + MAP_H - 9)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=REGIONS[region],
              outline=WHITE, width=1)
    text(px, py + 0.5, str(no), F(ARCH_B, 9), fill=WHITE, anchor="mm")

LEG_Y = MAP_Y + MAP_H + 8
lx = MAP_X
for name in ("EUROPE", "ASIA", "AMERICAS", "AFRICA", "OCEANIA"):
    d.ellipse([lx, LEG_Y + 3, lx + 8, LEG_Y + 11], fill=CONTINENT[name])
    text(lx + 11, LEG_Y + 7, name, F(ARCH_B, 9), fill=INK, anchor="lm")
    lx += int(tw(name, F(ARCH_B, 9))) + 30
text(MAP_X, LEG_Y + 18, "Numbered pins = the 13 pictured stories.",
     F(ARCH_M, 9), fill=SOFT)

# --- Briefs: hard one-liners, pitch 10.5 px -------------------------------------------
BR_X, BR_Y = 426, 720
BR_COLW = 286
BF, BNF = F(ARCH_M, 10), F(ARCH_B, 10)
half = (len(BRIEFS) + 1) // 2
for ci, chunk in enumerate((BRIEFS[:half], BRIEFS[half:])):
    bx = BR_X + ci * (BR_COLW + 12)
    for ri, (no, leadin, tail) in enumerate(chunk):
        by = BR_Y + ri * 10.5
        text(bx, by, "%d" % no, BNF, fill=RED, anchor="lm")
        num_w = tw("%d " % no, BNF)
        text(bx + num_w, by, leadin, BNF, fill=INK, anchor="lm")
        lead_w = tw(leadin + " ", BNF)
        avail = BR_COLW - num_w - lead_w
        tsize = fit(tail, ARCH_M, 10, avail, floor=8)
        text(bx + num_w + lead_w, by, tail, F(ARCH_M, tsize), fill=INK,
             anchor="lm")

# --- DATE CHECK -------------------------------------------------------------------------
DC_Y, DC_H = 892, 58
d.rectangle([MX, DC_Y, MX + CW, DC_Y + DC_H], outline=RED, width=2)
lab = "DATE CHECK"
lab_w = tw(lab, F(ARCH_B, 11)) + 12
d.rectangle([MX, DC_Y, MX + lab_w, DC_Y + 20], fill=RED)
text(MX + 6, DC_Y + 10, lab, F(ARCH_B, 11), fill=WHITE, anchor="lm")
body_x = MX + lab_w + 8
lines = []
lines += wrap(DATE_DISCARDS, F(ARCH_M, 10), MX + CW - body_x - 6)[:2]
lines += wrap(DATE_UNVERIFIED, F(ARCH_M, 10), MX + CW - MX - 12)
lines += wrap(DATE_NOTYET, F(ARCH_M, 10), MX + CW - MX - 12)
yy = DC_Y + 3
for i, ln in enumerate(lines[:4]):
    xx = body_x if i < 2 else MX + 8
    text(xx, yy, ln, F(ARCH_M, 10), fill=SOFT)
    yy += 13

# --- Footer, one line ---------------------------------------------------------------------
text(MX + CW // 2, 972, FOOTER, F(ARCH_M, fit(FOOTER, ARCH_M, 10, CW - 8)),
     fill=SOFT, anchor="mm")

img_q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
img_q.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT))

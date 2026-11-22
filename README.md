[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Desember17-cpu/the-overnight-edition-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Desember17-cpu/the-overnight-edition-21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The Overnight Edition — Saturday 21 November 2026 (challenger B4, round 4)

A light-edition one-page newspaper that sums up a whole day of world news in a
single 1024x1024 picture: 40 stories from 7 regions, every one of them dated
Saturday 21 November 2026. This round-4 rebuild keeps the paper's name but
replaces round 3's dark navy page with a cream-paper, black-ink broadsheet:
a black masthead block with the paper's name in giant Playfair, a red
top-stories hook band, a five-slot UTC timeline and a black "Day in Numbers"
strip (3 weapons into Poland, 42 injured at Kryvyi Rih, Nasdaq -5.28%,
372,000 sheltered in Odisha, €1BN of EU aid adopted, India 159/1).

Thirteen stories are pictured as cards with original flat drawings — Rutte
flying to Warsaw after two missiles and a jet drone land in Poland, COP31
running into overtime in Antalya, Wall Street entering correction, Denmark
exposing an assassination plot, the EU adopting €1bn of military aid for
Ukraine (joint buying via the Peace Facility, with Britain pledging 1,000+
drones alongside), Mongolia's president resigning, the ANC's worst result
since 1994 and India fighting back to 159/1 in Wellington — and 27 further
stories run as numbered briefs. A locator map pins the 13 pictured stories
(18px numbered pins) and dots the briefs on real country outlines. A date
check names the Friday 20 November stories deliberately left out and the
things that had not happened yet. A source is named beside every story.

## Duel record (round 4)

Three layout variants were built and duelled on readability at 300px plus
completeness: A = three equal lead cards on cream; B = black masthead block
with a wide hero lead (card 1) and cards 2-3 stacked beside it, briefs left
and map right; C = red masthead with a full-width banner lead. **Winner: B** —
the hero headline is the largest text on the page and stays legible at
300px, the black masthead is the strongest anchor, and every card still
carries at least two pool facts. A is the backup (balanced but flatter);
C was dropped (banner wastes width, lower leads cramped).

3D vs 2D: the page is a flat 2D broadsheet by design; a 3D treatment was
considered and rejected — flat 2D won on 300px readability and print-paper
identity. A 3D masthead treatment remains the noted backup if a later round
needs it.

The image is produced by a deterministic Pillow program (`draw.py`,
standard library plus PIL only, no network), saved as a 256-colour palette
PNG; `main.py` copies the rendered `entry.png` to the output directory
named by `MAKEFUN_OUTPUT_DIR`.

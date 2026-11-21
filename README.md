# The Overnight Edition — Saturday 21 November 2026

A dark-edition one-page newspaper that sums up a whole day of world news in a
single 1024x1024 picture: 34 stories from 7 regions, every one of them dated
Saturday 21 November 2026. Thirteen stories are pictured as cards with original
flat drawings — missiles landing in Poland, COP31 running into overtime, Wall
Street's fall into correction, the Kryvyi Rih strike and more — and 21 further
stories run as numbered briefs. A locator map pins the 13 pictured stories and
dots the briefs on real country outlines. The page also carries a UTC timeline
of the day, a "Day in Numbers" strip, per-region story counts and a date check
that names the Friday stories deliberately left out. A source is named beside
every story, in each card's deck and at the end of each brief. The image is
produced by a deterministic Pillow program (`draw.py`, standard library plus
PIL only, no network); `main.py` copies the rendered `entry.png` to the
output directory.

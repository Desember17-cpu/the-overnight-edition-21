[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Desember17-cpu/the-overnight-edition-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Desember17-cpu/the-overnight-edition-21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The Overnight Edition — Saturday 21 November 2026

A dark-edition one-page newspaper that sums up a whole day of world news in a
single 1024x1024 picture: 40 stories from 7 regions, every one of them dated
Saturday 21 November 2026. Thirteen stories are pictured as cards with original
flat drawings — missiles landing in Poland, COP31 running into overtime, the
US clearing 900,000 AI chips for China, coalition strikes on Houthi workshops
and three missiles downed over Riyadh, the EU's €8bn payout to Kyiv, the
Kryvyi Rih strike and more — and 27 further stories run as numbered briefs,
from BepiColombo's arrival at Mercury tonight to Manipur, the Kharg Island
tanker convoy and Voyager 1 reaching one light-day from Earth. A locator map
pins the 13 pictured stories and dots the briefs on real country outlines.
The page also carries a UTC timeline of the day, a "Day in Numbers" strip, per-region
story counts and a date check that names the Friday stories deliberately
left out — among them Wall Street's AI sell-off and Mongolia's president
quitting, both Friday 20 November news. A source is named beside every story,
in each card's deck and at the end of each brief. The image is
produced by a deterministic Pillow program (`draw.py`, standard library plus
PIL only, no network), saved as a 256-colour palette PNG (about 115 KB);
`main.py` copies the rendered `entry.png` to the output directory.

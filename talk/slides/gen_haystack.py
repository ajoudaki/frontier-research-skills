"""Redraw the haystack on talk/slides/slides/bottleneck.html: a full mound of straw with one gem in it.

The gem has the same shape and sapphire colour as the gem on the 'gem in the haystack' slide, so the
two slides visibly connect. Only the haystack <svg> element is replaced; the rest of the slide is kept.

Usage: python talk/slides/gen_haystack.py
"""

import math
import random
import re
from pathlib import Path

from gen_gem_slide import GEM, SAPPHIRE, SAPPHIRE_SOFT

SLIDE = Path(__file__).resolve().parent / "slides" / "bottleneck.html"
STRAWS = ["#8C7A52", "#A38D5E", "#B9A170", "#6F6346", "#C8B080", "#7E6F4C"]
W, H = 432, 560                 # the svg's viewBox, as placed on the slide
BASE, PEAK, MID, HALF = 525, 185, 216, 196
GEM_AT, GEM_SCALE = (258, 402), 0.46


def top(x):
    """The mound's upper edge at x (None outside the mound)."""
    u = (x - MID) / HALF
    if abs(u) >= 1:
        return None
    return BASE - (BASE - PEAK) * (1 - u * u) ** 0.75


def straw(rng, x, y):
    angle = math.radians(rng.gauss(0, 24) + rng.choice([0, 0, 0, 180]))
    length = rng.uniform(18, 40)
    dx, dy = math.cos(angle) * length / 2, math.sin(angle) * length / 2
    return (f'<line x1="{x - dx:.1f}" y1="{y - dy:.1f}" x2="{x + dx:.1f}" y2="{y + dy:.1f}" stroke="{rng.choice(STRAWS)}" '
            f'stroke-width="{rng.uniform(2.4, 3.6):.1f}" stroke-linecap="round" opacity="{rng.uniform(0.55, 0.95):.2f}"/>')


def inside(rng):
    while True:
        x, y = rng.uniform(MID - HALF, MID + HALF), rng.uniform(PEAK, BASE)
        t = top(x)
        if t is not None and y >= t + rng.uniform(-6, 10):
            return x, y


def main():
    rng = random.Random(7)
    under = "".join(straw(rng, *inside(rng)) for _ in range(560))
    gx, gy = GEM_AT
    gem = (f'<g transform="translate({gx - 45 * GEM_SCALE:.1f},{gy - 40 * GEM_SCALE:.1f}) scale({GEM_SCALE})">'
           + GEM.format(fill=SAPPHIRE, line=SAPPHIRE_SOFT) + "</g>")
    # a few straws across the gem, so it is half hidden
    over = "".join(straw(rng, gx + rng.uniform(-28, 28), gy + rng.uniform(-6, 22)) for _ in range(7))
    ground = f'<ellipse cx="{MID}" cy="{BASE + 6}" rx="{HALF + 14}" ry="9" fill="#141822"/>'
    art = (f'<svg data-build-in="fade 4" xmlns="http://www.w3.org/2000/svg" aria-label="A full haystack of straw with one sapphire gem half hidden inside" '
           f'viewBox="0 0 {W} {H}" style="position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px">'
           f'{ground}{under}{gem}{over}</svg>')
    html = SLIDE.read_text()
    html, n = re.subn(r'<svg data-build-in="fade 4".*?</svg>', lambda m: art, html, count=1, flags=re.S)
    assert n == 1
    SLIDE.write_text(html)
    print(f"wrote {SLIDE}")


if __name__ == "__main__":
    main()

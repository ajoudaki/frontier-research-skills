"""Generate talk/slides/slides/bottleneck.html: the problem, with a gem in the haystack.

Light theme. The haystack is a full mound of straw with a clear pocket around one gem, drawn in the
same shape and sapphire colour as the gem on the strategy and recap slides, so the slides connect.

Usage: python talk/slides/gen_bottleneck.py
"""

import math
import random
from pathlib import Path

from gen_gem_slide import GEM, SAPPHIRE
from gen_skill_slides import DARK, INK, PAPER, RED, SANS, SERIF, p, section

SLIDE = Path(__file__).resolve().parent / "slides" / "bottleneck.html"
STRAWS = ["#C9B27A", "#B89C5E", "#D9C691", "#A98E55", "#E2D2A6", "#BFA46A"]
W, H = 432, 560                 # the haystack's viewBox, as placed on the slide
BASE, PEAK, MID, HALF = 525, 185, 216, 196
GEM_AT, GEM_SCALE, POCKET = (236, 388), 0.62, 40


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
    return (x - dx, y - dy, x + dx, y + dy, rng.choice(STRAWS), rng.uniform(2.4, 3.6), rng.uniform(0.6, 1.0))


def near_gem(s, gap):
    """Whether a straw passes within `gap` of the gem's centre."""
    x1, y1, x2, y2 = s[:4]
    gx, gy = GEM_AT
    dx, dy = x2 - x1, y2 - y1
    t = max(0.0, min(1.0, ((gx - x1) * dx + (gy - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x1 + t * dx - gx, y1 + t * dy - gy) < gap


def draw(s):
    x1, y1, x2, y2, color, width, alpha = s
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width:.1f}" '
            f'stroke-linecap="round" opacity="{alpha:.2f}"/>')


def haystack():
    rng = random.Random(7)
    straws = []
    while len(straws) < 620:
        x, y = rng.uniform(MID - HALF, MID + HALF), rng.uniform(PEAK, BASE)
        t = top(x)
        if t is not None and y >= t + rng.uniform(-6, 10):
            s = straw(rng, x, y)
            if not near_gem(s, POCKET):
                straws.append(s)
    gx, gy = GEM_AT
    gem = (f'<g transform="translate({gx - 45 * GEM_SCALE:.1f},{gy - 40 * GEM_SCALE:.1f}) scale({GEM_SCALE})">'
           + GEM.format(fill=SAPPHIRE, line=PAPER) + "</g>")
    # two straws lie across the gem's edges, so it still sits in the hay
    over = [(gx - 46, gy + 20, gx - 12, gy + 26, STRAWS[1], 3.2, 0.95), (gx + 14, gy - 22, gx + 48, gy - 14, STRAWS[3], 3.0, 0.95)]
    ground = f'<ellipse cx="{MID}" cy="{BASE + 6}" rx="{HALF + 14}" ry="9" fill="#E8E1D2"/>'
    return (f'  <svg data-build-in="fade 4" xmlns="http://www.w3.org/2000/svg" aria-label="A full haystack of straw with one sapphire gem in it" '
            f'viewBox="0 0 {W} {H}" style="position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px">'
            f'{ground}{"".join(draw(s) for s in straws)}{gem}{"".join(draw(s) for s in over)}</svg>')


def main():
    points = ["More and more research goes to capable models.",
              "It fails silently: one hidden assumption sinks it.",
              "More output than we can check: you're the bottleneck."]
    L = [f'  <div style="width:920px; display:flex; flex-direction:column; gap:16px">\n'
         f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">01 · The problem</p>\n'
         f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">Smart models fail beautifully.</h2>\n  </div>']
    for i, (s, top_) in enumerate(zip(points, (400, 480, 560))):
        L.append(p(128, top_, 920, f'<span style="color:{RED}">{i + 1}</span>  {s}', 32, DARK, build=f"rise {i + 1}", extra="; line-height:1.4"))
    L.append(haystack().replace(' data-build-in="fade 4"', ''))   # on the slide from the start
    L.append(p(1183, 196, 600, f'A <b style="color:{SAPPHIRE}">gem</b> in the haystack.', 48, INK, 600, "center", family=SERIF))
    notes = ("Let's start with where we are today. We're in the middle of a fundamental transition: from writing every line of code, "
             "paper and theory ourselves, to delegating much more research to very capable models. "
             "The transition is hard, because in research, agents fail silently, and the smarter they get, the harder those failures "
             "are to catch. The text looks flawless, the figures look great, even the math looks great at a glance. But the real failure "
             "is hidden on page 12, in some assumption that quietly absorbs all the complexity. "
             "On top of that, they produce code, theory and papers far faster than we can read. "
             "So we end up with a pile of results that may contain some gems, but finding them takes an enormous amount of time: "
             "a gem in a haystack. And noise isn't only mistakes: a result can be correct but irrelevant. "
             "You lose so much control that it can defeat the purpose of using them at all.")
    SLIDE.write_text(section("bottleneck", "\n".join(L), notes))
    print(f"wrote {SLIDE}")


if __name__ == "__main__":
    main()

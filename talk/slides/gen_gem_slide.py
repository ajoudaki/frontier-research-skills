"""Generate talk/slides/slides/gem.html: the whole project as a haystack, a small part of it as the gem.

A large radial tree (about 200 studies) grows from the research question, one level per step. Any
study may branch, promoted or not: by default studies don't see each other, but with your approval
one can build on another's unpromoted work. The established core is one contiguous lake with a
single shoreline around the promoted studies (about a fifth of the graph); unpromoted studies stay
outside it. Then the haystack dims, and a coherent part of the core, always including the research
question, is carved out for a paper and shown as the gem, in the same sapphire as the gem on the opening slide.

Usage: python talk/slides/gen_gem_slide.py
"""

import math
import random
from pathlib import Path

import numpy as np
from matplotlib.path import Path as Polygon
from skimage import measure

from gen_skill_slides import BG, CORE, INK, MONO, MUTED, PAPER, RED, SANS, SERIF, arrow, p, section, svg

OUT = Path(__file__).resolve().parent / "slides" / "gem.html"

SAPPHIRE, SAPPHIRE_SOFT = "#2F6FC9", "#DCE7F6"
STRAW, STRAW_EDGE = "#CDB98C", "#DDD2B8"
GEM = ('<polygon points="22,4 68,4 86,28 45,76 4,28" fill="{fill}"/>'
       '<polyline points="4,28 86,28" fill="none" stroke="{line}" stroke-width="3"/>'
       '<polyline points="22,4 34,28 45,76 56,28 68,4" fill="none" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>')

LEVELS = 6
CX, CY = 700, 615          # the research question, on the slide
RX, RY = 95, 53            # level k sits at k times these radii
R_ROOT, R_NODE = 26, 7
# how many children a study at each level may get (any study may branch, promoted or not)
KIDS = {0: [6], 1: [2, 2, 3], 2: [1, 2, 2, 3], 3: [1, 1, 2, 2, 2], 4: [0, 1, 1, 2, 2], 5: [0, 1, 1, 1, 2]}


def build_tree(seed):
    rng = random.Random(seed)
    nodes = [{"level": 0, "parent": None, "kids": []}]
    frontier = [0]
    for level in range(LEVELS):
        new = []
        for i in frontier:
            for _ in range(rng.choice(KIDS[level])):
                nodes.append({"level": level + 1, "parent": i, "kids": []})
                nodes[i]["kids"].append(len(nodes) - 1)
                new.append(len(nodes) - 1)
        frontier = new
    return nodes


def layout(nodes, start):
    """Radial layout: every leaf gets an angular slot, wider the closer it is to the centre; a parent
    sits at its children's mean angle."""
    for nd in nodes:
        nd.pop("angle", None)
    leaves = []

    def walk(i):
        if not nodes[i]["kids"]:
            leaves.append(i)
        for k in nodes[i]["kids"]:
            walk(k)

    walk(0)
    weight = [3 / nodes[i]["level"] for i in leaves]
    unit, at = 360 / sum(weight), start
    for i, w in zip(leaves, weight):
        nodes[i]["angle"] = at + unit * w / 2
        at += unit * w

    def angle(i):
        if "angle" not in nodes[i]:
            nodes[i]["angle"] = sum(angle(k) for k in nodes[i]["kids"]) / len(nodes[i]["kids"])
        return nodes[i]["angle"]

    for i in range(1, len(nodes)):
        angle(i)
    for nd in nodes:
        a, k = math.radians(nd.get("angle", 0)), nd["level"]
        nd["xy"] = (CX + k * RX * math.cos(a), CY + k * RY * math.sin(a))


def min_gap(nodes):
    pts = np.array([nd["xy"] for nd in nodes])
    d = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    d[np.diag_indices(len(pts))] = 1e9
    return d.min()


def promote(nodes):
    """The core: studies inside a smooth, star-shaped region around the question whose parent is in the core."""
    nodes[0]["core"] = True
    for nd in nodes[1:]:
        a = math.radians(nd["angle"])
        reach = 2.9 + 1.0 * math.sin(2 * a + 1.0) + 0.7 * math.sin(3 * a + 2.4) + 0.45 * math.sin(5 * a + 0.7)
        nd["core"] = nd["level"] <= reach and nodes[nd["parent"]]["core"]


GRID = (260, 1000, 300, 1320, 3)   # y0, y1, x0, x1, step: the slide area the field is evaluated on


def shore(inside, outside, sigma, root=True):
    """One closed shoreline around the studies in `inside`, with every study in `outside` left out.

    The shore is a level set of a smooth field: a soft bump on each inside study, a sharp dip on each
    outside one, and a faint ripple so it looks natural. Only the outer contour is kept, so the region
    is one piece with no holes; then it is checked against every study."""
    y0, y1, x0, x1, s = GRID
    ys, xs = np.mgrid[y0:y1:s, x0:x1:s].astype(float)

    def bump(c, sig):
        return np.exp(-((xs - c[0]) ** 2 + (ys - c[1]) ** 2) / (2 * sig ** 2))

    field = 1.6 * bump((CX, CY), sigma * 1.3) if root else 0 * xs
    for nd in inside:
        field = field + bump(nd["xy"], sigma)
    for nd in outside:
        field = field - 2.6 * bump(nd["xy"], 13)
    field = field + 0.06 * np.sin(xs / 37 + 0.3) * np.sin(ys / 29 + 1.1)
    target = (CX, CY) if root else inside[0]["xy"]
    best = None
    for c in measure.find_contours(field, 0.5):
        poly = np.c_[x0 + s * c[:, 1], y0 + s * c[:, 0]]
        if Polygon(poly).contains_point(target) and (best is None or len(poly) > len(best)):
            best = poly
    region = Polygon(best)
    for nd in inside:
        assert region.contains_point(nd["xy"]), f"study at {nd['xy']} is outside its shore"
    for nd in outside:
        assert not region.contains_point(nd["xy"]), f"study at {nd['xy']} is inside a shore it doesn't belong to"
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in best[::2]) + " Z"


def full(content, label, build=None):
    return svg(0, 0, 1920, 1080, content, label, build)


def main():
    # pick a tree of about 200 studies whose layout keeps every study clear of the others
    for seed in range(400):
        nodes = build_tree(seed)
        if not 190 <= len(nodes) - 1 <= 215:
            continue
        start = max(range(0, 360, 6), key=lambda s: (layout(nodes, s), min_gap(nodes))[1])
        layout(nodes, start)
        promote(nodes)
        share = sum(nd["core"] for nd in nodes[1:]) / (len(nodes) - 1)
        if min_gap(nodes) >= 20 and 0.17 <= share <= 0.24:
            break
    total = len(nodes) - 1
    core = [nd for nd in nodes[1:] if nd["core"]]
    rest = [nd for nd in nodes[1:] if not nd["core"]]
    xs_, ys_ = [nd["xy"][0] for nd in nodes], [nd["xy"][1] for nd in nodes]
    print(f"seed {seed}: {total} studies, {len(core)} in the core ({len(core) / total:.0%}); "
          f"x {min(xs_):.0f}-{max(xs_):.0f}, y {min(ys_):.0f}-{max(ys_):.0f}; closest pair {min_gap(nodes):.0f}px")

    # the gem: the research question plus one level-1 core branch, the one closest to ten studies
    def core_subtree(i):
        out = [i]
        for k in nodes[i]["kids"]:
            if nodes[k]["core"]:
                out += core_subtree(k)
        return out

    candidates = [i for i, nd in enumerate(nodes) if nd["level"] == 1 and nd["core"]]
    gem = [nodes[i] for i in core_subtree(min(candidates, key=lambda i: abs(len(core_subtree(i)) - 10)))]
    print(f"gem: {len(gem)} studies")

    def edge(nd, color, width=2):
        (ax, ay), (bx, by) = nodes[nd["parent"]]["xy"], nd["xy"]
        r_a = R_ROOT if nd["parent"] == 0 else R_NODE
        d = math.dist((ax, ay), (bx, by))
        ux, uy = (bx - ax) / d, (by - ay) / d
        return (f'<line x1="{ax + ux * r_a:.1f}" y1="{ay + uy * r_a:.1f}" x2="{bx - ux * R_NODE:.1f}" y2="{by - uy * R_NODE:.1f}" '
                f'stroke="{color}" stroke-width="{width}"/>')

    def disc(nd, fill, r=R_NODE):
        return f'<circle cx="{nd["xy"][0]:.1f}" cy="{nd["xy"][1]:.1f}" r="{r}" fill="{fill}"/>'

    # one lake per level that adds core studies, each containing the last
    lakes, last = [], 0
    for k in range(1, LEVELS + 1):
        inside = [nd for nd in core if nd["level"] <= k]
        if len(inside) > last:
            last = len(inside)
            lakes.append(full(f'<path d="{shore(inside, rest, 46)}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                              f"The established core grows at level {k}: one contiguous lake.", f"fade {k}"))
    levels = []
    for k in range(1, LEVELS + 1):
        here = [nd for nd in nodes[1:] if nd["level"] == k]
        art = "".join(edge(nd, RED if nd["core"] else STRAW_EDGE) for nd in here)
        art += "".join(disc(nd, RED if nd["core"] else STRAW) for nd in here)
        levels.append(full(art, f"Level {k}: {len(here)} new studies, {sum(nd['core'] for nd in here)} of them promoted.", f"fade {k}"))
    root = full(f'<circle cx="{CX}" cy="{CY}" r="{R_ROOT}" fill="{INK}"/>', "The research question.")

    # step 7: the haystack dims and the core stands out
    x0, y0 = min(xs_) - 20, min(ys_) - 20
    x1, y1 = max(xs_) + 20, max(ys_) + 20
    dim = full(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" fill="{BG}" opacity="0.7"/>',
               "The haystack fades.", "fade 7")
    final_lake = lakes[-1][:lakes[-1].rindex('data-build-in=')] + 'data-build-in="fade 7"' + lakes[-1][lakes[-1].index(' style=', lakes[-1].rindex('data-build-in=')):]
    core_art = "".join(edge(nd, RED) for nd in core) + "".join(disc(nd, RED) for nd in core) + f'<circle cx="{CX}" cy="{CY}" r="{R_ROOT}" fill="{INK}"/>'
    again = [final_lake, full(core_art, "The established core, highlighted.", "fade 7")]
    unknown = p(x1 - 240, y1 - 34, 240, "the unknown", 30, MUTED, align="right", family=SERIF, build="fade 7", extra="; font-style:italic")

    # step 8: a coherent part of the core is carved out for a paper, in sapphire
    gem_shape = shore(gem, [nd for nd in nodes[1:] if nd not in gem], 32)
    gem_art = (f'<path d="{gem_shape}" fill="{SAPPHIRE_SOFT}" stroke="{SAPPHIRE}" stroke-width="3" stroke-linejoin="round"/>'
               + "".join(edge(nd, SAPPHIRE, 3) for nd in gem)
               + "".join(disc(nd, SAPPHIRE, R_NODE + 1) for nd in gem)
               + f'<circle cx="{CX}" cy="{CY}" r="{R_ROOT}" fill="{INK}" stroke="{SAPPHIRE}" stroke-width="5"/>')
    carve = full(gem_art, f"A coherent part of the core, {len(gem)} studies, carved out for the paper.", "fade 8")

    # the right-hand column
    C = 1350
    col = [p(C, 320, 442, "The established core", 32, RED, 600, family=SERIF, build="fade 7"),
           p(C, 364, 442, f"true and relevant: {len(core)} of {total} studies", 24, INK, build="fade 7"),
           p(C, 420, 442, "Its shoreline", 32, MUTED, 600, family=SERIF, build="fade 7"),
           p(C, 464, 442, "the frontier with the unknown", 24, MUTED, build="fade 7"),
           svg(C + 30, 508, 40, 52, arrow(20, 2, 20, 48, SAPPHIRE, 3), "Carve a part of the core for a paper.", "fade 8"),
           f'  <div data-build-in="rise 8" style="position:absolute; top:566px; left:{C}px; width:442px; display:flex; flex-direction:column; '
           f'gap:8px; padding:20px 24px; background:{PAPER}; border:2px solid {SAPPHIRE}; border-radius:16px">\n'
           f'    <p style="{SERIF}; font-size:28px; font-weight:600; color:{INK}">A coherent part, for a paper</p>\n'
           f'    <p style="{SANS}; font-size:22px; color:{MUTED}">new gates: novelty, significance</p>\n'
           f'    <p style="align-self:flex-start; padding:4px 14px; {MONO}; font-size:22px; color:{RED}; background:{CORE}; border-radius:8px">review-paper</p>\n  </div>',
           svg(C + 30, 756, 40, 52, arrow(20, 2, 20, 48, SAPPHIRE, 3), "The audited part becomes the paper.", "fade 9"),
           svg(C, 820, 90, 80, GEM.format(fill=SAPPHIRE, line=PAPER), "The gem.", "pop 9"),
           p(C + 110, 818, 332, f"The gem:<br>{len(gem)} of {total} studies", 32, INK, 600, family=SERIF, build="fade 9")]

    head = (f'  <div style="display:flex; flex-direction:column; gap:12px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">10 · The gem in the haystack</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">From the haystack to the gem.</h2>\n  </div>')
    layers = lakes + levels + [root, dim] + again + [carve, unknown] + col
    notes = ("Remember the gem in the haystack? Here's what a real project looks like over time. "
             "From the research question, studies branch out. "
             "Some pass the gate, and the core forms around them, like a lake. "
             "Studies keep branching, level by level. By default they don't see each other, but with your approval one can build on "
             "another, even on work that hasn't been promoted yet. "
             "So the graph gets large and tangled, "
             "while the core grows slowly, "
             "and always in one piece. "
             "In the end, the core is about a fifth of everything: an ocean of knowledge that's true and relevant, with a long shoreline "
             "to the unknown. "
             "But a paper isn't the whole core. You carve out a coherent part, grown from the original question, and it has to pass new gates: novelty and significance. "
             "That's the audit. "
             f"So out of {total} studies, {len(gem)} become the paper. That's the gem in the haystack. So let me wrap up.")
    OUT.write_text(section("gem", head + "\n" + "\n".join(layers), notes))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

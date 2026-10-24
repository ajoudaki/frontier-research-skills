"""Generate talk/slides/slides/gem.html: the whole project as a haystack, a small part of it as the gem.

A large, irregular tree (about 200 studies) grows from the research question, one level per step.
Every edge has the same length; branches turn into free space as they grow.
Some lines of work are bushy and deep, others stop early. Any study may branch, promoted or not: by default studies don't see each other, but with your approval
one can build on another's unpromoted work. The established core is one contiguous lake with a
single shoreline around the promoted studies (about a fifth of the graph); unpromoted studies stay
outside it. Then the haystack dims, and a coherent part of the core, always including the research
question, is carved out for a paper and shown as the gem, in the same sapphire as the gem on the opening slide.

Usage: python talk/slides/gen_gem_slide.py
"""

import math
import random
import subprocess
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

STEPS = 6                  # build steps for the growth; deeper studies arrive with the last step
MAX_DEPTH = 7
R_NODE = 7
R_ROOT = R_NODE             # the research question is drawn like any other study
# expected children per unit of vigor, by depth: any study may branch, promoted or not. Vigor is
# inherited with noise, so some lines of work become bushy and deep while others stop early.
BASE = {1: 1.6, 2: 1.35, 3: 1.15, 4: 0.95, 5: 0.85, 6: 0.7, 7: 0.5}


def poisson(rng, lam):
    k, p, limit = 0, 1.0, math.exp(-lam)
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def build_tree(seed):
    rng = random.Random(seed)
    nodes = [{"level": 0, "parent": None, "kids": [], "vigor": 1.0}]

    def add(parent, vigor):
        nd = {"level": nodes[parent]["level"] + 1, "parent": parent, "kids": [], "vigor": vigor}
        nodes.append(nd)
        nodes[parent]["kids"].append(len(nodes) - 1)
        return len(nodes) - 1

    frontier = [add(0, rng.lognormvariate(0, 0.6)) for _ in range(6)]
    while frontier and len(nodes) <= 400:   # oversized trees are rejected by the caller anyway
        new = []
        for i in frontier:
            nd = nodes[i]
            if nd["level"] < MAX_DEPTH:
                for _ in range(poisson(rng, nd["vigor"] * BASE[nd["level"]])):
                    new.append(add(i, nd["vigor"] ** 0.75 * rng.lognormvariate(0, 0.45)))
        frontier = new
    return nodes


AREA = (150, 300, 1280, 945)   # x0, y0, x1, y1: where the graph may sit on the slide


def place(nodes, seed):
    """Lay the tree out with Graphviz neato (stress majorization) asking for the same length on every
    edge, turn it so its long axis runs across the slide, and scale it uniformly into AREA, which keeps
    the edges equal."""
    lines = [f"graph G {{ graph [start={seed}, maxiter=3000, epsilon=0.00001]; node [shape=point, width=0.05]; edge [len=1];"]
    lines += [f"  {i} -- {k};" for i, nd in enumerate(nodes) for k in nd["kids"]]
    lines.append("}")
    out = subprocess.run(["neato", "-Tplain"], input="\n".join(lines), capture_output=True, text=True, check=True).stdout
    pos = {}
    for row in out.splitlines():
        f = row.split()
        if f and f[0] == "node":
            pos[int(f[1])] = (float(f[2]), float(f[3]))
    pts = np.array([pos[i] for i in range(len(nodes))])
    pts -= pts.mean(0)
    _, _, vt = np.linalg.svd(pts, full_matrices=False)
    pts = pts @ vt.T                                          # long axis along x
    aspect = np.ptp(pts[:, 0]) / np.ptp(pts[:, 1])
    x0, y0, x1, y1 = AREA
    scale = min((x1 - x0) / np.ptp(pts[:, 0]), (y1 - y0) / np.ptp(pts[:, 1]))
    pts = (pts - pts.min(0)) * scale
    pts += ((x0 + x1 - pts[:, 0].max()) / 2, (y0 + y1 - pts[:, 1].max()) / 2)
    pts = relax(pts, gap=22)
    for nd, (x, y) in zip(nodes, pts):
        nd["xy"] = (float(x), float(y))
    lengths = [math.dist(nd["xy"], nodes[nd["parent"]]["xy"]) for nd in nodes[1:]]
    return float(np.std(lengths) / np.mean(lengths)), float(aspect)


def relax(pts, gap, rounds=80):
    """Nudge apart any two studies closer than `gap` pixels, so no two discs crowd each other."""
    pts = pts.copy()
    for _ in range(rounds):
        diff = pts[:, None] - pts[None]
        dist = np.sqrt((diff ** 2).sum(-1)) + np.eye(len(pts)) * 1e9
        push = np.clip(gap - dist, 0, None) / 2
        if not push.any():
            break
        pts += (diff / dist[..., None] * push[..., None]).sum(1)
    return pts


def min_gap(nodes):
    pts = np.array([nd["xy"] for nd in nodes])
    d = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    d[np.diag_indices(len(pts))] = 1e9
    return d.min()


def promote(nodes, share=0.2):
    """The core: studies inside a smooth, organic region around the question, whose parent is in the
    core. The region's size is tuned so the core holds about `share` of all studies."""
    cx, cy = nodes[0]["xy"]

    def mark(size):
        nodes[0]["core"] = True
        for i in sorted(range(1, len(nodes)), key=lambda i: nodes[i]["level"]):
            nd = nodes[i]
            dx, dy = nd["xy"][0] - cx, nd["xy"][1] - cy
            a = math.atan2(dy, dx)
            reach = size * (1 + 0.35 * math.sin(2 * a + 1.0) + 0.25 * math.sin(3 * a + 2.4) + 0.15 * math.sin(5 * a + 0.7))
            nd["core"] = math.hypot(dx, dy) <= reach and nodes[nd["parent"]]["core"]
            nd["step"] = min(nd["level"], STEPS)
        return sum(nd["core"] for nd in nodes[1:]) / (len(nodes) - 1)

    lo, hi = 20.0, 900.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mark(mid) < share else (lo, mid)
    mark(hi)


GRID = (260, 1000, 300, 1320, 3)   # y0, y1, x0, x1, step: the slide area the field is evaluated on


def shore(inside, outside, sigma, center=None):
    """One closed shoreline around the studies in `inside`, with every study in `outside` left out.

    The shore is a level set of a smooth field: a soft bump on each inside study, a sharp dip on each
    outside one, and a faint ripple so it looks natural. Only the outer contour is kept, so the region
    is one piece with no holes; then it is checked against every study."""
    y0, y1, x0, x1, s = GRID
    ys, xs = np.mgrid[y0:y1:s, x0:x1:s].astype(float)

    def bump(c, sig):
        return np.exp(-((xs - c[0]) ** 2 + (ys - c[1]) ** 2) / (2 * sig ** 2))

    field = 1.6 * bump(center, sigma * 1.3) if center else 0 * xs
    for nd in inside:
        field = field + bump(nd["xy"], sigma)
    for nd in outside:
        field = field - 2.6 * bump(nd["xy"], 13)
    field = field + 0.06 * np.sin(xs / 37 + 0.3) * np.sin(ys / 29 + 1.1)
    target = center or inside[0]["xy"]
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
    # pick a tree of about 200 studies whose layout keeps every study clear of the others, and whose
    # core can be drawn as one lake that leaves every other study outside
    for seed in range(2000):
        nodes = build_tree(seed)
        if not 190 <= len(nodes) - 1 <= 220:
            continue
        spread, aspect = place(nodes, seed)
        promote(nodes)
        share = sum(nd["core"] for nd in nodes[1:]) / (len(nodes) - 1)
        if spread > 0.25 or aspect < 1.35 or min_gap(nodes) < 18 or not 0.17 <= share <= 0.24:
            continue
        try:
            html = render(nodes, seed)
        except AssertionError as err:
            print(f"seed {seed}: {err}")
            continue
        OUT.write_text(html)
        print(f"wrote {OUT}")
        return


def render(nodes, seed):
    CX, CY = nodes[0]["xy"]
    total = len(nodes) - 1
    core = [nd for nd in nodes[1:] if nd["core"]]
    rest = [nd for nd in nodes[1:] if not nd["core"]]
    xs_, ys_ = [nd["xy"][0] for nd in nodes], [nd["xy"][1] for nd in nodes]
    lengths = [math.dist(nd["xy"], nodes[nd["parent"]]["xy"]) for nd in nodes[1:]]
    print(f"edges {np.mean(lengths):.0f}px ± {np.std(lengths) / np.mean(lengths):.0%}")
    print(f"seed {seed}: {total} studies, {len(core)} in the core ({len(core) / total:.0%}); "
          f"x {min(xs_):.0f}-{max(xs_):.0f}, y {min(ys_):.0f}-{max(ys_):.0f}; closest pair {min_gap(nodes):.0f}px")

    # the gem: about ten core studies grown outward from the question, always taking the core study
    # closest to what is already in the gem, so the carved part stays compact and connected
    gem, frontier = [], [k for k in nodes[0]["kids"] if nodes[k]["core"]]
    while frontier and len(gem) < 10:
        pts = [nodes[0]["xy"]] + [nd["xy"] for nd in gem]
        cx_, cy_ = sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
        i = min(frontier, key=lambda i: math.dist(nodes[i]["xy"], (cx_, cy_)))
        frontier.remove(i)
        gem.append(nodes[i])
        frontier += [k for k in nodes[i]["kids"] if nodes[k]["core"]]
    print(f"gem: {len(gem)} studies")

    def edge(nd, color, width=2):
        (ax, ay), (bx, by) = nodes[nd["parent"]]["xy"], nd["xy"]
        r_a = R_ROOT if nd["parent"] == 0 else R_NODE
        d = math.dist((ax, ay), (bx, by))
        ux, uy = (bx - ax) / d, (by - ay) / d
        sx, sy, ex, ey = ax + ux * r_a, ay + uy * r_a, bx - ux * R_NODE, by - uy * R_NODE
        return (f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" stroke-width="{width}"/>')

    def disc(nd, fill, r=R_NODE):
        return f'<circle cx="{nd["xy"][0]:.1f}" cy="{nd["xy"][1]:.1f}" r="{r}" fill="{fill}"/>'

    # one lake per level that adds core studies, each containing the last
    lakes, last = [], 0
    for k in range(1, STEPS + 1):
        inside = [nd for nd in core if nd["step"] <= k]
        if len(inside) > last:
            last = len(inside)
            lakes.append(full(f'<path d="{shore(inside, rest, 46, (CX, CY))}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                              f"The established core grows at level {k}: one contiguous lake.", f"fade {k}"))
    levels = []
    for k in range(1, STEPS + 1):
        here = [nd for nd in nodes[1:] if nd["step"] == k]
        art = "".join(edge(nd, RED if nd["core"] else STRAW_EDGE) for nd in here)
        art += "".join(disc(nd, RED if nd["core"] else STRAW) for nd in here)
        levels.append(full(art, f"Step {k}: {len(here)} new studies, {sum(nd['core'] for nd in here)} of them promoted.", f"fade {k}"))
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
    gem_shape = shore(gem, [nd for nd in nodes[1:] if nd not in gem], 32, (CX, CY))
    gem_art = (f'<path d="{gem_shape}" fill="{SAPPHIRE_SOFT}" stroke="{SAPPHIRE}" stroke-width="3" stroke-linejoin="round"/>'
               + "".join(edge(nd, SAPPHIRE, 3) for nd in gem)
               + "".join(disc(nd, SAPPHIRE, R_NODE + 1) for nd in gem)
               + f'<circle cx="{CX}" cy="{CY}" r="{R_ROOT + 1}" fill="{INK}" stroke="{SAPPHIRE}" stroke-width="3"/>')
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
    return section("gem", head + "\n" + "\n".join(layers), notes)


if __name__ == "__main__":
    main()

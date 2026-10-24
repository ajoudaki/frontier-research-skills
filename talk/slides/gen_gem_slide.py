"""Generate talk/slides/slides/{strategy,gem}.html: the whole project as a haystack, a small part of it as the gem.

The same graph serves both: the strategy at a glance (slide 02, with a light legend) and the recap
(slide 10, with the skills drawn as a pipeline in the colours of the regions they produce).

A tree of about 150 studies grows from the research question. Most studies lead to exactly one
next study; only a few are branching points with two to four branches, inside the core and outside
it alike. Any study may branch, promoted or not: by default studies don't see each other, but with
your approval one can build on another's unpromoted work.

Layout: Graphviz neato places the tree, then every edge is rebuilt at exactly one length along the
direction neato chose; only layouts with no crossing edges and comfortable spacing are kept.

Two shorelines: the established core is one contiguous lake with a single shore around the promoted
studies (about a fifth of the graph), with every unpromoted study outside it; and the explored region
around all studies has its own shore, where uncharted waters begin. Then the haystack dims, and a
compact part of the core, grown from the research question, is carved out for a paper and shown as
the gem, in the same sapphire as the gem on the opening slide.

Usage: python talk/slides/gen_gem_slide.py
"""

import json
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from matplotlib.path import Path as Polygon
from skimage import measure

from gen_skill_slides import BG, CORE, DARK, INK, MONO, MUTED, PAPER, RED, SANS, SERIF, arrow, p, section, svg

OUT = Path(__file__).resolve().parent / "slides" / "gem.html"
SNAPSHOT = Path(__file__).resolve().parent / "gem_snapshot.json"   # the final picture, reused on the conclusion slide

SAPPHIRE, SAPPHIRE_SOFT = "#2F6FC9", "#DCE7F6"
STRAW, STRAW_EDGE = "#CDB98C", "#D9CCAE"
CHARTED, CHARTED_EDGE = "#EFEADF", "#C9BFA8"
GEM = ('<polygon points="22,4 68,4 86,28 45,76 4,28" fill="{fill}"/>'
       '<polyline points="4,28 86,28" fill="none" stroke="{line}" stroke-width="3"/>'
       '<polyline points="22,4 34,28 45,76 56,28 68,4" fill="none" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>')

STUDIES = 150
STEPS = 6                       # build steps for the growth
R_NODE = 5                      # every study is drawn at this size
R_ROOT = 13                     # the research question, drawn larger
AREA = (200, 350, 1250, 905)    # x0, y0, x1, y1: where the graph may sit on the slide


def build_tree(seed):
    """Mostly single lines of work: a study usually leads to one next study, sometimes stops, and
    occasionally branches into two, three or four."""
    rng = random.Random(seed)
    nodes = [{"level": 0, "parent": None, "kids": []}]

    def add(parent):
        nodes.append({"level": nodes[parent]["level"] + 1, "parent": parent, "kids": []})
        nodes[parent]["kids"].append(len(nodes) - 1)
        return len(nodes) - 1

    frontier = [add(0) for _ in range(5)]
    while frontier and len(nodes) <= STUDIES:
        new = []
        for i in frontier:
            if len(nodes) > STUDIES:
                break
            if nodes[i]["level"] > 2 and rng.random() < 0.09:
                continue
            r = rng.random()
            kids = 4 if r < 0.015 else 3 if r < 0.05 else 2 if r < 0.15 else 1
            new += [add(i) for _ in range(kids)]
        frontier = new
    return nodes


def neato(nodes, seed):
    lines = [f"graph G {{ graph [start={seed}, maxiter=20000, epsilon=0.0000001]; node [shape=point, width=0.05]; edge [len=1];"]
    lines += [f"  {i} -- {k};" for i, nd in enumerate(nodes) for k in nd["kids"]]
    lines.append("}")
    out = subprocess.run(["neato", "-Tplain"], input="\n".join(lines), capture_output=True, text=True, check=True).stdout
    pos = {}
    for row in out.splitlines():
        f = row.split()
        if f and f[0] == "node":
            pos[int(f[1])] = (float(f[2]), float(f[3]))
    return np.array([pos[i] for i in range(len(nodes))])


def place(nodes, seed):
    """Lay the tree out with neato, rebuild every edge at unit length along neato's direction, turn the
    long axis across the slide, and scale uniformly into AREA. Returns crossing count, closest pair and
    closest node-to-edge distance (both in edge lengths), the aspect ratio, and the edge length in px."""
    P = neato(nodes, seed)
    rng = random.Random(seed + 1)
    Q = np.zeros_like(P)
    turn = {0: 0.0}
    order = [0]
    for i in order:
        for k in nodes[i]["kids"]:
            # follow neato's direction, with a slowly wandering turn so lines meander a little
            turn[k] = 0.6 * turn[i] + rng.gauss(0, 0.09)
            v = P[k] - P[i]
            a = math.atan2(v[1], v[0]) + turn[k]
            Q[k] = Q[i] + (math.cos(a), math.sin(a))
            order.append(k)
    Q -= Q.mean(0)
    _, _, vt = np.linalg.svd(Q, full_matrices=False)
    Q = Q @ vt.T
    aspect = np.ptp(Q[:, 0]) / np.ptp(Q[:, 1])
    edges = [(nd["parent"], i) for i, nd in enumerate(nodes) if i]
    cross = crossings(Q, edges)
    gap = (np.sqrt(((Q[:, None] - Q[None]) ** 2).sum(-1)) + np.eye(len(Q)) * 1e9).min()
    near = min_node_edge(Q, edges)
    x0, y0, x1, y1 = AREA
    scale = min((x1 - x0) / np.ptp(Q[:, 0]), (y1 - y0) / np.ptp(Q[:, 1]))
    Q = (Q - Q.min(0)) * scale
    Q += ((x0 + x1 - Q[:, 0].max()) / 2, (y0 + y1 - Q[:, 1].max()) / 2)
    for nd, (x, y) in zip(nodes, Q):
        nd["xy"] = (float(x), float(y))
    return cross, gap, near, aspect, scale


def crossings(P, edges):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    count = 0
    for x in range(len(edges)):
        a, b = edges[x]
        for y in range(x + 1, len(edges)):
            c, d = edges[y]
            if len({a, b, c, d}) == 4 and ccw(P[a], P[c], P[d]) != ccw(P[b], P[c], P[d]) and ccw(P[a], P[b], P[c]) != ccw(P[a], P[b], P[d]):
                count += 1
    return count


def min_node_edge(P, edges):
    near = 1e9
    for a, b in edges:
        A, AB = P[a], P[b] - P[a]
        t = np.clip(((P - A) @ AB) / (AB @ AB), 0, 1)
        dist = np.linalg.norm(P - (A + t[:, None] * AB), axis=1)
        dist[[a, b]] = 1e9
        near = min(near, dist.min())
    return near


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
        return sum(nd["core"] for nd in nodes[1:]) / (len(nodes) - 1)

    lo, hi = 20.0, 900.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mark(mid) < share else (lo, mid)
    return mark(hi)


GRID = (250, 1010, 120, 1330, 3)   # y0, y1, x0, x1, step: the slide area the fields are evaluated on


def shore(inside, outside, sigma, center=None, dip=None):
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
        field = field - 2.6 * bump(nd["xy"], dip)
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
    # keep the first tree whose layout has no crossing edges, comfortable spacing, a wide shape, and a
    # core that can be drawn as one lake leaving every other study outside
    for seed in range(3000):
        nodes = build_tree(seed)
        if len(nodes) - 1 < STUDIES - 5:
            continue
        cross, gap, near, aspect, scale = place(nodes, seed)
        if cross or gap < 0.55 or near < 0.4 or aspect < 1.15 or scale < 27:
            continue
        share = promote(nodes)
        if not 0.17 <= share <= 0.24:
            continue
        try:
            pages = {sid: render(nodes, scale, sid) for sid in ("strategy", "gem")}
        except AssertionError as err:
            print(f"seed {seed}: {err}")
            continue
        for sid, html in pages.items():
            (OUT.parent / f"{sid}.html").write_text(html)
            print(f"wrote {sid}.html")
        print(f"seed {seed}: edges {scale:.0f}px, closest pair {gap:.2f} edges, closest node to edge {near:.2f} edges, aspect {aspect:.2f}")
        return
    raise SystemExit("no layout passed the checks")


def render(nodes, edge_px, variant):
    CX, CY = nodes[0]["xy"]
    total = len(nodes) - 1
    core = [nd for nd in nodes[1:] if nd["core"]]
    rest = [nd for nd in nodes[1:] if not nd["core"]]
    deepest = max(nd["level"] for nd in nodes)
    for nd in nodes[1:]:
        nd["step"] = min(STEPS, 1 + (nd["level"] - 1) * STEPS // deepest)
    print(f"{total} studies, {len(core)} in the core ({len(core) / total:.0%}), deepest line {deepest} studies")

    # the gem: about ten core studies grown outward from the question, always taking the core study
    # closest to what is already in the gem, so the carved part stays compact and connected
    gem, frontier = [], [k for k in nodes[0]["kids"] if nodes[k]["core"]]
    while frontier and len(gem) < 10:
        pts = [nodes[0]["xy"]] + [nd["xy"] for nd in gem]
        gx, gy = sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
        i = min(frontier, key=lambda i: math.dist(nodes[i]["xy"], (gx, gy)))
        frontier.remove(i)
        gem.append(nodes[i])
        frontier += [k for k in nodes[i]["kids"] if nodes[k]["core"]]

    def edge(nd, color, width=2):
        (ax, ay), (bx, by) = nodes[nd["parent"]]["xy"], nd["xy"]
        d = math.dist((ax, ay), (bx, by))
        ux, uy = (bx - ax) / d, (by - ay) / d
        r_a = R_ROOT if nd["parent"] == 0 else R_NODE
        return (f'<line x1="{ax + ux * r_a:.1f}" y1="{ay + uy * r_a:.1f}" x2="{bx - ux * R_NODE:.1f}" y2="{by - uy * R_NODE:.1f}" '
                f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')

    def disc(nd, fill, r=R_NODE):
        return f'<circle cx="{nd["xy"][0]:.1f}" cy="{nd["xy"][1]:.1f}" r="{r}" fill="{fill}"/>'

    question = f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="{R_ROOT}" fill="{INK}"/>'
    for nd in nodes[1:]:
        assert math.dist(nd["xy"], (CX, CY)) >= R_ROOT + R_NODE + 4, "a study crowds the research question"
    sea, lake = 1.15 * edge_px, 0.95 * edge_px

    # the explored region's shore grows step by step on both slides
    charted = []
    for k in range(1, STEPS + 1):
        known = [nd for nd in nodes[1:] if nd["step"] <= k]
        charted.append(full(f'<path d="{shore(known, [], sea, (CX, CY))}" fill="{CHARTED}" stroke="{CHARTED_EDGE}" stroke-width="2" '
                            f'stroke-dasharray="7 6" stroke-linejoin="round"/>', f"Step {k}: the explored region grows.", f"fade {k}"))
    core_shape = shore(core, rest, lake, (CX, CY), 0.3 * edge_px)
    core_art = "".join(edge(nd, RED) for nd in core) + "".join(disc(nd, RED) for nd in core) + question
    xs, ys = [nd["xy"][0] for nd in nodes], [nd["xy"][1] for nd in nodes]
    x0, y0, x1, y1 = min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60

    gem_shape = shore(gem, [nd for nd in nodes[1:] if nd not in gem], 0.8 * edge_px, (CX, CY), 0.3 * edge_px)
    gem_art = (f'<path d="{gem_shape}" fill="{SAPPHIRE_SOFT}" stroke="{SAPPHIRE}" stroke-width="3" stroke-linejoin="round"/>'
               + "".join(edge(nd, SAPPHIRE, 3) for nd in gem)
               + "".join(disc(nd, SAPPHIRE, R_NODE + 1) for nd in gem)
               + f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="{R_ROOT + 1}" fill="{INK}" stroke="{SAPPHIRE}" stroke-width="3"/>')
    carve = full(gem_art, "A compact part of the core, grown from the question, carved out for the paper.", "fade 8")
    root = full(question, "The research question.")

    if variant == "strategy":
        # the research thrusts grow first, all alike; then the established core is revealed inside them
        levels = []
        for k in range(1, STEPS + 1):
            here = [nd for nd in nodes[1:] if nd["step"] == k]
            art = "".join(edge(nd, STRAW_EDGE) for nd in here) + "".join(disc(nd, STRAW) for nd in here)
            levels.append(full(art, f"Step {k}: {len(here)} new studies in the research thrusts.", f"fade {k}"))
        reveal = [full(f'<path d="{core_shape}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                       "The established core: the fully audited and relevant parts, one contiguous lake.", "fade 7")]
        layers = charted + reveal + levels + [root, full(core_art, "The established core.", "fade 7"), carve,
                                              p(128, 320, 320, "uncharted waters", 28, MUTED, family=SERIF, build="fade 6", extra="; font-style:italic")]
    else:
        # the core grows with the thrusts; then the haystack dims and the core stands out
        lakes, levels, last = [], [], 0
        for k in range(1, STEPS + 1):
            inside = [nd for nd in core if nd["step"] <= k]
            if len(inside) > last:
                last = len(inside)
                lakes.append(full(f'<path d="{shore(inside, rest, lake, (CX, CY), 0.3 * edge_px)}" fill="{CORE}" stroke="{RED}" '
                                  f'stroke-width="3" stroke-linejoin="round"/>', f"Step {k}: the established core grows, one contiguous lake.", f"fade {k}"))
            here = [nd for nd in nodes[1:] if nd["step"] == k]
            art = "".join(edge(nd, RED if nd["core"] else STRAW_EDGE) for nd in here)
            art += "".join(disc(nd, RED if nd["core"] else STRAW) for nd in here)
            levels.append(full(art, f"Step {k}: {len(here)} new studies, {sum(nd['core'] for nd in here)} of them promoted.", f"fade {k}"))
        dim = full(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" fill="{BG}" opacity="0.55"/>',
                   "The haystack fades.", "fade 7")
        again = [full(f'<path d="{core_shape}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                      "The established core.", "fade 7"), full(core_art, "The established core, highlighted.", "fade 7")]
        layers = charted + lakes + levels + [root, dim] + again + [carve,
                 p(128, 320, 320, "uncharted waters", 28, MUTED, family=SERIF, build="fade 7", extra="; font-style:italic")]
        # the final picture, for the conclusion slide
        snapshot = (charted[-1].split(">", 1)[1].rsplit("</svg>", 1)[0]
                    + f'<path d="{core_shape}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>'
                    + "".join(edge(nd, RED if nd["core"] else STRAW_EDGE) for nd in nodes[1:])
                    + "".join(disc(nd, RED if nd["core"] else STRAW) for nd in nodes[1:]) + gem_art)
        SNAPSHOT.write_text(json.dumps({"viewBox": [x0, y0, x1 - x0, y1 - y0], "svg": snapshot}))

    # the right-hand column
    C = 1350
    if variant == "strategy":
        # a light legend, introduced as the narration reaches each part, and the question for the next slide
        def legend(top, swatch, title, sub, build):
            return [svg(C, top + 4, 40, 40, swatch, title, build),
                    p(C + 56, top, 386, title, 28, INK, 600, family=SERIF, build=build),
                    p(C + 56, top + 40, 386, sub, 22, MUTED, build=build)]
        col = (legend(320, f'<circle cx="20" cy="20" r="13" fill="{INK}"/>', "Open-ended question", "where every research thrust starts", None)
               + legend(430, f'<rect x="2" y="2" width="36" height="36" rx="8" fill="{CHARTED}" stroke="{CHARTED_EDGE}" stroke-width="2" stroke-dasharray="5 4"/>'
                      f'<circle cx="20" cy="20" r="6" fill="{STRAW}"/>', "Research thrusts", "fresh exploration, pushed forward", "fade 1")
               + legend(540, f'<rect x="2" y="2" width="36" height="36" rx="8" fill="{CORE}" stroke="{RED}" stroke-width="3"/>'
                        f'<circle cx="20" cy="20" r="6" fill="{RED}"/>', "Established core", "the fully audited and relevant parts", "fade 7")
               + legend(650, f'<g transform="scale(0.44)">{GEM.format(fill=SAPPHIRE, line=PAPER)}</g>', "The gem: a paper",
                        "carved out, audited for novelty and significance", "fade 8")
               + [p(C, 780, 442, "That's the gem in the haystack.", 30, SAPPHIRE, 600, family=SERIF, build="fade 9"),
                  p(128, 950, 1664, "Easier said than done. How do we actually achieve it?", 30, RED, family=SERIF, build="fade 10",
                    extra="; font-style:italic")])
    else:
        # four regions as a pipeline, coloured like the graph; the skills annotate the edges between them
        def block(top, label, fill, border, color, build, dashed=False, height=64, pad_left=24):
            style = "dashed" if dashed else "solid"
            return (f'  <div data-build-in="{build}" style="position:absolute; top:{top}px; left:{C}px; width:442px; height:{height}px; '
                    f'padding:{(height - 34) / 2 - 2:.0f}px 24px 0 {pad_left}px; background:{fill}; border:2px {style} {border}; border-radius:14px">\n'
                    f'    <p style="{SERIF}; font-size:28px; line-height:34px; font-weight:600; color:{color}">{label}</p>\n  </div>')

        def link(top, height, color, lines, build):
            return [svg(C + 30, top, 40, height, arrow(20, 4, 20, height - 4, color, 3), lines[0], build),
                    p(C + 84, top + (height - 30 * len(lines)) / 2, 358, "<br>".join(lines), 21, color, build=build,
                      extra=f"; {MONO}; line-height:1.43")]

        mono = ["organize-research-project", "formulate-problem", "solve-problem", "teach-material"]
        col = ([block(310, "Open-ended question", INK, INK, "#F6F4EF", "fade 0")]
               + link(380, 134, DARK, mono, "fade 1")
               + [block(520, "Research thrusts", CHARTED, CHARTED_EDGE, INK, "rise 1", dashed=True)]
               + link(590, 66, RED, ["promotion gate"], "fade 7")
               + [block(662, "Established core", CORE, RED, RED, "rise 7")]
               + link(732, 76, SAPPHIRE, ["review-paper:", "novelty, significance"], "fade 8")
               + [block(814, "Carved-out paper", SAPPHIRE_SOFT, SAPPHIRE, INK, "rise 8", height=80, pad_left=110),
                  svg(C + 18, 820, 76, 68, f'<g transform="scale(0.84)">{GEM.format(fill=SAPPHIRE, line=PAPER)}</g>', "The gem.", "pop 9")])
        col[0] = col[0].replace(' data-build-in="fade 0"', "")

    eyebrow, title = (("02 · The strategy", "The strategy at a glance.") if variant == "strategy"
                      else ("10 · Putting it all together", "From the haystack to the core to the gem."))
    head = (f'  <div style="display:flex; flex-direction:column; gap:12px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>\n  </div>')
    layers = layers + col
    if variant == "strategy":
        notes = ("Here's the strategy at a glance, and it answers both questions. Start from one open-ended research question. "
                 "We organize it into research thrusts: separate lines of exploration, each pushed forward. "
                 "Most go step by step; "
                 "now and then one splits; "
                 "some stop. "
                 "And the explored region keeps growing. "
                 "Its shore is where the uncharted waters begin. "
                 "Inside it, the parts that are fully audited and relevant form the established core, always in one piece. "
                 "So instead of reading everything, you read the core: that's the signal-to-noise ratio, and that's how you stay in control. "
                 "Finally, a part of the core is carved out and audited again, for novelty and significance: is it scientifically "
                 "worthy? That's the paper, "
                 "and that's the gem in the haystack. "
                 "But this is easier said than done. How do we actually achieve it?")
        return section("strategy", head + "\n" + "\n".join(layers), notes)
    notes = ("Let's put it all together, now that we've seen every piece. We start from one open-ended question. "
             "organize-research-project turns it into research thrusts, and inside each one, formulate, solve and learn. "
             "The explored region grows fast, and its shore is where the uncharted waters begin. "
             "The core grows slowly, through the promotion gate, and always in one piece. "
             "That's the balance between exploration and exploitation: fresh, independent exploration out at the edge, "
             "and a core you can build on. "
             "And every step raised the signal-to-noise ratio: agents in adversarial positions audit each other, keep the spirit of the "
             "question, solve it without much help from us, and help us understand the result, so we can judge it quickly. "
             "Then review-paper audits the carved-out part as a whole paper: the claims, the literature, the novelty. "
             "Only a small part of everything we explored becomes the paper. Reading all of it would have been an enormous effort; "
             "reading and digesting this part is not. That's the gem in the haystack. So let me wrap up.")
    return section("gem", head + "\n" + "\n".join(layers), notes)

if __name__ == "__main__":
    main()

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
around all studies has its own shore, where uncharted waters begin.

Both slides animate the same way: the research thrusts grow first; the core starts a couple of steps
later and grows steadily until just after the thrusts are done; then a compact part of the core, grown
from the research question, is carved out for a paper and shown as the gem, in the same sapphire as
the gem on the opening slide.

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
SNAPSHOT = Path(__file__).resolve().parent / "gem_snapshot.json"
EXTRA = {}                       # interlude pages built alongside the two slides   # the final picture, reused on the conclusion slide

SAPPHIRE, SAPPHIRE_SOFT = "#2F6FC9", "#DCE7F6"
STRAW, STRAW_EDGE = "#CDB98C", "#D9CCAE"
CHARTED, CHARTED_EDGE = "#EFEADF", "#C9BFA8"
GEM = ('<polygon points="22,4 68,4 86,28 45,76 4,28" fill="{fill}"/>'
       '<polyline points="4,28 86,28" fill="none" stroke="{line}" stroke-width="3"/>'
       '<polyline points="22,4 34,28 45,76 56,28 68,4" fill="none" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>')

STUDIES = 150
STEPS = 6                       # build steps for the research thrusts
CORE_START, CORE_END = 3, STEPS + 1   # the established core starts later and keeps growing a step past the thrusts
GEM_STEP = CORE_END + 1         # the carved-out paper comes last
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


def shore(inside, outside, sigma, center=None, dip=None, polygon=False):
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
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in best[::2]) + " Z"
    return (path, region) if polygon else path


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
        for sid, html in {**pages, **EXTRA}.items():
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
    xs, ys = [nd["xy"][0] for nd in nodes], [nd["xy"][1] for nd in nodes]
    x0, y0, x1, y1 = min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60

    # one push out of the explored region: from a study in the core at the edge, a dashed edge into
    # uncharted waters, where the next thrust has to break through; circled to zoom into on the next slide
    _, explored = shore(nodes[1:], [], sea, (CX, CY), polygon=True)
    best = None
    for nd, reach in ((nd, f * edge_px) for nd in core for f in (1.6, 2.0, 2.4, 2.8)):
        out_dir = math.atan2(nd["xy"][1] - CY, nd["xy"][0] - CX)
        for deg in range(0, 360, 5):
            a = math.radians(deg)
            nx, ny = nd["xy"][0] + reach * math.cos(a), nd["xy"][1] + reach * math.sin(a)
            if not (200 <= nx <= 1250 and 360 <= ny <= 900):
                continue
            ring = [(nx + 0.4 * edge_px * math.cos(b), ny + 0.4 * edge_px * math.sin(b)) for b in [k * math.pi / 6 for k in range(12)]]
            if explored.contains_point((nx, ny)) or any(explored.contains_point(q) for q in ring):
                continue
            room = min(math.dist((nx, ny), o["xy"]) for o in nodes)
            path_room = min(min(math.dist(o["xy"], (nd["xy"][0] + s * (nx - nd["xy"][0]), nd["xy"][1] + s * (ny - nd["xy"][1])))
                                for s in (0.25, 0.5, 0.75)) for o in nodes if o is not nd)
            if room < 1.2 * edge_px or path_room < 0.6 * edge_px:
                continue
            score = room - 0.6 * reach + (0.5 * edge_px if not nd["kids"] else 0) + 0.5 * edge_px * math.cos(a - out_dir)
            if best is None or score > best[0]:
                best = (score, nd, (nx, ny), reach)
    assert best, "no study in the core can push out into uncharted waters here"
    _, edge_nd, (nx, ny), reach = best
    (px, py), push_ang = edge_nd["xy"], math.atan2(ny - edge_nd["xy"][1], nx - edge_nd["xy"][0])
    # a dashed shaft ending in an arrowhead, pointing out into uncharted waters
    ux, uy = math.cos(push_ang), math.sin(push_ang)
    head_len, head_w = 16, 9
    bx, by = nx - ux * head_len, ny - uy * head_len
    push_art = (f'<line x1="{px + R_NODE * ux:.1f}" y1="{py + R_NODE * uy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
                f'stroke="{INK}" stroke-width="3" stroke-dasharray="6 5" stroke-linecap="round"/>'
                f'<polygon points="{nx:.1f},{ny:.1f} {bx - uy * head_w:.1f},{by + ux * head_w:.1f} {bx + uy * head_w:.1f},{by - ux * head_w:.1f}" '
                f'fill="{INK}" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
    mx, my, ring_r = (px + nx) / 2, (py + ny) / 2, reach / 2 + 20

    gem_shape = shore(gem, [nd for nd in nodes[1:] if nd not in gem], 0.8 * edge_px, (CX, CY), 0.3 * edge_px)
    gem_art = (f'<path d="{gem_shape}" fill="{SAPPHIRE_SOFT}" stroke="{SAPPHIRE}" stroke-width="3" stroke-linejoin="round"/>'
               + "".join(edge(nd, SAPPHIRE, 3) for nd in gem)
               + "".join(disc(nd, SAPPHIRE, R_NODE + 1) for nd in gem)
               + f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="{R_ROOT + 1}" fill="{INK}" stroke="{SAPPHIRE}" stroke-width="3"/>')
    carve = full(gem_art, "A compact part of the core, grown from the question, carved out for the paper.", f"fade {GEM_STEP}")
    root = full(question, "The research question.")

    # the same growth on both slides: research thrusts grow for STEPS steps; the established core starts later
    # and grows steadily, breadth first, until a step after the thrusts are done; then the gem
    ranked = sorted(core, key=lambda nd: (nd["level"], nodes.index(nd)))
    span = CORE_END - CORE_START + 1
    for r, nd in enumerate(ranked):
        nd["core_step"] = max(CORE_START + r * span // len(ranked), nd["step"] + 1)
    levels, lakes, promoted, last = [], [], [], 0
    for k in range(1, STEPS + 1):
        here = [nd for nd in nodes[1:] if nd["step"] == k]
        art = "".join(edge(nd, STRAW_EDGE) for nd in here) + "".join(disc(nd, STRAW) for nd in here)
        levels.append(full(art, f"Step {k}: {len(here)} new studies in the research thrusts.", f"fade {k}"))
    for k in range(CORE_START, CORE_END + 1):
        inside = [nd for nd in core if nd["core_step"] <= k]
        fresh = [nd for nd in core if nd["core_step"] == k]
        if len(inside) > last:
            last = len(inside)
            lakes.append(full(f'<path d="{shore(inside, rest, lake, (CX, CY), 0.3 * edge_px)}" fill="{CORE}" stroke="{RED}" '
                              f'stroke-width="3" stroke-linejoin="round"/>', f"Step {k}: the established core grows, one contiguous lake.", f"fade {k}"))
        if fresh:
            promoted.append(full("".join(edge(nd, RED) for nd in fresh) + "".join(disc(nd, RED) for nd in fresh),
                                 f"Step {k}: {len(fresh)} studies pass the promotion gate.", f"fade {k}"))
    layers = charted + lakes + levels + promoted + [root, carve]
    if variant == "strategy":
        # the push into uncharted waters, then the circle around it, which the next slide magnifies
        side = 1 if math.cos(push_ang) >= 0 else -1
        lx = nx + 22 if side > 0 else nx - 22 - 260
        layers += [full(push_art, "A study at the edge of the core pushes into uncharted waters.", f"fade {GEM_STEP + 1}"),
                   p(lx, ny + (8 if math.sin(push_ang) > 0 else -44), 260, "uncharted waters", 28, MUTED, "left" if side > 0 else "right",
                     family=SERIF, build=f"fade {GEM_STEP + 1}", extra="; font-style:italic"),
                   full(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{ring_r:.1f}" fill="none" stroke="{INK}" stroke-width="3"/>',
                        "A circle around the push, to zoom into.", f"fade {GEM_STEP + 2}")]
    else:
        layers.append(p(x0 + 20, y0, 320, "uncharted waters", 28, MUTED, family=SERIF, build=f"fade {STEPS}", extra="; font-style:italic"))
        # the same picture, scaled into the space left by the strip above and the install box on the right
        bx0, by0, bx1, by1 = 128, 420, 1200, 955
        sc = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
        dx = bx0 - x0 * sc + ((bx1 - bx0) - (x1 - x0) * sc) / 2
        dy = by0 - y0 * sc + ((by1 - by0) - (y1 - y0) * sc) / 2
        layers = ([f'  <div style="position:absolute; top:0; left:0; width:1920px; height:1080px; transform:translate({dx:.1f}px, {dy:.1f}px) '
                   f'scale({sc:.4f}); transform-origin:0 0">'] + layers + ["  </div>"])
    # the final picture: the strategy slide zooms into it, and the conclusion slide shows it in miniature
    snapshot = (charted[-1].split(">", 1)[1].rsplit("</svg>", 1)[0]
                + f'<path d="{core_shape}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>'
                + "".join(edge(nd, RED if nd["core"] else STRAW_EDGE) for nd in nodes[1:])
                + "".join(disc(nd, RED if nd["core"] else STRAW) for nd in nodes[1:]) + gem_art)
    if variant == "strategy":
        # the interlude after this slide: the map in a corner, the circled push magnified, and the question
        vx, vy, vw, vh = x0, y0, x1 - x0, y1 - y0
        IW, IX, IY = 480, 200, 310
        s = IW / vw
        IH = round(vh * s)
        BR, bx, by = 250, 1330, 560
        zoom = 1.25 * ring_r
        sx, sy, sr = IX + (mx - vx) * s, IY + (my - vy) * s, ring_r * s
        tx, ty = bx + (nx - mx) * BR / zoom, by + (ny - my) * BR / zoom      # the arrow tip, magnified
        zl = [f'  <svg aria-label="The map, shrunk, with the push into uncharted waters circled." '
              f'style="position:absolute; top:{IY}px; left:{IX}px; width:{IW}px; height:{IH}px" width="{IW}" height="{IH}" '
              f'viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}">{snapshot}{push_art}'
              f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{ring_r:.1f}" fill="none" stroke="{INK}" stroke-width="{3 / s:.1f}"/></svg>',
              full(f'<line x1="{sx:.1f}" y1="{sy - sr:.1f}" x2="{bx:.1f}" y2="{by - BR:.1f}" stroke="{INK}" stroke-width="1.5"/>'
                   f'<line x1="{sx:.1f}" y1="{sy + sr:.1f}" x2="{bx:.1f}" y2="{by + BR:.1f}" stroke="{INK}" stroke-width="1.5"/>',
                   "Lines joining the small circle to its magnified view."),
              f'  <svg aria-label="The push, magnified: from the edge of the core out into uncharted waters." '
              f'style="position:absolute; top:{by - BR:.0f}px; left:{bx - BR:.0f}px; width:{2 * BR}px; height:{2 * BR}px" '
              f'width="{2 * BR}" height="{2 * BR}" viewBox="{mx - zoom:.1f} {my - zoom:.1f} {2 * zoom:.1f} {2 * zoom:.1f}">'
              f'<defs><clipPath id="lens"><circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom:.1f}"/></clipPath></defs>'
              f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom:.1f}" fill="{BG}"/>'
              f'<g clip-path="url(#lens)">{snapshot}{push_art}</g>'
              f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom - 1.5 * zoom / BR:.1f}" fill="none" stroke="{INK}" stroke-width="{3 * zoom / BR:.2f}"/></svg>']
        ux_, uy_ = math.cos(push_ang), math.sin(push_ang)
        px_, py_ = tx + ux_ * 26, ty + uy_ * 26
        if tx < bx:
            zl += [p(IX + IW + 30, py_ - 40, bx - BR - IX - IW - 70, "uncharted<br>waters", 34, INK, 600, "right", family=SERIF,
                     extra="; font-style:italic; line-height:1.15"),
                   full(f'<line x1="{bx - BR - 26:.1f}" y1="{py_:.1f}" x2="{px_:.1f}" y2="{py_:.1f}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4"/>',
                        "A leader to the uncharted waters.")]
        else:
            zl.append(p(bx - BR, by + BR - 70, 2 * BR, "uncharted waters", 34, INK, 600, "center", family=SERIF, extra="; font-style:italic"))
        zl.append(p(128, 870, 1664, "How do we make each push succeed?",
                    52, INK, 600, "center", family=SERIF, extra="; line-height:1.3").replace("<p", "<h2", 1).replace("</p>", "</h2>"))
        EXTRA["q-frontier"] = section("q-frontier", "\n".join(zl), "Let's zoom in. This is the frontier, and it's hard, even for a very capable model. "
                                      "How do we make each push succeed?")
    if variant == "gem":
        SNAPSHOT.write_text(json.dumps({"viewBox": [x0, y0, x1 - x0, y1 - y0], "svg": snapshot, "push": push_art,
                                        "base": snapshot[:-len(gem_art)], "gem": gem_art,
                                        "circle": [mx, my, ring_r], "push_line": [px, py, nx, ny]}))

    # the right-hand column
    C = 1350
    if variant == "strategy":
        # a light legend, introduced as the narration reaches each part, and the question for the next slide
        def legend(top, swatch, title, sub, build):
            return [svg(C, top + 4, 40, 40, swatch, title, build),
                    p(C + 56, top, 386, title, 28, INK, 600, family=SERIF, build=build),
                    p(C + 56, top + 40, 386, sub, 22, MUTED, build=build)]
        col = (legend(320, f'<circle cx="20" cy="20" r="13" fill="{INK}"/>', "Open-ended question", "where every thrust starts", None)
               + legend(430, f'<rect x="2" y="2" width="36" height="36" rx="8" fill="{CHARTED}" stroke="{CHARTED_EDGE}" stroke-width="2" stroke-dasharray="5 4"/>'
                      f'<circle cx="20" cy="20" r="6" fill="{STRAW}"/>', "Research thrusts", "fresh exploration, pushed forward", "fade 1")
               + legend(540, f'<rect x="2" y="2" width="36" height="36" rx="8" fill="{CORE}" stroke="{RED}" stroke-width="3"/>'
                        f'<circle cx="20" cy="20" r="6" fill="{RED}"/>', "Established core", "audited and relevant", f"fade {CORE_START}")
               + legend(650, f'<g transform="scale(0.44)">{GEM.format(fill=SAPPHIRE, line=PAPER)}</g>', "The gem: a paper",
                        "carved out, audited for novelty, significance", f"fade {GEM_STEP}")
               + [p(C, 780, 442, "That's the gem in the haystack.", 30, SAPPHIRE, 600, family=SERIF, build=f"fade {GEM_STEP}"),
                  ])
    else:
        # the four regions as one horizontal strip under the title, coloured like the graph, with the skills on the
        # edges between them; then, once the gem is in, how to use it all today
        def block(left, width, label, fill, border, color, build, dashed=False, icon=False):
            style = "dashed" if dashed else "solid"
            b_ = f' data-build-in="{build}"' if build else ""
            pad = 64 if icon else 18
            return (f'  <div{b_} style="position:absolute; top:{SY}px; left:{left}px; width:{width}px; height:56px; '
                    f'padding:10px 14px 0 {pad}px; background:{fill}; border:2px {style} {border}; border-radius:12px">\n'
                    f'    <p style="{SERIF}; font-size:22px; line-height:32px; font-weight:600; color:{color}; white-space:nowrap">{label}</p>\n  </div>')

        def link(left, width, color, lines, build):
            return [svg(left + 8, SY + 14, width - 16, 28, arrow(2, 14, width - 18, 14, color, 3), lines[0], build),
                    p(left, SY - 18 * len(lines) - 4, width, "<br>".join(lines), 17, color, align="center", build=build,
                      extra=f"; {MONO}; line-height:1.2")]

        SY = 330
        col = ([block(128, 270, "Open-ended question", INK, INK, "#F6F4EF", None)]
               + link(398, 260, DARK, ["organize-research-project", "formulate · solve · learn"], "fade 1")
               + [block(658, 230, "Research thrusts", CHARTED, CHARTED_EDGE, INK, "rise 1", dashed=True)]
               + link(888, 200, RED, ["promotion gate"], f"fade {CORE_START}")
               + [block(1088, 230, "Established core", CORE, RED, RED, f"rise {CORE_START}")]
               + link(1318, 204, SAPPHIRE, ["review-paper"], f"fade {GEM_STEP}")
               + [block(1522, 270, "Carved-out paper", SAPPHIRE_SOFT, SAPPHIRE, INK, f"rise {GEM_STEP}", icon=True),
                  svg(1534, SY + 10, 44, 40, f'<g transform="scale(0.48)">{GEM.format(fill=SAPPHIRE, line=PAPER)}</g>', "The gem.", f"pop {GEM_STEP}")])
        # how to use it today, kept short: the README has the rest
        code = f"{MONO}; font-size:17px; line-height:1.45; color:{INK}; background:#EFEBE2; border-radius:8px; padding:10px 14px; white-space:pre"
        U = GEM_STEP + 1
        col += [f'  <div data-build-in="rise {U}" style="position:absolute; top:440px; left:1220px; width:572px; height:494px; '
                f'background:{PAPER}; border:1px solid #DCD6CA; border-radius:16px"></div>',
                p(1248, 466, 500, "How to use it", 30, INK, 600, family=SERIF, build=f"rise {U}"),
                p(1248, 520, 500, "Get", 20, RED, 600, build=f"rise {U}"),
                f'  <p data-build-in="rise {U}" style="position:absolute; top:550px; left:1248px; width:516px; {code}">git clone \\\n  github.com/ajoudaki/frontier-research-skills</p>',
                p(1248, 642, 500, "Install", 20, RED, 600, build=f"rise {U}"),
                f'  <p data-build-in="rise {U}" style="position:absolute; top:672px; left:1248px; width:516px; {code}">ln -s $PWD/&lt;skill&gt; ~/.claude/skills/\n# or ~/.codex/skills/ for Codex</p>',
                p(1248, 764, 500, "Or per project", 20, RED, 600, build=f"rise {U}"),
                f'  <p data-build-in="rise {U}" style="position:absolute; top:794px; left:1248px; width:516px; {code}">name it in AGENTS.md or CLAUDE.md</p>',
                p(1248, 886, 500, "The README has the details.", 20, MUTED, build=f"rise {U}")]

    eyebrow, title = (("02 · The strategy", "The strategy at a glance.") if variant == "strategy"
                      else ("11 · Putting it all together", "From the haystack to the core to the gem."))
    head = (f'  <div style="display:flex; flex-direction:column; gap:12px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>\n  </div>')
    layers = layers + col
    if variant == "strategy":
        notes = ("Here's the strategy at a glance, and it answers both questions. Start from one open-ended research question. "
                 "We organize it into research thrusts: separate lines of exploration, each pushed forward. "
                 "Most go step by step; now and then one splits, and some stop. "
                 "And with some lag, the parts that are fully audited and relevant form the established core. "
                 "The thrusts keep pushing out, "
                 "and the core follows, always in one piece. "
                 "The explored region's shore is where the uncharted waters begin. "
                 "Instead of reading everything, you read the core: that's the signal-to-noise ratio, "
                 "and that's how you stay in control. "
                 "Finally, a part of the core is carved out and audited again, for novelty and significance: is it scientifically "
                 "worthy? That's the paper, and that's the gem in the haystack. "
                 "That's the map, the global strategy. "
                 "But look at one thrust at the edge, pushing out into uncharted waters.")
        return section("strategy", head + "\n" + "\n".join(layers), notes)
    notes = ("Now that we've seen every piece: we start from one open-ended question. "
             "organize-research-project turns it into research thrusts, and inside each one, formulate, solve and learn. "
             "The explored region grows fast, and its shore is where the uncharted waters begin. "
             "Behind it, with some lag, the core grows through the promotion gate, always in one piece. "
             "That's the balance between exploration and exploitation: fresh, independent exploration out at the edge, "
             "and a core you can build on. "
             "And every step raises the signal-to-noise ratio: agents in adversarial positions audit each other, keep the spirit of the "
             "question, solve it without much help from us, "
             "and help us understand the result, so we can judge it quickly. "
             "Then review-paper audits the carved-out part as a whole paper: the claims, the literature, the novelty. Only a small part "
             "of everything we explored becomes the paper. Reading all of it would have been an enormous effort; reading and digesting "
             "this part is not. That's the gem in the haystack. "
             "Here's how to use it. Clone the repo, link a skill into your agent's skills folder, or make it a "
             "project's default from its AGENTS.md or CLAUDE.md. The README has the details. So let me wrap up.")
    return section("gem", head + "\n" + "\n".join(layers), notes)

if __name__ == "__main__":
    main()

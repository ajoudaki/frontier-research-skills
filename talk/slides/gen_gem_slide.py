"""Generate talk/slides/slides/gem.html: the whole project as a haystack, its core as the gem.

A radial tree grows from the research question, one level per step: the level's
studies appear, then some pass the gate (red) and the rest fail (dark), and the
established core grows as an organic outline around everything that passed.
New studies branch only off promoted ones. Then the haystack dims, the core
stands out, and the core goes through the audit to become the paper.

Usage: python talk/slides/gen_gem_slide.py
"""

import math
from pathlib import Path

from gen_skill_slides import BG, BORDER, CORE, DARK, GRAY, INK, MONO, MUTED, PAPER, RED, SANS, SERIF, arrow, p, section, svg

OUT = Path(__file__).resolve().parent / "slides" / "gem.html"

# outcome of every study, level by level: P passes the gate, F fails, O is still open.
# Children hang off the promoted studies of the level above, in order.
LEVELS = [
    ["PFPFFPF"],
    ["PFF", "FPP", "PFF"],
    ["FPF", "PF", "FFP", "FP"],
    ["FPF", "FF", "PFO", "FO"],
]
CX, CY = 712, 622          # the research question, on the slide
RX, RY = 150, 78           # radii of the first level; level k sits at k times these
R_ROOT, R_NODE, PAD = 30, 12, 14


def build_tree():
    """Nodes as dicts with level, outcome, parent index; children only under promoted parents."""
    nodes = [{"level": 0, "out": "P", "parent": None, "kids": []}]
    frontier = [0]
    for groups in LEVELS:
        promoted = [i for i in frontier if nodes[i]["out"] == "P"]
        assert len(groups) == len(promoted)
        new = []
        for parent, outs in zip(promoted, groups):
            for out in outs:
                nodes.append({"level": nodes[parent]["level"] + 1, "out": out, "parent": parent, "kids": []})
                nodes[parent]["kids"].append(len(nodes) - 1)
                new.append(len(nodes) - 1)
        frontier = new
    return nodes


def layout(nodes, start):
    """Radial layout: every leaf gets an angular slot, wider the closer it sits to the centre (its ring is
    shorter); a parent sits at its children's mean angle."""
    for nd in nodes:
        nd.pop("angle", None)
    leaves = []

    def walk(i):
        if not nodes[i]["kids"]:
            leaves.append(i)
        for k in nodes[i]["kids"]:
            walk(k)

    walk(0)
    weight = [2 / nodes[i]["level"] for i in leaves]
    unit = 360 / sum(weight)
    at = start
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
    nodes[0]["xy"] = (CX, CY)


def min_gap(nodes):
    pts = [nd["xy"] for nd in nodes]
    return min(math.dist(a, b) for i, a in enumerate(pts) for b in pts[i + 1:])


def seg(a, b, r_a, r_b):
    """A line from the rim of circle a to the rim of circle b."""
    d = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
    return (a[0] + ux * r_a, a[1] + uy * r_a), (b[0] - ux * r_b, b[1] - uy * r_b)


def full(content, label, build=None):
    return svg(0, 0, 1920, 1080, content, label, build)


def main():
    nodes = build_tree()
    best = max(range(0, 360, 2), key=lambda s: (layout(nodes, s), min_gap(nodes))[1])
    layout(nodes, best)
    xs_ = [nd["xy"][0] for nd in nodes]
    print(f"x from {min(xs_):.0f} to {max(xs_):.0f}; {len(nodes) - 1} studies, {sum(nd['out'] == 'P' for nd in nodes) - 1} promoted, closest pair {min_gap(nodes):.0f}px")

    def radius(i):
        return R_ROOT if i == 0 else R_NODE

    # the core: thick strokes along promoted edges and discs on promoted nodes. Every outline layer
    # (red, wider) sits under every fill layer, so the union shows one clean organic border.
    outline, fill = [], []
    W = 2 * (R_NODE + PAD)
    for k in range(1, len(LEVELS) + 1):
        o = f = ""
        if k == 1:
            x, y = nodes[0]["xy"]
            o += f'<circle cx="{x}" cy="{y}" r="{R_ROOT + PAD + 3}" fill="{RED}"/>'
            f += f'<circle cx="{x}" cy="{y}" r="{R_ROOT + PAD}" fill="{CORE}"/>'
        for i, nd in enumerate(nodes):
            if nd["level"] == k and nd["out"] == "P":
                (x1, y1), (x2, y2) = nodes[nd["parent"]]["xy"], nd["xy"]
                o += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{RED}" stroke-width="{W + 6}" stroke-linecap="round"/>')
                f += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CORE}" stroke-width="{W}" stroke-linecap="round"/>')
        outline.append(full(o, f"The established core grows at level {k}: outline.", f"fade {2 * k}"))
        fill.append(full(f, f"The established core grows at level {k}.", f"fade {2 * k}"))

    def edge(i, color, width=3):
        (a, b) = seg(nodes[nodes[i]["parent"]]["xy"], nodes[i]["xy"], radius(nodes[i]["parent"]), R_NODE)
        return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{width}"/>'

    def disc(i, fill_, stroke=None):
        x, y = nodes[i]["xy"]
        st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R_NODE}" fill="{fill_}"{st}/>'

    grow, judge = [], []
    for k in range(1, len(LEVELS) + 1):
        level = [i for i, nd in enumerate(nodes) if nd["level"] == k]
        grow.append(full("".join(edge(i, GRAY) + disc(i, PAPER, GRAY) for i in level),
                         f"Level {k}: new studies branch out.", f"fade {2 * k - 1}"))
        verdict = ""
        for i in level:
            out = nodes[i]["out"]
            if out == "P":
                verdict += edge(i, RED) + disc(i, RED)
            elif out == "F":
                verdict += disc(i, DARK)
        judge.append(full(verdict, f"Level {k}: some studies pass the gate, the rest fail.", f"fade {2 * k}"))

    root = nodes[0]["xy"]
    question = [full(f'<circle cx="{root[0]}" cy="{root[1]}" r="{R_ROOT}" fill="{INK}"/>', "The research question.")]

    # step 9: the haystack dims and the core stands out
    xs = [nd["xy"][0] for nd in nodes]
    ys = [nd["xy"][1] for nd in nodes]
    x0, y0, x1, y1 = min(xs) - 30, min(ys) - 30, max(xs) + 30, max(ys) + 30
    dim = full(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" fill="{BG}" opacity="0.72"/>',
               "The haystack fades.", "fade 9")
    core_again = [el.replace(f'data-build-in="fade {2 * k + 2}"', 'data-build-in="fade 9"') for k, el in enumerate(outline)]
    core_again += [el.replace(f'data-build-in="fade {2 * k + 2}"', 'data-build-in="fade 9"') for k, el in enumerate(fill)]
    core_nodes = "".join(edge(i, RED) + disc(i, RED) for i, nd in enumerate(nodes) if i and nd["out"] == "P")
    core_again.append(full(core_nodes + f'<circle cx="{root[0]}" cy="{root[1]}" r="{R_ROOT}" fill="{INK}"/>', "The established core, highlighted.", "fade 9"))

    # the right-hand column: haystack and core (9), then audit and the paper (10)
    C = 1340
    col = [p(C, 330, 452, "The haystack", 34, MUTED, 600, family=SERIF, build="fade 9"),
           p(C, 378, 452, "every study, explored in isolation", 24, MUTED, build="fade 9"),
           p(C, 450, 452, "The established core", 34, RED, 600, family=SERIF, build="fade 9"),
           p(C, 498, 452, "checked, understood, approved", 24, INK, build="fade 9"),
           svg(C + 30, 548, 40, 60, arrow(20, 2, 20, 56, RED, 3), "The core goes to the audit.", "fade 10"),
           f'  <div data-build-in="rise 10" style="position:absolute; top:616px; left:{C}px; width:452px; display:flex; flex-direction:row; '
           f'align-items:center; gap:16px; padding:22px 24px; background:{PAPER}; border:1px solid {BORDER}; border-radius:16px">\n'
           f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">Audit</p>\n'
           f'    <p style="padding:4px 14px; {MONO}; font-size:24px; color:{RED}; background:{CORE}; border-radius:8px">review-paper</p>\n  </div>',
           svg(C + 30, 714, 40, 60, arrow(20, 2, 20, 56, RED, 3), "The audited core becomes the paper.", "fade 10"),
           svg(C, 790, 90, 80, f'<polygon points="22,4 68,4 86,28 45,76 4,28" fill="{RED}"/>'
               f'<polyline points="4,28 86,28" fill="none" stroke="{PAPER}" stroke-width="3"/>'
               f'<polyline points="22,4 34,28 45,76 56,28 68,4" fill="none" stroke="{PAPER}" stroke-width="3" stroke-linejoin="round"/>',
               "A gem.", "pop 10"),
           p(C + 110, 800, 342, "The paper:<br>your gem", 34, INK, 600, family=SERIF, build="fade 10")]

    head = (f'  <div style="display:flex; flex-direction:column; gap:12px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">10 · The gem in the haystack</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">From the haystack to the gem.</h2>\n  </div>')
    layers = outline + fill + grow + judge + question + [dim] + core_again + col
    notes = ("Remember the gem in the haystack? Here's what a real project looks like over time. "
             "From the research question, studies branch out. "
             "Some pass the gate and join the core; most don't. "
             "New studies branch off what passed, level by level. "
             "And the core grows with them, into this organic shape. "
             "The project keeps growing, and the more it grows, the smaller the core is in comparison. "
             "That's the point. You don't have to read the haystack. You read the core, and everything in it was formulated, solved, "
             "understood and approved. "
             "Then the core goes through the audit and becomes a paper. That's the gem. So let me wrap up.")
    OUT.write_text(section("gem", head + "\n" + "\n".join(layers), notes))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

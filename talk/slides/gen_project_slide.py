"""Generate talk/slides/slides/project.html, the animated promotion-gate slide.

Build order: studies appear one by one; the promotion-gate card comes in;
A, B, C are promoted one by one (edge and node turn orange, a tick appears on
the edge, and the established core grows to enclose them); D, E, F fail one
by one (cross on the edge); then new studies branch off the established A
and B; finally the audit card comes in.

Usage: python talk/slides/gen_project_slide.py
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "slides" / "project.html"

SANS = "font-family:'IBM Plex Sans', Arial, sans-serif"
MONO = "font-family:'IBM Plex Mono', 'Courier New', monospace"
SERIF = "font-family:'Source Serif 4', Georgia, serif"
GRAY, RED, DARK, PAPER, CORE = "#A9A293", "#B04A33", "#4A4F5C", "#FDFCF9", "#F3E3DC"

OX, OY, W, H = 128, 300, 700, 470  # the diagram's box on the slide
CENTER, R_CENTER, R_NODE = (300, 240), 62, 28
NODES = {
    "A": (150, 110), "B": (95, 265), "C": (190, 385),
    "D": (530, 90), "E": (600, 250), "F": (530, 400),
    "G": (255, 40), "H": (45, 390),
}
PARENT = {"G": "A", "H": "B"}  # branches off established studies

APPEAR = {"A": 1, "D": 2, "B": 3, "E": 4, "C": 5, "F": 6}
DEVELOP_CARD = 7
PROMOTE = {"A": 8, "B": 9, "C": 10}
FAIL = {"D": 11, "E": 12, "F": 13}
BRANCH = {"G": 14, "H": 15}
AUDIT_CARD = 16


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    return dx / length, dy / length


def endpoints(src, r_src, dst):
    """Start and arrow tip of an edge between two circles."""
    ux, uy = unit(src, dst)
    start = (src[0] + ux * r_src, src[1] + uy * r_src)
    tip = (dst[0] - ux * (R_NODE + 2), dst[1] - uy * (R_NODE + 2))
    return start, tip


def edge(src, r_src, dst, color):
    start, tip = endpoints(src, r_src, dst)
    ux, uy = unit(src, dst)
    base = (tip[0] - ux * 14, tip[1] - uy * 14)
    px, py = -uy, ux
    head = f"{tip[0]:.1f},{tip[1]:.1f} {base[0] + px * 8:.1f},{base[1] + py * 8:.1f} {base[0] - px * 8:.1f},{base[1] - py * 8:.1f}"
    return (f'<line x1="{start[0]:.1f}" y1="{start[1]:.1f}" x2="{base[0]:.1f}" y2="{base[1]:.1f}" stroke="{color}" stroke-width="3"/>'
            f'<polygon points="{head}" fill="{color}"/>')


def study_edge(n, color):
    if n in PARENT:
        return edge(NODES[PARENT[n]], R_NODE, NODES[n], color)
    return edge(CENTER, R_CENTER, NODES[n], color)


def badge_point(n, t):
    start, tip = endpoints(CENTER, R_CENTER, NODES[n])
    return start[0] + (tip[0] - start[0]) * t, start[1] + (tip[1] - start[1]) * t


def tick(n):
    x, y = badge_point(n, 0.5)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{PAPER}" stroke="{RED}" stroke-width="3"/>'
            f'<polyline points="{x - 7:.1f},{y:.1f} {x - 2:.1f},{y + 5:.1f} {x + 7:.1f},{y - 6:.1f}" fill="none" '
            f'stroke="{RED}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(n):
    x, y = badge_point(n, 0.68)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{PAPER}" stroke="{DARK}" stroke-width="3"/>'
            f'<line x1="{x - 6:.1f}" y1="{y - 6:.1f}" x2="{x + 6:.1f}" y2="{y + 6:.1f}" stroke="{DARK}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<line x1="{x + 6:.1f}" y1="{y - 6:.1f}" x2="{x - 6:.1f}" y2="{y + 6:.1f}" stroke="{DARK}" stroke-width="3.5" stroke-linecap="round"/>')


def hull(circles, pad=16, samples=72):
    """Smooth outline around circles: the convex hull of points on each padded circle."""
    pts = []
    for (cx, cy), r in circles:
        for k in range(samples):
            a = 2 * math.pi * k / samples
            pts.append((cx + (r + pad) * math.cos(a), cy + (r + pad) * math.sin(a)))
    pts = sorted(set(pts))

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    ring = lower[:-1] + upper[:-1]
    return ring


def svg(content, label, build=None):
    b = f' data-build-in="{build}"' if build else ""
    return (f'  <svg aria-label="{label}"{b} style="position:absolute; top:{OY}px; left:{OX}px; width:{W}px; height:{H}px" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">{content}</svg>')


def text(n, color, build):
    x, y = NODES[n]
    return (f'  <p data-build-in="{build}" style="position:absolute; top:{OY + y - 17}px; left:{OX + x - 28}px; width:56px; '
            f'{SANS}; font-size:24px; font-weight:600; text-align:center; color:{color}">{n}</p>')


def card(build, top, stage, chip, body):
    return f'''  <div data-build-in="rise {build}" style="position:absolute; top:{top}px; left:1000px; width:792px; display:flex; flex-direction:column; gap:12px; padding:40px; background:#fdfcf9; border:1px solid #dcd6ca; border-radius:16px">
    <div style="display:flex; flex-direction:row; gap:16px; align-items:center">
      <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#b04a33">{stage}</p>
      <p style="padding:6px 16px; {MONO}; font-size:24px; color:#b04a33; background:#f3e3dc; border-radius:8px">{chip}</p>
    </div>
{body}
  </div>'''


NOTES = (
    "Most open-ended research questions aren't a single question. You start from one big question and push in many directions. "
    "Some succeed, some don't, and from the successful ones you push further. That takes a lot of exploration, and exploration "
    "needs fresh, independent thinking: agents biased by a failed attempt keep chasing the same failed route. So develop-project "
    "keeps the thrusts, or studies, as independent as possible, mechanically limiting each one to its own isolated folder. "
    "But a project can't be purely independent, or you never build on what you've found. So the skill balances independent "
    "thrusts with an established core of theory or experiments. Results enter the core through a promotion gate: robustly "
    "audited, coherent notation, a good interface, and, most importantly, your approval. Results that fail the gate stay "
    "outside, with their evidence kept. So the core holds results that are true and worthwhile, and new studies can branch "
    "off it and build on them. That's the answer to the gem in the haystack: if it's in the core, it's worth your time to "
    "read. And when you turn the work into a paper, review-paper audits the whole package from every angle: the logic, but "
    "also the citations, the literature and the novelty. It's what a researcher with real integrity would do to their own "
    "paper. That's the whole toolkit, so let me wrap up."
)


def main():
    layers = []
    # The core grows: one outline per promotion, each enclosing the last, under everything else.
    promoted = []
    core_ring = None
    for n, build in PROMOTE.items():
        promoted.append(n)
        core_ring = hull([(CENTER, R_CENTER)] + [(NODES[m], R_NODE) for m in promoted])
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in core_ring)
        layers.append(svg(f'<polygon points="{path}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                          f"The established core grows to include study {n}.", f"fade {build}"))
    bottom = max(y for _, y in core_ring)
    core_x = sum(x for x, _ in core_ring) / len(core_ring)
    layers.append(f'  <p data-build-in="fade {PROMOTE["C"]}" style="position:absolute; top:{OY + bottom + 6:.0f}px; '
                  f'left:{OX + core_x - 150:.0f}px; width:300px; {SANS}; font-size:24px; font-weight:600; letter-spacing:3px; '
                  f'text-align:center; text-transform:uppercase; color:{RED}">Established core</p>')

    for n, build in list(APPEAR.items()) + list(BRANCH.items()):
        x, y = NODES[n]
        layers.append(svg(study_edge(n, GRAY) + f'<circle cx="{x}" cy="{y}" r="{R_NODE}" fill="{PAPER}" stroke="{GRAY}" stroke-width="3"/>',
                          f"Study {n}" + (f", branching off established study {PARENT[n]}." if n in PARENT else ", a thrust out from the research question."),
                          f"fade {build}"))
        layers.append(text(n, "#4a4f5c", f"fade {build}"))
    for n, build in PROMOTE.items():
        x, y = NODES[n]
        layers.append(svg(study_edge(n, RED) + f'<circle cx="{x}" cy="{y}" r="{R_NODE}" fill="{RED}"/>' + tick(n),
                          f"Study {n} passes the promotion gate.", f"fade {build}"))
        layers.append(text(n, "#f6f4ef", f"fade {build}"))
    for n, build in FAIL.items():
        x, y = NODES[n]
        layers.append(svg(f'<circle cx="{x}" cy="{y}" r="{R_NODE}" fill="{DARK}"/>' + cross(n),
                          f"Study {n} fails the promotion gate.", f"fade {build}"))
        layers.append(text(n, "#f6f4ef", f"fade {build}"))
        layers.append(f'  <p data-build-in="fade {build}" style="position:absolute; top:{OY + y - 17}px; left:{OX + x + 40}px; '
                      f'width:230px; {SANS}; font-size:24px; font-weight:600; color:#1b1f2a">failed the gate</p>')
    layers.append(svg(f'<circle cx="{CENTER[0]}" cy="{CENTER[1]}" r="{R_CENTER}" fill="#1B1F2A"/>', "The research question at the centre."))
    layers.append(f'  <p style="position:absolute; top:{OY + CENTER[1] - 29}px; left:{OX + CENTER[0] - 62}px; width:124px; {SANS}; '
                  f'font-size:22px; line-height:1.3; text-align:center; color:#f6f4ef">Research<br>question</p>')
    layers.append(f'  <p data-build-in="fade 6" style="position:absolute; top:810px; left:128px; width:820px; {SANS}; '
                  f'font-size:24px; line-height:1.4; color:#6b6f7a">Inside each study: formulate, solve, learn.</p>')

    develop = card(DEVELOP_CARD, 300, "Develop", "develop-project", f'''    <p style="{SERIF}; font-size:32px; font-weight:600; color:#1b1f2a">The promotion gate</p>
    <p style="{SANS}; font-size:28px; line-height:1.4; color:#1b1f2a"><span style="color:#b04a33">1</span>  Independent audit</p>
    <p style="{SANS}; font-size:28px; line-height:1.4; color:#1b1f2a"><span style="color:#b04a33">2</span>  Integration: notation, tests, interfaces</p>
    <p style="{SANS}; font-size:28px; line-height:1.4; color:#1b1f2a"><span style="color:#b04a33">3</span>  Your approval</p>
    <p style="{SANS}; font-size:24px; line-height:1.4; color:#4a4f5c"><span style="color:#b04a33">✓ Pass:</span> joins the core.  <span style="color:#1b1f2a">✕ Fail:</span> stays outside, evidence kept.</p>''')
    audit = card(AUDIT_CARD, 705, "Audit", "review-paper",
                 f'    <p style="{SANS}; font-size:24px; line-height:1.4; color:#1b1f2a">A fresh reviewer gets the finished paper, not its history.</p>')

    html = f'''<section id="project" data-transition="fade" style="display:flex; flex-direction:column; gap:48px; padding:128px 128px 160px; background:#f6f4ef">
  <div style="display:flex; flex-direction:column; gap:16px">
    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#b04a33">06 · A whole project</p>
    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:#1b1f2a">Develop in isolation, then audit cold.</h2>
  </div>
{chr(10).join(layers)}
{develop}
{audit}
  <aside>{NOTES}</aside>
</section>
'''
    OUT.write_text(html)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

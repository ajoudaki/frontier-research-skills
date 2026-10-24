"""Generate talk/slides/slides/develop.html, the animated promotion-gate slide.

Build order: studies appear one by one with the first idea (isolation); the
promotion gate comes in (7); A, B, C are promoted one by one (edge and node
turn orange, a tick appears on the edge, and the established core grows to
enclose them); D, E, F fail one by one (cross on the edge); new studies branch
off the established A and B (14, 15); G is promoted and the core grows (16).
The three-idea panel on the right builds in step with the diagram.

Usage: python talk/slides/gen_project_slide.py
"""

import math
from pathlib import Path

from gen_skill_slides import tracker

OUT = Path(__file__).resolve().parent / "slides" / "develop.html"

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
GATE = 7  # the panel's second idea
PROMOTE = {"A": 8, "B": 9, "C": 10}
FAIL = {"D": 11, "E": 12, "F": 13}
BRANCH = {"G": 14, "H": 15}


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
    src, r_src = (NODES[PARENT[n]], R_NODE) if n in PARENT else (CENTER, R_CENTER)
    start, tip = endpoints(src, r_src, NODES[n])
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
    return (f'  <svg aria-label="{label}"{b} style="position:absolute; top:{OY}px; left:{OX}px; width:{W}px; height:{H}px; overflow:visible" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">{content}</svg>')


def text(n, color, build):
    x, y = NODES[n]
    return (f'  <p data-build-in="{build}" style="position:absolute; top:{OY + y - 17}px; left:{OX + x - 28}px; width:56px; '
            f'{SANS}; font-size:24px; font-weight:600; text-align:center; color:{color}">{n}</p>')


DEVELOP_NOTES = (
    "Here's the architecture. A project is one big open question, and develop-project rests on three ideas. "
    "From the research question, studies branch out, and the first idea is isolation: each study has its own question, "
    "inputs and folder, and by default it doesn't see the others' work. With your approval, one study can build on another. "
    "That way, an agent stuck on one failed idea can't drag the others into it, and you get the widest exploration. "
    "Inside each study, the agents formulate, solve and learn. "
    "The second idea is the promotion gate. A result enters the project's core only if it's correct, by an independent review; "
    "coherent, in notation, interfaces and tests; and relevant, which means your approval. "
    "These pass, and the core grows with each one. "
    "These fail and stay outside, with their evidence kept. So whatever is in the core is worth your time: "
    "that's the signal-to-noise ratio. "
    "The third idea: you build on the core. New studies can rely on promoted results, "
    "and they can be promoted in turn, so the core keeps growing. "
    "But each thrust is itself a research problem. Even a narrowed question is still open, and it leaves a lot of wiggle room. "
    "So inside a thrust, the first challenge is to formulate it."
)


def core_snapshot():
    """The diagram's final state, without letters or labels, in its own coordinates (for the audit slide)."""
    promote = {**PROMOTE, "G": 16}
    ring = hull([(CENTER, R_CENTER)] + [(NODES[m], R_NODE) for m in promote])
    out = [f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ring)}" fill="{CORE}" stroke="{RED}" stroke-width="5" stroke-linejoin="round"/>']
    for n in list(APPEAR) + list(BRANCH):
        x, y = NODES[n]
        color = RED if n in promote else DARK if n in FAIL else GRAY
        fill = PAPER if color == GRAY else color
        out.append(study_edge(n, RED if n in promote else GRAY) + f'<circle cx="{x}" cy="{y}" r="{R_NODE}" fill="{fill}" stroke="{color}" stroke-width="4"/>')
    out.append(f'<circle cx="{CENTER[0]}" cy="{CENTER[1]}" r="{R_CENTER}" fill="#1B1F2A"/>')
    return "".join(out)


def render(sid, eyebrow, title, chip, notes, promote, panel):
    layers = []
    # The core grows: one outline per promotion, each enclosing the last, under everything else.
    promoted = []
    core_ring = None
    label_ring = None
    for n, build in promote.items():
        promoted.append(n)
        core_ring = hull([(CENTER, R_CENTER)] + [(NODES[m], R_NODE) for m in promoted])
        if n == "C":
            label_ring = core_ring
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in core_ring)
        layers.append(svg(f'<polygon points="{path}" fill="{CORE}" stroke="{RED}" stroke-width="3" stroke-linejoin="round"/>',
                          f"The established core grows to include study {n}.", f"fade {build}"))
    bottom = max(y for _, y in label_ring)
    core_x = sum(x for x, _ in label_ring) / len(label_ring)
    layers.append(f'  <p data-build-in="fade {PROMOTE["C"]}" style="position:absolute; top:{OY + bottom + 6:.0f}px; '
                  f'left:{OX + core_x - 150:.0f}px; width:300px; {SANS}; font-size:24px; font-weight:600; letter-spacing:3px; '
                  f'text-align:center; text-transform:uppercase; color:{RED}">Established core</p>')

    for n, build in list(APPEAR.items()) + list(BRANCH.items()):
        x, y = NODES[n]
        layers.append(svg(study_edge(n, GRAY) + f'<circle cx="{x}" cy="{y}" r="{R_NODE}" fill="{PAPER}" stroke="{GRAY}" stroke-width="3"/>',
                          f"Study {n}" + (f", branching off established study {PARENT[n]}." if n in PARENT else ", a thrust out from the research question."),
                          f"fade {build}"))
        layers.append(text(n, "#4a4f5c", f"fade {build}"))
    for n, build in promote.items():
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

    html = f'''<section id="{sid}" data-transition="fade" style="display:flex; flex-direction:column; gap:48px; padding:128px 128px 160px; background:#f6f4ef">
  <div style="display:flex; flex-direction:column; gap:16px">
    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#b04a33">{eyebrow}</p>
    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:#1b1f2a">{title}</h2>
  </div>{chip_tag(chip)}
{chr(10).join(layers)}
{panel}
  <aside>{notes}</aside>
</section>
'''
    out = OUT.parent / f"{sid}.html"
    out.write_text(html)
    print(f"wrote {out}")


def chip_tag(chip):
    if not chip:
        return ""
    return (f'\n  <p style="position:absolute; top:120px; right:128px; padding:6px 20px; {MONO}; font-size:28px; '
            f'color:#b04a33; background:{CORE}; border-radius:8px">{chip}</p>')


def three_ideas():
    """The closer look: the three ideas, each line arriving with its step of the animation."""
    PX, PW = 1040, 752

    def ln(top, build, text, size=24, color="#1b1f2a", weight=400, family=SANS):
        return (f'  <p data-build-in="fade {build}" style="position:absolute; top:{top}px; left:{PX + 48}px; width:{PW - 88}px; '
                f'{family}; font-size:{size}px; font-weight:{weight}; line-height:1.4; color:{color}">{text}</p>')

    def head(top, build, num, text):
        return (f'  <p data-build-in="fade {build}" style="position:absolute; top:{top}px; left:{PX + 48}px; width:{PW - 88}px; '
                f'{SERIF}; font-size:32px; font-weight:600; color:#1b1f2a"><span style="color:#b04a33">{num}</span>  {text}</p>')

    rows = [
        f'  <div data-build-in="fade 1" style="position:absolute; top:300px; left:{PX}px; width:{PW}px; height:600px; background:#fdfcf9; border:1px solid #dcd6ca; border-radius:16px"></div>',
        head(330, 1, 1, "Isolated studies"),
        ln(380, 1, "Each thrust has its own question, inputs and folder; by default it doesn\u2019t see the others\u2019 work."),
        ln(448, 6, "→ the widest exploration", color="#b04a33", weight=600),
        head(518, 7, 2, "A promotion gate"),
        ln(568, 7, "<b>Correct:</b> an independent review"),
        ln(604, 7, "<b>Coherent:</b> notation, interfaces, tests"),
        ln(640, 7, "<b>Relevant:</b> your approval"),
        ln(688, 13, "→ only what passes enters: high signal-to-noise", color="#b04a33", weight=600),
        head(758, 14, 3, "Build on the core"),
        ln(808, 14, "New studies rely on promoted results,"),
        ln(842, 16, "and can be promoted in turn."),
    ]
    return "\n".join(rows)


def main():
    render("develop", tracker("Develop"), "Develop in isolation, build on what passes.", "develop-project", DEVELOP_NOTES,
           {**PROMOTE, "G": 16}, three_ideas())


if __name__ == "__main__":
    main()

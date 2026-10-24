"""Generate the skill slides: the overview, then one per skill, with step-by-step builds.

Writes talk/slides/slides/{overview,formulate,solve,teach,review}.html; the deck
order lives in talk/slides/deck.json.

Usage: python talk/slides/gen_skill_slides.py
"""

import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDES = HERE / "slides"

SANS = "font-family:'IBM Plex Sans', Arial, sans-serif"
MONO = "font-family:'IBM Plex Mono', 'Courier New', monospace"
SERIF = "font-family:'Source Serif 4', Georgia, serif"
RED, CORE, GRAY, DARK = "#B04A33", "#F3E3DC", "#A9A293", "#4A4F5C"
PAPER, INK, MUTED, BORDER, BG = "#FDFCF9", "#1B1F2A", "#6B6F7A", "#DCD6CA", "#F6F4EF"


# ---------- shared pieces ----------

def header(eyebrow, title, chip):
    return f'''  <div style="display:flex; flex-direction:column; gap:12px">
    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>
    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>
  </div>
  <p style="position:absolute; top:120px; right:128px; padding:6px 20px; {MONO}; font-size:28px; color:{RED}; background:{CORE}; border-radius:8px">{chip}</p>'''


def section(sid, body, notes):
    return f'''<section id="{sid}" data-transition="fade" style="display:flex; flex-direction:column; gap:32px; padding:128px 128px 160px; background:{BG}">
{body}
  <aside>{notes}</aside>
</section>
'''


def svg(left, top, w, h, content, label, build=None):
    b = f' data-build-in="{build}"' if build else ""
    return (f'  <svg aria-label="{label}"{b} style="position:absolute; top:{top}px; left:{left}px; width:{w}px; height:{h}px" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">{content}</svg>')


def p(left, top, width, text, size=24, color=INK, weight=400, align="left", build=None, extra="", family=SANS):
    b = f' data-build-in="{build}"' if build else ""
    return (f'  <p{b} style="position:absolute; top:{top}px; left:{left}px; width:{width}px; {family}; font-size:{size}px; '
            f'font-weight:{weight}; line-height:1.3; text-align:{align}; color:{color}{extra}">{text}</p>')


def arrow(x1, y1, x2, y2, color, width=3, dash=None):
    ux, uy = x2 - x1, y2 - y1
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    bx, by = x2 - ux * 14, y2 - uy * 14
    px, py = -uy, ux
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{width}"{d}/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {bx + px * 8:.1f},{by + py * 8:.1f} {bx - px * 8:.1f},{by - py * 8:.1f}" fill="{color}"/>')


def tick_badge(x, y, color=RED, r=15):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{color}" stroke-width="3"/>'
            f'<polyline points="{x - 7:.1f},{y:.1f} {x - 2:.1f},{y + 5:.1f} {x + 7:.1f},{y - 6:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')


def cross_badge(x, y, color=DARK, r=15):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{color}" stroke-width="3"/>'
            f'<line x1="{x - 6:.1f}" y1="{y - 6:.1f}" x2="{x + 6:.1f}" y2="{y + 6:.1f}" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<line x1="{x + 6:.1f}" y1="{y - 6:.1f}" x2="{x - 6:.1f}" y2="{y + 6:.1f}" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>')


def query_badge(x, y, r=15):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{GRAY}" stroke-width="3" stroke-dasharray="5 4"/>')


def box(left, top, width, inner, build=None, border=BORDER, bg=PAPER, pad=24, gap=8, dashed=False, height=None):
    b = f' data-build-in="{build}"' if build else ""
    style = "dashed" if dashed else "solid"
    h = f" height:{height}px;" if height else ""
    return (f'  <div{b} style="position:absolute; top:{top}px; left:{left}px; width:{width}px;{h} display:flex; flex-direction:column; '
            f'gap:{gap}px; padding:{pad}px; background:{bg}; border:2px {style} {border}; border-radius:14px">\n{inner}\n  </div>')


def line(text, size=24, color=INK, weight=400, family=SANS, extra=""):
    return f'    <p style="{family}; font-size:{size}px; font-weight:{weight}; line-height:1.3; color:{color}{extra}">{text}</p>'


def label(text, color=RED):
    return line(text, 22, color, 600, extra="; letter-spacing:3px; text-transform:uppercase")


STAGES = ("Organize", "Formulate", "Solve", "Learn", "Audit")
NUMBER = {"Organize": "05", "Formulate": "06", "Solve": "07", "Learn": "08", "Audit": "09"}
FAINT = "#B9B4A8"


def tracker(current):
    """The eyebrow: the slide number, then the five stages with the current one highlighted."""
    return f'<span style="color:{RED}">{NUMBER[current]}</span> · ' + " · ".join(
        f'<span style="color:{RED if s == current else FAINT}">{s}</span>' for s in STAGES)


def chips(*names):
    return "\n".join(f'  <p style="position:absolute; top:{120 + 60 * i}px; right:128px; padding:6px 20px; {MONO}; font-size:28px; '
                     f'color:{RED}; background:{CORE}; border-radius:8px">{n}</p>' for i, n in enumerate(names))


def transition(text, build, top=950):
    """The closing question at the bottom of a slide, which the next slide answers."""
    return p(128, top, 1664, text, 30, RED, 400, family=SERIF, build=f"fade {build}", extra="; font-style:italic")


def title_block(eyebrow, title):
    return (f'  <div style="display:flex; flex-direction:column; gap:12px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>\n  </div>')


# ---------- 04 · overview: the five skills, one block at a time ----------

def overview():
    L = [title_block("04 · Five skills", "Five skills: from open-ended question to paper.")]

    def card(left, top, stage, chip, desc, build):
        return (f'  <div data-build-in="rise {build}" style="position:absolute; top:{top}px; left:{left}px; width:406px; display:flex; '
                f'flex-direction:column; gap:10px; padding:24px; background:{PAPER}; border:1px solid {BORDER}; border-radius:16px">\n'
                f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">{stage}</p>\n'
                f'    <p style="padding:6px 16px; {MONO}; font-size:20px; white-space:nowrap; color:{RED}; background:{CORE}; border-radius:8px">{chip}</p>\n'
                f'    <p style="{SANS}; font-size:24px; line-height:1.4; color:{DARK}">{desc}</p>\n  </div>')

    def row_label(top, title, sub, build):
        return (f'  <div data-build-in="fade {build}" style="position:absolute; top:{top}px; left:128px; width:250px; display:flex; flex-direction:column; gap:4px">\n'
                f'    <h3 style="{SERIF}; font-size:32px; font-weight:600; color:{INK}">{title}</h3>\n'
                f'    <p style="{SANS}; font-size:24px; color:{MUTED}">{sub}</p>\n  </div>')

    def right_arrow(left, cy, build, length=48):
        return svg(left, cy - 14, length, 28, f'<polygon points="0,9 {length - 18},9 {length - 18},0 {length},14 {length - 18},28 {length - 18},19 0,19" fill="{RED}"/>',
                   "Arrow to the next stage.", f"fade {build}")

    R1, R2 = 297, 561
    L += [row_label(R1 + 52, "A whole project", "one big, open question", 1),
          card(398, R1, "Organize", "organize-research-project", "Many thrusts → one core", 1),
          p(398, 504, 900, "↓ every thrust runs these three", 24, MUTED, build="fade 2"),
          row_label(R2 + 52, "Each thrust", "one targeted question", 2),
          card(398, R2, "Formulate", "formulate-problem", "Open → precise question", 2),
          right_arrow(824, R2 + 91, 3), card(892, R2, "Solve", "solve-problem", "Question → checked proof", 3),
          right_arrow(1318, R2 + 91, 4), card(1386, R2, "Learn", "teach-material", "Result → understood", 4),
          right_arrow(824, R1 + 91, 5, 542), p(892, R1 + 40, 470, "the core becomes a paper", 24, MUTED, align="center", build="fade 5"),
          card(1386, R1, "Audit", "review-paper", "Paper → rigorous audit", 5),
          p(1386, 504, 406, "↺ findings start the next round", 24, MUTED, build="fade 5")]
    notes = ("So the strategy rests on those foundations, and it's implemented as five skills. Here they are at a glance, "
             "from an open-ended research question to a paper. "
             "organize-research-project is the main one: it organizes a whole project, one big open question, into many separate "
             "thrusts, and builds the established core. "
             "Inside each thrust, formulate-problem pins down its question, "
             "solve-problem solves it, with every step checked, "
             "and teach-material makes sure you understand the result. "
             "Finally, review-paper audits the part of the core that becomes a paper, and its findings can start the next round. "
             "Let's start with the main one.")
    return section("overview", "\n".join(L), notes)


# ---------- 06 · formulate-problem: rule out the easier questions, then freeze ----------

def formulate():
    L = [header(tracker("Formulate"), "Formulate the steelman, then freeze it.", "formulate-problem")]
    OX, OY, W, H = 128, 270, 1664, 660
    cx, cy, rx, ry = 832, 310, 380, 218
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        r = 1 + 0.08 * math.sin(5 * a) + 0.05 * math.sin(9 * a + 1)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    cloud = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    # the vague question (static)
    L.append(svg(OX, OY, W, H, f'<polygon points="{cloud}" fill="#EFEBE2" stroke="{GRAY}" stroke-width="3" stroke-dasharray="10 8"/>',
                 "A vague research question, drawn as a soft dashed cloud."))
    L.append(p(OX + cx - 200, OY + cy - 20, 400, "A vague question", 30, MUTED, 400, "center", family=SERIF, extra="; font-style:italic"))
    # step 6: the vague boundary fades into the background, still visible
    L.append(svg(OX, OY, W, H, f'<polygon points="{cloud}" fill="{BG}" opacity="0.7"/>', "The vague boundary fades into the background.", "fade 6"))
    # each contract field rules out one easier question: a point on the vague edge, labelled where it sits
    rows = [("Question", "rules out an easier target", 195, "left"),
            ("Definitions", "rules out a drifting definition", 245, "left"),
            ("Quantifiers", "rules out ‘for all’ weakened to ‘there exists’", 300, "right"),
            ("Evidence standard", "rules out a proxy metric", 10, "right"),
            ("Scope", "rules out one example for a whole class", 125, "below")]
    dots = []
    for i, (field, rule, deg, side) in enumerate(rows):
        k = i + 1
        a = math.radians(deg)
        dx, dy = cx + 0.98 * rx * math.cos(a), cy + 0.98 * ry * math.sin(a)
        dots.append((dx, dy))
        L.append(svg(OX, OY, W, H, f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="14" fill="{DARK}"/>',
                     f"{field}: an answer to an easier question sits on the vague edge.", f"pop {k}"))
        lw = 480
        left, top, align = {"right": (OX + dx + 34, OY + dy - 34, "left"),
                            "left": (OX + dx - 34 - lw, OY + dy - 34, "right"),
                            "above": (OX + dx - lw / 2, OY + dy - 100, "center"),
                            "below": (OX + dx - lw / 2, OY + dy + 26, "center")}[side]
        L.append(p(left, top, lw, field, 28, INK, 600, align, build=f"fade {k}"))
        L.append(p(left, top + 38, lw, rule, 22, MUTED, 400, align, build=f"fade {k}"))
    # step 6: the sharp boundary emerges; every point lies outside it
    sx0, sy0, sx1, sy1 = cx - 240, cy - 118, cx + 240, cy + 118
    crosses = "".join(cross_badge(dx, dy, RED, 16) for dx, dy in dots)
    L.append(svg(OX, OY, W, H, f'<rect x="{sx0}" y="{sy0}" width="{sx1 - sx0}" height="{sy1 - sy0}" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>' + crosses,
                 "The sharp conjecture: a crisp boundary, with every point outside it.", "fade 6"))
    L.append(p(OX + sx0 + 20, OY + sy0 + 44, sx1 - sx0 - 40, "For every <i>x</i> in <i>D</i><br>with <i>H</i>(<i>x</i>), <i>C</i>(<i>x</i>) holds.",
               32, INK, 400, "center", build="fade 6", family=SERIF))
    L.append(p(OX + sx0 + 20, OY + sy0 + 170, sx1 - sx0 - 40, "the sharp conjecture", 20, MUTED, 600, "center", build="fade 6",
               extra="; letter-spacing:3px; text-transform:uppercase"))
    # step 7: frozen
    L.append(p(OX + sx1 - 140, OY + sy0 - 30, 200, "Frozen", 30, RED, 600, "center", build="pop 7",
               extra=f"; letter-spacing:4px; text-transform:uppercase; border:4px solid {RED}; border-radius:10px; background:{PAPER}; transform:rotate(-8deg)"))
    L.append(p(OX + cx - 400, OY + cy + ry + 100, 800, "Frozen: a material change needs your say.", 26, RED, 600, "center", build="fade 7"))
    L.append(transition("The question is pinned down. But how do we solve it?", 8))
    notes = ("Take one thrust. Even a narrowed question is still open, and usually vague, like this cloud. "
             "The danger is that a vague question leaves room for answers to an easier question, and an agent will happily take them. "
             "The goal is the steelman, not the straw man: the strongest version that stays faithful to what you meant. "
             "So formulate-problem writes a research contract, and each field rules something out. "
             "The question itself is pinned down, so an easier target doesn't count. "
             "The definitions are fixed, so they can't drift halfway through. "
             "The quantifiers keep their order, so 'for all' can't quietly become 'there exists'. "
             "The evidence standard says what counts, so a proxy metric doesn't. "
             "And the scope is explicit, so one example can't stand in for a whole class. "
             "Notice that the vague boundary couldn't tell us whether any of these were in or out. "
             "Once they're ruled out, the sharp boundary emerges: one precise conjecture. "
             "Then it's frozen. A material change needs your say, and results for a changed question never count as answers to the original. "
             "Now the question is pinned down, with no wiggle room. But we still have to solve it, and that's the next hard push.")
    return section("formulate", "\n".join(L), notes)


# ---------- 07 · solve: many independent routes, one audited proof ----------

def solve():
    L = [header(tracker("Solve"), "Solve by many routes, then audit the proof.", "solve-problem")]
    lanes = [400, 510, 620, 730]
    mid = sum(lanes) / 4
    # the frozen contract (static)
    L.append(box(128, int(mid - 58), 220, line("∀ <i>x</i> ∈ <i>D</i>:  <i>C</i>(<i>x</i>)", 28, INK, family=SERIF) + "\n" +
                 line("frozen contract", 18, RED, 600, extra="; letter-spacing:2px; text-transform:uppercase"), border=INK, pad=18))
    # step 1: parallel routes, one agent each, different mechanisms
    names = ["Route 1 · duality", "Route 2 · induction", "Route 3 · induction, renamed", "Route 4 · extremal"]
    fan = "".join(arrow(4, mid - 340, 70, y - 340, GRAY, 2) for y in lanes)
    L.append(svg(348, 340, 80, 460, fan, "The same contract goes to every route.", "fade 1"))
    for y, n in zip(lanes, names):
        L.append(box(420, y - 32, 340, line(n, 22, INK, 600), build="fade 1", pad=16, height=64))
    L.append(p(420, 320, 640, "parallel agents, one route each, same contract", 22, MUTED, 400, build="fade 1"))
    # step 2: the registry after a round: a duplicate is merged, a stalled route is blocked
    L.append(svg(420, lanes[1] + 32, 340, 120, f'<rect x="0" y="46" width="340" height="64" rx="14" fill="{BG}" opacity="0.7"/>'
                 + arrow(170, 44, 170, 2, DARK, 3), "Route 3 is merged into route 2: same mechanism.", "fade 2"))
    L.append(p(780, lanes[2] - 16, 300, "merged: same mechanism", 22, DARK, 600, build="fade 2"))
    L.append(svg(420, lanes[3] - 32, 340, 64, f'<rect x="0" y="0" width="340" height="64" rx="14" fill="{BG}" opacity="0.7"/>',
                 "Route 4 fades: blocked.", "fade 2"))
    L.append(svg(770, lanes[3] - 20, 40, 40, cross_badge(20, 20, DARK, 15), "Route 4 is blocked.", "fade 2"))
    L.append(p(820, lanes[3] - 28, 250, "blocked: its missing lemma is as hard as the theorem", 20, DARK, 600, build="fade 2"))
    # step 3: route 1 supplies a lemma; route 2 becomes a candidate proof
    L.append(svg(570, lanes[0] + 32, 40, lanes[1] - lanes[0] - 64, arrow(20, 2, 20, lanes[1] - lanes[0] - 66, RED, 3),
                 "Route 1 supplies a missing lemma to route 2.", "fade 3"))
    L.append(p(780, lanes[0] - 16, 280, "supplies a missing lemma", 22, RED, 600, build="fade 3"))
    L.append(svg(760, lanes[1] - 20, 70, 40, arrow(2, 20, 66, 20, RED, 3), "Route 2 completes.", "fade 3"))
    L.append(box(830, lanes[1] - 32, 200, line("candidate proof", 22, INK, 600, extra="; text-align:center"), build="fade 3",
                 border=RED, bg=CORE, pad=16, height=64))
    # step 4: independent audit, separate checks
    AX, AW = 1090, 702
    checks = ["Rebuild every implication from the contract", "Check each cited theorem and its hypotheses",
              "Hunt counterexamples: boundary, degenerate cases"]
    L.append(svg(1030, lanes[1] - 20, 62, 40, arrow(2, 20, 58, 20, RED, 3), "The candidate goes to independent audit.", "fade 4"))
    L.append(box(AX, 320, AW, label("Independent audit · separate checks", DARK), build="fade 4", height=260))
    for i, c in enumerate(checks):
        y = 384 + i * 62
        L.append(svg(AX + 24, y, 40, 40, tick_badge(20, 20, RED, 16), f"Check passed: {c}.", "fade 4"))
        L.append(p(AX + 80, y + 4, AW - 110, c, 24, INK, 400, build="fade 4"))
    # step 5: the proof, written by solve-problem
    props = ["The plan first, then every nontrivial step", "No “clearly” in place of a reason",
             "Answers exactly the question in the contract"]
    L.append(box(AX, 610, AW, f'    <div style="display:flex; flex-direction:row; gap:16px; align-items:center">'
                 f'<p style="{SANS}; font-size:22px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">The written proof</p>'
                 f'<p style="padding:4px 14px; {MONO}; font-size:22px; color:{RED}; background:{CORE}; border-radius:8px">solve-problem</p></div>',
                 build="rise 5", border=RED, height=236))
    for i, c in enumerate(props):
        L.append(p(AX + 34, 680 + i * 50, AW - 60, "· " + c, 24, INK, 400, build="rise 5"))
    L.append(p(128, 830, 920, f'The search and its audit: <span style="{MONO}; color:{RED}">formulate-problem</span>. '
               f'The written proof: <span style="{MONO}; color:{RED}">solve-problem</span>.', 22, MUTED, 400, build="fade 5"))
    L.append(transition("Solved, most likely. But to judge it, we still have to understand it.", 6))
    notes = ("Solving is the second hard push, and it starts from the frozen contract. "
             "With your go-ahead, the proof search runs as parallel agents, one per route, and each route uses a genuinely different mechanism: "
             "duality, induction, an extremal argument. They all get the same contract, and none is told which strategy to favor, so they stay independent. "
             "After every round, a registry keeps score. Two routes that turn out to use the same idea are merged. "
             "A route that needs a lemma as hard as the theorem itself is marked blocked, but its valid lemmas are kept. "
             "Mature routes can borrow from each other: here duality supplies the missing lemma, and induction becomes a candidate proof. "
             "But a candidate isn't a proof yet. Separate checks rebuild every implication from the contract, check each cited theorem and its hypotheses, "
             "and hunt for counterexamples at the boundary and in degenerate cases. "
             "Only what survives gets written up by solve-problem: the plan first, every nontrivial step derived, no 'clearly' in place of a reason, "
             "and an answer to exactly the question in the contract. "
             "So now the thrust has a written proof that's most likely correct. We've delegated as much as we could, "
             "but we still have to stay in charge: someone has to judge whether it's relevant, whether it's the right direction, "
             "and whether an assumption or technique was quietly tweaked along the way. That means reading it, and agent output "
             "can be very hard to read. That's the third stage.")
    return section("solve", "\n".join(L), notes)


# ---------- 08 · learn: the idea first, then every step ----------

def teach():
    L = [title_block(tracker("Learn"), "Learn the idea first, then every step."), chips("teach-material", "explain-canonically")]
    LX, BX, BW = 128, 468, 1324
    rows = [(300, "The paper", None), (416, "Canonical notation", 1), (572, "The idea", 2),
            (706, "A toy example", 3), (810, "Theorems, checked", 4)]
    for top, name, build in rows:
        L.append(p(LX, top + 22, 290, name, 26, INK if build else MUTED, 600, build=f"fade {build}" if build else None, family=SERIF))
    # the paper's line, in private notation (static)
    L.append(box(BX, 300, BW, line("𝔘<sub>k+1</sub> = 𝔘<sub>k</sub> − η 𝔇(𝔘<sub>k</sub>),   𝔇 := ∂𝔏/∂𝔘,   ‖𝔇(𝔘) − 𝔇(𝔙)‖ ≤ β‖𝔘 − 𝔙‖   ⟹   𝔏(𝔘<sub>k</sub>) ↓",
                                    30, MUTED, family=SERIF), dashed=True, border=GRAY, bg="#EFEBE2", pad=22))
    # 1. canonical notation: a few global symbols, each typed
    L.append(box(BX, 416, BW, line("θ<sub>k+1</sub> = θ<sub>k</sub> − η ∇L(θ<sub>k</sub>)", 34, INK, family=SERIF) + "\n" +
                 line("𝔘 → θ ∈ ℝ<sup>d</sup>, the parameters  ·  𝔏 → L : ℝ<sup>d</sup> → ℝ, the loss  ·  𝔇 → ∇L, its gradient  ·  η > 0, the step size", 22, MUTED),
                 build="rise 1", pad=20, gap=6))
    # 2. the idea, which is also the plan of the proof
    L.append(box(BX, 572, BW, line("Each step goes downhill; if the slope can’t change too fast, each step lowers L by a definite amount.", 26, INK, family=SERIF) + "\n" +
                 line("plan:  a drop per step  →  add up the drops", 22, RED, 600), build="rise 2", pad=20, gap=6))
    # 3. a toy example that keeps the structure
    L.append(box(BX, 706, BW, line("L(θ) = θ²/2 in one dimension:  θ<sub>k+1</sub> = (1 − η) θ<sub>k</sub>,  so θ<sub>k</sub> → 0 exactly when 0 < η < 2.",
                                    26, INK, family=SERIF), build="rise 3", pad=20))
    dots = "".join(f'<circle cx="{40 + 230 * (0.6 ** k):.1f}" cy="20" r="{9 - k}" fill="{RED}" opacity="{1 - 0.12 * k:.2f}"/>' for k in range(6))
    L.append(svg(BX + BW - 320, 720, 300, 40, f'<line x1="30" y1="20" x2="290" y2="20" stroke="{BORDER}" stroke-width="2"/>'
                 f'<line x1="40" y1="6" x2="40" y2="34" stroke="{INK}" stroke-width="2"/>' + dots, "Iterates shrinking toward zero.", "fade 3"))
    # 4. the invoked theorem, stated and checked where it is used
    L.append(box(BX, 810, BW, line("Descent lemma: if ∇L is β-Lipschitz, then L(θ − η∇L(θ)) ≤ L(θ) − η(1 − βη/2)‖∇L(θ)‖².", 26, INK, family=SERIF) + "\n" +
                 line("hypothesis: ∇L is β-Lipschitz, given in the paper ✓  ·  here, with η ≤ 1/β, each step lowers L by at least (η/2)‖∇L(θ<sub>k</sub>)‖²", 22, RED, 600),
                 build="rise 4", pad=20, gap=6))
    # zoom: from the idea down to the details
    L.append(svg(BX - 40, 572, 30, 354, arrow(15, 6, 15, 348, RED, 3), "From the high-level idea down to the details.", "fade 4"))
    L.append(transition("Now we can judge what joins the core.", 5))
    notes = ("A correct proof you don't understand isn't worth much. "
             "Here's the kind of line an agent, or a paper, might hand you: private symbols everywhere. "
             "teach-material, together with explain-canonically, teaches it in layers. "
             "First, notation. It translates into the symbols the field already uses: the parameters theta, the loss L, its gradient. "
             "Only a few global symbols, each defined with its type before it's used. "
             "Then the idea, before any detail: every step goes downhill, and if the slope can't change too fast, each step lowers the loss by a definite amount. "
             "That's also the plan of the proof. "
             "Then a toy example that keeps the real structure: a one-dimensional quadratic, where you can see exactly when the iterates shrink to zero. "
             "And only then the details. When the argument invokes a theorem, it's stated right there, in the exact form needed, "
             "with its hypothesis checked and its conclusion spelled out for our objects. "
             "And if you're confused at any point, it rewrites the whole block rather than patching a sentence. "
             "Once you understand it, you can judge whether it joins the core. And that completes the loop for one thrust.")
    return section("teach", "\n".join(L), notes)


# ---------- 09 · review-paper: back to the core, then a ledger of claims ----------

def review():
    L = [header(tracker("Audit"), "Audit every claim against its evidence.", "review-paper")]
    # the paper page
    PX, PY, PW, PH = 128, 330, 250, 330
    lines = "".join(f'<line x1="24" y1="{40 + 22 * k}" x2="{226 - (k % 3) * 30}" y2="{40 + 22 * k}" stroke="#D6D0C3" stroke-width="6" stroke-linecap="round"/>' for k in range(13))
    L.append(svg(PX, PY, PW, PH, f'<rect x="2" y="2" width="{PW - 4}" height="{PH - 4}" rx="8" fill="{PAPER}" stroke="{BORDER}" stroke-width="2"/>' + lines,
                 "The submitted paper."))
    L.append(p(PX, PY + PH + 12, PW, "the paper, read in full", 22, MUTED, 400, "center"))
    marks = (1, 4, 7, 10)
    hl = "".join(f'<rect x="20" y="{40 + 22 * k - 8}" width="210" height="16" rx="4" fill="{RED}" opacity="0.35"/>' for k in marks)
    L.append(svg(PX, PY, PW, PH, hl, "Four key claims highlighted in the paper.", "fade 1"))
    # ledger rows: (claim, plausibility, plausibility colour, soundness note, note colour)
    claims = [("C1 · key lemma", "plausible", RED, "flawed proof", DARK),
              ("C2 · main theorem", "plausible", RED, "depends on C1", MUTED),
              ("C3 · novelty", "questionable", DARK, "unverified source", MUTED),
              ("C4 · beats baselines", "questionable", DARK, "unfair baselines", DARK)]
    RX, RY, RW, RH, RG = 490, 330, 540, 84, 22
    rows_y = [RY + i * (RH + RG) for i in range(4)]
    for (c, *_), y in zip(claims, rows_y):
        L.append(box(RX, y, RW, line(c, 26, INK, 600), build="rise 1", pad=22, height=RH))
    L.append(svg(PX, PY, 330, 460, "".join(arrow(232, 40 + 22 * k, RX - 62 - PX - 6, rows_y[i] - PY + RH / 2, RED, 2, "5 5") for i, k in enumerate(marks)),
                 "Claims lifted from the paper into the ledger.", "fade 1"))
    # evidence sources, ordered so that no two evidence lines cross
    EX = 1290
    sources = [("Proofs", "re-derived step by step", 330), ("Cited papers", "retrieved and checked", 500), ("Code", "audited as untrusted", 670)]
    # (claim, source, verdict, step)
    edges = [(0, 0, "cross", 2), (1, 1, "tick", 3), (2, 1, "query", 3), (3, 2, "cross", 4)]
    first_step = {0: 2, 1: 3, 2: 4}
    for k, (name, sub, y) in enumerate(sources):
        L.append(box(EX, y, 502, line(name, 26, INK, 600) + "\n" + line(sub, 22, MUTED), build=f"fade {first_step[k]}", pad=18, height=110))
    EOX, EOY = RX + RW, 300
    for ci, si, kind, step in edges:
        x1, y1 = 6, rows_y[ci] + RH / 2 - EOY
        x2, y2 = EX - EOX - 6, sources[si][2] + 55 - EOY
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        badge = {"tick": tick_badge(mx, my, RED), "cross": cross_badge(mx, my, DARK), "query": query_badge(mx, my)}[kind]
        col = {"tick": RED, "cross": DARK, "query": GRAY}[kind]
        L.append(svg(EOX, EOY, EX - EOX, 520, arrow(x1, y1, x2, y2, col, 2) + badge, f"Evidence for claim C{ci + 1}: {kind}.", f"fade {step}"))
    L.append(p(EX, 792, 502, "✓ valid   ✕ flawed   ◌ unverifiable", 22, MUTED, 400, build="fade 2"))
    # plausibility of the conclusion, separate from soundness of the argument
    for (_, pl, c1, so, c2), y in zip(claims, rows_y):
        L.append(p(RX + 320, y + 10, 190, pl, 18, PAPER, 600, "center", build="fade 5",
                   extra=f"; padding:4px 0; border-radius:16px; background:{c1}; letter-spacing:1px; text-transform:uppercase"))
        L.append(p(RX + 320, y + 46, 210, so, 18, c2, 600, "center", build="fade 5", extra="; letter-spacing:1px; text-transform:uppercase"))
    L.append(p(RX, rows_y[-1] + RH + 14, 820, "Plausibility of the conclusion ≠ soundness of the argument.", 22, MUTED, 400, build="fade 5"))
    # severity tags
    for tag, ci, col in (("F1", 0, RED), ("L1", 2, MUTED), ("M1", 3, DARK)):
        L.append(p(RX - 62, rows_y[ci] + 22, 56, tag, 22, PAPER, 600, "center", build="pop 6",
                   extra=f"; padding:4px 0; border-radius:8px; background:{col}"))
    # cascade: C1's fatal flaw reaches the main theorem
    gap = rows_y[1] - rows_y[0]
    L.append(svg(RX - 100, rows_y[0] + 30, 40, gap + 10,
                 f'<path d="M 34 4 C 4 14, 4 {gap - 14}, 28 {gap - 2}" fill="none" stroke="{RED}" stroke-width="3"/>'
                 f'<polygon points="34,{gap} 20,{gap - 4} 28,{gap - 14}" fill="{RED}"/>',
                 "The fatal flaw in C1 cascades to the main theorem C2.", "fade 7"))
    L.append(p(RX - 62, rows_y[1] + 22, 56, "F1", 22, PAPER, 600, "center", build="pop 7",
               extra="; padding:4px 0; border-radius:8px; background:#CF9182"))
    # verdict and confidence
    meter = (f'<rect x="0" y="0" width="502" height="18" rx="9" fill="#E6E1D6"/>'
             f'<rect x="0" y="0" width="330" height="18" rx="9" fill="{RED}"/>')
    L.append(box(128, 830, 902, line("Verdict: central message <b>unsupported</b> until C1 is repaired", 28, INK, 400, family=SERIF), build="rise 8", border=INK, pad=20))
    L.append(svg(EX, 860, 502, 18, meter, "Confidence meter, lowered by one unverifiable source.", "fade 8"))
    L.append(p(EX, 886, 502, "confidence: lowered for what couldn't be checked", 22, MUTED, 400, build="fade 8"))
    notes = ("So now we know how to run organize-research-project: we make the thrusts, formulate them, solve them, understand "
             "them, and promote what's true and relevant into the established core. But is that a scientific result? Not yet. "
             "Some results matter more than others, and a paper is judged on more than truth: novelty, significance, the literature. "
             "So we carve out the high-value part, and that needs a different kind of audit. "
             "review-paper reads the full submission, code included. "
             "It lifts out the three to five claims that matter most, into a ledger. "
             "Then it checks each one against its evidence. It re-derives the key proofs: here, the key lemma's proof fails. "
             "It retrieves the cited papers and checks that each citation is used correctly: one holds, and one source can't be verified. "
             "It audits the code: these baselines are unfair. "
             "It rates how plausible each conclusion is separately from how sound its argument is. "
             "Each flaw gets a severity: fatal, major or minor. "
             "And a fatal flaw cascades to every claim that depends on it: the main theorem falls with the lemma. "
             "The verdict says whether the central message stands, and the confidence reflects only what was actually checked. "
             "And its findings can start the next round of the project. Now let's put it all together.")
    # step 0 is a reminder of the project's established core; the paper replaces it at step 1
    L = [re.sub(r'data-build-in="(\w+) (\d+)"', lambda m: f'data-build-in="{m[1]} {int(m[2]) + 1}"', el) for el in L]
    from gen_project_slide import core_snapshot
    s = 1.1
    SX, SY = 960 - 350 * s, 330
    L.insert(1, svg(SX, SY, 700 * s, 490 * s, f'<g transform="translate(0,{10 * s}) scale({s})">{core_snapshot()}</g>',
                    "The project's established core, as built on the organize slide."))
    L.insert(2, p(SX, SY + 490 * s + 16, 700 * s, "the established core", 28, RED, 600, "center", extra="; letter-spacing:3px; text-transform:uppercase"))
    L.insert(3, transition("We can now build a core that's true and relevant. But a paper needs more: novelty, significance, the literature.", 0).replace(' data-build-in="fade 0"', ""))
    L.insert(4, f'  <div data-build-in="fade 1" style="position:absolute; top:290px; left:0; width:1920px; height:790px; background:{BG}"></div>')
    L.append(transition("Now let's put it all together.", 10))
    i = next(k for k, el in enumerate(L) if "The submitted paper." in el)
    L[i] = L[i].replace('aria-label="The submitted paper."', 'aria-label="The submitted paper." data-build-in="fade 1"')
    i = next(k for k, el in enumerate(L) if "the paper, read in full" in el)
    L[i] = L[i].replace("<p style=", '<p data-build-in="fade 1" style=').replace(f"color:{MUTED}\"", f"color:{MUTED}; background:{BG}\"")
    return section("review", "\n".join(L), notes)


def main():
    for sid, make in (("overview", overview), ("formulate", formulate), ("solve", solve), ("teach", teach), ("review", review)):
        (SLIDES / f"{sid}.html").write_text(make())
        print(f"wrote {sid}.html")


if __name__ == "__main__":
    main()

"""Generate the four 'closer look' slides, one per skill, with step-by-step builds.

Writes talk/slides/slides/{formulate,solve,teach,review}.html and appends
their ids to talk/slides/deck.json if missing.

Usage: python talk/slides/gen_skill_slides.py
"""

import json
import math
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
  <p style="position:absolute; top:136px; right:128px; padding:6px 20px; {MONO}; font-size:28px; color:{RED}; background:{CORE}; border-radius:8px">{chip}</p>'''


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


# ---------- 1. formulate-problem: seal the loopholes ----------

def formulate():
    L = [header("A closer look · Formulate", "Seal the loopholes first.", "formulate-problem")]
    # diagram box on the slide
    OX, OY, W, H = 128, 330, 900, 600
    cx, cy = 470, 300
    # vague cloud (static)
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        r = 1 + 0.10 * math.sin(5 * a) + 0.06 * math.sin(9 * a + 1)
        pts.append((cx + 215 * r * math.cos(a), cy + 105 * r * math.sin(a)))
    cloud = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    L.append(svg(OX, OY, W, H, f'<polygon points="{cloud}" fill="#EFEBE2" stroke="{GRAY}" stroke-width="3" stroke-dasharray="10 8"/>',
                 "A vague research question, drawn as a soft dashed cloud."))
    L.append(p(OX + cx - 200, OY + cy - 20, 400, "A vague question", 30, MUTED, 400, "center", family=SERIF,
               extra="; font-style:italic"))
    # contract card on the right (fields build in one by one)
    fields = ["Objects and definitions", "Admissible domain", "Quantifier order: ∀ before ∃",
              "Conclusion and scope", "Evidence standard", "Forbidden substitutions"]
    CX, CY = 1110, 330
    L.append(box(CX, CY, 682, label("The research contract"), build="fade 1", height=470))
    for i, f in enumerate(fields):
        y = CY + 84 + i * 62
        L.append(svg(CX + 24, y + 2, 32, 32, tick_badge(16, 16, RED, 13), f"Contract field: {f}.", f"fade {i + 1}"))
        L.append(p(CX + 70, y, 580, f, 28, INK, 400, build=f"fade {i + 1}"))
    # sharp conjecture over the cloud
    sx0, sy0, sx1, sy1 = cx - 260, cy - 125, cx + 260, cy + 125
    L.append(svg(OX, OY, W, H, f'<rect x="{sx0}" y="{sy0}" width="{sx1 - sx0}" height="{sy1 - sy0}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>',
                 "The sharp conjecture: a crisp box replacing the cloud.", "fade 7"))
    L.append(p(OX + sx0 + 40, OY + sy0 + 50, 440, "For every <i>x</i> in <i>D</i> with <i>H</i>(<i>x</i>),<br><i>C</i>(<i>x</i>) holds.",
               34, INK, 400, "center", build="fade 7", family=SERIF))
    L.append(p(OX + sx0 + 40, OY + sy0 + 160, 440, "the sharp conjecture", 22, MUTED, 600, "center", build="fade 7",
               extra="; letter-spacing:3px; text-transform:uppercase"))
    # cheats bouncing off: (label, start, end on the box, label position)
    cheats = [
        ("an easier target", (40, 40), (sx0 + 60, sy0), (0, 0)),
        ("definition drift", (20, 300), (sx0, cy), (0, 252)),
        ("∀ weakened to ∃", (40, 560), (sx0 + 60, sy1), (0, 568)),
        ("a proxy metric", (880, 560), (sx1 - 60, sy1), (650, 568)),
        ("one example for a class", (880, 40), (sx1 - 60, sy0), (590, 0)),
    ]
    for i, (name, (x1, y1), (x2, y2), (lx, ly)) in enumerate(cheats):
        build = f"fade {8 + i}"
        ux, uy = x2 - x1, y2 - y1
        n = math.hypot(ux, uy)
        hx, hy = x2 - ux / n * 22, y2 - uy / n * 22
        L.append(svg(OX, OY, W, H, arrow(x1, y1, hx, hy, DARK, 3, "8 6") + cross_badge(hx, hy, RED, 16),
                     f"A cheat, {name}, blocked at the contract.", build))
        L.append(p(OX + lx, OY + ly, 280, name, 24, DARK, 600, "left", build=build))
    # frozen stamp
    L.append(p(OX + sx1 - 150, OY + sy0 - 34, 210, "Frozen", 30, RED, 600, "center", build="pop 13",
               extra=f"; letter-spacing:4px; text-transform:uppercase; border:4px solid {RED}; border-radius:10px; background:{PAPER}; transform:rotate(-8deg)"))
    L.append(p(1110, 830, 682, "Every cheat it finds is closed before any attempt to solve.", 26, MUTED, 400, build="fade 13"))
    notes = ("First, formulate-problem. A research question usually starts vague. "
             "Before anyone tries to solve it, the skill writes a research contract: the objects and definitions, the admissible domain, "
             "the order of the quantifiers, the conclusion and its scope, what counts as evidence, and which substitutions are forbidden. "
             "Only then does it state a sharp conjecture. And then it attacks its own statement, looking for the ways an agent could cheat: "
             "an easier target, a definition that drifts, a 'for all' quietly weakened to 'there exists', a proxy metric, or one example "
             "passed off as a whole class. Every loophole it finds gets closed, and the result is frozen as a contract, so no later step "
             "can quietly change the question.")
    return section("formulate", "\n".join(L), notes)


# ---------- 2. solve-problem: an audited chain ----------

def solve():
    L = [header("A closer look · Solve", "Every step, checked.", "solve-problem")]
    OX, OY, W, H = 128, 330, 1664, 610
    mid = 300
    # contract (frozen) on the left, empty conclusion on the right
    L.append(box(OX, OY + mid - 55, 250, line("∀ <i>x</i> ∈ <i>D</i>:  <i>C</i>(<i>x</i>)", 28, INK, family=SERIF) + "\n" +
                 line("frozen contract", 20, RED, 600, extra="; letter-spacing:2px; text-transform:uppercase"),
                 border=INK, pad=20))
    L.append(box(OX + 1414, OY + mid - 55, 250, line("Conclusion", 26, MUTED, family=SERIF) + "\n" +
                 line("to be shown", 20, MUTED, 600, extra="; letter-spacing:2px; text-transform:uppercase"), dashed=True, border=GRAY, pad=20))
    # 1. strongest reading
    L.append(svg(OX, OY + mid + 92, 260, 120,
                 cross_badge(20, 30, DARK, 14) + tick_badge(20, 88, RED, 14), "Two readings: the straw man is rejected, the strongest kept.", "fade 1"))
    L.append(p(OX + 44, OY + mid + 106, 220, "a straw-man reading", 22, MUTED, 400, build="fade 1", extra="; text-decoration:line-through"))
    L.append(p(OX + 44, OY + mid + 164, 220, "the strongest reading", 22, INK, 600, build="fade 1"))
    # 2. proof plan: three lemma boxes and arrows
    xs = [390, 720, 1050]
    names = ["Lemma 1", "Lemma 2", "Lemma 3"]
    arrows = arrow(250, mid, xs[0] - 8, mid, GRAY) + "".join(arrow(x + 250, mid, x + 330 - 8, mid, GRAY) for x in xs[:2]) + arrow(xs[2] + 250, mid, 1414 - 8, mid, GRAY)
    plan = arrows + "".join(f'<rect x="{x}" y="{mid - 60}" width="250" height="120" rx="12" fill="{PAPER}" stroke="{GRAY}" stroke-width="3" stroke-dasharray="9 7"/>' for x in xs)
    L.append(svg(OX, OY, W, H, plan, "The proof plan: three lemmas leading to the conclusion.", "fade 2"))
    for x, n in zip(xs, names):
        L.append(p(OX + x, OY + mid - 20, 250, n, 28, MUTED, 600, "center", build="fade 2", family=SERIF))
    L.append(p(OX + 390, OY + mid - 104, 300, "The plan comes first.", 24, MUTED, 400, build="fade 2"))

    def filled(x, color=RED):
        return f'<rect x="{x}" y="{mid - 60}" width="250" height="120" rx="12" fill="{CORE}" stroke="{color}" stroke-width="3"/>'

    def steps_drawn(x):
        return "".join(f'<line x1="{x + 30}" y1="{mid - 4 + 18 * k}" x2="{x + 220 - 30 * (k % 2)}" y2="{mid - 4 + 18 * k}" stroke="{RED}" stroke-width="4" stroke-linecap="round" opacity="0.55"/>' for k in range(3))

    # 3. lemma 1 derived
    L.append(svg(OX, OY, W, H, filled(xs[0]) + steps_drawn(xs[0]) + tick_badge(xs[0] + 250, mid - 60), "Lemma 1 derived, every step shown.", "fade 3"))
    L.append(p(OX + xs[0], OY + mid - 46, 250, "Lemma 1", 28, INK, 600, "center", build="fade 3", family=SERIF))
    # 4. cited theorem with hypothesis sockets
    tx, ty = xs[1] - 10, 30
    sockets = "".join(f'<circle cx="{tx + 60 + 70 * k}" cy="{ty + 92}" r="16" fill="{PAPER}" stroke="{GRAY}" stroke-width="3" stroke-dasharray="5 4"/>' for k in range(3))
    L.append(svg(OX, OY, W, H, f'<rect x="{tx}" y="{ty}" width="270" height="130" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>' + sockets
                 + arrow(tx + 135, ty + 130, tx + 135, mid - 62, INK, 2, "6 5"), "A cited theorem with three hypotheses still to check.", "fade 4"))
    L.append(p(OX + tx + 16, OY + ty + 14, 240, "Cited theorem", 24, INK, 600, build="fade 4"))
    L.append(p(OX + tx + 290, OY + ty + 40, 330, "hypotheses h1, h2, h3:<br>checked one by one", 22, MUTED, 400, build="fade 4"))
    # 5. hypotheses checked, lemma 2 derived
    L.append(svg(OX, OY, W, H, "".join(tick_badge(tx + 60 + 70 * k, ty + 92, RED, 16) for k in range(3)) + filled(xs[1]) + steps_drawn(xs[1]) + tick_badge(xs[1] + 250, mid - 60),
                 "All three hypotheses checked; lemma 2 derived.", "fade 5"))
    L.append(p(OX + xs[1], OY + mid - 46, 250, "Lemma 2", 28, INK, 600, "center", build="fade 5", family=SERIF))
    # 6. edge cases probed, lemma 3 derived
    probes = ["x = 0", "on the boundary", "degenerate case"]
    pr = ""
    for k, name in enumerate(probes):
        py_ = mid + 120 + 56 * k
        pr += f'<line x1="{xs[2] + 125}" y1="{mid + 60}" x2="{xs[2] + 125}" y2="{py_}" stroke="{GRAY}" stroke-width="2"/>' if k == 2 else ""
        pr += tick_badge(xs[2] + 125, py_, RED, 13)
    L.append(svg(OX, OY, W, H, filled(xs[2]) + steps_drawn(xs[2]) + tick_badge(xs[2] + 250, mid - 60) + pr, "Lemma 3 derived; edge cases tested.", "fade 6"))
    L.append(p(OX + xs[2], OY + mid - 46, 250, "Lemma 3", 28, INK, 600, "center", build="fade 6", family=SERIF))
    for k, name in enumerate(probes):
        L.append(p(OX + xs[2] + 148, OY + mid + 120 + 56 * k - 16, 260, name, 24, INK, 400, build="fade 6"))
    # 7. self-audit catches a "clearly"
    L.append(svg(OX, OY, W, H, f'<rect x="{xs[1] - 14}" y="{mid - 82}" width="296" height="160" rx="18" fill="none" stroke="{DARK}" stroke-width="3" stroke-dasharray="4 6"/>',
                 "The self-audit flags one step in lemma 2.", "fade 7"))
    L.append(p(OX + xs[1] - 75, OY + mid + 90, 400, "Audit: “clearly” → a real derivation", 24, DARK, 600, "center", build="fade 7"))
    # 8. conclusion shown, matches the contract
    L.append(box(OX + 1414, OY + mid - 55, 250, line("Conclusion", 26, INK, 600, family=SERIF) + "\n" +
                 line("the exact question", 20, RED, 600, extra="; letter-spacing:2px; text-transform:uppercase"),
                 build="fade 8", border=RED, bg=CORE, pad=20))
    L.append(svg(OX, OY, W, H, tick_badge(1664 - 20, mid - 55, RED, 16), "The conclusion answers the exact question.", "fade 8"))
    notes = ("solve-problem picks up that frozen question. It first takes the strongest reasonable reading, never a straw man. "
             "Before a long proof, it lays out the plan: the lemmas and how they combine. Then it derives every nontrivial step. "
             "When it relies on an external theorem, it states the exact form it needs and checks every hypothesis against the actual objects. "
             "It tests edge cases: zero, the boundary, degenerate cases. Then it audits its own draft, and any step that leans on 'clearly' "
             "gets a real derivation. Only then does the answer go out, and it answers exactly the question in the contract.")
    return section("solve", "\n".join(L), notes)


# ---------- 3. teach-material: light up every symbol ----------

def teach():
    L = [header("A closer look · Learn", "Light up every symbol.", "teach-material")]
    # the formula as tiles; each symbol lights up when its block defines it
    tiles = [("Ψᵢⱼ⁽ᵏ⁾", 6), (":=", None), ("Σₗ", 6), ("κₗ", 2), ("Λₗⱼ", 2), ("(Ωᵢ ⊗ ξ⁽ᵏ⁻¹⁾)", 1), ("−", None), ("θᵢ", 5)]
    widths = [150, 70, 90, 90, 110, 300, 60, 90]
    gap = 12
    total = sum(widths) + gap * (len(widths) - 1)
    x = 128 + (1664 - total) // 2
    ty = 330
    for (sym, block), w in zip(tiles, widths):
        L.append(p(x, ty, w, sym, 40, "#B9B4A8", 400, "center", family=SERIF,
                   extra=f"; padding:10px 0; border-radius:10px; background:#ECE8DF"))
        if block:
            L.append(p(x, ty, w, sym, 40, INK, 600, "center", build=f"fade {block}", family=SERIF,
                       extra=f"; padding:10px 0; border-radius:10px; background:{CORE}; box-shadow:0 0 0 3px {RED}"))
        x += w + gap
    L.append(p(128, 420, 1664, "Dozens of symbols in one line. Dim means not yet defined.", 24, MUTED, 400, "center"))
    # lesson blocks
    blocks = [
        (1, "Block 1 · inputs", "Ωᵢ, ξ⁽ᵏ⁻¹⁾: vectors in ℝⁿ, one per unit <i>i</i>; ξ evolves with step <i>k</i>.", "exact"),
        (2, "Block 2 · weights", "Λ: a fixed n×n matrix. κₗ: one scalar weight per term <i>l</i>.", "assumption"),
        (3, "Block 3 · offset", "θᵢ: the A.4(ii)-regularized residual.", "heuristic"),
        (4, "Block 4 · the update", "Ψ⁽ᵏ⁾ sums the weighted terms; derived line by line from blocks 1–2.", "exact"),
    ]
    bw, bx0, by = 392, 128, 500
    tag_color = {"exact": RED, "assumption": DARK, "heuristic": MUTED}
    order = {1: 1, 2: 2, 3: 3, 4: 6}
    for i, (_, title, text, status) in enumerate(blocks):
        left = bx0 + i * (bw + 32)
        inner = (label(title, MUTED) + "\n" + line(text, 24, INK) + "\n" +
                 f'    <p style="align-self:flex-start; padding:4px 14px; {SANS}; font-size:20px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:{PAPER}; background:{tag_color[status]}; border-radius:20px">{status}</p>')
        L.append(box(left, by, bw, inner, build=f"rise {order[i + 1]}", height=250, gap=14))
    # confusion on block 3, then the whole block is rebuilt
    b3 = bx0 + 2 * (bw + 32)
    L.append(p(b3 + bw - 76, by + 18, 56, "?", 36, PAPER, 600, "center", build="pop 4",
               extra=f"; background:{DARK}; border-radius:50%; line-height:1.4"))
    L.append(p(b3 - 80, by + 270, bw + 160, "Confused? Rebuild the block, don't patch it.", 22, DARK, 600, "center", build="fade 4"))
    rebuilt = (label("Block 3 · rebuilt", RED) + "\n" +
               line("θᵢ: one number per unit <i>i</i>, fixed before step <i>k</i>. Subtracting it centres Ψ.", 24, INK) + "\n" +
               f'    <p style="align-self:flex-start; padding:4px 14px; {SANS}; font-size:20px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:{PAPER}; background:{DARK}; border-radius:20px">assumption</p>')
    L.append(box(b3, by, bw, rebuilt, build="rise 5", border=RED, height=250, gap=14))
    L.append(p(128, 860, 1664, "One block at a time · every symbol defined, with its type, before use · every claim labelled.", 26, MUTED, 400, "center", build="fade 6"))
    notes = ("The third stage is teach-material. Here's the kind of formula an agent might hand you: dozens of symbols packed into one line. "
             "The skill teaches it one block at a time. Each block introduces one new object, with its type, before using it, and as each block lands, "
             "another symbol in the formula becomes something you understand. Every claim carries its status: exact, an assumption, or a heuristic. "
             "And when you're confused, it doesn't append a one-line patch: it rebuilds the whole block. By the end, every symbol is lit.")
    return section("teach", "\n".join(L), notes)


# ---------- 4. review-paper: a ledger of claims ----------

def review():
    L = [header("A closer look · Audit", "A ledger of claims.", "review-paper")]
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
               extra=f"; padding:4px 0; border-radius:8px; background:{RED}; opacity:0.6"))
    # verdict and confidence
    meter = (f'<rect x="0" y="0" width="502" height="18" rx="9" fill="#E6E1D6"/>'
             f'<rect x="0" y="0" width="330" height="18" rx="9" fill="{RED}"/>')
    L.append(box(128, 830, 902, line("Verdict: central message <b>unsupported</b> until C1 is repaired", 28, INK, 400, family=SERIF), build="rise 8", border=INK, pad=20))
    L.append(svg(EX, 860, 502, 18, meter, "Confidence meter, lowered by one unverifiable source.", "fade 8"))
    L.append(p(EX, 886, 502, "confidence: lowered for what couldn't be checked", 22, MUTED, 400, build="fade 8"))
    notes = ("Finally, review-paper. It reads the whole paper and lifts out the three to five claims that matter most. For each one, it gathers evidence: "
             "it re-derives the key proofs, it retrieves the cited papers and checks that each citation is used correctly, and it audits the code "
             "for leakage and unfair baselines. It rates the plausibility of a conclusion separately from the soundness of its argument. "
             "Each flaw gets a severity, fatal, major or minor, and a fatal flaw cascades to every claim that depends on it. "
             "The verdict says whether the central message stands, and the confidence reflects only what was actually checked.")
    return section("review", "\n".join(L), notes)


def main():
    for sid, make in (("formulate", formulate), ("solve", solve), ("teach", teach), ("review", review)):
        (SLIDES / f"{sid}.html").write_text(make())
    deck_path = HERE / "deck.json"
    deck = json.loads(deck_path.read_text())
    for sid in ("formulate", "solve", "teach", "review"):
        if sid not in deck["order"]:
            deck["order"].append(sid)
    deck_path.write_text(json.dumps(deck, indent=2) + "\n")
    print("order:", deck["order"])


if __name__ == "__main__":
    main()

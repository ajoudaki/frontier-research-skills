"""Generate talk/slides/slides/{agents,foundations,close}.html.

agents: inside one thrust, the engine is many agents: one long thread, independent agents, and agents
in opposition, next to the map from the strategy slide with one edge highlighted.

foundations: the three foundations that make running agents practical, stacked on the left; one at
a time is highlighted and its details fill the panel on the right: context, persistence, and reuse
(projects and skills), which leads into the skills.

close: the conclusion, with the whole project in miniature (from gem_snapshot.json, written by
gen_gem_slide.py), the one goal, what's next, and the big question.

Usage: python talk/slides/gen_basics_slides.py
"""

import json
from pathlib import Path

from gen_gem_slide import SAPPHIRE, SAPPHIRE_SOFT
from gen_skill_slides import (BG, BORDER, CORE, DARK, GRAY, INK, MONO, MUTED, PAPER, RED, SANS, SERIF,
                              arrow, cross_badge, p, section, svg, tick_badge, transition)

SLIDES = Path(__file__).resolve().parent / "slides"
SOFT, TAINT = "#C9C3B5", "#E3B7A6"
CHIP = f'padding:4px 14px; {MONO}; font-size:22px; color:{RED}; background:{CORE}; border-radius:8px'


def heading(eyebrow, title, below=""):
    return (f'  <div style="display:flex; flex-direction:column; gap:16px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>\n{below}  </div>')


def dot(x, y, fill, stroke=None, r=17):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}/>'


def rect(x, y, w, h, fill=PAPER, stroke=BORDER, width=2, r=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def text(x, y, s, size=22, color=INK, weight=400, anchor="start", family="IBM Plex Sans, Arial, sans-serif", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}"{st}>{s}</text>')


# ---------- 03 · the foundations ----------

PX, PY, PW, PH = 688, 300, 1104, 620      # the detail panel
CARDS = [("Context", "A coding agent on one workstation"),
         ("Persistence", "Everything under version control"),
         ("Reuse", "Projects and skills")]


def card(i, highlight, build, cards=None):
    top = 300 + i * 158
    key, what = (cards or CARDS)[i]
    border = f"3px solid {RED}" if highlight else f"1px solid {BORDER}"
    bg = "#FBF3EF" if highlight else PAPER
    b = f' data-build-in="{build}"' if build else ""
    return (f'  <div{b} style="position:absolute; top:{top}px; left:128px; width:520px; height:136px; display:flex; flex-direction:column; '
            f'justify-content:center; gap:6px; padding:0 28px; background:{bg}; border:{border}; border-radius:14px">\n'
            f'    <p style="{SANS}; font-size:20px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">{key}</p>\n'
            f'    <p style="{SERIF}; font-size:28px; font-weight:600; line-height:1.2; color:{INK}">{what}</p>\n  </div>')


def panel(build, title):
    return (f'  <div data-build-in="fade {build}" style="position:absolute; top:{PY}px; left:{PX}px; width:{PW}px; height:{PH}px; '
            f'background:{PAPER}; border:1px solid {BORDER}; border-radius:16px"></div>\n'
            + p(PX + 40, PY + 32, PW - 80, title, 22, RED, 600, build=f"fade {build}", extra="; letter-spacing:3px; text-transform:uppercase"))


def bullets(build, lines, top):
    return [p(PX + 40, top + i * 44, PW - 80, "· " + s, 26, DARK, build=f"fade {build}") for i, s in enumerate(lines)]


def panel_context(build):
    L = [panel(build, "Context: everything in one place")]
    W, H = PW - 80, 330
    hub_x, hub_y, hub_w, hub_h = 270, 30, 340, 270
    art = rect(hub_x, hub_y, hub_w, hub_h, "#FBF3EF", RED, 3, r=16)
    art += text(hub_x + hub_w / 2, hub_y + 34, "your workstation", 24, INK, 600, "middle")
    art += text(hub_x + hub_w / 2, hub_y + 58, "always on", 18, MUTED, 400, "middle")
    for k, folder in enumerate(["theory/", "code/", "results/", "paper/"]):
        art += rect(hub_x + 25 + (k % 2) * 150, hub_y + 76 + (k // 2) * 58, 140, 46, PAPER, BORDER, 2, r=8)
        art += text(hub_x + 95 + (k % 2) * 150, hub_y + 106 + (k // 2) * 58, folder, 22, DARK, 400, "middle", "IBM Plex Mono, monospace")
    art += rect(hub_x + 60, hub_y + 200, 220, 46, CORE, CORE, 1, r=8)
    art += text(hub_x + 170, hub_y + 230, "coding agent", 22, RED, 600, "middle", "IBM Plex Mono, monospace")
    art += rect(20, 110, 180, 110, PAPER, GRAY, 2, r=12)
    art += text(110, 158, "you", 24, INK, 600, "middle") + text(110, 190, "from anywhere", 20, MUTED, 400, "middle")
    art += arrow(202, 165, hub_x - 6, 165, GRAY, 3)
    art += rect(W - 200, 110, 180, 110, PAPER, GRAY, 2, r=12)
    art += text(W - 110, 158, "GPU cluster", 24, INK, 600, "middle") + text(W - 110, 190, "or any server", 20, MUTED, 400, "middle")
    mid = (hub_x + hub_w + W - 200) / 2
    art += arrow(hub_x + hub_w + 6, 140, W - 206, 140, GRAY, 3) + text(mid, 128, "dispatch jobs", 20, MUTED, 400, "middle")
    art += arrow(W - 206, 192, hub_x + hub_w + 6, 192, RED, 3) + text(mid, 222, "results come back", 20, RED, 600, "middle")
    L.append(svg(PX + 40, PY + 84, W, H, art, "Your always-on workstation holds theory, code, results and the paper, with a coding agent; "
                 "you connect from anywhere, jobs go out and results come back.", f"fade {build}"))
    L += bullets(build, ["A coding agent, not a chat",
                         "Theory, code, results, paper: all in reach",
                         "Works overnight, waits for runs"], PY + 440)
    return L


def panel_persistence(build):
    """Snapshots in time, each holding the whole project (theory included); an agent's refactor breaks the
    last one, and the project rolls back to the one before."""
    L = [panel(build, "Persistence: every snapshot holds everything")]
    W, H = PW - 80, 340
    rows = ["theory", "code", "audits", "paper"]
    snaps = [("v1 · theory draft", {"theory"}), ("v2 · experiment", {"code"}), ("v3 · audit", {"audits", "paper"}),
             ("v4 · refactor", {"theory", "code", "paper"})]
    art = f'<line x1="10" y1="318" x2="{W - 20}" y2="318" stroke="{GRAY}" stroke-width="3"/>'
    art += f'<polygon points="{W - 6},318 {W - 22},310 {W - 22},326" fill="{GRAY}"/>' + text(W - 30, 306, "time", 18, MUTED, 400, "end")
    for k, (name, changed) in enumerate(snaps):
        x, y, w, h = 14 + k * 252, 70, 226, 222
        broken = k == 3
        art += rect(x, y, w, h, "#FBF3EF" if broken else PAPER, DARK if broken else BORDER, 2, r=12)
        art += text(x + 16, y + 34, name, 20, DARK if broken else INK, 600, "start")
        for r, row in enumerate(rows):
            ry = y + 64 + r * 38
            hit = row in changed
            color = (DARK if broken else RED) if hit else "#E6E1D6"
            art += f'<rect x="{x + 16}" y="{ry}" width="{w - 32}" height="26" rx="6" fill="{color}" opacity="{0.85 if hit else 1}"/>'
            art += text(x + 28, ry + 19, row, 18, PAPER if hit else MUTED, 600 if hit else 400, "start", "IBM Plex Mono, monospace")
        if broken:
            art += cross_badge(x + w - 26, y + 28, DARK, 15)
        art += dot(x + w / 2, 318, RED if k < 3 else DARK, r=8)
    # roll back from the broken snapshot to the last good one
    art += (f'<path d="M {14 + 3 * 252 + 113} 64 C {14 + 3 * 252 + 113} 16, {14 + 2 * 252 + 113} 16, {14 + 2 * 252 + 113} 58" fill="none" '
            f'stroke="{RED}" stroke-width="3" stroke-dasharray="8 6"/>')
    art += f'<polygon points="{14 + 2 * 252 + 113},66 {14 + 2 * 252 + 105},52 {14 + 2 * 252 + 121},52" fill="{RED}"/>'
    art += text(14 + 2 * 252 + 239, 22, "roll back", 22, RED, 600, "middle")
    L.append(svg(PX + 40, PY + 74, W, H, art, "Four snapshots, each holding theory, code, audits and paper; an agent's refactor breaks the last, "
                 "and the project rolls back to the one before.", f"fade {build}"))
    L += bullets(build, ["Not just code: theory, audits, paper",
                         "Roll back a bad agent or decision",
                         "Big refactors become safe"], PY + 440)
    return L


def panel_reuse(build):
    """A project is a folder with a file every agent in it reads; repeated prompts become skills inside it."""
    L = [panel(build, "Reuse: projects and skills")]
    W, H = PW - 80, 330
    art = ""
    for k in range(3):
        art += rect(10 + k * 12, 92 + k * 20, 270, 64, PAPER, GRAY, 2, r=12)
    art += text(54, 168, "“check every hypothesis…”", 21, DARK, 400, "start", italic=True)
    art += text(160, 232, "a prompt typed again and again", 18, MUTED, 400, "middle")
    # the project folder
    fx, fy, fw, fh = 360, 20, W - 370, 296
    art += f'<path d="M {fx} {fy + 34} L {fx} {fy + 10} Q {fx} {fy} {fx + 10} {fy} L {fx + 170} {fy} L {fx + 196} {fy + 26} L {fx + fw - 10} {fy + 26} Q {fx + fw} {fy + 26} {fx + fw} {fy + 36} L {fx + fw} {fy + fh - 10} Q {fx + fw} {fy + fh} {fx + fw - 10} {fy + fh} L {fx + 10} {fy + fh} Q {fx} {fy + fh} {fx} {fy + fh - 10} Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    art += text(fx + 18, fy + 22, "my-project/", 20, INK, 600, "start", "IBM Plex Mono, monospace")
    rows = [("AGENTS.md", "the project's rules, read by every agent", RED, CORE),
            ("skills/ SKILL.md", "loads by name or by task", RED, CORE),
            ("theory/ code/ paper/", "the project itself", MUTED, "#EFEBE2")]
    for k, (chipt, desc, fg, bg) in enumerate(rows):
        ry = fy + 56 + k * 80
        cw = 14 + 13 * len(chipt)
        art += rect(fx + 24, ry, cw, 40, bg, bg, 1, r=8) + text(fx + 36, ry + 27, chipt, 20, fg, 600, "start", "IBM Plex Mono, monospace")
        art += text(fx + 24, ry + 64, desc, 19, DARK, 400, "start")
    art += arrow(300, 140, fx + 22, fy + 56 + 80 + 20, RED, 3)
    L.append(svg(PX + 40, PY + 84, W, H, art, "A project folder: AGENTS.md, read by every agent in it; a skills folder where repeated prompts "
                 "become skills; and the project's theory, code and paper.", f"fade {build}"))
    L += bullets(build, ["A project: a folder with shared rules",
                         "Skills are plain files: portable across models",
                         "Everything in this repo is a skill"], PY + 440)
    return L


# ---------- 03 · inside one thrust: the multi-agent engine ----------

ENGINE_CARDS = [("One thread", "Why one long thread fails"),
                ("Independence", "Fresh agents, different angles"),
                ("Opposition", "An author and a critic"),
                ("Cost", "A pyramid, and cheap checks")]


def engine():
    """Four stacked cards on the left, one highlighted at a time; the big panel on the right opens on what the
    engine is for, then shows each card's details in turn."""
    L = [heading("03 · Inside one thrust", "The multi-agent engine behind every thrust.")]
    for i in range(4):
        L.append(card(i, False, None, ENGINE_CARDS))

    # step 0: the panel states what the engine is for; each card then opens its details
    L.append(f'  <div style="position:absolute; top:{PY}px; left:{PX}px; width:{PW}px; height:{PH}px; background:{PAPER}; '
             f'border:1px solid {BORDER}; border-radius:16px"></div>')
    L.append(p(PX + 60, PY + 190, PW - 120, "Many agents, well organized, make the push feasible.",
               52, INK, 600, family=SERIF, extra="; line-height:1.25"))

    W = PW - 80
    R = 16

    def show(i, step, title):
        out = [card(i, True, f"fade {step}", ENGINE_CARDS)]
        if i:
            out.append(card(i - 1, False, f"fade {step}", ENGINE_CARDS))
        out.append(panel(step, title))
        return out

    # 1. one long thread: the first steps, the mistake, then everything after it
    L += show(0, 1, "One long thread")
    xs = [30 + 74 * k for k in range(13)]
    base = f'<line x1="{xs[0]}" y1="60" x2="{xs[-1]}" y2="60" stroke="{GRAY}" stroke-width="3"/>' + dot(xs[0], 60, INK, r=R) + "".join(dot(x, 60, SOFT, r=R) for x in xs[1:3])
    L.append(svg(PX + 40, PY + 110, W, 140, base, "One thread: the main agent's first steps.", "fade 1"))
    L.append(svg(PX + 40, PY + 110, W, 140, dot(xs[3], 60, RED, r=R) + text(xs[3], 112, "one mistake", 24, RED, 600, "middle"),
                 "The fourth step is a mistake.", "fade 2"))
    L.append(svg(PX + 40, PY + 110, W, 140, "".join(dot(x, 60, TAINT, r=R) for x in xs[4:]) + text(xs[-1] + R, 112, "…and it never recovers", 24, MUTED, 400, "end"),
                 "Every later step inherits the mistake.", "fade 3"))
    L += bullets(3, ["Every dead end piles into one context",
                     "An early mistake anchors the rest",
                     "\u201cBe unbiased\u201d can't undo it"], PY + 330)

    # 2. independent agents: one branch at a time, the last one catching the flaw
    L += show(1, 4, "Independence: fresh agents, different angles")
    root = (W / 2, 36)
    cols = [W / 2 - 330, W / 2 - 110, W / 2 + 110, W / 2 + 330]
    lv = [116, 196]
    tree = [[(0, 0, 0), (1, 0, 0)],
            [(0, 0, 0), (1, -30, 0), (1, 30, 0)],
            [(0, 0, 0)],
            [(0, -28, None), (0, 28, None), (1, 28, 28)]]
    CAUGHT = (3, 1, 28)
    L.append(svg(PX + 40, PY + 90, W, 290, dot(*root, INK, r=R), "The main agent starts fresh agents.", "fade 4"))
    labels = ["missed", "missed", "missed", "caught it"]
    for b, nodes in enumerate(tree):
        art = ""
        for level, dx, pdx in nodes:
            x, y = cols[b] + dx, lv[level]
            px, py = (root[0], root[1] + R) if level == 0 else (cols[b] + pdx, lv[level - 1] + R)
            on_path = b == CAUGHT[0] and dx == CAUGHT[2]
            art += f'<line x1="{px:.1f}" y1="{py}" x2="{x:.1f}" y2="{y - R}" stroke="{RED if on_path else SOFT}" stroke-width="3"/>'
            if (b, level, dx) == CAUGHT:
                art += dot(x, y, RED, r=R) + (f'<polyline points="{x - 8},{y} {x - 2},{y + 6} {x + 8},{y - 7}" fill="none" '
                                              f'stroke="{PAPER}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                art += dot(x, y, PAPER, GRAY, R)
        art += text(cols[b], 256, labels[b], 24, RED if b == 3 else MUTED, 600 if b == 3 else 400, "middle")
        L.append(svg(PX + 40, PY + 90, W, 290, art, f"Fresh agent {b + 1} explores its own branch and {labels[b]} the flaw.", f"fade {4 + b}"))
    L += bullets(7, ["Each starts clean, sees only its folder",
                     "Several miss; one catch is enough",
                     "Skills: parallel proof routes, gate reviews"], PY + 420)

    # 3. agents in opposition: an author and a critic, round by round
    L += show(2, 8, "Opposition: an author and a critic")
    ax, cx = 220, W - 220
    head = (f'<line x1="{ax}" y1="74" x2="{ax}" y2="290" stroke="{BORDER}" stroke-width="3" stroke-dasharray="6 6"/>'
            f'<line x1="{cx}" y1="74" x2="{cx}" y2="290" stroke="{BORDER}" stroke-width="3" stroke-dasharray="6 6"/>'
            + dot(ax, 54, INK, r=R) + dot(cx, 54, RED, r=R)
            + text(ax, 24, "author", 24, INK, 600, "middle") + text(cx, 24, "critic", 24, RED, 600, "middle"))
    L.append(svg(PX + 40, PY + 84, W, 310, head, "An author and a critic.", "fade 8"))
    for k, (name, x1, x2, color, y) in enumerate([("claim", ax, cx, INK, 120), ("objection", cx, ax, RED, 180), ("repair", ax, cx, INK, 240)]):
        sgn = 1 if x2 > x1 else -1
        art = arrow(x1 + 12 * sgn, y, x2 - 12 * sgn, y, color, 3) + text((ax + cx) / 2, y - 12, name, 24, color, 600, "middle")
        L.append(svg(PX + 40, PY + 84, W, 310, art, f"The {name}.", f"fade {8 + k}"))
    L.append(svg(PX + 40, PY + 84, W, 310, tick_badge(cx, 286, RED, 17) + text(cx - 30, 294, "re-checked: resolved", 24, RED, 600, "end"),
                 "The critic re-checks: the objection is resolved.", "fade 11"))
    L += bullets(11, ["Opposing roles, round after round",
                      "Skills: the hostile audit in formulate-problem",
                      "A fresh review after every fix"], PY + 430)

    # 4. cost: the pyramid, and cheap checks
    L += show(3, 12, "Cost: a pyramid, and cheap checks")
    tiers = [("you", "judgment, approval", INK, PAPER),
             ("most capable models", "reviews, final checks, hardest steps", RED, PAPER),
             ("capable models", "drafting, derivations", "#D98A72", INK),
             ("cheaper models", "code, routine runs", "#EBC3B5", INK)]
    # one true pyramid with straight sides: a pointed top tier (taller, so its label fits), the rest following the slope
    PWid, y0, gap = 700, 6, 6
    heights = [128, 78, 78, 78]
    y_end = y0 + sum(heights) + gap * (len(heights) - 1)
    c = PWid / 2

    def half(y):
        return (y - y0) / (y_end - y0) * (PWid / 2)

    art, y = "", y0
    for k, ((who, what, fill, fg), h) in enumerate(zip(tiers, heights)):
        a_, b_ = half(y), half(y + h)
        if k == 0:
            art += f'<polygon points="{c:.1f},{y:.1f} {c + b_:.1f},{y + h:.1f} {c - b_:.1f},{y + h:.1f}" fill="{fill}"/>'
        else:
            art += f'<polygon points="{c - a_:.1f},{y:.1f} {c + a_:.1f},{y:.1f} {c + b_:.1f},{y + h:.1f} {c - b_:.1f},{y + h:.1f}" fill="{fill}"/>'
        art += text(c, y + h - 38, who, 23, fg, 600, "middle") + text(c, y + h - 13, what, 20, fg, 400, "middle")
        y += h + gap
    L.append(svg(PX + 40, PY + 80, PWid, 380, art, "A cost pyramid: you at the top, the most capable models just below for what is mission-critical, "
                 "capable models below them, and cheaper models at the base.", "fade 12"))
    # two parallel arrows: reliability and cost rise together up the pyramid; the main point sits beside them
    def side_arrow(x, label, color):
        return (arrow(x, 336, x, 28, color, 3)
                + f'<text transform="translate({x - 10},182) rotate(-90)" text-anchor="middle" font-family="IBM Plex Sans, Arial, sans-serif" '
                  f'font-size="19" font-weight="600" fill="{color}">{label}</text>')
    up = (side_arrow(26, "more reliable", INK) + side_arrow(76, "more expensive", MUTED)
          + text(51, 362, "cheaper", 19, MUTED, 600, "middle")
          + text(104, 168, "failures below", 23, RED, 600, "start") + text(104, 198, "are caught above", 23, RED, 600, "start"))
    L.append(svg(PX + 40 + PWid + 6, PY + 80, 318, 380, up, "Two parallel arrows: going up the pyramid, models are more reliable and more "
                 "expensive; failures at a lower level are caught by the audits above it.", "fade 13"))
    L.append(f'  <div data-build-in="fade 14" style="position:absolute; top:{PY + 480}px; left:{PX + 40}px; width:{W}px; display:flex; flex-direction:column; '
             f'gap:6px; padding:18px 22px; background:#FBF3EF; border:2px solid {RED}; border-radius:14px">\n'
             f'    <p style="{SANS}; font-size:22px; font-weight:600; color:{RED}">If a claim can be tested, test it</p>\n'
             f'    <p style="{SANS}; font-size:22px; line-height:1.4; color:{DARK}">A script refutes in seconds. Skills: small-case checks, counterexample search.</p>\n  </div>')
    notes = ("The answer is a multi-agent engine: many agents, organized well, are what make a push into the research frontier "
             "feasible. It has four parts. "
             "First, why not one long thread? It accumulates everything: every dead end, every earlier claim, every sentiment. "
             "Once it makes an early mistake, "
             "everything after it is anchored to it, and telling it to be unbiased can't undo that. "
             "Independent agents start fresh, isolated, from different angles. The first one misses the flaw. "
             "So does the second. "
             "And the third. "
             "The fourth catches it, and one catch is all you need. That's how the skills run parallel proof routes and "
             "independent reviews. "
             "Agents can also work against each other. An author makes a claim. "
             "A critic objects. "
             "The author repairs it. "
             "And the critic checks again, round after round, until the objections are resolved. A single thread can't argue "
             "with itself like that. "
             "And it has to be cost-effective. Think of it as a pyramid. You're at the top: judgment and approval. Just below you, "
             "the most capable and most expensive models, for what's mission-critical: reviews, final checks, the hardest steps. "
             "Below them, capable models for drafting and derivations; at the base, cheaper models for code and routine runs. "
             "The pyramid is built so that a failure at a lower level gets caught by the audits above it. "
             "And when a claim can be tested, test it: a short script can refute a false claim in seconds, while re-checking a proof "
             "takes far longer.")
    return section("agents", "\n".join(L), notes)


# ---------- 04 · the foundations ----------

def foundations():
    L = [heading("04 · The foundations", "Three foundations that make it practical.")]
    for i in range(3):
        L.append(card(i, False, None))
    # each foundation in turn: its card lights up (a plain copy covers the previous one) and its panel opens
    for i, make in enumerate([panel_context, panel_persistence, panel_reuse]):
        step = i + 1
        L.append(card(i, True, f"fade {step}"))
        if i:
            L.append(card(i - 1, False, f"fade {step}"))
        L += make(step)
    notes = ("You can simply ask the main thread to start agents. What makes it practical are three foundations. "
             "Context: a coding agent, not a chat, on one always-on workstation. Then the theory, the LaTeX, the code, the results and "
             "the figures are all in reach. Agents work overnight, and even if you dispatch jobs elsewhere, the results come back. "
             "Persistence: everything under version control, and everything in the same place, theory included. Every snapshot holds "
             "the theory, the code, the audits and the paper together, so when an agent's refactor goes wrong, or you change your mind, "
             "you roll all of it back. "
             "Reuse. A project is just a folder with a file every agent in it reads, so the project's rules load by default. "
             "Prompts you type again and again become skills, which load by name or when a task matches them, and they're plain "
             "files, so they move with you to another model.")
    return section("foundations", "\n".join(L), notes)


# ---------- 12 · conclusion ----------

def close():
    snap = json.loads((Path(__file__).resolve().parent / "gem_snapshot.json").read_text())
    vx, vy, vw, vh = snap["viewBox"]
    GW = 732
    GH = round(GW * vh / vw)
    L = [heading("12 · Conclusion", "From one question to a gem, and what's next.")]
    L.append(f'  <svg data-build-in="fade 1" aria-label="The whole project in miniature: the explored region, the established core, and the gem." '
             f'style="position:absolute; top:296px; left:128px; width:{GW}px; height:{GH}px" width="{GW}" height="{GH}" '
             f'viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}">{snap["svg"]}</svg>')
    chain = [("open question", INK, INK, "#F6F4EF"), ("thrusts", "#EFEADF", "#C9BFA8", INK), ("core", CORE, RED, RED), ("gem", SAPPHIRE_SOFT, SAPPHIRE, SAPPHIRE)]
    x, cy = 128, 296 + GH + 24
    for k, (name, bg, border, fg) in enumerate(chain):
        w = 40 + 14 * len(name)
        L.append(f'  <p data-build-in="fade 1" style="position:absolute; top:{cy}px; left:{x}px; width:{w}px; padding:6px 0; text-align:center; '
                 f'{SANS}; font-size:22px; font-weight:600; color:{fg}; background:{bg}; border:2px solid {border}; border-radius:10px">{name}</p>')
        x += w
        if k < 3:
            L.append(p(x, cy + 6, 40, "→", 24, MUTED, 600, "center", build="fade 1"))
            x += 40
    L.append(p(128, cy + 76, GW, "One goal: raise the signal-to-noise ratio.", 34, INK, 600, family=SERIF, build="fade 2",
               extra="; line-height:1.3"))
    R0, RW = 940, 852
    L.append(p(R0, 300, RW, "What's next", 22, RED, 600, build="fade 3", extra="; letter-spacing:3px; text-transform:uppercase"))
    nexts = [("Beyond theory", "other domains"), ("Evaluations", "does a change help a skill?"), ("Live skills", "learn from your chats")]
    for k, (h, s_) in enumerate(nexts):
        L.append(p(R0, 346 + k * 60, RW, f'<b style="color:{INK}">{h}</b>  <span style="color:{MUTED}">{s_}</span>', 32, DARK, build="fade 3"))
    L.append(p(R0, 560, RW, "The big question", 22, RED, 600, build="fade 4", extra="; letter-spacing:3px; text-transform:uppercase"))
    L.append(p(R0, 602, RW, "Can agents learn research taste?", 44, INK, 600, family=SERIF, build="fade 4"))
    L.append(f'  <p data-build-in="fade 5" style="position:absolute; top:806px; left:{R0}px; width:{RW}px; {MONO}; font-size:28px; color:{RED}">'
             f'<a href="https://github.com/ajoudaki/frontier-research-skills">github.com/ajoudaki/frontier-research-skills</a></p>')
    L.append(p(R0, 860, RW, "Thank you.", 48, INK, 600, family=SERIF, build="fade 5"))
    notes = ("So to wrap up. We started from one open-ended question, explored it in thrusts, built a core, and carved out a gem. "
             "Everything we discussed has one goal: raise the signal-to-noise ratio, and save your time in every possible way, so you "
             "get what you're really after. In my own project, that meant about two hundred and thirty-five studies in eleven weeks, "
             "and only a small fraction of them ever made it into the core. "
             "What's next? These skills are very theory-oriented, but there's no reason they can't be adapted to other domains, and I "
             "hope people do. Two things I'd have liked to add: evaluations for skills, because right now, when you change a skill, it's "
             "not clear whether it really improved; and what I'd call live skills: a process under the hood that watches your chats, "
             "adapts your skills, maybe even writes new ones, and uses those evaluations to check. "
             "And a last, more philosophical note. We've gone from delegating tiny tasks to delegating maybe ninety-five percent of the "
             "mechanical work. So where does it stop? Right now, what's missing seems to be taste: knowing which direction is relevant, "
             "which is a dead end, where to explore in uncharted waters and when to stop. The good old exploration-exploitation "
             "dilemma. Ask an agent to supervise the whole thing today and you'll get a paper, at enormous cost, maybe even correct, "
             "but rarely a great one. Could we one day give a machine one open question and come back two months later to something "
             "extraordinary? There's no reason to think not. But not today. "
             "Everything is in the repo. Thank you.")
    return section("close", "\n".join(L), notes)


def main():
    for sid, make in (("agents", engine), ("foundations", foundations), ("close", close)):
        (SLIDES / f"{sid}.html").write_text(make())
        print(f"wrote {sid}.html")


if __name__ == "__main__":
    main()

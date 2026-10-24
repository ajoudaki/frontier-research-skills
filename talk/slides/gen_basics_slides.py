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


def card(i, highlight, build):
    top = 300 + i * 158
    key, what = CARDS[i]
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
    L += bullets(build, ["A coding agent, not a chat: no uploading back and forth",
                         "Theory, LaTeX, code, results and figures, all in reach",
                         "Agents work overnight, and wait for runs to finish"], PY + 440)
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
    L += bullets(build, ["Not just code: the theory, the notes, the audits, the paper, all in one place",
                         "Roll back when an agent, or a decision, goes wrong",
                         "Big refactors become safe to try"], PY + 440)
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
    rows = [("AGENTS.md", "every agent in this folder reads it: the project's rules", RED, CORE),
            ("skills/ SKILL.md", "loads by name, or when a task matches it", RED, CORE),
            ("theory/ code/ paper/", "the project itself", MUTED, "#EFEBE2")]
    for k, (chipt, desc, fg, bg) in enumerate(rows):
        ry = fy + 56 + k * 80
        cw = 14 + 13 * len(chipt)
        art += rect(fx + 24, ry, cw, 40, bg, bg, 1, r=8) + text(fx + 36, ry + 27, chipt, 20, fg, 600, "start", "IBM Plex Mono, monospace")
        art += text(fx + 24, ry + 64, desc, 19, DARK, 400, "start")
    art += arrow(300, 140, fx + 22, fy + 56 + 80 + 20, RED, 3)
    L.append(svg(PX + 40, PY + 84, W, H, art, "A project folder: AGENTS.md, read by every agent in it; a skills folder where repeated prompts "
                 "become skills; and the project's theory, code and paper.", f"fade {build}"))
    L += bullets(build, ["A project is a folder with a file every agent in it reads",
                         "Skills are plain files: they move with you to another model",
                         "Everything in this repo is a skill"], PY + 440)
    return L


# ---------- 03 · inside one thrust: many agents ----------

def engine():
    """Zoom into one edge of the map; three ways of working side by side: one long thread, independent
    agents (three miss the flaw, one catches it), and agents in opposition (an author and a critic
    exchanging rounds until the objections are resolved)."""
    L = [heading("03 · Inside one thrust", "The engine: many agents.")]
    # the map in miniature with the circled push, and below it the same circle magnified, as in a textbook figure
    snap = json.loads((Path(__file__).resolve().parent / "gem_snapshot.json").read_text())
    vx, vy, vw, vh = snap["viewBox"]
    mx, my, cr = snap["circle"]
    IW, IX, IY = 340, 128, 296
    s = IW / vw
    IH = round(vh * s)
    L.append(f'  <svg aria-label="The map from the strategy slide, with the push into uncharted waters circled." '
             f'style="position:absolute; top:{IY}px; left:{IX}px; width:{IW}px; height:{IH}px" width="{IW}" height="{IH}" '
             f'viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}">{snap["svg"]}{snap["push"]}'
             f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{cr:.1f}" fill="none" stroke="{INK}" stroke-width="{3 / s:.1f}"/></svg>')
    sx, sy, sr = IX + (mx - vx) * s, IY + (my - vy) * s, cr * s          # the small circle on the slide
    BR = 132
    bx, by = IX + IW / 2, IY + IH + 26 + BR                              # the magnified circle
    zoom = 1.25 * cr                                                     # half-width of the region it shows
    lines = (f'<line x1="{sx - sr:.1f}" y1="{sy:.1f}" x2="{bx - BR:.1f}" y2="{by:.1f}" stroke="{INK}" stroke-width="1.5"/>'
             f'<line x1="{sx + sr:.1f}" y1="{sy:.1f}" x2="{bx + BR:.1f}" y2="{by:.1f}" stroke="{INK}" stroke-width="1.5"/>')
    L.append(svg(0, 0, 1920, 1080, lines, "Lines joining the small circle to its magnified view."))
    L.append(f'  <svg aria-label="The circled push, magnified: a study at the edge of the core reaching into uncharted waters." '
             f'style="position:absolute; top:{by - BR:.0f}px; left:{bx - BR:.0f}px; width:{2 * BR}px; height:{2 * BR}px" '
             f'width="{2 * BR}" height="{2 * BR}" viewBox="{mx - zoom:.1f} {my - zoom:.1f} {2 * zoom:.1f} {2 * zoom:.1f}">'
             f'<defs><clipPath id="lens"><circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom:.1f}"/></clipPath></defs>'
             f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom:.1f}" fill="{BG}"/>'
             f'<g clip-path="url(#lens)">{snap["svg"]}{snap["push"]}</g>'
             f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{zoom - 1.5 * zoom / BR:.1f}" fill="none" stroke="{INK}" stroke-width="{3 * zoom / BR:.2f}"/></svg>')
    L.append(p(128, by + BR + 14, IW, "One push into uncharted waters. The frontier is hard: how do we make it succeed, and correctly?",
               22, DARK, extra="; line-height:1.4"))

    PW_, PT, PH_ = 412, 300, 580
    lefts = [520, 950, 1380]

    def frame(i, title, color, b):
        return (f'  <div data-build-in="fade {b}" style="position:absolute; top:{PT}px; left:{lefts[i]}px; width:{PW_}px; height:{PH_}px; '
                f'background:{PAPER}; border:2px solid {color}; border-radius:16px"></div>\n'
                + p(lefts[i] + 24, PT + 22, PW_ - 48, title, 20, color, 600, build=f"fade {b}", extra="; letter-spacing:3px; text-transform:uppercase"))

    def words(i, top, s, b, size=22, color=DARK, weight=400):
        return p(lefts[i] + 24, PT + top, PW_ - 48, s, size, color, weight, build=f"fade {b}", extra="; line-height:1.4")

    R, SW = 12, PW_ - 48
    # 1. one long thread: the first steps, the mistake, then everything after it
    L.append(frame(0, "One long thread", MUTED, 1))
    xs = [18 + 52 * k for k in range(7)]
    base = f'<line x1="{xs[0]}" y1="40" x2="{xs[-1]}" y2="40" stroke="{GRAY}" stroke-width="3"/>' + dot(xs[0], 40, INK, r=R) + dot(xs[1], 40, SOFT, r=R)
    L.append(svg(lefts[0] + 24, PT + 80, SW, 100, base, "One thread: the main agent's first steps.", "fade 1"))
    L.append(svg(lefts[0] + 24, PT + 80, SW, 100, dot(xs[2], 40, RED, r=R) + text(xs[2], 84, "one mistake", 20, RED, 600, "middle"),
                 "The third step is a mistake.", "fade 2"))
    L.append(svg(lefts[0] + 24, PT + 80, SW, 100, "".join(dot(x, 40, TAINT, r=R) for x in xs[3:]) + text(xs[-1] + R, 84, "…never recovers", 20, MUTED, 400, "end"),
                 "Every later step inherits the mistake.", "fade 3"))
    L.append(words(0, 300, "Everything piles into one context. An early mistake anchors everything after it, and asking the thread "
                   "to be unbiased can't undo that.", 3))
    # 2. independent agents: one branch at a time, the last one catching the flaw
    L.append(frame(1, "Independent agents", RED, 4))
    root = (SW / 2, 26)
    cols = [SW / 2 - 132, SW / 2 - 44, SW / 2 + 44, SW / 2 + 132]
    lv = [92, 152]
    tree = [[(0, 0, 0), (1, 0, 0)],
            [(0, 0, 0), (1, -20, 0), (1, 20, 0)],
            [(0, 0, 0)],
            [(0, -18, None), (0, 18, None), (1, 18, 18)]]
    CAUGHT = (3, 1, 18)
    L.append(svg(lefts[1] + 24, PT + 70, SW, 230, dot(*root, INK, r=R), "The main agent starts fresh agents.", "fade 4"))
    labels = ["missed", "missed", "missed", "caught"]
    for b, nodes in enumerate(tree):
        art = ""
        for level, dx, pdx in nodes:
            x, y = cols[b] + dx, lv[level]
            px, py = (root[0], root[1] + R) if level == 0 else (cols[b] + pdx, lv[level - 1] + R)
            on_path = b == CAUGHT[0] and dx == CAUGHT[2]
            art += f'<line x1="{px:.1f}" y1="{py}" x2="{x:.1f}" y2="{y - R}" stroke="{RED if on_path else SOFT}" stroke-width="3"/>'
            if (b, level, dx) == CAUGHT:
                art += dot(x, y, RED, r=R) + (f'<polyline points="{x - 6},{y} {x - 2},{y + 4} {x + 6},{y - 5}" fill="none" '
                                              f'stroke="{PAPER}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                art += dot(x, y, PAPER, GRAY, R)
        art += text(cols[b], 200, labels[b], 20, RED if b == 3 else MUTED, 600 if b == 3 else 400, "middle")
        L.append(svg(lefts[1] + 24, PT + 70, SW, 230, art, f"Fresh agent {b + 1} explores its own branch and {labels[b]} the flaw.", f"fade {4 + b}"))
    L.append(words(1, 300, "Fresh, isolated, from different angles. Several can miss; one catch is enough.", 7))
    L.append(words(1, 420, "In the skills: parallel proof routes; independent reviews at the promotion gate.", 7, 20, MUTED))
    # 3. agents in opposition: an author and a critic, round by round
    L.append(frame(2, "Agents in opposition", INK, 8))
    ax, cx = 70, SW - 70
    head = (f'<line x1="{ax}" y1="56" x2="{ax}" y2="256" stroke="{BORDER}" stroke-width="3" stroke-dasharray="6 6"/>'
            f'<line x1="{cx}" y1="56" x2="{cx}" y2="256" stroke="{BORDER}" stroke-width="3" stroke-dasharray="6 6"/>'
            + dot(ax, 40, INK, r=R) + dot(cx, 40, RED, r=R)
            + text(ax, 18, "author", 20, INK, 600, "middle") + text(cx, 18, "critic", 20, RED, 600, "middle"))
    L.append(svg(lefts[2] + 24, PT + 70, SW, 270, head, "An author and a critic.", "fade 8"))
    rounds = [("claim", ax, cx, INK, 96), ("objection", cx, ax, RED, 148), ("repair", ax, cx, INK, 200)]
    for k, (name, x1, x2, color, y) in enumerate(rounds):
        art = arrow(x1 + (10 if x2 > x1 else -10), y, x2 - (10 if x2 > x1 else -10), y, color, 3) + text((ax + cx) / 2, y - 10, name, 20, color, 600, "middle")
        L.append(svg(lefts[2] + 24, PT + 70, SW, 270, art, f"The {name}.", f"fade {8 + k}"))
    done = tick_badge(cx, 246, RED, 15) + text(cx - 26, 252, "resolved", 20, RED, 600, "end")
    L.append(svg(lefts[2] + 24, PT + 70, SW, 270, done, "The critic re-checks: the objection is resolved.", "fade 11"))
    L.append(words(2, 360, "Opposing roles, round after round. A single thread can't argue with itself.", 11))
    L.append(words(2, 450, "In the skills: the hostile audit of formulate-problem; separate checks of a candidate proof; "
                   "a fresh review after every correction.", 11, 20, MUTED))
    L.append(transition("Easier said than done. How do we run this in practice?", 12))
    notes = ("Let's zoom into that one push. It's a hard research barrier, out in uncharted waters, and even a very capable model can "
             "fail here. How do we maximize the chance it gets through, and correctly? The answer is many agents. "
             "Compare three ways of working. "
             "One long thread accumulates everything: every dead end, every earlier claim, every sentiment. "
             "Once it makes an early mistake, "
             "everything after it is anchored to it, and telling it to be unbiased can't undo that. "
             "Independent agents start fresh, isolated, and from different angles. The first one misses the flaw. "
             "So does the second. "
             "And the third. "
             "The fourth catches it, and one catch is all you need. That's how the skills run parallel proof routes and "
             "independent reviews. "
             "And agents can also work against each other. An author makes a claim. "
             "A critic objects. "
             "The author repairs it. "
             "And the critic checks again, round after round, until the objections are resolved. A single thread can't argue "
             "with itself like that. That's the hostile audit in formulate-problem, the separate checks on a candidate proof, and "
             "the fresh review after every correction. "
             "But this is easier said than done. How do we run it in practice?")
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
    L.append(transition("In fact, everything we'll talk about from here is a skill. Here are the five.", 4))
    notes = ("You can simply ask the main thread to start agents. What makes it practical are three foundations. "
             "Context: a coding agent, not a chat, on one always-on workstation. Then the theory, the LaTeX, the code, the results and "
             "the figures are all in reach. Agents work overnight, and even if you dispatch jobs elsewhere, the results come back. "
             "Persistence: everything under version control, and everything in the same place, theory included. Every snapshot holds "
             "the theory, the code, the audits and the paper together, so when an agent's refactor goes wrong, or you change your mind, "
             "you roll all of it back. "
             "And reuse. A project is just a folder with a file every agent in it reads, so the project's rules load by default. "
             "Prompts you type again and again become skills, which load by name or when a task matches them, and they're plain "
             "files, so they move with you to another model. "
             "In fact, everything we'll talk about from here is a skill. Here are the five.")
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
    L.append(p(128, cy + 76, GW, "One goal throughout: raise the signal-to-noise ratio, and spend your time only on what matters.",
               30, INK, 600, family=SERIF, build="fade 2", extra="; line-height:1.3"))
    R0, RW = 940, 852
    L.append(p(R0, 300, RW, "What's next", 22, RED, 600, build="fade 3", extra="; letter-spacing:3px; text-transform:uppercase"))
    nexts = [("Beyond theory:", "adapt these theory-first skills to other domains"),
             ("Evaluations:", "know whether a change really improves a skill"),
             ("Live skills:", "learn from your own chats, adapt skills and write new ones, checked by those evaluations")]
    for k, (h, s) in enumerate(nexts):
        L.append(p(R0, 344 + k * 76, RW, f"<b>{h}</b> {s}", 26, DARK, build="fade 3", extra="; line-height:1.35"))
    L.append(p(R0, 600, RW, "The big question", 22, RED, 600, build="fade 4", extra="; letter-spacing:3px; text-transform:uppercase"))
    L.append(p(R0, 642, RW, "Agents now do most of the mechanical work. What's missing is research taste: where to explore, when to stop. "
               "Could they one day run a whole project from a single open question? Not today.", 26, DARK, build="fade 4", extra="; line-height:1.4"))
    L.append(f'  <p data-build-in="fade 5" style="position:absolute; top:846px; left:{R0}px; width:{RW}px; {MONO}; font-size:28px; color:{RED}">'
             f'<a href="https://github.com/ajoudaki/personal-skills">github.com/ajoudaki/personal-skills</a></p>')
    L.append(p(R0, 896, RW, "Thank you.", 36, INK, 600, family=SERIF, build="fade 5"))
    notes = ("So to wrap up. We started from one open-ended question, explored it in thrusts, built a core, and carved out a gem. "
             "Everything we discussed has one goal: raise the signal-to-noise ratio, and save your time in every possible way, so you "
             "get what you're really after. "
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

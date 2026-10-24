"""Generate talk/slides/slides/{foundations,close}.html.

foundations: the four foundations under the strategy, stacked on the left; one at a time is
highlighted and its details fill the panel on the right (context, persistence, reuse, many agents).
The many-agents panel shows one long thread building up a mistake, then fresh agents exploring one
branch at a time: three miss the flaw, one catches it.

close: what comes next, on the light theme.

Usage: python talk/slides/gen_basics_slides.py
"""

from pathlib import Path

from gen_skill_slides import (BORDER, CORE, DARK, GRAY, INK, MONO, MUTED, PAPER, RED, SANS, SERIF,
                              arrow, cross_badge, p, section, svg, transition)

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
CARDS = [("Context", "A coding agent on one always-on machine"),
         ("Persistence", "Everything under version control"),
         ("Reuse", "Prompts become skills"),
         ("Many agents", "Fresh, independent agents")]


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
    L = [panel(build, "Context: everything in reach")]
    W, H = PW - 80, 330
    hub_x, hub_y, hub_w, hub_h = 270, 30, 340, 270
    art = rect(hub_x, hub_y, hub_w, hub_h, "#FBF3EF", RED, 3, r=16)
    art += text(hub_x + hub_w / 2, hub_y + 40, "one always-on machine", 24, INK, 600, "middle")
    for k, folder in enumerate(["theory/", "code/", "results/", "paper/"]):
        art += rect(hub_x + 25 + (k % 2) * 150, hub_y + 66 + (k // 2) * 62, 140, 48, PAPER, BORDER, 2, r=8)
        art += text(hub_x + 95 + (k % 2) * 150, hub_y + 97 + (k // 2) * 62, folder, 22, DARK, 400, "middle", "IBM Plex Mono, monospace")
    art += rect(hub_x + 60, hub_y + 200, 220, 46, CORE, CORE, 1, r=8)
    art += text(hub_x + 170, hub_y + 230, "coding agent", 22, RED, 600, "middle", "IBM Plex Mono, monospace")
    # you, from anywhere
    art += rect(20, 110, 180, 110, PAPER, GRAY, 2, r=12)
    art += text(110, 158, "you", 24, INK, 600, "middle") + text(110, 190, "from anywhere", 20, MUTED, 400, "middle")
    art += arrow(202, 165, hub_x - 6, 165, GRAY, 3)
    # the cluster: jobs out, results back
    art += rect(W - 200, 110, 180, 110, PAPER, GRAY, 2, r=12)
    art += text(W - 110, 158, "GPU cluster", 24, INK, 600, "middle") + text(W - 110, 190, "or any server", 20, MUTED, 400, "middle")
    mid = (hub_x + hub_w + W - 200) / 2
    art += arrow(hub_x + hub_w + 6, 140, W - 206, 140, GRAY, 3) + text(mid, 128, "dispatch jobs", 20, MUTED, 400, "middle")
    art += arrow(W - 206, 192, hub_x + hub_w + 6, 192, RED, 3) + text(mid, 222, "results come back", 20, RED, 600, "middle")
    L.append(svg(PX + 40, PY + 84, W, H, art, "One always-on machine holds theory, code, results and the paper, with a coding agent; "
                 "you connect from anywhere, jobs go out and results come back.", f"fade {build}"))
    L += bullets(build, ["A coding agent, not a chat: no uploading back and forth",
                         "Chats can be grouped into projects; here the repo is the project, for everything",
                         "Agents work overnight, and wait for runs to finish"], PY + 440)
    return L


def panel_persistence(build):
    L = [panel(build, "Persistence: every step can be undone")]
    W, H = PW - 80, 330
    y, xs = 120, [70, 220, 370, 520, 670]
    labels = ["theory note", "experiment", "audit", "paper draft", "next idea"]
    art = f'<line x1="20" y1="{y}" x2="{W - 20}" y2="{y}" stroke="{GRAY}" stroke-width="4"/>'
    for x, lab in zip(xs, labels):
        art += dot(x, y, PAPER, GRAY, 13) if lab == "next idea" else dot(x, y, RED, None, 13)
        art += text(x, y - 30, lab, 20, DARK, 400, "middle")
    # an agent's big refactor branches off and goes wrong; the project rolls back
    bx = [590, 730, 870]
    art += f'<path d="M {xs[3]} {y} C {xs[3] + 30} {y + 70}, {bx[0] - 40} {y + 110}, {bx[0]} {y + 110}" fill="none" stroke="{GRAY}" stroke-width="4"/>'
    art += f'<line x1="{bx[0]}" y1="{y + 110}" x2="{bx[2]}" y2="{y + 110}" stroke="{GRAY}" stroke-width="4"/>'
    for x in bx[:2]:
        art += dot(x, y + 110, SOFT, None, 13)
    art += cross_badge(bx[2], y + 110, DARK, 18)
    art += text(bx[1], y + 160, "an agent's big refactor goes wrong", 20, DARK, 400, "middle")
    art += (f'<path d="M {bx[2] + 20} {y + 92} C {bx[2] + 120} {y + 20}, {xs[3] + 120} {y - 120}, {xs[3] + 10} {y - 48}" fill="none" '
            f'stroke="{RED}" stroke-width="3" stroke-dasharray="8 6"/>')
    art += f'<polygon points="{xs[3] + 6},{y - 44} {xs[3] + 26},{y - 56} {xs[3] + 22},{y - 36}" fill="{RED}"/>'
    art += text(bx[2] + 70, y - 40, "roll back", 22, RED, 600, "start")
    L.append(svg(PX + 40, PY + 84, W, H, art, "A version history of theory, experiments, audits and the paper; an agent's refactor branch fails and the "
                 "project rolls back to the last good state.", f"fade {build}"))
    L += bullets(build, ["Not just code: the theory, the notes, the audits, the paper",
                         "Roll back when an agent, or a decision, goes wrong",
                         "Big refactors become safe to try"], PY + 440)
    return L


def panel_reuse(build):
    L = [panel(build, "Reuse: prompts become skills")]
    W, H = PW - 80, 330
    art = ""
    for k in range(3):
        art += rect(20 + k * 14, 40 + k * 22, 300, 70, PAPER, GRAY, 2, r=12)
    art += text(70, 120, "“check every hypothesis…”", 22, DARK, 400, "start", italic=True)
    art += text(190, 190, "typed again and again", 20, MUTED, 400, "middle")
    art += arrow(360, 105, 440, 105, RED, 3)
    art += rect(450, 30, 220, 160, "#FBF3EF", RED, 3, r=12)
    art += text(560, 70, "SKILL.md", 24, RED, 600, "middle", "IBM Plex Mono, monospace")
    for k in range(4):
        art += f'<line x1="480" y1="{98 + k * 22}" x2="{640 - (k % 2) * 40}" y2="{98 + k * 22}" stroke="{TAINT}" stroke-width="6" stroke-linecap="round"/>'
    ways = [("default for a project", "every agent in its folder reads it"),
            ("by name", "when you ask for it"),
            ("by keywords", "when a task matches it")]
    art += text(724, 40, "it loads", 20, MUTED, 600, "start")
    for k, (a, b) in enumerate(ways):
        art += arrow(676, 110, 716, 72 + k * 82, GRAY, 2)
        art += text(724, 80 + k * 82, a, 22, INK, 600, "start") + text(724, 106 + k * 82, b, 20, MUTED, 400, "start")
    L.append(svg(PX + 40, PY + 84, W, H, art, "A prompt typed again and again becomes a SKILL.md file, which loads by default for a project, "
                 "by name, or by keywords.", f"fade {build}"))
    L += bullets(build, ["Plain files: unlike a chat's memory, they move with you to another model",
                         "A large skill routes to parts that load only when needed",
                         "Everything in this repo is a skill"], PY + 440)
    return L


def panel_agents(build):
    """The many-agents panel: the long thread at once, then each fresh agent's branch in its own step."""
    L = [panel(build, "Many agents: not for speed, for independence")]
    L.append(p(PX + 40, PY + 70, PW - 80, f'built into <span style="{CHIP}">formulate-problem</span> '
               f'<span style="{CHIP}">organize-research-project</span>', 20, MUTED, build=f"fade {build}"))
    # one long thread
    SX, SY, SW = PX + 40, PY + 126, PW - 80
    xs = [24 + 50 * k for k in range(14)]
    art = f'<line x1="4" y1="30" x2="{xs[-1] + 20}" y2="30" stroke="{GRAY}" stroke-width="3"/>'
    art += "".join(dot(x, 30, SOFT, r=14) for x in xs[:2]) + dot(xs[2], 30, RED, r=14) + "".join(dot(x, 30, TAINT, r=14) for x in xs[3:])
    art += text(4, 82, "one long thread: one mistake…", 22, RED, 400, "start") + text(xs[-1] + 14, 82, "…and it never recovers", 22, MUTED, 400, "end")
    L.append(svg(SX, SY, SW, 100, art, "One long thread: the third step is a mistake and every step after it inherits it.", f"fade {build}"))
    # fresh agents, one branch at a time
    TX, TY, TW, TH = PX + 40, PY + 236, PW - 80, 270
    root, R = (TW / 2, 20), 14
    cols = [TW / 2 - 330, TW / 2 - 110, TW / 2 + 110, TW / 2 + 330]
    lv = [80, 136, 192]
    tree = [
        [(0, 0, 0), (1, 0, 0), (2, 0, 0)],
        [(0, 0, 0), (1, 0, 0), (2, -32, 0), (2, 32, 0)],
        [(0, 0, 0), (1, -28, 0), (1, 28, 0), (2, 28, 28)],
        [(0, 0, 0), (1, 0, 0)],
    ]
    CAUGHT = (2, 2, 28)
    L.append(svg(TX, TY, TW, TH, f'<circle cx="{root[0]}" cy="{root[1]}" r="18" fill="{INK}"/>', "A main agent starts fresh agents.", f"fade {build}"))
    labels = ["missed", "missed", "caught it", "missed"]
    for b, nodes in enumerate(tree):
        art = ""
        for level, dx, pdx in nodes:
            x, y = cols[b] + dx, lv[level]
            px, py = (cols[b] + pdx, lv[level - 1] + R) if level else (root[0], root[1] + 18)
            on_path = b == CAUGHT[0] and (dx == CAUGHT[2] or level == 0)
            art += f'<line x1="{px}" y1="{py}" x2="{x}" y2="{y - R}" stroke="{RED if on_path else SOFT}" stroke-width="3"/>'
            if (b, level, dx) == CAUGHT:
                art += dot(x, y, RED, r=R + 3) + (f'<polyline points="{x - 8},{y} {x - 2},{y + 6} {x + 9},{y - 7}" fill="none" '
                                                  f'stroke="{PAPER}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                art += dot(x, y, PAPER, GRAY, R)
        art += text(cols[b], 252, labels[b], 22, RED if b == 2 else MUTED, 600 if b == 2 else 400, "middle")
        L.append(svg(TX, TY, TW, TH, art, f"Fresh agent {b + 1} explores its own branch and {labels[b]} the flaw.", f"fade {build + 1 + b}"))
    L.append(p(PX + 40, PY + 556, PW - 80, "Each starts clean and sees only its own folder. Several can miss; one catch is enough.",
               24, DARK, build=f"fade {build + 4}"))
    return L


def foundations():
    L = [heading("03 · The foundations", "Four foundations under the strategy.")]
    for i in range(4):
        L.append(card(i, False, None))
    # each foundation in turn: its card lights up (a plain copy covers the previous one) and its panel opens
    for i, make in enumerate([panel_context, panel_persistence, panel_reuse, panel_agents]):
        step = i + 1
        L.append(card(i, True, f"fade {step}"))
        if i:
            L.append(card(i - 1, False, f"fade {step}"))
        L += make(step)
    L.append(transition("And everything in this repo is a skill built on these. Here are the five.", 9))
    notes = ("So that's the strategy. But it's easier said than done. Do we need smarter models? Surprisingly, no: the models already "
             "have the capability. What's missing is the workflow around them, and it rests on four foundations. "
             "First, context. Use a coding agent, not a chat, and run it on one central, always-on machine. Then the theory, the LaTeX, "
             "the code, the results and the figures are all in reach, and you stop uploading things back and forth. Chat apps let you "
             "group threads into projects; here the repo is the project, for everything. Agents work overnight, and even if you "
             "dispatch jobs elsewhere, the results come back to that one place. "
             "Second, persistence: put everything under version control. Not just the code, which most of us already do, but the "
             "theory, the notes, the audits, the paper. When you give agents freedom, things go wrong, or you change your mind, or you "
             "want a big refactor, and you can always roll back. "
             "Third, reuse. If you type the same prompt again and again, turn it into a skill. A skill can be the default for a "
             "project, so every agent in that folder reads it; or you load it by name; or it loads itself when a task matches its "
             "description. And unlike a chat's memory, skills are plain files, so they move with you to another model. "
             "The fourth is less obvious: many agents. Not because they're faster: you pay for the tokens either way. A single thread "
             "accumulates everything: every dead end, every earlier claim, every sentiment. Once it makes an early mistake, everything "
             "after it is anchored to it, and telling it to be unbiased can't undo that. "
             "Separate agents start clean, especially if you isolate them and decide mechanically what they see. Run four, prompted "
             "for diversity. The first misses the flaw. "
             "So does the second. "
             "The third catches it. "
             "The fourth misses again. One catch is all you need: it's asking ten people instead of one person ten times. "
             "And everything in this repo is a skill built on these foundations. Here are the five.")
    return section("foundations", "\n".join(L), notes)


# ---------- 11 · what's next ----------

def close():
    L = [heading("11 · What's next", "This is just the beginning.",
                 f'    <p style="{SANS}; font-size:32px; line-height:1.4; color:{DARK}">Simple ideas made an enormous difference. '
                 f'There\'s much more room to improve.</p>\n')]
    ideas = [("Skills that adapt", "Skills that learn from how you correct them, while you work."),
             ("Evaluations for skills", "Measure whether a skill actually improves the research it touches."),
             ("Beyond theory", "These habits come from theoretical research. How do they extend to other kinds?")]
    for i, (h, s) in enumerate(ideas):
        left = 128 + i * 572
        L.append(f'  <div data-build-in="rise {i + 1}" style="position:absolute; top:470px; left:{left}px; width:520px; height:250px; '
                 f'display:flex; flex-direction:column; gap:14px; padding:32px; background:{PAPER}; border:1px solid {BORDER}; border-radius:16px">\n'
                 f'    <p style="{SANS}; font-size:22px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">0{i + 1}</p>\n'
                 f'    <h3 style="{SERIF}; font-size:34px; font-weight:600; color:{INK}">{h}</h3>\n'
                 f'    <p style="{SANS}; font-size:24px; line-height:1.4; color:{DARK}">{s}</p>\n  </div>')
    L.append(f'  <p data-build-in="rise 4" style="position:absolute; top:790px; left:128px; width:1664px; {MONO}; font-size:32px; color:{RED}">'
             f'<a href="https://github.com/ajoudaki/personal-skills">github.com/ajoudaki/personal-skills</a></p>')
    L.append(p(128, 860, 1664, "Thank you.", 40, INK, 600, family=SERIF, build="rise 4"))
    notes = ("So to wrap up. All the ideas I've shared are simple, but for me they made an enormous difference, and this is clearly "
             "just the beginning. Three directions I'd love to see. "
             "Skills that adapt while you work, learning from how you correct them. "
             "Evaluations for skills, so we know whether a skill actually helps; I didn't have time to add them. "
             "And extending these habits beyond theoretical research, where they come from. "
             "Everything is in the repo: use it, improve it, and add your own tricks for your domain. Thank you.")
    return section("close", "\n".join(L), notes)


def main():
    for sid, make in (("foundations", foundations), ("close", close)):
        (SLIDES / f"{sid}.html").write_text(make())
        print(f"wrote {sid}.html")


if __name__ == "__main__":
    main()

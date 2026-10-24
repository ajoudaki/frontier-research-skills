"""Generate talk/slides/slides/{setup,agents}.html: the four foundations, and why many agents.

setup: four cards (context, persistence, reuse, many agents), one per step.
agents: one long thread builds block by block until a mistake taints the rest;
then fresh agents explore one branch at a time: three miss the flaw, one catches it.

Usage: python talk/slides/gen_basics_slides.py
"""

from pathlib import Path

from gen_skill_slides import (BG, BORDER, CORE, DARK, GRAY, INK, MONO, MUTED, PAPER, RED, SANS, SERIF,
                              p, section, svg)

SLIDES = Path(__file__).resolve().parent / "slides"
SOFT, TAINT = "#C9C3B5", "#E3B7A6"


def heading(eyebrow, title, below=""):
    return (f'  <div style="display:flex; flex-direction:column; gap:16px">\n'
            f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:{RED}">{eyebrow}</p>\n'
            f'    <h2 style="{SERIF}; font-size:72px; font-weight:600; line-height:1.1; color:{INK}">{title}</h2>\n{below}  </div>')


# ---------- 02 · the basics: four foundations ----------

def setup():
    sub = f'    <p style="{SANS}; font-size:32px; line-height:1.4; color:{DARK}">Obvious one by one. Together, they already create a lot of value.</p>\n'
    L = [heading("02 · The basics", "Four simple foundations.", sub)]
    cards = [
        ("Context", "A coding agent on one always-on machine",
         ["Theory, LaTeX, code and results, all in reach", "Dispatch jobs anywhere; results come back here"]),
        ("Persistence", "Everything under version control",
         ["Not just code: theory, notes, audits, the paper", "Roll back when an agent, or a decision, goes wrong"]),
        ("Reuse", "Prompts become skills",
         ["Loaded only when a task needs them", "Project rules load by default; big skills route", "Plain files: they move with you to any model"]),
        ("Many agents", "Fresh, independent agents",
         ["The one that isn't obvious: next slide"]),
    ]
    W, G, TOP = 398, 24, 420
    for i, (key, what, points) in enumerate(cards):
        left = 128 + i * (W + G)
        last = i == len(cards) - 1
        border = f"2px solid {RED}" if last else f"1px solid {BORDER}"
        bullets = "\n".join(f'    <p style="{SANS}; font-size:24px; line-height:1.4; color:{DARK}">{pt}</p>' for pt in points)
        L.append(f'  <div data-build-in="rise {i + 1}" style="position:absolute; top:{TOP}px; left:{left}px; width:{W}px; height:440px; '
                 f'display:flex; flex-direction:column; gap:14px; padding:32px; background:{PAPER}; border:{border}; border-radius:16px">\n'
                 f'    <p style="{SANS}; font-size:24px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{RED}">{key}</p>\n'
                 f'    <h3 style="{SERIF}; font-size:34px; font-weight:600; line-height:1.2; color:{INK}">{what}</h3>\n{bullets}\n  </div>')
    notes = ("The first part of the answer is basic. Before we can look for any gem, we have to solve a simpler problem: context. "
             "So first, a coding agent, running on one central, always-on machine. Then the theory, the LaTeX, the code, the results and "
             "the figures are all in context, and you stop uploading things back and forth. Agents can work overnight, and even if you "
             "dispatch jobs elsewhere, the results come back to that one place. "
             "Second, persistence: put everything under version control. Not just the code, which most of us already do, but the theory, "
             "the notes, the audits, the paper. When you give agents freedom, things go wrong, or you change your mind, or you want a big "
             "refactor, and you can always roll back. "
             "Third, reuse. If you type the same prompt again and again, turn it into a skill, which the agent loads only when it needs it. "
             "What a project always needs goes in a default file, AGENTS.md or CLAUDE.md, and a large skill can route to parts loaded on "
             "demand. And unlike a chat's memory, these are plain files, so they move with you to another model. "
             "Each of these is obvious on its own, but together they already create a lot of value. "
             "The fourth one is less obvious: many agents. It deserves its own slide.")
    return section("setup", "\n".join(L), notes)


# ---------- 03 · many agents ----------

def dot(x, y, fill, stroke=None, r=17):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{st}/>'


def agents():
    chip = f'padding:6px 20px; {MONO}; font-size:28px; color:{RED}; background:{CORE}; border-radius:8px'
    below = (f'    <div style="display:flex; flex-direction:row; flex-wrap:wrap; align-items:center; gap:12px">\n'
             f'      <p style="{SANS}; font-size:24px; color:{MUTED}">Built into</p>\n'
             f'      <p style="{chip}">formulate-problem</p>\n      <p style="{chip}">develop-project</p>\n    </div>\n')
    L = [heading("03 · Many agents", "Many agents beat one long thread.", below)]
    L.append(p(128, 350, 1664, "Not for speed: same tokens, same rate limits. Ask ten people once, not one person ten times.", 32, DARK))
    PT, PW, PH = 432, 816, 494
    # left panel: one long thread
    L.append(f'  <div data-build-in="rise 1" style="position:absolute; top:{PT}px; left:128px; width:{PW}px; height:{PH}px; '
             f'background:{PAPER}; border:1px solid {BORDER}; border-radius:16px"></div>')
    L.append(p(168, PT + 40, 600, "One long thread", 24, MUTED, 600, build="rise 1", extra="; letter-spacing:3px; text-transform:uppercase"))
    SX, SY, SW, SH = 168, PT + 100, 736, 120
    xs = [24 + 58 * k for k in range(12)]
    L.append(svg(SX, SY, SW, SH, f'<line x1="4" y1="60" x2="{SW - 4}" y2="60" stroke="{GRAY}" stroke-width="3"/>' +
                 "".join(dot(x, 60, SOFT) for x in xs[:2]), "A single thread: the first steps.", "rise 1"))
    L.append(svg(SX, SY, SW, SH, dot(xs[2], 60, RED), "The third step is a mistake.", "fade 2"))
    L.append(p(SX, SY + 96, 300, "one mistake", 24, RED, build="fade 2"))
    L.append(svg(SX, SY, SW, SH, "".join(dot(x, 60, TAINT) for x in xs[3:]), "Every later step inherits the mistake.", "fade 3"))
    L.append(p(SX + SW - 420, SY + 96, 420, "…and it never recovers", 24, MUTED, align="right", build="fade 3"))
    L.append(p(168, PT + 400, PW - 80, "Everything piles up in one context. Once something goes wrong, everything after it inherits the mistake.",
               24, DARK, build="fade 3", extra="; line-height:1.4"))
    # right panel: fresh agents, shown one branch at a time; three miss, one catches the flaw
    RX = 976
    L.append(f'  <div data-build-in="rise 4" style="position:absolute; top:{PT}px; left:{RX}px; width:{PW}px; height:{PH}px; '
             f'background:{PAPER}; border:2px solid {RED}; border-radius:16px"></div>')
    L.append(p(RX + 40, PT + 40, 600, "Many fresh agents", 24, RED, 600, build="rise 4", extra="; letter-spacing:3px; text-transform:uppercase"))
    TX, TY, TW, TH = RX + 40, PT + 80, 736, 270
    root, R = (368, 20), 15
    cols = [92, 276, 460, 644]
    lv = [80, 140, 200]
    # per branch: (level, x offset, parent's x offset); branches explore and split on their own
    tree = [
        [(0, 0, 0), (1, 0, 0), (2, 0, 0)],
        [(0, 0, 0), (1, 0, 0), (2, -34, 0), (2, 34, 0)],
        [(0, 0, 0), (1, -30, 0), (1, 30, 0), (2, 30, 30)],
        [(0, 0, 0), (1, 0, 0)],
    ]
    CAUGHT = (2, 2, 30)
    L.append(svg(TX, TY, TW, TH, f'<circle cx="{root[0]}" cy="{root[1]}" r="20" fill="{INK}"/>', "The main agent.", "rise 4"))
    labels = ["missed", "missed", "caught it", "missed"]
    for b, nodes in enumerate(tree):
        art = ""
        for level, dx, pdx in nodes:
            x, y = cols[b] + dx, lv[level]
            px, py = (cols[b] + pdx, lv[level - 1] + R) if level else (root[0], root[1] + 20)
            caught = (b, level, dx) == CAUGHT
            on_path = b == CAUGHT[0] and (dx == CAUGHT[2] or level == 0)
            art += f'<line x1="{px}" y1="{py}" x2="{x}" y2="{y - R}" stroke="{RED if on_path else SOFT}" stroke-width="3"/>'
            if caught:
                art += dot(x, y, RED, r=R + 3) + (f'<polyline points="{x - 8},{y} {x - 2},{y + 6} {x + 9},{y - 7}" fill="none" '
                                                  f'stroke="{PAPER}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                art += dot(x, y, PAPER, GRAY, R)
        step = 5 + b
        L.append(svg(TX, TY, TW, TH, art, f"Fresh agent {b + 1} explores its own branch and {labels[b]} the flaw.", f"fade {step}"))
        L.append(p(TX + cols[b] - 90, TY + TH - 16, 180, labels[b], 24, RED if b == 2 else MUTED, 600 if b == 2 else 400, "center",
                   build=f"fade {step}"))
    L.append(p(RX + 40, PT + 400, PW - 80, "Each starts clean and sees only its own folder. Several can miss; one catch is enough.",
               24, DARK, build="fade 8", extra="; line-height:1.4"))
    notes = ("Many agents deserve their own slide, because here's one conceptual point I think many people still underestimate: "
             "multiple agents are fundamentally more powerful than one long thread. Not because they're faster. You pay for the tokens "
             "either way, and you're rate-limited. The difference is conceptual. "
             "A single thread accumulates everything: every dead end, every earlier claim, every sentiment, enthusiasm or pessimism. "
             "Once it makes an early mistake, "
             "everything after it is anchored to it, and telling it to be unbiased can't undo that. It doesn't know how. "
             "Separate agents get a clean, independent start, especially if you isolate them and decide mechanically what they see. "
             "Each one explores its own branch, and a branch can split when it finds something worth following. "
             "Run four agents, ideally prompted for diversity. The first one misses the flaw. So does the second. "
             "The third catches it. The fourth misses again. And that's still a success: one catch is all you need. "
             "It's asking ten people instead of asking one person ten times. Most of the skills in this repo build on this. "
             "Let me show you how they fit together.")
    return section("agents", "\n".join(L), notes)


def main():
    for sid, make in (("setup", setup), ("agents", agents)):
        (SLIDES / f"{sid}.html").write_text(make())
        print(f"wrote {sid}.html")


if __name__ == "__main__":
    main()

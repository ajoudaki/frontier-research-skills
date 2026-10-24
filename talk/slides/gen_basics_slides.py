"""Generate talk/slides/slides/{setup,agents}.html: the four foundations, and why many agents.

setup: four cards (context, persistence, reuse, many agents), one per step.
agents: one long thread builds block by block until a mistake taints the rest;
then fresh agents branch out and explore in parallel, and one catches the flaw.

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

def block(x, y, fill, stroke=None, s=34):
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    return f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" rx="6" fill="{fill}"{st}/>'


def agents():
    chip = f'padding:6px 20px; {MONO}; font-size:28px; color:{RED}; background:{CORE}; border-radius:8px'
    below = (f'    <div style="display:flex; flex-direction:row; flex-wrap:wrap; align-items:center; gap:12px">\n'
             f'      <p style="{SANS}; font-size:24px; color:{MUTED}">Built into</p>\n'
             f'      <p style="{chip}">formulate-problem</p>\n      <p style="{chip}">develop-project</p>\n    </div>\n')
    L = [heading("03 · Many agents", "Many agents beat one long thread.", below)]
    L.append(p(128, 350, 1664, "Not for speed: same tokens, same rate limits. Ask ten people once, not one person ten times.", 32, DARK))
    PT, PW, PH = 432, 816, 470
    # left panel: one long thread
    L.append(f'  <div data-build-in="rise 1" style="position:absolute; top:{PT}px; left:128px; width:{PW}px; height:{PH}px; '
             f'background:{PAPER}; border:1px solid {BORDER}; border-radius:16px"></div>')
    L.append(p(168, PT + 40, 600, "One long thread", 24, MUTED, 600, build="rise 1", extra="; letter-spacing:3px; text-transform:uppercase"))
    SX, SY, SW, SH = 168, PT + 100, 736, 120
    xs = [24 + 58 * k for k in range(12)]
    L.append(svg(SX, SY, SW, SH, f'<line x1="4" y1="60" x2="{SW - 4}" y2="60" stroke="{GRAY}" stroke-width="3"/>' +
                 "".join(block(x, 60, SOFT) for x in xs[:2]), "A single thread: the first steps.", "rise 1"))
    L.append(svg(SX, SY, SW, SH, block(xs[2], 60, RED), "The third step is a mistake.", "fade 2"))
    L.append(p(SX, SY + 96, 300, "one mistake", 24, RED, build="fade 2"))
    L.append(svg(SX, SY, SW, SH, "".join(block(x, 60, TAINT) for x in xs[3:]), "Every later step inherits the mistake.", "fade 3"))
    L.append(p(SX + SW - 420, SY + 96, 420, "…and it never recovers", 24, MUTED, align="right", build="fade 3"))
    L.append(p(168, PT + 330, PW - 80, "Everything piles up in one context. Once something goes wrong, everything after it inherits the mistake.",
               24, DARK, build="fade 3", extra="; line-height:1.4"))
    # right panel: fresh agents branch out and explore in parallel
    RX = 976
    L.append(f'  <div data-build-in="rise 4" style="position:absolute; top:{PT}px; left:{RX}px; width:{PW}px; height:{PH}px; '
             f'background:{PAPER}; border:2px solid {RED}; border-radius:16px"></div>')
    L.append(p(RX + 40, PT + 40, 600, "Many fresh agents", 24, RED, 600, build="rise 4", extra="; letter-spacing:3px; text-transform:uppercase"))
    TX, TY, TW, TH = RX + 40, PT + 84, 736, 250
    root = (368, 22)
    cols = [92, 276, 460, 644]
    lv = [80, 140, 200]
    # (branch, level, x offset): every branch grows in parallel; branch 2 splits at the third level
    tree = {0: [(0, 0), (1, 0), (2, 0)], 1: [(0, 0), (1, 0), (2, -40), (2, 40)], 2: [(0, 0), (1, 0), (2, 0)], 3: [(0, 0), (1, 0)]}

    def pos(b, level, dx):
        return cols[b] + dx, lv[level]

    stage = {0: "", 1: "", 2: ""}
    for b, nodes in tree.items():
        for level, dx in nodes:
            x, y = pos(b, level, dx)
            px, py = pos(b, level - 1, 0) if level else root
            caught = b == 2 and level == 2
            edge_col = RED if caught else SOFT
            stage[level] += f'<line x1="{px}" y1="{py + (17 if level else 20)}" x2="{x}" y2="{y - 17}" stroke="{edge_col}" stroke-width="3"/>'
            if caught:
                stage[level] += block(x, y, RED, s=38) + (f'<polyline points="{x - 10},{y} {x - 3},{y + 8} {x + 11},{y - 8}" fill="none" '
                                                         f'stroke="{PAPER}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                stage[level] += block(x, y, PAPER, GRAY)
    head = f'<circle cx="{root[0]}" cy="{root[1]}" r="20" fill="{INK}"/>'
    L.append(svg(TX, TY, TW, TH, head + stage[0], "A main agent starts four fresh agents.", "rise 4"))
    L.append(svg(TX, TY, TW, TH, stage[1], "Each fresh agent explores its own branch.", "fade 5"))
    L.append(svg(TX, TY, TW, TH, stage[2], "The branches keep growing in parallel; one splits, and one catches the flaw.", "fade 6"))
    for b, label in enumerate(["missed", "missed", "caught it", "missed"]):
        L.append(p(TX + cols[b] - 90, TY + 226, 180, label, 24, RED if b == 2 else MUTED, 600 if b == 2 else 400, "center", build="fade 6"))
    L.append(p(RX + 40, PT + 380, PW - 80, "Each starts clean and sees only its own folder. Their errors are independent, so it only takes one to catch the flaw.",
               24, DARK, build="fade 6", extra="; line-height:1.4"))
    notes = ("Many agents deserve their own slide, because here's one conceptual point I think many people still underestimate: "
             "multiple agents are fundamentally more powerful than one long thread. Not because they're faster. You pay for the tokens "
             "either way, and you're rate-limited. The difference is conceptual. "
             "A single thread accumulates everything: every dead end, every earlier claim, every sentiment, enthusiasm or pessimism. "
             "Once it makes an early mistake, "
             "everything after it is anchored to it, and telling it to be unbiased can't undo that. It doesn't know how. "
             "Separate agents get a clean, independent start, especially if you isolate them and decide mechanically what they see. "
             "Each one explores its own branch, in parallel, and a branch can split when it finds something worth following. "
             "Run four agents, ideally prompted for diversity, and three may miss a flaw while the fourth catches it. "
             "It's asking ten people instead of asking one person ten times. Most of the skills in this repo build on this. "
             "Let me show you how they fit together.")
    return section("agents", "\n".join(L), notes)


def main():
    for sid, make in (("setup", setup), ("agents", agents)):
        (SLIDES / f"{sid}.html").write_text(make())
        print(f"wrote {sid}.html")


if __name__ == "__main__":
    main()

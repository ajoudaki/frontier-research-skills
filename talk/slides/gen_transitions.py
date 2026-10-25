"""Generate the interlude slides: each closing question on its own unnumbered slide, between the two
slides it connects. (The interlude after the strategy slide, with the magnified push, is written by
gen_gem_slide.py; run it before this one.)

Usage: python talk/slides/gen_transitions.py
"""

import json
from pathlib import Path

from gen_bottleneck import haystack
from gen_skill_slides import INK, MUTED, PAPER, RED, SANS, SERIF, arrow, p, section, svg, tick_badge

HERE = Path(__file__).resolve().parent
SLIDES = HERE / "slides"

# (id, comes after, question, notes)
INTERLUDES = [
    ("q-problem", "bottleneck", "How do we find the gem,<br>and stay in control?",
     "So how do we find the gem, and stay in control?"),
    ("q-practice", "agents", "How do we do this in practice?",
     "So how do we do this in practice?"),
    ("q-skills", "foundations", "Everything from here is a skill.",
     "Everything from here is a skill. Here are the five."),
    ("q-solve", "formulate", "Now, how do we solve it?",
     "Now we have a frozen conjecture, and from what we know to it, a dashed arrow: the proof we still need. "
     "Now, how do we solve it?"),
    ("q-understand", "solve", "Solved. Do we understand it?",
     "Solved, most likely: the arrow is solid. But understanding is still the key: to judge the result, and to build on it, "
     "we have to understand it. Do we understand it?"),
    ("q-paper", "teach", "Is it a paper?",
     "So the core grows with results that are true and that we understand. Now we carve out a part of it as a paper. "
     "But is it a paper? Being correct isn't enough: a paper also needs novelty and significance, and it has to stand "
     "against the literature. That needs a different kind of audit."),
    ("q-together", "review", "Putting it all together.",
     "Let's put it all together."),
]


def heading(element):
    """The question is the interlude's title, so mark it up as one."""
    return element.replace("<p", "<h2", 1).replace("</p>", "</h2>")


def thrust(solved):
    """One thrust: an established node and the frozen conjecture, the proof between them dashed, or solid once proved."""
    X0, X1, Y = 660, 1260, 400
    if solved:
        line_ = (f'<line x1="{X0 + 30}" y1="{Y}" x2="{X1 - 52}" y2="{Y}" stroke="{RED}" stroke-width="6"/>'
                 f'<polygon points="{X1 - 38},{Y} {X1 - 60},{Y - 13} {X1 - 60},{Y + 13}" fill="{RED}"/>'
                 + tick_badge((X0 + X1) / 2, Y, RED, 22))
        q = (X1, Y - 70)          # the open question is now about the result itself
    else:
        line_ = (f'<line x1="{X0 + 30}" y1="{Y}" x2="{X1 - 52}" y2="{Y}" stroke="{INK}" stroke-width="4" stroke-dasharray="12 9"/>'
                 f'<polygon points="{X1 - 38},{Y} {X1 - 58},{Y - 11} {X1 - 58},{Y + 11}" fill="{INK}"/>')
        q = ((X0 + X1) / 2, Y - 34)
    art = (line_ + f'<circle cx="{X0}" cy="{Y}" r="24" fill="{RED}"/>'
           + f'<circle cx="{X1}" cy="{Y}" r="34" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
           + f'<text x="{q[0]}" y="{q[1]}" text-anchor="middle" font-family="Source Serif 4, Georgia, serif" font-size="72" '
             f'font-weight="600" fill="{RED}">?</text>')
    label = "The thrust, proved: a solid arrow with a tick, and a question mark over the result." if solved else \
        "The thrust: an established node, a dashed arrow with a question mark, and the frozen conjecture."
    return [svg(0, 0, 1920, 1080, art, label),
            p(X0 - 160, 450, 320, "established", 26, RED, 600, "center"),
            p(X1 - 160, 460, 320, "frozen conjecture", 26, INK, 600, "center")]


def schematic():
    """The whole project in one static picture: thrusts, the established core and the carved-out gem."""
    snap = json.loads((HERE / "gem_snapshot.json").read_text())
    vx, vy, vw, vh = snap["viewBox"]
    W = 860
    H = round(vh * W / vw)
    return svg(960 - W / 2, 170, W, H, snap["svg"], "The project at a glance: thrusts, the established core, and the gem carved out of it.") \
        .replace(f'viewBox="0 0 {W} {H}"', f'viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}"')


def interlude(sid, question, notes):
    if sid == "q-problem":
        # keep the gem in the haystack above the two questions
        hay = haystack()
        hay = hay.replace(' data-build-in="fade 4"', "").replace(
            "style=\"position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px\"",
            "style=\"position:absolute; top:250px; left:780px; width:360px; height:467px\"")
        body = [hay, heading(p(128, 770, 1664, question, 56, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    elif sid in ("q-solve", "q-understand"):
        body = thrust(sid == "q-understand") + [
            heading(p(128, 620, 1664, question, 64, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    elif sid == "q-paper":
        body = [schematic(), heading(p(128, 840, 1664, question, 64, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    else:
        body = [f'  <div style="position:absolute; top:440px; left:920px; width:80px; height:4px; background:{RED}"></div>',
                heading(p(128, 480, 1664, question, 72, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    return section(sid, "\n".join(body), notes)


def main():
    deck_path = HERE / "deck.json"
    deck = json.loads(deck_path.read_text())
    order = [s for s in deck["order"] if not s.startswith("q-")]
    for sid, after, question, notes in INTERLUDES:
        (SLIDES / f"{sid}.html").write_text(interlude(sid, question, notes))
    # each interlude right after the slide it closes; the frontier interlude follows the strategy slide
    after_of = {sid: after for sid, after, _, _ in INTERLUDES}
    after_of["q-frontier"] = "strategy"
    for sid, after in after_of.items():
        order.insert(order.index(after) + 1, sid)
    deck["order"] = order
    deck_path.write_text(json.dumps(deck, indent=2) + "\n")
    print("order:", order)


if __name__ == "__main__":
    main()

"""Generate the interlude slides: each closing question on its own unnumbered slide, between the two
slides it connects. (The interlude after the strategy slide, with the magnified push, is written by
gen_gem_slide.py; run it before this one.)

Usage: python talk/slides/gen_transitions.py
"""

import json
from pathlib import Path

from gen_bottleneck import haystack
from gen_skill_slides import INK, RED, SERIF, p, section

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
     "Now, how do we solve it?"),
    ("q-understand", "solve", "Solved. Do we understand it?",
     "Solved, most likely. But we still have to judge it, and to judge it, we have to understand it."),
    ("q-paper", "teach", "Is it a paper?",
     "We can judge what joins the core now. But is it a paper?"),
    ("q-together", "review", "Putting it all together.",
     "Let's put it all together."),
]


def heading(element):
    """The question is the interlude's title, so mark it up as one."""
    return element.replace("<p", "<h2", 1).replace("</p>", "</h2>")


def interlude(sid, question, notes):
    if sid == "q-problem":
        # keep the gem in the haystack above the two questions
        hay = haystack()
        hay = hay.replace(' data-build-in="fade 4"', "").replace(
            "style=\"position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px\"",
            "style=\"position:absolute; top:250px; left:780px; width:360px; height:467px\"")
        body = [hay, heading(p(128, 770, 1664, question, 56, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
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

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
    ("q-problem", "bottleneck",
     f'How do we raise the <span style="color:{RED}">signal-to-noise</span> ratio?<br>And how do we stay in control?',
     "So we have two questions. How do we raise the signal-to-noise ratio? And how do we stay in control?"),
    ("q-practice", "agents", "How do we implement all this in practice?",
     "So how do we implement all this in practice?"),
    ("q-skills", "foundations", "In fact, everything we'll talk about from here is a skill.<br>Here are the five.",
     "In fact, everything we'll talk about from here is a skill. Here are the five."),
    ("q-thrust", "develop", "But each thrust is still open:<br>what exactly is its question, and how do we solve it?",
     "What exactly is its question? And how do we solve it? Let's take one thrust."),
    ("q-solve", "formulate", "The target is sharp now.<br>But the arrow is still dashed: how do we solve it?",
     "But the arrow is still dashed: nothing is proved yet. How do we solve it?"),
    ("q-understand", "solve", "Solved, most likely.<br>But to judge it, we still have to understand it.",
     "We've delegated as much as we could, but we still have to stay in charge: someone has to judge whether it's relevant, "
     "whether it's the right direction, and whether an assumption or technique was quietly tweaked along the way. That means "
     "reading it, and agent output can be very hard to read. That's the third stage."),
    ("q-paper", "teach", "Now we can judge what joins the core.<br>But a paper needs more: novelty, significance, the literature.",
     "Now we can judge what joins the core. But is that a paper? A paper needs more: novelty, significance, the literature."),
    ("q-together", "review", "Now let's put it all together.",
     "Now let's put it all together."),
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
        body = [f'  <div style="position:absolute; top:420px; left:920px; width:80px; height:4px; background:{RED}"></div>',
                heading(p(128, 460, 1664, question, 60, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
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

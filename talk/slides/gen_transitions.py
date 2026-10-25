"""Generate the interlude slides: each closing question on its own unnumbered slide, between the two
slides it connects. (The interlude after the strategy slide, with the magnified push, is written by
gen_gem_slide.py; run it before this one.)

Usage: python talk/slides/gen_transitions.py
"""

import json
import re
from pathlib import Path

from gen_bottleneck import haystack
from gen_skill_slides import INK, MUTED, PAPER, RED, SANS, SERIF, arrow, p, section, svg, tick_badge

HERE = Path(__file__).resolve().parent
SLIDES = HERE / "slides"

# (id, comes after, question, notes)
INTERLUDES = [
    ("q-problem", "bottleneck", "How do we find the gem?",
     "So how do we find the gem?"),
    ("q-practice", "agents", "How do we do this in practice?",
     "So how do we do this in practice?"),
    ("q-skills", "foundations", "Everything from here is a skill.",
     "Everything from here is a skill. Here are the five."),
    ("q-formulate", "develop", "First, what exactly is the question?",
     "Here's one thrust: from something we already know to the next result. But look at the target: it isn't a sharp "
     "question at all. It's vague, with fuzzy boundaries, and an agent will happily answer an easier one. "
     "So first: what exactly is the question?"),
    ("q-solve", "formulate", "Now, how do we solve it?",
     "Now we have a frozen conjecture, and from what we know to it, a dashed arrow: the proof we still need. "
     "Now, how do we solve it?"),
    ("q-understand", "solve", "Solved. Do we understand it?",
     "Solved, most likely: the arrow is solid. But understanding is still the key: to judge the result, and to build on it, "
     "we have to understand it. Do we understand it?"),
    ("q-paper", "teach", "Carved out of the core: is it a paper?",
     "So far, results enter the core when they're correct, coherent and relevant. Now we take one compact part of "
     "the core, the part that tells a story, and carve it out as a paper. But correct isn't enough for a paper: it also "
     "needs novelty and significance, and it has to stand against the literature. Is it a paper?"),
    ("q-together", "review", "Putting it all together.",
     "Let's put it all together."),
]


def heading(element):
    """The question is the interlude's title, so mark it up as one."""
    return element.replace("<p", "<h2", 1).replace("</p>", "</h2>")


def thrust(state):
    """One thrust, from an established node to its target, in three states:
    "vague" (the target itself is unclear), "open" (a frozen conjecture, the proof still dashed), "solved"."""
    X0, X1, Y = 660, 1260, 400
    dashed = f'stroke="{INK}" stroke-width="4" stroke-dasharray="12 9"'
    if state == "solved":
        line_ = (f'<line x1="{X0 + 30}" y1="{Y}" x2="{X1 - 52}" y2="{Y}" stroke="{RED}" stroke-width="6"/>'
                 f'<polygon points="{X1 - 38},{Y} {X1 - 60},{Y - 13} {X1 - 60},{Y + 13}" fill="{RED}"/>'
                 + tick_badge((X0 + X1) / 2, Y, RED, 22))
    else:
        line_ = (f'<line x1="{X0 + 30}" y1="{Y}" x2="{X1 - 52}" y2="{Y}" {dashed}/>'
                 f'<polygon points="{X1 - 38},{Y} {X1 - 58},{Y - 11} {X1 - 58},{Y + 11}" fill="{INK}"/>')
    if state == "vague":
        target = f'<circle cx="{X1}" cy="{Y}" r="34" fill="{PAPER}" stroke="{INK}" stroke-width="5" stroke-dasharray="9 7"/>'
    else:
        target = f'<circle cx="{X1}" cy="{Y}" r="34" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
    q = (X1, Y - 70) if state in ("vague", "solved") else ((X0 + X1) / 2, Y - 34)
    art = (line_ + f'<circle cx="{X0}" cy="{Y}" r="24" fill="{RED}"/>' + target
           + f'<text x="{q[0]}" y="{q[1]}" text-anchor="middle" font-family="Source Serif 4, Georgia, serif" font-size="72" '
             f'font-weight="600" fill="{RED}">?</text>')
    label = {"vague": "The thrust: an established node, a dashed arrow, and a dashed target with a question mark: the question itself is unclear.",
             "open": "The thrust: an established node, a dashed arrow with a question mark, and the frozen conjecture.",
             "solved": "The thrust, proved: a solid arrow with a tick, and a question mark over the result."}[state]
    target_name = "a vague question" if state == "vague" else "frozen conjecture"
    return [svg(0, 0, 1920, 1080, art, label),
            p(X0 - 160, 450, 320, "established", 26, RED, 600, "center"),
            p(X1 - 160, 460, 320, target_name, 26, INK, 600, "center")]


def bbox(path_d):
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", path_d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def carved():
    """The whole map, faded, with the gem lifted out of the core and shown on its own."""
    snap = json.loads((HERE / "gem_snapshot.json").read_text())
    vx, vy, vw, vh = snap["viewBox"]
    W = 760
    H = round(vh * W / vw)
    X, Y = 200, 200
    k = W / vw
    gx0, gy0, gx1, gy1 = bbox(re.search(r'd="([^"]+)"', snap["gem"]).group(1))
    m = 14
    gx0, gy0, gx1, gy1 = gx0 - m, gy0 - m, gx1 + m, gy1 + m
    GS = 2.1                               # the carved piece, enlarged
    GW, GH = round((gx1 - gx0) * k * GS), round((gy1 - gy0) * k * GS)
    GX, GY = 1240, round(Y + H / 2 - GH / 2)
    sx, sy = X + ((gx0 + gx1) / 2 - vx) * k, Y + ((gy0 + gy1) / 2 - vy) * k   # the gem on the map
    return [svg(X, Y, W, H, f'<g opacity="0.45">{snap["base"]}</g>{snap["gem"]}',
                "The whole map, faded, with the gem still in place inside the core.")
            .replace(f'viewBox="0 0 {W} {H}"', f'viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}"'),
            svg(GX, GY, GW, GH, snap["gem"], "The gem, carved out of the core and shown on its own.")
            .replace(f'viewBox="0 0 {GW} {GH}"', f'viewBox="{gx0:.1f} {gy0:.1f} {gx1 - gx0:.1f} {gy1 - gy0:.1f}"'),
            svg(0, 0, 1920, 1080, arrow(sx + (gx1 - gx0) * k / 2 + 6, sy, GX - 30, GY + GH / 2, "#2F6FC9", 4, "10 8"),
                "An arrow from the gem in the core to the carved-out piece.")]


def interlude(sid, question, notes):
    if sid == "q-problem":
        # keep the gem in the haystack above the two questions
        hay = haystack()
        hay = hay.replace(' data-build-in="fade 4"', "").replace(
            "style=\"position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px\"",
            "style=\"position:absolute; top:250px; left:780px; width:360px; height:467px\"")
        body = [hay, heading(p(128, 770, 1664, question, 56, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    elif sid in ("q-formulate", "q-solve", "q-understand"):
        state = {"q-formulate": "vague", "q-solve": "open", "q-understand": "solved"}[sid]
        body = thrust(state) + [
            heading(p(128, 620, 1664, question, 64, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    elif sid == "q-paper":
        body = carved() + [heading(p(128, 820, 1664, question, 64, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    else:
        body = [f'  <div style="position:absolute; top:440px; left:920px; width:80px; height:4px; background:{RED}"></div>',
                heading(p(128, 480, 1664, question, 72, INK, 600, "center", family=SERIF, extra="; line-height:1.3"))]
    return section(sid, "\n".join(body), notes)


COVER_NOTES = (
    "Hi everyone, I'm Amir. Today's models are smart enough to do real research, but using them on open questions is "
    "surprisingly hard: they produce far more than we can check, and their mistakes are silent. What comes out is a "
    "haystack, and somewhere in it there may be a gem. This talk is about finding that gem: the practical habits I "
    "developed to use these models on open questions without losing control. It isn't a principled framework, just "
    "what worked for me, mostly in theoretical research, and everything is in a repo linked at the end. "
    "Let me start with the problem.")


def cover():
    hay = haystack().replace(' data-build-in="fade 4"', "").replace(
        "style=\"position:absolute; top:0; right:24.55px; width:816.38px; height:880.16px\"",
        "style=\"position:absolute; top:190px; left:1400px; width:400px; height:431px\"")
    return f'''<section id="cover" data-transition="fade" style="display:flex; flex-direction:column; gap:40px; justify-content:center; padding:128px; background:#f6f4ef">
  <h1 style="font-family:'Source Serif 4', Georgia, serif; font-size:120px; font-weight:600; line-height:1.05; color:#1b1f2a">Open-ended research<br>with AI agents</h1>
  <p style="font-family:'Source Serif 4', Georgia, serif; font-style:italic; font-size:52px; line-height:1.3; color:#2F6FC9">Finding a gem in a haystack</p>
{hay}
  <div style="position:absolute; bottom:96px; left:128px; width:1664px; display:flex; flex-direction:column; gap:12px">
    <x-shape kind="line" style="width:120px; height:4px; flex:0 0 auto; background:#b04a33"></x-shape>
    <p style="font-family:'IBM Plex Sans', Arial, sans-serif; font-size:48px; font-weight:600; color:#1b1f2a">Amir Joudaki</p>
    <p style="font-family:'IBM Plex Sans', Arial, sans-serif; font-size:32px; color:#b04a33">October 12, 2026</p>
  </div>
  <aside>{COVER_NOTES}</aside>
</section>
'''


def main():
    (SLIDES / "cover.html").write_text(cover())
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

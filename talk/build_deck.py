"""Build talk/deck.html, a self-contained HTML slide deck.

The slides live in talk/slides/slides/<id>.html (one <section> each) and
talk/slides/deck.json gives their order. This script wraps them in a small
presenter: arrow keys or clicks step through the build animations
(data-build-in="<effect> <order>") and the slides.

Usage: python talk/build_deck.py
"""

import json
from pathlib import Path

TALK = Path(__file__).resolve().parent
SLIDES = TALK / "slides"
OUT = TALK / "deck.html"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">
<style>
  html, body { margin: 0; height: 100%; background: #0f1218; overflow: hidden; }
  #stage {
    position: absolute; left: 50%; top: 50%;
    width: 1920px; height: 1080px; transform-origin: 0 0;
  }
  #stage * { margin: 0; padding: 0; box-sizing: border-box; }
  #stage section {
    position: absolute; inset: 0; width: 1920px; height: 1080px;
    overflow: hidden; display: flex; flex-direction: column;
    color: #1b1f2a; font-family: 'IBM Plex Sans', Arial, sans-serif;
    opacity: 0; visibility: hidden;
    transition: opacity 450ms ease, visibility 0s linear 450ms;
  }
  #stage section.current {
    opacity: 1; visibility: visible;
    transition: opacity 450ms ease, visibility 0s;
  }
  #stage div { display: flex; flex-direction: column; }
  #stage p { font-size: 32px; line-height: 1.4; font-weight: 400; }
  #stage h1 { font-size: 96px; line-height: 1.1; font-weight: 600; }
  #stage h2 { font-size: 64px; line-height: 1.15; font-weight: 600; }
  #stage h3 { font-size: 44px; line-height: 1.2; font-weight: 600; }
  #stage a { color: inherit; text-decoration: underline; }
  #stage svg { flex: none; }
  /* The Slides editor draws one uniform border, so match its look. */
  #stage [style*="border-left:8px"],
  #stage [style*="border-left: 8px"] { border-left: 1px solid #dcd6ca !important; }
  #stage aside { display: none; }
  #stage x-shape { display: block; flex: none; }
  #stage x-shape[kind="arrow-right"] {
    clip-path: polygon(0 30%, 60% 30%, 60% 0, 100% 50%, 60% 100%, 60% 70%, 0 70%);
  }
  #stage [data-build-in] {
    transition: opacity 500ms ease, translate 500ms cubic-bezier(.2, .7, .2, 1);
  }
  #stage [data-build-in].pending { opacity: 0; }
  #stage [data-build-in^="rise"].pending { translate: 0 32px; }
  body.static #stage section,
  body.static #stage [data-build-in] { transition: none !important; }
  #notes {
    position: fixed; left: 0; right: 0; bottom: 0; max-height: 40vh;
    overflow: auto; padding: 16px 24px; display: none;
    background: rgba(15, 18, 24, .92); color: #f6f4ef;
    font: 18px/1.5 'IBM Plex Sans', Arial, sans-serif;
  }
  body.show-notes #notes { display: block; }
  #counter {
    position: fixed; right: 16px; bottom: 12px; display: none;
    color: #8a90a0; font: 14px 'IBM Plex Sans', Arial, sans-serif;
  }
  body.show-notes #counter { display: block; }
</style>
</head>
<body>
<div id="stage">
__SLIDES__
</div>
<div id="notes"></div>
<div id="counter"></div>
<script>
(() => {
  const stage = document.getElementById('stage');
  const slides = [...stage.querySelectorAll(':scope > section')];
  const notes = document.getElementById('notes');
  const counter = document.getElementById('counter');

  // Each slide's steps are the distinct build orders on it, ascending.
  const builds = slides.map(s => [...s.querySelectorAll('[data-build-in]')].map(el => {
    const [effect, order] = el.dataset.buildIn.trim().split(/\\s+/);
    return { el, effect, order: Number(order) || 1 };
  }));
  const steps = builds.map(bs => [...new Set(bs.map(b => b.order))].sort((a, b) => a - b));

  let slide = 0, step = 0;

  function fit() {
    const k = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `scale(${k}) translate(-50%, -50%)`;
  }

  function render() {
    slides.forEach((s, i) => s.classList.toggle('current', i === slide));
    const shown = steps[slide].slice(0, step);
    builds[slide].forEach(b => b.el.classList.toggle('pending', !shown.includes(b.order)));
    const aside = slides[slide].querySelector('aside');
    notes.textContent = aside ? aside.textContent : '';
    counter.textContent = `${slide + 1}/${slides.length} · step ${step}/${steps[slide].length}`;
    history.replaceState(null, '', `#${slide + 1}.${step}`);
  }

  function go(i, k) {
    slide = Math.max(0, Math.min(slides.length - 1, i));
    step = Math.max(0, Math.min(steps[slide].length, k));
    // Hide later slides' builds so they replay when reached.
    builds.forEach((bs, j) => { if (j !== slide) bs.forEach(b => b.el.classList.add('pending')); });
    render();
  }

  function next() {
    if (step < steps[slide].length) go(slide, step + 1);
    else if (slide < slides.length - 1) go(slide + 1, 0);
  }

  function prev() {
    if (step > 0) go(slide, step - 1);
    else if (slide > 0) go(slide - 1, steps[slide - 1].length);
  }

  addEventListener('keydown', e => {
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') go(0, 0);
    else if (e.key === 'End') go(slides.length - 1, steps[slides.length - 1].length);
    else if (e.key === 'n' || e.key === 'N') document.body.classList.toggle('show-notes');
    else if (e.key === 'f' || e.key === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }
  });
  addEventListener('click', e => { if (!e.target.closest('a')) next(); });
  addEventListener('resize', fit);

  // For rendering: deck.html?static#<slide>.<step> shows that state with no animation.
  if (new URLSearchParams(location.search).has('static')) document.body.classList.add('static');
  window.deck = { go, steps, count: slides.length };

  const m = location.hash.match(/^#(\\d+)(?:\\.(\\d+))?$/);
  fit();
  go(m ? Number(m[1]) - 1 : 0, m && m[2] ? Number(m[2]) : 0);
})();
</script>
</body>
</html>
"""


def main():
    deck = json.loads((SLIDES / "deck.json").read_text())
    sections = [(SLIDES / "slides" / f"{sid}.html").read_text().strip() for sid in deck["order"]]
    html = TEMPLATE.replace("__TITLE__", "Open-ended research with AI agents")
    html = html.replace("__SLIDES__", "\n".join(sections))
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(sections)} slides)")


if __name__ == "__main__":
    main()

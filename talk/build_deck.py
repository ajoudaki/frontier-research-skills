"""Build talk/deck.html, a self-contained HTML slide deck.

The slides live in talk/slides/slides/<id>.html (one <section> each) and
talk/slides/deck.json gives their order. This script wraps them in a small
presenter: arrow keys or clicks step through the build animations
(data-build-in="<effect> <order>") and the slides. N toggles the speaker
notes over the slide; P opens a presenter window (slide, next build, notes,
timer) that stays in sync with the deck. F toggles fullscreen.

Usage: python talk/build_deck.py
"""

import html
import json
import re
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
  /* Presenter view (deck.html?presenter, opened with P): the slide on the
     left, the next build and the notes on the right, synced with the deck. */
  #preview { display: none; }
  body.presenter #preview {
    display: block; position: fixed; top: 24px; right: 24px; border: 0;
    width: calc(34vw - 48px); aspect-ratio: 16 / 9; pointer-events: none;
    outline: 1px solid #3a4050;
  }
  body.presenter #preview-label {
    display: block; position: fixed; right: 32px; top: 30px;
    color: #8a90a0; font: 14px 'IBM Plex Sans', Arial, sans-serif; z-index: 1;
  }
  #preview-label { display: none; }
  body.presenter #notes {
    display: block; left: auto; right: 0; bottom: 0; width: 34vw;
    top: calc((34vw - 48px) * 9 / 16 + 48px); max-height: none;
    padding: 0 28px 28px 24px; box-sizing: border-box;
    background: none; font-size: 22px; line-height: 1.55;
  }
  body.presenter #counter {
    display: block; left: 24px; right: auto; bottom: 20px; font-size: 22px;
  }
</style>
</head>
<body>
<div id="stage">
__SLIDES__
</div>
<div id="notes"></div>
<div id="counter"></div>
<div id="preview-label">next</div>
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
  const params = new URLSearchParams(location.search);
  const presenter = params.has('presenter');
  const started = Date.now();
  let peer = presenter ? window.opener : null, preview = null;
  let channel = null;
  const follower = params.has('preview') || params.has('static');
  if (!follower) try { channel = new BroadcastChannel('deck'); } catch (e) {}

  function nextState() {
    if (step < steps[slide].length) return [slide, step + 1];
    if (slide < slides.length - 1) return [slide + 1, 0];
    return null;
  }

  function clock() {
    const t = Math.floor((Date.now() - started) / 1000);
    return `${Math.floor(t / 60)}:${String(t % 60).padStart(2, '0')}`;
  }

  function fit() {
    if (presenter) {
      const k = Math.min((innerWidth * 0.66 - 48) / 1920, (innerHeight - 96) / 1080);
      stage.style.left = stage.style.top = '24px';
      stage.style.transform = `scale(${k})`;
      return;
    }
    const k = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `scale(${k}) translate(-50%, -50%)`;
  }

  function render() {
    slides.forEach((s, i) => s.classList.toggle('current', i === slide));
    const shown = steps[slide].slice(0, step);
    builds[slide].forEach(b => b.el.classList.toggle('pending', !shown.includes(b.order)));
    // The notes for the current step: the last part that starts at or before it.
    const aside = slides[slide].querySelector('aside');
    const parts = aside ? [...aside.querySelectorAll('[data-step]')] : [];
    const part = parts.filter(d => Number(d.dataset.step) <= step).pop();
    notes.textContent = part ? part.textContent : (aside ? aside.textContent : '');
    counter.textContent = `${slide + 1}/${slides.length} · step ${step}/${steps[slide].length}`
      + (presenter ? ` · ${clock()}` : '');
    // Sandboxed viewers (e.g. an embedded srcdoc frame) refuse URL changes; the deck works without them.
    try { history.replaceState(null, '', `#${slide + 1}.${step}`); } catch (e) {}
    if (preview) {
      const n = nextState();
      preview.style.visibility = n ? 'visible' : 'hidden';
      if (n) preview.contentWindow.postMessage({ deck: n }, '*');
    }
  }

  // Keep the deck and its presenter window on the same slide and step.
  function share() {
    if (follower) return;
    const msg = { deck: [slide, step] };
    if (peer && !peer.closed) peer.postMessage(msg, '*');
    if (channel) channel.postMessage(msg);
  }

  function receive(data) {
    if (!data || !Array.isArray(data.deck)) return;
    const [i, k] = data.deck;
    if (i !== slide || k !== step) go(i, k, false);
  }

  addEventListener('message', e => {
    if (!presenter && e.source && e.source !== window && e.source !== window.parent) peer = e.source;
    receive(e.data);
  });
  if (channel) channel.onmessage = e => receive(e.data);

  function go(i, k, broadcast = true) {
    slide = Math.max(0, Math.min(slides.length - 1, i));
    step = Math.max(0, Math.min(steps[slide].length, k));
    // Hide later slides' builds so they replay when reached.
    builds.forEach((bs, j) => { if (j !== slide) bs.forEach(b => b.el.classList.add('pending')); });
    render();
    if (broadcast) share();
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
    else if ((e.key === 'p' || e.key === 'P') && !presenter) {
      peer = window.open(`${location.pathname}?presenter${location.hash}`, 'deck-presenter',
                         'width=1440,height=900');
    }
    else if (e.key === 'f' || e.key === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }
  });
  addEventListener('click', e => {
    if (e.target.closest('a') || (presenter && !e.target.closest('#stage'))) return;
    next();
  });
  addEventListener('resize', fit);

  // For rendering: deck.html?static#<slide>.<step> shows that state with no animation.
  if (params.has('static')) document.body.classList.add('static');
  if (presenter) {
    document.body.classList.add('presenter');
    document.title = `Presenter · ${document.title}`;
    preview = document.createElement('iframe');
    preview.id = 'preview';
    const n = nextState() || [slide, step];
    preview.src = `${location.pathname}?static&preview#${n[0] + 1}.${n[1]}`;
    preview.addEventListener('load', render);
    document.body.appendChild(preview);
    setInterval(render, 1000);
  }
  window.deck = { go, steps, count: slides.length };

  const m = location.hash.match(/^#(\\d+)(?:\\.(\\d+))?$/);
  fit();
  go(m ? Number(m[1]) - 1 : 0, m && m[2] ? Number(m[2]) : 0);
})();
</script>
</body>
</html>
"""


def note_parts(text, anchors):
    """Split a slide's notes where each build step's anchor phrase begins: [(step, text)]."""
    cuts, pos = [], 0
    for step, phrase in anchors:
        i = text.find(phrase, pos)
        if i < 0:
            raise SystemExit(f"anchor {phrase!r} not found after position {pos}")
        cuts.append((step, i))
        pos = i + len(phrase)
    bounds = [(0, 0)] + cuts + [(None, len(text))]
    parts = [(bounds[k][0], text[bounds[k][1]:bounds[k + 1][1]].strip()) for k in range(len(bounds) - 1)]
    return [(st, t) for st, t in parts if t]


def split_notes(section, anchors):
    """Rewrite the slide's <aside> as one block per build step; return the section and its parts."""
    m = re.search(r"(<aside[^>]*>)(.*?)(</aside>)", section, re.S)
    if not m:
        return section, []
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2)))).strip()
    parts = note_parts(text, anchors) if anchors else [(0, text)]
    inner = "".join(f'<div data-step="{st}">{html.escape(t)}</div>' for st, t in parts)
    return section[:m.start()] + m.group(1) + inner + m.group(3) + section[m.end():], parts


def write_notes(deck, sections, all_parts):
    """speaker-notes.md: each slide's notes, split at the clicks that bring in each build step."""
    out = ["# Research with AI Agents: speaker notes", "",
           "Each slide's notes are split by build step: **[k]** is what to say once click k has brought "
           "in its part; **[k–m]** covers several clicks.", ""]
    for i, (sid, sec, parts) in enumerate(zip(deck["order"], sections, all_parts), 1):
        m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", sec, re.S)
        title = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()) if m else sid
        out.append(f"## {i}. {'→ ' if sid.startswith('q-') else ''}{title}")
        steps = sorted({int(o) for o in re.findall(r'data-build-in="\S+ (\d+)"', sec)})
        n = len(steps)
        for k, (st, t) in enumerate(parts):
            end = (parts[k + 1][0] - 1) if k + 1 < len(parts) else n
            if len(parts) == 1 and st == 0:
                out.append(t)
            else:
                label = f"{st}" if end <= st else f"{st}–{end}"
                out.append(f"**[{label}]** {t}")
            out.append("")
    (TALK / "speaker-notes.md").write_text("\n".join(out))


def main():
    deck = json.loads((SLIDES / "deck.json").read_text())
    sections = [(SLIDES / "slides" / f"{sid}.html").read_text().strip() for sid in deck["order"]]
    anchors = json.loads((SLIDES / "note_steps.json").read_text())
    split = [split_notes(sec, anchors.get(sid, [])) for sid, sec in zip(deck["order"], sections)]
    sections = [sec for sec, _ in split]
    write_notes(deck, sections, [parts for _, parts in split])
    html = TEMPLATE.replace("__TITLE__", "Open-ended research with AI agents")
    html = html.replace("__SLIDES__", "\n".join(sections))
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(sections)} slides)")


if __name__ == "__main__":
    main()

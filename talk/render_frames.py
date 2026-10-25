"""Render every slide and build step of talk/deck.html to PNG.

Writes <out_dir>/s<slide>_<step>.png at 1920x1080, where step 0 is the
slide before any build and the last step is the fully built slide.
Needs Playwright with Chromium (pip install playwright;
python -m playwright install chromium).

Usage: python talk/render_frames.py <out_dir>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DECK = Path(__file__).resolve().parent / "deck.html"


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(DECK.as_uri() + "?static")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)
        steps = page.evaluate("deck.steps.map(s => s.length)")
        for i, n in enumerate(steps):
            for k in range(n + 1):
                page.evaluate(f"deck.go({i}, {k})")
                page.wait_for_timeout(50)
                page.screenshot(path=str(out / f"s{i + 1}_{k}.png"))
        browser.close()
    print(f"rendered {sum(n + 1 for n in steps)} frames to {out}")


if __name__ == "__main__":
    main(sys.argv[1])

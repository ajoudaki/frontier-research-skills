"""Re-cut the talk audio so each build step lands right before its speech.

For every slide change and build step there is an anchor: the phrase that
starts talking about that piece. The audio is cut at the quietest moment
just before the phrase and PAUSE seconds of silence are inserted there; the
piece appears at the start of that pause, so it is on screen just before
the speaker starts talking about it.

Inputs are the talk audio and its Whisper word timestamps
(a JSON list of {"w", "s", "e"}). Writes the edited audio (AAC, mono 64k)
and cues.json, a list of [slide, step, seconds] for make_video.py.

Usage: python talk/align_audio.py <audio> <words.json> <out.m4a> <cues.json>
"""

import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

RATE = 48000
PAUSE = 0.7  # seconds of silence inserted before each piece
SEARCH = 10.0  # how far (s) from the expected time to look for an anchor

# (slide, step, expected seconds in the original audio, opening phrase)
ANCHORS = [
    (2, 0, 98.8, "let's start with where we are today"),
    (2, 1, 101.0, "we're in the middle"),
    (2, 2, 145.4, "and in these open"),
    (2, 3, 193.6, "and in fact the fact that"),
    (2, 4, 206.4, "so we end up with this pile"),
    (2, 5, 230.9, "and when you lose so much control"),
    (3, 0, 242.8, "so to tackle this challenge"),
    (3, 1, 275.6, "first one is to leave"),
    (3, 2, 307.8, "and the second one"),
    (3, 3, 346.8, "and i've also listed"),
    (4, 0, 386.4, "so beyond"),
    (4, 1, 408.9, "a single thread"),
    (4, 2, 431.7, "separate agents"),
    (5, 0, 478.1, ""),  # first word after the pause, whatever Whisper heard
    (5, 1, 483.3, "sometimes you have"),
    (5, 2, 505.3, "but most open research"),
    (6, 0, 536.0, "let's start with the targeted"),
    (6, 1, 623.0, "so the first skill"),
    (6, 2, 632.0, "it basically uses"),
    (6, 3, 660.0, "and this will move"),
    (7, 0, 721.9, "now i mentioned"),
    (7, 1, 742.3, "some succeed"),
    (7, 2, 798.7, "so the results from"),
    (7, 3, 861.9, "and when you turn"),
    (8, 0, 899.6, "and one more important point"),
    (8, 1, 910.6, "one very important thing"),
    (8, 2, 930.5, "so one of the important skills"),
    (8, 3, 954.1, "so i packed everything"),
    (9, 0, 965.8, "so to wrap up"),
    (9, 1, 982.4, "the table here"),
    (9, 2, 987.0, "and they're all in the"),
]


def norm(text):
    return re.sub(r"[^a-z]", "", text.lower())


def find_anchor(words, expected, phrase):
    """Index of the word where `phrase` starts, closest to `expected`."""
    target = norm(phrase)
    best = None
    for i, w in enumerate(words):
        if abs(w["s"] - expected) > SEARCH:
            continue
        if target:
            joined = "".join(norm(x["w"]) for x in words[i:i + 12])
            if not joined.startswith(target):
                continue
        elif i == 0 or w["s"] - words[i - 1]["e"] < 0.5:
            continue  # empty phrase: the first word after a clear pause
        if best is None or abs(w["s"] - expected) < abs(words[best]["s"] - expected):
            best = i
    if best is None:
        near = " ".join(w["w"] for w in words if abs(w["s"] - expected) < SEARCH)
        raise SystemExit(f"anchor {phrase!r} not found near {expected}s: {near}")
    return best


def quietest(audio, lo, hi, win=0.1):
    """Centre (s) of the quietest `win`-second window in [lo, hi]."""
    a, b = int(lo * RATE), int(hi * RATE)
    n = int(win * RATE)
    seg = audio[a:b].astype(np.float64) ** 2
    if len(seg) < n:
        return (lo + hi) / 2
    energy = np.convolve(seg, np.ones(n), "valid")
    return (a + int(np.argmin(energy)) + n // 2) / RATE


def main(audio_in, words_json, audio_out, cues_out):
    words = json.loads(Path(words_json).read_text())
    work = Path(tempfile.mkdtemp(prefix="talk_align_"))
    raw = work / "in.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", audio_in, "-ac", "1", "-ar", str(RATE), str(raw)],
                   check=True)
    with wave.open(str(raw)) as f:
        audio = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16)

    cuts, missing = [], []
    for slide, step, expected, phrase in ANCHORS:
        try:
            i = find_anchor(words, expected, phrase)
        except SystemExit as e:
            missing.append(str(e))
            continue
        start = words[i]["s"]
        prev_end = words[i - 1]["e"] if i > 0 else 0.0
        lo = max(prev_end - 0.1, start - 0.8)
        cut = quietest(audio, lo, start + 0.05)
        cuts.append((slide, step, cut))
        print(f"{slide}.{step}  {cut:8.2f}s  {phrase or words[i]['w'].strip()!r}")

    if missing:
        raise SystemExit("\n".join(missing))
    times = [c for _, _, c in cuts]
    assert times == sorted(times), "anchors out of order"

    # Splice: original audio with PAUSE seconds of silence at every cut,
    # with 10 ms fades either side of each cut to avoid clicks.
    fade = int(0.01 * RATE)
    ramp = np.linspace(0, 1, fade)
    pieces, cues, offset, last = [], [[1, 0, 0.0]], 0.0, 0
    for slide, step, cut in cuts:
        k = int(cut * RATE)
        chunk = audio[last:k].astype(np.float64)
        if last > 0:
            chunk[:fade] *= ramp
        chunk[-fade:] *= ramp[::-1]
        pieces.append(chunk)
        offset += len(chunk) / RATE
        cues.append([slide, step, round(offset, 3)])
        pieces.append(np.zeros(int(PAUSE * RATE)))
        offset += PAUSE
        last = k
    tail = audio[last:].astype(np.float64)
    tail[:fade] *= ramp
    pieces.append(tail)

    out = work / "out.wav"
    with wave.open(str(out), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(np.concatenate(pieces).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-c:a", "aac", "-b:a", "64k", audio_out],
                   check=True)
    Path(cues_out).write_text(json.dumps(cues))
    print(f"wrote {audio_out} and {cues_out} ({len(cues)} cues)")


if __name__ == "__main__":
    main(*sys.argv[1:5])

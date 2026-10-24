"""Read the whole talk's speaker notes in a cloned voice with Higgs TTS 3.

Each slide's notes are split at its build anchors, then into sentence-aligned
chunks. Every chunk is generated with the same reference clip, its trailing
breath is cut, and it is checked by transcribing it with Whisper; chunks with
misread words or a suspicious length are regenerated with another seed.
Chunks are loudness-matched and joined with short pauses.

Build steps are timed to the speech in one of three ways:
  - an anchor that starts a sentence splits the notes there; a short beat
    is inserted and the piece appears at its start, just before the words;
  - an anchor inside a sentence is located with Whisper word timestamps and
    the piece appears just before that word, with no pause;
  - steps without an anchor are spread evenly between their neighbours.

Usage:
  env/bin/python speak_talk.py --notes speaker-notes.md --ref refs/agents.wav \
      --out out/talk.wav --timings out/talk_slides.json --cues out/talk_cues.json
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import whisper

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "node"))
import native as N  # noqa: E402

SR = N.SAMPLE_RATE
CHUNK_GAP = 0.32   # seconds between chunks of one build step
BUILD_GAP = 0.7    # beat before a build step's speech; the piece appears at its start
SLIDE_GAP = 1.0    # seconds between slides; the new slide appears at its start
LEAD = 0.25        # an inline piece appears this long before its word

# Per slide: (step, phrase) where each build step's speech starts. Steps left out
# are spread evenly between their neighbours.
BUILD_ANCHORS = {
    2: [(1, "We're in the middle"), (2, "The transition is hard"), (3, "On top of that"), (4, "So we end up")],
    4: [(1, "We organize it into research thrusts"), (2, "Most go step by step"), (3, "And with some lag"),
        (4, "The thrusts keep pushing out"), (5, "and the core follows"), (6, "The explored region's shore"),
        (7, "Instead of reading everything"), (8, "Finally, a part of the core"),
        (9, "But look at one thrust"), (10, "pushing out into uncharted waters")],
    6: [(1, "First, why not one long thread?"), (2, "Once it makes an early mistake"), (3, "everything after it is anchored"),
        (4, "Independent agents start fresh"), (5, "So does the second."), (6, "And the third."), (7, "The fourth catches it"),
        (8, "Agents can also work against each other."), (9, "A critic objects."), (10, "The author repairs it."),
        (11, "And the critic checks again"), (12, "And it has to be cost-effective."), (13, "The pyramid is built"),
        (14, "And when a claim can be tested")],
    8: [(1, "Context:"), (2, "Persistence:"), (3, "Reuse.")],
    10: [(1, "organize-research-project is the main one"), (2, "Inside each thrust"), (3, "solve-problem solves it"),
         (4, "and teach-material makes sure"), (5, "Finally, review-paper audits")],
    11: [(1, "From the research question, studies branch out"), (6, "That way, an agent stuck"),
         (7, "The second idea is the promotion gate."), (8, "These pass"), (11, "These fail"),
         (13, "So whatever is in the core"), (14, "The third idea"), (15, "New studies can rely"),
         (16, "and they can be promoted in turn"), (17, "But let's zoom in on one thrust.")],
    12: [(1, "The question itself is pinned down"), (2, "The definitions are fixed"), (3, "The quantifiers keep their order"),
         (4, "The evidence standard"), (5, "And the scope is explicit"), (6, "Once they're ruled out"), (7, "Then it's frozen.")],
    14: [(1, "With your go-ahead"), (2, "Two routes that turn out"), (3, "Mature routes can borrow"),
         (4, "But a candidate isn't a proof yet."), (5, "Only what survives"), (6, "And now the arrow is solid")],
    16: [(1, "First, notation."), (2, "Then the idea"), (3, "Then a toy example"), (4, "And only then the details.")],
    18: [(1, "review-paper reads the full submission"), (2, "It lifts out"), (3, "It re-derives"), (4, "It retrieves the cited papers"),
         (5, "It audits the code"), (6, "It rates how plausible"), (7, "Each flaw gets a severity"),
         (8, "And a fatal flaw cascades"), (9, "The verdict says")],
    20: [(1, "organize-research-project turns it"), (2, "The explored region grows fast"), (3, "Behind it, with some lag"),
         (4, "That's the balance"), (7, "And every step raises"), (8, "Then review-paper audits"), (9, "Here's how to use it.")],
    21: [(1, "We started from one"), (2, "Everything we discussed has one goal"), (3, "What's next?"),
         (4, "And a last, more philosophical note."), (5, "Everything is in the repo.")],
}
TRIES = 3
MAX_ERR = 0.06     # fraction of words Whisper may get wrong before a retry

# Written forms the model should read the way the speaker says them.
SPOKEN = [
    (r"AGENTS\.md", "agents dot M D"),
    (r"CLAUDE\.md", "Claude dot M D"),
    (r"\bLaTeX\b", "LaTeX"),
    (r"organize-research-project", "organize research project"),
    (r"formulate-problem", "formulate problem"),
    (r"solve-problem", "solve problem"),
    (r"teach-material", "teach material"),
    (r"explain-canonically", "explain canonically"),
    (r"review-paper", "review paper"),
]


def spoken(text):
    for pat, rep in SPOKEN:
        text = re.sub(pat, rep, text)
    return text


def read_notes(path):
    parts = re.split(r"^## ", Path(path).read_text(), flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1].strip()) for p in parts]


def sentences(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def build_segments(slide_no, notes):
    """Split a slide's notes at its sentence-start anchors: [(step, text, [(step, phrase), ...inline])]."""
    anchors = BUILD_ANCHORS.get(slide_no, [])
    segments = [[0, [], []]]
    k = 0
    for sentence in sentences(notes):
        while k < len(anchors):
            step, phrase = anchors[k]
            if sentence.startswith(phrase):
                segments.append([step, [sentence], []])
                k += 1
                continue
            if phrase in sentence and not any(sentence.startswith(p) for _, p in anchors[k + 1:]):
                if not segments[-1][1] or segments[-1][1][-1] != sentence:
                    segments[-1][1].append(sentence)
                segments[-1][2].append((step, phrase))
                k += 1
                continue
            break
        if not segments[-1][1] or segments[-1][1][-1] != sentence:
            segments[-1][1].append(sentence)
    if k != len(anchors):
        raise SystemExit(f"slide {slide_no}: anchor {anchors[k][1]!r} not found in order")
    return [(step, " ".join(ss), inl) for step, ss, inl in segments if ss]


def chunks(text, max_words=45):
    out, cur = [], []
    for s in sentences(text):
        if cur and len(" ".join(cur + [s]).split()) > max_words:
            out.append(" ".join(cur))
            cur = []
        cur.append(s)
    if cur:
        out.append(" ".join(cur))
    return out


def words(text):
    text = text.lower().replace("-", " ")
    text = re.sub(r"\b10\b", "ten", text)
    return re.sub(r"[^a-z0-9' ]", " ", text).split()


def error_rate(ref, hyp):
    a, b = words(ref), words(hyp)
    sm = difflib.SequenceMatcher(a=a, b=b)
    errs = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    return errs / max(1, len(a))


def level(audio, target_rms=0.08):
    voiced = audio[np.abs(audio) > 0.01]
    rms = np.sqrt((voiced ** 2).mean()) if len(voiced) else 0
    return audio * (target_rms / rms) if rms > 0 else audio


def trim_tail(audio, margin=0.1, fade=0.06):
    """Cut the exhale the model adds after the last word: end shortly after the last loud frame, with a fade."""
    fr = int(0.02 * SR)
    m = len(audio) // fr
    if m < 10:
        return audio
    r = np.sqrt((audio[:m * fr].reshape(m, fr) ** 2).mean(1))
    speech = np.median(r[r > np.percentile(r, 50)])
    last = m - 1 - int(np.argmax(r[::-1] > 0.2 * speech))
    end = min(len(audio), (last + 1) * fr + int(margin * SR))
    out = audio[:end].copy()
    n = min(int(fade * SR), len(out))
    out[-n:] *= np.linspace(1, 0, n)
    return out


def to16k(audio):
    n = int(len(audio) * 16000 / SR)
    return np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)


def phrase_time(phrase, chunk, heard_words, secs):
    """Seconds into a chunk where `phrase` starts: from Whisper's word timestamps, else by text position."""
    target = words(spoken(phrase))
    hw = [(words(w["word"]), w["start"]) for w in heard_words]
    flat = [(t, s) for ws, s in hw for t in ws]
    toks = [t for t, _ in flat]
    for i in range(len(toks) - len(target) + 1):
        if toks[i:i + len(target)] == target:
            return flat[i][1], "whisper"
    sm = difflib.SequenceMatcher(a=toks, b=target)
    m = sm.find_longest_match(0, len(toks), 0, len(target))
    if m.size >= max(2, len(target) // 2):
        return flat[m.a][1], "whisper~"
    pos = spoken(chunk).find(spoken(phrase))
    return secs * max(pos, 0) / max(1, len(spoken(chunk))), "text"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timings", required=True)
    ap.add_argument("--cues", required=True, help="video cues: [[slide, step, seconds], ...]")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--asr-device", default="cuda:1")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--only", type=int, nargs="*", help="check anchors and print segments, no audio")
    args = ap.parse_args()

    notes = read_notes(args.notes)
    plan = [(n, title, build_segments(n, text)) for n, (title, text) in enumerate(notes, start=1)]
    if args.only is not None:
        for n, title, segs in plan:
            if not args.only or n in args.only:
                print(f"== {n}. {title}")
                for step, text, inl in segs:
                    print(f"  [{step}] {text[:90]}{' …' if len(text) > 90 else ''}  inline={inl}")
        return

    model_dir = ROOT / "model"
    device = torch.device(args.device)
    model = N.build_native_model(N.read_config(model_dir), torch.bfloat16, "sdpa")
    N.load_native_weights(model, model_dir, device, torch.bfloat16)
    codec = N.HiggsAudioCodec.from_pretrained(model_dir, device=device, dtype=torch.float32)
    tok = N.load_tokenizer(model_dir)
    asr = whisper.load_model("medium", device=args.asr_device)

    ref_path = Path(args.ref)
    ref_text = ref_path.with_suffix(".txt").read_text().strip()
    data, sr = sf.read(str(ref_path), dtype="float32", always_2d=True)
    ref_delayed = N.apply_delay_pattern(codec.encode_reference(torch.from_numpy(data.mean(axis=1)), sr))

    def generate(text, seed):
        torch.manual_seed(seed)
        prompt = tok.build_prompt(text, num_ref_tokens=int(ref_delayed.shape[0]), reference_text=ref_text)
        with torch.inference_mode():
            delayed = model.generate_codes(prompt, ref_delayed, max_new_tokens=1500,
                                           temperature=0.8, top_p=None, top_k=50)
            audio = codec.decode(N.reverse_delay_pattern(delayed))
        return trim_tail(N.trim_silence_edges(audio, SR).numpy())

    pieces, timings, cues, t, seed = [], [], [], 0.0, args.seed
    log = []

    def pause(secs):
        nonlocal t
        pieces.append(np.zeros(int(secs * SR), dtype=np.float32))
        t += secs

    for slide_no, title, segs in plan:
        cues.append([slide_no, 0, round(t, 3)])
        if slide_no > 1:
            pause(SLIDE_GAP)
        timings.append({"slide": slide_no, "title": title, "start": round(t, 3)})
        slide_cues = {0: cues[-1][2]}
        for step, segment, inline in segs:
            if step > 0:
                slide_cues[step] = round(t, 3)
                pause(BUILD_GAP)
            pending = list(inline)
            for k, chunk in enumerate(chunks(segment)):
                if k > 0:
                    pause(CHUNK_GAP)
                text = spoken(chunk)
                best = None
                for attempt in range(TRIES):
                    seed += 1
                    audio = generate(text, seed)
                    secs = len(audio) / SR
                    rate = len(text.split()) / max(secs, 0.1) * 60  # words per minute
                    with torch.cuda.device(torch.device(args.asr_device)):
                        res = asr.transcribe(to16k(audio), language="en", word_timestamps=True)
                    heard = res["text"]
                    err = error_rate(text, heard)
                    ok = err <= MAX_ERR and 110 <= rate <= 220
                    score = err + (0 if 110 <= rate <= 220 else 1)
                    if best is None or score < best[0]:
                        hw = [w for s in res["segments"] for w in s.get("words", [])]
                        best = (score, audio, err, rate, attempt + 1, heard, hw)
                    if ok:
                        break
                _, audio, err, rate, tries, heard, hw = best
                secs = len(audio) / SR
                for st, phrase in [x for x in pending if x[1] in chunk]:
                    at, how = phrase_time(phrase, chunk, hw, secs)
                    slide_cues[st] = round(max(t, t + at - LEAD), 3)
                    pending.remove((st, phrase))
                    print(f"  inline step {st} at +{at:.2f}s ({how}): {phrase!r}", flush=True)
                print(f"slide {slide_no} step {step} chunk {k + 1}: {secs:5.1f}s "
                      f"{rate:4.0f} wpm, err {err:.1%}, tries {tries}", flush=True)
                log.append({"slide": slide_no, "step": step, "chunk": k + 1, "text": chunk,
                            "heard": heard.strip(), "err": round(err, 3), "wpm": round(rate), "tries": tries})
                pieces.append(level(audio).astype(np.float32))
                t += secs
            assert not pending, f"slide {slide_no}: inline anchors not placed: {pending}"
        # steps without an anchor: spread evenly between their neighbours
        last = max(slide_cues)
        known = sorted(slide_cues)
        for s in range(1, last + 1):
            if s not in slide_cues:
                lo = max(k for k in known if k < s)
                hi = min(k for k in known if k > s)
                slide_cues[s] = round(slide_cues[lo] + (slide_cues[hi] - slide_cues[lo]) * (s - lo) / (hi - lo), 3)
        cues += [[slide_no, s, slide_cues[s]] for s in range(1, last + 1)]
        timings[-1]["end"] = round(t, 3)
    pause(1.5)

    sf.write(args.out, np.concatenate(pieces).clip(-1, 1), SR)
    Path(args.timings).write_text(json.dumps({"slides": timings, "chunks": log}, indent=1))
    Path(args.cues).write_text(json.dumps(cues))
    print(f"wrote {args.out} ({t / 60:.1f} min)")


if __name__ == "__main__":
    main()

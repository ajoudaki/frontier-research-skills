"""Read the whole talk's speaker notes in a cloned voice with Higgs TTS 3.

Each slide's notes are split into sentence-aligned chunks. Every chunk is
generated with the same reference clip, then checked by transcribing it with
Whisper; chunks with misread words or a suspicious length are regenerated
with another seed. Chunks are loudness-matched and joined with short pauses
inside a slide and longer ones between slides.

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

# Per slide, the sentence openings where each build step starts (in order).
BUILD_ANCHORS = {
    2: ["We're in the middle", "The transition is hard", "On top of that", "So we end up", "You lose so much control"],
    3: ["First, leave the chat", "Second, run everything", "Then a few more basics"],
    4: ["The difference is conceptual", "Separate agents get"],
    5: ["Sometimes you have", "But most open"],
    6: ["So the first skill", "It uses its own intelligence", "Then the second skill"],
    7: ["Some succeed", "Results enter the core", "And when you turn"],
    8: ["Even after all these steps", "So one of the most important skills", "I packed everything"],
    9: ["The table shows", "Feel free"],
}
TRIES = 3
MAX_ERR = 0.06     # fraction of words Whisper may get wrong before a retry

# Written forms the model should read the way the speaker says them.
SPOKEN = [
    (r"AGENTS\.md", "agents dot M D"),
    (r"CLAUDE\.md", "Claude dot M D"),
    (r"80/20", "eighty-twenty"),
    (r"\bLaTeX\b", "LaTeX"),
    (r"investigate-conjectures", "investigate conjectures"),
    (r"solve-math-rigorously", "solve math rigorously"),
    (r"organize-research-project", "organize research project"),
    (r"review-ai-paper", "review AI paper"),
    (r"teach-technical-math", "teach technical math"),
]


def spoken(text):
    for pat, rep in SPOKEN:
        text = re.sub(pat, rep, text)
    return text


def read_notes(path):
    parts = re.split(r"^## ", Path(path).read_text(), flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1].strip()) for p in parts]


def build_segments(slide_no, notes):
    """Split a slide's notes into (step, text) at its build anchors."""
    sentences = re.split(r"(?<=[.!?])\s+", notes.strip())
    anchors = BUILD_ANCHORS.get(slide_no, [])
    segments, step = [[0, []]], 0
    for sentence in sentences:
        if step < len(anchors) and sentence.startswith(anchors[step]):
            step += 1
            segments.append([step, []])
        segments[-1][1].append(sentence)
    if step != len(anchors):
        raise SystemExit(f"slide {slide_no}: anchor {anchors[step]!r} not found")
    return [(k, " ".join(ss)) for k, ss in segments if ss]


def chunks(text, max_words=45):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    out, cur = [], []
    for s in sentences:
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
    args = ap.parse_args()

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
        return N.trim_silence_edges(audio, SR).numpy()

    pieces, timings, cues, t, seed = [], [], [], 0.0, args.seed
    log = []

    def pause(secs):
        nonlocal t
        pieces.append(np.zeros(int(secs * SR), dtype=np.float32))
        t += secs

    for slide_no, (title, notes) in enumerate(read_notes(args.notes), start=1):
        cues.append([slide_no, 0, round(t, 3)])
        if slide_no > 1:
            pause(SLIDE_GAP)
        timings.append({"slide": slide_no, "title": title, "start": round(t, 3)})
        for step, segment in build_segments(slide_no, notes):
            if step > 0:
                cues.append([slide_no, step, round(t, 3)])
                pause(BUILD_GAP)
            for k, chunk in enumerate(chunks(spoken(segment))):
                if k > 0:
                    pause(CHUNK_GAP)
                best = None
                for attempt in range(TRIES):
                    seed += 1
                    audio = generate(chunk, seed)
                    secs = len(audio) / SR
                    rate = len(chunk.split()) / max(secs, 0.1) * 60  # words per minute
                    heard = asr.transcribe(audio.astype(np.float32), language="en")["text"]
                    err = error_rate(chunk, heard)
                    ok = err <= MAX_ERR and 110 <= rate <= 220
                    score = err + (0 if 110 <= rate <= 220 else 1)
                    if best is None or score < best[0]:
                        best = (score, audio, err, rate, attempt + 1, heard)
                    if ok:
                        break
                _, audio, err, rate, tries, heard = best
                print(f"slide {slide_no} step {step} chunk {k + 1}: {len(audio) / SR:5.1f}s "
                      f"{rate:4.0f} wpm, err {err:.1%}, tries {tries}", flush=True)
                log.append({"slide": slide_no, "step": step, "chunk": k + 1, "text": chunk,
                            "heard": heard.strip(), "err": round(err, 3), "wpm": round(rate), "tries": tries})
                audio = level(audio).astype(np.float32)
                pieces.append(audio)
                t += len(audio) / SR
        timings[-1]["end"] = round(t, 3)
    pause(1.5)

    sf.write(args.out, np.concatenate(pieces).clip(-1, 1), SR)
    Path(args.timings).write_text(json.dumps({"slides": timings, "chunks": log}, indent=1))
    Path(args.cues).write_text(json.dumps(cues))
    print(f"wrote {args.out} ({t / 60:.1f} min)")


if __name__ == "__main__":
    main()

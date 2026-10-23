"""Speak text in a cloned voice with Higgs TTS 3, without ComfyUI.

Uses the native PyTorch implementation from the Higgs_v3-TTS-ComfyUI node
(node/native.py) with the official weights in model/.

Usage:
  env/bin/python speak.py --ref refs/agents.wav --text-file in.txt --out out.wav
  (the reference transcript is read from refs/agents.txt)
"""

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "node"))
import native as N  # noqa: E402


def chunks(text, max_words=40):
    """Group whole sentences into chunks of at most ~max_words words."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--text-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--top-k", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--gap", type=float, default=0.25, help="seconds of silence between chunks")
    args = ap.parse_args()

    model_dir = ROOT / "model"
    device = torch.device(args.device)
    dtype = torch.bfloat16

    model = N.build_native_model(N.read_config(model_dir), dtype, "sdpa")
    N.load_native_weights(model, model_dir, device, dtype)
    codec = N.HiggsAudioCodec.from_pretrained(model_dir, device=device, dtype=torch.float32)
    tok = N.load_tokenizer(model_dir)

    ref_path = Path(args.ref)
    ref_text = ref_path.with_suffix(".txt").read_text().strip()
    data, sr = sf.read(str(ref_path), dtype="float32", always_2d=True)
    wav = torch.from_numpy(data.mean(axis=1))
    ref_delayed = N.apply_delay_pattern(codec.encode_reference(wav, sr))

    torch.manual_seed(args.seed)
    pieces = []
    for i, chunk in enumerate(chunks(Path(args.text_file).read_text())):
        prompt = tok.build_prompt(chunk, num_ref_tokens=int(ref_delayed.shape[0]), reference_text=ref_text)
        with torch.inference_mode():
            delayed = model.generate_codes(
                prompt, ref_delayed, max_new_tokens=1500,
                temperature=args.temperature, top_p=None, top_k=args.top_k,
            )
            audio = codec.decode(N.reverse_delay_pattern(delayed))
        audio = N.trim_silence_edges(audio, N.SAMPLE_RATE).numpy()
        print(f"chunk {i + 1}: {len(audio) / N.SAMPLE_RATE:.1f}s  {chunk[:60]}...")
        pieces += [audio, np.zeros(int(args.gap * N.SAMPLE_RATE), dtype=np.float32)]
    sf.write(args.out, np.concatenate(pieces).clip(-1, 1), N.SAMPLE_RATE)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

"""Make the talk video: rendered slide frames timed to the recorded audio.

Each build step of talk/deck.html appears at its cue, with a short
crossfade. Frames come from talk/render_frames.py; the audio and cues.json
(a list of [slide, step, seconds]; step 0 is the slide before any build)
come from talk/align_audio.py.

Usage: python talk/make_video.py <frames_dir> <audio.m4a> <cues.json> <out.mp4>
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

FADE_FRAMES = 10  # crossfade length, at 25 frames per second
FADE_STEP = 0.04


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout)


def main(frames_dir, audio, cues_json, out):
    frames = Path(frames_dir)
    cues = json.loads(Path(cues_json).read_text())
    end = duration(audio)
    work = Path(tempfile.mkdtemp(prefix="talk_video_"))
    entries = []  # (image path, seconds shown)
    prev = None
    for i, (slide, step, start) in enumerate(cues):
        stop = cues[i + 1][2] if i + 1 < len(cues) else end
        img = frames / f"s{slide}_{step}.png"
        hold = stop - start
        if prev is not None:
            a = Image.open(prev).convert("RGB")
            b = Image.open(img).convert("RGB")
            for k in range(1, FADE_FRAMES + 1):
                blend = work / f"fade_{i:02d}_{k:02d}.png"
                Image.blend(a, b, k / (FADE_FRAMES + 1)).save(blend)
                entries.append((blend, FADE_STEP))
            hold -= FADE_FRAMES * FADE_STEP
        entries.append((img, hold))
        prev = img

    listing = work / "list.txt"
    with listing.open("w") as f:
        for path, secs in entries:
            f.write(f"file '{path}'\nduration {secs:.3f}\n")
        f.write(f"file '{entries[-1][0]}'\n")  # the concat demuxer needs the last file repeated

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-i", audio, "-map", "0:v", "-map", "1:a",
         "-vf", "fps=25,format=yuv420p", "-c:v", "libx264",
         "-tune", "stillimage", "-crf", "20", "-g", "7500",
         "-c:a", "copy", "-movflags", "+faststart", out],
        check=True,
    )
    print(f"wrote {out} ({duration(out):.1f} s)")


if __name__ == "__main__":
    main(*sys.argv[1:5])

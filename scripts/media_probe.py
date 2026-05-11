from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe media and generate review artifacts with FFmpeg.")
    parser.add_argument("input")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--fps", default="1/10")
    parser.add_argument("--scale", default="220:-1")
    parser.add_argument("--tile", default="4x4")
    parser.add_argument("--extract-audio", action="store_true")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    probe_path = args.output_dir / "media-info.json"
    sheet_path = args.output_dir / "contact-sheet.jpg"
    audio_path = args.output_dir / "audio.wav"

    probe = run(
        [
            args.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,sample_rate,channels",
            "-of",
            "json",
            args.input,
        ]
    )
    probe_path.write_text(probe.stdout or probe.stderr, encoding="utf-8")

    sheet = run(
        [
            args.ffmpeg,
            "-y",
            "-v",
            "error",
            "-i",
            args.input,
            "-vf",
            f"fps={args.fps},scale={args.scale},tile={args.tile}",
            "-frames:v",
            "1",
            str(sheet_path),
        ]
    )

    audio_result = None
    if args.extract_audio:
        audio_result = run(
            [
                args.ffmpeg,
                "-y",
                "-v",
                "error",
                "-i",
                args.input,
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                str(audio_path),
            ]
        )

    result = {
        "ok": probe.returncode == 0,
        "input": args.input,
        "media_info": str(probe_path),
        "contact_sheet": str(sheet_path) if sheet_path.exists() else None,
        "audio": str(audio_path) if audio_path.exists() else None,
        "probe_exit": probe.returncode,
        "contact_sheet_exit": sheet.returncode,
        "audio_exit": audio_result.returncode if audio_result else None,
    }
    (args.output_dir / "probe-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

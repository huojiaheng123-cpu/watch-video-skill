from __future__ import annotations

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


def format_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe audio/video with faster-whisper.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--no-vad", action="store_true")
    args = parser.parse_args()

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments_iter, info = model.transcribe(
        str(args.input),
        language=args.language,
        vad_filter=not args.no_vad,
        word_timestamps=True,
        beam_size=5,
    )

    segments = []
    words = []
    for index, segment in enumerate(segments_iter, start=1):
        segment_words = []
        for word in segment.words or []:
            item = {
                "text": word.word,
                "start": round(float(word.start), 3),
                "end": round(float(word.end), 3),
                "probability": round(float(word.probability), 4),
            }
            segment_words.append(item)
            words.append(item)
        segments.append(
            {
                "index": index,
                "start": round(float(segment.start), 3),
                "end": round(float(segment.end), 3),
                "text": segment.text.strip(),
                "words": segment_words,
            }
        )

    payload = {
        "ok": True,
        "engine": "faster-whisper",
        "model": args.model,
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "duration": round(float(info.duration), 3),
        "segment_count": len(segments),
        "word_count": len(words),
        "segments": segments,
        "words": words,
    }

    args.output_prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.output_prefix.with_suffix(".json")
    srt_path = args.output_prefix.with_suffix(".srt")
    txt_path = args.output_prefix.with_suffix(".txt")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    txt_path.write_text(
        "\n".join(segment["text"] for segment in segments if segment["text"]),
        encoding="utf-8",
    )

    lines = []
    for segment in segments:
        if not segment["text"]:
            continue
        lines.append(str(segment["index"]))
        lines.append(f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}")
        lines.append(segment["text"])
        lines.append("")
    srt_path.write_text("\n".join(lines), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "json": str(json_path),
                "srt": str(srt_path),
                "txt": str(txt_path),
                "segments": len(segments),
                "words": len(words),
                "duration": payload["duration"],
                "language": payload["language"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

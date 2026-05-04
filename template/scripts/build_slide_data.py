#!/usr/bin/env python3
"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.

Codex Phase 3B design (2026-05-04, CODEX_PHASE3B_NEXT) 推奨: A 一択 + deterministic first.

入力:
    <PROJECT>/transcript_fixed.json  - segments[] / words[]
    <PROJECT>/project-config.json    - format / tone
    (任意) <PROJECT>/vad_result.json - cut segments の元データ (cut 後 frame 変換用)

出力:
    <PROJECT>/src/Slides/slideData.ts - SlideSegment[]

Usage:
    python3 scripts/build_slide_data.py [--mode topic|segment]

  --mode topic    (default): 連続 segments をグループ化して 1 slide に
  --mode segment           : 1 transcript segment = 1 slide (シンプル)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
FPS = 60  # videoConfig.FPS と同期、後段で project-config から読むよう拡張可能
SILENCE_THRESHOLD_MS = 1500  # 1.5 秒以上の無音で話題区切り
TITLE_MAX_CHARS = {"youtube": 18, "short": 14, "square": 16}
BULLET_MAX_CHARS = {"youtube": 24, "short": 18, "square": 20}
MAX_BULLETS_PER_SLIDE = 5
MAX_SEGMENTS_PER_SLIDE = 5  # silence 検出失敗時の機械 fallback


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def build_cut_segments_from_vad(vad: dict | None) -> list[dict]:
    if not vad or "speech_segments" not in vad:
        return []
    out = []
    cursor_ms = 0
    for i, seg in enumerate(vad["speech_segments"]):
        s_ms = seg["start"]
        e_ms = seg["end"]
        dur_ms = e_ms - s_ms
        out.append({
            "id": i + 1,
            "originalStartMs": s_ms,
            "originalEndMs": e_ms,
            "playbackStart": round(cursor_ms / 1000 * FPS),
            "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
        })
        cursor_ms += dur_ms
    return out


def ms_to_playback_frame(ms: int, cut_segments: list[dict]) -> int | None:
    if not cut_segments:
        return round(ms / 1000 * FPS)
    for cs in cut_segments:
        if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
            offset_ms = ms - cs["originalStartMs"]
            return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
    return None


def truncate(text: str, max_chars: int) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 1] + "…"


def group_topics(segments: list[dict], threshold_ms: int = SILENCE_THRESHOLD_MS) -> list[list[dict]]:
    """隣接 segments の間隔 >= threshold_ms で話題区切り."""
    if not segments:
        return []
    groups: list[list[dict]] = [[segments[0]]]
    for prev, cur in zip(segments, segments[1:]):
        gap_ms = cur["start"] - prev["end"]
        if gap_ms >= threshold_ms or len(groups[-1]) >= MAX_SEGMENTS_PER_SLIDE:
            groups.append([cur])
        else:
            groups[-1].append(cur)
    return groups


def style_for_tone(tone: str) -> dict:
    table = {
        "プロフェッショナル": {"align": "center", "bg": "rgba(20, 26, 44, 0.92)", "emphasis_ratio": 0.2},
        "エンタメ": {"align": "left", "bg": "#101a2c", "emphasis_ratio": 0.4},
        "カジュアル": {"align": "left", "bg": "rgba(40, 30, 60, 0.9)", "emphasis_ratio": 0.3},
        "教育的": {"align": "left", "bg": "#0f2540", "emphasis_ratio": 0.4},
    }
    return table.get(tone, table["プロフェッショナル"])


def build_slides_topic_mode(segments: list[dict], cut_segments: list[dict],
                            fmt: str, tone: str) -> list[dict]:
    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
    bullet_max = BULLET_MAX_CHARS.get(fmt, BULLET_MAX_CHARS["short"])
    style = style_for_tone(tone)
    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None

    slides: list[dict] = []
    groups = group_topics(segments)
    for group_idx, group in enumerate(groups):
        first = group[0]
        last = group[-1]

        pb_start = ms_to_playback_frame(first["start"], cut_segments)
        pb_end = ms_to_playback_frame(last["end"], cut_segments)
        if pb_start is None or pb_end is None:
            continue
        if cut_total is not None:
            pb_end = min(pb_end, cut_total)
        if pb_end <= pb_start:
            continue

        title = truncate(first["text"], title_max)
        subtitle = truncate(last["text"], title_max + 6) if len(group) > 1 and last is not first else None
        if subtitle == title:
            subtitle = None

        bullets: list[dict] = []
        bullets_source = group[1:-1] if len(group) >= 3 else group
        for i, seg in enumerate(bullets_source[:MAX_BULLETS_PER_SLIDE]):
            text = truncate(seg["text"], bullet_max)
            emphasis = (i == 0 and style["emphasis_ratio"] >= 0.4) or (
                style["emphasis_ratio"] >= 0.3 and i == len(bullets_source) // 2
            )
            bullets.append({"text": text, "emphasis": emphasis})

        slides.append({
            "id": group_idx + 1,
            "startFrame": pb_start,
            "endFrame": pb_end,
            "title": title,
            "subtitle": subtitle,
            "bullets": bullets if bullets else None,
            "align": style["align"],
            "backgroundColor": style["bg"],
            "videoLayer": "visible",
        })
    return slides


def build_slides_segment_mode(segments: list[dict], cut_segments: list[dict],
                              fmt: str, tone: str) -> list[dict]:
    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
    style = style_for_tone(tone)
    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None

    slides: list[dict] = []
    for i, seg in enumerate(segments):
        pb_start = ms_to_playback_frame(seg["start"], cut_segments)
        pb_end = ms_to_playback_frame(seg["end"], cut_segments)
        if pb_start is None or pb_end is None:
            continue
        if cut_total is not None:
            pb_end = min(pb_end, cut_total)
        if pb_end <= pb_start:
            continue
        slides.append({
            "id": i + 1,
            "startFrame": pb_start,
            "endFrame": pb_end,
            "title": truncate(seg["text"], title_max),
            "align": style["align"],
            "backgroundColor": style["bg"],
            "videoLayer": "visible",
        })
    return slides


def render_slide_data_ts(slides: list[dict]) -> str:
    lines = [
        "import type { SlideSegment } from './types';",
        "",
        "// 自動生成: scripts/build_slide_data.py",
        f"// {len(slides)} slides を transcript_fixed.json から生成",
        "",
        "export const slideData: SlideSegment[] = [",
    ]
    for s in slides:
        parts = [
            f"id: {s['id']}",
            f"startFrame: {s['startFrame']}",
            f"endFrame: {s['endFrame']}",
            f"title: {json.dumps(s['title'], ensure_ascii=False)}",
        ]
        if s.get("subtitle"):
            parts.append(f"subtitle: {json.dumps(s['subtitle'], ensure_ascii=False)}")
        if s.get("bullets"):
            bullets_ts = ", ".join(
                "{ text: " + json.dumps(b["text"], ensure_ascii=False)
                + (", emphasis: true" if b.get("emphasis") else "")
                + " }"
                for b in s["bullets"]
            )
            parts.append(f"bullets: [{bullets_ts}]")
        if s.get("align"):
            parts.append(f"align: '{s['align']}'")
        if s.get("backgroundColor"):
            parts.append(f"backgroundColor: {json.dumps(s['backgroundColor'], ensure_ascii=False)}")
        if s.get("videoLayer"):
            parts.append(f"videoLayer: '{s['videoLayer']}'")
        lines.append("  { " + ", ".join(parts) + " },")
    lines.append("];")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["topic", "segment"], default="topic")
    args = ap.parse_args()

    transcript_path = PROJ / "transcript_fixed.json"
    config_path = PROJ / "project-config.json"
    if not transcript_path.exists() or not config_path.exists():
        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")

    transcript = load_json(transcript_path)
    config = load_json(config_path)
    fmt = config.get("format", "short")
    tone = config.get("tone", "プロフェッショナル")
    segments = transcript.get("segments", [])

    vad_path = PROJ / "vad_result.json"
    vad = load_json(vad_path) if vad_path.exists() else None
    cut_segments = build_cut_segments_from_vad(vad)

    if args.mode == "topic":
        slides = build_slides_topic_mode(segments, cut_segments, fmt, tone)
    else:
        slides = build_slides_segment_mode(segments, cut_segments, fmt, tone)

    out_path = PROJ / "src" / "Slides" / "slideData.ts"
    backup = PROJ / "src" / "Slides" / "slideData.backup.ts"
    if out_path.exists() and not backup.exists():
        backup.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")
    ts = render_slide_data_ts(slides)
    out_path.write_text(ts, encoding="utf-8")

    print(f"=== slideData.ts 生成 (mode={args.mode}) ===")
    print(f"path: {out_path}")
    print(f"input segments: {len(segments)}")
    print(f"output slides: {len(slides)}")
    for s in slides:
        bullets_count = len(s.get("bullets") or [])
        print(f"  [{s['id']:2}] f{s['startFrame']:5}-{s['endFrame']:5} '{s['title']}' (bullets={bullets_count})")


if __name__ == "__main__":
    main()

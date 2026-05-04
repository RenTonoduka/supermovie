#!/usr/bin/env python3
"""SuperMovie Phase 3-K integration smoke test (pure python).

template/scripts/timeline.py + 3 script (voicevox_narration / build_slide_data /
build_telop_data) の連鎖が破損していないか、engine / node_modules 不要で
unit test する。Phase 3-J で導入した timeline.py の前提を壊す変更があれば
失敗する。

Usage:
    python3 scripts/test_timeline_integration.py

Exit code:
    0 = 全 assertion pass
    1 = 1 件以上 fail (assertion error)、stderr に詳細
"""
from __future__ import annotations

import json
import struct
import sys
import tempfile
import wave
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import timeline  # noqa: E402


def make_videoconfig_ts(fps: int) -> str:
    return (
        "export type VideoFormat = 'youtube' | 'short' | 'square';\n"
        "export const FORMAT: VideoFormat = 'youtube';\n"
        f"export const FPS = {fps};\n"
        "export const SOURCE_DURATION_FRAMES = 1500;\n"
        "export const VIDEO_FILE = 'main.mp4';\n"
    )


def write_synthetic_wav(path: Path, duration_sec: float, framerate: int = 22050) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(framerate)
        n_frames = int(framerate * duration_sec)
        w.writeframes(struct.pack("<%dh" % n_frames, *[0] * n_frames))


def assert_eq(actual, expected, msg: str) -> None:
    if actual != expected:
        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")


def assert_raises(callable_, exc_type, msg: str):
    try:
        callable_()
    except exc_type:
        return
    raise AssertionError(f"{msg}: expected {exc_type.__name__} but no exception raised")


def test_fps_consistency() -> None:
    """3 script が timeline.read_video_config_fps を経由して同じ FPS を返す."""
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "src").mkdir()
        (proj / "src" / "videoConfig.ts").write_text(make_videoconfig_ts(60))

        # timeline 直読
        assert_eq(timeline.read_video_config_fps(proj), 60, "timeline FPS read")

        # malformed 検出 (FPS 行なし)
        (proj / "src" / "videoConfig.ts").write_text("// no fps line\n")
        assert_eq(
            timeline.read_video_config_fps(proj, default=42),
            42,
            "malformed FPS fallback",
        )

        # FPS=0 を default に倒す
        (proj / "src" / "videoConfig.ts").write_text(
            "export const FPS = 0;\n"
        )
        assert_eq(timeline.read_video_config_fps(proj), timeline.DEFAULT_FPS, "FPS=0 fallback")


def test_vad_schema_validation() -> None:
    """VadSchemaError が部分破損を全て検出する."""
    # 非 dict
    assert_raises(
        lambda: timeline.validate_vad_schema("not dict"),
        timeline.VadSchemaError,
        "non-dict",
    )
    # speech_segments 非 list
    assert_raises(
        lambda: timeline.validate_vad_schema({"speech_segments": "wrong"}),
        timeline.VadSchemaError,
        "speech_segments non-list",
    )
    # segment 非 dict
    assert_raises(
        lambda: timeline.validate_vad_schema({"speech_segments": ["str"]}),
        timeline.VadSchemaError,
        "segment non-dict",
    )
    # start 型不正
    assert_raises(
        lambda: timeline.validate_vad_schema(
            {"speech_segments": [{"start": "bad", "end": 100}]}
        ),
        timeline.VadSchemaError,
        "start non-numeric",
    )
    # end 欠落
    assert_raises(
        lambda: timeline.validate_vad_schema({"speech_segments": [{"start": 0}]}),
        timeline.VadSchemaError,
        "end missing",
    )
    # start > end
    assert_raises(
        lambda: timeline.validate_vad_schema(
            {"speech_segments": [{"start": 100, "end": 50}]}
        ),
        timeline.VadSchemaError,
        "start > end",
    )
    # OK
    timeline.validate_vad_schema(
        {"speech_segments": [{"start": 0, "end": 1000}]}
    )


def test_ms_to_playback_frame() -> None:
    # No cut: 直接 ms→frame
    assert_eq(timeline.ms_to_playback_frame(0, 30, []), 0, "no-cut start")
    assert_eq(timeline.ms_to_playback_frame(1000, 30, []), 30, "no-cut 1s")
    assert_eq(timeline.ms_to_playback_frame(500, 30, []), 15, "no-cut 0.5s")

    # With cut: gap removed
    cut_segs = [
        {"originalStartMs": 0, "originalEndMs": 500, "playbackStart": 0, "playbackEnd": 15},
        {"originalStartMs": 1500, "originalEndMs": 3000, "playbackStart": 15, "playbackEnd": 60},
    ]
    assert_eq(timeline.ms_to_playback_frame(200, 30, cut_segs), 6, "cut seg0 200ms")
    assert_eq(timeline.ms_to_playback_frame(1500, 30, cut_segs), 15, "cut seg1 start")
    assert_eq(timeline.ms_to_playback_frame(2000, 30, cut_segs), 30, "cut seg1 +500ms")
    # 800ms: gap (excluded)
    assert_eq(timeline.ms_to_playback_frame(800, 30, cut_segs), None, "cut gap excluded")


def test_load_cut_segments_fail_fast() -> None:
    """fail_fast=True で部分破損を raise する."""
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "vad_result.json").write_text(
            json.dumps({"speech_segments": [{"start": 100}]})  # end missing
        )
        # default fail_fast=False で []
        assert_eq(timeline.load_cut_segments(proj, 30, fail_fast=False), [], "soft fail")
        # fail_fast=True で raise
        assert_raises(
            lambda: timeline.load_cut_segments(proj, 30, fail_fast=True),
            timeline.VadSchemaError,
            "fail_fast raise",
        )


def test_transcript_segment_validation() -> None:
    """validate_transcript_segment が壊れた transcript を検出する."""
    # OK: timing なし (--script の chunk)
    timeline.validate_transcript_segment({"text": "hi"}, 0)
    # OK: 通常 transcript
    timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
    # NG: start > end
    assert_raises(
        lambda: timeline.validate_transcript_segment(
            {"text": "hi", "start": 1000, "end": 500}, 0
        ),
        timeline.TranscriptSegmentError,
        "transcript start>end",
    )
    # NG: text 非 str
    assert_raises(
        lambda: timeline.validate_transcript_segment({"text": 123}, 0),
        timeline.TranscriptSegmentError,
        "text non-str",
    )
    # NG: start 型不正
    assert_raises(
        lambda: timeline.validate_transcript_segment(
            {"text": "hi", "start": "bad"}, 0
        ),
        timeline.TranscriptSegmentError,
        "start non-numeric",
    )


def test_voicevox_collect_chunks_validation() -> None:
    """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
    import voicevox_narration as vn

    class Args:
        script = None
        script_json = None

    bad = {"segments": [{"text": "hi", "start": 100, "end": 50}]}
    assert_raises(
        lambda: vn.collect_chunks(Args(), bad),
        vn.TranscriptSegmentError,
        "voicevox start>end transcript",
    )

    good = {"segments": [{"text": "hi", "start": 0, "end": 1000}]}
    out = vn.collect_chunks(Args(), good)
    assert_eq(len(out), 1, "voicevox good transcript len")
    assert_eq(out[0]["sourceStartMs"], 0, "voicevox sourceStartMs")
    assert_eq(out[0]["sourceEndMs"], 1000, "voicevox sourceEndMs")

    # Codex Phase 3-J review P2 #1 反映: validate を `.get(...).strip()` 前に通す
    # 非 dict segment → TranscriptSegmentError
    assert_raises(
        lambda: vn.collect_chunks(Args(), {"segments": ["not a dict"]}),
        vn.TranscriptSegmentError,
        "voicevox non-dict segment",
    )
    # segments 非 list → TranscriptSegmentError
    assert_raises(
        lambda: vn.collect_chunks(Args(), {"segments": "wrong"}),
        vn.TranscriptSegmentError,
        "voicevox non-list segments",
    )
    # text 非 str (int) → TranscriptSegmentError
    assert_raises(
        lambda: vn.collect_chunks(Args(), {"segments": [{"text": 123}]}),
        vn.TranscriptSegmentError,
        "voicevox text non-str",
    )
    # text=None は filter (空文字列と同じ扱い、空 list 返す)
    assert_eq(
        vn.collect_chunks(Args(), {"segments": [{"text": None, "start": 0, "end": 100}]}),
        [],
        "voicevox text=None filtered",
    )


def test_voicevox_write_narration_data_alignment() -> None:
    """transcript timing alignment が cut-aware で正しく動く end-to-end."""
    import voicevox_narration as vn

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        vn.PROJ = proj
        vn.NARRATION_DIR = proj / "public" / "narration"
        vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
        vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
        vn.NARRATION_DIR.mkdir(parents=True)
        vn.NARRATION_DATA_TS.parent.mkdir(parents=True)

        write_synthetic_wav(vn.NARRATION_DIR / "chunk_000.wav", 1.0)
        write_synthetic_wav(vn.NARRATION_DIR / "chunk_001.wav", 0.5)

        # No cut, transcript timing 0ms と 1000ms
        chunks_data = [
            (vn.NARRATION_DIR / "chunk_000.wav", "first", 0, 1000),
            (vn.NARRATION_DIR / "chunk_001.wav", "second", 1000, 1500),
        ]
        segments, ts_path, meta_path = vn.write_narration_data(chunks_data, 30, [])
        assert_eq(segments[0]["startFrame"], 0, "chunk0 startFrame")
        assert_eq(segments[0]["durationInFrames"], 30, "chunk0 dur")
        assert_eq(segments[0]["timing_source"], "transcript_aligned", "chunk0 source")
        assert_eq(segments[1]["startFrame"], 30, "chunk1 startFrame (1000ms*30fps)")

        # Verify TS file is valid
        ts = ts_path.read_text(encoding="utf-8")
        assert "narrationData" in ts
        assert "sourceStartMs: 0" in ts
        assert "sourceStartMs: 1000" in ts


def main() -> int:
    tests = [
        test_fps_consistency,
        test_vad_schema_validation,
        test_ms_to_playback_frame,
        test_load_cut_segments_fail_fast,
        test_transcript_segment_validation,
        test_voicevox_collect_chunks_validation,
        test_voicevox_write_narration_data_alignment,
    ]
    failed = []
    for t in tests:
        name = t.__name__
        try:
            t()
            print(f"  [OK]   {name}")
        except AssertionError as e:
            failed.append((name, str(e)))
            print(f"  [FAIL] {name}: {e}", file=sys.stderr)
        except Exception as e:
            failed.append((name, f"{type(e).__name__}: {e}"))
            print(f"  [ERR]  {name}: {type(e).__name__}: {e}", file=sys.stderr)

    total = len(tests)
    print(f"\nResult: {total - len(failed)}/{total} pass, {len(failed)} fail")
    if failed:
        for name, msg in failed:
            print(f"  - {name}: {msg}", file=sys.stderr)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

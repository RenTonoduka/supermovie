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

    # Phase 3-L (Codex Phase 3-J review Part B 推奨): require_timing=True で
    # start/end 必須化、欠落 / None で raise。
    assert_raises(
        lambda: timeline.validate_transcript_segment(
            {"text": "hi"}, 0, require_timing=True
        ),
        timeline.TranscriptSegmentError,
        "require_timing missing both",
    )
    assert_raises(
        lambda: timeline.validate_transcript_segment(
            {"text": "hi", "start": 0, "end": None}, 0, require_timing=True
        ),
        timeline.TranscriptSegmentError,
        "require_timing end None",
    )
    # OK: require_timing=True + 両方 numeric
    timeline.validate_transcript_segment(
        {"text": "hi", "start": 0, "end": 1000}, 0, require_timing=True
    )

    # validate_transcript_segments 一括 helper
    out = timeline.validate_transcript_segments(
        [{"text": "a", "start": 0, "end": 100}, {"text": "b", "start": 100, "end": 200}],
        require_timing=True,
    )
    assert_eq(len(out), 2, "validate_transcript_segments OK length")
    # 非 list で raise
    assert_raises(
        lambda: timeline.validate_transcript_segments("not a list"),
        timeline.TranscriptSegmentError,
        "validate_transcript_segments non-list",
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


def _setup_temp_project(tmp: Path, fps: int = 30) -> Path:
    """build_slide / build_telop が読む最小ファイルを temp project に揃える."""
    (tmp / "src").mkdir(parents=True, exist_ok=True)
    (tmp / "src" / "videoConfig.ts").write_text(make_videoconfig_ts(fps))
    (tmp / "src" / "Slides").mkdir(parents=True, exist_ok=True)
    (tmp / "src" / "テロップテンプレート").mkdir(parents=True, exist_ok=True)
    return tmp


def test_build_slide_data_main_e2e() -> None:
    """build_slide_data.py を temp project で main() 実行、SlideData.ts 出力を検証.

    Codex Phase 3-L 推奨 vi 反映: integration_smoke を build_slide にも展開。
    monkey-patch (PROJ / FPS) で in-process 実行。
    """
    import importlib
    import build_slide_data as bsd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        # 通常 transcript: 2 segments
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "duration_ms": 5000,
                    "text": "test",
                    "segments": [
                        {"text": "hello", "start": 0, "end": 2000},
                        {"text": "world", "start": 2000, "end": 4000},
                    ],
                    "words": [],
                }
            ),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロフェッショナル"}),
            encoding="utf-8",
        )

        # monkey-patch PROJ + FPS (import time に固定されるため re-binding 必要)
        original_proj = bsd.PROJ
        original_fps = bsd.FPS
        bsd.PROJ = proj
        bsd.FPS = 30
        try:
            # main() を直接呼出 (引数は空 → topic mode default)
            import sys as _sys

            old_argv = _sys.argv
            _sys.argv = ["build_slide_data.py"]
            try:
                bsd.main()
            finally:
                _sys.argv = old_argv

            # slideData.ts が生成されたか
            slide_ts = proj / "src" / "Slides" / "slideData.ts"
            if not slide_ts.exists():
                raise AssertionError(f"slideData.ts not generated at {slide_ts}")
            content = slide_ts.read_text(encoding="utf-8")
            if "slideData" not in content:
                raise AssertionError(f"slideData.ts does not export slideData: {content[:100]}")
        finally:
            bsd.PROJ = original_proj
            bsd.FPS = original_fps


def test_build_slide_data_validates_bad_transcript() -> None:
    """build_slide_data.py が壊れた transcript で SystemExit する."""
    import build_slide_data as bsd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        # 壊れた transcript: start > end
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "segments": [{"text": "hi", "start": 1000, "end": 500}],
                    "words": [],
                }
            ),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロフェッショナル"}),
            encoding="utf-8",
        )

        original_proj = bsd.PROJ
        bsd.PROJ = proj
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["build_slide_data.py"]
            try:
                bsd.main()
                raise AssertionError("build_slide_data should fail with bad transcript")
            except SystemExit as e:
                # 期待: validation error message
                msg = str(e)
                if "transcript validation failed" not in msg:
                    raise AssertionError(f"Expected validation error, got: {msg}")
            finally:
                _sys.argv = old_argv
        finally:
            bsd.PROJ = original_proj


def test_build_telop_data_main_e2e() -> None:
    """build_telop_data.py を temp project で main() 実行、call_budoux stub.

    Codex Phase 3-L 推奨 vi 拡張 (Phase 3-M 候補 i): build_telop も e2e。
    Node 依存の budoux_split.mjs は deterministic stub に差し替え。
    """
    import build_telop_data as btd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "duration_ms": 5000,
                    "text": "test",
                    "segments": [
                        {"text": "こんにちは世界", "start": 0, "end": 2000},
                        {"text": "さようなら空", "start": 2000, "end": 4000},
                    ],
                    "words": [],
                }
            ),
            encoding="utf-8",
        )
        (proj / "vad_result.json").write_text(
            json.dumps(
                {"speech_segments": [{"start": 0, "end": 4000}]}
            ),
            encoding="utf-8",
        )

        # call_budoux stub: text を 4文字毎に分割した phrases に変換
        def stub_call_budoux(seg_texts):
            return [
                [t[i : i + 4] for i in range(0, len(t), 4)] or [t]
                for t in seg_texts
            ]

        original_proj = btd.PROJ
        original_call = btd.call_budoux
        btd.PROJ = proj
        btd.call_budoux = stub_call_budoux
        try:
            import sys as _sys

            old_argv = _sys.argv
            _sys.argv = ["build_telop_data.py"]
            try:
                btd.main()
            finally:
                _sys.argv = old_argv
            # telopData.ts が生成されたか
            telop_ts = proj / "src" / "テロップテンプレート" / "telopData.ts"
            if not telop_ts.exists():
                raise AssertionError(f"telopData.ts not generated at {telop_ts}")
            content = telop_ts.read_text(encoding="utf-8")
            if "telopData" not in content:
                raise AssertionError(
                    f"telopData.ts does not export telopData: {content[:100]}"
                )
        finally:
            btd.PROJ = original_proj
            btd.call_budoux = original_call


def test_build_telop_data_validates_bad_transcript() -> None:
    """build_telop_data.py が壊れた transcript で SystemExit する."""
    import build_telop_data as btd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "segments": [{"text": "hi", "start": 1000, "end": 500}],
                    "words": [],
                }
            ),
            encoding="utf-8",
        )
        (proj / "vad_result.json").write_text(
            json.dumps({"speech_segments": [{"start": 0, "end": 1000}]}),
            encoding="utf-8",
        )

        original_proj = btd.PROJ
        original_call = btd.call_budoux
        btd.PROJ = proj
        # call_budoux stub (validation 前で raise されるので invoke されない想定)
        btd.call_budoux = lambda x: [["dummy"] for _ in x]
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["build_telop_data.py"]
            try:
                btd.main()
                raise AssertionError(
                    "build_telop_data should fail with bad transcript"
                )
            except SystemExit as e:
                msg = str(e)
                if "transcript validation failed" not in msg:
                    raise AssertionError(f"Expected validation error, got: {msg}")
            finally:
                _sys.argv = old_argv
        finally:
            btd.PROJ = original_proj
            btd.call_budoux = original_call


def test_generate_slide_plan_skip_no_api_key() -> None:
    """generate_slide_plan.py: ANTHROPIC_API_KEY 未設定で exit 0 (skip)."""
    import generate_slide_plan as gsp
    import os as _os

    original_proj = gsp.PROJ
    with tempfile.TemporaryDirectory() as tmp:
        gsp.PROJ = Path(tmp)
        original_key = _os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["generate_slide_plan.py"]
            try:
                ret = gsp.main()
                assert_eq(ret, 0, "no-api-key skip exit 0")
            finally:
                _sys.argv = old_argv
        finally:
            if original_key is not None:
                _os.environ["ANTHROPIC_API_KEY"] = original_key
            gsp.PROJ = original_proj


def test_generate_slide_plan_missing_inputs() -> None:
    """generate_slide_plan.py: transcript / config 不在で exit 3."""
    import generate_slide_plan as gsp
    import os as _os

    original_proj = gsp.PROJ
    with tempfile.TemporaryDirectory() as tmp:
        gsp.PROJ = Path(tmp)  # transcript_fixed.json / project-config.json なし
        _os.environ["ANTHROPIC_API_KEY"] = "test-key-fake"
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["generate_slide_plan.py"]
            try:
                ret = gsp.main()
                assert_eq(ret, 3, "missing inputs exit 3")
            finally:
                _sys.argv = old_argv
        finally:
            del _os.environ["ANTHROPIC_API_KEY"]
            gsp.PROJ = original_proj


def test_build_scripts_wiring() -> None:
    """build_slide_data / build_telop_data が timeline 経由で正しく wire されている."""
    import importlib
    bsd = importlib.import_module("build_slide_data")
    btd = importlib.import_module("build_telop_data")

    # FPS が videoConfig.ts から読まれている (Phase 3-J 統合確認)
    if bsd.FPS <= 0:
        raise AssertionError(f"build_slide_data FPS should be positive, got {bsd.FPS}")
    if btd.FPS <= 0:
        raise AssertionError(f"build_telop_data FPS should be positive, got {btd.FPS}")

    # validate_transcript_segment が timeline から wire されている
    if bsd.validate_transcript_segment is None:
        raise AssertionError("build_slide_data should import validate_transcript_segment")
    if btd.validate_transcript_segment is None:
        raise AssertionError("build_telop_data should import validate_transcript_segment")

    # build_slide_data の cut helper wrapper が timeline 経由で動く
    cuts = bsd.build_cut_segments_from_vad(
        {"speech_segments": [{"start": 0, "end": 1000}]}
    )
    assert_eq(len(cuts), 1, "bsd.build_cut_segments_from_vad len")
    assert_eq(cuts[0]["originalStartMs"], 0, "bsd cuts[0] originalStartMs")

    # build_telop_data の cut helper も validate_vad_schema 経由
    cuts_t = btd.build_cut_segments_from_vad(
        {"speech_segments": [{"start": 0, "end": 1000}]}
    )
    assert_eq(len(cuts_t), 1, "btd.build_cut_segments_from_vad len")

    # 壊れた VAD で raise (3 script で挙動統一の確認)
    bad_vad = {"speech_segments": [{"start": 100, "end": 50}]}
    assert_raises(
        lambda: bsd.build_cut_segments_from_vad(bad_vad),
        timeline.VadSchemaError,
        "bsd raises VadSchemaError",
    )
    assert_raises(
        lambda: btd.build_cut_segments_from_vad(bad_vad),
        timeline.VadSchemaError,
        "btd raises VadSchemaError",
    )


def main() -> int:
    tests = [
        test_fps_consistency,
        test_vad_schema_validation,
        test_ms_to_playback_frame,
        test_load_cut_segments_fail_fast,
        test_transcript_segment_validation,
        test_voicevox_collect_chunks_validation,
        test_voicevox_write_narration_data_alignment,
        test_build_scripts_wiring,
        test_build_slide_data_main_e2e,
        test_build_slide_data_validates_bad_transcript,
        test_build_telop_data_main_e2e,
        test_build_telop_data_validates_bad_transcript,
        test_generate_slide_plan_skip_no_api_key,
        test_generate_slide_plan_missing_inputs,
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

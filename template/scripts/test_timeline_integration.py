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


def test_voicevox_write_order_narrationdata_before_wav() -> None:
    """Phase 3-N race fix regression: write 順序 narrationData.ts → narration.wav.

    旧順序 (narration.wav 先) では Studio hot-reload で legacy 経路に一瞬流れる
    race があった (Codex CODEX_REVIEW_PHASE3N_AND_3O P2 #1)。新順序を保証する
    ため、本 test は call order を直接 verify する:

    1. main() を temp project + module-level state monkey-patch で実行
    2. concat_wavs_atomic を「narrationData.ts 存在を assert する mock」で
       置換、call 時点で narrationData.ts populated でないなら raise
    3. 旧順序に戻れば assert で必ず落ちる

    Codex Phase 3-O fix re-review P2 #2 反映 (旧 test は逆順でも通る)。
    """
    import voicevox_narration as vn

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
    }
    original_concat = vn.concat_wavs_atomic
    original_check_engine = vn.check_engine
    original_synthesize = vn.synthesize

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "src" / "videoConfig.ts").write_text(
                make_videoconfig_ts(30), encoding="utf-8"
            )
            # transcript で 1 chunk 用意
            (proj / "transcript_fixed.json").write_text(
                json.dumps(
                    {"segments": [{"text": "hi", "start": 0, "end": 1000}]}
                ),
                encoding="utf-8",
            )

            # engine OK + synthesize stub (synthetic 22050Hz mono WAV bytes)
            import wave
            import io

            buf = io.BytesIO()
            with wave.open(buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(22050)
                import struct
                w.writeframes(struct.pack("<22050h", *([0] * 22050)))
            wav_bytes = buf.getvalue()

            vn.check_engine = lambda: (True, "0.0.0-test")
            vn.synthesize = lambda text, speaker: wav_bytes

            # concat_wavs_atomic を「narrationData.ts populated を assert + raise」に
            order_check_log = []

            def assert_concat_after_narrationdata(wavs, out_path):
                # narrationData.ts 存在 + 空 array でないことを確認
                if not vn.NARRATION_DATA_TS.exists():
                    order_check_log.append("FAIL: narrationData.ts not created before concat")
                    raise RuntimeError("write order regression: narrationData.ts missing")
                content = vn.NARRATION_DATA_TS.read_text(encoding="utf-8")
                if "narration/chunk_000.wav" not in content:
                    order_check_log.append(
                        f"FAIL: narrationData.ts not populated before concat: {content[:100]}"
                    )
                    raise RuntimeError("write order regression: narrationData.ts empty")
                order_check_log.append("OK: narrationData.ts populated before concat")
                # 失敗を演じて rollback path を起動 (P1 fix の Exception catch)
                raise PermissionError("simulated permission error")

            vn.concat_wavs_atomic = assert_concat_after_narrationdata

            # main() を実行、concat で失敗 → exit 6 期待
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["voicevox_narration.py"]
            try:
                ret = vn.main()
            finally:
                _sys.argv = old_argv

            # call order assertion
            if not order_check_log:
                raise AssertionError("concat mock not invoked (main() flow regression)")
            if "OK:" not in order_check_log[0]:
                raise AssertionError(
                    f"write order regression detected: {order_check_log}"
                )
            # exit code: rollback path の return 6 を期待 (Codex P1 fix が動作)
            assert_eq(ret, 6, "concat failure → exit 6 (P1 rollback)")
            # rollback 後: narrationData.ts は empty に戻り、chunks 削除済み
            content = vn.NARRATION_DATA_TS.read_text(encoding="utf-8")
            if "export const narrationData: NarrationSegment[] = []" not in content:
                raise AssertionError(
                    f"rollback failed: narrationData.ts not empty: {content[:100]}"
                )
            chunk_files = list(vn.NARRATION_DIR.glob("chunk_*.wav"))
            if chunk_files:
                raise AssertionError(f"rollback failed: chunks left: {chunk_files}")
    finally:
        for k, v in state.items():
            setattr(vn, k, v)
        vn.concat_wavs_atomic = original_concat
        vn.check_engine = original_check_engine
        vn.synthesize = original_synthesize


def test_voicevox_write_narration_data_alignment() -> None:
    """transcript timing alignment が cut-aware で正しく動く end-to-end."""
    import voicevox_narration as vn

    # Codex Phase 3-L re-review P3 #2 反映: module-level state を try/finally で
    # restore (test 間 leak 防止、後続 voicevox test 追加時の汚染回避)。
    original_proj = vn.PROJ
    original_narration_dir = vn.NARRATION_DIR
    original_narration_data_ts = vn.NARRATION_DATA_TS
    original_chunk_meta_json = vn.CHUNK_META_JSON
    original_narration_legacy_wav = vn.NARRATION_LEGACY_WAV

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
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
    finally:
        vn.PROJ = original_proj
        vn.NARRATION_DIR = original_narration_dir
        vn.NARRATION_DATA_TS = original_narration_data_ts
        vn.CHUNK_META_JSON = original_chunk_meta_json
        vn.NARRATION_LEGACY_WAV = original_narration_legacy_wav


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
    # Codex Phase 3-M review P2 #2 反映: 既存 ANTHROPIC_API_KEY を save、
    # finally で復元 (test 間の env leak 防止)。
    original_api_key = _os.environ.get("ANTHROPIC_API_KEY")
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
            if original_api_key is None:
                _os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                _os.environ["ANTHROPIC_API_KEY"] = original_api_key
            gsp.PROJ = original_proj


def test_generate_slide_plan_api_mock_success() -> None:
    """generate_slide_plan API mock: valid response → slide_plan.json 生成.

    Codex Phase 3-M cand iii の残置部分 (urllib mock + valid response 検証)。
    """
    import generate_slide_plan as gsp
    import os as _os
    import urllib.request as _urlreq

    fake_plan = {
        "version": gsp.PLAN_VERSION,
        "slides": [
            {
                "id": 1,
                "startWordIndex": 0,
                "endWordIndex": 0,
                "title": "テスト",
                "bullets": [],
                "align": "left",
            }
        ],
    }
    fake_response_body = json.dumps(
        {"content": [{"type": "text", "text": json.dumps(fake_plan, ensure_ascii=False)}]}
    ).encode("utf-8")

    class FakeResponse:
        def __init__(self, body):
            self._body = body

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            pass

        def read(self):
            return self._body

    def mock_urlopen(req, timeout=60):
        return FakeResponse(fake_response_body)

    original_urlopen = _urlreq.urlopen
    original_proj = gsp.PROJ
    original_api_key = _os.environ.get("ANTHROPIC_API_KEY")  # Codex P2 #2 反映

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        gsp.PROJ = proj
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "words": [{"text": "hi", "start": 0, "end": 100}],
                    "segments": [{"text": "hi", "start": 0, "end": 100}],
                }
            ),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロ"}),
            encoding="utf-8",
        )

        _os.environ["ANTHROPIC_API_KEY"] = "fake-key"
        _urlreq.urlopen = mock_urlopen
        try:
            import sys as _sys
            old_argv = _sys.argv
            output_path = proj / "slide_plan.json"
            _sys.argv = ["generate_slide_plan.py", "--output", str(output_path)]
            try:
                ret = gsp.main()
                assert_eq(ret, 0, "API mock success exit 0")
                if not output_path.exists():
                    raise AssertionError(f"slide_plan.json not generated at {output_path}")
                plan = json.loads(output_path.read_text(encoding="utf-8"))
                assert_eq(plan["version"], gsp.PLAN_VERSION, "plan version")
                assert_eq(len(plan["slides"]), 1, "plan slides count")
            finally:
                _sys.argv = old_argv
        finally:
            if original_api_key is None:
                _os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                _os.environ["ANTHROPIC_API_KEY"] = original_api_key
            _urlreq.urlopen = original_urlopen
            gsp.PROJ = original_proj


def test_generate_slide_plan_api_http_error() -> None:
    """generate_slide_plan API mock: HTTP error → exit 4."""
    import generate_slide_plan as gsp
    import os as _os
    import urllib.error as _urlerr
    import urllib.request as _urlreq
    from io import BytesIO

    def mock_urlopen_http_error(req, timeout=60):
        raise _urlerr.HTTPError(
            "https://api.anthropic.com/v1/messages",
            429,
            "Rate Limit",
            {},
            BytesIO(b'{"error": {"type": "rate_limit_error"}}'),
        )

    original_urlopen = _urlreq.urlopen
    original_proj = gsp.PROJ
    original_api_key = _os.environ.get("ANTHROPIC_API_KEY")  # Codex P2 #2 反映

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        gsp.PROJ = proj
        (proj / "transcript_fixed.json").write_text(
            json.dumps({"words": [], "segments": []}),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロ"}),
            encoding="utf-8",
        )
        _os.environ["ANTHROPIC_API_KEY"] = "fake-key"
        _urlreq.urlopen = mock_urlopen_http_error
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["generate_slide_plan.py"]
            try:
                ret = gsp.main()
                assert_eq(ret, 4, "API HTTP error → exit 4")
            finally:
                _sys.argv = old_argv
        finally:
            if original_api_key is None:
                _os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                _os.environ["ANTHROPIC_API_KEY"] = original_api_key
            _urlreq.urlopen = original_urlopen
            gsp.PROJ = original_proj


def test_generate_slide_plan_api_invalid_json() -> None:
    """generate_slide_plan API mock: response が JSON parse 失敗 → exit 5."""
    import generate_slide_plan as gsp
    import os as _os
    import urllib.request as _urlreq

    invalid_response = json.dumps(
        {"content": [{"type": "text", "text": "this is not json {{{"}]}
    ).encode("utf-8")

    class FakeResponse:
        def __init__(self, body):
            self._body = body

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            pass

        def read(self):
            return self._body

    def mock_urlopen(req, timeout=60):
        return FakeResponse(invalid_response)

    original_urlopen = _urlreq.urlopen
    original_proj = gsp.PROJ
    original_api_key = _os.environ.get("ANTHROPIC_API_KEY")  # Codex P2 #2 反映

    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        gsp.PROJ = proj
        (proj / "transcript_fixed.json").write_text(
            json.dumps({"words": [], "segments": []}),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロ"}),
            encoding="utf-8",
        )
        _os.environ["ANTHROPIC_API_KEY"] = "fake-key"
        _urlreq.urlopen = mock_urlopen
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["generate_slide_plan.py"]
            try:
                ret = gsp.main()
                assert_eq(ret, 5, "API invalid JSON → exit 5")
            finally:
                _sys.argv = old_argv
        finally:
            if original_api_key is None:
                _os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                _os.environ["ANTHROPIC_API_KEY"] = original_api_key
            _urlreq.urlopen = original_urlopen
            gsp.PROJ = original_proj


def test_build_slide_data_plan_validation_fallback() -> None:
    """build_slide_data --plan で validate 失敗 → deterministic fallback (default).

    Codex Phase 3-M review P2 #3 反映: API mock の出口に build_slide_data
    を繋いで schema validation 経路まで踏む integration test。
    """
    import build_slide_data as bsd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        # 通常 transcript
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "duration_ms": 4000,
                    "text": "test",
                    "segments": [
                        {"text": "hello", "start": 0, "end": 2000},
                        {"text": "world", "start": 2000, "end": 4000},
                    ],
                    "words": [
                        {"text": "hello", "start": 0, "end": 1000},
                        {"text": "world", "start": 2000, "end": 3000},
                    ],
                }
            ),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロフェッショナル"}),
            encoding="utf-8",
        )
        # 壊れた slide_plan: 必須 version 欠落
        bad_plan = {
            "slides": [
                {
                    "id": 1,
                    "startWordIndex": 0,
                    "endWordIndex": 1,
                    "title": "test",
                    "bullets": [],
                    "align": "left",
                }
            ]
        }
        plan_path = proj / "bad_plan.json"
        plan_path.write_text(json.dumps(bad_plan), encoding="utf-8")

        original_proj = bsd.PROJ
        bsd.PROJ = proj
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = [
                "build_slide_data.py",
                "--plan",
                str(plan_path),
                # default: validation 失敗で WARN + deterministic fallback
            ]
            try:
                bsd.main()
                # fallback 経路: deterministic で slideData.ts 生成
                slide_ts = proj / "src" / "Slides" / "slideData.ts"
                if not slide_ts.exists():
                    raise AssertionError(
                        f"slideData.ts not generated (fallback expected): {slide_ts}"
                    )
            finally:
                _sys.argv = old_argv
        finally:
            bsd.PROJ = original_proj


def test_build_slide_data_plan_strict_failure() -> None:
    """build_slide_data --plan + --strict-plan で validate 失敗 → SystemExit 2."""
    import build_slide_data as bsd

    with tempfile.TemporaryDirectory() as tmp:
        proj = _setup_temp_project(Path(tmp))
        (proj / "transcript_fixed.json").write_text(
            json.dumps(
                {
                    "duration_ms": 2000,
                    "text": "test",
                    "segments": [{"text": "hello", "start": 0, "end": 2000}],
                    "words": [{"text": "hello", "start": 0, "end": 1000}],
                }
            ),
            encoding="utf-8",
        )
        (proj / "project-config.json").write_text(
            json.dumps({"format": "short", "tone": "プロ"}),
            encoding="utf-8",
        )
        # 壊れた plan: version 欠落
        bad_plan = {"slides": []}
        plan_path = proj / "bad_plan.json"
        plan_path.write_text(json.dumps(bad_plan), encoding="utf-8")

        original_proj = bsd.PROJ
        bsd.PROJ = proj
        try:
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = [
                "build_slide_data.py",
                "--plan",
                str(plan_path),
                "--strict-plan",
            ]
            try:
                bsd.main()
                raise AssertionError(
                    "build_slide_data --strict-plan should fail with bad plan"
                )
            except SystemExit as e:
                # exit code 2 期待 (strict-plan + validation error)
                code = e.code if e.code is not None else 0
                assert_eq(code, 2, "strict-plan validation failure → exit 2")
            finally:
                _sys.argv = old_argv
        finally:
            bsd.PROJ = original_proj


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


def test_ms_to_playback_frame_edge_cases() -> None:
    """ms_to_playback_frame の境界・degenerate ケース (Phase 3 post-freeze 補強)."""
    cut_segs = [
        {"originalStartMs": 0, "originalEndMs": 500, "playbackStart": 0, "playbackEnd": 15},
        {"originalStartMs": 1500, "originalEndMs": 3000, "playbackStart": 15, "playbackEnd": 60},
    ]
    # 境界 inclusive: <= / >=
    assert_eq(timeline.ms_to_playback_frame(0, 30, cut_segs), 0, "boundary seg0 originalStartMs")
    assert_eq(timeline.ms_to_playback_frame(500, 30, cut_segs), 15, "boundary seg0 originalEndMs")
    assert_eq(timeline.ms_to_playback_frame(3000, 30, cut_segs), 60, "boundary seg1 originalEndMs")

    # cut 範囲外 (隙間 / 全体外)
    assert_eq(timeline.ms_to_playback_frame(501, 30, cut_segs), None, "1ms after seg0 end (gap)")
    assert_eq(timeline.ms_to_playback_frame(1499, 30, cut_segs), None, "1ms before seg1 start (gap)")
    assert_eq(timeline.ms_to_playback_frame(3500, 30, cut_segs), None, "after all cuts")

    # Single cut
    single = [{"originalStartMs": 100, "originalEndMs": 600, "playbackStart": 0, "playbackEnd": 15}]
    assert_eq(timeline.ms_to_playback_frame(100, 30, single), 0, "single cut at originalStart")
    assert_eq(timeline.ms_to_playback_frame(50, 30, single), None, "single cut before range")
    assert_eq(timeline.ms_to_playback_frame(700, 30, single), None, "single cut after range")

    # fps boundary
    assert_eq(timeline.ms_to_playback_frame(1000, 1, []), 1, "no-cut fps=1 1s")
    assert_eq(timeline.ms_to_playback_frame(1000, 120, []), 120, "no-cut fps=120 1s")

    # Adjacent cuts (gap=0): seg0 ends at 500, seg1 starts at 500.
    # 仕様: for-loop が最初に matching 要素を返す。境界値で両方 match だが
    # 累積 playback の連続性により同じ frame に着地する。
    adjacent = [
        {"originalStartMs": 0, "originalEndMs": 500, "playbackStart": 0, "playbackEnd": 15},
        {"originalStartMs": 500, "originalEndMs": 1000, "playbackStart": 15, "playbackEnd": 30},
    ]
    assert_eq(
        timeline.ms_to_playback_frame(500, 30, adjacent), 15,
        "adjacent cuts boundary 500: seg0 first match, both yield 15",
    )
    assert_eq(
        timeline.ms_to_playback_frame(600, 30, adjacent), 18,
        "adjacent cuts: 600ms in seg1, offset=100ms, 15+round(3.0)=18",
    )


def test_load_cut_segments_edge_cases() -> None:
    """load_cut_segments の corner case (空 / 単一 / 不在)."""
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        # vad_result.json 不在 → []
        assert_eq(timeline.load_cut_segments(proj, 30), [], "no vad file returns empty")

        # 空 speech_segments → []
        (proj / "vad_result.json").write_text(
            json.dumps({"speech_segments": [], "duration_ms": 5000}),
            encoding="utf-8",
        )
        result = timeline.load_cut_segments(proj, 30)
        assert_eq(len(result), 0, "empty speech_segments → []")

        # 単一 speech_segment → 1 要素 with playback frames
        (proj / "vad_result.json").write_text(
            json.dumps({
                "speech_segments": [{"start": 200, "end": 1200}],
                "duration_ms": 5000,
            }),
            encoding="utf-8",
        )
        result = timeline.load_cut_segments(proj, 30)
        assert_eq(len(result), 1, "single speech_segment → 1 cut")
        assert_eq(result[0]["originalStartMs"], 200, "single seg originalStartMs")
        assert_eq(result[0]["originalEndMs"], 1200, "single seg originalEndMs")
        assert_eq(result[0]["playbackStart"], 0, "single seg playbackStart=0")
        assert_eq(result[0]["playbackEnd"], 30, "single seg playbackEnd=30 (1s @ 30fps)")


def test_build_cut_segments_multi_with_gaps() -> None:
    """build_cut_segments_from_vad で複数 speech segment + gap removal を検証."""
    vad = {
        "speech_segments": [
            {"start": 0, "end": 1000},      # 1.0s
            {"start": 2000, "end": 3500},   # 1.5s (gap 1000ms 除去)
            {"start": 5000, "end": 6000},   # 1.0s
        ],
        "duration_ms": 7000,
    }
    cuts = timeline.build_cut_segments_from_vad(vad, 30)
    assert_eq(len(cuts), 3, "3 segments expected")

    # seg 0: original 0→1000、playback 0→30 (1s @ 30fps)
    assert_eq(cuts[0]["playbackStart"], 0, "seg0 playbackStart")
    assert_eq(cuts[0]["playbackEnd"], 30, "seg0 playbackEnd")

    # seg 1: original 2000→3500、cumulative 1000→2500ms → playback 30→75
    assert_eq(cuts[1]["playbackStart"], 30, "seg1 playbackStart (cumulative 1000ms = 30 frames)")
    assert_eq(cuts[1]["playbackEnd"], 75, "seg1 playbackEnd (cumulative 2500ms = 75 frames)")

    # seg 2: original 5000→6000、cumulative 2500→3500ms → playback 75→105
    assert_eq(cuts[2]["playbackStart"], 75, "seg2 playbackStart (cumulative 2500ms = 75 frames)")
    assert_eq(cuts[2]["playbackEnd"], 105, "seg2 playbackEnd (cumulative 3500ms = 105 frames)")


def test_voicevox_cleanup_stale_unlinks_sentinel() -> None:
    """Phase 3-V P5: cleanup_stale_all() が stale narration.ready.json を削除."""
    import voicevox_narration as vn

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
        "NARRATION_READY_JSON": vn.NARRATION_READY_JSON,
    }
    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            vn.NARRATION_READY_JSON = proj / "public" / "narration.ready.json"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "public").mkdir(parents=True)

            # Pre-create stale sentinel + stale narrationData.ts
            vn.NARRATION_READY_JSON.write_text(
                '{"schemaVersion":1,"status":"ready","chunkCount":3,"totalFrames":99,"generatedAtMs":1000}',
                encoding="utf-8",
            )
            vn.NARRATION_DATA_TS.write_text(
                "// stale stub\nexport const narrationData = [];\n", encoding="utf-8"
            )
            if not vn.NARRATION_READY_JSON.exists():
                raise AssertionError("pre-cond: stale sentinel must exist")

            vn.cleanup_stale_all()

            if vn.NARRATION_READY_JSON.exists():
                raise AssertionError(
                    "cleanup_stale_all failed to remove stale narration.ready.json"
                )
    finally:
        for k, v in state.items():
            setattr(vn, k, v)


def test_voicevox_sentinel_written_after_wav() -> None:
    """Phase 3-V P5: sentinel write 順序 narration.wav → narration.ready.json verify.

    write_narration_ready の mock が「narration.wav existence を assert + 元実装に
    delegate」する形で、call 時点で narration.wav が出ていなければ raise。旧順序
    (sentinel 先) に regress すると必ず fail。
    """
    import voicevox_narration as vn

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
        "NARRATION_READY_JSON": vn.NARRATION_READY_JSON,
    }
    original_concat = vn.concat_wavs_atomic
    original_check_engine = vn.check_engine
    original_synthesize = vn.synthesize
    original_write_ready = vn.write_narration_ready

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            vn.NARRATION_READY_JSON = proj / "public" / "narration.ready.json"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "src" / "videoConfig.ts").write_text(
                make_videoconfig_ts(30), encoding="utf-8"
            )
            (proj / "transcript_fixed.json").write_text(
                json.dumps({"segments": [{"text": "hi", "start": 0, "end": 1000}]}),
                encoding="utf-8",
            )

            import wave as _wave
            import io as _io
            import struct as _struct

            buf = _io.BytesIO()
            with _wave.open(buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(22050)
                w.writeframes(_struct.pack("<22050h", *([0] * 22050)))
            wav_bytes = buf.getvalue()

            vn.check_engine = lambda: (True, "0.0.0-test")
            vn.synthesize = lambda text, speaker: wav_bytes

            # concat: 実際に narration.wav を書く (next step で sentinel check が exists を見る)
            def real_concat(wavs, out_path):
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(wav_bytes)

            vn.concat_wavs_atomic = real_concat

            # sentinel write 順序 check + delegate
            order_log = []

            def assert_sentinel_after_wav(chunk_count, total_frames):
                if not vn.NARRATION_LEGACY_WAV.exists():
                    order_log.append("FAIL: narration.wav missing when sentinel write called")
                    raise RuntimeError("write order regression: narration.wav missing")
                order_log.append("OK: narration.wav exists before sentinel write")
                original_write_ready(chunk_count, total_frames)

            vn.write_narration_ready = assert_sentinel_after_wav

            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["voicevox_narration.py"]
            try:
                ret = vn.main()
            finally:
                _sys.argv = old_argv

            assert_eq(ret, 0, "successful main() exit 0")
            if not order_log or "OK:" not in order_log[0]:
                raise AssertionError(
                    f"sentinel write order regression: {order_log}"
                )
            if not vn.NARRATION_READY_JSON.exists():
                raise AssertionError("sentinel file not created after success")
            payload = json.loads(vn.NARRATION_READY_JSON.read_text(encoding="utf-8"))
            assert_eq(payload.get("schemaVersion"), 1, "sentinel schemaVersion=1")
            assert_eq(payload.get("status"), "ready", "sentinel status=ready")
            assert_eq(payload.get("chunkCount"), 1, "sentinel chunkCount=1")
            if not isinstance(payload.get("totalFrames"), int):
                raise AssertionError(
                    f"sentinel totalFrames must be int, got {type(payload.get('totalFrames'))}"
                )
            if not isinstance(payload.get("generatedAtMs"), int):
                raise AssertionError(
                    f"sentinel generatedAtMs must be int, got {type(payload.get('generatedAtMs'))}"
                )
    finally:
        for k, v in state.items():
            setattr(vn, k, v)
        vn.concat_wavs_atomic = original_concat
        vn.check_engine = original_check_engine
        vn.synthesize = original_synthesize
        vn.write_narration_ready = original_write_ready


def test_voicevox_sentinel_write_fail_rollback() -> None:
    """Phase 3-V P5 review P2 #3 + P1 反映: write_narration_ready 失敗時の rollback.

    sentinel write を強制 OSError で fail させ、rollback path で chunks /
    out_path / narrationData.ts / sentinel が全削除されること、custom --output
    指定時も out_path が unlink されることを verify (Codex P5 review P1)。
    """
    import voicevox_narration as vn

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
        "NARRATION_READY_JSON": vn.NARRATION_READY_JSON,
    }
    original_concat = vn.concat_wavs_atomic
    original_check_engine = vn.check_engine
    original_synthesize = vn.synthesize
    original_write_ready = vn.write_narration_ready

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            vn.NARRATION_READY_JSON = proj / "public" / "narration.ready.json"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "src" / "videoConfig.ts").write_text(
                make_videoconfig_ts(30), encoding="utf-8"
            )
            (proj / "transcript_fixed.json").write_text(
                json.dumps({"segments": [{"text": "hi", "start": 0, "end": 1000}]}),
                encoding="utf-8",
            )

            import wave as _wave
            import io as _io
            import struct as _struct

            buf = _io.BytesIO()
            with _wave.open(buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(22050)
                w.writeframes(_struct.pack("<22050h", *([0] * 22050)))
            wav_bytes = buf.getvalue()

            vn.check_engine = lambda: (True, "0.0.0-test")
            vn.synthesize = lambda text, speaker: wav_bytes

            # custom out_path で concat 成功 (P5 review P1: rollback が
            # NARRATION_LEGACY_WAV ではなく out_path を unlink するか verify)
            custom_out = proj / "public" / "custom_narration.wav"

            def real_concat(wavs, out_path):
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(wav_bytes)

            vn.concat_wavs_atomic = real_concat
            vn.write_narration_ready = lambda c, t: (_ for _ in ()).throw(
                OSError("simulated sentinel write failure")
            )

            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["voicevox_narration.py", "--output", str(custom_out)]
            try:
                ret = vn.main()
            finally:
                _sys.argv = old_argv

            assert_eq(ret, 6, "sentinel write fail → exit 6 (rollback path)")
            # all-or-nothing rollback verify
            chunk_files = list(vn.NARRATION_DIR.glob("chunk_*.wav"))
            if chunk_files:
                raise AssertionError(
                    f"rollback failed: chunks left after sentinel fail: {chunk_files}"
                )
            # P5 review P1 fix: custom out_path も unlink される
            if custom_out.exists():
                raise AssertionError(
                    f"P5 review P1 fix regression: custom out_path 残置: {custom_out}"
                )
            # default NARRATION_LEGACY_WAV は元々書かれていない (custom 指定なので)
            # narrationData.ts は empty に reset
            content = vn.NARRATION_DATA_TS.read_text(encoding="utf-8")
            if "export const narrationData: NarrationSegment[] = []" not in content:
                raise AssertionError(
                    f"rollback failed: narrationData.ts not reset: {content[:100]}"
                )
            # sentinel 不在 (write 中に失敗したので)
            if vn.NARRATION_READY_JSON.exists():
                raise AssertionError(
                    "rollback failed: sentinel left after write failure"
                )
            # chunk_meta.json も削除
            if vn.CHUNK_META_JSON.exists():
                raise AssertionError(
                    "rollback failed: chunk_meta.json left after sentinel fail"
                )
    finally:
        for k, v in state.items():
            setattr(vn, k, v)
        vn.concat_wavs_atomic = original_concat
        vn.check_engine = original_check_engine
        vn.synthesize = original_synthesize
        vn.write_narration_ready = original_write_ready


def test_voicevox_sentinel_rollback_on_concat_fail() -> None:
    """Phase 3-V P5: concat 失敗時に sentinel が残らない (all-or-nothing 維持).

    concat_wavs_atomic を強制 PermissionError で fail させ、rollback 経路後に
    NARRATION_READY_JSON が存在しないことを確認。sentinel は concat 後に書く設計
    なので、concat fail 経路では当然書かれないが、defensive verification として明示。
    """
    import voicevox_narration as vn

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
        "NARRATION_READY_JSON": vn.NARRATION_READY_JSON,
    }
    original_concat = vn.concat_wavs_atomic
    original_check_engine = vn.check_engine
    original_synthesize = vn.synthesize

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            vn.NARRATION_READY_JSON = proj / "public" / "narration.ready.json"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "src" / "videoConfig.ts").write_text(
                make_videoconfig_ts(30), encoding="utf-8"
            )
            (proj / "transcript_fixed.json").write_text(
                json.dumps({"segments": [{"text": "hi", "start": 0, "end": 1000}]}),
                encoding="utf-8",
            )

            import wave as _wave
            import io as _io
            import struct as _struct

            buf = _io.BytesIO()
            with _wave.open(buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(22050)
                w.writeframes(_struct.pack("<22050h", *([0] * 22050)))
            wav_bytes = buf.getvalue()

            vn.check_engine = lambda: (True, "0.0.0-test")
            vn.synthesize = lambda text, speaker: wav_bytes
            vn.concat_wavs_atomic = lambda wavs, out_path: (_ for _ in ()).throw(
                PermissionError("simulated concat failure")
            )

            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["voicevox_narration.py"]
            try:
                ret = vn.main()
            finally:
                _sys.argv = old_argv

            assert_eq(ret, 6, "concat failure → exit 6 (rollback path)")
            if vn.NARRATION_READY_JSON.exists():
                raise AssertionError(
                    "sentinel must not exist after concat failure (all-or-nothing 破れ)"
                )
            # rollback: chunks も 削除されている
            chunk_files = list(vn.NARRATION_DIR.glob("chunk_*.wav"))
            if chunk_files:
                raise AssertionError(
                    f"rollback failed: chunks left after concat fail: {chunk_files}"
                )
    finally:
        for k, v in state.items():
            setattr(vn, k, v)
        vn.concat_wavs_atomic = original_concat
        vn.check_engine = original_check_engine
        vn.synthesize = original_synthesize


def test_voicevox_json_log_emits_pure_json() -> None:
    """Phase 3-V 第2弾 P3 (Codex CODEX_NEXT_PRIORITY:15-18):
    --json-log flag で末尾 1 行に純 JSON summary が emit される."""
    import voicevox_narration as vn
    import io as _io
    import contextlib

    state = {
        "PROJ": vn.PROJ,
        "NARRATION_DIR": vn.NARRATION_DIR,
        "NARRATION_DATA_TS": vn.NARRATION_DATA_TS,
        "CHUNK_META_JSON": vn.CHUNK_META_JSON,
        "NARRATION_LEGACY_WAV": vn.NARRATION_LEGACY_WAV,
        "NARRATION_READY_JSON": vn.NARRATION_READY_JSON,
    }
    original_concat = vn.concat_wavs_atomic
    original_check_engine = vn.check_engine
    original_synthesize = vn.synthesize

    try:
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            vn.PROJ = proj
            vn.NARRATION_DIR = proj / "public" / "narration"
            vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
            vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
            vn.NARRATION_LEGACY_WAV = proj / "public" / "narration.wav"
            vn.NARRATION_READY_JSON = proj / "public" / "narration.ready.json"
            (proj / "src" / "Narration").mkdir(parents=True)
            (proj / "src" / "videoConfig.ts").write_text(
                make_videoconfig_ts(30), encoding="utf-8"
            )
            (proj / "transcript_fixed.json").write_text(
                json.dumps({"segments": [{"text": "hi", "start": 0, "end": 1000}]}),
                encoding="utf-8",
            )

            import wave as _wave
            import struct as _struct

            buf = _io.BytesIO()
            with _wave.open(buf, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(22050)
                w.writeframes(_struct.pack("<22050h", *([0] * 22050)))
            wav_bytes = buf.getvalue()

            vn.check_engine = lambda: (True, "0.0.0-test")
            vn.synthesize = lambda text, speaker: wav_bytes
            vn.concat_wavs_atomic = lambda wavs, out: out.write_bytes(wav_bytes)

            captured = _io.StringIO()
            import sys as _sys
            old_argv = _sys.argv
            _sys.argv = ["voicevox_narration.py", "--json-log"]
            try:
                with contextlib.redirect_stdout(captured):
                    ret = vn.main()
            finally:
                _sys.argv = old_argv

            assert_eq(ret, 0, "main() exit 0 with --json-log")
            stdout = captured.getvalue()
            lines = [ln for ln in stdout.splitlines() if ln.strip()]
            if not lines:
                raise AssertionError("--json-log produced no stdout")
            # 末尾行は純 JSON (prefix なし)
            last = lines[-1]
            try:
                payload = json.loads(last)
            except json.JSONDecodeError as e:
                raise AssertionError(
                    f"--json-log last line not pure JSON: {last!r} ({e})"
                ) from e
            # expected key 集
            for key in ("speaker", "fps", "chunks", "total_chunks", "narration_ready_json"):
                if key not in payload:
                    raise AssertionError(
                        f"--json-log missing expected key {key}: {payload}"
                    )
            # 既存 stdout (`summary: {...}` 行) も維持されている
            if not any("summary:" in ln for ln in lines):
                raise AssertionError(
                    "existing 'summary:' line missing (should be preserved when --json-log set)"
                )
    finally:
        for k, v in state.items():
            setattr(vn, k, v)
        vn.concat_wavs_atomic = original_concat
        vn.check_engine = original_check_engine
        vn.synthesize = original_synthesize


def test_visual_smoke_patch_format_youtube_to_short() -> None:
    """Phase 3-V post-freeze 第2弾 P4 (Codex CODEX_NEXT_PRIORITY:21-23):
    visual_smoke.patch_format が videoConfig.ts の FORMAT 行を正しく書き換える."""
    import visual_smoke as vs

    src = "export const FORMAT: VideoFormat = 'youtube';\nexport const FPS = 30;\n"
    out = vs.patch_format(src, "short")
    if "export const FORMAT: VideoFormat = 'short';" not in out:
        raise AssertionError(f"patch_format failed: {out!r}")
    if "export const FORMAT: VideoFormat = 'youtube';" in out:
        raise AssertionError(
            f"patch_format left old FORMAT in content: {out!r}"
        )
    # 他行は破壊しない
    if "export const FPS = 30;" not in out:
        raise AssertionError(
            f"patch_format broke unrelated lines: {out!r}"
        )


def test_visual_smoke_patch_format_no_match_raises() -> None:
    """Phase 3-V P4: FORMAT 行不在で ValueError."""
    import visual_smoke as vs

    bad = "export const FPS = 30;\n// no FORMAT line\n"
    raised = False
    try:
        vs.patch_format(bad, "short")
    except ValueError:
        raised = True
    if not raised:
        raise AssertionError("patch_format should raise ValueError on missing FORMAT")


def test_visual_smoke_patch_format_round_trip() -> None:
    """Phase 3-V P4: youtube → short → youtube round trip で原型に戻る."""
    import visual_smoke as vs

    src = "export const FORMAT: VideoFormat = 'youtube';\n"
    step1 = vs.patch_format(src, "short")
    step2 = vs.patch_format(step1, "youtube")
    if step2 != src:
        raise AssertionError(
            f"round trip mismatch: src={src!r} step2={step2!r}"
        )


def test_visual_smoke_format_dims_completeness() -> None:
    """Phase 3-V P4: FORMAT_DIMS が 3 format 全部を期待 dimension で持つ."""
    import visual_smoke as vs

    expected = {
        "youtube": (1920, 1080),
        "short": (1080, 1920),
        "square": (1080, 1080),
    }
    for fmt, dims in expected.items():
        if fmt not in vs.FORMAT_DIMS:
            raise AssertionError(f"FORMAT_DIMS missing {fmt}")
        if vs.FORMAT_DIMS[fmt] != dims:
            raise AssertionError(
                f"FORMAT_DIMS[{fmt}] = {vs.FORMAT_DIMS[fmt]}, expected {dims}"
            )
    # 余計な entry がない (3 format のみ)
    if set(vs.FORMAT_DIMS.keys()) != set(expected.keys()):
        raise AssertionError(
            f"FORMAT_DIMS unexpected extras: {set(vs.FORMAT_DIMS.keys()) - set(expected.keys())}"
        )


def main() -> int:
    tests = [
        test_fps_consistency,
        test_vad_schema_validation,
        test_ms_to_playback_frame,
        test_ms_to_playback_frame_edge_cases,
        test_load_cut_segments_fail_fast,
        test_load_cut_segments_edge_cases,
        test_build_cut_segments_multi_with_gaps,
        test_transcript_segment_validation,
        test_voicevox_collect_chunks_validation,
        test_voicevox_write_narration_data_alignment,
        test_voicevox_write_order_narrationdata_before_wav,
        test_voicevox_cleanup_stale_unlinks_sentinel,
        test_voicevox_sentinel_written_after_wav,
        test_voicevox_sentinel_write_fail_rollback,
        test_voicevox_sentinel_rollback_on_concat_fail,
        test_voicevox_json_log_emits_pure_json,
        test_visual_smoke_patch_format_youtube_to_short,
        test_visual_smoke_patch_format_no_match_raises,
        test_visual_smoke_patch_format_round_trip,
        test_visual_smoke_format_dims_completeness,
        test_build_scripts_wiring,
        test_build_slide_data_main_e2e,
        test_build_slide_data_validates_bad_transcript,
        test_build_telop_data_main_e2e,
        test_build_telop_data_validates_bad_transcript,
        test_generate_slide_plan_skip_no_api_key,
        test_generate_slide_plan_missing_inputs,
        test_generate_slide_plan_api_mock_success,
        test_generate_slide_plan_api_http_error,
        test_generate_slide_plan_api_invalid_json,
        test_build_slide_data_plan_validation_fallback,
        test_build_slide_data_plan_strict_failure,
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

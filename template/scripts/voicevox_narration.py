#!/usr/bin/env python3
"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.

Phase 3-D 設計起点 (Codex CODEX_PHASE3D_VOICEVOX, 2026-05-04):
- engine 不在で skip (--require-engine 指定時のみ exit non-zero)
- 入力: transcript_fixed.json の segments[] / project-config.json の tone
- 入力 override: --script narration_script.txt / --script-json narration_script.json
- 出力: public/narration.wav (segments 個別 wav を結合、legacy fallback)
- API: POST /audio_query → POST /synthesis (公式 https://github.com/VOICEVOX/voicevox_engine)

Phase 3-H 拡張 (Codex CODEX_PHASE3H_NEXT, 2026-05-04):
- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
- 各 chunk の wave header から実 duration を測定
- src/Narration/narrationData.ts を all-or-nothing で生成
  (NarrationSegment[] = [{id, startFrame, durationInFrames, file, text}])
- public/narration/chunk_meta.json も debug 用に出力
- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
- partial failure 時は narrationData.ts を空に reset、二重音声防止

Usage:
    python3 scripts/voicevox_narration.py
    python3 scripts/voicevox_narration.py --speaker 3
    python3 scripts/voicevox_narration.py --script narration.txt
    python3 scripts/voicevox_narration.py --list-speakers
    python3 scripts/voicevox_narration.py --require-engine
    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)

Engine 起動 (Roku ローカル):
    https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
    127.0.0.1:50021 で REST API が立つ。Docker 版もあり (公式 README 参照)。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
ENGINE_BASE = "http://127.0.0.1:50021"
DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
DEFAULT_FPS = 30
TIMEOUT = 30

NARRATION_DIR = PROJ / "public" / "narration"
NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
EMPTY_NARRATION_DATA = (
    "import type { NarrationSegment } from './types';\n"
    "\n"
    "export const narrationData: NarrationSegment[] = [];\n"
)


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def http_request(method: str, path: str, params: dict | None = None,
                 body: dict | None = None) -> bytes:
    url = ENGINE_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def check_engine() -> tuple[bool, str | None]:
    try:
        body = http_request("GET", "/version")
        return True, body.decode("utf-8").strip().strip('"')
    except (urllib.error.URLError, OSError, urllib.error.HTTPError) as e:
        return False, str(e)


def list_speakers() -> list[dict]:
    body = http_request("GET", "/speakers")
    return json.loads(body.decode("utf-8"))


def synthesize(text: str, speaker: int) -> bytes:
    """audio_query → synthesis の二段階で WAV bytes を返す."""
    aq_body = http_request("POST", "/audio_query", params={"text": text, "speaker": speaker}, body={})
    aq = json.loads(aq_body.decode("utf-8"))
    wav_bytes = http_request("POST", "/synthesis", params={"speaker": speaker}, body=aq)
    return wav_bytes


def concat_wavs(wavs: list[Path], out_path: Path) -> None:
    """同一 sample rate / channel の wav 列を時系列で結合."""
    if not wavs:
        return
    with wave.open(str(wavs[0]), "rb") as w0:
        params = w0.getparams()
        frames = [w0.readframes(w0.getnframes())]
    for p in wavs[1:]:
        with wave.open(str(p), "rb") as w:
            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (params.framerate, params.nchannels, params.sampwidth):
                print(f"WARN: {p.name} format mismatch、skip", file=sys.stderr)
                continue
            frames.append(w.readframes(w.getnframes()))
    with wave.open(str(out_path), "wb") as out:
        out.setparams(params)
        for f in frames:
            out.writeframes(f)


def measure_duration_seconds(wav_path: Path) -> float:
    """WAV header の (nframes / framerate) で正確な duration を返す."""
    with wave.open(str(wav_path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def cleanup_stale_chunks() -> None:
    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
    narrationData.ts も空 array に reset する。"""
    if NARRATION_DIR.exists():
        for p in NARRATION_DIR.glob("chunk_*.wav"):
            try:
                p.unlink()
            except OSError as e:
                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
        if CHUNK_META_JSON.exists():
            try:
                CHUNK_META_JSON.unlink()
            except OSError as e:
                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
    reset_narration_data_ts()


def reset_narration_data_ts() -> None:
    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
    if NARRATION_DATA_TS.parent.exists():
        NARRATION_DATA_TS.write_text(EMPTY_NARRATION_DATA, encoding="utf-8")


def read_render_fps(default: int = DEFAULT_FPS) -> int:
    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
    cfg_path = PROJ / "project-config.json"
    if not cfg_path.exists():
        return default
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default
    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
    if isinstance(fps, (int, float)) and fps > 0:
        return int(fps)
    return default


def write_narration_data(
    chunks: list[tuple[Path, str]],
    fps: int,
) -> tuple[list[dict], Path, Path]:
    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
    segments: list[dict] = []
    cumulative_frame = 0
    for i, (path, text) in enumerate(chunks):
        duration_sec = measure_duration_seconds(path)
        duration_frames = max(1, round(duration_sec * fps))
        rel = path.relative_to(PROJ / "public").as_posix()
        segments.append({
            "id": i,
            "startFrame": cumulative_frame,
            "durationInFrames": duration_frames,
            "file": rel,
            "text": text[:100],  # debug 用、長文は切り詰め
            "duration_sec": round(duration_sec, 3),
        })
        cumulative_frame += duration_frames

    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
    CHUNK_META_JSON.write_text(
        json.dumps(
            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ts_lines = [
        "/**",
        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
        " * 手動編集禁止 (script 再実行で上書きされる)。",
        " */",
        "import type { NarrationSegment } from './types';",
        "",
        "export const narrationData: NarrationSegment[] = [",
    ]
    for s in segments:
        ts_lines.append(
            "  { "
            f"id: {s['id']}, "
            f"startFrame: {s['startFrame']}, "
            f"durationInFrames: {s['durationInFrames']}, "
            f"file: {json.dumps(s['file'])}, "
            f"text: {json.dumps(s['text'], ensure_ascii=False)} "
            "},"
        )
    ts_lines.append("];")
    ts_lines.append("")
    NARRATION_DATA_TS.parent.mkdir(parents=True, exist_ok=True)
    NARRATION_DATA_TS.write_text("\n".join(ts_lines), encoding="utf-8")

    return segments, NARRATION_DATA_TS, CHUNK_META_JSON


def _resolve_path(path_str: str) -> Path:
    """非 absolute path は PROJ 相対に解決 (skill 実行時の cwd 揺れを吸収)."""
    p = Path(path_str)
    return p if p.is_absolute() else PROJ / p


def collect_chunks(args, transcript: dict) -> list[str]:
    if args.script:
        text = _resolve_path(args.script).read_text(encoding="utf-8")
        return [line.strip() for line in text.splitlines() if line.strip()]
    if args.script_json:
        plan = load_json(_resolve_path(args.script_json))
        return [s.get("text", "").strip() for s in plan.get("segments", []) if s.get("text", "").strip()]
    return [s.get("text", "").strip() for s in transcript.get("segments", []) if s.get("text", "").strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speaker", type=int, default=DEFAULT_SPEAKER,
                    help=f"VOICEVOX speaker id (default {DEFAULT_SPEAKER}=ずんだもんノーマル)")
    ap.add_argument("--script", help="custom plain-text narration (1 line = 1 chunk)")
    ap.add_argument("--script-json", help="custom JSON {segments:[{text}]} narration")
    ap.add_argument("--list-speakers", action="store_true")
    ap.add_argument("--require-engine", action="store_true",
                    help="engine 不在で exit 4 (default は skip exit 0)")
    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
    ap.add_argument(
        "--fps",
        type=int,
        default=None,
        help=f"narrationData.ts に書き込む frame 換算 fps "
             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
    )
    ap.add_argument("--allow-partial", action="store_true",
                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
                         "(default は全 chunk 成功必須)")
    args = ap.parse_args()

    ok, info = check_engine()
    if not ok:
        msg = f"VOICEVOX engine unavailable at {ENGINE_BASE}: {info}"
        if args.require_engine:
            print(f"ERROR: {msg}", file=sys.stderr)
            return 4
        print(f"INFO: {msg} -> narration generation skipped")
        print(
            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
            "(Phase 3-F asset gate + Phase 3-H per-segment Sequence)"
        )
        return 0
    print(f"VOICEVOX engine OK (version: {info})")

    if args.list_speakers:
        speakers = list_speakers()
        for s in speakers:
            for style in s.get("styles", []):
                print(f"  [{style.get('id'):3}] {s.get('name')} / {style.get('name')}")
        return 0

    transcript_path = PROJ / "transcript_fixed.json"
    if not transcript_path.exists() and not (args.script or args.script_json):
        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
        return 3
    transcript = load_json(transcript_path) if transcript_path.exists() else {}
    chunks = collect_chunks(args, transcript)
    if not chunks:
        print("ERROR: no narration chunks", file=sys.stderr)
        return 3

    fps = args.fps if args.fps is not None else read_render_fps()
    print(f"target fps: {fps}")

    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
    cleanup_stale_chunks()
    NARRATION_DIR.mkdir(parents=True, exist_ok=True)

    chunk_paths: list[Path] = []
    chunk_texts: list[str] = []
    for i, text in enumerate(chunks):
        try:
            wav_bytes = synthesize(text, args.speaker)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
            continue
        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
        p.write_bytes(wav_bytes)
        chunk_paths.append(p)
        chunk_texts.append(text)
        print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")

    if not chunk_paths:
        print("ERROR: no chunks succeeded", file=sys.stderr)
        return 5
    if not args.allow_partial and len(chunk_paths) < len(chunks):
        print(
            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
            f"(--allow-partial で部分成功でも narration.wav 出力可)",
            file=sys.stderr,
        )
        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
        for p in chunk_paths:
            try:
                p.unlink()
            except OSError:
                pass
        reset_narration_data_ts()
        return 6

    out_path = _resolve_path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_wavs(chunk_paths, out_path)
    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")

    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
    pairs = list(zip(chunk_paths, chunk_texts))
    segments, ts_path, meta_path = write_narration_data(pairs, fps)
    print(f"wrote: {ts_path} ({len(segments)} segments, {sum(s['durationInFrames'] for s in segments)} frames)")
    print(f"wrote: {meta_path}")

    summary = {
        "speaker": args.speaker,
        "fps": fps,
        "chunks": len(chunk_paths),
        "total_chunks": len(chunks),
        "total_frames": sum(s["durationInFrames"] for s in segments),
        "narration_wav": str(out_path),
        "narration_data_ts": str(ts_path),
        "chunk_meta_json": str(meta_path),
        "engine_version": info,
    }
    print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.

Codex Phase 3D design (2026-05-04, CODEX_PHASE3D_VOICEVOX) 推奨:
- engine 不在で skip (--require-engine 指定時のみ exit non-zero)
- 入力: transcript_fixed.json の segments[] / project-config.json の tone
- 入力 override: --script narration_script.txt / --script-json narration_script.json
- 出力: public/narration.wav (segments 個別 wav を結合)
- API: POST /audio_query → POST /synthesis (公式 https://github.com/VOICEVOX/voicevox_engine)

Usage:
    python3 scripts/voicevox_narration.py
    python3 scripts/voicevox_narration.py --speaker 3
    python3 scripts/voicevox_narration.py --script narration.txt
    python3 scripts/voicevox_narration.py --list-speakers
    python3 scripts/voicevox_narration.py --require-engine

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
TIMEOUT = 30


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
    ap.add_argument("--keep-chunks", action="store_true",
                    help="chunk wav を public/narration/ に保存 (debug 用)")
    ap.add_argument("--allow-partial", action="store_true",
                    help="一部 chunk synthesis 失敗でも narration.wav を出力 (default は全 chunk 成功必須)")
    args = ap.parse_args()

    ok, info = check_engine()
    if not ok:
        msg = f"VOICEVOX engine unavailable at {ENGINE_BASE}: {info}"
        if args.require_engine:
            print(f"ERROR: {msg}", file=sys.stderr)
            return 4
        print(f"INFO: {msg} -> narration generation skipped")
        print(
            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
            "getStaticFiles で検出し null を返すため render は失敗しない (Phase 3-F asset gate)"
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

    chunks_dir = PROJ / "public" / "narration"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    chunk_paths: list[Path] = []
    for i, text in enumerate(chunks):
        try:
            wav_bytes = synthesize(text, args.speaker)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
            continue
        p = chunks_dir / f"chunk_{i:03d}.wav"
        p.write_bytes(wav_bytes)
        chunk_paths.append(p)
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
        return 6

    out_path = _resolve_path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_wavs(chunk_paths, out_path)
    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")

    if not args.keep_chunks:
        for p in chunk_paths:
            try:
                p.unlink()
            except OSError:
                pass
        try:
            chunks_dir.rmdir()
        except OSError:
            pass

    summary = {
        "speaker": args.speaker,
        "chunks": len(chunk_paths),
        "total_chunks": len(chunks),
        "output": str(out_path),
        "engine_version": info,
    }
    print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

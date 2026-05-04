#!/usr/bin/env python3
"""SuperMovie Phase 3-C optional script: Anthropic API で slide_plan.json を生成.

Codex Phase 3C design (2026-05-04, CODEX_PHASE3C_LLM_PLAN) 推奨:
- LLM は word index ベースの slide_plan.json を返す (frame は build_slide_data.py が変換)
- ANTHROPIC_API_KEY が無ければ skip (非ゼロ終了しない)
- build_slide_data.py が plan を validate して invalid なら deterministic fallback

Usage:
    ANTHROPIC_API_KEY=sk-ant-... python3 scripts/generate_slide_plan.py \\
        --output slide_plan.json [--model claude-haiku-4-5-20251001]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
PLAN_VERSION = "supermovie.slide_plan.v1"

PROMPT_TEMPLATE = """\
あなたは動画編集者です。SuperMovie パイプラインの slide_plan を返してください。

## 入力
- transcript: 動画のナレーション文字起こし (ms timestamps + words 配列)
- format: {fmt} (短尺=short / 横長=youtube / 正方形=square)
- tone: {tone}

## 制約 (絶対ルール)
1. word index で slide 範囲を返す (startWordIndex / endWordIndex 必須)
2. word index は 0..{n_words_minus_1} の範囲、startWordIndex <= endWordIndex
3. 隣接 slide の word range は overlap しない (前 slide の endWordIndex < 次 slide の startWordIndex)
4. id は 1 から昇順
5. title は {title_max} 文字以内、必須、空不可
6. bullets は最大 {max_bullets} 個、各 bullet text は {bullet_max} 文字以内
7. align は "center" or "left" のみ
8. videoLayer は "visible" / "dimmed" / "hidden" のみ (省略可)

## 出力 (JSON のみ、コードフェンス不要)
{{
  "version": "{plan_version}",
  "slides": [
    {{
      "id": 1,
      "startWordIndex": 0,
      "endWordIndex": 30,
      "title": "短い見出し",
      "subtitle": "任意",
      "bullets": [
        {{ "text": "要点", "emphasis": true }}
      ],
      "align": "left",
      "videoLayer": "visible"
    }}
  ]
}}

## transcript (words 配列、最大 200 word のみ抜粋。全 {n_words} 個の最初):
{words_preview}

## 全 segments (timestamp 付き):
{segments_preview}
"""


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=str(PROJ / "slide_plan.json"))
    ap.add_argument("--model", default="claude-haiku-4-5-20251001",
                    help="Anthropic model (default: claude-haiku-4-5、cost 最小)")
    args = ap.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("INFO: ANTHROPIC_API_KEY 未設定 → slide_plan 生成 skip")
        print("      build_slide_data.py は --plan 無しで deterministic に走ります")
        return 0

    transcript_path = PROJ / "transcript_fixed.json"
    config_path = PROJ / "project-config.json"
    if not transcript_path.exists() or not config_path.exists():
        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
        return 3

    transcript = load_json(transcript_path)
    config = load_json(config_path)
    fmt = config.get("format", "short")
    tone = config.get("tone", "プロフェッショナル")
    words = transcript.get("words", [])
    segments = transcript.get("segments", [])
    n_words = len(words)

    title_max = {"youtube": 18, "short": 14, "square": 16}.get(fmt, 14)
    bullet_max = {"youtube": 24, "short": 18, "square": 20}.get(fmt, 18)

    words_preview = "\n".join(
        f"  [{i}] {w.get('text','')!r} ({w.get('start')}ms-{w.get('end')}ms)"
        for i, w in enumerate(words[:200])
    )
    segments_preview = "\n".join(
        f"  seg[{i}] {s.get('start')}-{s.get('end')}ms: {s.get('text','')}"
        for i, s in enumerate(segments)
    )

    prompt = PROMPT_TEMPLATE.format(
        fmt=fmt,
        tone=tone,
        n_words=n_words,
        n_words_minus_1=max(n_words - 1, 0),
        title_max=title_max,
        bullet_max=bullet_max,
        max_bullets=5,
        plan_version=PLAN_VERSION,
        words_preview=words_preview,
        segments_preview=segments_preview,
    )

    # Anthropic API 呼び出し (urllib で SDK 不要に保つ)
    import urllib.request
    import urllib.error
    body = {
        "model": args.model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: Anthropic API HTTP {e.code}: {body[:500]}", file=sys.stderr)
        return 4

    text = "".join(b.get("text", "") for b in response.get("content", []) if b.get("type") == "text")
    # コードフェンス除去 (LLM が markdown 返した場合)
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    text = text.strip()

    try:
        plan = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"ERROR: LLM 応答が JSON parse 失敗: {e}\n--- raw ---\n{text[:1000]}", file=sys.stderr)
        return 5

    out_path = Path(args.output)
    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote: {out_path}")
    print(f"slides: {len(plan.get('slides', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

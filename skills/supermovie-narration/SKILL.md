---
name: supermovie-narration
description: |
  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
  Remotion の <NarrationAudio /> layer で再生するスキル。
  「ナレーション」「TTS」「VOICEVOX」「読み上げ」と言われたときに使用。
argument-hint: [プロジェクトパス] [--speaker N] [--script <path>]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
effort: medium
---

# SuperMovie Narration — VOICEVOX 自動ナレーション

Senior video producer として、文字起こし結果から自動ナレーションを生成し、
動画の元音声を差し替える形で動画コンテンツの語り直しを行う。

**前提**: Phase 3-A SlideSequence、Phase 3-B/3-C supermovie-slides 完成後の運用想定。

## 設計起点

Codex Phase 3-D design (2026-05-04, CODEX_PHASE3D_VOICEVOX) 推奨:
- engine 不在で skip (`--require-engine` 指定時のみ exit non-zero)
- Phase 3-C と同じく optional 経路で deterministic フォールバックなし (engine 必須)
- Anthropic API ではなく VOICEVOX ローカル engine、課金ゼロ

## ワークフロー

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. engine│ → │ 2. 入力  │ → │ 3. 合成  │ → │ 4. Remotion │
│   起動確認│    │   解決   │    │   結合   │    │   接合    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Phase 1: VOICEVOX engine 起動確認

VOICEVOX engine は localhost:50021 で REST API を提供する。
Roku が以下のいずれかで起動した後に実行:

- VOICEVOX デスクトップアプリ (https://voicevox.hiroshiba.jp/)
- VOICEVOX engine Docker (https://github.com/VOICEVOX/voicevox_engine)

`voicevox_narration.py` は `/version` で自動確認、不在なら skip。

## Phase 2: 入力解決

優先順位:
1. `--script <path>` で plain-text 指定 (1 行 1 chunk)
2. `--script-json <path>` で `{segments: [{text}]}` JSON 指定
3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk

## Phase 3: 合成 + 結合

各 chunk について:
1. `POST /audio_query?text=...&speaker=<id>` → query JSON
2. `POST /synthesis?speaker=<id>` body=query → WAV bytes

すべての chunk wav を時系列で結合し `public/narration.wav` を生成。
`--keep-chunks` で chunk 個別 wav も保持 (debug)。

## Phase 4: Remotion 接合

`template/src/Narration/NarrationAudio.tsx` を `MainVideo.tsx` に追加。
narration.wav が存在する時のみコメントアウトを外す:

```tsx
// Phase 3-D scaffold: 生成後に以下を有効化
import { NarrationAudio } from './Narration';
// <Video ... volume={0} />  ← base 元音声 mute
// <NarrationAudio volume={1.0} />  ← narration 再生
```

## 実行コマンド

```bash
# default (transcript の segments すべて、speaker=3 = ずんだもんノーマル)
python3 <PROJECT>/scripts/voicevox_narration.py

# speaker 指定 (一覧は --list-speakers で確認)
python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers

# 別スクリプト読み込み
python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json

# engine 不在で fail させる (CI 用)
python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
```

## 出力

- `<PROJECT>/public/narration.wav` (本命、結合済)
- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| engine 不在 | INFO ログ + exit 0 (skip)、`--require-engine` 時のみ exit 4 |
| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
| `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
| WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |

## 連携マップ

```
/supermovie-init / transcribe / transcript-fix / cut / subtitles / slides
    ↓ transcript_fixed.json
/supermovie-narration         ← ★ここ: VOICEVOX で narration.wav 生成
    ↓ public/narration.wav
MainVideo.tsx <NarrationAudio /> 有効化
    ↓
npm run render
```

## VOICEVOX 利用規約

- 商用/非商用利用可、音声ライブラリごとにクレジット表記必須 (https://voicevox.hiroshiba.jp/term/)
- 話者選定 + クレジット明記は Roku 判断領域

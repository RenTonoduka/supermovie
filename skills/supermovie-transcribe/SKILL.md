---
name: supermovie-transcribe
description: |
  動画/音声ファイルからワードタイムスタンプ付きの高精度文字起こしを行うスキル。
  Mac/Windows環境を自動判定し、最適なエンジン（mlx-whisper / faster-whisper）を選択。
  話者分離が必要な場合のみAssemblyAIを使用。完全ローカル・無料で動作可能。
  「文字起こし」「transcribe」「書き起こし」「transcript」と言われたときに使用。
argument-hint: <動画/音声ファイルパス> [--speakers 話者数]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
effort: high
---

# SuperMovie Transcribe — 高精度文字起こし

Senior speech recognition engineer として、ユーザー環境に最適な
文字起こしエンジンを選択し、ワードタイムスタンプ付きの正確な書き起こしを生成する。

## ワークフロー概要

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. ヒアリング│→│ 2. 環境構築│→│ 3. 音声抽出│→│ 4. 文字起こし│→│ 5. 後処理  │
│ 環境/話者確認│  │ エンジン準備│  │ ffmpeg   │  │ Whisper等 │  │ JSON保存  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                                   │
              ┌──────────────────────────────────────────────────────┘
              ↓
        transcript.json → /supermovie-subtitles へ
```

---

## 前提条件チェックリスト

- [ ] ffmpeg がインストール済み
- [ ] Python 3.9+ がインストール済み
- [ ] 動画/音声ファイルが存在

---

## Phase 1: ヒアリング（初回のみ）

**ユーザーに以下を確認する:**

```
文字起こしの設定を確認させてください:

1. OS / マシンは？
   → Mac (Apple Silicon) / Mac (Intel) / Windows (NVIDIA GPU) / Windows (CPU)

2. 話者は何人？
   → 1人（話者分離不要）→ ローカルWhisperで処理
   → 2人以上 → AssemblyAI使用（話者分離対応）

3. 言語は？
   → 日本語 / 英語 / 自動検出 / その他

4. 既にWhisperはインストール済み？
   → はい / いいえ / わからない
```

**$ARGUMENTS に `--speakers N` がある場合:**
- N=1 → ローカルWhisper（ヒアリングで話者数は聞かない）
- N≧2 → AssemblyAI

**プロジェクト内に `project-config.json` がある場合:**
- 前回のヒアリング結果を参照し、環境確認はスキップ

---

## Phase 2: 環境構築（エンジン選択 & インストール）

### 2-1. エンジン選択マトリクス

```
┌────────────────────┬────────────────┬──────────┬──────────┐
│ 環境                │ エンジン        │ 速度      │ 品質     │
├────────────────────┼────────────────┼──────────┼──────────┤
│ Mac Apple Silicon   │ mlx-whisper    │ ★★★★★  │ ★★★★★ │
│ Mac Intel           │ faster-whisper │ ★★★☆☆  │ ★★★★★ │
│ Windows NVIDIA GPU  │ faster-whisper │ ★★★★☆  │ ★★★★★ │
│ Windows CPU         │ faster-whisper │ ★★☆☆☆  │ ★★★★★ │
│ 話者分離が必要       │ AssemblyAI     │ ★★★☆☆  │ ★★★★☆ │
└────────────────────┴────────────────┴──────────┴──────────┘
```

### 2-2. モデルサイズ選択

| モデル | サイズ | 日本語精度 | 速度 | 推奨場面 |
|--------|--------|----------|------|---------|
| `large-v3` | 3GB | 最高 | 遅い | 最終版、長い動画 |
| `medium` | 1.5GB | 高い | 普通 | 通常使用（デフォルト） |
| `small` | 500MB | そこそこ | 速い | 短い動画、テスト |

**デフォルト: `large-v3`**（最高精度。初回ダウンロードに時間がかかる旨を通知）

### 2-3. インストール手順

**Mac Apple Silicon — mlx-whisper:**
```bash
pip install mlx-whisper
```

**Mac Intel / Windows — faster-whisper:**
```bash
pip install faster-whisper
```

**インストール確認:**
```bash
# mlx-whisper
python3 -c "import mlx_whisper; print('mlx-whisper OK')"

# faster-whisper
python3 -c "from faster_whisper import WhisperModel; print('faster-whisper OK')"
```

**インストール失敗時:**
- pip が古い → `pip install --upgrade pip`
- Python バージョン不足 → 3.9以上が必要
- Mac Intel で mlx が入らない → faster-whisper にフォールバック

---

## Phase 3: 音声抽出

```bash
ffmpeg -y -i "<INPUT_FILE>" \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  "<PROJECT>/transcript_audio.wav"
```

**入力ファイル判定:**
- `.mp4`, `.mov`, `.mkv`, `.webm` → 動画（音声抽出必要）
- `.mp3`, `.wav`, `.m4a`, `.flac` → 音声（そのまま or 変換）

---

## Phase 4: 文字起こし実行

### 4-1. mlx-whisper（Mac Apple Silicon）

```bash
python3 -c "
import mlx_whisper
import json

result = mlx_whisper.transcribe(
    '<PROJECT>/transcript_audio.wav',
    path_or_hf_repo='mlx-community/whisper-large-v3-mlx',
    language='ja',
    word_timestamps=True,
    verbose=False,
)

# ワードタイムスタンプを抽出
words = []
for segment in result['segments']:
    if 'words' in segment:
        for w in segment['words']:
            words.append({
                'text': w['word'].strip(),
                'start': round(w['start'] * 1000),
                'end': round(w['end'] * 1000),
                'confidence': round(w.get('probability', 0.0), 3),
            })

output = {
    'engine': 'mlx-whisper',
    'model': 'large-v3',
    'language': result.get('language', 'ja'),
    'duration_ms': round(result['segments'][-1]['end'] * 1000) if result['segments'] else 0,
    'text': result['text'],
    'words': words,
    'segments': [
        {
            'text': seg['text'].strip(),
            'start': round(seg['start'] * 1000),
            'end': round(seg['end'] * 1000),
        }
        for seg in result['segments']
    ],
}

with open('<PROJECT>/transcript.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Words: {len(words)}')
print(f'Segments: {len(output[\"segments\"])}')
print(f'Duration: {output[\"duration_ms\"]/1000:.1f}s')
"
```

### 4-2. faster-whisper（Mac Intel / Windows）

```bash
python3 -c "
from faster_whisper import WhisperModel
import json

model = WhisperModel('large-v3', device='auto', compute_type='auto')
segments_iter, info = model.transcribe(
    '<PROJECT>/transcript_audio.wav',
    language='ja',
    word_timestamps=True,
    vad_filter=True,
)

words = []
segments = []
full_text = ''

for segment in segments_iter:
    segments.append({
        'text': segment.text.strip(),
        'start': round(segment.start * 1000),
        'end': round(segment.end * 1000),
    })
    full_text += segment.text
    if segment.words:
        for w in segment.words:
            words.append({
                'text': w.word.strip(),
                'start': round(w.start * 1000),
                'end': round(w.end * 1000),
                'confidence': round(w.probability, 3),
            })

output = {
    'engine': 'faster-whisper',
    'model': 'large-v3',
    'language': info.language,
    'duration_ms': segments[-1]['end'] if segments else 0,
    'text': full_text.strip(),
    'words': words,
    'segments': segments,
}

with open('<PROJECT>/transcript.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Words: {len(words)}')
print(f'Segments: {len(segments)}')
print(f'Duration: {output[\"duration_ms\"]/1000:.1f}s')
"
```

### 4-3. AssemblyAI（話者分離が必要な場合のみ）

```bash
# 音声アップロード
UPLOAD_URL=$(curl -s -X POST "https://api.assemblyai.com/v2/upload" \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  --data-binary @"<PROJECT>/transcript_audio.wav" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['upload_url'])")

# 文字起こし開始（話者分離ON）
TRANSCRIPT_ID=$(curl -s -X POST "https://api.assemblyai.com/v2/transcript" \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  -H "content-type: application/json" \
  -d "{
    \"audio_url\": \"$UPLOAD_URL\",
    \"language_code\": \"ja\",
    \"speaker_labels\": true,
    \"speakers_expected\": <話者数>
  }" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# ポーリング
while true; do
  RESULT=$(curl -s "https://api.assemblyai.com/v2/transcript/$TRANSCRIPT_ID" \
    -H "authorization: $ASSEMBLYAI_API_KEY")
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  [ "$STATUS" = "completed" ] && break
  [ "$STATUS" = "error" ] && echo "ERROR" && exit 1
  sleep 5
done

# JSON変換して保存
python3 -c "
import json

with open('/dev/stdin') as f:
    data = json.load(f)

words = []
for w in data.get('words', []):
    words.append({
        'text': w['text'],
        'start': w['start'],
        'end': w['end'],
        'confidence': round(w['confidence'], 3),
        'speaker': w.get('speaker', None),
    })

output = {
    'engine': 'assemblyai',
    'model': 'default',
    'language': 'ja',
    'duration_ms': data.get('audio_duration', 0) * 1000,
    'text': data['text'],
    'words': words,
    'segments': [
        {
            'text': u['text'],
            'start': u['start'],
            'end': u['end'],
            'speaker': u.get('speaker', None),
        }
        for u in data.get('utterances', [])
    ],
    'speakers': list(set(w.get('speaker') for w in data.get('words', []) if w.get('speaker'))),
}

with open('<PROJECT>/transcript.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Words: {len(words)}')
print(f'Speakers: {len(output[\"speakers\"])}')
" <<< "$RESULT"
```

---

## Phase 5: 後処理 & 出力

### 5-1. transcript.json 出力スキーマ

```json
{
  "engine": "mlx-whisper",
  "model": "large-v3",
  "language": "ja",
  "duration_ms": 60000,
  "text": "全文テキスト...",
  "words": [
    {
      "text": "こんにちは",
      "start": 1200,
      "end": 1800,
      "confidence": 0.95,
      "speaker": null
    }
  ],
  "segments": [
    {
      "text": "こんにちは、今日はAIについてお話しします",
      "start": 1200,
      "end": 5400,
      "speaker": null
    }
  ],
  "speakers": []
}
```

**フィールド説明:**

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `engine` | string | 使用エンジン |
| `model` | string | モデル名 |
| `language` | string | 検出言語 |
| `duration_ms` | number | 音声の長さ(ms) |
| `text` | string | 全文（改行なし） |
| `words` | array | ワードタイムスタンプ配列 |
| `words[].text` | string | 単語テキスト |
| `words[].start` | number | 開始時刻(ms) |
| `words[].end` | number | 終了時刻(ms) |
| `words[].confidence` | number | 信頼度 0.0-1.0 |
| `words[].speaker` | string\|null | 話者ID（話者分離時のみ） |
| `segments` | array | 文単位セグメント |
| `speakers` | array | 話者ID一覧（話者分離時のみ） |

### 5-2. バリデーション

| チェック項目 | 条件 | 失敗時の対応 |
|-------------|------|------------|
| words が空でない | `words.length > 0` | エンジンのエラーログを確認 |
| タイムスタンプ順序 | `words[n].start <= words[n+1].start` | ソートして修正 |
| 信頼度範囲 | `0 <= confidence <= 1` | クランプ |
| duration整合性 | 最後のword.end ≒ duration_ms | duration_msを更新 |
| テキスト空白 | text が空文字でない | 無音動画の可能性を通知 |

### 5-3. 環境設定の保存

初回ヒアリング結果を `project-config.json` に追記:
```json
{
  "transcribe": {
    "os": "mac-apple-silicon",
    "engine": "mlx-whisper",
    "model": "large-v3",
    "language": "ja"
  }
}
```

---

## 完了時の報告フォーマット

```
✅ 文字起こし完了

🎙️ エンジン: <engine> (<model>)
📝 テキスト: <最初の50文字>...
🔤 ワード数: <N>個
📋 セグメント数: <N>個
⏱️ 音声長: <duration>秒
👥 話者: <N>人（話者分離時のみ）

📄 保存先: <PROJECT>/transcript.json

次のステップ:
→ transcript.json の内容を確認・修正
→ /supermovie-subtitles でテロップ生成
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| ffmpeg 未インストール | `brew install ffmpeg` (Mac) / `choco install ffmpeg` (Win) |
| Python 3.9未満 | バージョンアップを案内 |
| pip install 失敗 | `pip install --upgrade pip` → 再実行 |
| mlx-whisper がIntel Macで失敗 | faster-whisper にフォールバック |
| faster-whisper CUDA エラー(Win) | `compute_type='int8'` + `device='cpu'` にフォールバック |
| モデルダウンロード失敗 | ネットワーク確認、`medium` モデルで再試行 |
| 音声なし動画 | ffprobeで音声ストリーム確認、ユーザーに通知 |
| ASSEMBLYAI_API_KEY 未設定 | ローカルエンジンを提案（話者1人なら不要） |
| メモリ不足 | `medium` → `small` モデルにダウングレード |
| 文字起こし結果が空 | 音声レベル確認、言語設定確認 |

---

## 連携マップ（更新版）

```
/supermovie-init              ← プロジェクト作成（起点）
    ↓
/supermovie-transcribe        ← ★文字起こし（ここ）
    ↓ transcript.json
    ↓ （確認・手修正可能）
/supermovie-subtitles         ← テロップ＆タイトル生成
    ↓
/supermovie-se                ← SE自動配置
    ↓
npm run dev                   ← プレビュー
```

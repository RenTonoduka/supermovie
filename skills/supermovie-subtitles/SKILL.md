---
name: supermovie-subtitles
description: |
  SuperMovieプロジェクトの動画から音声を抽出し、テロップ（telopData.ts）と
  タイトル（titleData.ts）を自動生成するスキル。AssemblyAI文字起こし →
  スタイル自動割り当て → フレーム同期データ生成。
  「テロップ生成」「字幕生成」「supermovie subtitles」と言われたときに使用。
argument-hint: [プロジェクトパス]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# SuperMovie Subtitles — テロップ＆タイトル自動生成

Senior video subtitle designer として、音声内容を分析し、
視聴者を引きつけるテロップとセグメントタイトルを自動生成する。

## ワークフロー概要

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. 設定読込 │→│ 2. 音声抽出│→│ 3. 文字起こし│→│ 4. テロップ │→│ 5. タイトル │
│ config確認 │  │ ffmpeg   │  │ AssemblyAI│  │ データ生成 │  │ データ生成 │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                    ↓              ↓
                                              telopData.ts   titleData.ts
```

---

## 前提条件チェックリスト

- [ ] `/supermovie-init` でプロジェクト生成済み
- [ ] `public/main.mp4` が存在
- [ ] `project-config.json` が存在（ヒアリング結果）
- [ ] 環境変数 `ASSEMBLYAI_API_KEY` がセット済み

**ASSEMBLYAI_API_KEY が未設定の場合:**
```
AssemblyAI APIキーが必要です。
→ https://www.assemblyai.com でアカウント作成（無料枠あり）
→ export ASSEMBLYAI_API_KEY="your-key-here"
```

---

## Phase 1: 設定読み込み

### 1-1. プロジェクト設定
`Root.tsx` から取得:
```
VIDEO_DURATION_FRAMES, FPS, VIDEO_FILE
```

### 1-2. ヒアリング結果
`project-config.json` から取得:
```json
{
  "tone": "プロフェッショナル",
  "telopStyle": { "main": "...", "emphasis": "...", "negative": "..." },
  "notes": "キーワード「AI」を強調"
}
```

---

## Phase 2: 音声抽出

```bash
ffmpeg -y -i "<PROJECT>/public/main.mp4" \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  /tmp/supermovie_audio.wav
```

---

## Phase 3: 文字起こし（AssemblyAI）

### 3-1. アップロード
```bash
UPLOAD_URL=$(curl -s -X POST "https://api.assemblyai.com/v2/upload" \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  --data-binary @/tmp/supermovie_audio.wav \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['upload_url'])")
```

### 3-2. 文字起こし開始
```bash
TRANSCRIPT_ID=$(curl -s -X POST "https://api.assemblyai.com/v2/transcript" \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  -H "content-type: application/json" \
  -d "{\"audio_url\": \"$UPLOAD_URL\", \"language_code\": \"ja\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

### 3-3. ポーリング（完了待ち）
```bash
while true; do
  STATUS=$(curl -s "https://api.assemblyai.com/v2/transcript/$TRANSCRIPT_ID" \
    -H "authorization: $ASSEMBLYAI_API_KEY" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  [ "$STATUS" = "completed" ] && break
  [ "$STATUS" = "error" ] && echo "ERROR" && exit 1
  sleep 5
done
```

### 3-4. ワードデータ取得
```bash
curl -s "https://api.assemblyai.com/v2/transcript/$TRANSCRIPT_ID" \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  > /tmp/supermovie_transcript.json
```

出力JSONに含まれるワードデータ:
```json
{
  "words": [
    { "text": "こんにちは", "start": 1200, "end": 1800, "confidence": 0.98 },
    ...
  ]
}
```

---

## Phase 4: テロップデータ生成

### 4-1. セグメント分割ルール

| ルール | 値 | 優先度 |
|--------|-----|-------|
| 最大文字数 | 30文字/テロップ | 高 |
| 句読点分割 | 。！？で強制分割 | 高 |
| 読点分割 | 、で分割（25文字超の場合） | 中 |
| 無音分割 | 2秒以上の空白で分割 | 高 |
| 最小表示時間 | 0.5秒（= FPS/2 フレーム） | 高 |
| テロップ間ギャップ | 最低2フレーム空ける | 中 |

### 4-2. フレーム計算

```
startFrame = Math.round(wordStartMs / 1000 * FPS)
endFrame = Math.round(wordEndMs / 1000 * FPS)
```

### 4-3. スタイル自動割り当て

**project-config.json の `tone` に応じて配分比率を調整:**

```
┌─────────────────┬──────────┬──────────┬──────────┬──────────┐
│ 判定条件         │ style    │ animation│ 比率目安  │ template │
├─────────────────┼──────────┼──────────┼──────────┼──────────┤
│ 通常の文         │ normal   │ fadeOnly │ 60-70%   │ 2        │
│ 疑問文（？）     │ normal   │ slideIn  │ 5-10%    │ 2        │
│ 強調キーワード含む│ emphasis │ slideIn  │ 10-15%   │ 1 or 6   │
│ ネガティブ表現   │ warning  │ slideIn  │ 5-10%    │ 4 or 5   │
│ ポジティブ表現   │ success  │ fadeOnly │ 5-10%    │ 3        │
│ 最重要メッセージ │ emphasis │ charByChar│ 1-3%    │ 1        │
└─────────────────┴──────────┴──────────┴──────────┴──────────┘
```

**強調判定キーワード（emphasis）:**
```
重要, ポイント, すごい, 注目, 革命, 最強, 必見, 衝撃, 驚き,
本質, 秘密, 真実, 鍵, コツ, 裏技, 必須, 絶対
+ project-config.json の notes に含まれるキーワード
```

**ネガティブ判定キーワード（warning）:**
```
問題, 失敗, 難しい, 危険, 注意, やばい, 最悪, 損, 無駄,
間違い, リスク, 落とし穴, 罠, 搾取, 地獄
```

**ポジティブ判定キーワード（success）:**
```
解決, 成功, できる, 簡単, 効果, 結果, 実現, 達成, 完成,
自動化, 効率, 時短, 無料, 利益, 成長
```

### 4-4. トーン別アニメーション調整

| トーン | fadeOnly | slideIn | charByChar | slideFromLeft |
|--------|---------|---------|-----------|--------------|
| プロフェッショナル | 70% | 25% | 0% | 5% |
| エンタメ | 40% | 35% | 10% | 15% |
| カジュアル | 50% | 25% | 5% | 20% |
| 教育的 | 75% | 20% | 0% | 5% |

---

## Phase 5: タイトルデータ生成

テロップの内容全体を俯瞰し、**話題の転換点**を検出してセグメント分割。

### 分割基準
- 5秒以上の無音
- 話題の明確な切り替わり（「次に」「それでは」「ここからは」等）
- 質問から回答への転換
- 目安: 5〜15セグメント（動画の長さに応じて）

### タイトル生成ルール
- 最大15文字
- キャッチーかつ内容を的確に表現
- 視聴者が「ここ見たい」と思えるフレーズ

---

## Phase 6: ファイル書き込み

### telopData.ts の出力形式
```typescript
import type { TelopSegment } from './telopTypes';

export const FPS = <検出値>;
export const TOTAL_FRAMES = <計算値>;

export const telopData: TelopSegment[] = [
  {
    id: 1,
    startFrame: 45,
    endFrame: 105,
    text: 'こんにちは、今日は...',
    style: 'normal',
    animation: 'fadeOnly',
  },
  // ...
];
```

### titleData.ts の出力形式
```typescript
import type { TitleSegment } from './Title';

const FPS = <検出値>;
const toFrame = (seconds: number) => Math.round(seconds * FPS);

export const titleData: TitleSegment[] = [
  { id: 1, startFrame: toFrame(0), endFrame: toFrame(30), text: 'オープニング' },
  // ...
];
```

---

## Phase 7: バリデーション（必須）

| チェック項目 | 条件 | 失敗時の対応 |
|-------------|------|------------|
| フレーム順序 | startFrame < endFrame | endFrameを+1補正 |
| フレーム重複 | テロップ同士が重ならない | 前のendFrameをカット |
| 範囲超過 | endFrame ≤ TOTAL_FRAMES | カット |
| 最小表示時間 | duration ≥ FPS/2 | 短すぎるものは前後と統合 |
| ID連番 | 1から連番 | 採番し直し |
| テキスト空 | text.length > 0 | 空エントリ削除 |

---

## 完了時の報告フォーマット

```
✅ テロップ＆タイトル生成完了

📝 テロップ: <N>個
   - normal: <n>個 / emphasis: <n>個 / warning: <n>個 / success: <n>個
🏷️ タイトル: <N>セグメント

次のステップ:
→ /supermovie-se でSE自動配置
→ npm run dev でプレビュー確認
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| ASSEMBLYAI_API_KEY 未設定 | 設定方法を案内 |
| 文字起こし失敗 | エラー詳細を表示、リトライ提案 |
| 音声なし動画 | ユーザーに確認（テロップ手動入力への切替提案） |
| project-config.json なし | デフォルト設定（プロフェッショナル）で続行 |

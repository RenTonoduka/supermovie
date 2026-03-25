---
name: supermovie-subtitles
description: |
  transcript_fixed.jsonからテロップ（telopData.ts）とタイトル（titleData.ts）を
  自動生成するスキル。修正済み文字起こしデータを元に、スタイル自動割り当て →
  フレーム同期データ生成。文字起こし自体は行わない（transcribeスキルが担当）。
  「テロップ生成」「字幕生成」「supermovie subtitles」と言われたときに使用。
argument-hint: [プロジェクトパス]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# SuperMovie Subtitles — テロップ＆タイトル自動生成

Senior video subtitle designer として、修正済み文字起こしデータを元に
視聴者を引きつけるテロップとセグメントタイトルを自動生成する。

**注意: このスキルは文字起こしを行わない。** 文字起こしは `/supermovie-transcribe` → `/supermovie-transcript-fix` で事前に完了していること。

## ワークフロー概要

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. 設定読込│→│ 2. データ変換│→│ 3. スタイル│→│ 4. タイトル │→│ 5. 検証   │
│ config+   │  │ words→    │  │ 自動割当  │  │ データ生成 │  │ +書き出し │
│ transcript│  │ telopData │  │ tone連動  │  │           │  │           │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

---

## 前提条件チェックリスト

- [ ] `/supermovie-init` でプロジェクト生成済み
- [ ] `/supermovie-transcribe` で文字起こし済み
- [ ] `/supermovie-transcript-fix` で誤字修正済み
- [ ] `transcript_fixed.json` が存在し `words` 配列がある
- [ ] `project-config.json` が存在

**AssemblyAI APIキーは不要。**

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

### 1-3. 修正済み文字起こし
`transcript_fixed.json` を読み込み:
- `words` 配列（ワードタイムスタンプ）
- `segments` 配列（文単位）
- `duration_ms`

---

## Phase 2: words → TelopSegment 変換

### 2-1. セグメント分割ルール

transcript_fixed.json の `words` を以下のルールでテロップ単位に分割:

| ルール | 値 | 優先度 |
|--------|-----|-------|
| 最大文字数 | 30文字/テロップ | 高 |
| 句読点分割 | 。！？で強制分割 | 高 |
| 読点分割 | 、で分割（25文字超の場合） | 中 |
| 無音分割 | 次のwordまで2秒以上空白 | 高 |
| 最小表示時間 | 0.5秒（= FPS/2 フレーム） | 高 |
| テロップ間ギャップ | 最低2フレーム空ける | 中 |

### 2-2. フレーム計算

```
startFrame = Math.round(word.start / 1000 * FPS)
endFrame = Math.round(word.end / 1000 * FPS)
```

**注意:** transcript_fixed.json の `start`/`end` は**ミリ秒**。FPSは Root.tsx の値を使用。

### 2-3. TelopSegment 生成

```typescript
// transcript_fixed.json の words → TelopSegment[]
{
  id: 連番,
  startFrame: 計算値,
  endFrame: 計算値,
  text: words結合テキスト,
  style: Phase 3で決定,
  animation: Phase 3で決定,
}
```

---

## Phase 3: スタイル自動割り当て

### 3-1. スタイル配分テーブル

**project-config.json の `tone` に応じて配分比率を調整:**

| 判定条件 | style | animation | 比率目安 | template |
|---------|-------|-----------|---------|---------|
| 通常の文 | normal | fadeOnly | 60-70% | 2 |
| 疑問文（？） | normal | slideIn | 5-10% | 2 |
| 強調キーワード含む | emphasis | slideIn | 10-15% | 1 or 6 |
| ネガティブ表現 | warning | slideIn | 5-10% | 4 or 5 |
| ポジティブ表現 | success | fadeOnly | 5-10% | 3 |
| 最重要メッセージ | emphasis | charByChar | 1-3% | 1 |

### 3-2. キーワード辞書

**強調判定（emphasis）:**
```
重要, ポイント, すごい, 注目, 革命, 最強, 必見, 衝撃, 驚き,
本質, 秘密, 真実, 鍵, コツ, 裏技, 必須, 絶対
+ project-config.json の notes に含まれるキーワード
```

**ネガティブ判定（warning）:**
```
問題, 失敗, 難しい, 危険, 注意, やばい, 最悪, 損, 無駄,
間違い, リスク, 落とし穴, 罠, 搾取, 地獄
```

**ポジティブ判定（success）:**
```
解決, 成功, できる, 簡単, 効果, 結果, 実現, 達成, 完成,
自動化, 効率, 時短, 無料, 利益, 成長
```

### 3-3. トーン別アニメーション調整

| トーン | fadeOnly | slideIn | charByChar | slideFromLeft |
|--------|---------|---------|-----------|--------------|
| プロフェッショナル | 70% | 25% | 0% | 5% |
| エンタメ | 40% | 35% | 10% | 15% |
| カジュアル | 50% | 25% | 5% | 20% |
| 教育的 | 75% | 20% | 0% | 5% |

---

## Phase 4: タイトルデータ生成

transcript_fixed.json の `segments` を俯瞰し、話題の転換点を検出。

### 分割基準
- 5秒以上の無音
- 話題の切り替わり（「次に」「それでは」「ここからは」等）
- 質問から回答への転換
- 目安: 5〜15セグメント

### タイトル生成ルール
- 最大15文字
- キャッチーかつ内容を的確に表現
- `TitleSegment` 型で出力

---

## Phase 5: ファイル書き込み＆検証

### 5-1. telopData.ts 出力

```typescript
import type { TelopSegment } from './telopTypes';

export const FPS = <Root.tsxの値>;
export const TOTAL_FRAMES = <Root.tsxの値>;

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

**保存先:** `src/テロップテンプレート/telopData.ts`

### 5-2. titleData.ts 出力

```typescript
import type { TitleSegment } from './Title';

const FPS = <Root.tsxの値>;
const toFrame = (seconds: number) => Math.round(seconds * FPS);

export const titleData: TitleSegment[] = [
  { id: 1, startFrame: toFrame(0), endFrame: toFrame(30), text: 'オープニング' },
  // ...
];
```

**保存先:** `src/Title/titleData.ts`

### 5-3. バリデーション

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
| transcript_fixed.json が存在しない | `/supermovie-transcribe` → `/supermovie-transcript-fix` の実行を促す |
| transcript.json しかない（fixされていない） | `/supermovie-transcript-fix` の実行を促す |
| words 配列が空 | 音声なし動画の可能性を通知 |
| project-config.json なし | デフォルト設定（プロフェッショナル）で続行 |
| FPS / TOTAL_FRAMES が取得できない | Root.tsx の確認を促す |

---

## 連携マップ

```
/supermovie-init              ← ヒアリング → プロジェクト作成
    ↓
/supermovie-transcribe        ← 文字起こし（ローカル無料）
    ↓ transcript.json
/supermovie-transcript-fix    ← 誤字修正（辞書 + Claude LLM）
    ↓ transcript_fixed.json
/supermovie-subtitles         ← ★ここ: テロップ＆タイトル生成
    ↓ telopData.ts + titleData.ts
/supermovie-se                ← SE自動配置
    ↓
npm run dev                   ← プレビュー
```

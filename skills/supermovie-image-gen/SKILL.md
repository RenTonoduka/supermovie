---
name: supermovie-image-gen
description: |
  テロップ・タイトルの内容を分析し、挿入画像を自動生成・配置するスキル。
  Gemini APIで図解・インフォグラフィック・イメージ画像を生成し、
  insertImageData.tsのタイミングデータも自動作成。動画フォーマット連動。
  「画像生成」「挿入画像」「image gen」「図解作成」と言われたときに使用。
argument-hint: [プロジェクトパス]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
effort: high
---

# SuperMovie Image Gen — 挿入画像自動生成・配置

Senior visual content designer として、テロップの内容を分析し、
視聴者の理解を助ける画像を自動生成・最適タイミングに配置する。

## ワークフロー概要

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. 分析   │→│ 2. 画像計画│→│ 3. 生成   │→│ 4. 配置   │→│ 5. 検証   │
│ テロップ  │  │ 何をどこに │  │ Gemini API│  │ Data生成  │  │ プレビュー │
│ +タイトル │  │ ヒアリング │  │ 画像作成  │  │ TS書出し  │  │           │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

---

## 前提条件チェックリスト

- [ ] `/supermovie-subtitles` でテロップ＆タイトル生成済み
- [ ] `src/テロップテンプレート/telopData.ts` にデータがある
- [ ] `src/Title/titleData.ts` にデータがある
- [ ] `project-config.json` が存在（format/resolution参照）
- [ ] 環境変数 `GEMINI_API_KEY` が**存在**（値は表示・ログ化しない、存在チェックのみ）
- [ ] cost guard 設定（**未設定なら生成禁止**、§Phase 2-3 Cost Guard / Plan-only Gate 参照）:
  - [ ] `{{MONTHLY_BUDGET_USD}}` — Roku 判断 placeholder（月次予算上限 USD）
  - [ ] `{{GEMINI_IMAGE_UNIT_COST_USD}}` — 公式価格または運用入力（doc に price hardcode 禁止）
  - [ ] `{{MAX_GENERATIONS_PER_RUN}}` — 1 invocation あたり生成上限
  - [ ] `{{GEMINI_USAGE_LEDGER_PATH}}` — 月次使用量 ledger（未設定なら「当月残額不明」として生成禁止）

---

## Phase 1: コンテンツ分析

### 1-1. データ読み込み

- `telopData.ts` — 全テロップのテキスト・スタイル・タイミング
- `titleData.ts` — セグメント（チャプター）構成
- `project-config.json` — format, tone, notes

### 1-2. 画像候補の自動抽出

テロップとタイトルを分析し、**画像が効果的な箇所**を自動判定:

| 判定基準 | 画像タイプ | 例 |
|---------|----------|-----|
| 数字・データが含まれる | `infographic` | 「3つのポイント」「売上が50%増」 |
| 手順・ステップの説明 | `infographic` | 「まず〜、次に〜、最後に〜」 |
| 比較・対比 | `infographic` | 「AとBの違い」「ビフォーアフター」 |
| 抽象的な概念 | `photo` | 「未来のビジョン」「成功のイメージ」 |
| ツール・サービス紹介 | `infographic` | 「ChatGPTとは」「Remotionの特徴」 |
| ネガティブな問題提起 | `overlay` | 「こんな悩みありませんか？」 |
| タイトル切り替わり | なし（タイトル自体が表示） | — |

### 1-3. 候補リスト生成

```json
[
  {
    "insertAt": { "startFrame": 150, "endFrame": 450 },
    "reason": "「3つのポイント」を説明している箇所",
    "suggestedType": "infographic",
    "promptDraft": "3つのポイントを示す図解。1.○○ 2.○○ 3.○○",
    "priority": "high"
  }
]
```

---

## Phase 2: 画像計画（ヒアリング）

候補リストをユーザーに提示し、確認:

```
テロップ内容を分析しました。以下の箇所に画像を挿入する計画です:

1. [0:05-0:15] 📊 インフォグラフィック（高優先）
   → 「3つのポイント」の図解
   → プロンプト案: "3つのポイントを示すモダンな図解..."

2. [0:30-0:45] 🖼️ イメージ画像（中優先）
   → 「AIの未来」のビジュアル
   → プロンプト案: "未来的なAIテクノロジーのイメージ..."

3. [1:20-1:35] 📊 インフォグラフィック（高優先）
   → 「ステップ1→2→3」のフロー図
   → プロンプト案: "3ステップのフローチャート..."

修正・追加・削除があれば教えてください。
**OK と言われても直接 Phase 3 に進まない**。次は §Phase 2-3 Cost Guard / Plan-only Gate に進み、plan-only summary を出してから guard pass + 明示承認 `yes` を取得する。
```

**ユーザーが調整できるポイント:**
- 画像の追加/削除
- プロンプトの修正
- タイプの変更（infographic ↔ photo ↔ overlay）
- 表示タイミングの変更

---

## Phase 2-3: Cost Guard / Plan-only Gate

**default は `plan_only`**。本 skill は API call の前に必ず以下の cost guard を通し、guard pass + ユーザー明示承認の後に限り Phase 3 生成コマンドを実行する。

### 2-3-1. Plan-only summary（API call なし、毎回出力）

```
🧮 cost guard plan-only summary

  planned_generation_count : N （retries / regeneration を含む上限カウント）
  GEMINI_API_KEY           : present / absent （値は表示しない）
  {{MONTHLY_BUDGET_USD}}   : <Roku 判断 placeholder>
  {{GEMINI_IMAGE_UNIT_COST_USD}} : <公式価格 or 運用入力>
  {{MAX_GENERATIONS_PER_RUN}}    : <上限>
  {{GEMINI_USAGE_LEDGER_PATH}}   : <月次 ledger path>

  推定 cost (USD)          : planned_generation_count * {{GEMINI_IMAGE_UNIT_COST_USD}}
  当月残額 (USD)            : {{MONTHLY_BUDGET_USD}} - <ledger 実績>
  guard verdict            : pass / block
```

### 2-3-2. Block 条件（一つでも該当したら Phase 3 生成禁止）

- `GEMINI_API_KEY` 不在
- `{{MONTHLY_BUDGET_USD}}` 未設定（Roku 判断未確定）
- `{{GEMINI_IMAGE_UNIT_COST_USD}}` 未設定（doc に price hardcode 禁止のため、運用入力または公式価格 fetch が必須）
- `{{MAX_GENERATIONS_PER_RUN}}` 未設定
- `{{GEMINI_USAGE_LEDGER_PATH}}` 未設定（当月残額が確認できない）
- `planned_generation_count > {{MAX_GENERATIONS_PER_RUN}}`
- 推定 cost > 当月残額
- 推定 cost に retries / regeneration が含まれていない

### 2-3-3. ユーザー明示承認

guard verdict = `pass` の場合、以下を明示確認:

```
guard pass。{{MAX_GENERATIONS_PER_RUN}} 内 / 当月残額内で N 枚生成します。よろしいですか？
- yes / 生成して: Phase 3 へ進む
- 修正: Phase 2 候補リストに戻る
- no / cancel: 終了
```

ユーザーが `yes` と明示するまで Phase 3 生成コマンドは実行禁止。

---

## Phase 3: Gemini API で画像生成

**前提**: Phase 2-3 cost guard が `pass` + ユーザー明示承認 `yes` 後のみ実行可能。guard が `block` または承認未取得の場合、本 phase の生成コマンドは禁止。

### 3-1. フォーマット別アスペクト比

project-config.json の `format` に連動:

| format | Gemini API `-a` | 用途 |
|--------|----------------|------|
| `youtube` | `16:9` | 横長（デフォルト） |
| `short` | `9:16` | 縦長 |
| `square` | `1:1` | 正方形 |

### 3-2. タイプ別プロンプトテンプレート

**infographic（図解・データ）:**
```
Create a clean, modern infographic with the following content:
[内容]
Style: minimalist, dark background (#1a1a2e), bright accent colors,
no text (text will be overlaid separately),
aspect ratio: [format], high contrast for video overlay
```

**photo（イメージ画像）:**
```
Photorealistic image of [内容].
Style: cinematic lighting, shallow depth of field,
professional stock photo quality,
aspect ratio: [format]
```

**overlay（問題提起・暗い背景）:**
```
Dark, moody background image representing [内容].
Style: abstract, dark tones with subtle color accents,
suitable as a video overlay with text on top,
aspect ratio: [format]
```

### 3-3. 生成実行

> ⚠️ **guard pass + 明示承認 後のみ**: Phase 2-3 Cost Guard / Plan-only Gate を通り、ユーザーが `yes` と明示してから本コマンドを実行する。guard 未通過の状態で以下を走らせるのは禁止。

```bash
cd ~/.claude/skills/gemini-api-image && \
python scripts/run.py api_generator.py \
  --prompt "<プロンプト>" \
  -a <アスペクト比> \
  -m pro \
  -o "<PROJECT>/public/images/generated/<filename>.png"
```

**ファイル名規約:**
```
<startSec>s_<type>_<連番>.png
例: 005s_infographic_01.png, 030s_photo_02.png
```

### 3-4. 生成の進捗表示

```
🎨 画像生成中...
  [1/3] 005s_infographic_01.png ... ✅ (12秒)
  [2/3] 030s_photo_02.png ... ✅ (8秒)
  [3/3] 080s_infographic_03.png ... ✅ (15秒)
```

---

## Phase 4: insertImageData.ts 生成

### 4-1. 出力形式

```typescript
import type { ImageSegment } from './types';

const FPS = 30; // Root.tsxの値
const toFrame = (seconds: number) => Math.round(seconds * FPS);

export const insertImageData: ImageSegment[] = [
  {
    id: 1,
    startFrame: toFrame(5),
    endFrame: toFrame(15),
    file: 'generated/005s_infographic_01.png',
    type: 'infographic',
  },
  {
    id: 2,
    startFrame: toFrame(30),
    endFrame: toFrame(45),
    file: 'generated/030s_photo_02.png',
    type: 'photo',
  },
  {
    id: 3,
    startFrame: toFrame(80),
    endFrame: toFrame(95),
    file: 'generated/080s_infographic_03.png',
    type: 'overlay',
  },
];
```

**保存先:** `src/InsertImage/insertImageData.ts`

### 4-2. タイプ別表示ロジック（InsertImage.tsx連携）

| type | 表示方法 |
|------|---------|
| `infographic` | 全画面固定表示 |
| `photo` | 全画面 + Ken Burnsズーム（1.0→1.05） |
| `overlay` | 暗背景(0.7) + 中央配置 |

---

## Phase 5: 検証

### 5-1. バリデーション

| チェック項目 | 条件 | 失敗時の対応 |
|-------------|------|------------|
| 画像ファイル存在 | 全ファイルが `public/images/generated/` にある | §Phase 2-3 に戻り cost guard 再通過 (missing file の再生成も `planned_generation_count` に加算) + ユーザー明示承認 `yes` 取得後に再生成 |
| フレーム重複 | 画像同士が重ならない | 前の画像のendFrameをカット |
| テロップとの共存 | 画像表示中もテロップは読める | overlay時はテロップ位置を確認 |
| 範囲超過 | endFrame ≤ TOTAL_FRAMES | カット |
| 画像枚数の目安 | 動画1分あたり1-3枚 | 多すぎる場合は優先度lowを削除 |

### 5-2. プレビュー確認

```bash
cd <PROJECT> && npm run dev
```

Remotion StudioでMainVideoを確認。画像の表示タイミング・サイズが適切か確認。

---

## 完了時の報告フォーマット

```
✅ 画像生成・配置完了

🎨 生成画像: <N>枚
   - infographic: <n>枚
   - photo: <n>枚
   - overlay: <n>枚
📂 保存先: public/images/generated/

📄 insertImageData.ts 更新済み

次のステップ:
→ npm run dev で画像の表示タイミングを確認
→ /supermovie-se でSE配置（画像出現タイミングにもSE付与）
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| GEMINI_API_KEY 未設定（存在チェック失敗） | cost guard で `block`、画像なしで続行を提案。値の表示・ログ化はしない |
| cost guard `block`（{{MONTHLY_BUDGET_USD}} 等未設定） | Phase 3 生成禁止。Roku に placeholder 確定を依頼 or 画像なしで続行 |
| Gemini API エラー（レート制限） | **自動 retry 禁止**。`{{MAX_GENERATIONS_PER_RUN}}` 残量と当月残額を再確認してから続行（retry も `planned_generation_count` の枠内でカウント） |
| 生成画像の品質が低い | プロンプト調整して再生成を提案。再生成も `planned_generation_count` に含める |
| telopData.ts が空 | `/supermovie-subtitles` の実行を促す |
| project-config.json なし | デフォルト（youtube 16:9）で続行 |
| gemini-api-image スキルが見つからない | インストール方法を案内 |

---

## 連携マップ

```
/supermovie-init              ← ヒアリング → プロジェクト作成
    ↓
/supermovie-transcribe        ← 文字起こし（ローカル無料）
    ↓ transcript.json
/supermovie-transcript-fix    ← 誤字修正（辞書 + Claude LLM）
    ↓ transcript_fixed.json
/supermovie-cut               ← 不要区間カット（VAD + LLM分析）
    ↓ cutData.ts
/supermovie-subtitles         ← テロップ＆タイトル生成
    ↓ telopData.ts + titleData.ts
/supermovie-image-gen         ← ★ここ: 画像生成 + 配置データ
    ↓ insertImageData.ts
/supermovie-se                ← SE自動配置
    ↓
npm run dev                   ← プレビュー
```

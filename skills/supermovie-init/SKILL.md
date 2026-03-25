---
name: supermovie-init
description: |
  SuperMovie動画編集プロジェクトを自動生成するスキル。
  ヒアリングで動画の方向性を確認 → Remotionプロジェクトを構築。
  「動画プロジェクト作成」「supermovie init」「新しい動画を編集」と言われたときに使用。
argument-hint: <動画ファイルパス> [プロジェクト名]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
---

# SuperMovie Init — 動画編集プロジェクト自動生成

Senior video production engineer として、ユーザーの動画素材から
最適なRemotionプロジェクトを構築する。**必ずヒアリングから始める。**

## ワークフロー概要

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. ヒアリング │ → │ 2. 動画解析  │ → │ 3. プロジェクト│ → │ 4. カスタマイズ│
│  動画の方向性  │    │  FPS/尺検出  │    │  テンプレコピー│    │  設定反映     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Phase 1: ヒアリング（必須・スキップ不可）

動画ファイルパスを確認した後、**1回のメッセージで以下を全て聞く**。
回答は箇条書きでOKと伝える。

```
プロジェクトを作成する前に、動画の方向性を確認させてください。
（箇条書きでサクッと答えてもらえればOKです）

1. 動画の種類は？
   → YouTube解説 / セミナー録画 / プロモーション / Vlog / インタビュー / その他

2. ターゲット視聴者は？
   → ビジネスパーソン / 初心者 / エンジニア / 一般層 / その他

3. 動画のトーンは？
   → プロフェッショナル / カジュアル / エンタメ / 教育的

4. テロップのスタイル希望は？（おまかせOK）
   ┌──────────┬──────────────────────────────┐
   │ カテゴリ  │ 選択肢                        │
   ├──────────┼──────────────────────────────┤
   │ メイン    │ 白青テロップ / 白青ver2（立体） │
   │ 強調     │ 赤文字 / オレンジグラデーション   │
   │ ネガティブ │ 黒文字白背景 / 残酷紺 / 黒紫グラデ│
   └──────────┴──────────────────────────────┘

5. BGMの雰囲気は？
   → アップテンポ / 落ち着いた / なし / おまかせ

6. 特に意識したいこと・注意点は？
   → 例: テンポ重視 / 特定キーワード強調 / 情報量多め
```

### ヒアリング結果 → `project-config.json`

回答を以下のJSON形式で保存（プロジェクトルートに配置）:

```json
{
  "videoType": "YouTube解説",
  "targetAudience": "ビジネスパーソン",
  "tone": "プロフェッショナル",
  "telopStyle": {
    "main": "白青テロップver2",
    "emphasis": "オレンジグラデーション",
    "negative": "黒紫グラデ"
  },
  "bgmMood": "アップテンポ",
  "notes": "テンポ重視、キーワード「AI」を強調",
  "createdAt": "2026-03-25"
}
```

**「おまかせ」の場合のデフォルト選択ロジック:**

| トーン | メイン | 強調 | ネガティブ |
|--------|--------|------|-----------|
| プロフェッショナル | 白青ver2 | オレンジグラデーション | 黒紫グラデ |
| エンタメ | 白青テロップ | 赤文字 | 残酷紺 |
| カジュアル | 白青テロップ | オレンジグラデーション | 黒文字白背景 |
| 教育的 | 白青ver2 | オレンジグラデーション | 黒文字白背景 |

---

## Phase 2: 動画解析

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "$VIDEO_PATH"
```

抽出する値:
- `duration`（秒）
- `r_frame_rate`（FPS — "30/1" → 30, "25/1" → 25）
- `DURATION_FRAMES = Math.round(duration * fps)`

---

## Phase 3: プロジェクト生成

### 3-1. テンプレートコピー
```bash
cp -r /Users/tonodukaren/movie/YT/supermovie/template "<PROJECT_DIR>"
```

### 3-2. 動画配置
```bash
cp "$VIDEO_PATH" "<PROJECT_DIR>/public/main.mp4"
```

### 3-3. ファイル更新

**Root.tsx:**
```typescript
const VIDEO_DURATION_FRAMES = <計算値>;
const FPS = <検出値>;
const VIDEO_FILE = 'main.mp4';
```

**テロップテンプレート/telopData.ts:**
```typescript
export const FPS = <検出値>;
export const TOTAL_FRAMES = <計算値>;
```

**Title/titleData.ts:**
```typescript
const FPS = <検出値>;
```

**package.json:**
```json
{ "name": "<プロジェクト名>" }
```

---

## Phase 4: ヒアリング結果のカスタマイズ反映

トーンに応じて `telopStyles.ts` のデフォルトマッピングコメントを追記:

| トーン | アニメーション傾向 | charByChar | テンポ |
|--------|-------------------|-----------|--------|
| プロフェッショナル | `fadeOnly` 中心 | 使わない | 落ち着き |
| エンタメ | `slideIn` 多め | 積極使用 | 速い |
| カジュアル | バリエーション豊富 | たまに | 普通 |
| 教育的 | `fadeOnly` 中心 | 使わない | ゆっくり |

---

## Phase 5: セットアップ

```bash
cd "<PROJECT_DIR>" && npm install
```

---

## Phase 6: 起動確認

```bash
cd "<PROJECT_DIR>" && npx remotion studio
```

---

## 完了時の報告フォーマット

```
✅ プロジェクト作成完了

📁 パス: <PROJECT_DIR>
🎬 動画: <duration>秒 / <fps>fps / <frames>フレーム
🎨 スタイル: <ヒアリング結果サマリー>

次のステップ:
→ /supermovie-subtitles でテロップ自動生成
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| 動画ファイルが存在しない | パスを再確認してもらう |
| ffprobeがインストールされていない | `brew install ffmpeg` を提案 |
| npm installが失敗 | node_modulesを削除して再実行 |
| テンプレートが見つからない | テンプレートパスを確認 |

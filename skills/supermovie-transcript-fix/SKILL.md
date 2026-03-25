---
name: supermovie-transcript-fix
description: |
  Whisper文字起こしの誤字脱字を自動修正するスキル。
  辞書ベース修正（確実）+ Claude LLM文脈修正（賢い）の2段階で
  ワードタイムスタンプを保持したまま高精度に整形。
  「誤字修正」「transcript fix」「文字起こし修正」「整形」と言われたときに使用。
argument-hint: [プロジェクトパス]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
effort: high
---

# SuperMovie Transcript Fix — 文字起こし誤字修正

Senior Japanese language editor として、Whisper出力の誤字脱字を
辞書＋文脈AIの2段階で修正し、ワードタイムスタンプを完全に保持する。

## ワークフロー概要

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1. 読み込み│→│ 2. 辞書修正│→│ 3. LLM修正│→│ 4. 再マッピング│→│ 5. 検証  │
│ transcript│  │ 機械的置換 │  │ 文脈理解  │  │ タイムスタンプ│  │ 保存    │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
    ↑                                                              │
    │          transcript.json                    transcript_fixed.json
```

---

## 前提条件チェックリスト

- [ ] `/supermovie-transcribe` で文字起こし済み
- [ ] `transcript.json` が存在
- [ ] `transcript.json` に `words` 配列がある

---

## Phase 1: 読み込み＆分析

### 1-1. transcript.json 読み込み

```json
{
  "words": [
    { "text": "広価", "start": 1200, "end": 1500, "confidence": 0.72 },
    { "text": "的に", "start": 1500, "end": 1800, "confidence": 0.95 }
  ],
  "segments": [
    { "text": "広価的にAIで以降する", "start": 1200, "end": 5000 }
  ]
}
```

### 1-2. 品質スキャン

修正前の状態を把握:
- 低信頼度ワード数（confidence < 0.7）
- 総ワード数
- セグメント数

```
📊 品質スキャン結果:
  総ワード: 523個
  低信頼度（< 0.7）: 47個（9.0%）← 重点修正対象
  セグメント: 38個
```

### 1-3. project-config.json の読み込み（あれば）

動画の文脈情報を取得:
- `videoType`: 動画ジャンル（専門用語の推測に使用）
- `notes`: キーワード（固有名詞の手がかり）

---

## Phase 2: 辞書修正（機械的・確実）

### 2-1. typo_dict.json の構造

プロジェクトルートに `typo_dict.json` を配置（なければ自動生成）:

```json
{
  "replace": {
    "広価": "効果",
    "人口知能": "人工知能",
    "プログラミ": "プログラミング",
    "チャットGPT": "ChatGPT",
    "クロードコード": "Claude Code",
    "リモーション": "Remotion"
  },
  "fillers": [
    "えーと", "あのー", "えー", "うーん", "まあ",
    "そのー", "なんか", "ええと", "あのですね"
  ],
  "preserve": [
    "AI", "ChatGPT", "Claude", "Remotion", "YouTube"
  ]
}
```

**3つのセクション:**

| セクション | 機能 | 処理 |
|-----------|------|------|
| `replace` | 既知の誤変換を修正 | 完全一致で置換 |
| `fillers` | フィラー（つなぎ言葉）除去 | 該当wordを削除 |
| `preserve` | 正しい表記を保護 | LLM修正で変更されないようマーク |

### 2-2. 辞書修正の実行

```
処理フロー:
1. words配列を順にスキャン
2. word.text が replace に一致 → テキスト置換（タイムスタンプ保持）
3. word.text が fillers に一致 → wordを削除リストに追加
4. word.text が preserve に一致 → 保護フラグを付与

修正前: [広価(1200-1500)] [的に(1500-1800)] [えーと(2000-2400)] [AIで(2500-2900)]
修正後: [効果(1200-1500)] [的に(1500-1800)]                    [AIで(2500-2900)]
         ↑ 辞書置換           ↑ そのまま      ↑ フィラー削除      ↑ そのまま
```

### 2-3. typo_dict.json がない場合

デフォルト辞書を自動生成:
```json
{
  "replace": {},
  "fillers": ["えーと", "あのー", "えー", "うーん", "まあ", "そのー"],
  "preserve": []
}
```

ユーザーに通知:
```
typo_dict.json を自動生成しました。
プロジェクト固有の誤変換があれば "replace" に追加してください。
```

---

## Phase 3: Claude LLM 文脈修正

### 3-1. セグメント分割

辞書修正済みのwordsをセグメント単位（5〜10文）にまとめる。
各セグメントは **前後1文をオーバーラップ** させて文脈を保持。

```
セグメント1: [文1, 文2, 文3, 文4, 文5]
セグメント2:              [文5, 文6, 文7, 文8, 文9]  ← 文5が重複（文脈接続）
```

### 3-2. Claude への修正プロンプト

各セグメントに対して以下のプロンプトで修正を依頼:

```
あなたは日本語校正の専門家です。
Whisper（音声認識）の出力テキストを修正してください。

## ルール
1. 漢字の誤変換を文脈から正しく修正（例: 「以降」→「移行」）
2. 同音異義語を文脈で正しく判定
3. 助詞の脱落・誤りを修正
4. 固有名詞を正しい表記に修正
5. 意味を変えない。内容を追加・削除しない
6. 句読点が不自然な位置にあれば調整
7. 【保護ワード】は変更しない: <preserveリスト>

## 動画の文脈情報
- 種類: <videoType>
- キーワード: <notes>

## 入力テキスト
<セグメントテキスト>

## 出力形式
修正後のテキストのみを返してください。
変更箇所がない場合はそのまま返してください。
修正した箇所は【修正: 元→修正後】の形式でコメントを末尾に付けてください。
```

### 3-3. 並列処理

セグメントが多い場合は **Agentツールで並列実行**:
- 3〜5セグメントを同時にサブエージェントで処理
- 各エージェントは独立したセグメントを担当
- 結果をマージ（オーバーラップ部分は後のセグメントを優先）

### 3-4. 修正の差分記録

全ての修正を記録:
```json
{
  "corrections": [
    {
      "original": "以降",
      "corrected": "移行",
      "position": { "start": 3000, "end": 3300 },
      "reason": "文脈: 「AIで移行する」- システム移行の意",
      "phase": "llm"
    }
  ]
}
```

---

## Phase 4: ワードタイムスタンプ再マッピング

### 4-1. 修正テキストと元wordsの照合

```
元words:  [効果(1200-1500)] [的に(1500-1800)] [AIで(2500-2900)] [移行(3000-3300)]
修正text: "効果的にAIで移行する"

照合アルゴリズム:
1. 元wordsのテキストを結合 → "効果的にAIで移行"
2. 修正テキストと差分比較
3. 変更なし → タイムスタンプそのまま
4. 文字変更のみ（文字数同じ） → タイムスタンプそのまま
5. 文字数変化 → 前後のタイムスタンプから比例配分
```

### 4-2. タイムスタンプ保持の原則

| ケース | 処理 |
|--------|------|
| テキスト変更なし | タイムスタンプ保持 |
| 文字変更のみ（「以降」→「移行」） | タイムスタンプ保持 |
| フィラー削除 | wordごと削除、前後のギャップはそのまま |
| 単語分割（「効果的」→「効果」+「的」） | 文字数比でタイムスタンプ分割 |
| 単語結合（「効」+「果」→「効果」） | start=最初のstart, end=最後のend |
| テキスト追加（助詞挿入） | 前のwordのend〜次のwordのstartの間に配置 |

### 4-3. 比例配分の計算式

```
元word: { text: "効果的に", start: 1200, end: 1800 }  (4文字, 600ms)
分割後:
  "効果" → start: 1200, end: 1200 + 600*(2/4) = 1500
  "的に" → start: 1500, end: 1800
```

---

## Phase 5: 検証＆保存

### 5-1. バリデーション

| チェック項目 | 条件 | 失敗時の対応 |
|-------------|------|------------|
| タイムスタンプ順序 | `words[n].start <= words[n+1].start` | ソートして修正 |
| start < end | 全wordで成立 | end = start + 1 に修正 |
| テキスト空白なし | `word.text.trim().length > 0` | 空wordを削除 |
| 総duration保持 | 最後のword.end ≒ 元のduration | 警告のみ |
| 修正率チェック | 修正が全体の30%以下 | 30%超は過剰修正の警告 |

### 5-2. 出力ファイル

**transcript_fixed.json** — 修正済みメインファイル:
```json
{
  "engine": "mlx-whisper",
  "model": "large-v3",
  "language": "ja",
  "duration_ms": 60000,
  "text": "効果的にAIで移行する...",
  "words": [
    { "text": "効果", "start": 1200, "end": 1500, "confidence": 0.95 },
    { "text": "的に", "start": 1500, "end": 1800, "confidence": 0.95 }
  ],
  "segments": [
    { "text": "効果的にAIで移行する", "start": 1200, "end": 5000 }
  ],
  "fix_meta": {
    "original_file": "transcript.json",
    "total_corrections": 12,
    "dict_corrections": 5,
    "llm_corrections": 7,
    "fillers_removed": 8
  }
}
```

**transcript_corrections.json** — 修正履歴（デバッグ用）:
```json
{
  "corrections": [
    { "original": "広価", "corrected": "効果", "phase": "dict" },
    { "original": "以降", "corrected": "移行", "phase": "llm", "reason": "文脈" }
  ],
  "fillers_removed": [
    { "text": "えーと", "start": 2000, "end": 2400 }
  ]
}
```

### 5-3. typo_dict.json の学習更新

LLM修正で見つかった新しい誤変換パターンを `typo_dict.json` に追記提案:
```
💡 以下の修正パターンを typo_dict.json に追加しますか？
  - "以降" → "移行"（3回出現）
  - "加工" → "下降"（2回出現）

追加すると次回以降はPhase 2（辞書）で即座に修正されます。
```

---

## 完了時の報告フォーマット

```
✅ 文字起こし修正完了

📊 修正サマリー:
  辞書修正: <N>箇所
  LLM修正: <N>箇所
  フィラー除去: <N>個
  修正率: <X>%（全<total>ワード中）

📝 主な修正:
  - 「広価」→「効果」（辞書）
  - 「以降」→「移行」（文脈）
  - 「えーと」× 8個 除去

📄 保存先:
  transcript_fixed.json（修正済み）
  transcript_corrections.json（修正履歴）

次のステップ:
→ transcript_fixed.json を確認
→ /supermovie-subtitles でテロップ生成
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| transcript.json が存在しない | `/supermovie-transcribe` の実行を促す |
| words 配列が空 | 音声なし動画の可能性を通知 |
| LLM修正が過剰（30%超） | 警告を表示、元テキストとの差分を提示 |
| タイムスタンプ破損 | 元のtranscript.jsonから復元 |
| typo_dict.json のJSON構文エラー | 構文を修正して再読み込み |
| セグメント分割でオーバーラップ不整合 | 後のセグメントを優先して統合 |

---

## 連携マップ（更新版）

```
/supermovie-init              ← ヒアリング → プロジェクト作成
    ↓
/supermovie-transcribe        ← 文字起こし（ローカル無料）
    ↓ transcript.json
/supermovie-transcript-fix    ← ★ 誤字修正（辞書 + Claude LLM）
    ↓ transcript_fixed.json
    ↓ （ここで最終確認OK）
/supermovie-subtitles         ← テロップ＆タイトル生成
    ↓
/supermovie-se                ← SE自動配置
    ↓
npm run dev                   ← プレビュー
```

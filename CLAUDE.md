# SuperMovie — プロジェクトルール

## 正規ワークフロー（必ずこの順序で実行）

```
/supermovie-init              ← ヒアリング → プロジェクト作成
    ↓ project-config.json
/supermovie-transcribe        ← 文字起こし（ローカルWhisper or AssemblyAI）
    ↓ transcript.json
/supermovie-transcript-fix    ← 誤字修正（辞書 + Claude LLM）
    ↓ transcript_fixed.json
    ↓ （ユーザー確認ポイント）
/supermovie-cut               ← 不要区間カット（VAD + LLM分析）
    ↓ cutData.ts
/supermovie-subtitles         ← transcript_fixed.json → telopData.ts + titleData.ts
    ↓
/supermovie-image-gen         ← テロップ分析 → 画像生成 + insertImageData.ts
    ↓
/supermovie-se                ← telopData.ts + insertImageData.ts → seData.ts
    ↓
npm run dev                   ← Remotion Studioプレビュー
```

## 動画フォーマット定義

| フォーマット | アスペクト比 | 解像度 | 用途 |
|-------------|------------|--------|------|
| `youtube` | 16:9 | 1920×1080 | YouTube通常動画（デフォルト） |
| `short` | 9:16 | 1080×1920 | YouTube Shorts / TikTok / Reels |
| `square` | 1:1 | 1080×1080 | Instagram / SNS投稿 |

**フォーマットはプロジェクト作成時にヒアリングで決定し、以下に影響する:**
- Root.tsx の `width` / `height`
- テロップの `fontSize`・`position.bottom`（縦動画は調整が必要）
- 挿入画像のサイズ・配置
- 画像生成時のアスペクト比（Gemini API）

### フォーマット別テロップ調整

| 設定 | youtube (16:9) | short (9:16) | square (1:1) |
|------|---------------|--------------|-------------|
| fontSize | 80 | 60 | 70 |
| position.bottom | 100 | 150 | 120 |
| maxWidth | 85% | 90% | 90% |
| Title fontSize | 42 | 32 | 36 |

## 画像生成（Gemini API）

挿入画像・インフォグラフィックの生成に使用。

```bash
# 基本
python scripts/run.py api_generator.py --prompt "説明図" -a 16:9

# アスペクト比は動画フォーマットに連動
# youtube → -a 16:9
# short   → -a 9:16
# square  → -a 1:1
```

- スクリプト: `.claude/skills/gemini-api-image/scripts/run.py`
- 環境変数: `GEMINI_API_KEY`
- 生成先: `<PROJECT>/public/images/`

## データスキーマ（全スキル共通の信頼できる唯一の定義）

### project-config.json

```json
{
  "format": "youtube",
  "resolution": { "width": 1920, "height": 1080 },
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
  "createdAt": "2026-03-25",
  "transcribe": {
    "os": "darwin-arm64",
    "engine": "mlx-whisper",
    "model": "large-v3",
    "language": "ja",
    "venv": ".venv"
  }
}
```

### transcript.json / transcript_fixed.json

```json
{
  "engine": "mlx-whisper",
  "model": "large-v3",
  "language": "ja",
  "duration_ms": 60000,
  "text": "全文テキスト",
  "words": [
    { "text": "こんにちは", "start": 1200, "end": 1800, "confidence": 0.95 }
  ],
  "segments": [
    { "text": "こんにちは、今日は...", "start": 1200, "end": 5400 }
  ]
}
```

- `start` / `end` は**ミリ秒**
- `confidence` は 0.0〜1.0
- transcript_fixed.json は追加で `fix_meta` を持つ

### telopData.ts（TelopSegment型）

```typescript
interface TelopSegment {
  id: number;
  startFrame: number;       // フレーム番号
  endFrame: number;
  text: string;
  highlight?: string;
  style?: 'normal' | 'emphasis' | 'warning' | 'success';
  template?: 1 | 2 | 3 | 4 | 5 | 6;
  animation?: 'none' | 'slideIn' | 'fadeOnly' | 'slideFromLeft' |
              'fadeBlurFromBottom' | 'slideLeftFadeBlur' |
              'fadeFromRight' | 'fadeFromLeft' | 'charByChar';
}
```

### titleData.ts（TitleSegment型）

```typescript
interface TitleSegment {
  id: number;
  startFrame: number;
  endFrame: number;
  text: string;
}
```

### cutData.ts（CutSegment型）

```typescript
interface CutSegment {
  id: number;
  originalStart: number;   // 元動画のフレーム
  originalEnd: number;
  playbackStart: number;   // カット後の再生フレーム
  playbackEnd: number;
}
```

### seData.ts（SoundEffect型）

```typescript
type SoundEffect = {
  id: number;
  startFrame: number;
  file: string;
  volume?: number;
};
```

## ファイルパス規約

| ファイル | パス |
|---------|------|
| プロジェクト設定 | `<PROJECT>/project-config.json` |
| 文字起こし生データ | `<PROJECT>/transcript.json` |
| 文字起こし修正済み | `<PROJECT>/transcript_fixed.json` |
| 修正履歴 | `<PROJECT>/transcript_corrections.json` |
| 誤字辞書 | `<PROJECT>/typo_dict.json` |
| 音声ファイル | `<PROJECT>/transcript_audio.wav` |
| VAD結果 | `<PROJECT>/vad_result.json` |
| カットデータ | `<PROJECT>/src/cutData.ts` |
| テロップデータ | `<PROJECT>/src/テロップテンプレート/telopData.ts` |
| テロップスタイル | `<PROJECT>/src/テロップテンプレート/telopStyles.ts` |
| テロップ型定義 | `<PROJECT>/src/テロップテンプレート/telopTypes.ts` |
| タイトルデータ | `<PROJECT>/src/Title/titleData.ts` |
| SEデータ | `<PROJECT>/src/SoundEffects/seData.ts` |
| ベース動画 | `<PROJECT>/public/main.mp4` |
| SE素材 | `<PROJECT>/public/se/` |
| BGM素材 | `<PROJECT>/public/BGM/` |
| 挿入画像 | `<PROJECT>/public/images/` |
| Python仮想環境 | `<PROJECT>/.venv/` |
| 生成画像 | `<PROJECT>/public/images/generated/` |
| Gemini APIスクリプト | `~/.claude/skills/gemini-api-image/scripts/run.py` |

## 用語統一ルール

| 正式名称 | 使わない表記 |
|---------|-------------|
| `TelopSegment` | SubtitleSegment |
| `telopData` | subtitleData |
| `テロップテンプレート/` | Subtitles/ |
| `transcript_fixed.json` | transcript_corrected.json |
| `transcript_audio.wav` | /tmp/supermovie_audio.wav |

## アップデート手順

「アップデートして」と言われたら以下を実行:

```bash
# 1. リモートの変更を取得
cd ~/.claude/plugins/supermovie && git fetch origin

# 2. 差分を確認
git log HEAD..origin/main --oneline

# 3. 変更がある場合のみpull
git pull origin main
```

**変更があった場合、ユーザーに報告:**
```
📦 SuperMovie アップデート完了

更新内容:
- <コミットメッセージ1>
- <コミットメッセージ2>

⚠️ 新しいスキルが追加された場合はセッション再起動が必要です。
```

**変更がない場合:**
```
✅ SuperMovie は最新版です（現在: <最新コミットハッシュ短縮>）
```

## スキル間の依存関係

- `supermovie-init` がヒアリングで `format` を決定 → 全スキルに影響
- `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
- `supermovie-se` は `src/テロップテンプレート/telopData.ts` を読む
- 全スキルは `project-config.json` の `format` / `resolution` を参照してサイズ調整する
- AssemblyAI は `supermovie-transcribe` の話者分離時のみ使用
- 画像生成は `gemini-api-image` スキルを使用。アスペクト比は `format` に連動

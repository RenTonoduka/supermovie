# SuperMovie — プロジェクトルール

## 正規ワークフロー（必ずこの順序で実行）

```
/supermovie-init              ← ヒアリング → プロジェクト作成 + preflight_video.py
    ↓ project-config.json
/supermovie-transcribe        ← 文字起こし（ローカルWhisper or AssemblyAI）
    ↓ transcript.json
/supermovie-transcript-fix    ← 誤字修正（辞書 + Claude LLM）
    ↓ transcript_fixed.json
    ↓ （ユーザー確認ポイント）
/supermovie-cut               ← 不要区間カット（VAD + LLM分析）
    ↓ cutData.ts
/supermovie-subtitles         ← transcript_fixed.json → telopData.ts + titleData.ts
    ↓                          (BudouX 意味分割 + 30 templates registry)
/supermovie-slides            ← Phase 3-A/B/C: SlideSequence + slideData.ts
    ↓                          (deterministic / optional Anthropic LLM plan)
/supermovie-narration         ← Phase 3-D: VOICEVOX → public/narration.wav
    ↓                          (engine 不在で skip、--require-engine で fail)
/supermovie-image-gen         ← テロップ分析 → 画像生成 + insertImageData.ts (Roku 課金判断)
    ↓
/supermovie-se                ← telopData.ts + insertImageData.ts → seData.ts (Roku 素材判断)
    ↓
npm run dev                   ← Remotion Studioプレビュー
npm run render                ← out/video.mp4 出力
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
  "source": {
    "video": "main.mp4",
    "raw": { "width": 3840, "height": 2160 },
    "display": { "width": 2160, "height": 3840 },
    "rotation": { "raw": -90, "normalized": -90, "source": "Display Matrix" },
    "aspect": 0.5625,
    "sar": "1:1",
    "dar": null,
    "inferred_format": "short",
    "chosen_format": "short",
    "fps": {
      "r_frame_rate": "60/1",
      "avg_frame_rate": "503200/8387",
      "render_fps": 60,
      "vfr_metadata_suspect": false
    },
    "duration_sec": 41.93,
    "duration_frames": 2516,
    "codec": {
      "name": "hevc",
      "profile": "Main 10",
      "pix_fmt": "yuv420p10le",
      "field_order": "progressive"
    },
    "color": {
      "range": "tv",
      "space": "bt2020nc",
      "transfer": "arib-std-b67",
      "primaries": "bt2020",
      "hdr_suspect": true,
      "dovi": { "dv_profile": 8, "dv_level": 9 }
    },
    "streams": { "video": 1, "audio": 1, "subtitle": 0, "data": 5 },
    "risks": ["hdr-or-dovi", "10bit"],
    "requiresConfirmation": true
  },
  "transcribe": {
    "os": "darwin-arm64",
    "engine": "mlx-whisper",
    "model": "large-v3",
    "language": "ja",
    "venv": ".venv"
  }
}
```

**source.* schema は `template/scripts/preflight_video.py` が自動生成する。手書きで埋めない。**

**risks キー一覧** (Phase 2 罠ガードと一致):
`rotation-non-canonical` / `non-square-sar` / `unknown-aspect` / `vfr` / `hdr-or-dovi` / `10bit` / `interlaced` / `multiple-or-missing-video` / `multiple-or-missing-audio` / `embedded-subtitle`

`requiresConfirmation: true` の場合は Roku に risks 内容を提示してから次 phase に進む。

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

### insertImageData.ts（ImageSegment型）

```typescript
interface ImageSegment {
  id: number;
  startFrame: number;
  endFrame: number;
  file: string;
  type: 'photo' | 'infographic' | 'overlay';
  scale?: number;
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
| 挿入画像データ | `<PROJECT>/src/InsertImage/insertImageData.ts` |
| テロップデータ | `<PROJECT>/src/テロップテンプレート/telopData.ts` |
| テロップスタイル | `<PROJECT>/src/テロップテンプレート/telopStyles.ts` |
| テロップ型定義 | `<PROJECT>/src/テロップテンプレート/telopTypes.ts` |
| タイトルデータ | `<PROJECT>/src/Title/titleData.ts` |
| SEデータ | `<PROJECT>/src/SoundEffects/seData.ts` |
| 動画設定（SSoT） | `<PROJECT>/src/videoConfig.ts` |
| ベース動画 | `<PROJECT>/public/main.mp4` |
| SE素材 | `<PROJECT>/public/se/` |
| BGM 本体 (asset gate) | `<PROJECT>/public/BGM/bgm.mp3` |
| ナレーション本体 (asset gate) | `<PROJECT>/public/narration.wav` |
| 挿入画像（手動配置） | `<PROJECT>/public/images/` |
| 挿入画像（AI生成） | `<PROJECT>/public/images/generated/` |
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

## Visual Smoke (Phase 3-G、format 切替後の dimension 検査)

```bash
cd <PROJECT>
npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
npm run test           # lint + visual-smoke を一気に
```

`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
youtube → short → square と切替て `npx remotion still` を 2 frame ずつ生成、
各 PNG を ffprobe で検証する:

| format | 期待 dimension |
|--------|---------------|
| youtube | 1920 × 1080 |
| short   | 1080 × 1920 |
| square  | 1080 × 1080 |

mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
原本 `videoConfig.ts` は finally で必ず復元される (途中 fail 安全)。

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

- `supermovie-init` がヒアリングで `format` を決定 → `videoConfig.ts` を書き換え → 全コンポーネントに反映
- `videoConfig.ts` がFPS, 解像度, テロップサイズのSingle Source of Truth。各.tsxは直接値を持たない
- `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
- `supermovie-se` は `src/テロップテンプレート/telopData.ts` を読む
- 全スキルは `project-config.json` の `format` / `resolution` を参照してサイズ調整する
- AssemblyAI は `supermovie-transcribe` の話者分離時のみ使用
- 画像生成は `gemini-api-image` スキルを使用。アスペクト比は `format` に連動

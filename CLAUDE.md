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
/supermovie-subtitles         ← transcript_fixed.json → telopData.ts + titleData.ts
    ↓
/supermovie-se                ← telopData.ts → seData.ts
    ↓
npm run dev                   ← Remotion Studioプレビュー
```

## データスキーマ（全スキル共通の信頼できる唯一の定義）

### project-config.json

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

## 用語統一ルール

| 正式名称 | 使わない表記 |
|---------|-------------|
| `TelopSegment` | SubtitleSegment |
| `telopData` | subtitleData |
| `テロップテンプレート/` | Subtitles/ |
| `transcript_fixed.json` | transcript_corrected.json |
| `transcript_audio.wav` | /tmp/supermovie_audio.wav |

## スキル間の依存関係

- `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
- `supermovie-se` は `src/テロップテンプレート/telopData.ts` を読む
- 全スキルは `project-config.json` を参照できる
- AssemblyAI は `supermovie-transcribe` の話者分離時のみ使用

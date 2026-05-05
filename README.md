# SuperMovie

Remotionベースの動画編集自動化ツール。
Claude Code のスキルで、テロップ・SE・タイトルを自動生成。
**誰でも簡単にプロ品質の動画編集ができる。**

## 使い方

### 方法1: Claude Code Plugin（推奨）

```bash
# 1. リポジトリをクローン
git clone https://github.com/RenTonoduka/supermovie.git ~/.claude/plugins/supermovie

# 2-A. 起動時にプラグイン指定
claude --plugin-dir ~/.claude/plugins/supermovie

# 2-B. または settings.json に追加して常に有効化（推奨）
# ~/.claude/settings.json に以下を追加:
# "pluginDirs": ["~/.claude/plugins/supermovie"]
```

インストール後、Claude Code で以下のスキルが使えます:

| スキル | コマンド | 機能 |
|--------|---------|------|
| プロジェクト作成 | `/supermovie-init` | ヒアリング → Remotionプロジェクト自動生成 |
| 文字起こし | `/supermovie-transcribe` | ローカルWhisperで高精度文字起こし |
| 誤字修正 | `/supermovie-transcript-fix` | 辞書 + Claude LLMで誤字脱字修正 |
| 動画カット | `/supermovie-cut` | Silero VAD + LLM分析で不要区間カット |
| テロップ生成 | `/supermovie-subtitles` | LLM意味分割 + 改行処理でテロップ生成 |
| 画像生成 | `/supermovie-image-gen` | Gemini APIで図解・画像を自動生成・配置 |
| SE配置 | `/supermovie-se` | テロップ+画像分析 → 効果音自動配置 |
| テロップ作成 | `/supermovie-telop-creator` | 新テロップスタイルをデザイン |
| スキル追加 | `/supermovie-skill-creator` | 新しいスキルを設計・追加 |

#### クイックスタート

```
あなた: 動画プロジェクトを作成して
        /path/to/your-video.mp4

Claude: ヒアリング → プロジェクト生成 → 文字起こし → 誤字修正 → カット → テロップ → 画像生成 → SE → 完成
```

#### プラグインの更新

```bash
cd ~/.claude/plugins/supermovie && git pull
```

### 方法2: GitHub Template

1. このリポジトリの「**Use this template**」ボタンをクリック
2. `template/` フォルダをコピーしてプロジェクト開始
3. データファイルを編集して動画をカスタマイズ

```bash
# テンプレートからプロジェクト作成
cp -r template/ my-video-project/
cd my-video-project/
bash ../scripts/safe_rsync.sh --init-sentinel --dest .  # safe rsync 用 sandbox sentinel 作成
npm install
npm run dev    # Remotion Studio起動
```

> **既存 project への template 同期は `rsync --delete` 直接禁止**。Roku の前 work artifact (`typo_dict.json` / `transcript_*.json` / `vad_result.json` 等) を消す事故が 2026-05-05 16:14 に発生済み。template 同期は `bash scripts/safe_rsync.sh --source <repo>/template --dest <project>` を使う (default dry-run、`--apply` で実 sync、`scripts/safe_rsync.protect` の protect list 違反時に停止)。

## テンプレート構成

```
template/
├── src/
│   ├── Root.tsx                    ← 動画設定（FPS, フレーム数）
│   ├── MainVideo.tsx               ← 5レイヤー合成
│   ├── テロップテンプレート/         ← 6テンプレート × 9アニメーション
│   │   ├── Telop.tsx               ← 統合テロップコンポーネント
│   │   ├── TelopPlayer.tsx         ← テロップ再生
│   │   ├── telopData.ts            ← テロップデータ（★ここを編集）
│   │   ├── telopStyles.ts          ← スタイル定義
│   │   └── telopTypes.ts           ← 型定義
│   ├── メインテロップ/              ← 白青テロップ × 2バリエーション
│   ├── 強調テロップ/                ← 赤文字、オレンジグラデーション
│   ├── ネガティブテロップ/           ← 黒文字白背景、残酷紺、黒紫グラデ
│   ├── Title/                      ← セグメントタイトル
│   ├── SoundEffects/               ← SE + BGM
│   └── InsertImage/                ← 画像挿入
└── public/
    ├── main.mp4                    ← ベース動画
    ├── se/                         ← 効果音素材
    ├── BGM/                        ← BGM素材
    └── images/                     ← 挿入画像
```

## テロップスタイル一覧

### メインテロップ（通常会話）
| スタイル | 特徴 |
|---------|------|
| 白青テロップ | 白文字 + 青ストローク。シンプルで読みやすい |
| 白青テロップver2 | ダブルストローク（外側白＋内側青）。より立体的 |

### 強調テロップ
| スタイル | 特徴 |
|---------|------|
| 赤文字 | 赤文字 + 白ストローク。インパクト重視 |
| オレンジグラデーション | ダブルストローク + 黄金縁取り。高級感 |

### ネガティブテロップ
| スタイル | 特徴 |
|---------|------|
| 黒文字白背景 | 白背景ボックス + 黒文字。シンプル |
| 残酷テロップ・紺 | 筆体フォント + 紺色ダブルストローク |
| 黒紫グラデ | 黒→紫の垂直グラデーション + 多層影 |

## 動画レイヤー構成

```
┌──────────────────────────────┐
│          効果音 (SE)          │  ← 最前面（音声のみ）
├──────────────────────────────┤
│          BGM                  │
├──────────────────────────────┤
│     セグメントタイトル（左上）   │
├──────────────────────────────┤
│       テロップ（下部）          │
├──────────────────────────────┤
│       挿入画像/動画            │
├──────────────────────────────┤
│        ベース動画              │  ← 最背面
└──────────────────────────────┘
```

## 必要環境

- Node.js 18+
- npm or yarn
- ffmpeg（動画解析・音声抽出に使用）

### Claude Codeスキル使用時の追加要件
- [Claude Code](https://claude.ai/claude-code)
- GEMINI_API_KEY（画像生成に使用）
- AssemblyAI APIキー（話者分離が必要な場合のみ。1人の場合はローカルWhisperで無料）

## ライセンス

MIT

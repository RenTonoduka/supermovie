# SuperMovie 将来 Feature 要件定義 v0 (2026-05-05 起草)

本 doc は Roku 発言 (前セッション 869aaf03-...jsonl 2026-05-04T06:58 実測) を起点に、Phase 3-V release-ready 後の未着手 scope を整理する v0 draft。

**v0 構造**: 構造 + 範囲 + roadmap 骨子 + リスク framework は Claude 起草で verify 済み、詳細技術選定 (各ツールの benchmark / コスト / OSS active 度 / 法規制現状) は **[要 Codex 補完]** marker、後続 bg consult 経由で v0.1 で埋める方針。

## 0. メタ情報

- **作成**: 2026-05-05 09:35 (Claude 起草、Codex 補完 pending)
- **HEAD reference**: `roku/phase3j-timeline` `21dd075` (Phase 3-V release-ready + post-freeze backlog P1-P4 反映済)
- **位置**: `docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md` (Phase 3 release 済み artifact と分離)
- **next review**: Codex で §4 / §7 fill-in 後、Roku で §6 判断

## 1. 目的とスコープ境界

### 1.1 Roku 発言 (verbatim、869aaf03-...jsonl 2026-05-04T06:58 Bash 実測)

> 「スライド生成の技術とかと合わせたら、スライドをAIアバターに解説させるようなセミナー動画とかを作れたりするのかな？スライドも、自動的に入れ替わる編集などができるのかな。できる方法を探すだけだよな。将来はそういうこともやりたいと思っている。ショート動画の制作やYouTubeの制作、動画教材の制作もやりたい。将来的にそういうことを見越して、できるようになりたいから、少しCodexとClaude Codeを協力してリサーチしてみてほしい。今やらなくてもいいかもしれないけど、将来的にできるかどうかも知りたい。で、それをこのパイプライン上でやるのか、別パイプラインに組み込むのか、今のパイプラインを拡張させていくのかっていうのは...」

### 1.2 やりたいこと (4 領域)

| # | 領域 | 概要 |
|---|---|---|
| 1 | 動画教材制作 (lesson video) | 講義スライド + 解説 narration + 章立て、長尺 (10-30 min) |
| 2 | AI アバター解説セミナー動画 | スライド + talking head アバター話者、長尺 |
| 3 | YouTube 長尺動画 | 上記 1+2 を統合した自動生成 10-30min コンテンツ |
| 4 | ショート動画 高度編集 | Instagram リール / TikTok 流の高速カット・テロップ・SE 編集 |

### 1.3 Phase 3-V 既存範囲との境界

| 項目 | Phase 3-V (release-ready) | 将来 feature |
|---|---|---|
| timeline pipeline | ✅ init→transcribe→cut→narration→subtitles→render | (基盤として再利用、拡張) |
| スライド生成 | ✅ generate_slide_plan.py (Anthropic API word index) + build_slide_data.py | スライド自動切替 / 章立て連動が拡張対象 |
| 動画 input | ✅ 既存 main.mp4 を編集する前提 | アバター動画 / 完全合成動画は別 |
| 音声 | ✅ VOICEVOX local TTS (template/scripts/voicevox_narration.py) | アバター用 voice cloning は別 |
| アバター描画 | ❌ なし | 新規 (talking head 合成) |
| 画像生成 | (memo: Gemini 統合候補、PHASE3_RELEASE_NOTE.md:125) | 動画教材の挿入図、infographic 自動生成 |
| 動画生成 | (memo: Kling 統合候補、PHASE3_RELEASE_NOTE.md:127) | B-roll、シーン挿入 |

## 2. 段階的 Roadmap (Phase 4 → 5 → 6)

各 Phase は **Phase 3-V release-ready 状態を破壊しない** 前提。新機能は optional asset gate (既存パターン、handoff:11) で skip 可能に追加。

### Phase 4: 動画教材最小構成 (lesson video v0)

| 項目 | 内容 |
|---|---|
| 目的 | スライド + narration の組合せで 5-10 min の章立て型 lesson video を出力 |
| 前提 | Phase 3-V timeline pipeline、generate_slide_plan、VOICEVOX |
| 成果物 | `<PROJECT>/src/Chapter/chapterData.ts` (章立てデータ)、`Chapter` Remotion component (slide + narration sync) |
| 検証ゲート | python smoke (chapter timeline integration test)、React component test (Chapter render) |
| 依存技術 | Anthropic API (chapter plan)、VOICEVOX (既)、既存 slide |
| 想定 effort | M (timeline.py の chapter helper、build_chapter_data.py、Remotion component、test) |
| API 課金 | Anthropic Haiku 4-5 ~$0.10/章 plan 生成想定 [要 Codex 補完で実コスト見積] |
| Roku 判断領域 | chapter 自動分割 prompt 設計、分量設計 |

### Phase 5: スライド自動切替 + B-roll 挿入 (visual richness v0)

| 項目 | 内容 |
|---|---|
| 目的 | 章ごとに自動切替、各スライドに静止画 / B-roll 挿入で視覚情報密度を上げる |
| 前提 | Phase 4 完了、画像生成 API (Gemini or 別) 統合 |
| 成果物 | `insertImageData.ts` の自動生成版、Phase 5 Studio preview |
| 検証ゲート | image asset gate (生成失敗時 skip)、visual smoke 拡張 |
| 依存技術 | Gemini image API (既存 supermovie-image-gen skill 拡張)、Anthropic API (image prompt 生成) |
| 想定 effort | M-L (画像生成 API 統合、prompt design、品質 gate) |
| API 課金 | Gemini ~$0.04/image × N images [要 Codex 補完] |
| リスク (memo only、Roku 判断領域) | 法的: 生成画像の著作権 / 商用利用条件、品質: 生成失敗率 |

### Phase 6: AI アバター解説 (talking head v0)

| 項目 | 内容 |
|---|---|
| 目的 | スライド + アバター話者で セミナー動画スタイル |
| 前提 | Phase 5 完了 (スライド構造)、アバター技術選定 |
| 成果物 | `Avatar` Remotion component、avatar 合成 pipeline (offline batch) |
| 検証ゲート | アバター still image render test、lip sync 簡易 metric |
| 依存技術 | [要 Codex 補完]: SadTalker / Wav2Lip (OSS) or HeyGen / D-ID (商用 API) |
| 想定 effort | L-XL (技術選定 + integration + 品質チューニング) |
| API 課金 | [要 Codex 補完] 商用 API ~$0.20-0.50/min 想定、OSS 自前 GPU の場合は infra cost |
| **リスク (memo only、Roku 判断領域)** | 法的: deepfake 規制 / 本人許諾、モラル: 偽情報生成 / なりすまし、品質: uncanny valley、信頼喪失リスク |

## 3. 統合パス選択肢

### Option A: 既存 supermovie に拡張 (1 plugin / 1 repo)

| 観点 | 評価 |
|---|---|
| 再利用性 | 高 (transcript / VAD / narration / slide 共通) |
| 複雑度 | 中-高 (skill 数増加、CLAUDE.md / SKILL.md 更新) |
| migration cost | 低 (既存 user project が自動恩恵) |
| 並列開発 | 低 (1 repo で複数 phase 同時開発はコンフリクト) |
| 推奨度 | Phase 4-5 にはこれ |

### Option B: 別 plugin / 別 repo

| 観点 | 評価 |
|---|---|
| 再利用性 | 低 (共通 backbone を再実装 or shared lib 化必要) |
| 複雑度 | 低-中 (各 repo が小さい) |
| migration cost | 高 (user は plugin 切替 / 複数 install) |
| 並列開発 | 高 (独立 repo で並列 OK) |
| 推奨度 | Phase 6 (アバター系) のように法的・課金リスクの強い領域 |

### Option C: ハイブリッド (共通 backbone + format-specific frontend)

| 観点 | 評価 |
|---|---|
| 再利用性 | 高 (backbone shared) |
| 複雑度 | 高 (interface 設計 / monorepo 運用) |
| migration cost | 中 |
| 並列開発 | 中-高 |
| 推奨度 | 長期 vision として、Phase 6+ で検討 |

**推奨**: Phase 4-5 は Option A (拡張)、Phase 6 は Option B/C (アバター固有のリスクと開発粒度を分離)。

## 4. 技術選定マトリクス v0 [要 Codex 補完]

各セルの数値 / 評価 / OSS active 度 は Codex consult で fill-in 予定。Claude による暫定 framework のみ。

### 4.1 AI アバター (Phase 6 候補)

| ツール | 種別 | 機能 | コスト | 品質 | 統合難度 | 法的・モラル制約 (memo only) |
|---|---|---|---|---|---|---|
| SadTalker | OSS (PyTorch) | talking head 静止画 + 音声 → 動画 | self-host GPU | [要 Codex 補完] | 中 (Python) | deepfake 規制圏で利用注意 |
| Wav2Lip | OSS | lip sync 特化 | self-host GPU | [要 Codex 補完] | 中 | 同上 |
| HeyGen | 商用 API | アバター + 音声 → 動画 | [要 Codex 補完] | [要 Codex 補完] | 低 (API 1 call) | 商用利用条件、本人許諾 |
| D-ID | 商用 API | 同上 | [要 Codex 補完] | [要 Codex 補完] | 低 | 同上 |
| Synthesia | 商用 API | スライド + アバター統合 | [要 Codex 補完] | [要 Codex 補完] | 中 (UI 連携) | 同上 |
| Hedra | 商用 API | character video gen | [要 Codex 補完] | [要 Codex 補完] | 中 | 同上 |

### 4.2 画像生成 (Phase 5 候補)

| ツール | 種別 | コスト | 品質 | 統合難度 | 既存 supermovie 連携 |
|---|---|---|---|---|---|
| Gemini (image) | 商用 API | [要 Codex 補完] | [要 Codex 補完] | 低 | 既 skill (gemini-api-image)、CLAUDE.md (supermovie):55 で推奨形式 |
| SDXL | OSS | self-host GPU | [要 Codex 補完] | 高 (infra) | 別途 infra 必要 |
| FLUX | OSS / API | [要 Codex 補完] | [要 Codex 補完] | 中 | API 経由可能 |
| Imagen | 商用 API | [要 Codex 補完] | [要 Codex 補完] | 中 | Google API |

### 4.3 動画生成 (Phase 5+ 候補、B-roll / シーン挿入)

| ツール | 種別 | コスト | 品質 | 統合難度 |
|---|---|---|---|---|
| Kling | 商用 API | [要 Codex 補完] | [要 Codex 補完] | 中 |
| Runway | 商用 API | [要 Codex 補完] | [要 Codex 補完] | 中 |
| Pika | 商用 API | [要 Codex 補完] | [要 Codex 補完] | 中 |
| Sora | 商用 API (限定アクセス) | [要 Codex 補完] | [要 Codex 補完] | 高 (アクセス申請) |

### 4.4 音声合成 (拡張 / アバター用)

| ツール | 種別 | コスト | 既存 supermovie 連携 |
|---|---|---|---|
| VOICEVOX | OSS local | 0 | ✅ 既存 (Phase 3-D で統合済、template/scripts/voicevox_narration.py) |
| Style-Bert-VITS2 | OSS local | 0 (GPU 推奨) | 別途 infra 必要 |
| ElevenLabs | 商用 API | [要 Codex 補完] | 拡張 narration mode 候補 |
| OpenAI TTS | 商用 API | [要 Codex 補完] | 簡易 fallback 候補 |

## 5. リスク (memo only、Roku 判断領域、断定推奨せず並列提示)

### 5.1 法的

- AI アバター (SadTalker / HeyGen 等) は **deepfake 規制** に抵触する可能性 (国・州ごとに異なる、要法務相談)
- 生成画像 / 生成動画の **著作権 / 商用利用条件** は各 API ToS で確認必要
- 教材コンテンツの **本人許諾** (アバター話者として誰の顔を使うか)
- [要 Codex 補完]: 現行法 (US / EU / JP / 中国) の deepfake 規制比較

### 5.2 モラル

- アバター動画は受講者を **誤誘導 / なりすまし** リスク (本人と勘違いされる)
- 偽情報 / hallucination 含むコンテンツの自動量産リスク
- 信頼喪失: AI 生成コンテンツとの開示有無

### 5.3 課金

- 商用 API 統合は **コスト ceiling** + rate limit 必要
- 予算 over の検出 (cost guard、observability)
- 1 動画あたり想定コスト見積を Phase 単位で先行検証

### 5.4 品質

- アバターの **uncanny valley** (公開ベンチで評価)
- lip sync 精度 / 音声品質
- 章立てロジックが破綻していないかの検証 gate

## 6. オープンクエスチョン (Roku 判断領域、答え保留)

1. **Q1**: 5/13 リリース branch (Phase 3-V) merge 後、Phase 4 着手は何ヶ月後想定?
2. **Q2**: アバター用顔画像 (Phase 6) は Roku 自身 / 雇用ナレーター / 完全合成のどれ?
3. **Q3**: 商用 API 月予算上限 (Anthropic + Gemini + アバター API + 動画生成) は?
4. **Q4**: 教材動画の主用途は HugRuma 内部研修 / 外販 LMS / YouTube 公開のどれ?
5. **Q5**: 動画教材の最終 publish 先は LMS / YouTube / 別 plugin?
6. **Q6**: ショート動画 (Instagram リール風) と長尺教材 (YouTube 風) は同じ pipeline か別か?
7. **Q7**: アバター技術選定 (OSS self-host vs 商用 API) は infra 設備投資 / API 課金のどちら寄り?

## 7. 既知の罠 / 過去事例 [要 Codex 補完]

- [要 Codex 補完]: SadTalker / Wav2Lip 公開ベンチでの平均品質指標
- [要 Codex 補完]: HeyGen / D-ID の運用事故事例 (本人許諾なしで使われた事案)
- [要 Codex 補完]: Kling / Runway の rate limit 実態
- [要 Codex 補完]: 各 OSS の active 度 (commit frequency、issue 対応速度)
- [要 Codex 補完]: deepfake 規制の現行法 (US / EU / JP)

## 8. 次ステップ

- [ ] Codex consult で §4 / §7 の [要 Codex 補完] を埋める (smaller scope で再 kick、本 commit と並行)
- [ ] Roku 復帰時に §6 オープンクエスチョン 7 件への判断を求める
- [ ] Phase 4 開始判断は §6 Q1 / Q3 / Q4 確定後

---

**起草経緯メモ**: 当初 Codex に 1 prompt で全 8 章を起草依頼したが、30 min 進捗 0 で stuck (PID 73874 sleeping、tee buffer 0 byte)。Codex CLI 健全性は別途 tiny test (`OK alive`) で確認済み、複合 prompt の生成失敗が原因と推定。本 v0 は構造・verifiable 部分を Claude 起草、詳細 marker を smaller scope で再 consult する分担に切替。

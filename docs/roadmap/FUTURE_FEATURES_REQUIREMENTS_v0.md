# SuperMovie 将来 Feature 要件定義 v0 (2026-05-05 起草)

本 doc は Roku 発言 (前セッション 869aaf03-...jsonl 2026-05-04T06:58 実測) を起点に、Phase 3-V release-ready 後の未着手 scope を整理する v0 draft。

**v0 構造**: 構造 + 範囲 + roadmap 骨子 + リスク framework は Claude 起草で verify 済み。詳細技術選定 (§4) と既知の罠 / 過去事例 / 法規制現状 (§7) は Codex fill-in 反映済 (794e3bc、35 citations [S1]-[S35]、一次情報中心。一部は第三者 (G2 / Renderful 等) または報道として明示)。価格 hardcode は invariant 上禁止、各 Phase 着手判断時に Roku + Codex で再 consult する方針。

## 0. メタ情報

- **作成**: 2026-05-05 09:35 (Claude 起草) / **Codex fill-in 反映**: 2026-05-05 09:51 (CODEX_FUTURE_FILLIN_20260505T094327.md → 794e3bc 経由 §4/§7 + §9 References)
- **HEAD reference**: `roku/phase3j-timeline` `a85bdb1` (Phase 3-V release-ready + post-freeze backlog P1-P4 + v0 fill-in + drift fix 全反映済)
- **位置**: `docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md` (Phase 3 release 済み artifact と分離)
- **next review**: §6 オープンクエスチョン 7 件への Roku 判断 / §2 Phase 単位 API 課金見積の再 consult (各 Phase 着手判断時)

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
| API 課金 | [Roku 判断 + Phase 4 着手判断時に再 consult、価格 hardcode invariant 禁止、§4.1/4.4 一次情報 citation 参照] |
| Roku 判断領域 | chapter 自動分割 prompt 設計、分量設計 |

### Phase 5: スライド自動切替 + B-roll 挿入 (visual richness v0)

| 項目 | 内容 |
|---|---|
| 目的 | 章ごとに自動切替、各スライドに静止画 / B-roll 挿入で視覚情報密度を上げる |
| 前提 | Phase 4 完了、画像生成 API (Gemini or 別) 統合 |
| 成果物 | `insertImageData.ts` の自動生成版、Phase 5 Studio preview |
| 検証ゲート | image asset gate (生成失敗時 skip)、visual smoke 拡張 |
| 依存技術 | Gemini image API (既存 supermovie-image-gen skill 拡張)、Anthropic API (image prompt 生成)、動画生成 API (Kling / Runway / Pika / Sora 等、§4.3 候補) — B-roll 挿入対応 |
| 想定 effort | M-L (画像生成 API 統合、prompt design、品質 gate) |
| API 課金 | [Roku 判断 + Phase 5 着手判断時に再 consult、価格 hardcode invariant 禁止、§4.2/4.3 一次情報 citation 参照] |
| リスク (memo only、Roku 判断領域) | 法的: 生成画像の著作権 / 商用利用条件、品質: 生成失敗率 |

### Phase 6: AI アバター解説 (talking head v0)

| 項目 | 内容 |
|---|---|
| 目的 | スライド + アバター話者で セミナー動画スタイル |
| 前提 | Phase 4 完了 (slide + narration sync 成果物、§Phase 4 Chapter component)、アバター技術選定 — Phase 5 は B-roll / 画像 visual richness 拡張で Phase 6 必須ではない |
| 成果物 | `Avatar` Remotion component、avatar 合成 pipeline (offline batch) |
| 検証ゲート | アバター still image render test、lip sync 簡易 metric |
| 依存技術 | SadTalker / Wav2Lip (OSS、self-host GPU) or HeyGen / D-ID / Synthesia / Hedra (商用 API) — §4.1 一次情報 citation 参照、最終選定は Phase 6 着手時 Roku + Codex consult |
| 想定 effort | L-XL (技術選定 + integration + 品質チューニング) |
| API 課金 | [Roku 判断 + Phase 6 着手判断時に再 consult、価格 hardcode invariant 禁止、§4.1 一次情報 citation 参照、OSS 自前 GPU の場合は infra cost も Roku 判断] |
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

## 4. 技術選定マトリクス v0

評価凡例: 品質は「公開ベンチあり」は数値優先、「公開ベンチ未確認」は demo / API 仕様ベースの暫定評価。統合難度は API / file format / setup の観点。citation 方針: (a) Codex consult (CODEX_FUTURE_FILLIN 20260505T094327) で fill-in した cell は [S*] citation 付き (一次情報中心、一部は第三者 G2 / Renderful 等または報道として明示、§9 References)、(b) 既存 supermovie 採用 OSS (VOICEVOX 等) は public_reference 公式 repo / 採用済み事実で代替 (本 doc 内 [S*] index 不要)、(c) 暫定候補 (一次情報未確認、Phase 着手時 consult 対象) は [S*] index なしで「[一次情報未確認]」マーカー明示 (Style-Bert-VITS2 等)。3 種いずれにも該当しない citation 漏れがあれば P1。

### 4.1 AI アバター (Phase 6 候補)

| ツール | 種別 | 機能 | コスト | 品質 | OSS active 度 | 統合難度 | 法的・モラル制約 (memo only) |
|---|---|---|---|---|---|---|---|
| SadTalker | OSS (PyTorch) | 静止画 + 音声 → talking head | self-host GPU / API 価格なし | 中: HDTF cross-ID で LSE-C 7.343 / LSE-D 7.709、Wav2Lip より lip sync は弱いが head motion あり [S1] | 13.8k stars、直近 commit 2023-10、open issues 617 / PR 39 [S2] | 高: Python 3.8 + Torch + ffmpeg + checkpoints + face enhancer [S2] | 本人許諾・合成開示・用途限定が必要 |
| Wav2Lip | OSS | 既存動画の lip sync 特化 | self-host GPU / API 価格なし | 高(lip sync) / 中(画質): LRS2 で LSE-D 6.386 / LSE-C 7.789、GAN 版は画質改善だが sync 微低下 [S3] | 12.9k stars、直近 commit 2025-06、open issues 337 / PR 29 [S4] | 中-高: Python + ffmpeg + checkpoint、旧 OSS は非商用・commercial は Sync Labs 誘導 [S4] | 既存人物動画の改変なので許諾・表示が必須 |
| HeyGen | 商用 API | avatar video / translation / LiveAvatar | API pay-as-you-go: 標準 avatar video $1/min、Avatar IV $4/min、translation $2/min、TTS Starfish $0.04、最小 $5 credit [S5] | 中-高(暫定): 公開ベンチ未確認、vendor demo/API 機能ベース | N/A | 低: Direct API / MCP / Skills、API concurrency 10 videos [S5] | Digital Twin / custom avatar は Enterprise 制限あり [S5] |
| D-ID | 商用 API | talking portrait / agents / video translate | 公式 API price page は金額本文取得不可。公式FAQでは API minutes は web plan balance から控除、G2 掲載値は Lite $4.70/mo annual, Pro $16/mo annual, Advanced $108/mo annual [S6][S7] | 中(暫定): 公開ベンチ未確認、watermark / ethics 表示重視 [S6] | N/A | 低-中: API key + minutes balance、動画長は 15 秒単位切上げ [S6] | Trial/Lite watermark は synthetic transparency 方針 [S6] |
| Synthesia | 商用 SaaS/API | スライド + avatar + dubbing | Starter $29/mo、Creator $89/mo、Enterprise custom。API access は Creator 以上、Creator は 360 min/year 相当 [S8] | 中-高(暫定): 公開ベンチ未確認、L&D 向け完成度重視 | N/A | 中: API は Creator 以上、workspace / template 前提 [S8] | stock / personal avatar の権利・開示が前提 |
| Hedra | 商用 SaaS | character video gen | Basic $15/mo、Creator $30/mo、Professional/Teams $75/mo、Enterprise custom [S9] | 中(暫定): 公開ベンチ未確認 | N/A | 中: pricing は公開、API 仕様の公開確認は別途必要 [S9] | character / voice の本人許諾が必要 |

### 4.2 画像生成 (Phase 5 候補)

| ツール | 種別 | コスト | 品質 | OSS active 度 | 統合難度 | 既存 supermovie 連携 |
|---|---|---|---|---|---|---|
| Gemini image | 商用 API | Gemini image generation は paid tier $0.039/image、Batch $0.0195/image [S10] | 中-高: Gemini 2.5 Flash Image は conversational image gen、SynthID watermark あり [S11] | N/A | 低: Gemini API で text/image 入力 | 既 skill 拡張候補 |
| SDXL | OSS | self-host GPU / API 価格なし | 中: SDXL 1.0 は公開済みだが世代は古め、release は 2023-07 [S12] | 27.1k stars、latest release 2023-07、issues 286 / PR 56 [S12] | 高: local GPU / ComfyUI 等の infra 必要 | 別途 infra 必要 |
| FLUX | OSS / API | BFL API: FLUX.1 Kontext pro $0.04/image、max $0.08/image、FLUX.2 klein from $0.014/image、FLUX.2 pro from $0.03/MP [S13] | 高(暫定): BFL は FLUX.2 を latest generation / text rendering 改善と説明 [S14] | FLUX.1 repo 25.4k stars、直近 update 2025-07。FLUX.2 repo 2.2k stars、2026-03 update [S15] | 中: API は低、local は VRAM 要件あり | API 経由が現実的 |
| Imagen | 商用 API | Imagen 4 Fast $0.02/image、Standard $0.04/image、Ultra $0.06/image、Imagen 3 $0.03/image [S16] | 高: Imagen 4 は text rendering と全体品質改善の公式説明あり [S16] | N/A | 低-中: Gemini API / Imagen model 指定 | Google API 統合候補 |

### 4.3 動画生成 (Phase 5+ 候補、B-roll / シーン挿入)

| ツール | 種別 | コスト | 品質 | 統合難度 | rate limit / 運用 memo |
|---|---|---|---|---|---|
| Kling | 商用 API | 公式(Kuaishou直)価格は公開情報未確認。klingapi.com は $1 free credits と async API を記載、第三者 Renderful は $0.20-$1.40/generation と記載 [S17][S18] | 中-高(暫定): 公開ベンチ未確認 | 中: async submit + polling | rate limit は公式一次情報未確認 |
| Runway | 商用 API | credits は $0.01/credit。gen4_turbo 5 credits/sec = $0.05/sec、gen4.5 12 credits/sec = $0.12/sec [S19] | 中-高(暫定): 公開ベンチ未確認 | 中: API + async job | Tier1 concurrency 1 / 50 gens/day、Tier3 concurrency 5 / 1,000 gens/day、超過時 THROTTLED または 429 [S20] |
| Pika | 商用 SaaS/API | Web: Standard $8/mo annual / Pro $28/mo annual / Fancy $76/mo annual。API: Pika 1.0 $0.05/sec、1.5 $0.07/sec、2.0 $0.11-$0.156/sec [S21][S22] | 中(暫定): 公開ベンチ未確認 | 中: API は early-access / Fal.ai 導線 | API rate limit 20 generations/min、MP4 720p [S22] |
| Sora | 商用 API preview | sora-2 $0.10/sec、sora-2-pro $0.30/sec(720p)、$0.50/sec(1024x1792) [S23] | 高: Sora 2 Pro は production-quality / higher-resolution cinematic 向けと公式説明 [S24] | 中-高: preview API、async job + polling/webhook | real people 生成不可、human face input rejected など制約強い [S24] |

### 4.4 音声合成 (拡張 / アバター用)

| ツール | 種別 | コスト | 品質 | 統合難度 | 既存 supermovie 連携 |
|---|---|---|---|---|---|
| VOICEVOX | OSS local | 0 | 中: local TTS として既存採用済み | 低: 既存 script | 既存 (Phase 3-D で統合済、template/scripts/voicevox_narration.py) |
| Style-Bert-VITS2 | OSS local | self-host GPU / API 価格なし [一次情報未確認、Phase 6 着手時に Roku + Codex で再 consult] | 中(暫定、公開ベンチ未確認): voice model 管理が品質依存 | 高: model / GPU / rights 管理 | 別途 infra (現時点で採用済みでない、暫定候補) |
| ElevenLabs | 商用 API | Free $0/10k credits、Starter $6/30k credits、Creator $11/121k credits、Pro $99/600k credits。API 追加費なしで credits 消費 [S25][S26] | 高(暫定): 商用品質、voice cloning あり | 低: API key + credits | 拡張 narration mode 候補 |
| OpenAI TTS | 商用 API | gpt-4o-mini-tts: text input $0.60/1M tokens、audio output $12/1M tokens [S27] | 高(暫定): 13 voices、instructions で tone / speed 等制御 [S28] | 低: `/v1/audio/speech` | fallback / prototype 候補 |

## 5. リスク (memo only、Roku 判断領域、断定推奨せず並列提示)

### 5.1 法的

- AI アバター (SadTalker / HeyGen 等) は **deepfake 規制** に抵触する可能性 (国・州ごとに異なる、要法務相談)
- 生成画像 / 生成動画の **著作権 / 商用利用条件** は各 API ToS で確認必要
- 教材コンテンツの **本人許諾** (アバター話者として誰の顔を使うか)
- 現行法 (US TAKE IT DOWN Act / EU AI Act Article 50 / JP AI 事業者ガイドライン) の deepfake 規制詳細は §7 で整理済 [S31]-[S35]、中国は §7 範囲外 (要追加 consult)

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

## 7. 既知の罠 / 過去事例

- SadTalker と Wav2Lip は評価軸が違う。Wav2Lip は lip sync 数値が強く、LRS2 で LSE-D 6.386 / LSE-C 7.789 [S3]。SadTalker は head motion も生成するため、HDTF cross-ID では LSE-C 7.343 / LSE-D 7.709 と lip sync 単体では Wav2Lip より弱い [S1]。
- OSS active は star 数だけで判断しない。SadTalker は 13.8k stars だが直近 commit は 2023-10、open issues 617 [S2]。Wav2Lip は 12.9k stars で 2025-06 README 更新があるが、open issues 337 [S4]。SDXL repo は 27.1k stars だが latest release は 2023-07 [S12]。
- HeyGen / D-ID 固有の「本人許諾なし運用事故」は、本 consult 範囲では一次ソース未確認。近接事例として Yepic が記者の公開写真で無許諾 deepfake を作成した報道、Grok / xAI が非同意 sexual deepfake で規制当局調査を受けた報道は確認できたが、HeyGen / D-ID には帰属させない [S29][S30]。
- Kling / Runway の rate limit は非対称。Runway は tier ごとに concurrency / gens/day / monthly spend が明示され、超過時は THROTTLED または 429 [S20]。Kling は今回確認できた公開 API docs では固定 rate limit 未確認 [S17]。
- 商用 avatar API は「API call だけ」でも権利処理は軽くならない。HeyGen は custom Digital Twin / Proofreading API を Enterprise のみに制限 [S5]、D-ID は Trial/Lite watermark を synthetic transparency のためと説明 [S6]。
- US: TAKE IT DOWN Act は 2025-05-19 に Public Law No. 119-12 となり、nonconsensual intimate visual depictions / digital forgeries の公開禁止と notice-and-removal を規定 [S31][S32]。
- EU: AI Act Article 50 は synthetic audio/image/video/text output の machine-readable marking と、deep fake の人工生成・操作の disclosure を要求 [S33]。
- JP: AI 事業者ガイドライン第1.2版は公開済みだがガイドラインであり、EU Article 50 相当の deepfake disclosure 専用法までは本 consult では一次資料確認なし。顔画像・音声は個人情報保護法上の個人情報に該当し得るため、本人素材の扱いは別途確認が必要 [S34][S35]。

## 8. 次ステップ

- [x] Codex consult で §4 / §7 の [要 Codex 補完] を埋める (CODEX_FUTURE_FILLIN_20260505T094327.md → 794e3bc + a85bdb1 で integrate)
- [ ] Roku 復帰時に §6 オープンクエスチョン 7 件への判断を求める
- [ ] Phase 4 開始判断は §6 Q1 / Q3 / Q4 確定後
- [ ] §4 / §7 の二次レビュー (法務確認・実装着手前の price tier 再確認)

## 9. References

| ID | URL |
|---|---|
| [S1] | https://ar5iv.labs.arxiv.org/html/2211.12194 (SadTalker paper) |
| [S2] | https://github.com/OpenTalker/SadTalker |
| [S3] | https://ar5iv.labs.arxiv.org/html/2008.10010 (Wav2Lip paper) |
| [S4] | https://github.com/Rudrabha/Wav2Lip |
| [S5] | https://help.heygen.com/en/articles/10060327-new-heygen-api-plans |
| [S6] | https://www.d-id.com/pricing/studio/ |
| [S7] | https://www.g2.com/products/d-id/pricing |
| [S8] | https://www.synthesia.io/pricing |
| [S9] | https://www.hedra.com/pricing |
| [S10] | https://ai.google.dev/pricing |
| [S11] | https://ai.google.dev/gemini-api/docs/image-generation |
| [S12] | https://github.com/Stability-AI/generative-models |
| [S13] | https://docs.bfl.ai/quick_start/pricing |
| [S14] | https://help.bfl.ai/articles/9364115800-flux-models-overview |
| [S15] | https://github.com/black-forest-labs/flux |
| [S16] | https://ai.google.dev/gemini-api/docs/pricing?hl=ja |
| [S17] | https://klingapi.com/docs |
| [S18] | https://renderful.ai/blog/kling-api-pricing |
| [S19] | https://docs.dev.runwayml.com/guides/pricing/ |
| [S20] | https://docs.dev.runwayml.com/usage/tiers |
| [S21] | https://pika.art/pricing?tool=pika |
| [S22] | https://early-access.pika.art/api |
| [S23] | https://openai.com/api/pricing/ |
| [S24] | https://platform.openai.com/docs/guides/video-generation |
| [S25] | https://elevenlabs.io/pricing/ |
| [S26] | https://help.elevenlabs.io/hc/en-us/articles/28184926326033-How-much-does-it-cost-to-use-the-API |
| [S27] | https://developers.openai.com/api/docs/models/gpt-4o-mini-tts |
| [S28] | https://platform.openai.com/docs/guides/text-to-speech |
| [S29] | https://techcrunch.com/2023/10/11/yepic-ai-deepfakes-without-consent/ |
| [S30] | https://www.theguardian.com/technology/2026/feb/03/uk-privacy-watchdog-opens-inquiry-into-x-over-grok-ai-sexual-deepfakes |
| [S31] | https://www.congress.gov/bill/119th-congress/senate-bill/146/text |
| [S32] | https://www.law.cornell.edu/uscode/text/47/223a |
| [S33] | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50 |
| [S34] | https://www.meti.go.jp/shingikai/mono_info_service/ai_shakai_jisso/20260331_report.html |
| [S35] | https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/ |

---

**起草経緯メモ**: 当初 Codex に 1 prompt で全 8 章を起草依頼したが、30 min 進捗 0 で stuck (PID 73874 sleeping、tee buffer 0 byte)。Codex CLI 健全性は別途 tiny test (`OK alive`) で確認、複合 prompt の生成失敗が原因と推定。v0 は構造・verifiable 部分を Claude 起草、詳細 marker を smaller scope で再 consult する分担に切替 → §4/§7 fill-in は CODEX_FUTURE_FILLIN 20260505T094327 経由で 35 citations、一次情報中心、一部は第三者 (G2 / Renderful 等) または報道として明示 integrate (本 commit)。

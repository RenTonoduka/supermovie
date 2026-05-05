## 4. 技術選定マトリクス v0

評価凡例: 品質は「公開ベンチあり」は数値優先、「公開ベンチ未確認」は demo / API 仕様ベースの暫定評価。統合難度は API / file format / setup の観点。

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
| VOICEVOX | OSS local | 0 | 中: local TTS として既存採用済み | 低: 既存 script | 既存 |
| Style-Bert-VITS2 | OSS local | self-host GPU / API 価格なし | 中(暫定): voice model 管理が品質依存 | 高: model / GPU / rights 管理 | 別途 infra |
| ElevenLabs | 商用 API | Free $0/10k credits、Starter $6/30k credits、Creator $11/121k credits、Pro $99/600k credits。API 追加費なしで credits 消費 [S25][S26] | 高(暫定): 商用品質、voice cloning あり | 低: API key + credits | 拡張 narration mode 候補 |
| OpenAI TTS | 商用 API | gpt-4o-mini-tts: text input $0.60/1M tokens、audio output $12/1M tokens [S27] | 高(暫定): 13 voices、instructions で tone / speed 等制御 [S28] | 低: `/v1/audio/speech` | fallback / prototype 候補 |

## 7. 既知の罠 / 過去事例

- SadTalker と Wav2Lip は評価軸が違う。Wav2Lip は lip sync 数値が強く、LRS2 で LSE-D 6.386 / LSE-C 7.789 [S3]。SadTalker は head motion も生成するため、HDTF cross-ID では LSE-C 7.343 / LSE-D 7.709 と lip sync 単体では Wav2Lip より弱い [S1]。
- OSS active は star 数だけで判断しない。SadTalker は 13.8k stars だが直近 commit は 2023-10、open issues 617 [S2]。Wav2Lip は 12.9k stars で 2025-06 README 更新があるが、open issues 337 [S4]。SDXL repo は 27.1k stars だが latest release は 2023-07 [S12]。
- HeyGen / D-ID 固有の「本人許諾なし運用事故」は、この consult 範囲では一次ソース未確認。近接事例として Yepic が記者の公開写真で無許諾 deepfake を作成した報道、Grok / xAI が非同意 sexual deepfake で規制当局調査を受けた報道は確認済みだが、HeyGen / D-ID に帰属させない [S29][S30]。
- Kling / Runway の rate limit は非対称。Runway は tier ごとに concurrency / gens/day / monthly spend が明示され、超過時は THROTTLED または 429 [S20]。Kling は今回確認できた公開 API docs では固定 rate limit 未確認 [S17]。
- 商用 avatar API は「API call だけ」でも権利処理は軽くならない。HeyGen は custom Digital Twin / Proofreading API を Enterprise のみに制限 [S5]、D-ID は Trial/Lite watermark を synthetic transparency のためと説明 [S6]。
- US: TAKE IT DOWN Act は 2025-05-19 に Public Law No. 119-12 となり、nonconsensual intimate visual depictions / digital forgeries の公開禁止と notice-and-removal を規定 [S31][S32]。
- EU: AI Act Article 50 は synthetic audio/image/video/text output の machine-readable marking と、deep fake の人工生成・操作の disclosure を要求する [S33]。
- JP: AI 事業者ガイドライン第1.2版は公開済みだがガイドラインであり、EU Article 50 相当の deepfake disclosure 専用法までは本 consult では一次資料確認なし。顔画像・音声は個人情報保護法上の個人情報に該当し得るため、本人素材の扱いは別途確認が必要 [S34][S35]。

[S1]: https://ar5iv.labs.arxiv.org/html/2211.12194
[S2]: https://github.com/OpenTalker/SadTalker
[S3]: https://ar5iv.labs.arxiv.org/html/2008.10010
[S4]: https://github.com/Rudrabha/Wav2Lip
[S5]: https://help.heygen.com/en/articles/10060327-new-heygen-api-plans
[S6]: https://www.d-id.com/pricing/studio/
[S7]: https://www.g2.com/products/d-id/pricing
[S8]: https://www.synthesia.io/pricing
[S9]: https://www.hedra.com/pricing
[S10]: https://ai.google.dev/pricing
[S11]: https://ai.google.dev/gemini-api/docs/image-generation
[S12]: https://github.com/Stability-AI/generative-models
[S13]: https://docs.bfl.ai/quick_start/pricing
[S14]: https://help.bfl.ai/articles/9364115800-flux-models-overview
[S15]: https://github.com/black-forest-labs/flux
[S16]: https://ai.google.dev/gemini-api/docs/pricing?hl=ja
[S17]: https://klingapi.com/docs
[S18]: https://renderful.ai/blog/kling-api-pricing
[S19]: https://docs.dev.runwayml.com/guides/pricing/
[S20]: https://docs.dev.runwayml.com/usage/tiers
[S21]: https://pika.art/pricing?tool=pika
[S22]: https://early-access.pika.art/api
[S23]: https://openai.com/api/pricing/
[S24]: https://platform.openai.com/docs/guides/video-generation
[S25]: https://elevenlabs.io/pricing/
[S26]: https://help.elevenlabs.io/hc/en-us/articles/28184926326033-How-much-does-it-cost-to-use-the-API
[S27]: https://developers.openai.com/api/docs/models/gpt-4o-mini-tts
[S28]: https://platform.openai.com/docs/guides/text-to-speech
[S29]: https://techcrunch.com/2023/10/11/yepic-ai-deepfakes-without-consent/
[S30]: https://www.theguardian.com/technology/2026/feb/03/uk-privacy-watchdog-opens-inquiry-into-x-over-grok-ai-sexual-deepfakes
[S31]: https://www.congress.gov/bill/119th-congress/senate-bill/146/text
[S32]: https://www.law.cornell.edu/uscode/text/47/223a
[S33]: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50
[S34]: https://www.meti.go.jp/shingikai/mono_info_service/ai_shakai_jisso/20260331_report.html
[S35]: https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/

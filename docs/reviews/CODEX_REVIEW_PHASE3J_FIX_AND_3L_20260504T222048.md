Reading additional input from stdin...
2026-05-04T13:20:48.160268Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/rokumasuda/.claude/plugins/supermovie
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019df326-0420-77e3-b2da-db817b7f79bb
--------
user
SuperMovie Plugin の roku/phase3j-timeline branch 最新 4 commit を統合 review + Phase 3-L 推奨 consultation。

## Part A: Phase 3-J fix re-review

直近 4 commit (66e2aeb から e2a1a39 まで) の総合 verify:

`git log roku/phase3i-transcript-alignment..HEAD --oneline` で確認:
- 66e2aeb: Phase 3-J timeline.py 共通化 + 6 件 fix
- 398ea94: Phase 3-K core 1 integration smoke test
- 41b5ef2: Phase 3-K core 2 build_slide / build_telop transcript validation
- e2a1a39: Phase 3-J review 4 件 fix (P1×1 + P2×2 + P3×1)

verify checklist (前 review 4 件):
- P1 (VAD load synthesis 前移動): cleanup_stale_all 直後 + synthesis 前で
  project_load_cut_segments 呼出、VAD 破損で何も書かず exit 8 になるか
- P2 #1 (collect_chunks validate before strip): segment 非 dict / text 非 str
  で TranscriptSegmentError、AttributeError 経路ないか。segments 非 list
  ガードも有効か
- P2 #2 (build_telop validate_vad_schema): build_cut_segments_from_vad 内
  validate 経由、3 script (slide/telop/narration) で VAD 破損挙動統一
- P3 (SKILL.md exit 8): エラー table に exit 8 + exit 3 (TranscriptSegmentError)
  記載
- assert → RuntimeError raise (python -O safe): chunk_paths と chunk_meta
  長さ check が runtime で確実に発火

新規 regression / 罠:
- VAD synthesis 前移動で main() flow が cleanup → VAD 検証 → synthesis →
  concat → narrationData 書き出し に整理されたか
- collect_chunks の script_json path で plan が dict でない時の guard
- build_telop の build_cut_segments_from_vad が main() で 1 回だけ呼ばれるか
  (重複 validate_vad_schema 呼出で性能影響)
- test_timeline_integration.py に Phase 3-J P2 #1 regression test 追加 OK か

## Part B: Phase 3-L 推奨 consultation

Phase 3-A〜3-K 完了。残 Codex 残置 / 候補:

i. **timeline.validate_transcript_segments(require_timing=True|False)**
   (Codex Phase 3-J review Part B 設計概要で言及)
   - voicevox は optional、slide/telop は timing 必須を区別
   - 現状 build_slide / build_telop は validate するが require_timing 区別なし
   - 機械的、自走可

ii. **build_telop_data.py の cut helper 完全 timeline 統合** (Phase 3-J 残置)
   - find_cut_segment_for_ms / ms_to_playback_frame を timeline 経由に
   - find_cut_segment_for_ms は build_telop 固有なので局所関数で残置可
   - 中リスク (build_telop の cut 動作確認必要)

iii. **Studio hot-reload (watchStaticFile)** (Codex 過去 review でずっと残置)
   - mode.ts に watchStaticFile を組み込み Cmd+R 不要に
   - Remotion 公式 React hook 利用

iv. **any 警告ゼロ化** (Phase 3-E 残置)
   - eslint no-explicit-any error 化、telop-templates-30 由来 any 実型化

v. **Visual smoke を実 project で end-to-end 検証** (Phase 3-G 完成相当)
   - 実 main.mp4 + node_modules で 3 format × 2 frame の still を実行確認
   - 環境構築工数あり、Roku 判断 (main.mp4 fixture 用意)

vi. **integration_smoke を build_slide / build_telop / generate_slide_plan
    側にも展開** (Phase 3-K core 1 拡張)
   - 現状 voicevox 寄りの test、他 script の synthesis-side test 追加
   - 自走可

vii. **slide_plan.v2 + scene_plan 統合** (Roku ビジョン土台)
   - Anthropic API 課金 (Roku 判断)

聞きたいこと:
- どれを Phase 3-L に着手すべきか (推奨 1 + 次点 1 + 理由)
- 推奨 phase の設計概要
- 危険ポイント top3
- Codex review 重点項目

短く決定的に。
2026-05-04T13:20:48.463482Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
2026-05-04T13:20:48.465210Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
hook: SessionStart
hook: SessionStart
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
codex
確認します。事実主張を出す前に `verification-gate` を読み、ブランチ差分・該当ファイル・テストを実測してから review と Phase 3-L 推奨に絞ります。
hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "sed -n '1,220p' /Users/rokumasuda/.claude/skills/verification-gate/SKILL.md" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
---
name: verification-gate
description: 事実主張を含む応答を組み立てる前に必ず起動する Citation 強制 skill。Anthropic 公式 reduce hallucinations docs の「主張 → 引用検索 → 引用なし主張削除 + [] マーカー」フォーマットに従う。「分析して」「教えて」「まとめて」「報告して」「結論は」「現状は」「データは」「件数は」「いつ」「誰が」「どこで」「いくら」等の事実主張要求が来た時に即起動。Roku の「虚偽多すぎる」指摘 (2026-04-29) を起点とする構造的予防策の Layer 4。一次防衛は CLAUDE.md HARD RULE + UserPromptSubmit hook、本 skill は補強層
---

# Verification Gate

このskillはAnthropic公式 reduce hallucinations docs の「Citations フォーマット強制」パターンを skill 化したもの。

## 発動タイミング

ユーザーが事実主張・分析・報告・推論を求めた時:

- 「分析して」「教えて」「まとめて」「報告して」「調べて」
- 「結論は」「現状は」「データは」「状況は」
- 「件数は」「いつ」「誰が」「どこで」「いくら」「どのくらい」
- 「効果は」「結果は」「影響は」
- 過去状態・他者行動結果・外部システム状態への言及を含む応答

## Phase 1: 主張のリストアップ (内部処理)

ドラフト応答を組み立てる前に、含まれる主張を箇条書きで内部抽出する。

事実主張の定義:
- 数値 (件数・金額・%・時間・人数 等)
- 人物名・案件名・固有名詞
- 日時・予定・期日
- 他者の行動結果 (送信した・反映した・実行した 等)
- 外部システムの状態 (DB に N 件・ファイルに〜と書いてある 等)
- 状態評価 (動いている・壊れている・効果あった 等)

## Phase 2: 各主張に対する根拠取得

各主張について、必ず以下のいずれかで根拠を取得する:

| 主張のタイプ | 取得手段 | 引用フォーマット |
|---|---|---|
| ファイルの記述 | Read | `(file_path:line_number)` |
| Chatwork メッセージ | `mcp__chatwork__get_message_detail` | `(get_message_detail で取得, msg_id=...)` |
| Gmail スレッド | `mcp__claude_ai_Gmail__get_thread` | `(get_thread で取得, thread_id=...)` |
| Notion ページ | `mcp__hugruma-notion__API-retrieve-a-page` 等 | `(retrieve-a-page で取得)` |
| カレンダー予定 | `mcp__claude_ai_Google_Calendar__list_events` | `(list_events で取得)` |
| Web 公式ドキュメント | WebFetch | `(出典 URL)` |
| Git 状態 | Bash で `git log` `git show` `git diff` | `(Bash 実測)` |
| 過去のユーザー発言 | 会話履歴の原文引用 | `(Roku 発言: "原文")` |
| 上記いずれも不可 | 主張を削除 | `[未検証]` または `[不明]` マーカー |

## Phase 3: 引用なし主張の削除

根拠取得に失敗した主張は応答から削除し、削除位置に `[未検証]` または `[不明]` を残す。

例:
- Before: `この機能は3日で実装できます。`
- After: `この機能の実装期間は [未検証] です。`

## Phase 4: 残った主張のみで応答を再構成

引用付き主張のみで応答を組み立てる。引用がない主張は構造的に書けない。

## 限界

skill 自動起動忘れの可能性あり。

- 一次防衛 (確実): CLAUDE.md HARD RULE (Layer 1) + UserPromptSubmit hook 全ターン無条件注入 (Layer 2)
- 本 skill は補強層 (Layer 4)
- skill が起動しなくても Layer 1+2 が常時作動する設計

## 出典・関連

- Anthropic 公式 reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- 設計プラン: `~/.claude/plans/hallucination-prevention-overhaul.md` Layer 4
- 関連 feedback: `feedback_citation_enforcement.md` `feedback_structural_deception.md` `feedback_no_fake_knowledge_reference.md`

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'rg --files' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
CLAUDE.md
skills/supermovie-skill-creator/SKILL.md
skills/supermovie-subtitles/SKILL.md
skills/supermovie-init/SKILL.md
skills/supermovie-telop-creator/SKILL.md
skills/supermovie-cut/SKILL.md
skills/supermovie-transcribe/SKILL.md
skills/supermovie-se/SKILL.md
skills/supermovie-transcript-fix/SKILL.md
skills/supermovie-image-gen/SKILL.md
skills/supermovie-slides/SKILL.md
skills/supermovie-narration/SKILL.md
README.md
agents.disabled/skill-architect.md
agents.disabled/skill-auditor.md
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md
docs/reviews/CODEX_REVIEW_PHASE3J_AND_NEXT_20260504T221120.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md
docs/reviews/CODEX_REVIEW_PHASE3I_AND_NEXT_20260504T215824.md
docs/reviews/CODEX_REVIEW_PHASE3J_FIX_AND_3L_20260504T222048.md
sm-claude.sh
template/src/ネガティブテロップ/紫文字白背景.tsx
template/src/ネガティブテロップ/黒紫グラデ.tsx
template/src/ネガティブテロップ/残酷テロップ・紺.tsx
template/src/ネガティブテロップ/白文字紫シャドウ.tsx
template/src/ネガティブテロップ/黒文字白背景.tsx
template/src/SoundEffects/seData.ts
template/src/SoundEffects/SEPlayer.ts
template/src/SoundEffects/BGM.tsx
template/src/SoundEffects/SESequence.tsx
template/src/メインテロップ/白文字黒シャドウゴシック.tsx
template/src/メインテロップ/白青テロップ.tsx
template/src/メインテロップ/白文字黒シャドウ.tsx
template/src/メインテロップ/緑文字白背景.tsx
template/src/メインテロップ/白黒テロップ.tsx
template/src/メインテロップ/黒文字.tsx
template/src/メインテロップ/白文字黒シャドウ明朝体.tsx
template/src/メインテロップ/白文字黒背景.tsx
template/src/メインテロップ/白背景グラデ.tsx
template/src/メインテロップ/白青テロップver2.tsx
template/src/メインテロップ/青文字白背景.tsx
template/src/メインテロップ/白文字青ピンク背景グラデ.tsx
template/src/MainVideo.tsx
template/src/index.ts
template/src/Root.tsx
template/src/テロップテンプレート/telopTemplateRegistry.tsx
template/src/テロップテンプレート/telopTypes.ts
template/src/テロップテンプレート/Telop.tsx
template/src/テロップテンプレート/TelopPlayer.tsx
template/src/テロップテンプレート/telopData.ts
template/src/テロップテンプレート/telopStyles.ts
template/src/テロップテンプレート/index.tsx
template/src/Slides/Slide.tsx
template/src/Slides/slideData.ts
template/src/Slides/types.ts
template/src/Slides/SlideSequence.tsx
template/src/Slides/index.tsx
template/src/index.css
template/src/InsertImage/index.ts
template/src/InsertImage/insertImageData.ts
template/src/InsertImage/types.ts
template/src/InsertImage/InsertImage.tsx
template/src/InsertImage/ImageSequence.tsx
template/src/強調テロップ/白赤テロップver2.tsx
template/src/強調テロップ/オレンジグラデーション.tsx
template/src/強調テロップ/金グラデ・紺背景.tsx
template/src/強調テロップ/黄色文字黒シャドウ.tsx
template/src/強調テロップ/黄色シャドウ.tsx
template/src/強調テロップ/赤文字.tsx
template/src/強調テロップ/青文字金枠.tsx
template/src/強調テロップ/赤文字白背景.tsx
template/src/強調テロップ/白緑テロップ.tsx
template/src/強調テロップ/白赤テロップ.tsx
template/src/強調テロップ/黒文字黄色背景.tsx
template/src/強調テロップ/白文字赤シャドウ.tsx
template/src/強調テロップ/緑グラデ金シャドウ.tsx
template/src/Title/index.ts
template/src/Title/titleData.ts
template/src/Title/Title.tsx
template/src/Narration/NarrationAudio.tsx
template/src/Narration/index.ts
template/src/Narration/types.ts
template/src/Narration/narrationData.ts
template/src/Narration/mode.ts
template/src/videoConfig.ts
template/eslint.config.mjs
template/remotion.config.ts
template/tsconfig.json
LICENSE
template/package.json
template/scripts/timeline.py
template/scripts/test_timeline_integration.py
template/scripts/build_slide_data.py
template/scripts/budoux_split.mjs
template/scripts/preflight_video.py
template/scripts/visual_smoke.py
template/scripts/build_telop_data.py
template/scripts/voicevox_narration.py
template/scripts/generate_slide_plan.py
template/scripts/compare_telop_split.py

exec
/bin/zsh -lc 'git status --short --branch' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'git log roku/phase3i-transcript-alignment..HEAD --oneline' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-C75TjACr' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-2NMJqKqJ' (errno=Operation not permitted)
## roku/phase3j-timeline
?? docs/

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-UJHD2z6o' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-AUsOnUsh' (errno=Operation not permitted)
e2a1a39 fix(timeline): Codex Phase 3-J review 4 件 fix (P1×1 + P2×2 + P3×1)
41b5ef2 fix(timeline): transcript validation を build_slide / build_telop にも展開 (Phase 3-K core 2)
398ea94 test(timeline): pure python integration smoke test (Phase 3-K core 1)
66e2aeb feat(timeline): timeline.py 共通化 + Phase 3-I review 6 件 fix (Phase 3-J)

read-only のため実装はせず、git・ソース・テスト記述の検証に限定します。
  → ブランチ差分と対象ファイルを確認
  • Part A checklist をコードとテストで検証
  • Phase 3-L 候補を根拠付きで比較
  • 短い結論と review 重点項目を提示
codex
ブランチと commit 範囲は指定どおり見えています。次に timeline 共通化・3 script 側の呼び出し位置・regression test の実体を行番号付きで確認します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/scripts/timeline.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-J: timeline 共通 utility.
     3	
     4	Codex Phase 3-I review (CODEX_REVIEW_PHASE3I_AND_NEXT_20260504T215824) Part B
     5	推奨に従い、複数 script (voicevox_narration.py / build_slide_data.py /
     6	build_telop_data.py) で重複していた以下を 1 module に集約:
     7	
     8	- read_video_config_fps(): src/videoConfig.ts の FPS = N を一次 source 化
     9	- build_cut_segments_from_vad(): vad_result.json から cut timeline 構築
    10	- ms_to_playback_frame(): cut-aware ms → playback frame 変換
    11	- validate_vad_schema(): vad_result.json の部分破損 (KeyError / TypeError) を
    12	  早期 fail-fast で検出 (Codex Phase 3-I review P1 #2 反映)
    13	- validate_transcript_segment(): transcript_fixed.json segments[].start/end
    14	  の型 / 順序 validation (Codex Phase 3-I review P2 #3 反映)
    15	
    16	これにより slide / telop / narration が全て同一 ms→frame mapping を共有し、
    17	videoConfig.FPS を一次 source として Remotion render と同期する
    18	(出典: https://www.remotion.dev/docs/composition)。
    19	"""
    20	from __future__ import annotations
    21	
    22	import json
    23	import re
    24	from pathlib import Path
    25	
    26	DEFAULT_FPS = 30
    27	FPS_LINE_RE = re.compile(r"^export const FPS\s*=\s*(\d+)\s*;", re.MULTILINE)
    28	
    29	
    30	def read_video_config_fps(proj: Path, default: int = DEFAULT_FPS) -> int:
    31	    """`<proj>/src/videoConfig.ts` の `export const FPS = N;` を読む.
    32	
    33	    読めなければ default。`FPS <= 0` も default に倒す (P2 #4 反映)。
    34	    """
    35	    video_config = proj / "src" / "videoConfig.ts"
    36	    if not video_config.exists():
    37	        return default
    38	    try:
    39	        text = video_config.read_text(encoding="utf-8")
    40	    except OSError:
    41	        return default
    42	    m = FPS_LINE_RE.search(text)
    43	    if not m:
    44	        return default
    45	    try:
    46	        fps = int(m.group(1))
    47	    except ValueError:
    48	        return default
    49	    return fps if fps > 0 else default
    50	
    51	
    52	class VadSchemaError(ValueError):
    53	    """vad_result.json schema 不整合 (Codex P1 #2 反映、fail-fast 用)."""
    54	
    55	
    56	def validate_vad_schema(vad: object) -> dict:
    57	    """vad_result.json の最低限 schema を検査して dict を返す.
    58	
    59	    必須: dict に `speech_segments` key があり、list、各要素 dict で
    60	    `start` / `end` が int か float、start <= end。
    61	    破損は VadSchemaError。
    62	    """
    63	    if not isinstance(vad, dict):
    64	        raise VadSchemaError(f"vad must be dict, got {type(vad).__name__}")
    65	    segments = vad.get("speech_segments")
    66	    if not isinstance(segments, list):
    67	        raise VadSchemaError(
    68	            f"vad['speech_segments'] must be list, got {type(segments).__name__}"
    69	        )
    70	    for i, seg in enumerate(segments):
    71	        if not isinstance(seg, dict):
    72	            raise VadSchemaError(f"segment[{i}] must be dict, got {type(seg).__name__}")
    73	        for key in ("start", "end"):
    74	            v = seg.get(key)
    75	            if not isinstance(v, (int, float)):
    76	                raise VadSchemaError(
    77	                    f"segment[{i}].{key} must be int|float, got {type(v).__name__}"
    78	                )
    79	        if seg["start"] > seg["end"]:
    80	            raise VadSchemaError(
    81	                f"segment[{i}] start={seg['start']} > end={seg['end']}"
    82	            )
    83	    return vad
    84	
    85	
    86	def build_cut_segments_from_vad(vad: dict, fps: int) -> list[dict]:
    87	    """vad の speech_segments から cut 後 timeline mapping を構築.
    88	
    89	    呼び出し前に validate_vad_schema() で検査済みであることを前提とする。
    90	    fps は呼び出し側の videoConfig.FPS を渡す (Phase 3-J: hardcode 撤廃)。
    91	    """
    92	    out: list[dict] = []
    93	    cursor_ms = 0
    94	    for i, seg in enumerate(vad["speech_segments"]):
    95	        s_ms = seg["start"]
    96	        e_ms = seg["end"]
    97	        dur_ms = e_ms - s_ms
    98	        out.append(
    99	            {
   100	                "id": i + 1,
   101	                "originalStartMs": s_ms,
   102	                "originalEndMs": e_ms,
   103	                "playbackStart": round(cursor_ms / 1000 * fps),
   104	                "playbackEnd": round((cursor_ms + dur_ms) / 1000 * fps),
   105	            }
   106	        )
   107	        cursor_ms += dur_ms
   108	    return out
   109	
   110	
   111	def load_cut_segments(proj: Path, fps: int, fail_fast: bool = False) -> list[dict]:
   112	    """`<proj>/vad_result.json` から cut_segments を構築.
   113	
   114	    fail_fast=False (default): 不在 / I/O / schema エラーは [] にして黙過。
   115	    fail_fast=True: 部分破損も VadSchemaError / OSError で raise。
   116	
   117	    Codex Phase 3-I review P1 #2 反映: 黙過は legacy 経路へ流れて stale
   118	    narration を出す危険があるので、narration script では fail_fast=True 推奨。
   119	    """
   120	    vad_path = proj / "vad_result.json"
   121	    if not vad_path.exists():
   122	        return []
   123	    try:
   124	        with vad_path.open("r", encoding="utf-8") as f:
   125	            data = json.load(f)
   126	    except (OSError, json.JSONDecodeError) as e:
   127	        if fail_fast:
   128	            raise
   129	        return []
   130	    try:
   131	        validated = validate_vad_schema(data)
   132	    except VadSchemaError:
   133	        if fail_fast:
   134	            raise
   135	        return []
   136	    return build_cut_segments_from_vad(validated, fps)
   137	
   138	
   139	def ms_to_playback_frame(ms: int, fps: int, cut_segments: list[dict]) -> int | None:
   140	    """元動画の ms を playback frame に変換 (cut-aware).
   141	
   142	    cut_segments が空なら直接変換。ms が cut 範囲外 (cut で除外された箇所) は
   143	    None を返す (呼出側が累積 fallback or skip 判断)。
   144	    """
   145	    if not cut_segments:
   146	        return round(ms / 1000 * fps)
   147	    for cs in cut_segments:
   148	        if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
   149	            offset_ms = ms - cs["originalStartMs"]
   150	            return cs["playbackStart"] + round(offset_ms / 1000 * fps)
   151	    return None
   152	
   153	
   154	class TranscriptSegmentError(ValueError):
   155	    """transcript segment の型 / 順序 異常 (Codex P2 #3 反映)."""
   156	
   157	
   158	def validate_transcript_segment(
   159	    seg: object, idx: int = -1, require_timing: bool = False
   160	) -> dict:
   161	    """transcript_fixed.json の 1 segment の最低限検査.
   162	
   163	    必須: dict に `text` (str|None)、`start` / `end` が int|float|None。
   164	    両方 numeric なら start <= end。違反は TranscriptSegmentError。
   165	
   166	    require_timing=True: start / end の両方が int|float 必須 (None / 欠落 NG)。
   167	    build_slide_data / build_telop_data など timing 駆動の script で使う
   168	    (Codex Phase 3-J review Part B 設計概要 反映)。
   169	    """
   170	    label = f"segment[{idx}]" if idx >= 0 else "segment"
   171	    if not isinstance(seg, dict):
   172	        raise TranscriptSegmentError(f"{label} must be dict, got {type(seg).__name__}")
   173	    text = seg.get("text")
   174	    if text is not None and not isinstance(text, str):
   175	        raise TranscriptSegmentError(
   176	            f"{label}.text must be str|None, got {type(text).__name__}"
   177	        )
   178	    s = seg.get("start")
   179	    e = seg.get("end")
   180	    for k, v in (("start", s), ("end", e)):
   181	        if v is not None and not isinstance(v, (int, float)):
   182	            raise TranscriptSegmentError(
   183	                f"{label}.{k} must be int|float|None, got {type(v).__name__}"
   184	            )
   185	    if require_timing:
   186	        if not isinstance(s, (int, float)):
   187	            raise TranscriptSegmentError(
   188	                f"{label}.start required (int|float), got {type(s).__name__}"
   189	            )
   190	        if not isinstance(e, (int, float)):
   191	            raise TranscriptSegmentError(
   192	                f"{label}.end required (int|float), got {type(e).__name__}"
   193	            )
   194	    if isinstance(s, (int, float)) and isinstance(e, (int, float)) and s > e:
   195	        raise TranscriptSegmentError(f"{label} start={s} > end={e}")
   196	    return seg
   197	
   198	
   199	def validate_transcript_segments(
   200	    segments: object, require_timing: bool = False
   201	) -> list[dict]:
   202	    """segments[] 一括検証 (Codex Phase 3-J review Part B 推奨).
   203	
   204	    segments が list でない / 各要素が validate に通らない場合 raise。
   205	    require_timing=True で start/end 必須の strict mode (slide / telop 用)。
   206	    """
   207	    if not isinstance(segments, list):
   208	        raise TranscriptSegmentError(
   209	            f"segments must be list, got {type(segments).__name__}"
   210	        )
   211	    return [
   212	        validate_transcript_segment(seg, idx=i, require_timing=require_timing)
   213	        for i, seg in enumerate(segments)
   214	    ]

exec
/bin/zsh -lc 'rg -n "project_load_cut_segments|cleanup_stale_all|collect_chunks|validate_transcript|validate_vad_schema|build_cut_segments_from_vad|chunk_paths|chunk_meta|TranscriptSegmentError|exit 8|Exit 8|find_cut_segment|ms_to_playback_frame|watchStaticFile|no-explicit-any|any" template/scripts skills template/src template/eslint.config.mjs' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
template/eslint.config.mjs:6:// telop-templates-30.zip 由来の component が `any` を使っているため、
template/eslint.config.mjs:7:// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
template/eslint.config.mjs:12:      "@typescript-eslint/no-explicit-any": "warn",
template/scripts/voicevox_narration.py:16:- public/narration/chunk_meta.json も debug 用に出力
template/scripts/voicevox_narration.py:21:- 全 narration 出力 (narration.wav / narrationData.ts / chunk_meta.json) を
template/scripts/voicevox_narration.py:56:    TranscriptSegmentError,
template/scripts/voicevox_narration.py:58:    build_cut_segments_from_vad,
template/scripts/voicevox_narration.py:60:    ms_to_playback_frame,
template/scripts/voicevox_narration.py:62:    validate_transcript_segment,
template/scripts/voicevox_narration.py:72:CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
template/scripts/voicevox_narration.py:209:    """cleanup_stale_all() で legacy narration.wav の削除に失敗した時に raise."""
template/scripts/voicevox_narration.py:212:def cleanup_stale_all() -> None:
template/scripts/voicevox_narration.py:213:    """旧 chunk_*.wav / chunk_meta.json / narration.wav / narrationData.ts を全 reset.
template/scripts/voicevox_narration.py:220:    経路に入り、stale narration を再生してしまう)。chunks / chunk_meta は
template/scripts/voicevox_narration.py:233:                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
template/scripts/voicevox_narration.py:250:def project_load_cut_segments(fps: int) -> list[dict]:
template/scripts/voicevox_narration.py:265:    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く.
template/scripts/voicevox_narration.py:284:            mapped = ms_to_playback_frame(source_start_ms, fps, cut_segments)
template/scripts/voicevox_narration.py:389:def collect_chunks(args, transcript: dict) -> list[dict]:
template/scripts/voicevox_narration.py:393:    Phase 3-J: validate_transcript_segment で start > end / 型不正を検出して
template/scripts/voicevox_narration.py:394:    TranscriptSegmentError raise (Codex review P2 #3 反映、mlx-whisper の
template/scripts/voicevox_narration.py:407:    # TranscriptSegmentError として捕まらない経路があるため。
template/scripts/voicevox_narration.py:411:            raise TranscriptSegmentError(f"script-json must be dict, got {type(plan).__name__}")
template/scripts/voicevox_narration.py:414:            raise TranscriptSegmentError(
template/scripts/voicevox_narration.py:420:            validate_transcript_segment(
template/scripts/voicevox_narration.py:446:        raise TranscriptSegmentError(
template/scripts/voicevox_narration.py:452:        validate_transcript_segment(s, idx=i)
template/scripts/voicevox_narration.py:516:        chunks = collect_chunks(args, transcript)
template/scripts/voicevox_narration.py:517:    except TranscriptSegmentError as e:
template/scripts/voicevox_narration.py:532:    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
template/scripts/voicevox_narration.py:534:        cleanup_stale_all()
template/scripts/voicevox_narration.py:545:        cut_segments = project_load_cut_segments(fps)
template/scripts/voicevox_narration.py:551:        # cleanup_stale_all() 直後で何も書いていない、追加 rollback 不要
template/scripts/voicevox_narration.py:556:    chunk_paths: list[Path] = []
template/scripts/voicevox_narration.py:557:    chunk_meta: list[tuple[str, int | None, int | None]] = []  # (text, sourceStartMs, sourceEndMs)
template/scripts/voicevox_narration.py:567:        chunk_paths.append(p)
template/scripts/voicevox_narration.py:568:        chunk_meta.append((text, ch.get("sourceStartMs"), ch.get("sourceEndMs")))
template/scripts/voicevox_narration.py:571:    if not chunk_paths:
template/scripts/voicevox_narration.py:574:    if not args.allow_partial and len(chunk_paths) < len(chunks):
template/scripts/voicevox_narration.py:576:            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
template/scripts/voicevox_narration.py:581:        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
template/scripts/voicevox_narration.py:582:        for p in chunk_paths:
template/scripts/voicevox_narration.py:591:        concat_wavs_atomic(chunk_paths, out_path)
template/scripts/voicevox_narration.py:594:        for p in chunk_paths:
template/scripts/voicevox_narration.py:601:    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
template/scripts/voicevox_narration.py:606:    # Codex Phase 3-I review P3 #6 反映: chunk_paths と chunk_meta の長さ ガード
template/scripts/voicevox_narration.py:609:    if len(chunk_paths) != len(chunk_meta):
template/scripts/voicevox_narration.py:611:            f"chunk_paths ({len(chunk_paths)}) と chunk_meta ({len(chunk_meta)}) の長さズレ"
template/scripts/voicevox_narration.py:615:        for path, (text, source_start, source_end) in zip(chunk_paths, chunk_meta)
template/scripts/voicevox_narration.py:623:        for p in chunk_paths:
template/scripts/voicevox_narration.py:643:        "chunks": len(chunk_paths),
template/scripts/voicevox_narration.py:652:        "chunk_meta_json": str(meta_path),
template/scripts/build_telop_data.py:34:    TranscriptSegmentError,
template/scripts/build_telop_data.py:37:    validate_transcript_segment,
template/scripts/build_telop_data.py:38:    validate_vad_schema,
template/scripts/build_telop_data.py:241:def build_cut_segments_from_vad(vad):
template/scripts/build_telop_data.py:245:    同じ validate_vad_schema を経由して、3 script で壊れた VAD の扱いを揃える。
template/scripts/build_telop_data.py:247:    validate_vad_schema(vad)
template/scripts/build_telop_data.py:266:def find_cut_segment_for_ms(ms, cut_segments):
template/scripts/build_telop_data.py:273:def ms_to_playback_frame(ms, cut_segments):
template/scripts/build_telop_data.py:274:    cs = find_cut_segment_for_ms(ms, cut_segments)
template/scripts/build_telop_data.py:292:    cut_segments = build_cut_segments_from_vad(vad)
template/scripts/build_telop_data.py:304:            validate_transcript_segment(seg, idx=i, require_timing=True)
template/scripts/build_telop_data.py:305:        except TranscriptSegmentError as e:
template/scripts/build_telop_data.py:363:            cs_start = find_cut_segment_for_ms(ms_start, cut_segments)
template/scripts/build_telop_data.py:364:            cs_end = find_cut_segment_for_ms(ms_end, cut_segments)
template/scripts/build_telop_data.py:369:            pb_start = ms_to_playback_frame(ms_start, cut_segments)
template/scripts/build_telop_data.py:370:            pb_end = ms_to_playback_frame(ms_end, cut_segments)
template/scripts/visual_smoke.py:250:    if any(f < 0 for f in frames):
template/scripts/build_slide_data.py:30:    TranscriptSegmentError,
template/scripts/build_slide_data.py:31:    build_cut_segments_from_vad as _bcs_raw,
template/scripts/build_slide_data.py:32:    ms_to_playback_frame as _msf_raw,
template/scripts/build_slide_data.py:34:    validate_transcript_segment,
template/scripts/build_slide_data.py:35:    validate_vad_schema,
template/scripts/build_slide_data.py:50:def build_cut_segments_from_vad(vad: dict | None) -> list[dict]:
template/scripts/build_slide_data.py:51:    """Phase 3-J: timeline.build_cut_segments_from_vad を FPS 注入 wrapper.
template/scripts/build_slide_data.py:58:    return _bcs_raw(validate_vad_schema(vad), FPS)
template/scripts/build_slide_data.py:61:def ms_to_playback_frame(ms: int, cut_segments: list[dict]) -> int | None:
template/scripts/build_slide_data.py:62:    """Phase 3-J: timeline.ms_to_playback_frame を FPS 注入 wrapper."""
template/scripts/build_slide_data.py:110:        pb_start = ms_to_playback_frame(first["start"], cut_segments)
template/scripts/build_slide_data.py:111:        pb_end = ms_to_playback_frame(last["end"], cut_segments)
template/scripts/build_slide_data.py:155:        pb_start = ms_to_playback_frame(seg["start"], cut_segments)
template/scripts/build_slide_data.py:156:        pb_end = ms_to_playback_frame(seg["end"], cut_segments)
template/scripts/build_slide_data.py:288:        pb_start = ms_to_playback_frame(ms_start, cut_segments)
template/scripts/build_slide_data.py:289:        pb_end = ms_to_playback_frame(ms_end, cut_segments)
template/scripts/build_slide_data.py:331:    # ms_to_playback_frame 呼出箇所 4 件すべてで start/end を使用するため)。
template/scripts/build_slide_data.py:334:            validate_transcript_segment(seg, idx=i, require_timing=True)
template/scripts/build_slide_data.py:335:        except TranscriptSegmentError as e:
template/scripts/build_slide_data.py:340:    cut_segments = build_cut_segments_from_vad(vad)
template/scripts/timeline.py:9:- build_cut_segments_from_vad(): vad_result.json から cut timeline 構築
template/scripts/timeline.py:10:- ms_to_playback_frame(): cut-aware ms → playback frame 変換
template/scripts/timeline.py:11:- validate_vad_schema(): vad_result.json の部分破損 (KeyError / TypeError) を
template/scripts/timeline.py:13:- validate_transcript_segment(): transcript_fixed.json segments[].start/end
template/scripts/timeline.py:56:def validate_vad_schema(vad: object) -> dict:
template/scripts/timeline.py:86:def build_cut_segments_from_vad(vad: dict, fps: int) -> list[dict]:
template/scripts/timeline.py:89:    呼び出し前に validate_vad_schema() で検査済みであることを前提とする。
template/scripts/timeline.py:131:        validated = validate_vad_schema(data)
template/scripts/timeline.py:136:    return build_cut_segments_from_vad(validated, fps)
template/scripts/timeline.py:139:def ms_to_playback_frame(ms: int, fps: int, cut_segments: list[dict]) -> int | None:
template/scripts/timeline.py:154:class TranscriptSegmentError(ValueError):
template/scripts/timeline.py:158:def validate_transcript_segment(
template/scripts/timeline.py:164:    両方 numeric なら start <= end。違反は TranscriptSegmentError。
template/scripts/timeline.py:172:        raise TranscriptSegmentError(f"{label} must be dict, got {type(seg).__name__}")
template/scripts/timeline.py:175:        raise TranscriptSegmentError(
template/scripts/timeline.py:182:            raise TranscriptSegmentError(
template/scripts/timeline.py:187:            raise TranscriptSegmentError(
template/scripts/timeline.py:191:            raise TranscriptSegmentError(
template/scripts/timeline.py:195:        raise TranscriptSegmentError(f"{label} start={s} > end={e}")
template/scripts/timeline.py:199:def validate_transcript_segments(
template/scripts/timeline.py:208:        raise TranscriptSegmentError(
template/scripts/timeline.py:212:        validate_transcript_segment(seg, idx=i, require_timing=require_timing)
template/scripts/test_timeline_integration.py:93:        lambda: timeline.validate_vad_schema("not dict"),
template/scripts/test_timeline_integration.py:99:        lambda: timeline.validate_vad_schema({"speech_segments": "wrong"}),
template/scripts/test_timeline_integration.py:105:        lambda: timeline.validate_vad_schema({"speech_segments": ["str"]}),
template/scripts/test_timeline_integration.py:111:        lambda: timeline.validate_vad_schema(
template/scripts/test_timeline_integration.py:119:        lambda: timeline.validate_vad_schema({"speech_segments": [{"start": 0}]}),
template/scripts/test_timeline_integration.py:125:        lambda: timeline.validate_vad_schema(
template/scripts/test_timeline_integration.py:132:    timeline.validate_vad_schema(
template/scripts/test_timeline_integration.py:137:def test_ms_to_playback_frame() -> None:
template/scripts/test_timeline_integration.py:139:    assert_eq(timeline.ms_to_playback_frame(0, 30, []), 0, "no-cut start")
template/scripts/test_timeline_integration.py:140:    assert_eq(timeline.ms_to_playback_frame(1000, 30, []), 30, "no-cut 1s")
template/scripts/test_timeline_integration.py:141:    assert_eq(timeline.ms_to_playback_frame(500, 30, []), 15, "no-cut 0.5s")
template/scripts/test_timeline_integration.py:148:    assert_eq(timeline.ms_to_playback_frame(200, 30, cut_segs), 6, "cut seg0 200ms")
template/scripts/test_timeline_integration.py:149:    assert_eq(timeline.ms_to_playback_frame(1500, 30, cut_segs), 15, "cut seg1 start")
template/scripts/test_timeline_integration.py:150:    assert_eq(timeline.ms_to_playback_frame(2000, 30, cut_segs), 30, "cut seg1 +500ms")
template/scripts/test_timeline_integration.py:152:    assert_eq(timeline.ms_to_playback_frame(800, 30, cut_segs), None, "cut gap excluded")
template/scripts/test_timeline_integration.py:173:    """validate_transcript_segment が壊れた transcript を検出する."""
template/scripts/test_timeline_integration.py:175:    timeline.validate_transcript_segment({"text": "hi"}, 0)
template/scripts/test_timeline_integration.py:177:    timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
template/scripts/test_timeline_integration.py:180:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:183:        timeline.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:188:        lambda: timeline.validate_transcript_segment({"text": 123}, 0),
template/scripts/test_timeline_integration.py:189:        timeline.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:194:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:197:        timeline.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:202:def test_voicevox_collect_chunks_validation() -> None:
template/scripts/test_timeline_integration.py:203:    """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
template/scripts/test_timeline_integration.py:212:        lambda: vn.collect_chunks(Args(), bad),
template/scripts/test_timeline_integration.py:213:        vn.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:218:    out = vn.collect_chunks(Args(), good)
template/scripts/test_timeline_integration.py:224:    # 非 dict segment → TranscriptSegmentError
template/scripts/test_timeline_integration.py:226:        lambda: vn.collect_chunks(Args(), {"segments": ["not a dict"]}),
template/scripts/test_timeline_integration.py:227:        vn.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:230:    # segments 非 list → TranscriptSegmentError
template/scripts/test_timeline_integration.py:232:        lambda: vn.collect_chunks(Args(), {"segments": "wrong"}),
template/scripts/test_timeline_integration.py:233:        vn.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:236:    # text 非 str (int) → TranscriptSegmentError
template/scripts/test_timeline_integration.py:238:        lambda: vn.collect_chunks(Args(), {"segments": [{"text": 123}]}),
template/scripts/test_timeline_integration.py:239:        vn.TranscriptSegmentError,
template/scripts/test_timeline_integration.py:244:        vn.collect_chunks(Args(), {"segments": [{"text": None, "start": 0, "end": 100}]}),
template/scripts/test_timeline_integration.py:259:        vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
template/scripts/test_timeline_integration.py:288:        test_ms_to_playback_frame,
template/scripts/test_timeline_integration.py:291:        test_voicevox_collect_chunks_validation,
skills/supermovie-narration/SKILL.md:66:- `public/narration/chunk_meta.json` に fps + total_frames + cut_aware +
skills/supermovie-narration/SKILL.md:76:  `ms_to_playback_frame` と同型関数を内蔵)
skills/supermovie-narration/SKILL.md:79:  (chunk_meta.json の `overlaps[]` にも記録、render では `<Sequence>` 重複で
skills/supermovie-narration/SKILL.md:141:- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
skills/supermovie-narration/SKILL.md:156:| transcript validation 失敗 (TranscriptSegmentError) | exit 3 (start>end / 型不正 / 非 dict、collect_chunks で early raise、Codex Phase 3-I review P2 #3 反映) |
skills/supermovie-narration/SKILL.md:157:| vad_result.json 部分破損 (VadSchemaError / OSError / JSONDecodeError) | exit 8 (synthesis 前に fail-fast、stale legacy が legacy mode へ流れる事故防止、Codex Phase 3-I review P1 #2 + Phase 3-J review P1 反映で synthesis 前に validation 移動済) |
skills/supermovie-narration/SKILL.md:166:    ├─ public/narration/chunk_meta.json (debug、fps + segments[])
template/src/テロップテンプレート/Telop.tsx:126:  config: any;
template/src/テロップテンプレート/Telop.tsx:127:  animation: any;
template/src/テロップテンプレート/Telop.tsx:131:  const charDelay = (animation as any).charDelay || 2;
template/src/テロップテンプレート/Telop.tsx:133:  const fillGradient = (font as any).fillGradient;
template/src/テロップテンプレート/Telop.tsx:249:  const slideDirection = (animation as any).slideDirection || 'up';
template/src/テロップテンプレート/Telop.tsx:320:    const fillGradient = (font as any).fillGradient;
template/src/テロップテンプレート/Telop.tsx:394:  const strokeGradient = (textStroke as any).gradient || { start: '#ffffff', end: '#ffffff' };
template/src/テロップテンプレート/Telop.tsx:395:  const fillGradient = (font as any).fillGradient;
template/src/テロップテンプレート/Telop.tsx:397:  const textOpacity = (font as any).opacity ?? 1;

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/scripts/build_slide_data.py' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'nl -ba template/scripts/build_telop_data.py' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'nl -ba template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie subtitles phase: transcript_fixed.json → telopData.ts (BudouX 分割版).
     3	
     4	Codex Phase 2b design (2026-05-04, CODEX_PHASE2B_BUDOUX) 推奨:
     5	  C' = BudouX first + optional LLM plan.
     6	
     7	設計差分 (Phase 1 build_telop_data.py との違い):
     8	  - 文字数比例で句読点・助詞境界を探す split_segment_text() を廃止
     9	  - 代わりに BudouX (scripts/budoux_split.mjs) で意味単位の phrases を取得
    10	  - phrases を「max_chars 以内になる範囲で連結」しながら 1 telop 化
    11	  - 単語途中切れ・1字単独 telop が発生しにくい
    12	
    13	Usage:
    14	    python3 scripts/build_telop_data.py [--baseline]
    15	
    16	  --baseline を付けると BudouX 不使用の旧ロジックで生成する (KPI 比較用).
    17	
    18	入力: transcript_fixed.json + vad_result.json + (optional) typo_dict.json
    19	出力: src/テロップテンプレート/telopData.ts
    20	"""
    21	from __future__ import annotations
    22	
    23	import argparse
    24	import json
    25	import re
    26	import subprocess
    27	import tempfile
    28	from pathlib import Path
    29	
    30	PROJ = Path(__file__).resolve().parent.parent
    31	import sys as _sys
    32	_sys.path.insert(0, str(Path(__file__).resolve().parent))
    33	from timeline import (  # noqa: E402
    34	    TranscriptSegmentError,
    35	    VadSchemaError,
    36	    read_video_config_fps,
    37	    validate_transcript_segment,
    38	    validate_vad_schema,
    39	)
    40	
    41	FPS = read_video_config_fps(PROJ)  # Phase 3-J: timeline 共通化、videoConfig.FPS と同期
    42	# Phase 1 短尺 (short) format 既定値、後段で project-config.json から読むよう拡張可能
    43	MAX_CHARS = 24
    44	MAX_CHARS_PER_LINE = 12
    45	LINE_BREAK_THRESHOLD = 10
    46	MIN_DURATION_FRAMES = round(1.5 * FPS)
    47	MAX_DURATION_FRAMES = round(5.0 * FPS)
    48	
    49	
    50	# ---------------- BudouX phrase 連結 (新ロジック) ----------------
    51	def split_segment_text_budoux(seg_text: str, phrases: list[str], max_chars: int = MAX_CHARS) -> tuple[list[str], list[list[str]]]:
    52	    """BudouX phrases を max_chars 以内で連結して telop 列にする。
    53	    1 phrase が max_chars を超える場合のみ強制分割する。
    54	    返り値: (parts: 各 telop の文字列, parts_phrases: 各 telop に含まれる phrase 列)"""
    55	    parts: list[str] = []
    56	    parts_phrases: list[list[str]] = []
    57	    buf = ""
    58	    buf_phrases: list[str] = []
    59	    for p in phrases:
    60	        if not p:
    61	            continue
    62	        if len(p) > max_chars:
    63	            if buf:
    64	                parts.append(buf)
    65	                parts_phrases.append(buf_phrases)
    66	                buf = ""
    67	                buf_phrases = []
    68	            for i in range(0, len(p), max_chars):
    69	                chunk = p[i:i + max_chars]
    70	                parts.append(chunk)
    71	                parts_phrases.append([chunk])
    72	            continue
    73	        if len(buf) + len(p) <= max_chars:
    74	            buf += p
    75	            buf_phrases.append(p)
    76	        else:
    77	            parts.append(buf)
    78	            parts_phrases.append(buf_phrases)
    79	            buf = p
    80	            buf_phrases = [p]
    81	    if buf:
    82	        parts.append(buf)
    83	        parts_phrases.append(buf_phrases)
    84	    return parts, parts_phrases
    85	
    86	
    87	# ---------------- Phase 1 旧ロジック (baseline 比較用) ----------------
    88	def split_segment_text_legacy(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    89	    if len(text) <= max_chars:
    90	        return [text]
    91	    split_priority = ["。", "！", "？", "、", "ので", "けど", "から", "って", "ように", "として"]
    92	    parts = [text]
    93	    while True:
    94	        new_parts = []
    95	        changed = False
    96	        for p in parts:
    97	            if len(p) <= max_chars:
    98	                new_parts.append(p)
    99	                continue
   100	            best = None
   101	            for kw in split_priority:
   102	                for m in re.finditer(re.escape(kw), p):
   103	                    end = m.end()
   104	                    if end == 0 or end >= len(p):
   105	                        continue
   106	                    if end <= max_chars:
   107	                        if best is None or end > best:
   108	                            best = end
   109	            if best is None:
   110	                best = max_chars
   111	            new_parts.append(p[:best])
   112	            new_parts.append(p[best:])
   113	            changed = True
   114	        parts = new_parts
   115	        if not changed:
   116	            break
   117	    return parts
   118	
   119	
   120	# ---------------- 改行 (phase 1 と同じ、preserve / ASCII word 保護) ----------------
   121	def _is_inside_preserve(text: str, i: int, preserve: list[str]) -> bool:
   122	    for p in preserve:
   123	        if not p:
   124	            continue
   125	        start = 0
   126	        while True:
   127	            idx = text.find(p, start)
   128	            if idx < 0:
   129	                break
   130	            end = idx + len(p)
   131	            if idx < i < end:
   132	                return True
   133	            start = idx + 1
   134	    return False
   135	
   136	
   137	def _is_inside_word(text: str, i: int) -> bool:
   138	    if i <= 0 or i >= len(text):
   139	        return False
   140	    prev_ch = text[i - 1]
   141	    cur_ch = text[i]
   142	    return (prev_ch.isascii() and prev_ch.isalnum()) and (cur_ch.isascii() and cur_ch.isalnum())
   143	
   144	
   145	def _candidate_score(text, i, target, breakpoints, particles_after):
   146	    score = 0
   147	    prev = text[i - 1]
   148	    if prev in breakpoints:
   149	        score += 100
   150	    for p in particles_after:
   151	        if text[max(0, i - len(p)):i] == p:
   152	            score += 50
   153	            break
   154	    score -= abs(i - target)
   155	    return score
   156	
   157	
   158	def _phrase_boundaries(phrases: list[str]) -> set[int]:
   159	    """phrases から累積文字数 = 切り位置候補集合を返す."""
   160	    out = set()
   161	    cum = 0
   162	    for p in phrases:
   163	        cum += len(p)
   164	        out.add(cum)
   165	    return out
   166	
   167	
   168	def insert_linebreak(text, max_per_line=MAX_CHARS_PER_LINE, threshold=LINE_BREAK_THRESHOLD,
   169	                    preserve=None, phrases=None):
   170	    """改行挿入。tier 優先順位:
   171	      tier 0 (phrase aware): phrase 境界のみ + max_per_line ±2 内に収まる位置
   172	      tier 1: phrase 境界 + max_per_line を超えても 2 行目が 3 字以上
   173	      tier 2: phrase 不問 + max_per_line 内
   174	      tier 3: 諦めて max_per_line 直後
   175	    `phrases` を渡すと BudouX 文節境界が最優先される (Codex Phase 2b)。
   176	    """
   177	    preserve = preserve or []
   178	    if len(text) <= threshold or "\n" in text:
   179	        return text
   180	    breakpoints = ["、", "。", "！", "？"]
   181	    particles_after = ["を", "に", "で", "が", "は", "と", "から", "けど", "ので", "って", "ような", "として"]
   182	    n = len(text)
   183	    target = n // 2
   184	    phrase_pos = _phrase_boundaries(phrases) if phrases else set()
   185	
   186	    def forbidden(i):
   187	        return _is_inside_preserve(text, i, preserve) or _is_inside_word(text, i)
   188	
   189	    # tier 0: phrase 境界 ∩ tier1 範囲 (両行 max_per_line 以内 + 各行 2 字以上)
   190	    tier0 = [i for i in phrase_pos
   191	             if 1 <= i < n and not forbidden(i)
   192	             and len(text[:i]) <= max_per_line and len(text[i:]) <= max_per_line
   193	             and len(text[i:]) >= 2]
   194	    # tier 1: phrase 境界 ∩ ゆるめ (max_per_line 超過許容、2 行目 3 字以上)
   195	    tier1 = [i for i in phrase_pos
   196	             if 1 <= i < n and not forbidden(i)
   197	             and len(text[i:]) >= 3]
   198	    # tier 2: phrase 不問 + max_per_line 内
   199	    tier2 = [i for i in range(1, n) if not forbidden(i)
   200	             and len(text[:i]) <= max_per_line and len(text[i:]) <= max_per_line]
   201	    # tier 3: phrase 不問 + 両行 2 字以上
   202	    tier3 = [i for i in range(1, n) if not forbidden(i)
   203	             and len(text[:i]) >= 2 and len(text[i:]) >= 2]
   204	
   205	    for tier in (tier0, tier1, tier2, tier3):
   206	        if tier:
   207	            candidates = tier
   208	            break
   209	    else:
   210	        return text[:max_per_line] + "\n" + text[max_per_line:]
   211	
   212	    best = max(candidates, key=lambda i: _candidate_score(text, i, target, breakpoints, particles_after))
   213	    return text[:best] + "\n" + text[best:]
   214	
   215	
   216	# ---------------- BudouX 呼び出し ----------------
   217	def call_budoux(seg_texts: list[str]) -> list[list[str]]:
   218	    """proj/scripts/budoux_split.mjs を呼んで各 segment の phrases を返す."""
   219	    proj = PROJ
   220	    payload = {"segments": [{"id": i, "text": t} for i, t in enumerate(seg_texts)]}
   221	    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fin:
   222	        json.dump(payload, fin, ensure_ascii=False)
   223	        fin_path = fin.name
   224	    fout_path = fin_path.replace(".json", "_out.json")
   225	    script = proj / "scripts" / "budoux_split.mjs"
   226	    if not script.exists():
   227	        raise FileNotFoundError(f"budoux_split.mjs not found at {script}")
   228	    res = subprocess.run(
   229	        ["node", str(script), "--in", fin_path, "--out", fout_path],
   230	        cwd=str(proj),
   231	        capture_output=True,
   232	        text=True,
   233	    )
   234	    if res.returncode != 0:
   235	        raise RuntimeError(f"budoux_split.mjs failed: {res.stderr}")
   236	    out = json.loads(Path(fout_path).read_text(encoding="utf-8"))
   237	    return [s.get("phrases", []) for s in out["segments"]]
   238	
   239	
   240	# ---------------- VAD / cut ----------------
   241	def build_cut_segments_from_vad(vad):
   242	    """vad の speech_segments から cut timeline 構築 (Phase 3-K: validate 経由).
   243	
   244	    Codex Phase 3-J review P2 #2 反映: build_slide_data / voicevox_narration と
   245	    同じ validate_vad_schema を経由して、3 script で壊れた VAD の扱いを揃える。
   246	    """
   247	    validate_vad_schema(vad)
   248	    speech = vad["speech_segments"]
   249	    out = []
   250	    cursor_ms = 0
   251	    for i, seg in enumerate(speech):
   252	        s_ms = seg["start"]
   253	        e_ms = seg["end"]
   254	        dur_ms = e_ms - s_ms
   255	        out.append({
   256	            "id": i + 1,
   257	            "originalStartMs": s_ms,
   258	            "originalEndMs": e_ms,
   259	            "playbackStart": round(cursor_ms / 1000 * FPS),
   260	            "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
   261	        })
   262	        cursor_ms += dur_ms
   263	    return out
   264	
   265	
   266	def find_cut_segment_for_ms(ms, cut_segments):
   267	    for cs in cut_segments:
   268	        if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
   269	            return cs
   270	    return None
   271	
   272	
   273	def ms_to_playback_frame(ms, cut_segments):
   274	    cs = find_cut_segment_for_ms(ms, cut_segments)
   275	    if not cs:
   276	        return None
   277	    offset_ms = ms - cs["originalStartMs"]
   278	    return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
   279	
   280	
   281	# ---------------- 本体 ----------------
   282	def main():
   283	    ap = argparse.ArgumentParser()
   284	    ap.add_argument("--baseline", action="store_true", help="BudouX を使わず Phase 1 旧ロジックで生成")
   285	    args = ap.parse_args()
   286	
   287	    transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
   288	    vad = json.loads((PROJ / "vad_result.json").read_text(encoding="utf-8"))
   289	    typo = (PROJ / "typo_dict.json")
   290	    typo_dict = json.loads(typo.read_text(encoding="utf-8")) if typo.exists() else {}
   291	    preserve = typo_dict.get("preserve", [])
   292	    cut_segments = build_cut_segments_from_vad(vad)
   293	    cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else 0
   294	
   295	    words = transcript["words"]
   296	    segments = transcript["segments"]
   297	
   298	    # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_telop でも transcript
   299	    # 壊れたデータを早期検出。
   300	    # Phase 3-L: require_timing=True で start/end 必須化 (telop は ms→frame
   301	    # 変換で start/end を必須使用するため)。
   302	    for i, seg in enumerate(segments):
   303	        try:
   304	            validate_transcript_segment(seg, idx=i, require_timing=True)
   305	        except TranscriptSegmentError as e:
   306	            raise SystemExit(f"transcript validation failed: {e}")
   307	
   308	    # 分割 phase: BudouX 呼出 (一括)
   309	    seg_parts: list[list[str]] = []
   310	    seg_parts_phrases: list[list[list[str]]] = []  # part 毎の phrase リスト (insert_linebreak で使用)
   311	    if args.baseline:
   312	        for s in segments:
   313	            parts = split_segment_text_legacy(s["text"], MAX_CHARS)
   314	            seg_parts.append(parts)
   315	            seg_parts_phrases.append([[] for _ in parts])  # baseline は phrase なし
   316	    else:
   317	        try:
   318	            phrases_list = call_budoux([s["text"] for s in segments])
   319	            for i, s in enumerate(segments):
   320	                parts, parts_phrases = split_segment_text_budoux(s["text"], phrases_list[i], MAX_CHARS)
   321	                seg_parts.append(parts)
   322	                seg_parts_phrases.append(parts_phrases)
   323	        except Exception as e:
   324	            print(f"WARN: BudouX 失敗 → legacy fallback: {e}")
   325	            for s in segments:
   326	                parts = split_segment_text_legacy(s["text"], MAX_CHARS)
   327	                seg_parts.append(parts)
   328	                seg_parts_phrases.append([[] for _ in parts])
   329	
   330	    telop_segments = []
   331	    weaknesses = []
   332	    telop_id = 1
   333	
   334	    for seg_idx, (seg, parts, parts_phrases) in enumerate(zip(segments, seg_parts, seg_parts_phrases)):
   335	        if not parts:
   336	            continue
   337	        # 1-2 字を直前にマージ (文末「す」等の単独 telop 抑制)、phrases も追従
   338	        merged: list[str] = []
   339	        merged_phrases: list[list[str]] = []
   340	        for p_idx, p in enumerate(parts):
   341	            ph = parts_phrases[p_idx] if p_idx < len(parts_phrases) else []
   342	            if merged and len(p) <= 2:
   343	                merged[-1] = merged[-1] + p
   344	                merged_phrases[-1] = (merged_phrases[-1] or []) + ph
   345	            else:
   346	                merged.append(p)
   347	                merged_phrases.append(ph)
   348	        parts = merged
   349	        parts_phrases = merged_phrases
   350	
   351	        seg_total_chars = sum(len(p) for p in parts)
   352	        cum_chars = 0
   353	        for p_idx, part_text in enumerate(parts):
   354	            part_phrases = parts_phrases[p_idx] if p_idx < len(parts_phrases) else []
   355	            part_chars = len(part_text)
   356	            ratio_start = cum_chars / max(seg_total_chars, 1)
   357	            ratio_end = (cum_chars + part_chars) / max(seg_total_chars, 1)
   358	            seg_dur_ms = seg["end"] - seg["start"]
   359	            ms_start = seg["start"] + round(seg_dur_ms * ratio_start)
   360	            ms_end = seg["start"] + round(seg_dur_ms * ratio_end)
   361	
   362	            # cut 境界またぎ防止
   363	            cs_start = find_cut_segment_for_ms(ms_start, cut_segments)
   364	            cs_end = find_cut_segment_for_ms(ms_end, cut_segments)
   365	            if cs_start and cs_end and cs_start is not cs_end:
   366	                ms_end = cs_start["originalEndMs"]
   367	                weaknesses.append({"type": "telop_cut_boundary_clamp", "telop_text": part_text})
   368	
   369	            pb_start = ms_to_playback_frame(ms_start, cut_segments)
   370	            pb_end = ms_to_playback_frame(ms_end, cut_segments)
   371	            if pb_start is None or pb_end is None:
   372	                fallback = next((cs for cs in cut_segments if ms_start <= cs["originalEndMs"]), None)
   373	                if fallback:
   374	                    pb_start = fallback["playbackStart"]
   375	                    pb_end = min(fallback["playbackEnd"], (pb_start or 0) + MAX_DURATION_FRAMES)
   376	                else:
   377	                    weaknesses.append({"type": "telop_outside_cut", "telop_text": part_text})
   378	                    cum_chars += part_chars
   379	                    continue
   380	
   381	            duration = pb_end - pb_start
   382	            if duration < MIN_DURATION_FRAMES:
   383	                pb_end = pb_start + MIN_DURATION_FRAMES
   384	            if duration > MAX_DURATION_FRAMES:
   385	                pb_end = pb_start + MAX_DURATION_FRAMES
   386	            if pb_end > cut_total_frames:
   387	                pb_end = cut_total_frames
   388	            if pb_start >= cut_total_frames:
   389	                weaknesses.append({"type": "telop_after_cut_total", "telop_text": part_text})
   390	                cum_chars += part_chars
   391	                continue
   392	            if telop_segments and pb_start < telop_segments[-1]["endFrame"]:
   393	                pb_start = telop_segments[-1]["endFrame"]
   394	                if pb_end <= pb_start:
   395	                    pb_end = min(pb_start + MIN_DURATION_FRAMES, cut_total_frames)
   396	                    if pb_end <= pb_start:
   397	                        weaknesses.append({"type": "telop_overlap_unresolvable"})
   398	                        cum_chars += part_chars
   399	                        continue
   400	
   401	            wrapped = insert_linebreak(part_text, preserve=preserve, phrases=part_phrases)
   402	            telop_segments.append({
   403	                "id": telop_id,
   404	                "startFrame": pb_start,
   405	                "endFrame": pb_end,
   406	                "text": wrapped,
   407	                "style": "normal",
   408	                "templateId": "WhiteBlueTeleopV2",
   409	                "template": 2,
   410	                "animation": "fadeOnly",
   411	            })
   412	            telop_id += 1
   413	            cum_chars += part_chars
   414	
   415	    ts_lines = [
   416	        "import type { TelopSegment } from './telopTypes';",
   417	        "import { FPS as CONFIG_FPS } from '../videoConfig';",
   418	        "import { CUT_TOTAL_FRAMES } from '../cutData';",
   419	        "",
   420	        "// 自動生成: scripts/build_telop_data.py" + (" (--baseline)" if args.baseline else " (BudouX)"),
   421	        "// transcript_fixed.json の segments を BudouX phrase 単位で分割し、",
   422	        "// cutData 経由で playback frame に変換した TelopSegment[]",
   423	        "",
   424	        "export const FPS = CONFIG_FPS;",
   425	        "export const TOTAL_FRAMES = CUT_TOTAL_FRAMES;",
   426	        "",
   427	        "export const telopData: TelopSegment[] = [",
   428	    ]
   429	    for t in telop_segments:
   430	        ts_lines.append(
   431	            f"  {{ id: {t['id']}, startFrame: {t['startFrame']}, endFrame: {t['endFrame']}, "
   432	            f"text: {json.dumps(t['text'], ensure_ascii=False)}, "
   433	            f"style: '{t['style']}', templateId: '{t['templateId']}', "
   434	            f"template: {t['template']}, animation: '{t['animation']}' }},"
   435	        )
   436	    ts_lines.append("];")
   437	    ts_lines.append("")
   438	
   439	    out_path = PROJ / "src" / "テロップテンプレート" / "telopData.ts"
   440	    out_path.write_text("\n".join(ts_lines), encoding="utf-8")
   441	
   442	    print(f"=== telopData.ts 生成 ({'baseline' if args.baseline else 'BudouX'}) ===")
   443	    print(f"path: {out_path}")
   444	    print(f"telop count: {len(telop_segments)}")
   445	    print(f"weaknesses: {len(weaknesses)}")
   446	    print()
   447	    for t in telop_segments:
   448	        text_oneline = t["text"].replace("\n", "↵")
   449	        print(f"  [{t['id']:2}] f{t['startFrame']:5}-{t['endFrame']:5} '{text_oneline}'")
   450	
   451	
   452	if __name__ == "__main__":
   453	    main()

 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
     3	
     4	Phase 3-D 設計起点 (Codex CODEX_PHASE3D_VOICEVOX, 2026-05-04):
     5	- engine 不在で skip (--require-engine 指定時のみ exit non-zero)
     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
     7	- 入力 override: --script narration_script.txt / --script-json narration_script.json
     8	- 出力: public/narration.wav (segments 個別 wav を結合、legacy fallback)
     9	- API: POST /audio_query → POST /synthesis (公式 https://github.com/VOICEVOX/voicevox_engine)
    10	
    11	Phase 3-H 拡張 (Codex CODEX_PHASE3H_NEXT, 2026-05-04):
    12	- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
    13	- 各 chunk の wave header から実 duration を測定
    14	- src/Narration/narrationData.ts を all-or-nothing で生成
    15	  (NarrationSegment[] = [{id, startFrame, durationInFrames, file, text}])
    16	- public/narration/chunk_meta.json も debug 用に出力
    17	- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
    18	- partial failure 時は narrationData.ts を空に reset + 部分 chunk 削除、二重音声防止
    19	
    20	Phase 3-H review fix (Codex CODEX_REVIEW_PHASE3H_20260504T213301, P1×2 + P2×4):
    21	- 全 narration 出力 (narration.wav / narrationData.ts / chunk_meta.json) を
    22	  tempfile + os.replace で atomic 書き換え (SIGINT/disk full 安全、P2 #3)
    23	- FPS は src/videoConfig.ts の `export const FPS = N;` を一次 source に
    24	  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
    25	- wave.Error / EOFError を catch して exit 6 で all-or-nothing rollback (P2 #6)
    26	- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
    27	
    28	Usage:
    29	    python3 scripts/voicevox_narration.py
    30	    python3 scripts/voicevox_narration.py --speaker 3
    31	    python3 scripts/voicevox_narration.py --script narration.txt
    32	    python3 scripts/voicevox_narration.py --list-speakers
    33	    python3 scripts/voicevox_narration.py --require-engine
    34	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は src/videoConfig.ts FPS)
    35	
    36	Engine 起動 (Roku ローカル):
    37	    https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
    38	    127.0.0.1:50021 で REST API が立つ。Docker 版もあり (公式 README 参照)。
    39	"""
    40	from __future__ import annotations
    41	
    42	import argparse
    43	import json
    44	import os
    45	import sys
    46	import urllib.error
    47	import urllib.parse
    48	import urllib.request
    49	import wave
    50	from pathlib import Path
    51	
    52	PROJ = Path(__file__).resolve().parent.parent
    53	sys.path.insert(0, str(Path(__file__).resolve().parent))
    54	from timeline import (  # noqa: E402
    55	    DEFAULT_FPS,
    56	    TranscriptSegmentError,
    57	    VadSchemaError,
    58	    build_cut_segments_from_vad,
    59	    load_cut_segments,
    60	    ms_to_playback_frame,
    61	    read_video_config_fps,
    62	    validate_transcript_segment,
    63	)
    64	
    65	ENGINE_BASE = "http://127.0.0.1:50021"
    66	DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
    67	TIMEOUT = 30
    68	
    69	NARRATION_DIR = PROJ / "public" / "narration"
    70	NARRATION_LEGACY_WAV = PROJ / "public" / "narration.wav"
    71	NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
    72	CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
    73	EMPTY_NARRATION_DATA = (
    74	    "import type { NarrationSegment } from './types';\n"
    75	    "\n"
    76	    "export const narrationData: NarrationSegment[] = [];\n"
    77	)
    78	
    79	
    80	def _tmp_path(path: Path) -> Path:
    81	    """`.{name}.{pid}.tmp` 形式の temp path を返す.
    82	
    83	    PID 付与で同一 project の同時実行による tmp 衝突を回避
    84	    (Codex Phase 3-H fix re-review 新規 P2 反映)。
    85	    """
    86	    return path.with_name(f".{path.name}.{os.getpid()}.tmp")
    87	
    88	
    89	def atomic_write_bytes(path: Path, data: bytes) -> None:
    90	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映).
    91	
    92	    write 中例外時は finally で tmp を unlink (Codex re-review 新規 P3 反映)。
    93	    """
    94	    path.parent.mkdir(parents=True, exist_ok=True)
    95	    tmp = _tmp_path(path)
    96	    try:
    97	        tmp.write_bytes(data)
    98	        os.replace(tmp, path)
    99	    except Exception:
   100	        if tmp.exists():
   101	            try:
   102	                tmp.unlink()
   103	            except OSError:
   104	                pass
   105	        raise
   106	
   107	
   108	def atomic_write_text(path: Path, content: str) -> None:
   109	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映).
   110	
   111	    write 中例外時は finally で tmp を unlink (Codex re-review 新規 P3 反映)。
   112	    """
   113	    path.parent.mkdir(parents=True, exist_ok=True)
   114	    tmp = _tmp_path(path)
   115	    try:
   116	        tmp.write_text(content, encoding="utf-8")
   117	        os.replace(tmp, path)
   118	    except Exception:
   119	        if tmp.exists():
   120	            try:
   121	                tmp.unlink()
   122	            except OSError:
   123	                pass
   124	        raise
   125	
   126	
   127	def load_json(p: Path):
   128	    return json.loads(p.read_text(encoding="utf-8"))
   129	
   130	
   131	def http_request(method: str, path: str, params: dict | None = None,
   132	                 body: dict | None = None) -> bytes:
   133	    url = ENGINE_BASE + path
   134	    if params:
   135	        url += "?" + urllib.parse.urlencode(params)
   136	    data = json.dumps(body).encode("utf-8") if body is not None else None
   137	    headers = {"Content-Type": "application/json"} if body is not None else {}
   138	    req = urllib.request.Request(url, data=data, headers=headers, method=method)
   139	    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
   140	        return resp.read()
   141	
   142	
   143	def check_engine() -> tuple[bool, str | None]:
   144	    try:
   145	        body = http_request("GET", "/version")
   146	        return True, body.decode("utf-8").strip().strip('"')
   147	    except (urllib.error.URLError, OSError, urllib.error.HTTPError) as e:
   148	        return False, str(e)
   149	
   150	
   151	def list_speakers() -> list[dict]:
   152	    body = http_request("GET", "/speakers")
   153	    return json.loads(body.decode("utf-8"))
   154	
   155	
   156	def synthesize(text: str, speaker: int) -> bytes:
   157	    """audio_query → synthesis の二段階で WAV bytes を返す."""
   158	    aq_body = http_request("POST", "/audio_query", params={"text": text, "speaker": speaker}, body={})
   159	    aq = json.loads(aq_body.decode("utf-8"))
   160	    wav_bytes = http_request("POST", "/synthesis", params={"speaker": speaker}, body=aq)
   161	    return wav_bytes
   162	
   163	
   164	def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
   165	    """同一 sample rate / channel の wav 列を時系列で結合し atomic に書く.
   166	
   167	    wave.Error は呼び出し側で catch して all-or-nothing rollback する
   168	    (Codex Phase 3-H review P2 #6 反映). write 中例外時は finally で tmp を
   169	    unlink して残骸を残さない (Codex re-review 新規 P3 反映)。
   170	    """
   171	    if not wavs:
   172	        return
   173	    out_path.parent.mkdir(parents=True, exist_ok=True)
   174	    tmp = _tmp_path(out_path)
   175	    try:
   176	        with wave.open(str(wavs[0]), "rb") as w0:
   177	            params = w0.getparams()
   178	            frames = [w0.readframes(w0.getnframes())]
   179	        for p in wavs[1:]:
   180	            with wave.open(str(p), "rb") as w:
   181	                if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (params.framerate, params.nchannels, params.sampwidth):
   182	                    print(f"WARN: {p.name} format mismatch、skip", file=sys.stderr)
   183	                    continue
   184	                frames.append(w.readframes(w.getnframes()))
   185	        with wave.open(str(tmp), "wb") as out:
   186	            out.setparams(params)
   187	            for f in frames:
   188	                out.writeframes(f)
   189	        os.replace(tmp, out_path)
   190	    except Exception:
   191	        if tmp.exists():
   192	            try:
   193	                tmp.unlink()
   194	            except OSError:
   195	                pass
   196	        raise
   197	
   198	
   199	def measure_duration_seconds(wav_path: Path) -> float:
   200	    """WAV header の (nframes / framerate) で正確な duration を返す.
   201	
   202	    wave.Error / EOFError は呼び出し側で catch (Codex P2 #6 反映)。
   203	    """
   204	    with wave.open(str(wav_path), "rb") as w:
   205	        return w.getnframes() / float(w.getframerate())
   206	
   207	
   208	class StaleCleanupError(RuntimeError):
   209	    """cleanup_stale_all() で legacy narration.wav の削除に失敗した時に raise."""
   210	
   211	
   212	def cleanup_stale_all() -> None:
   213	    """旧 chunk_*.wav / chunk_meta.json / narration.wav / narrationData.ts を全 reset.
   214	
   215	    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
   216	    legacy mode で stale narration が再生される事故を起こすため、必ず全削除する。
   217	
   218	    Codex re-review P1 #2 partial 反映: legacy wav の削除失敗は WARN ではなく
   219	    StaleCleanupError raise (削除失敗を黙過すると残置 → mode helper が legacy
   220	    経路に入り、stale narration を再生してしまう)。chunks / chunk_meta は
   221	    どうせ atomic で上書きされるため WARN 継続で OK。
   222	    """
   223	    if NARRATION_DIR.exists():
   224	        for p in NARRATION_DIR.glob("chunk_*.wav"):
   225	            try:
   226	                p.unlink()
   227	            except OSError as e:
   228	                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
   229	        if CHUNK_META_JSON.exists():
   230	            try:
   231	                CHUNK_META_JSON.unlink()
   232	            except OSError as e:
   233	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
   234	    if NARRATION_LEGACY_WAV.exists():
   235	        try:
   236	            NARRATION_LEGACY_WAV.unlink()
   237	        except OSError as e:
   238	            raise StaleCleanupError(
   239	                f"stale narration.wav 削除失敗、stale legacy 再生事故防止のため処理中断: {e}"
   240	            ) from e
   241	    reset_narration_data_ts()
   242	
   243	
   244	def reset_narration_data_ts() -> None:
   245	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
   246	    if NARRATION_DATA_TS.parent.exists():
   247	        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
   248	
   249	
   250	def project_load_cut_segments(fps: int) -> list[dict]:
   251	    """voicevox 側の load_cut_segments wrapper (PROJ + fail_fast 戦略を固定).
   252	
   253	    Codex Phase 3-I review P1 #2 反映: narration script では legacy 経路へ
   254	    流れて stale narration を出す危険があるので fail_fast=True (raise)。
   255	    呼び出し側で VadSchemaError / OSError / json.JSONDecodeError を catch する。
   256	    """
   257	    return load_cut_segments(PROJ, fps, fail_fast=True)
   258	
   259	
   260	def write_narration_data(
   261	    chunks: list[tuple[Path, str, int | None, int | None]],
   262	    fps: int,
   263	    cut_segments: list[dict],
   264	) -> tuple[list[dict], Path, Path]:
   265	    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く.
   266	
   267	    両方とも atomic 書換 (Codex P2 #3 反映)。wave.Error は呼び出し側で catch。
   268	    Phase 3-I: chunks tuple は (path, text, sourceStartMs, sourceEndMs)。
   269	    sourceStartMs があれば transcript timing alignment、なければ累積 fallback。
   270	    cut_segments があれば cut-aware mapping、cut で除外された ms は累積 fallback。
   271	    """
   272	    segments: list[dict] = []
   273	    cumulative_frame = 0
   274	    overlap_warns: list[str] = []
   275	    for i, (path, text, source_start_ms, source_end_ms) in enumerate(chunks):
   276	        duration_sec = measure_duration_seconds(path)
   277	        duration_frames = max(1, round(duration_sec * fps))
   278	        rel = path.relative_to(PROJ / "public").as_posix()
   279	
   280	        # startFrame: transcript timing > 累積 fallback
   281	        start_frame = cumulative_frame
   282	        timing_source = "cumulative"
   283	        if source_start_ms is not None:
   284	            mapped = ms_to_playback_frame(source_start_ms, fps, cut_segments)
   285	            if mapped is None:
   286	                print(
   287	                    f"WARN: chunk {i} sourceStartMs={source_start_ms}ms は cut 範囲外、"
   288	                    f"累積 frame={cumulative_frame} で fallback",
   289	                    file=sys.stderr,
   290	                )
   291	            else:
   292	                start_frame = mapped
   293	                timing_source = "transcript_aligned"
   294	
   295	        # overlap 検出 (前 chunk の終端 > 現 startFrame)
   296	        if segments:
   297	            prev = segments[-1]
   298	            prev_end = prev["startFrame"] + prev["durationInFrames"]
   299	            if prev_end > start_frame:
   300	                overlap_warns.append(
   301	                    f"chunk {i - 1}->{i}: prev end frame={prev_end} > start={start_frame} "
   302	                    f"({prev_end - start_frame} frames overlap)"
   303	                )
   304	
   305	        seg_dict: dict = {
   306	            "id": i,
   307	            "startFrame": start_frame,
   308	            "durationInFrames": duration_frames,
   309	            "file": rel,
   310	            "text": text[:100],  # debug 用、長文は切り詰め
   311	            "duration_sec": round(duration_sec, 3),
   312	            "timing_source": timing_source,
   313	        }
   314	        if source_start_ms is not None:
   315	            seg_dict["sourceStartMs"] = source_start_ms
   316	        if source_end_ms is not None:
   317	            seg_dict["sourceEndMs"] = source_end_ms
   318	        segments.append(seg_dict)
   319	        cumulative_frame = start_frame + duration_frames
   320	
   321	    if overlap_warns:
   322	        # Codex Phase 3-I review P2 #4 反映: 文言を「transcript bug ではなく
   323	        # TTS が transcript より長い signal」として明確化、対処は transcript
   324	        # 再分割 / chunk text 短縮 / TTS 早話速度 / 隣接 chunk の sourceStart 後ろ送り。
   325	        print(
   326	            f"WARN: {len(overlap_warns)} narration <Sequence> overlap(s) detected. "
   327	            f"これは transcript の bug ではなく、TTS 出力 wav が元 transcript の "
   328	            f"interval より長いか、隣接 chunk が transcript timing 上で接近しすぎ。"
   329	            f"render では二重再生になるので、対処: "
   330	            f"(1) transcript 再分割、(2) chunk text 短縮、(3) speaker 早話速度、"
   331	            f"(4) sourceStartMs を後ろ送り。",
   332	            file=sys.stderr,
   333	        )
   334	        for w in overlap_warns:
   335	            print(f"  - {w}", file=sys.stderr)
   336	
   337	    total_frames = max((s["startFrame"] + s["durationInFrames"] for s in segments), default=0)
   338	    atomic_write_text(
   339	        CHUNK_META_JSON,
   340	        json.dumps(
   341	            {
   342	                "fps": fps,
   343	                "total_frames": total_frames,
   344	                "cut_aware": bool(cut_segments),
   345	                "overlaps": overlap_warns,
   346	                "segments": segments,
   347	            },
   348	            ensure_ascii=False,
   349	            indent=2,
   350	        ),
   351	    )
   352	
   353	    ts_lines = [
   354	        "/**",
   355	        " * Phase 3-H: voicevox_narration.py が all-or-nothing + atomic で書換える narration timeline。",
   356	        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
   357	        " * 手動編集禁止 (script 再実行で上書きされる)。",
   358	        " */",
   359	        "import type { NarrationSegment } from './types';",
   360	        "",
   361	        "export const narrationData: NarrationSegment[] = [",
   362	    ]
   363	    for s in segments:
   364	        parts = [
   365	            f"id: {s['id']}",
   366	            f"startFrame: {s['startFrame']}",
   367	            f"durationInFrames: {s['durationInFrames']}",
   368	            f"file: {json.dumps(s['file'])}",
   369	            f"text: {json.dumps(s['text'], ensure_ascii=False)}",
   370	        ]
   371	        if "sourceStartMs" in s:
   372	            parts.append(f"sourceStartMs: {s['sourceStartMs']}")
   373	        if "sourceEndMs" in s:
   374	            parts.append(f"sourceEndMs: {s['sourceEndMs']}")
   375	        ts_lines.append("  { " + ", ".join(parts) + " },")
   376	    ts_lines.append("];")
   377	    ts_lines.append("")
   378	    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
   379	
   380	    return segments, NARRATION_DATA_TS, CHUNK_META_JSON
   381	
   382	
   383	def _resolve_path(path_str: str) -> Path:
   384	    """非 absolute path は PROJ 相対に解決 (skill 実行時の cwd 揺れを吸収)."""
   385	    p = Path(path_str)
   386	    return p if p.is_absolute() else PROJ / p
   387	
   388	
   389	def collect_chunks(args, transcript: dict) -> list[dict]:
   390	    """各 chunk を {text, sourceStartMs, sourceEndMs} で返す.
   391	
   392	    Phase 3-I: transcript_fixed.json の segments[].start/end を保持。
   393	    Phase 3-J: validate_transcript_segment で start > end / 型不正を検出して
   394	    TranscriptSegmentError raise (Codex review P2 #3 反映、mlx-whisper の
   395	    稀なバグや手編集ミスによる壊れた transcript を早期検出)。
   396	    --script は 1 行 1 chunk で timing なし、--script-json は startMs/endMs
   397	    optional で受け付ける。
   398	    """
   399	    if args.script:
   400	        text = _resolve_path(args.script).read_text(encoding="utf-8")
   401	        return [
   402	            {"text": line.strip(), "sourceStartMs": None, "sourceEndMs": None}
   403	            for line in text.splitlines() if line.strip()
   404	        ]
   405	    # Codex Phase 3-J review P2 #1 反映: validate を `.get(...).strip()` より
   406	    # 先に通す。segment が非 dict / text 非 str だと AttributeError で落ちて
   407	    # TranscriptSegmentError として捕まらない経路があるため。
   408	    if args.script_json:
   409	        plan = load_json(_resolve_path(args.script_json))
   410	        if not isinstance(plan, dict):
   411	            raise TranscriptSegmentError(f"script-json must be dict, got {type(plan).__name__}")
   412	        plan_segments = plan.get("segments", [])
   413	        if not isinstance(plan_segments, list):
   414	            raise TranscriptSegmentError(
   415	                f"script-json segments must be list, got {type(plan_segments).__name__}"
   416	            )
   417	        out: list[dict] = []
   418	        for i, s in enumerate(plan_segments):
   419	            # validate を最初に通す (segment が非 dict なら raise)
   420	            validate_transcript_segment(
   421	                # script-json schema は startMs/endMs だが、validate は start/end を見るので map
   422	                (
   423	                    {
   424	                        "text": s.get("text"),
   425	                        "start": s.get("startMs"),
   426	                        "end": s.get("endMs"),
   427	                    }
   428	                    if isinstance(s, dict)
   429	                    else s
   430	                ),
   431	                idx=i,
   432	            )
   433	            text = (s.get("text") or "").strip()
   434	            if not text:
   435	                continue
   436	            out.append(
   437	                {
   438	                    "text": text,
   439	                    "sourceStartMs": s.get("startMs"),
   440	                    "sourceEndMs": s.get("endMs"),
   441	                }
   442	            )
   443	        return out
   444	    transcript_segments = transcript.get("segments", []) if isinstance(transcript, dict) else []
   445	    if not isinstance(transcript_segments, list):
   446	        raise TranscriptSegmentError(
   447	            f"transcript segments must be list, got {type(transcript_segments).__name__}"
   448	        )
   449	    out_t: list[dict] = []
   450	    for i, s in enumerate(transcript_segments):
   451	        # validate を最初に通す
   452	        validate_transcript_segment(s, idx=i)
   453	        text = (s.get("text") or "").strip()
   454	        if not text:
   455	            continue
   456	        out_t.append(
   457	            {
   458	                "text": text,
   459	                "sourceStartMs": s.get("start"),
   460	                "sourceEndMs": s.get("end"),
   461	            }
   462	        )
   463	    return out_t
   464	
   465	
   466	def main():
   467	    ap = argparse.ArgumentParser()
   468	    ap.add_argument("--speaker", type=int, default=DEFAULT_SPEAKER,
   469	                    help=f"VOICEVOX speaker id (default {DEFAULT_SPEAKER}=ずんだもんノーマル)")
   470	    ap.add_argument("--script", help="custom plain-text narration (1 line = 1 chunk)")
   471	    ap.add_argument("--script-json", help="custom JSON {segments:[{text}]} narration")
   472	    ap.add_argument("--list-speakers", action="store_true")
   473	    ap.add_argument("--require-engine", action="store_true",
   474	                    help="engine 不在で exit 4 (default は skip exit 0)")
   475	    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
   476	    ap.add_argument(
   477	        "--fps",
   478	        type=int,
   479	        default=None,
   480	        help=f"narrationData.ts に書き込む frame 換算 fps "
   481	             f"(default: src/videoConfig.ts FPS、読めなければ {DEFAULT_FPS})",
   482	    )
   483	    ap.add_argument("--allow-partial", action="store_true",
   484	                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
   485	                         "(default は全 chunk 成功必須)")
   486	    args = ap.parse_args()
   487	
   488	    ok, info = check_engine()
   489	    if not ok:
   490	        msg = f"VOICEVOX engine unavailable at {ENGINE_BASE}: {info}"
   491	        if args.require_engine:
   492	            print(f"ERROR: {msg}", file=sys.stderr)
   493	            return 4
   494	        print(f"INFO: {msg} -> narration generation skipped")
   495	        print(
   496	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
   497	            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
   498	            "(Phase 3-F asset gate + Phase 3-H per-segment Sequence)"
   499	        )
   500	        return 0
   501	    print(f"VOICEVOX engine OK (version: {info})")
   502	
   503	    if args.list_speakers:
   504	        speakers = list_speakers()
   505	        for s in speakers:
   506	            for style in s.get("styles", []):
   507	                print(f"  [{style.get('id'):3}] {s.get('name')} / {style.get('name')}")
   508	        return 0
   509	
   510	    transcript_path = PROJ / "transcript_fixed.json"
   511	    if not transcript_path.exists() and not (args.script or args.script_json):
   512	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
   513	        return 3
   514	    transcript = load_json(transcript_path) if transcript_path.exists() else {}
   515	    try:
   516	        chunks = collect_chunks(args, transcript)
   517	    except TranscriptSegmentError as e:
   518	        # Codex Phase 3-I review P2 #3: 壊れた transcript で TTS を回さない
   519	        print(f"ERROR: transcript validation failed: {e}", file=sys.stderr)
   520	        return 3
   521	    if not chunks:
   522	        print("ERROR: no narration chunks", file=sys.stderr)
   523	        return 3
   524	
   525	    fps = args.fps if args.fps is not None else read_video_config_fps(PROJ)
   526	    if fps <= 0:
   527	        print(f"ERROR: invalid fps={fps} (--fps is positive integer required)", file=sys.stderr)
   528	        return 4
   529	    print(f"target fps: {fps}")
   530	
   531	    # Phase 3-H: stale narration を全 reset BEFORE synthesis
   532	    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
   533	    try:
   534	        cleanup_stale_all()
   535	    except StaleCleanupError as e:
   536	        print(f"ERROR: {e}", file=sys.stderr)
   537	        return 7
   538	    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
   539	
   540	    # Codex Phase 3-J review P1 反映: VAD validation を synthesis 前 (cleanup 直後)
   541	    # に移動。VAD 破損時に synthesize / concat / narrationData 全 skip し、
   542	    # cleanup 直後の clean 状態で exit (stale narration.wav が legacy 経路に流れる
   543	    # 余地を完全に消す)。
   544	    try:
   545	        cut_segments = project_load_cut_segments(fps)
   546	    except (VadSchemaError, OSError, json.JSONDecodeError) as e:
   547	        print(
   548	            f"ERROR: vad_result.json schema invalid or unreadable: {e}",
   549	            file=sys.stderr,
   550	        )
   551	        # cleanup_stale_all() 直後で何も書いていない、追加 rollback 不要
   552	        return 8
   553	    if cut_segments:
   554	        print(f"cut-aware mapping: {len(cut_segments)} cut segments loaded from vad_result.json")
   555	
   556	    chunk_paths: list[Path] = []
   557	    chunk_meta: list[tuple[str, int | None, int | None]] = []  # (text, sourceStartMs, sourceEndMs)
   558	    for i, ch in enumerate(chunks):
   559	        text = ch["text"]
   560	        try:
   561	            wav_bytes = synthesize(text, args.speaker)
   562	        except (urllib.error.HTTPError, urllib.error.URLError) as e:
   563	            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
   564	            continue
   565	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
   566	        atomic_write_bytes(p, wav_bytes)
   567	        chunk_paths.append(p)
   568	        chunk_meta.append((text, ch.get("sourceStartMs"), ch.get("sourceEndMs")))
   569	        print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
   570	
   571	    if not chunk_paths:
   572	        print("ERROR: no chunks succeeded", file=sys.stderr)
   573	        return 5
   574	    if not args.allow_partial and len(chunk_paths) < len(chunks):
   575	        print(
   576	            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
   577	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
   578	            file=sys.stderr,
   579	        )
   580	        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
   581	        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
   582	        for p in chunk_paths:
   583	            try:
   584	                p.unlink()
   585	            except OSError:
   586	                pass
   587	        return 6
   588	
   589	    out_path = _resolve_path(args.output)
   590	    try:
   591	        concat_wavs_atomic(chunk_paths, out_path)
   592	    except (wave.Error, EOFError) as e:
   593	        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
   594	        for p in chunk_paths:
   595	            try:
   596	                p.unlink()
   597	            except OSError:
   598	                pass
   599	        return 6
   600	    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
   601	    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
   602	
   603	    # Phase 3-H/I: chunk metadata + narrationData.ts (atomic、最後に書く)
   604	    # cut_segments は synthesis 前 (Codex Phase 3-J review P1) で取得済み
   605	
   606	    # Codex Phase 3-I review P3 #6 反映: chunk_paths と chunk_meta の長さ ガード
   607	    # python -O で assert は消えるため、runtime check + raise 化
   608	    # (Codex Phase 3-J review checklist 指摘)。
   609	    if len(chunk_paths) != len(chunk_meta):
   610	        raise RuntimeError(
   611	            f"chunk_paths ({len(chunk_paths)}) と chunk_meta ({len(chunk_meta)}) の長さズレ"
   612	        )
   613	    pairs = [
   614	        (path, text, source_start, source_end)
   615	        for path, (text, source_start, source_end) in zip(chunk_paths, chunk_meta)
   616	    ]
   617	    try:
   618	        segments, ts_path, meta_path = write_narration_data(pairs, fps, cut_segments)
   619	    except (wave.Error, EOFError) as e:
   620	        print(f"ERROR: WAV duration probe failed (wave.Error / EOFError): {e}", file=sys.stderr)
   621	        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
   622	        # so user は再実行 or --allow-partial で部分書き出し選択可
   623	        for p in chunk_paths:
   624	            try:
   625	                p.unlink()
   626	            except OSError:
   627	                pass
   628	        if out_path.exists():
   629	            try:
   630	                out_path.unlink()
   631	            except OSError:
   632	                pass
   633	        return 6
   634	    total_frames = max(
   635	        (s["startFrame"] + s["durationInFrames"] for s in segments), default=0
   636	    )
   637	    print(f"wrote: {ts_path} ({len(segments)} segments, total_frames={total_frames})")
   638	    print(f"wrote: {meta_path}")
   639	
   640	    summary = {
   641	        "speaker": args.speaker,
   642	        "fps": fps,
   643	        "chunks": len(chunk_paths),
   644	        "total_chunks": len(chunks),
   645	        "total_frames": total_frames,
   646	        "cut_aware": bool(cut_segments),
   647	        "transcript_aligned_count": sum(
   648	            1 for s in segments if s.get("timing_source") == "transcript_aligned"
   649	        ),
   650	        "narration_wav": str(out_path),
   651	        "narration_data_ts": str(ts_path),
   652	        "chunk_meta_json": str(meta_path),
   653	        "engine_version": info,
   654	    }
   655	    print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")
   656	    return 0
   657	
   658	
   659	if __name__ == "__main__":
   660	    sys.exit(main())

 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
     3	
     4	Codex Phase 3B design (2026-05-04, CODEX_PHASE3B_NEXT) 推奨: A 一択 + deterministic first.
     5	
     6	入力:
     7	    <PROJECT>/transcript_fixed.json  - segments[] / words[]
     8	    <PROJECT>/project-config.json    - format / tone
     9	    (任意) <PROJECT>/vad_result.json - cut segments の元データ (cut 後 frame 変換用)
    10	
    11	出力:
    12	    <PROJECT>/src/Slides/slideData.ts - SlideSegment[]
    13	
    14	Usage:
    15	    python3 scripts/build_slide_data.py [--mode topic|segment]
    16	
    17	  --mode topic    (default): 連続 segments をグループ化して 1 slide に
    18	  --mode segment           : 1 transcript segment = 1 slide (シンプル)
    19	"""
    20	from __future__ import annotations
    21	
    22	import argparse
    23	import json
    24	import sys
    25	from pathlib import Path
    26	
    27	PROJ = Path(__file__).resolve().parent.parent
    28	sys.path.insert(0, str(Path(__file__).resolve().parent))
    29	from timeline import (  # noqa: E402
    30	    TranscriptSegmentError,
    31	    build_cut_segments_from_vad as _bcs_raw,
    32	    ms_to_playback_frame as _msf_raw,
    33	    read_video_config_fps,
    34	    validate_transcript_segment,
    35	    validate_vad_schema,
    36	)
    37	
    38	FPS = read_video_config_fps(PROJ)  # Phase 3-J: timeline 共通化、videoConfig.FPS と同期
    39	SILENCE_THRESHOLD_MS = 1500  # 1.5 秒以上の無音で話題区切り
    40	TITLE_MAX_CHARS = {"youtube": 18, "short": 14, "square": 16}
    41	BULLET_MAX_CHARS = {"youtube": 24, "short": 18, "square": 20}
    42	MAX_BULLETS_PER_SLIDE = 5
    43	MAX_SEGMENTS_PER_SLIDE = 5  # silence 検出失敗時の機械 fallback
    44	
    45	
    46	def load_json(p: Path):
    47	    return json.loads(p.read_text(encoding="utf-8"))
    48	
    49	
    50	def build_cut_segments_from_vad(vad: dict | None) -> list[dict]:
    51	    """Phase 3-J: timeline.build_cut_segments_from_vad を FPS 注入 wrapper.
    52	
    53	    旧 inline 実装は timeline.py に集約した。validate を経由して schema 破損は
    54	    raise (build_slide_data は cut が壊れていれば slide も壊れるため fail-fast)。
    55	    """
    56	    if not vad:
    57	        return []
    58	    return _bcs_raw(validate_vad_schema(vad), FPS)
    59	
    60	
    61	def ms_to_playback_frame(ms: int, cut_segments: list[dict]) -> int | None:
    62	    """Phase 3-J: timeline.ms_to_playback_frame を FPS 注入 wrapper."""
    63	    return _msf_raw(ms, FPS, cut_segments)
    64	
    65	
    66	def truncate(text: str, max_chars: int) -> str:
    67	    text = text.strip()
    68	    if len(text) <= max_chars:
    69	        return text
    70	    return text[:max_chars - 1] + "…"
    71	
    72	
    73	def group_topics(segments: list[dict], threshold_ms: int = SILENCE_THRESHOLD_MS) -> list[list[dict]]:
    74	    """隣接 segments の間隔 >= threshold_ms で話題区切り."""
    75	    if not segments:
    76	        return []
    77	    groups: list[list[dict]] = [[segments[0]]]
    78	    for prev, cur in zip(segments, segments[1:]):
    79	        gap_ms = cur["start"] - prev["end"]
    80	        if gap_ms >= threshold_ms or len(groups[-1]) >= MAX_SEGMENTS_PER_SLIDE:
    81	            groups.append([cur])
    82	        else:
    83	            groups[-1].append(cur)
    84	    return groups
    85	
    86	
    87	def style_for_tone(tone: str) -> dict:
    88	    table = {
    89	        "プロフェッショナル": {"align": "center", "bg": "rgba(20, 26, 44, 0.92)", "emphasis_ratio": 0.2},
    90	        "エンタメ": {"align": "left", "bg": "#101a2c", "emphasis_ratio": 0.4},
    91	        "カジュアル": {"align": "left", "bg": "rgba(40, 30, 60, 0.9)", "emphasis_ratio": 0.3},
    92	        "教育的": {"align": "left", "bg": "#0f2540", "emphasis_ratio": 0.4},
    93	    }
    94	    return table.get(tone, table["プロフェッショナル"])
    95	
    96	
    97	def build_slides_topic_mode(segments: list[dict], cut_segments: list[dict],
    98	                            fmt: str, tone: str) -> list[dict]:
    99	    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
   100	    bullet_max = BULLET_MAX_CHARS.get(fmt, BULLET_MAX_CHARS["short"])
   101	    style = style_for_tone(tone)
   102	    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
   103	
   104	    slides: list[dict] = []
   105	    groups = group_topics(segments)
   106	    for group_idx, group in enumerate(groups):
   107	        first = group[0]
   108	        last = group[-1]
   109	
   110	        pb_start = ms_to_playback_frame(first["start"], cut_segments)
   111	        pb_end = ms_to_playback_frame(last["end"], cut_segments)
   112	        if pb_start is None or pb_end is None:
   113	            continue
   114	        if cut_total is not None:
   115	            pb_end = min(pb_end, cut_total)
   116	        if pb_end <= pb_start:
   117	            continue
   118	
   119	        title = truncate(first["text"], title_max)
   120	        subtitle = truncate(last["text"], title_max + 6) if len(group) > 1 and last is not first else None
   121	        if subtitle == title:
   122	            subtitle = None
   123	
   124	        bullets: list[dict] = []
   125	        bullets_source = group[1:-1] if len(group) >= 3 else group
   126	        for i, seg in enumerate(bullets_source[:MAX_BULLETS_PER_SLIDE]):
   127	            text = truncate(seg["text"], bullet_max)
   128	            emphasis = (i == 0 and style["emphasis_ratio"] >= 0.4) or (
   129	                style["emphasis_ratio"] >= 0.3 and i == len(bullets_source) // 2
   130	            )
   131	            bullets.append({"text": text, "emphasis": emphasis})
   132	
   133	        slides.append({
   134	            "id": group_idx + 1,
   135	            "startFrame": pb_start,
   136	            "endFrame": pb_end,
   137	            "title": title,
   138	            "subtitle": subtitle,
   139	            "bullets": bullets if bullets else None,
   140	            "align": style["align"],
   141	            "backgroundColor": style["bg"],
   142	            "videoLayer": "visible",
   143	        })
   144	    return slides
   145	
   146	
   147	def build_slides_segment_mode(segments: list[dict], cut_segments: list[dict],
   148	                              fmt: str, tone: str) -> list[dict]:
   149	    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
   150	    style = style_for_tone(tone)
   151	    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
   152	
   153	    slides: list[dict] = []
   154	    for i, seg in enumerate(segments):
   155	        pb_start = ms_to_playback_frame(seg["start"], cut_segments)
   156	        pb_end = ms_to_playback_frame(seg["end"], cut_segments)
   157	        if pb_start is None or pb_end is None:
   158	            continue
   159	        if cut_total is not None:
   160	            pb_end = min(pb_end, cut_total)
   161	        if pb_end <= pb_start:
   162	            continue
   163	        slides.append({
   164	            "id": i + 1,
   165	            "startFrame": pb_start,
   166	            "endFrame": pb_end,
   167	            "title": truncate(seg["text"], title_max),
   168	            "align": style["align"],
   169	            "backgroundColor": style["bg"],
   170	            "videoLayer": "visible",
   171	        })
   172	    return slides
   173	
   174	
   175	def render_slide_data_ts(slides: list[dict]) -> str:
   176	    lines = [
   177	        "import type { SlideSegment } from './types';",
   178	        "",
   179	        "// 自動生成: scripts/build_slide_data.py",
   180	        f"// {len(slides)} slides を transcript_fixed.json から生成",
   181	        "",
   182	        "export const slideData: SlideSegment[] = [",
   183	    ]
   184	    for s in slides:
   185	        parts = [
   186	            f"id: {s['id']}",
   187	            f"startFrame: {s['startFrame']}",
   188	            f"endFrame: {s['endFrame']}",
   189	            f"title: {json.dumps(s['title'], ensure_ascii=False)}",
   190	        ]
   191	        if s.get("subtitle"):
   192	            parts.append(f"subtitle: {json.dumps(s['subtitle'], ensure_ascii=False)}")
   193	        if s.get("bullets"):
   194	            bullets_ts = ", ".join(
   195	                "{ text: " + json.dumps(b["text"], ensure_ascii=False)
   196	                + (", emphasis: true" if b.get("emphasis") else "")
   197	                + " }"
   198	                for b in s["bullets"]
   199	            )
   200	            parts.append(f"bullets: [{bullets_ts}]")
   201	        if s.get("align"):
   202	            parts.append(f"align: '{s['align']}'")
   203	        if s.get("backgroundColor"):
   204	            parts.append(f"backgroundColor: {json.dumps(s['backgroundColor'], ensure_ascii=False)}")
   205	        if s.get("videoLayer"):
   206	            parts.append(f"videoLayer: '{s['videoLayer']}'")
   207	        lines.append("  { " + ", ".join(parts) + " },")
   208	    lines.append("];")
   209	    lines.append("")
   210	    return "\n".join(lines)
   211	
   212	
   213	PLAN_VERSION = "supermovie.slide_plan.v1"
   214	ALLOWED_ALIGN = ("center", "left")
   215	ALLOWED_VIDEO_LAYER = ("visible", "dimmed", "hidden")
   216	
   217	
   218	def validate_slide_plan(plan: dict, words: list[dict], cut_total_frames: int | None,
   219	                        fmt: str) -> list[str]:
   220	    """Codex Phase 3-C validate (Q4) を実装。invalid なら理由を返す (空 list = OK)."""
   221	    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
   222	    bullet_max = BULLET_MAX_CHARS.get(fmt, BULLET_MAX_CHARS["short"])
   223	    errors: list[str] = []
   224	    if not isinstance(plan, dict):
   225	        return ["plan is not a dict"]
   226	    if plan.get("version") != PLAN_VERSION:
   227	        errors.append(f"version mismatch (expect {PLAN_VERSION})")
   228	    slides = plan.get("slides")
   229	    if not isinstance(slides, list):
   230	        errors.append("slides is not a list")
   231	        return errors
   232	    n_words = len(words)
   233	    last_end_idx = -1
   234	    last_id = 0
   235	    for i, s in enumerate(slides):
   236	        if not isinstance(s, dict):
   237	            errors.append(f"slides[{i}] not a dict")
   238	            continue
   239	        sid = s.get("id")
   240	        if not isinstance(sid, int) or sid <= last_id:
   241	            errors.append(f"slides[{i}].id must be ascending int (got {sid})")
   242	        else:
   243	            last_id = sid
   244	        sw = s.get("startWordIndex")
   245	        ew = s.get("endWordIndex")
   246	        if not (isinstance(sw, int) and isinstance(ew, int)
   247	                and 0 <= sw <= ew < n_words):
   248	            errors.append(f"slides[{i}] startWordIndex/endWordIndex out of range (got {sw}/{ew}, words={n_words})")
   249	            continue
   250	        if sw <= last_end_idx:
   251	            errors.append(f"slides[{i}] word range overlaps previous (sw={sw} <= prev end {last_end_idx})")
   252	        last_end_idx = ew
   253	        title = s.get("title")
   254	        if not isinstance(title, str) or not title.strip():
   255	            errors.append(f"slides[{i}].title empty")
   256	        elif len(title) > title_max:
   257	            errors.append(f"slides[{i}].title too long ({len(title)} > {title_max})")
   258	        bullets = s.get("bullets") or []
   259	        if not isinstance(bullets, list) or len(bullets) > MAX_BULLETS_PER_SLIDE:
   260	            errors.append(f"slides[{i}].bullets exceeds {MAX_BULLETS_PER_SLIDE}")
   261	        else:
   262	            for j, b in enumerate(bullets):
   263	                bt = b.get("text") if isinstance(b, dict) else None
   264	                if not isinstance(bt, str) or not bt.strip():
   265	                    errors.append(f"slides[{i}].bullets[{j}] empty text")
   266	                elif len(bt) > bullet_max:
   267	                    errors.append(f"slides[{i}].bullets[{j}] too long ({len(bt)} > {bullet_max})")
   268	        align = s.get("align")
   269	        if align is not None and align not in ALLOWED_ALIGN:
   270	            errors.append(f"slides[{i}].align invalid ({align})")
   271	        video_layer = s.get("videoLayer")
   272	        if video_layer is not None and video_layer not in ALLOWED_VIDEO_LAYER:
   273	            errors.append(f"slides[{i}].videoLayer invalid ({video_layer})")
   274	    return errors
   275	
   276	
   277	def build_slides_from_plan(plan: dict, words: list[dict], cut_segments: list[dict],
   278	                           fmt: str, tone: str) -> list[dict]:
   279	    """validated plan を SlideSegment dict 列に変換 (frame は script 側で計算)."""
   280	    style = style_for_tone(tone)
   281	    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
   282	    slides: list[dict] = []
   283	    for s in plan["slides"]:
   284	        sw = s["startWordIndex"]
   285	        ew = s["endWordIndex"]
   286	        ms_start = words[sw].get("start", 0)
   287	        ms_end = words[ew].get("end", 0)
   288	        pb_start = ms_to_playback_frame(ms_start, cut_segments)
   289	        pb_end = ms_to_playback_frame(ms_end, cut_segments)
   290	        if pb_start is None or pb_end is None or pb_end <= pb_start:
   291	            continue
   292	        if cut_total is not None:
   293	            pb_end = min(pb_end, cut_total)
   294	        slides.append({
   295	            "id": s["id"],
   296	            "startFrame": pb_start,
   297	            "endFrame": pb_end,
   298	            "title": s["title"],
   299	            "subtitle": s.get("subtitle"),
   300	            "bullets": s.get("bullets") or None,
   301	            "align": s.get("align") or style["align"],
   302	            "backgroundColor": s.get("backgroundColor") or style["bg"],
   303	            "videoLayer": s.get("videoLayer") or "visible",
   304	        })
   305	    return slides
   306	
   307	
   308	def main():
   309	    ap = argparse.ArgumentParser()
   310	    ap.add_argument("--mode", choices=["topic", "segment"], default="topic")
   311	    ap.add_argument("--plan", help="optional slide_plan.json (LLM 生成)")
   312	    ap.add_argument("--strict-plan", action="store_true",
   313	                    help="--plan の validate 失敗時に exit 2 (default は warning + deterministic fallback)")
   314	    args = ap.parse_args()
   315	
   316	    transcript_path = PROJ / "transcript_fixed.json"
   317	    config_path = PROJ / "project-config.json"
   318	    if not transcript_path.exists() or not config_path.exists():
   319	        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
   320	
   321	    transcript = load_json(transcript_path)
   322	    config = load_json(config_path)
   323	    fmt = config.get("format", "short")
   324	    tone = config.get("tone", "プロフェッショナル")
   325	    segments = transcript.get("segments", [])
   326	    words = transcript.get("words", [])
   327	
   328	    # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_slide_data でも
   329	    # transcript の壊れたデータを早期検出 (start>end / 型不正)。
   330	    # Phase 3-L: require_timing=True で start/end 必須化 (slide は timing 駆動、
   331	    # ms_to_playback_frame 呼出箇所 4 件すべてで start/end を使用するため)。
   332	    for i, seg in enumerate(segments):
   333	        try:
   334	            validate_transcript_segment(seg, idx=i, require_timing=True)
   335	        except TranscriptSegmentError as e:
   336	            raise SystemExit(f"transcript validation failed: {e}")
   337	
   338	    vad_path = PROJ / "vad_result.json"
   339	    vad = load_json(vad_path) if vad_path.exists() else None
   340	    cut_segments = build_cut_segments_from_vad(vad)
   341	    cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else None
   342	
   343	    used_plan = False
   344	    if args.plan:
   345	        plan_path = Path(args.plan)
   346	        if not plan_path.exists():
   347	            msg = f"--plan path not found: {plan_path}"
   348	            if args.strict_plan:
   349	                raise SystemExit(msg)
   350	            print(f"WARN: {msg} → deterministic fallback")
   351	        else:
   352	            plan = load_json(plan_path)
   353	            errors = validate_slide_plan(plan, words, cut_total_frames, fmt)
   354	            if errors:
   355	                if args.strict_plan:
   356	                    print("ERROR: plan validation failed:")
   357	                    for e in errors:
   358	                        print(f"  - {e}")
   359	                    raise SystemExit(2)
   360	                print("WARN: plan validation failed, deterministic fallback:")
   361	                for e in errors:
   362	                    print(f"  - {e}")
   363	            else:
   364	                slides = build_slides_from_plan(plan, words, cut_segments, fmt, tone)
   365	                used_plan = True
   366	                print(f"=== plan accepted ({len(plan.get('slides', []))} slides) ===")
   367	
   368	    if not used_plan:
   369	        if args.mode == "topic":
   370	            slides = build_slides_topic_mode(segments, cut_segments, fmt, tone)
   371	        else:
   372	            slides = build_slides_segment_mode(segments, cut_segments, fmt, tone)
   373	
   374	    out_path = PROJ / "src" / "Slides" / "slideData.ts"
   375	    backup = PROJ / "src" / "Slides" / "slideData.backup.ts"
   376	    if out_path.exists() and not backup.exists():
   377	        backup.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")
   378	    ts = render_slide_data_ts(slides)
   379	    out_path.write_text(ts, encoding="utf-8")
   380	
   381	    mode_label = "plan" if used_plan else f"deterministic-{args.mode}"
   382	    print(f"=== slideData.ts 生成 (mode={mode_label}) ===")
   383	    print(f"path: {out_path}")
   384	    print(f"input segments: {len(segments)}")
   385	    print(f"output slides: {len(slides)}")
   386	    for s in slides:
   387	        bullets_count = len(s.get("bullets") or [])
   388	        print(f"  [{s['id']:2}] f{s['startFrame']:5}-{s['endFrame']:5} '{s['title']}' (bullets={bullets_count})")
   389	
   390	
   391	if __name__ == "__main__":
   392	    main()

exec
/bin/zsh -lc 'nl -ba template/scripts/test_timeline_integration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-K integration smoke test (pure python).
     3	
     4	template/scripts/timeline.py + 3 script (voicevox_narration / build_slide_data /
     5	build_telop_data) の連鎖が破損していないか、engine / node_modules 不要で
     6	unit test する。Phase 3-J で導入した timeline.py の前提を壊す変更があれば
     7	失敗する。
     8	
     9	Usage:
    10	    python3 scripts/test_timeline_integration.py
    11	
    12	Exit code:
    13	    0 = 全 assertion pass
    14	    1 = 1 件以上 fail (assertion error)、stderr に詳細
    15	"""
    16	from __future__ import annotations
    17	
    18	import json
    19	import struct
    20	import sys
    21	import tempfile
    22	import wave
    23	from pathlib import Path
    24	
    25	SCRIPTS = Path(__file__).resolve().parent
    26	sys.path.insert(0, str(SCRIPTS))
    27	
    28	import timeline  # noqa: E402
    29	
    30	
    31	def make_videoconfig_ts(fps: int) -> str:
    32	    return (
    33	        "export type VideoFormat = 'youtube' | 'short' | 'square';\n"
    34	        "export const FORMAT: VideoFormat = 'youtube';\n"
    35	        f"export const FPS = {fps};\n"
    36	        "export const SOURCE_DURATION_FRAMES = 1500;\n"
    37	        "export const VIDEO_FILE = 'main.mp4';\n"
    38	    )
    39	
    40	
    41	def write_synthetic_wav(path: Path, duration_sec: float, framerate: int = 22050) -> None:
    42	    path.parent.mkdir(parents=True, exist_ok=True)
    43	    with wave.open(str(path), "wb") as w:
    44	        w.setnchannels(1)
    45	        w.setsampwidth(2)
    46	        w.setframerate(framerate)
    47	        n_frames = int(framerate * duration_sec)
    48	        w.writeframes(struct.pack("<%dh" % n_frames, *[0] * n_frames))
    49	
    50	
    51	def assert_eq(actual, expected, msg: str) -> None:
    52	    if actual != expected:
    53	        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")
    54	
    55	
    56	def assert_raises(callable_, exc_type, msg: str):
    57	    try:
    58	        callable_()
    59	    except exc_type:
    60	        return
    61	    raise AssertionError(f"{msg}: expected {exc_type.__name__} but no exception raised")
    62	
    63	
    64	def test_fps_consistency() -> None:
    65	    """3 script が timeline.read_video_config_fps を経由して同じ FPS を返す."""
    66	    with tempfile.TemporaryDirectory() as tmp:
    67	        proj = Path(tmp)
    68	        (proj / "src").mkdir()
    69	        (proj / "src" / "videoConfig.ts").write_text(make_videoconfig_ts(60))
    70	
    71	        # timeline 直読
    72	        assert_eq(timeline.read_video_config_fps(proj), 60, "timeline FPS read")
    73	
    74	        # malformed 検出 (FPS 行なし)
    75	        (proj / "src" / "videoConfig.ts").write_text("// no fps line\n")
    76	        assert_eq(
    77	            timeline.read_video_config_fps(proj, default=42),
    78	            42,
    79	            "malformed FPS fallback",
    80	        )
    81	
    82	        # FPS=0 を default に倒す
    83	        (proj / "src" / "videoConfig.ts").write_text(
    84	            "export const FPS = 0;\n"
    85	        )
    86	        assert_eq(timeline.read_video_config_fps(proj), timeline.DEFAULT_FPS, "FPS=0 fallback")
    87	
    88	
    89	def test_vad_schema_validation() -> None:
    90	    """VadSchemaError が部分破損を全て検出する."""
    91	    # 非 dict
    92	    assert_raises(
    93	        lambda: timeline.validate_vad_schema("not dict"),
    94	        timeline.VadSchemaError,
    95	        "non-dict",
    96	    )
    97	    # speech_segments 非 list
    98	    assert_raises(
    99	        lambda: timeline.validate_vad_schema({"speech_segments": "wrong"}),
   100	        timeline.VadSchemaError,
   101	        "speech_segments non-list",
   102	    )
   103	    # segment 非 dict
   104	    assert_raises(
   105	        lambda: timeline.validate_vad_schema({"speech_segments": ["str"]}),
   106	        timeline.VadSchemaError,
   107	        "segment non-dict",
   108	    )
   109	    # start 型不正
   110	    assert_raises(
   111	        lambda: timeline.validate_vad_schema(
   112	            {"speech_segments": [{"start": "bad", "end": 100}]}
   113	        ),
   114	        timeline.VadSchemaError,
   115	        "start non-numeric",
   116	    )
   117	    # end 欠落
   118	    assert_raises(
   119	        lambda: timeline.validate_vad_schema({"speech_segments": [{"start": 0}]}),
   120	        timeline.VadSchemaError,
   121	        "end missing",
   122	    )
   123	    # start > end
   124	    assert_raises(
   125	        lambda: timeline.validate_vad_schema(
   126	            {"speech_segments": [{"start": 100, "end": 50}]}
   127	        ),
   128	        timeline.VadSchemaError,
   129	        "start > end",
   130	    )
   131	    # OK
   132	    timeline.validate_vad_schema(
   133	        {"speech_segments": [{"start": 0, "end": 1000}]}
   134	    )
   135	
   136	
   137	def test_ms_to_playback_frame() -> None:
   138	    # No cut: 直接 ms→frame
   139	    assert_eq(timeline.ms_to_playback_frame(0, 30, []), 0, "no-cut start")
   140	    assert_eq(timeline.ms_to_playback_frame(1000, 30, []), 30, "no-cut 1s")
   141	    assert_eq(timeline.ms_to_playback_frame(500, 30, []), 15, "no-cut 0.5s")
   142	
   143	    # With cut: gap removed
   144	    cut_segs = [
   145	        {"originalStartMs": 0, "originalEndMs": 500, "playbackStart": 0, "playbackEnd": 15},
   146	        {"originalStartMs": 1500, "originalEndMs": 3000, "playbackStart": 15, "playbackEnd": 60},
   147	    ]
   148	    assert_eq(timeline.ms_to_playback_frame(200, 30, cut_segs), 6, "cut seg0 200ms")
   149	    assert_eq(timeline.ms_to_playback_frame(1500, 30, cut_segs), 15, "cut seg1 start")
   150	    assert_eq(timeline.ms_to_playback_frame(2000, 30, cut_segs), 30, "cut seg1 +500ms")
   151	    # 800ms: gap (excluded)
   152	    assert_eq(timeline.ms_to_playback_frame(800, 30, cut_segs), None, "cut gap excluded")
   153	
   154	
   155	def test_load_cut_segments_fail_fast() -> None:
   156	    """fail_fast=True で部分破損を raise する."""
   157	    with tempfile.TemporaryDirectory() as tmp:
   158	        proj = Path(tmp)
   159	        (proj / "vad_result.json").write_text(
   160	            json.dumps({"speech_segments": [{"start": 100}]})  # end missing
   161	        )
   162	        # default fail_fast=False で []
   163	        assert_eq(timeline.load_cut_segments(proj, 30, fail_fast=False), [], "soft fail")
   164	        # fail_fast=True で raise
   165	        assert_raises(
   166	            lambda: timeline.load_cut_segments(proj, 30, fail_fast=True),
   167	            timeline.VadSchemaError,
   168	            "fail_fast raise",
   169	        )
   170	
   171	
   172	def test_transcript_segment_validation() -> None:
   173	    """validate_transcript_segment が壊れた transcript を検出する."""
   174	    # OK: timing なし (--script の chunk)
   175	    timeline.validate_transcript_segment({"text": "hi"}, 0)
   176	    # OK: 通常 transcript
   177	    timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
   178	    # NG: start > end
   179	    assert_raises(
   180	        lambda: timeline.validate_transcript_segment(
   181	            {"text": "hi", "start": 1000, "end": 500}, 0
   182	        ),
   183	        timeline.TranscriptSegmentError,
   184	        "transcript start>end",
   185	    )
   186	    # NG: text 非 str
   187	    assert_raises(
   188	        lambda: timeline.validate_transcript_segment({"text": 123}, 0),
   189	        timeline.TranscriptSegmentError,
   190	        "text non-str",
   191	    )
   192	    # NG: start 型不正
   193	    assert_raises(
   194	        lambda: timeline.validate_transcript_segment(
   195	            {"text": "hi", "start": "bad"}, 0
   196	        ),
   197	        timeline.TranscriptSegmentError,
   198	        "start non-numeric",
   199	    )
   200	
   201	
   202	def test_voicevox_collect_chunks_validation() -> None:
   203	    """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
   204	    import voicevox_narration as vn
   205	
   206	    class Args:
   207	        script = None
   208	        script_json = None
   209	
   210	    bad = {"segments": [{"text": "hi", "start": 100, "end": 50}]}
   211	    assert_raises(
   212	        lambda: vn.collect_chunks(Args(), bad),
   213	        vn.TranscriptSegmentError,
   214	        "voicevox start>end transcript",
   215	    )
   216	
   217	    good = {"segments": [{"text": "hi", "start": 0, "end": 1000}]}
   218	    out = vn.collect_chunks(Args(), good)
   219	    assert_eq(len(out), 1, "voicevox good transcript len")
   220	    assert_eq(out[0]["sourceStartMs"], 0, "voicevox sourceStartMs")
   221	    assert_eq(out[0]["sourceEndMs"], 1000, "voicevox sourceEndMs")
   222	
   223	    # Codex Phase 3-J review P2 #1 反映: validate を `.get(...).strip()` 前に通す
   224	    # 非 dict segment → TranscriptSegmentError
   225	    assert_raises(
   226	        lambda: vn.collect_chunks(Args(), {"segments": ["not a dict"]}),
   227	        vn.TranscriptSegmentError,
   228	        "voicevox non-dict segment",
   229	    )
   230	    # segments 非 list → TranscriptSegmentError
   231	    assert_raises(
   232	        lambda: vn.collect_chunks(Args(), {"segments": "wrong"}),
   233	        vn.TranscriptSegmentError,
   234	        "voicevox non-list segments",
   235	    )
   236	    # text 非 str (int) → TranscriptSegmentError
   237	    assert_raises(
   238	        lambda: vn.collect_chunks(Args(), {"segments": [{"text": 123}]}),
   239	        vn.TranscriptSegmentError,
   240	        "voicevox text non-str",
   241	    )
   242	    # text=None は filter (空文字列と同じ扱い、空 list 返す)
   243	    assert_eq(
   244	        vn.collect_chunks(Args(), {"segments": [{"text": None, "start": 0, "end": 100}]}),
   245	        [],
   246	        "voicevox text=None filtered",
   247	    )
   248	
   249	
   250	def test_voicevox_write_narration_data_alignment() -> None:
   251	    """transcript timing alignment が cut-aware で正しく動く end-to-end."""
   252	    import voicevox_narration as vn
   253	
   254	    with tempfile.TemporaryDirectory() as tmp:
   255	        proj = Path(tmp)
   256	        vn.PROJ = proj
   257	        vn.NARRATION_DIR = proj / "public" / "narration"
   258	        vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
   259	        vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
   260	        vn.NARRATION_DIR.mkdir(parents=True)
   261	        vn.NARRATION_DATA_TS.parent.mkdir(parents=True)
   262	
   263	        write_synthetic_wav(vn.NARRATION_DIR / "chunk_000.wav", 1.0)
   264	        write_synthetic_wav(vn.NARRATION_DIR / "chunk_001.wav", 0.5)
   265	
   266	        # No cut, transcript timing 0ms と 1000ms
   267	        chunks_data = [
   268	            (vn.NARRATION_DIR / "chunk_000.wav", "first", 0, 1000),
   269	            (vn.NARRATION_DIR / "chunk_001.wav", "second", 1000, 1500),
   270	        ]
   271	        segments, ts_path, meta_path = vn.write_narration_data(chunks_data, 30, [])
   272	        assert_eq(segments[0]["startFrame"], 0, "chunk0 startFrame")
   273	        assert_eq(segments[0]["durationInFrames"], 30, "chunk0 dur")
   274	        assert_eq(segments[0]["timing_source"], "transcript_aligned", "chunk0 source")
   275	        assert_eq(segments[1]["startFrame"], 30, "chunk1 startFrame (1000ms*30fps)")
   276	
   277	        # Verify TS file is valid
   278	        ts = ts_path.read_text(encoding="utf-8")
   279	        assert "narrationData" in ts
   280	        assert "sourceStartMs: 0" in ts
   281	        assert "sourceStartMs: 1000" in ts
   282	
   283	
   284	def main() -> int:
   285	    tests = [
   286	        test_fps_consistency,
   287	        test_vad_schema_validation,
   288	        test_ms_to_playback_frame,
   289	        test_load_cut_segments_fail_fast,
   290	        test_transcript_segment_validation,
   291	        test_voicevox_collect_chunks_validation,
   292	        test_voicevox_write_narration_data_alignment,
   293	    ]
   294	    failed = []
   295	    for t in tests:
   296	        name = t.__name__
   297	        try:
   298	            t()
   299	            print(f"  [OK]   {name}")
   300	        except AssertionError as e:
   301	            failed.append((name, str(e)))
   302	            print(f"  [FAIL] {name}: {e}", file=sys.stderr)
   303	        except Exception as e:
   304	            failed.append((name, f"{type(e).__name__}: {e}"))
   305	            print(f"  [ERR]  {name}: {type(e).__name__}: {e}", file=sys.stderr)
   306	
   307	    total = len(tests)
   308	    print(f"\nResult: {total - len(failed)}/{total} pass, {len(failed)} fail")
   309	    if failed:
   310	        for name, msg in failed:
   311	            print(f"  - {name}: {msg}", file=sys.stderr)
   312	    return 0 if not failed else 1
   313	
   314	
   315	if __name__ == "__main__":
   316	    sys.exit(main())

codex
コード上では `validate_transcript_segments` 自体は既に存在しますが、呼び出し側はまだ一括 API ではなく segment 単位の validate です。ここは Phase 3-L 候補の評価で「残作業の実質量」として扱います。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/src/Narration/mode.ts' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import { getStaticFiles } from 'remotion';
     2	import { narrationData } from './narrationData';
     3	import type { NarrationSegment } from './types';
     4	
     5	export const NARRATION_LEGACY_FILE = 'narration.wav';
     6	
     7	/**
     8	 * Phase 3-H Codex review P1 #1 反映:
     9	 * NarrationAudio と MainVideo が narration の状態を別々に判定すると、
    10	 * chunk 不足 + legacy 存在で「narration も base 元音声も無音」になる
    11	 * 矛盾モードが発生する。本 helper を両者から呼ぶことで mode を一元化する。
    12	 */
    13	export type NarrationMode =
    14	  | { kind: 'chunks'; segments: readonly NarrationSegment[] }
    15	  | { kind: 'legacy'; file: string }
    16	  | { kind: 'none' };
    17	
    18	/**
    19	 * narration の有効モードを返す。優先順位:
    20	 *   1) narrationData が non-empty + 全 chunk file が public/ 配下に存在 → chunks
    21	 *   2) public/narration.wav 存在 → legacy
    22	 *   3) どちらも不在 → none
    23	 *
    24	 * getStaticFiles() の結果を一度 Set 化して O(1) lookup
    25	 * (Codex P3 #8 反映、毎 frame の some() 重複を防ぐ)。
    26	 *
    27	 * Codex re-review 新規 P3 反映: module-level memo で 1 render 内の
    28	 * 重複呼出 (MainVideo + NarrationAudio が両方 call) を 1 回に集約。
    29	 * Remotion は 1 render で 1 JS context を使うため、context-fresh で
    30	 * 自然に memo が消える (Studio hot-reload 時も module 再評価で reset)。
    31	 *
    32	 * 出典: https://www.remotion.dev/docs/getstaticfiles
    33	 */
    34	let _modeCache: NarrationMode | undefined;
    35	
    36	export const getNarrationMode = (): NarrationMode => {
    37	  if (_modeCache !== undefined) {
    38	    return _modeCache;
    39	  }
    40	  const names = new Set(getStaticFiles().map((f) => f.name));
    41	  if (
    42	    narrationData.length > 0 &&
    43	    narrationData.every((seg) => names.has(seg.file))
    44	  ) {
    45	    _modeCache = { kind: 'chunks', segments: narrationData };
    46	  } else if (names.has(NARRATION_LEGACY_FILE)) {
    47	    _modeCache = { kind: 'legacy', file: NARRATION_LEGACY_FILE };
    48	  } else {
    49	    _modeCache = { kind: 'none' };
    50	  }
    51	  return _modeCache;
    52	};

exec
/bin/zsh -lc 'PYTHONDONTWRITEBYTECODE=1 python3 template/scripts/test_timeline_integration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
  [ERR]  test_fps_consistency: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  [ERR]  test_load_cut_segments_fail_fast: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  [ERR]  test_voicevox_write_narration_data_alignment: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  - test_fps_consistency: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  - test_load_cut_segments_fail_fast: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  - test_voicevox_write_narration_data_alignment: FileNotFoundError: [Errno 2] No usable temporary directory found in ['/var/folders/kn/7rmr9pdx4fq8tqnsq4g8tyyh0000gn/T/', '/tmp', '/var/tmp', '/usr/tmp', '/Users/rokumasuda/.claude/plugins/supermovie']
  [OK]   test_vad_schema_validation
  [OK]   test_ms_to_playback_frame
  [OK]   test_transcript_segment_validation
  [OK]   test_voicevox_collect_chunks_validation

Result: 4/7 pass, 3 fail

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/eslint.config.mjs' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	// @remotion/eslint-config-flat 4.x は default export を提供せず、named exports
     2	// (config / makeConfig) を提供する。default import すると `does not provide an
     3	// export named 'default'` で fail するため、named import に切り替える。
     4	import { config } from "@remotion/eslint-config-flat";
     5	
     6	// telop-templates-30.zip 由来の component が `any` を使っているため、
     7	// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
     8	export default [
     9	  ...config,
    10	  {
    11	    rules: {
    12	      "@typescript-eslint/no-explicit-any": "warn",
    13	    },
    14	  },
    15	];

exec
/bin/zsh -lc 'nl -ba template/scripts/generate_slide_plan.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-C optional script: Anthropic API で slide_plan.json を生成.
     3	
     4	Codex Phase 3C design (2026-05-04, CODEX_PHASE3C_LLM_PLAN) 推奨:
     5	- LLM は word index ベースの slide_plan.json を返す (frame は build_slide_data.py が変換)
     6	- ANTHROPIC_API_KEY が無ければ skip (非ゼロ終了しない)
     7	- build_slide_data.py が plan を validate して invalid なら deterministic fallback
     8	
     9	Usage:
    10	    ANTHROPIC_API_KEY=sk-ant-... python3 scripts/generate_slide_plan.py \\
    11	        --output slide_plan.json [--model claude-haiku-4-5-20251001]
    12	"""
    13	from __future__ import annotations
    14	
    15	import argparse
    16	import json
    17	import os
    18	import sys
    19	from pathlib import Path
    20	
    21	PROJ = Path(__file__).resolve().parent.parent
    22	PLAN_VERSION = "supermovie.slide_plan.v1"
    23	
    24	PROMPT_TEMPLATE = """\
    25	あなたは動画編集者です。SuperMovie パイプラインの slide_plan を返してください。
    26	
    27	## 入力
    28	- transcript: 動画のナレーション文字起こし (ms timestamps + words 配列)
    29	- format: {fmt} (短尺=short / 横長=youtube / 正方形=square)
    30	- tone: {tone}
    31	
    32	## 制約 (絶対ルール)
    33	1. word index で slide 範囲を返す (startWordIndex / endWordIndex 必須)
    34	2. word index は 0..{n_words_minus_1} の範囲、startWordIndex <= endWordIndex
    35	3. 隣接 slide の word range は overlap しない (前 slide の endWordIndex < 次 slide の startWordIndex)
    36	4. id は 1 から昇順
    37	5. title は {title_max} 文字以内、必須、空不可
    38	6. bullets は最大 {max_bullets} 個、各 bullet text は {bullet_max} 文字以内
    39	7. align は "center" or "left" のみ
    40	8. videoLayer は "visible" / "dimmed" / "hidden" のみ (省略可)
    41	
    42	## 出力 (JSON のみ、コードフェンス不要)
    43	{{
    44	  "version": "{plan_version}",
    45	  "slides": [
    46	    {{
    47	      "id": 1,
    48	      "startWordIndex": 0,
    49	      "endWordIndex": 30,
    50	      "title": "短い見出し",
    51	      "subtitle": "任意",
    52	      "bullets": [
    53	        {{ "text": "要点", "emphasis": true }}
    54	      ],
    55	      "align": "left",
    56	      "videoLayer": "visible"
    57	    }}
    58	  ]
    59	}}
    60	
    61	## transcript (words 配列、最大 200 word のみ抜粋。全 {n_words} 個の最初):
    62	{words_preview}
    63	
    64	## 全 segments (timestamp 付き):
    65	{segments_preview}
    66	"""
    67	
    68	
    69	def load_json(p: Path):
    70	    return json.loads(p.read_text(encoding="utf-8"))
    71	
    72	
    73	def main():
    74	    ap = argparse.ArgumentParser()
    75	    ap.add_argument("--output", default=str(PROJ / "slide_plan.json"))
    76	    ap.add_argument("--model", default="claude-haiku-4-5-20251001",
    77	                    help="Anthropic model (default: claude-haiku-4-5、cost 最小)")
    78	    args = ap.parse_args()
    79	
    80	    api_key = os.environ.get("ANTHROPIC_API_KEY")
    81	    if not api_key:
    82	        print("INFO: ANTHROPIC_API_KEY 未設定 → slide_plan 生成 skip")
    83	        print("      build_slide_data.py は --plan 無しで deterministic に走ります")
    84	        return 0
    85	
    86	    transcript_path = PROJ / "transcript_fixed.json"
    87	    config_path = PROJ / "project-config.json"
    88	    if not transcript_path.exists() or not config_path.exists():
    89	        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
    90	        return 3
    91	
    92	    transcript = load_json(transcript_path)
    93	    config = load_json(config_path)
    94	    fmt = config.get("format", "short")
    95	    tone = config.get("tone", "プロフェッショナル")
    96	    words = transcript.get("words", [])
    97	    segments = transcript.get("segments", [])
    98	    n_words = len(words)
    99	
   100	    title_max = {"youtube": 18, "short": 14, "square": 16}.get(fmt, 14)
   101	    bullet_max = {"youtube": 24, "short": 18, "square": 20}.get(fmt, 18)
   102	
   103	    words_preview = "\n".join(
   104	        f"  [{i}] {w.get('text','')!r} ({w.get('start')}ms-{w.get('end')}ms)"
   105	        for i, w in enumerate(words[:200])
   106	    )
   107	    segments_preview = "\n".join(
   108	        f"  seg[{i}] {s.get('start')}-{s.get('end')}ms: {s.get('text','')}"
   109	        for i, s in enumerate(segments)
   110	    )
   111	
   112	    prompt = PROMPT_TEMPLATE.format(
   113	        fmt=fmt,
   114	        tone=tone,
   115	        n_words=n_words,
   116	        n_words_minus_1=max(n_words - 1, 0),
   117	        title_max=title_max,
   118	        bullet_max=bullet_max,
   119	        max_bullets=5,
   120	        plan_version=PLAN_VERSION,
   121	        words_preview=words_preview,
   122	        segments_preview=segments_preview,
   123	    )
   124	
   125	    # Anthropic API 呼び出し (urllib で SDK 不要に保つ)
   126	    import urllib.request
   127	    import urllib.error
   128	    body = {
   129	        "model": args.model,
   130	        "max_tokens": 4096,
   131	        "messages": [{"role": "user", "content": prompt}],
   132	    }
   133	    req = urllib.request.Request(
   134	        "https://api.anthropic.com/v1/messages",
   135	        data=json.dumps(body).encode("utf-8"),
   136	        headers={
   137	            "x-api-key": api_key,
   138	            "anthropic-version": "2023-06-01",
   139	            "content-type": "application/json",
   140	        },
   141	        method="POST",
   142	    )
   143	    try:
   144	        with urllib.request.urlopen(req, timeout=60) as resp:
   145	            response = json.loads(resp.read().decode("utf-8"))
   146	    except urllib.error.HTTPError as e:
   147	        body = e.read().decode("utf-8", errors="replace")
   148	        print(f"ERROR: Anthropic API HTTP {e.code}: {body[:500]}", file=sys.stderr)
   149	        return 4
   150	
   151	    text = "".join(b.get("text", "") for b in response.get("content", []) if b.get("type") == "text")
   152	    # コードフェンス除去 (LLM が markdown 返した場合)
   153	    text = text.strip()
   154	    if text.startswith("```"):
   155	        text = text.split("\n", 1)[1] if "\n" in text else text
   156	        if text.endswith("```"):
   157	            text = text.rsplit("```", 1)[0]
   158	    text = text.strip()
   159	
   160	    try:
   161	        plan = json.loads(text)
   162	    except json.JSONDecodeError as e:
   163	        print(f"ERROR: LLM 応答が JSON parse 失敗: {e}\n--- raw ---\n{text[:1000]}", file=sys.stderr)
   164	        return 5
   165	
   166	    out_path = Path(args.output)
   167	    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
   168	    print(f"wrote: {out_path}")
   169	    print(f"slides: {len(plan.get('slides', []))}")
   170	    return 0
   171	
   172	
   173	if __name__ == "__main__":
   174	    sys.exit(main())

exec
/bin/zsh -lc 'git show --stat --oneline --decorate --no-renames 66e2aeb..e2a1a39' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-zx9XFoMV' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-bkzDPTg9' (errno=Operation not permitted)
e2a1a39 (HEAD -> roku/phase3j-timeline) fix(timeline): Codex Phase 3-J review 4 件 fix (P1×1 + P2×2 + P3×1)
 skills/supermovie-narration/SKILL.md          |  2 +
 template/scripts/build_telop_data.py          |  8 +++
 template/scripts/test_timeline_integration.py | 26 +++++++
 template/scripts/voicevox_narration.py        | 99 +++++++++++++++++----------
 4 files changed, 97 insertions(+), 38 deletions(-)
41b5ef2 fix(timeline): transcript validation を build_slide / build_telop にも展開 (Phase 3-K core 2)
 template/scripts/build_slide_data.py | 11 +++++++++++
 template/scripts/build_telop_data.py | 14 +++++++++++++-
 2 files changed, 24 insertions(+), 1 deletion(-)
398ea94 test(timeline): pure python integration smoke test (Phase 3-K core 1)
 CLAUDE.md                                     |  14 +-
 template/package.json                         |   3 +-
 template/scripts/test_timeline_integration.py | 290 ++++++++++++++++++++++++++
 3 files changed, 303 insertions(+), 4 deletions(-)

codex
実行テストは read-only sandbox のため tempfile が必要な一部だけ失敗し、tempfile 不要の validation 系は通りました。VAD fail-fast と script-json guard はファイルを書かない monkeypatch テストで補強確認します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/package.json' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	{
     2	  "name": "supermovie-project",
     3	  "version": "1.0.0",
     4	  "description": "SuperMovie - Remotion動画プロジェクト",
     5	  "repository": {},
     6	  "license": "UNLICENSED",
     7	  "private": true,
     8	  "dependencies": {
     9	    "@remotion/cli": "4.0.403",
    10	    "@remotion/zod-types": "4.0.403",
    11	    "react": "19.2.3",
    12	    "react-dom": "19.2.3",
    13	    "remotion": "4.0.403",
    14	    "zod": "3.22.3",
    15	    "@remotion/tailwind-v4": "4.0.403",
    16	    "tailwindcss": "4.0.0",
    17	    "budoux": "^0.8.0"
    18	  },
    19	  "devDependencies": {
    20	    "@remotion/eslint-config-flat": "4.0.403",
    21	    "@types/react": "19.2.7",
    22	    "@types/web": "0.0.166",
    23	    "eslint": "9.19.0",
    24	    "prettier": "3.6.0",
    25	    "typescript": "5.9.3"
    26	  },
    27	  "scripts": {
    28	    "dev": "remotion studio",
    29	    "build": "remotion bundle",
    30	    "render": "remotion render MainVideo out/video.mp4",
    31	    "upgrade": "remotion upgrade",
    32	    "lint": "eslint src && tsc",
    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
    35	    "test:timeline": "python3 scripts/test_timeline_integration.py",
    36	    "test": "npm run lint && npm run test:timeline"
    37	  },
    38	  "sideEffects": [
    39	    "*.css"
    40	  ]
    41	}

exec
/bin/zsh -lc 'git diff --name-only roku/phase3i-transcript-alignment..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Dh18kigk' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-BLeFd0ZI' (errno=Operation not permitted)
CLAUDE.md
skills/supermovie-narration/SKILL.md
template/package.json
template/scripts/build_slide_data.py
template/scripts/build_telop_data.py
template/scripts/test_timeline_integration.py
template/scripts/timeline.py
template/scripts/voicevox_narration.py

codex
heredoc 自体が sandbox で一時ファイルを作れず失敗しました。読み取り検証の範囲に収めるため、同じ monkeypatch 確認を `python -c` 形式で再実行します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -c $'"'import sys\\nfrom pathlib import Path\\nsys.path.insert(0, str(Path(\"template/scripts\").resolve()))\\nimport voicevox_narration as vn\\nclass Args:\\n    script = None\\n    script_json = \"dummy.json\"\\ndef run_case(name, value):\\n    old = vn.load_json\\n    vn.load_json = lambda path: value\\n    try:\\n        try:\\n            vn.collect_chunks(Args(), {})\\n        except vn.TranscriptSegmentError as e:\\n            print(f\"OK {name}: {type(e).__name__}: {e}\")\\n        except Exception as e:\\n            print(f\"BAD {name}: {type(e).__name__}: {e}\")\\n        else:\\n            print(f\"BAD {name}: no exception\")\\n    finally:\\n        vn.load_json = old\\nrun_case(\"plan-not-dict\", [\"not dict\"])\\nrun_case(\"segments-not-list\", {\"segments\": \"wrong\"})\\nrun_case(\"segment-not-dict\", {\"segments\": [\"not dict\"]})\\nrun_case(\"text-not-str\", {\"segments\": [{\"text\": 123}]})\\nrun_case(\"timing-start-bad\", {\"segments\": [{\"text\": \"hi\", \"startMs\": \"bad\", \"endMs\": 100}]})'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
OK plan-not-dict: TranscriptSegmentError: script-json must be dict, got list
OK segments-not-list: TranscriptSegmentError: script-json segments must be list, got str
OK segment-not-dict: TranscriptSegmentError: segment[0] must be dict, got str
OK text-not-str: TranscriptSegmentError: segment[0].text must be str|None, got int
OK timing-start-bad: TranscriptSegmentError: segment[0].start must be int|float|None, got str

exec
/bin/zsh -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -c $'"'import sys\\nfrom pathlib import Path\\nsys.path.insert(0, str(Path(\"template/scripts\").resolve()))\\nimport voicevox_narration as vn\\nevents = []\\nold_argv = sys.argv[:]\\norig = {\"check_engine\": vn.check_engine, \"collect_chunks\": vn.collect_chunks, \"cleanup_stale_all\": vn.cleanup_stale_all, \"project_load_cut_segments\": vn.project_load_cut_segments, \"synthesize\": vn.synthesize, \"NARRATION_DIR\": vn.NARRATION_DIR}\\nclass DummyDir:\\n    def mkdir(self, *args, **kwargs):\\n        events.append(\"mkdir\")\\ndef cleanup():\\n    events.append(\"cleanup\")\\ndef load_cut(fps):\\n    events.append(\"vad\")\\n    raise vn.VadSchemaError(\"bad vad\")\\ndef synthesize(*args, **kwargs):\\n    events.append(\"synthesis\")\\n    raise RuntimeError(\"synthesis should not be called\")\\ntry:\\n    vn.check_engine = lambda: (True, \"test-engine\")\\n    vn.collect_chunks = lambda args, transcript: [{\"text\": \"hello\", \"sourceStartMs\": 0, \"sourceEndMs\": 100}]\\n    vn.cleanup_stale_all = cleanup\\n    vn.project_load_cut_segments = load_cut\\n    vn.synthesize = synthesize\\n    vn.NARRATION_DIR = DummyDir()\\n    sys.argv = [\"voicevox_narration.py\", \"--script\", \"dummy\"]\\n    code = vn.main()\\n    print(f\"code={code}\")\\n    print(\"events=\" + \",\".join(events))\\nfinally:\\n    sys.argv = old_argv\\n    for k, v in orig.items():\\n        setattr(vn, k, v)'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
ERROR: vad_result.json schema invalid or unreadable: bad vad
VOICEVOX engine OK (version: test-engine)
target fps: 30
code=8
events=cleanup,mkdir,vad

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -c $'"'import sys\\nfrom pathlib import Path\\nsys.path.insert(0, str(Path(\"template/scripts\").resolve()))\\nimport timeline\\nfor name, call in [\\n    (\"optional-ok\", lambda: timeline.validate_transcript_segments([{\"text\":\"hi\"}], require_timing=False)),\\n    (\"strict-missing-start\", lambda: timeline.validate_transcript_segments([{\"text\":\"hi\", \"end\": 100}], require_timing=True)),\\n    (\"strict-ok\", lambda: timeline.validate_transcript_segments([{\"text\":\"hi\", \"start\": 0, \"end\": 100}], require_timing=True)),\\n]:\\n    try:\\n        result = call()\\n    except Exception as e:\\n        print(f\"{name}: {type(e).__name__}: {e}\")\\n    else:\\n        print(f\"{name}: OK len={len(result)}\")'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
optional-ok: OK len=1
strict-missing-start: TranscriptSegmentError: segment[0].start required (int|float), got NoneType
strict-ok: OK len=1

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "test -d template/public/narration; printf 'narration_dir_exists=%s\\n' "'$?' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
narration_dir_exists=1

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'ls -la template/public 2>/dev/null' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "rg -n \"watchStaticFile|useCurrentFrame|staticFile\\(|getStaticFiles|watch\" template/src template/scripts template/package.json" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
 succeeded in 0ms:
template/src/ネガティブテロップ/紫文字白背景.tsx:4:  useCurrentFrame,
template/src/ネガティブテロップ/紫文字白背景.tsx:45:  const frame = useCurrentFrame();
template/src/ネガティブテロップ/黒紫グラデ.tsx:4:  useCurrentFrame,
template/src/ネガティブテロップ/黒紫グラデ.tsx:45:  const frame = useCurrentFrame();
template/src/ネガティブテロップ/残酷テロップ・紺.tsx:4:  useCurrentFrame,
template/src/ネガティブテロップ/残酷テロップ・紺.tsx:37:  const frame = useCurrentFrame();
template/src/ネガティブテロップ/白文字紫シャドウ.tsx:4:  useCurrentFrame,
template/src/ネガティブテロップ/白文字紫シャドウ.tsx:43:  const frame = useCurrentFrame();
template/src/ネガティブテロップ/黒文字白背景.tsx:4:  useCurrentFrame,
template/src/ネガティブテロップ/黒文字白背景.tsx:45:  const frame = useCurrentFrame();
template/src/Slides/Slide.tsx:2:import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
template/src/Slides/Slide.tsx:10:  const frame = useCurrentFrame();
template/src/SoundEffects/BGM.tsx:1:import { Audio, getStaticFiles, staticFile } from 'remotion';
template/src/SoundEffects/BGM.tsx:11: * 失敗させない。getStaticFiles() は public/ 以下の asset 一覧を返す Remotion 公式 API
template/src/SoundEffects/BGM.tsx:15:  const hasFile = getStaticFiles().some((f) => f.name === BGM_FILE);
template/src/SoundEffects/BGM.tsx:19:  return <Audio src={staticFile(BGM_FILE)} volume={() => volume} loop />;
template/src/SoundEffects/SESequence.tsx:11:            <Audio src={staticFile(`se/${se.file}`)} volume={() => v} />
template/src/InsertImage/InsertImage.tsx:2:import { useCurrentFrame, interpolate, Img, staticFile } from 'remotion';
template/src/InsertImage/InsertImage.tsx:10:  const frame = useCurrentFrame();
template/src/InsertImage/InsertImage.tsx:43:          src={staticFile(`images/${segment.file}`)}
template/src/InsertImage/InsertImage.tsx:65:        src={staticFile(`images/${segment.file}`)}
template/src/強調テロップ/白赤テロップver2.tsx:4:  useCurrentFrame,
template/src/強調テロップ/白赤テロップver2.tsx:43:  const frame = useCurrentFrame();
template/src/強調テロップ/オレンジグラデーション.tsx:4:  useCurrentFrame,
template/src/強調テロップ/オレンジグラデーション.tsx:37:  const frame = useCurrentFrame();
template/src/メインテロップ/白文字黒シャドウゴシック.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白文字黒シャドウゴシック.tsx:39:  const frame = useCurrentFrame();
template/src/強調テロップ/金グラデ・紺背景.tsx:4:  useCurrentFrame,
template/src/強調テロップ/金グラデ・紺背景.tsx:45:  const frame = useCurrentFrame();
template/src/強調テロップ/黄色文字黒シャドウ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/黄色文字黒シャドウ.tsx:39:  const frame = useCurrentFrame();
template/src/メインテロップ/白青テロップ.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白青テロップ.tsx:51:  const frame = useCurrentFrame();
template/src/強調テロップ/黄色シャドウ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/黄色シャドウ.tsx:39:  const frame = useCurrentFrame();
template/src/強調テロップ/赤文字.tsx:4:  useCurrentFrame,
template/src/強調テロップ/赤文字.tsx:43:  const frame = useCurrentFrame();
template/src/メインテロップ/白青テロップver2.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白青テロップver2.tsx:43:  const frame = useCurrentFrame();
template/src/メインテロップ/白文字黒シャドウ.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白文字黒シャドウ.tsx:47:  const frame = useCurrentFrame();
template/src/メインテロップ/緑文字白背景.tsx:4:  useCurrentFrame,
template/src/メインテロップ/緑文字白背景.tsx:45:  const frame = useCurrentFrame();
template/src/メインテロップ/黒文字.tsx:4:  useCurrentFrame,
template/src/メインテロップ/黒文字.tsx:43:  const frame = useCurrentFrame();
template/src/強調テロップ/青文字金枠.tsx:4:  useCurrentFrame,
template/src/強調テロップ/青文字金枠.tsx:41:  const frame = useCurrentFrame();
template/src/強調テロップ/白緑テロップ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/白緑テロップ.tsx:51:  const frame = useCurrentFrame();
template/src/メインテロップ/青文字白背景.tsx:4:  useCurrentFrame,
template/src/メインテロップ/青文字白背景.tsx:45:  const frame = useCurrentFrame();
template/src/強調テロップ/赤文字白背景.tsx:4:  useCurrentFrame,
template/src/強調テロップ/赤文字白背景.tsx:45:  const frame = useCurrentFrame();
template/src/MainVideo.tsx:19:  // で getStaticFiles cache を再生成する必要がある
template/src/MainVideo.tsx:28:        src={staticFile(VIDEO_FILE)}
template/src/強調テロップ/黒文字黄色背景.tsx:4:  useCurrentFrame,
template/src/強調テロップ/黒文字黄色背景.tsx:41:  const frame = useCurrentFrame();
template/src/強調テロップ/白赤テロップ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/白赤テロップ.tsx:51:  const frame = useCurrentFrame();
template/src/メインテロップ/白文字黒背景.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白文字黒背景.tsx:45:  const frame = useCurrentFrame();
template/src/メインテロップ/白黒テロップ.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白黒テロップ.tsx:41:  const frame = useCurrentFrame();
template/src/メインテロップ/白文字青ピンク背景グラデ.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白文字青ピンク背景グラデ.tsx:51:  const frame = useCurrentFrame();
template/src/メインテロップ/白背景グラデ.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白背景グラデ.tsx:44:  const frame = useCurrentFrame();
template/src/強調テロップ/白文字赤シャドウ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/白文字赤シャドウ.tsx:43:  const frame = useCurrentFrame();
template/src/Narration/NarrationAudio.tsx:28:            <Audio src={staticFile(seg.file)} volume={() => volume} />
template/src/Narration/NarrationAudio.tsx:36:    return <Audio src={staticFile(mode.file)} volume={() => volume} />;
template/src/強調テロップ/緑グラデ金シャドウ.tsx:4:  useCurrentFrame,
template/src/強調テロップ/緑グラデ金シャドウ.tsx:37:  const frame = useCurrentFrame();
template/src/Title/Title.tsx:3:  useCurrentFrame,
template/src/Title/Title.tsx:24:  const frame = useCurrentFrame();
template/src/テロップテンプレート/Telop.tsx:3:  useCurrentFrame,
template/src/テロップテンプレート/Telop.tsx:200:  const frame = useCurrentFrame();
template/src/テロップテンプレート/TelopPlayer.tsx:2:import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
template/src/テロップテンプレート/TelopPlayer.tsx:37:  const frame = useCurrentFrame();
template/src/メインテロップ/白文字黒シャドウ明朝体.tsx:4:  useCurrentFrame,
template/src/メインテロップ/白文字黒シャドウ明朝体.tsx:39:  const frame = useCurrentFrame();
template/src/Narration/mode.ts:1:import { getStaticFiles } from 'remotion';
template/src/Narration/mode.ts:24: * getStaticFiles() の結果を一度 Set 化して O(1) lookup
template/src/Narration/mode.ts:40:  const names = new Set(getStaticFiles().map((f) => f.name));

exec
/bin/zsh -lc "rg -n \"validate_transcript_segments|validate_transcript_segment\\(\" template/scripts" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
template/scripts/voicevox_narration.py:420:            validate_transcript_segment(
template/scripts/voicevox_narration.py:452:        validate_transcript_segment(s, idx=i)
template/scripts/build_telop_data.py:304:            validate_transcript_segment(seg, idx=i, require_timing=True)
template/scripts/build_slide_data.py:334:            validate_transcript_segment(seg, idx=i, require_timing=True)
template/scripts/timeline.py:13:- validate_transcript_segment(): transcript_fixed.json segments[].start/end
template/scripts/timeline.py:158:def validate_transcript_segment(
template/scripts/timeline.py:199:def validate_transcript_segments(
template/scripts/timeline.py:212:        validate_transcript_segment(seg, idx=i, require_timing=require_timing)
template/scripts/test_timeline_integration.py:175:    timeline.validate_transcript_segment({"text": "hi"}, 0)
template/scripts/test_timeline_integration.py:177:    timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
template/scripts/test_timeline_integration.py:180:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:188:        lambda: timeline.validate_transcript_segment({"text": 123}, 0),
template/scripts/test_timeline_integration.py:194:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:204:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:211:        lambda: timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:218:    timeline.validate_transcript_segment(
template/scripts/test_timeline_integration.py:222:    # validate_transcript_segments 一括 helper
template/scripts/test_timeline_integration.py:223:    out = timeline.validate_transcript_segments(
template/scripts/test_timeline_integration.py:227:    assert_eq(len(out), 2, "validate_transcript_segments OK length")
template/scripts/test_timeline_integration.py:230:        lambda: timeline.validate_transcript_segments("not a list"),
template/scripts/test_timeline_integration.py:232:        "validate_transcript_segments non-list",

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/src/MainVideo.tsx' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import { AbsoluteFill, Video, staticFile } from 'remotion';
     2	import { TelopPlayer } from './テロップテンプレート';
     3	import { SESequence } from './SoundEffects/SESequence';
     4	import { BGM } from './SoundEffects/BGM';
     5	import { ImageSequence } from './InsertImage';
     6	import { TitleSequence } from './Title';
     7	import { SlideSequence } from './Slides';
     8	import { NarrationAudio } from './Narration';
     9	import { getNarrationMode } from './Narration/mode';
    10	import { VIDEO_FILE } from './videoConfig';
    11	
    12	export const MainVideo: React.FC = () => {
    13	  // Phase 3-F asset gate + Phase 3-H per-segment Sequence の mode helper を共有
    14	  // (Codex Phase 3-H review P1 #1 反映)。chunks / legacy / none のいずれでも
    15	  // narration が「鳴る」状態なら base 元音声を mute、'none' なら 1.0 で再生する。
    16	  // これで NarrationAudio と判定が一致し、無音バグ (chunk 不足 + legacy 存在で
    17	  // 両方消える) を防ぐ。
    18	  // 注意: Studio 起動後に narration を生成した場合、Studio reload (Cmd+R / `r` キー)
    19	  // で getStaticFiles cache を再生成する必要がある
    20	  // (https://www.remotion.dev/docs/getstaticfiles)。
    21	  const narrationMode = getNarrationMode();
    22	  const baseVolume = narrationMode.kind === 'none' ? 1.0 : 0;
    23	
    24	  return (
    25	    <AbsoluteFill style={{ backgroundColor: 'black' }}>
    26	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
    27	      <Video
    28	        src={staticFile(VIDEO_FILE)}
    29	        volume={() => baseVolume}
    30	        style={{
    31	          width: '100%',
    32	          height: '100%',
    33	          objectFit: 'contain',
    34	        }}
    35	      />
    36	
    37	      {/* スライド (Phase 3-A、別レイヤーで動画の上に被せる) */}
    38	      <SlideSequence />
    39	
    40	      {/* 挿入画像 */}
    41	      <ImageSequence />
    42	
    43	      {/* テロップ */}
    44	      <TelopPlayer />
    45	
    46	      {/* タイトル */}
    47	      <TitleSequence />
    48	
    49	      {/* ナレーション (Phase 3-F asset gate、narration.wav 不在で null) */}
    50	      <NarrationAudio volume={1.0} />
    51	
    52	      {/* BGM (Phase 3-F asset gate、bgm.mp3 不在で null) */}
    53	      <BGM volume={0.08} />
    54	
    55	      {/* 効果音 */}
    56	      <SESequence />
    57	    </AbsoluteFill>
    58	  );
    59	};

hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/test_timeline_integration.py | sed -n '170,255p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   170	
   171	
   172	def test_transcript_segment_validation() -> None:
   173	    """validate_transcript_segment が壊れた transcript を検出する."""
   174	    # OK: timing なし (--script の chunk)
   175	    timeline.validate_transcript_segment({"text": "hi"}, 0)
   176	    # OK: 通常 transcript
   177	    timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
   178	    # NG: start > end
   179	    assert_raises(
   180	        lambda: timeline.validate_transcript_segment(
   181	            {"text": "hi", "start": 1000, "end": 500}, 0
   182	        ),
   183	        timeline.TranscriptSegmentError,
   184	        "transcript start>end",
   185	    )
   186	    # NG: text 非 str
   187	    assert_raises(
   188	        lambda: timeline.validate_transcript_segment({"text": 123}, 0),
   189	        timeline.TranscriptSegmentError,
   190	        "text non-str",
   191	    )
   192	    # NG: start 型不正
   193	    assert_raises(
   194	        lambda: timeline.validate_transcript_segment(
   195	            {"text": "hi", "start": "bad"}, 0
   196	        ),
   197	        timeline.TranscriptSegmentError,
   198	        "start non-numeric",
   199	    )
   200	
   201	    # Phase 3-L (Codex Phase 3-J review Part B 推奨): require_timing=True で
   202	    # start/end 必須化、欠落 / None で raise。
   203	    assert_raises(
   204	        lambda: timeline.validate_transcript_segment(
   205	            {"text": "hi"}, 0, require_timing=True
   206	        ),
   207	        timeline.TranscriptSegmentError,
   208	        "require_timing missing both",
   209	    )
   210	    assert_raises(
   211	        lambda: timeline.validate_transcript_segment(
   212	            {"text": "hi", "start": 0, "end": None}, 0, require_timing=True
   213	        ),
   214	        timeline.TranscriptSegmentError,
   215	        "require_timing end None",
   216	    )
   217	    # OK: require_timing=True + 両方 numeric
   218	    timeline.validate_transcript_segment(
   219	        {"text": "hi", "start": 0, "end": 1000}, 0, require_timing=True
   220	    )
   221	
   222	    # validate_transcript_segments 一括 helper
   223	    out = timeline.validate_transcript_segments(
   224	        [{"text": "a", "start": 0, "end": 100}, {"text": "b", "start": 100, "end": 200}],
   225	        require_timing=True,
   226	    )
   227	    assert_eq(len(out), 2, "validate_transcript_segments OK length")
   228	    # 非 list で raise
   229	    assert_raises(
   230	        lambda: timeline.validate_transcript_segments("not a list"),
   231	        timeline.TranscriptSegmentError,
   232	        "validate_transcript_segments non-list",
   233	    )
   234	
   235	
   236	def test_voicevox_collect_chunks_validation() -> None:
   237	    """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
   238	    import voicevox_narration as vn
   239	
   240	    class Args:
   241	        script = None
   242	        script_json = None
   243	
   244	    bad = {"segments": [{"text": "hi", "start": 100, "end": 50}]}
   245	    assert_raises(
   246	        lambda: vn.collect_chunks(Args(), bad),
   247	        vn.TranscriptSegmentError,
   248	        "voicevox start>end transcript",
   249	    )
   250	
   251	    good = {"segments": [{"text": "hi", "start": 0, "end": 1000}]}
   252	    out = vn.collect_chunks(Args(), good)
   253	    assert_eq(len(out), 1, "voicevox good transcript len")
   254	    assert_eq(out[0]["sourceStartMs"], 0, "voicevox sourceStartMs")
   255	    assert_eq(out[0]["sourceEndMs"], 1000, "voicevox sourceEndMs")

exec
/bin/zsh -lc 'git diff --stat roku/phase3i-transcript-alignment..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'git log --oneline --decorate -4' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-GH9Iv0Ow' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ggWLfi7Y' (errno=Operation not permitted)
a9019c7 (HEAD -> roku/phase3j-timeline) feat(timeline): require_timing strict mode + validate_transcript_segments helper (Phase 3-L core)
e2a1a39 fix(timeline): Codex Phase 3-J review 4 件 fix (P1×1 + P2×2 + P3×1)
41b5ef2 fix(timeline): transcript validation を build_slide / build_telop にも展開 (Phase 3-K core 2)
398ea94 test(timeline): pure python integration smoke test (Phase 3-K core 1)

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-pcEQOAQ8' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-h10HFnkq' (errno=Operation not permitted)
 CLAUDE.md                                     |  14 +-
 skills/supermovie-narration/SKILL.md          |   2 +
 template/package.json                         |   3 +-
 template/scripts/build_slide_data.py          |  55 ++--
 template/scripts/build_telop_data.py          |  28 ++-
 template/scripts/test_timeline_integration.py | 350 ++++++++++++++++++++++++++
 template/scripts/timeline.py                  | 214 ++++++++++++++++
 template/scripts/voicevox_narration.py        | 221 ++++++++--------
 8 files changed, 755 insertions(+), 132 deletions(-)

codex
検証中に `HEAD` が `a9019c7` へ進んでいることを確認しました。指定範囲は `66e2aeb..e2a1a39` として扱い、Phase 3-L 相談だけは新しい `a9019c7` の実体も分けて反映します。
hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git status --short --branch' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-WvnIxRBv' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-hwOmnODp' (errno=Operation not permitted)
## roku/phase3j-timeline
?? docs/

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git diff --name-only e2a1a39..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-L0k7auwu' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-7oTdV3pu' (errno=Operation not permitted)
template/scripts/build_slide_data.py
template/scripts/build_telop_data.py
template/scripts/test_timeline_integration.py
template/scripts/timeline.py

exec
/bin/zsh -lc 'git show --stat --oneline --decorate --no-renames a9019c7' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-E5GprCDS' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-lPPyYe0U' (errno=Operation not permitted)
a9019c7 (HEAD -> roku/phase3j-timeline) feat(timeline): require_timing strict mode + validate_transcript_segments helper (Phase 3-L core)
 template/scripts/build_slide_data.py          |  7 ++---
 template/scripts/build_telop_data.py          |  4 ++-
 template/scripts/test_timeline_integration.py | 34 ++++++++++++++++++++++++
 template/scripts/timeline.py                  | 37 +++++++++++++++++++++++++--
 4 files changed, 76 insertions(+), 6 deletions(-)

exec
/bin/zsh -lc 'git diff --unified=80 e2a1a39..HEAD -- template/scripts/timeline.py template/scripts/build_slide_data.py template/scripts/build_telop_data.py template/scripts/test_timeline_integration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-86cTvyAn' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ZahM3Ajp' (errno=Operation not permitted)
diff --git a/template/scripts/build_slide_data.py b/template/scripts/build_slide_data.py
index 1a7c97f..e8860e5 100644
--- a/template/scripts/build_slide_data.py
+++ b/template/scripts/build_slide_data.py
@@ -249,143 +249,144 @@ def validate_slide_plan(plan: dict, words: list[dict], cut_total_frames: int | N
             continue
         if sw <= last_end_idx:
             errors.append(f"slides[{i}] word range overlaps previous (sw={sw} <= prev end {last_end_idx})")
         last_end_idx = ew
         title = s.get("title")
         if not isinstance(title, str) or not title.strip():
             errors.append(f"slides[{i}].title empty")
         elif len(title) > title_max:
             errors.append(f"slides[{i}].title too long ({len(title)} > {title_max})")
         bullets = s.get("bullets") or []
         if not isinstance(bullets, list) or len(bullets) > MAX_BULLETS_PER_SLIDE:
             errors.append(f"slides[{i}].bullets exceeds {MAX_BULLETS_PER_SLIDE}")
         else:
             for j, b in enumerate(bullets):
                 bt = b.get("text") if isinstance(b, dict) else None
                 if not isinstance(bt, str) or not bt.strip():
                     errors.append(f"slides[{i}].bullets[{j}] empty text")
                 elif len(bt) > bullet_max:
                     errors.append(f"slides[{i}].bullets[{j}] too long ({len(bt)} > {bullet_max})")
         align = s.get("align")
         if align is not None and align not in ALLOWED_ALIGN:
             errors.append(f"slides[{i}].align invalid ({align})")
         video_layer = s.get("videoLayer")
         if video_layer is not None and video_layer not in ALLOWED_VIDEO_LAYER:
             errors.append(f"slides[{i}].videoLayer invalid ({video_layer})")
     return errors
 
 
 def build_slides_from_plan(plan: dict, words: list[dict], cut_segments: list[dict],
                            fmt: str, tone: str) -> list[dict]:
     """validated plan を SlideSegment dict 列に変換 (frame は script 側で計算)."""
     style = style_for_tone(tone)
     cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
     slides: list[dict] = []
     for s in plan["slides"]:
         sw = s["startWordIndex"]
         ew = s["endWordIndex"]
         ms_start = words[sw].get("start", 0)
         ms_end = words[ew].get("end", 0)
         pb_start = ms_to_playback_frame(ms_start, cut_segments)
         pb_end = ms_to_playback_frame(ms_end, cut_segments)
         if pb_start is None or pb_end is None or pb_end <= pb_start:
             continue
         if cut_total is not None:
             pb_end = min(pb_end, cut_total)
         slides.append({
             "id": s["id"],
             "startFrame": pb_start,
             "endFrame": pb_end,
             "title": s["title"],
             "subtitle": s.get("subtitle"),
             "bullets": s.get("bullets") or None,
             "align": s.get("align") or style["align"],
             "backgroundColor": s.get("backgroundColor") or style["bg"],
             "videoLayer": s.get("videoLayer") or "visible",
         })
     return slides
 
 
 def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--mode", choices=["topic", "segment"], default="topic")
     ap.add_argument("--plan", help="optional slide_plan.json (LLM 生成)")
     ap.add_argument("--strict-plan", action="store_true",
                     help="--plan の validate 失敗時に exit 2 (default は warning + deterministic fallback)")
     args = ap.parse_args()
 
     transcript_path = PROJ / "transcript_fixed.json"
     config_path = PROJ / "project-config.json"
     if not transcript_path.exists() or not config_path.exists():
         raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
 
     transcript = load_json(transcript_path)
     config = load_json(config_path)
     fmt = config.get("format", "short")
     tone = config.get("tone", "プロフェッショナル")
     segments = transcript.get("segments", [])
     words = transcript.get("words", [])
 
     # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_slide_data でも
-    # transcript の壊れたデータを早期検出 (start>end / 型不正)。voicevox_narration
-    # と同じ validate_transcript_segment を経由。
+    # transcript の壊れたデータを早期検出 (start>end / 型不正)。
+    # Phase 3-L: require_timing=True で start/end 必須化 (slide は timing 駆動、
+    # ms_to_playback_frame 呼出箇所 4 件すべてで start/end を使用するため)。
     for i, seg in enumerate(segments):
         try:
-            validate_transcript_segment(seg, idx=i)
+            validate_transcript_segment(seg, idx=i, require_timing=True)
         except TranscriptSegmentError as e:
             raise SystemExit(f"transcript validation failed: {e}")
 
     vad_path = PROJ / "vad_result.json"
     vad = load_json(vad_path) if vad_path.exists() else None
     cut_segments = build_cut_segments_from_vad(vad)
     cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else None
 
     used_plan = False
     if args.plan:
         plan_path = Path(args.plan)
         if not plan_path.exists():
             msg = f"--plan path not found: {plan_path}"
             if args.strict_plan:
                 raise SystemExit(msg)
             print(f"WARN: {msg} → deterministic fallback")
         else:
             plan = load_json(plan_path)
             errors = validate_slide_plan(plan, words, cut_total_frames, fmt)
             if errors:
                 if args.strict_plan:
                     print("ERROR: plan validation failed:")
                     for e in errors:
                         print(f"  - {e}")
                     raise SystemExit(2)
                 print("WARN: plan validation failed, deterministic fallback:")
                 for e in errors:
                     print(f"  - {e}")
             else:
                 slides = build_slides_from_plan(plan, words, cut_segments, fmt, tone)
                 used_plan = True
                 print(f"=== plan accepted ({len(plan.get('slides', []))} slides) ===")
 
     if not used_plan:
         if args.mode == "topic":
             slides = build_slides_topic_mode(segments, cut_segments, fmt, tone)
         else:
             slides = build_slides_segment_mode(segments, cut_segments, fmt, tone)
 
     out_path = PROJ / "src" / "Slides" / "slideData.ts"
     backup = PROJ / "src" / "Slides" / "slideData.backup.ts"
     if out_path.exists() and not backup.exists():
         backup.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")
     ts = render_slide_data_ts(slides)
     out_path.write_text(ts, encoding="utf-8")
 
     mode_label = "plan" if used_plan else f"deterministic-{args.mode}"
     print(f"=== slideData.ts 生成 (mode={mode_label}) ===")
     print(f"path: {out_path}")
     print(f"input segments: {len(segments)}")
     print(f"output slides: {len(slides)}")
     for s in slides:
         bullets_count = len(s.get("bullets") or [])
         print(f"  [{s['id']:2}] f{s['startFrame']:5}-{s['endFrame']:5} '{s['title']}' (bullets={bullets_count})")
 
 
 if __name__ == "__main__":
     main()
diff --git a/template/scripts/build_telop_data.py b/template/scripts/build_telop_data.py
index 44ce561..88e28f0 100644
--- a/template/scripts/build_telop_data.py
+++ b/template/scripts/build_telop_data.py
@@ -220,163 +220,165 @@ def call_budoux(seg_texts: list[str]) -> list[list[str]]:
     payload = {"segments": [{"id": i, "text": t} for i, t in enumerate(seg_texts)]}
     with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fin:
         json.dump(payload, fin, ensure_ascii=False)
         fin_path = fin.name
     fout_path = fin_path.replace(".json", "_out.json")
     script = proj / "scripts" / "budoux_split.mjs"
     if not script.exists():
         raise FileNotFoundError(f"budoux_split.mjs not found at {script}")
     res = subprocess.run(
         ["node", str(script), "--in", fin_path, "--out", fout_path],
         cwd=str(proj),
         capture_output=True,
         text=True,
     )
     if res.returncode != 0:
         raise RuntimeError(f"budoux_split.mjs failed: {res.stderr}")
     out = json.loads(Path(fout_path).read_text(encoding="utf-8"))
     return [s.get("phrases", []) for s in out["segments"]]
 
 
 # ---------------- VAD / cut ----------------
 def build_cut_segments_from_vad(vad):
     """vad の speech_segments から cut timeline 構築 (Phase 3-K: validate 経由).
 
     Codex Phase 3-J review P2 #2 反映: build_slide_data / voicevox_narration と
     同じ validate_vad_schema を経由して、3 script で壊れた VAD の扱いを揃える。
     """
     validate_vad_schema(vad)
     speech = vad["speech_segments"]
     out = []
     cursor_ms = 0
     for i, seg in enumerate(speech):
         s_ms = seg["start"]
         e_ms = seg["end"]
         dur_ms = e_ms - s_ms
         out.append({
             "id": i + 1,
             "originalStartMs": s_ms,
             "originalEndMs": e_ms,
             "playbackStart": round(cursor_ms / 1000 * FPS),
             "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
         })
         cursor_ms += dur_ms
     return out
 
 
 def find_cut_segment_for_ms(ms, cut_segments):
     for cs in cut_segments:
         if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
             return cs
     return None
 
 
 def ms_to_playback_frame(ms, cut_segments):
     cs = find_cut_segment_for_ms(ms, cut_segments)
     if not cs:
         return None
     offset_ms = ms - cs["originalStartMs"]
     return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
 
 
 # ---------------- 本体 ----------------
 def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--baseline", action="store_true", help="BudouX を使わず Phase 1 旧ロジックで生成")
     args = ap.parse_args()
 
     transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
     vad = json.loads((PROJ / "vad_result.json").read_text(encoding="utf-8"))
     typo = (PROJ / "typo_dict.json")
     typo_dict = json.loads(typo.read_text(encoding="utf-8")) if typo.exists() else {}
     preserve = typo_dict.get("preserve", [])
     cut_segments = build_cut_segments_from_vad(vad)
     cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else 0
 
     words = transcript["words"]
     segments = transcript["segments"]
 
     # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_telop でも transcript
     # 壊れたデータを早期検出。
+    # Phase 3-L: require_timing=True で start/end 必須化 (telop は ms→frame
+    # 変換で start/end を必須使用するため)。
     for i, seg in enumerate(segments):
         try:
-            validate_transcript_segment(seg, idx=i)
+            validate_transcript_segment(seg, idx=i, require_timing=True)
         except TranscriptSegmentError as e:
             raise SystemExit(f"transcript validation failed: {e}")
 
     # 分割 phase: BudouX 呼出 (一括)
     seg_parts: list[list[str]] = []
     seg_parts_phrases: list[list[list[str]]] = []  # part 毎の phrase リスト (insert_linebreak で使用)
     if args.baseline:
         for s in segments:
             parts = split_segment_text_legacy(s["text"], MAX_CHARS)
             seg_parts.append(parts)
             seg_parts_phrases.append([[] for _ in parts])  # baseline は phrase なし
     else:
         try:
             phrases_list = call_budoux([s["text"] for s in segments])
             for i, s in enumerate(segments):
                 parts, parts_phrases = split_segment_text_budoux(s["text"], phrases_list[i], MAX_CHARS)
                 seg_parts.append(parts)
                 seg_parts_phrases.append(parts_phrases)
         except Exception as e:
             print(f"WARN: BudouX 失敗 → legacy fallback: {e}")
             for s in segments:
                 parts = split_segment_text_legacy(s["text"], MAX_CHARS)
                 seg_parts.append(parts)
                 seg_parts_phrases.append([[] for _ in parts])
 
     telop_segments = []
     weaknesses = []
     telop_id = 1
 
     for seg_idx, (seg, parts, parts_phrases) in enumerate(zip(segments, seg_parts, seg_parts_phrases)):
         if not parts:
             continue
         # 1-2 字を直前にマージ (文末「す」等の単独 telop 抑制)、phrases も追従
         merged: list[str] = []
         merged_phrases: list[list[str]] = []
         for p_idx, p in enumerate(parts):
             ph = parts_phrases[p_idx] if p_idx < len(parts_phrases) else []
             if merged and len(p) <= 2:
                 merged[-1] = merged[-1] + p
                 merged_phrases[-1] = (merged_phrases[-1] or []) + ph
             else:
                 merged.append(p)
                 merged_phrases.append(ph)
         parts = merged
         parts_phrases = merged_phrases
 
         seg_total_chars = sum(len(p) for p in parts)
         cum_chars = 0
         for p_idx, part_text in enumerate(parts):
             part_phrases = parts_phrases[p_idx] if p_idx < len(parts_phrases) else []
             part_chars = len(part_text)
             ratio_start = cum_chars / max(seg_total_chars, 1)
             ratio_end = (cum_chars + part_chars) / max(seg_total_chars, 1)
             seg_dur_ms = seg["end"] - seg["start"]
             ms_start = seg["start"] + round(seg_dur_ms * ratio_start)
             ms_end = seg["start"] + round(seg_dur_ms * ratio_end)
 
             # cut 境界またぎ防止
             cs_start = find_cut_segment_for_ms(ms_start, cut_segments)
             cs_end = find_cut_segment_for_ms(ms_end, cut_segments)
             if cs_start and cs_end and cs_start is not cs_end:
                 ms_end = cs_start["originalEndMs"]
                 weaknesses.append({"type": "telop_cut_boundary_clamp", "telop_text": part_text})
 
             pb_start = ms_to_playback_frame(ms_start, cut_segments)
             pb_end = ms_to_playback_frame(ms_end, cut_segments)
             if pb_start is None or pb_end is None:
                 fallback = next((cs for cs in cut_segments if ms_start <= cs["originalEndMs"]), None)
                 if fallback:
                     pb_start = fallback["playbackStart"]
                     pb_end = min(fallback["playbackEnd"], (pb_start or 0) + MAX_DURATION_FRAMES)
                 else:
                     weaknesses.append({"type": "telop_outside_cut", "telop_text": part_text})
                     cum_chars += part_chars
                     continue
 
             duration = pb_end - pb_start
             if duration < MIN_DURATION_FRAMES:
                 pb_end = pb_start + MIN_DURATION_FRAMES
             if duration > MAX_DURATION_FRAMES:
diff --git a/template/scripts/test_timeline_integration.py b/template/scripts/test_timeline_integration.py
index 60db2fc..8a91330 100644
--- a/template/scripts/test_timeline_integration.py
+++ b/template/scripts/test_timeline_integration.py
@@ -121,160 +121,194 @@ def test_vad_schema_validation() -> None:
         "end missing",
     )
     # start > end
     assert_raises(
         lambda: timeline.validate_vad_schema(
             {"speech_segments": [{"start": 100, "end": 50}]}
         ),
         timeline.VadSchemaError,
         "start > end",
     )
     # OK
     timeline.validate_vad_schema(
         {"speech_segments": [{"start": 0, "end": 1000}]}
     )
 
 
 def test_ms_to_playback_frame() -> None:
     # No cut: 直接 ms→frame
     assert_eq(timeline.ms_to_playback_frame(0, 30, []), 0, "no-cut start")
     assert_eq(timeline.ms_to_playback_frame(1000, 30, []), 30, "no-cut 1s")
     assert_eq(timeline.ms_to_playback_frame(500, 30, []), 15, "no-cut 0.5s")
 
     # With cut: gap removed
     cut_segs = [
         {"originalStartMs": 0, "originalEndMs": 500, "playbackStart": 0, "playbackEnd": 15},
         {"originalStartMs": 1500, "originalEndMs": 3000, "playbackStart": 15, "playbackEnd": 60},
     ]
     assert_eq(timeline.ms_to_playback_frame(200, 30, cut_segs), 6, "cut seg0 200ms")
     assert_eq(timeline.ms_to_playback_frame(1500, 30, cut_segs), 15, "cut seg1 start")
     assert_eq(timeline.ms_to_playback_frame(2000, 30, cut_segs), 30, "cut seg1 +500ms")
     # 800ms: gap (excluded)
     assert_eq(timeline.ms_to_playback_frame(800, 30, cut_segs), None, "cut gap excluded")
 
 
 def test_load_cut_segments_fail_fast() -> None:
     """fail_fast=True で部分破損を raise する."""
     with tempfile.TemporaryDirectory() as tmp:
         proj = Path(tmp)
         (proj / "vad_result.json").write_text(
             json.dumps({"speech_segments": [{"start": 100}]})  # end missing
         )
         # default fail_fast=False で []
         assert_eq(timeline.load_cut_segments(proj, 30, fail_fast=False), [], "soft fail")
         # fail_fast=True で raise
         assert_raises(
             lambda: timeline.load_cut_segments(proj, 30, fail_fast=True),
             timeline.VadSchemaError,
             "fail_fast raise",
         )
 
 
 def test_transcript_segment_validation() -> None:
     """validate_transcript_segment が壊れた transcript を検出する."""
     # OK: timing なし (--script の chunk)
     timeline.validate_transcript_segment({"text": "hi"}, 0)
     # OK: 通常 transcript
     timeline.validate_transcript_segment({"text": "hi", "start": 0, "end": 1000}, 0)
     # NG: start > end
     assert_raises(
         lambda: timeline.validate_transcript_segment(
             {"text": "hi", "start": 1000, "end": 500}, 0
         ),
         timeline.TranscriptSegmentError,
         "transcript start>end",
     )
     # NG: text 非 str
     assert_raises(
         lambda: timeline.validate_transcript_segment({"text": 123}, 0),
         timeline.TranscriptSegmentError,
         "text non-str",
     )
     # NG: start 型不正
     assert_raises(
         lambda: timeline.validate_transcript_segment(
             {"text": "hi", "start": "bad"}, 0
         ),
         timeline.TranscriptSegmentError,
         "start non-numeric",
     )
 
+    # Phase 3-L (Codex Phase 3-J review Part B 推奨): require_timing=True で
+    # start/end 必須化、欠落 / None で raise。
+    assert_raises(
+        lambda: timeline.validate_transcript_segment(
+            {"text": "hi"}, 0, require_timing=True
+        ),
+        timeline.TranscriptSegmentError,
+        "require_timing missing both",
+    )
+    assert_raises(
+        lambda: timeline.validate_transcript_segment(
+            {"text": "hi", "start": 0, "end": None}, 0, require_timing=True
+        ),
+        timeline.TranscriptSegmentError,
+        "require_timing end None",
+    )
+    # OK: require_timing=True + 両方 numeric
+    timeline.validate_transcript_segment(
+        {"text": "hi", "start": 0, "end": 1000}, 0, require_timing=True
+    )
+
+    # validate_transcript_segments 一括 helper
+    out = timeline.validate_transcript_segments(
+        [{"text": "a", "start": 0, "end": 100}, {"text": "b", "start": 100, "end": 200}],
+        require_timing=True,
+    )
+    assert_eq(len(out), 2, "validate_transcript_segments OK length")
+    # 非 list で raise
+    assert_raises(
+        lambda: timeline.validate_transcript_segments("not a list"),
+        timeline.TranscriptSegmentError,
+        "validate_transcript_segments non-list",
+    )
+
 
 def test_voicevox_collect_chunks_validation() -> None:
     """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
     import voicevox_narration as vn
 
     class Args:
         script = None
         script_json = None
 
     bad = {"segments": [{"text": "hi", "start": 100, "end": 50}]}
     assert_raises(
         lambda: vn.collect_chunks(Args(), bad),
         vn.TranscriptSegmentError,
         "voicevox start>end transcript",
     )
 
     good = {"segments": [{"text": "hi", "start": 0, "end": 1000}]}
     out = vn.collect_chunks(Args(), good)
     assert_eq(len(out), 1, "voicevox good transcript len")
     assert_eq(out[0]["sourceStartMs"], 0, "voicevox sourceStartMs")
     assert_eq(out[0]["sourceEndMs"], 1000, "voicevox sourceEndMs")
 
     # Codex Phase 3-J review P2 #1 反映: validate を `.get(...).strip()` 前に通す
     # 非 dict segment → TranscriptSegmentError
     assert_raises(
         lambda: vn.collect_chunks(Args(), {"segments": ["not a dict"]}),
         vn.TranscriptSegmentError,
         "voicevox non-dict segment",
     )
     # segments 非 list → TranscriptSegmentError
     assert_raises(
         lambda: vn.collect_chunks(Args(), {"segments": "wrong"}),
         vn.TranscriptSegmentError,
         "voicevox non-list segments",
     )
     # text 非 str (int) → TranscriptSegmentError
     assert_raises(
         lambda: vn.collect_chunks(Args(), {"segments": [{"text": 123}]}),
         vn.TranscriptSegmentError,
         "voicevox text non-str",
     )
     # text=None は filter (空文字列と同じ扱い、空 list 返す)
     assert_eq(
         vn.collect_chunks(Args(), {"segments": [{"text": None, "start": 0, "end": 100}]}),
         [],
         "voicevox text=None filtered",
     )
 
 
 def test_voicevox_write_narration_data_alignment() -> None:
     """transcript timing alignment が cut-aware で正しく動く end-to-end."""
     import voicevox_narration as vn
 
     with tempfile.TemporaryDirectory() as tmp:
         proj = Path(tmp)
         vn.PROJ = proj
         vn.NARRATION_DIR = proj / "public" / "narration"
         vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
         vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
         vn.NARRATION_DIR.mkdir(parents=True)
         vn.NARRATION_DATA_TS.parent.mkdir(parents=True)
 
         write_synthetic_wav(vn.NARRATION_DIR / "chunk_000.wav", 1.0)
         write_synthetic_wav(vn.NARRATION_DIR / "chunk_001.wav", 0.5)
 
         # No cut, transcript timing 0ms と 1000ms
         chunks_data = [
             (vn.NARRATION_DIR / "chunk_000.wav", "first", 0, 1000),
             (vn.NARRATION_DIR / "chunk_001.wav", "second", 1000, 1500),
         ]
         segments, ts_path, meta_path = vn.write_narration_data(chunks_data, 30, [])
         assert_eq(segments[0]["startFrame"], 0, "chunk0 startFrame")
         assert_eq(segments[0]["durationInFrames"], 30, "chunk0 dur")
         assert_eq(segments[0]["timing_source"], "transcript_aligned", "chunk0 source")
         assert_eq(segments[1]["startFrame"], 30, "chunk1 startFrame (1000ms*30fps)")
 
         # Verify TS file is valid
         ts = ts_path.read_text(encoding="utf-8")
         assert "narrationData" in ts
         assert "sourceStartMs: 0" in ts
diff --git a/template/scripts/timeline.py b/template/scripts/timeline.py
index bc8b8e0..d85e2ec 100644
--- a/template/scripts/timeline.py
+++ b/template/scripts/timeline.py
@@ -78,104 +78,137 @@ def validate_vad_schema(vad: object) -> dict:
                 )
         if seg["start"] > seg["end"]:
             raise VadSchemaError(
                 f"segment[{i}] start={seg['start']} > end={seg['end']}"
             )
     return vad
 
 
 def build_cut_segments_from_vad(vad: dict, fps: int) -> list[dict]:
     """vad の speech_segments から cut 後 timeline mapping を構築.
 
     呼び出し前に validate_vad_schema() で検査済みであることを前提とする。
     fps は呼び出し側の videoConfig.FPS を渡す (Phase 3-J: hardcode 撤廃)。
     """
     out: list[dict] = []
     cursor_ms = 0
     for i, seg in enumerate(vad["speech_segments"]):
         s_ms = seg["start"]
         e_ms = seg["end"]
         dur_ms = e_ms - s_ms
         out.append(
             {
                 "id": i + 1,
                 "originalStartMs": s_ms,
                 "originalEndMs": e_ms,
                 "playbackStart": round(cursor_ms / 1000 * fps),
                 "playbackEnd": round((cursor_ms + dur_ms) / 1000 * fps),
             }
         )
         cursor_ms += dur_ms
     return out
 
 
 def load_cut_segments(proj: Path, fps: int, fail_fast: bool = False) -> list[dict]:
     """`<proj>/vad_result.json` から cut_segments を構築.
 
     fail_fast=False (default): 不在 / I/O / schema エラーは [] にして黙過。
     fail_fast=True: 部分破損も VadSchemaError / OSError で raise。
 
     Codex Phase 3-I review P1 #2 反映: 黙過は legacy 経路へ流れて stale
     narration を出す危険があるので、narration script では fail_fast=True 推奨。
     """
     vad_path = proj / "vad_result.json"
     if not vad_path.exists():
         return []
     try:
         with vad_path.open("r", encoding="utf-8") as f:
             data = json.load(f)
     except (OSError, json.JSONDecodeError) as e:
         if fail_fast:
             raise
         return []
     try:
         validated = validate_vad_schema(data)
     except VadSchemaError:
         if fail_fast:
             raise
         return []
     return build_cut_segments_from_vad(validated, fps)
 
 
 def ms_to_playback_frame(ms: int, fps: int, cut_segments: list[dict]) -> int | None:
     """元動画の ms を playback frame に変換 (cut-aware).
 
     cut_segments が空なら直接変換。ms が cut 範囲外 (cut で除外された箇所) は
     None を返す (呼出側が累積 fallback or skip 判断)。
     """
     if not cut_segments:
         return round(ms / 1000 * fps)
     for cs in cut_segments:
         if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
             offset_ms = ms - cs["originalStartMs"]
             return cs["playbackStart"] + round(offset_ms / 1000 * fps)
     return None
 
 
 class TranscriptSegmentError(ValueError):
     """transcript segment の型 / 順序 異常 (Codex P2 #3 反映)."""
 
 
-def validate_transcript_segment(seg: object, idx: int = -1) -> dict:
+def validate_transcript_segment(
+    seg: object, idx: int = -1, require_timing: bool = False
+) -> dict:
     """transcript_fixed.json の 1 segment の最低限検査.
 
-    必須: dict に `text` (str)、`start` / `end` が int|float|None。start/end
+    必須: dict に `text` (str|None)、`start` / `end` が int|float|None。
     両方 numeric なら start <= end。違反は TranscriptSegmentError。
+
+    require_timing=True: start / end の両方が int|float 必須 (None / 欠落 NG)。
+    build_slide_data / build_telop_data など timing 駆動の script で使う
+    (Codex Phase 3-J review Part B 設計概要 反映)。
     """
     label = f"segment[{idx}]" if idx >= 0 else "segment"
     if not isinstance(seg, dict):
         raise TranscriptSegmentError(f"{label} must be dict, got {type(seg).__name__}")
     text = seg.get("text")
     if text is not None and not isinstance(text, str):
         raise TranscriptSegmentError(
             f"{label}.text must be str|None, got {type(text).__name__}"
         )
     s = seg.get("start")
     e = seg.get("end")
     for k, v in (("start", s), ("end", e)):
         if v is not None and not isinstance(v, (int, float)):
             raise TranscriptSegmentError(
                 f"{label}.{k} must be int|float|None, got {type(v).__name__}"
             )
+    if require_timing:
+        if not isinstance(s, (int, float)):
+            raise TranscriptSegmentError(
+                f"{label}.start required (int|float), got {type(s).__name__}"
+            )
+        if not isinstance(e, (int, float)):
+            raise TranscriptSegmentError(
+                f"{label}.end required (int|float), got {type(e).__name__}"
+            )
     if isinstance(s, (int, float)) and isinstance(e, (int, float)) and s > e:
         raise TranscriptSegmentError(f"{label} start={s} > end={e}")
     return seg
+
+
+def validate_transcript_segments(
+    segments: object, require_timing: bool = False
+) -> list[dict]:
+    """segments[] 一括検証 (Codex Phase 3-J review Part B 推奨).
+
+    segments が list でない / 各要素が validate に通らない場合 raise。
+    require_timing=True で start/end 必須の strict mode (slide / telop 用)。
+    """
+    if not isinstance(segments, list):
+        raise TranscriptSegmentError(
+            f"segments must be list, got {type(segments).__name__}"
+        )
+    return [
+        validate_transcript_segment(seg, idx=i, require_timing=require_timing)
+        for i, seg in enumerate(segments)
+    ]

指定4 commitに加え、検証途中で追加された a9019c7 は Phase 3-L 相談にだけ別扱いで反映します。
  ✓ ブランチ差分と対象ファイルを確認
  → Part A checklist をコードとテストで検証
  • Phase 3-L 候補を根拠付きで比較
  • 短い結論と review 重点項目を提示
web search: 
web search: Remotion watchStaticFile hook documentation
web search: 
web search: https://www.remotion.dev/docs/getstaticfiles
web search: 
web search: https://www.remotion.dev/docs/watchstaticfile
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "test -d template/node_modules; printf 'node_modules_exists=%s\\n' "'$?' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'nl -ba template/tsconfig.json' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	{
     2	  "compilerOptions": {
     3	    "target": "ES2018",
     4	    "module": "commonjs",
     5	    "jsx": "react-jsx",
     6	    "strict": true,
     7	    "noEmit": true,
     8	    "lib": ["es2015"],
     9	    "esModuleInterop": true,
    10	    "skipLibCheck": true,
    11	    "forceConsistentCasingInFileNames": true,
    12	    "noUnusedLocals": true
    13	  },
    14	  "exclude": ["remotion.config.ts"]
    15	}

 succeeded in 0ms:
node_modules_exists=1

exec
/bin/zsh -lc "test -f template/transcript_fixed.json; printf 'transcript_exists=%s\\n' "'$?; test -f template/vad_result.json; printf '"'vad_exists=%s\\n' "'$?; test -f template/main.mp4; printf '"'main_mp4_exists=%s\\n' "'$?; test -f template/public/main.mp4; printf '"'public_main_mp4_exists=%s\\n' "'$?' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
transcript_exists=1
vad_exists=1
main_mp4_exists=1
public_main_mp4_exists=1

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba skills/supermovie-narration/SKILL.md | sed -n '148,160p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   148	| engine 不在 | INFO ログ + exit 0 (skip)、`--require-engine` 時のみ exit 4 |
   149	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
   150	| `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
   151	| WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |
   152	| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk + 旧 narration.wav 全削除、narrationData.ts 空 array (all-or-nothing) |
   153	| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
   154	| FPS 不正 (--fps <= 0 / videoConfig.ts FPS regex 失敗) | exit 4 (前者) or default 30 fallback (後者) |
   155	| stale narration.wav 削除失敗 (StaleCleanupError) | exit 7 (Codex Phase 3-H re-review P1 #2 partial 反映、stale legacy 再生事故防止) |
   156	| transcript validation 失敗 (TranscriptSegmentError) | exit 3 (start>end / 型不正 / 非 dict、collect_chunks で early raise、Codex Phase 3-I review P2 #3 反映) |
   157	| vad_result.json 部分破損 (VadSchemaError / OSError / JSONDecodeError) | exit 8 (synthesis 前に fail-fast、stale legacy が legacy mode へ流れる事故防止、Codex Phase 3-I review P1 #2 + Phase 3-J review P1 反映で synthesis 前に validation 移動済) |
   158	
   159	## 連携マップ
   160	

exec
/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '389,463p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   389	def collect_chunks(args, transcript: dict) -> list[dict]:
   390	    """各 chunk を {text, sourceStartMs, sourceEndMs} で返す.
   391	
   392	    Phase 3-I: transcript_fixed.json の segments[].start/end を保持。
   393	    Phase 3-J: validate_transcript_segment で start > end / 型不正を検出して
   394	    TranscriptSegmentError raise (Codex review P2 #3 反映、mlx-whisper の
   395	    稀なバグや手編集ミスによる壊れた transcript を早期検出)。
   396	    --script は 1 行 1 chunk で timing なし、--script-json は startMs/endMs
   397	    optional で受け付ける。
   398	    """
   399	    if args.script:
   400	        text = _resolve_path(args.script).read_text(encoding="utf-8")
   401	        return [
   402	            {"text": line.strip(), "sourceStartMs": None, "sourceEndMs": None}
   403	            for line in text.splitlines() if line.strip()
   404	        ]
   405	    # Codex Phase 3-J review P2 #1 反映: validate を `.get(...).strip()` より
   406	    # 先に通す。segment が非 dict / text 非 str だと AttributeError で落ちて
   407	    # TranscriptSegmentError として捕まらない経路があるため。
   408	    if args.script_json:
   409	        plan = load_json(_resolve_path(args.script_json))
   410	        if not isinstance(plan, dict):
   411	            raise TranscriptSegmentError(f"script-json must be dict, got {type(plan).__name__}")
   412	        plan_segments = plan.get("segments", [])
   413	        if not isinstance(plan_segments, list):
   414	            raise TranscriptSegmentError(
   415	                f"script-json segments must be list, got {type(plan_segments).__name__}"
   416	            )
   417	        out: list[dict] = []
   418	        for i, s in enumerate(plan_segments):
   419	            # validate を最初に通す (segment が非 dict なら raise)
   420	            validate_transcript_segment(
   421	                # script-json schema は startMs/endMs だが、validate は start/end を見るので map
   422	                (
   423	                    {
   424	                        "text": s.get("text"),
   425	                        "start": s.get("startMs"),
   426	                        "end": s.get("endMs"),
   427	                    }
   428	                    if isinstance(s, dict)
   429	                    else s
   430	                ),
   431	                idx=i,
   432	            )
   433	            text = (s.get("text") or "").strip()
   434	            if not text:
   435	                continue
   436	            out.append(
   437	                {
   438	                    "text": text,
   439	                    "sourceStartMs": s.get("startMs"),
   440	                    "sourceEndMs": s.get("endMs"),
   441	                }
   442	            )
   443	        return out
   444	    transcript_segments = transcript.get("segments", []) if isinstance(transcript, dict) else []
   445	    if not isinstance(transcript_segments, list):
   446	        raise TranscriptSegmentError(
   447	            f"transcript segments must be list, got {type(transcript_segments).__name__}"
   448	        )
   449	    out_t: list[dict] = []
   450	    for i, s in enumerate(transcript_segments):
   451	        # validate を最初に通す
   452	        validate_transcript_segment(s, idx=i)
   453	        text = (s.get("text") or "").strip()
   454	        if not text:
   455	            continue
   456	        out_t.append(
   457	            {
   458	                "text": text,
   459	                "sourceStartMs": s.get("start"),
   460	                "sourceEndMs": s.get("end"),
   461	            }
   462	        )
   463	    return out_t

exec
/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '531,612p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   531	    # Phase 3-H: stale narration を全 reset BEFORE synthesis
   532	    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
   533	    try:
   534	        cleanup_stale_all()
   535	    except StaleCleanupError as e:
   536	        print(f"ERROR: {e}", file=sys.stderr)
   537	        return 7
   538	    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
   539	
   540	    # Codex Phase 3-J review P1 反映: VAD validation を synthesis 前 (cleanup 直後)
   541	    # に移動。VAD 破損時に synthesize / concat / narrationData 全 skip し、
   542	    # cleanup 直後の clean 状態で exit (stale narration.wav が legacy 経路に流れる
   543	    # 余地を完全に消す)。
   544	    try:
   545	        cut_segments = project_load_cut_segments(fps)
   546	    except (VadSchemaError, OSError, json.JSONDecodeError) as e:
   547	        print(
   548	            f"ERROR: vad_result.json schema invalid or unreadable: {e}",
   549	            file=sys.stderr,
   550	        )
   551	        # cleanup_stale_all() 直後で何も書いていない、追加 rollback 不要
   552	        return 8
   553	    if cut_segments:
   554	        print(f"cut-aware mapping: {len(cut_segments)} cut segments loaded from vad_result.json")
   555	
   556	    chunk_paths: list[Path] = []
   557	    chunk_meta: list[tuple[str, int | None, int | None]] = []  # (text, sourceStartMs, sourceEndMs)
   558	    for i, ch in enumerate(chunks):
   559	        text = ch["text"]
   560	        try:
   561	            wav_bytes = synthesize(text, args.speaker)
   562	        except (urllib.error.HTTPError, urllib.error.URLError) as e:
   563	            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
   564	            continue
   565	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
   566	        atomic_write_bytes(p, wav_bytes)
   567	        chunk_paths.append(p)
   568	        chunk_meta.append((text, ch.get("sourceStartMs"), ch.get("sourceEndMs")))
   569	        print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
   570	
   571	    if not chunk_paths:
   572	        print("ERROR: no chunks succeeded", file=sys.stderr)
   573	        return 5
   574	    if not args.allow_partial and len(chunk_paths) < len(chunks):
   575	        print(
   576	            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
   577	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
   578	            file=sys.stderr,
   579	        )
   580	        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
   581	        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
   582	        for p in chunk_paths:
   583	            try:
   584	                p.unlink()
   585	            except OSError:
   586	                pass
   587	        return 6
   588	
   589	    out_path = _resolve_path(args.output)
   590	    try:
   591	        concat_wavs_atomic(chunk_paths, out_path)
   592	    except (wave.Error, EOFError) as e:
   593	        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
   594	        for p in chunk_paths:
   595	            try:
   596	                p.unlink()
   597	            except OSError:
   598	                pass
   599	        return 6
   600	    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
   601	    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
   602	
   603	    # Phase 3-H/I: chunk metadata + narrationData.ts (atomic、最後に書く)
   604	    # cut_segments は synthesis 前 (Codex Phase 3-J review P1) で取得済み
   605	
   606	    # Codex Phase 3-I review P3 #6 反映: chunk_paths と chunk_meta の長さ ガード
   607	    # python -O で assert は消えるため、runtime check + raise 化
   608	    # (Codex Phase 3-J review checklist 指摘)。
   609	    if len(chunk_paths) != len(chunk_meta):
   610	        raise RuntimeError(
   611	            f"chunk_paths ({len(chunk_paths)}) と chunk_meta ({len(chunk_meta)}) の長さズレ"
   612	        )

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/build_slide_data.py | sed -n '328,341p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   328	    # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_slide_data でも
   329	    # transcript の壊れたデータを早期検出 (start>end / 型不正)。
   330	    # Phase 3-L: require_timing=True で start/end 必須化 (slide は timing 駆動、
   331	    # ms_to_playback_frame 呼出箇所 4 件すべてで start/end を使用するため)。
   332	    for i, seg in enumerate(segments):
   333	        try:
   334	            validate_transcript_segment(seg, idx=i, require_timing=True)
   335	        except TranscriptSegmentError as e:
   336	            raise SystemExit(f"transcript validation failed: {e}")
   337	
   338	    vad_path = PROJ / "vad_result.json"
   339	    vad = load_json(vad_path) if vad_path.exists() else None
   340	    cut_segments = build_cut_segments_from_vad(vad)
   341	    cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else None

exec
/bin/zsh -lc "nl -ba template/scripts/build_telop_data.py | sed -n '240,307p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   240	# ---------------- VAD / cut ----------------
   241	def build_cut_segments_from_vad(vad):
   242	    """vad の speech_segments から cut timeline 構築 (Phase 3-K: validate 経由).
   243	
   244	    Codex Phase 3-J review P2 #2 反映: build_slide_data / voicevox_narration と
   245	    同じ validate_vad_schema を経由して、3 script で壊れた VAD の扱いを揃える。
   246	    """
   247	    validate_vad_schema(vad)
   248	    speech = vad["speech_segments"]
   249	    out = []
   250	    cursor_ms = 0
   251	    for i, seg in enumerate(speech):
   252	        s_ms = seg["start"]
   253	        e_ms = seg["end"]
   254	        dur_ms = e_ms - s_ms
   255	        out.append({
   256	            "id": i + 1,
   257	            "originalStartMs": s_ms,
   258	            "originalEndMs": e_ms,
   259	            "playbackStart": round(cursor_ms / 1000 * FPS),
   260	            "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
   261	        })
   262	        cursor_ms += dur_ms
   263	    return out
   264	
   265	
   266	def find_cut_segment_for_ms(ms, cut_segments):
   267	    for cs in cut_segments:
   268	        if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
   269	            return cs
   270	    return None
   271	
   272	
   273	def ms_to_playback_frame(ms, cut_segments):
   274	    cs = find_cut_segment_for_ms(ms, cut_segments)
   275	    if not cs:
   276	        return None
   277	    offset_ms = ms - cs["originalStartMs"]
   278	    return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
   279	
   280	
   281	# ---------------- 本体 ----------------
   282	def main():
   283	    ap = argparse.ArgumentParser()
   284	    ap.add_argument("--baseline", action="store_true", help="BudouX を使わず Phase 1 旧ロジックで生成")
   285	    args = ap.parse_args()
   286	
   287	    transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
   288	    vad = json.loads((PROJ / "vad_result.json").read_text(encoding="utf-8"))
   289	    typo = (PROJ / "typo_dict.json")
   290	    typo_dict = json.loads(typo.read_text(encoding="utf-8")) if typo.exists() else {}
   291	    preserve = typo_dict.get("preserve", [])
   292	    cut_segments = build_cut_segments_from_vad(vad)
   293	    cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else 0
   294	
   295	    words = transcript["words"]
   296	    segments = transcript["segments"]
   297	
   298	    # Phase 3-K (Codex Phase 3-I review P2 #3 拡張): build_telop でも transcript
   299	    # 壊れたデータを早期検出。
   300	    # Phase 3-L: require_timing=True で start/end 必須化 (telop は ms→frame
   301	    # 変換で start/end を必須使用するため)。
   302	    for i, seg in enumerate(segments):
   303	        try:
   304	            validate_transcript_segment(seg, idx=i, require_timing=True)
   305	        except TranscriptSegmentError as e:
   306	            raise SystemExit(f"transcript validation failed: {e}")
   307	

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "if [ -d template/public/narration ]; then printf 'template/public/narration: exists\\n'; else printf 'template/public/narration: missing\\n'; fi; if [ -d template/public ]; then printf 'template/public: exists\\n'; else printf 'template/public: missing\\n'; fi; if [ -d template/node_modules ]; then printf 'template/node_modules: exists\\n'; else printf 'template/node_modules: missing\\n'; fi; if [ -f template/public/main.mp4 ]; then printf 'template/public/main.mp4: exists\\n'; else printf 'template/public/main.mp4: missing\\n'; fi" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
template/public/narration: missing
template/public: missing
template/node_modules: missing
template/public/main.mp4: missing

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/test_timeline_integration.py | sed -n '284,315p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   284	def test_voicevox_write_narration_data_alignment() -> None:
   285	    """transcript timing alignment が cut-aware で正しく動く end-to-end."""
   286	    import voicevox_narration as vn
   287	
   288	    with tempfile.TemporaryDirectory() as tmp:
   289	        proj = Path(tmp)
   290	        vn.PROJ = proj
   291	        vn.NARRATION_DIR = proj / "public" / "narration"
   292	        vn.NARRATION_DATA_TS = proj / "src" / "Narration" / "narrationData.ts"
   293	        vn.CHUNK_META_JSON = vn.NARRATION_DIR / "chunk_meta.json"
   294	        vn.NARRATION_DIR.mkdir(parents=True)
   295	        vn.NARRATION_DATA_TS.parent.mkdir(parents=True)
   296	
   297	        write_synthetic_wav(vn.NARRATION_DIR / "chunk_000.wav", 1.0)
   298	        write_synthetic_wav(vn.NARRATION_DIR / "chunk_001.wav", 0.5)
   299	
   300	        # No cut, transcript timing 0ms と 1000ms
   301	        chunks_data = [
   302	            (vn.NARRATION_DIR / "chunk_000.wav", "first", 0, 1000),
   303	            (vn.NARRATION_DIR / "chunk_001.wav", "second", 1000, 1500),
   304	        ]
   305	        segments, ts_path, meta_path = vn.write_narration_data(chunks_data, 30, [])
   306	        assert_eq(segments[0]["startFrame"], 0, "chunk0 startFrame")
   307	        assert_eq(segments[0]["durationInFrames"], 30, "chunk0 dur")
   308	        assert_eq(segments[0]["timing_source"], "transcript_aligned", "chunk0 source")
   309	        assert_eq(segments[1]["startFrame"], 30, "chunk1 startFrame (1000ms*30fps)")
   310	
   311	        # Verify TS file is valid
   312	        ts = ts_path.read_text(encoding="utf-8")
   313	        assert "narrationData" in ts
   314	        assert "sourceStartMs: 0" in ts
   315	        assert "sourceStartMs: 1000" in ts

exec
/bin/zsh -lc 'rg -n "import build_slide|import build_telop|import generate_slide|build_slide_data|build_telop_data|generate_slide_plan|voicevox_narration" template/scripts/test_timeline_integration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
4:template/scripts/timeline.py + 3 script (voicevox_narration / build_slide_data /
5:build_telop_data) の連鎖が破損していないか、engine / node_modules 不要で
237:    """voicevox_narration.collect_chunks が壊れた transcript で raise する."""
238:    import voicevox_narration as vn
286:    import voicevox_narration as vn

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/test_timeline_integration.py | sed -n '315,335p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   315	        assert "sourceStartMs: 1000" in ts
   316	
   317	
   318	def main() -> int:
   319	    tests = [
   320	        test_fps_consistency,
   321	        test_vad_schema_validation,
   322	        test_ms_to_playback_frame,
   323	        test_load_cut_segments_fail_fast,
   324	        test_transcript_segment_validation,
   325	        test_voicevox_collect_chunks_validation,
   326	        test_voicevox_write_narration_data_alignment,
   327	    ]
   328	    failed = []
   329	    for t in tests:
   330	        name = t.__name__
   331	        try:
   332	            t()
   333	            print(f"  [OK]   {name}")
   334	        except AssertionError as e:
   335	            failed.append((name, str(e)))

主要 checklist はコード行・Bash 実測・Remotion 公式 docs で根拠取りしました。
  ✓ ブランチ差分と対象ファイルを確認
  ✓ Part A checklist をコードとテストで検証
  ✓ Phase 3-L 候補を根拠付きで比較
  → 短い結論と review 重点項目を提示
codex
**Part A**
結論: P1 は「synthesis 前 exit 8」は通るが、「何も書かず」は厳密には未達。`cleanup_stale_all()` 後、VAD 検証前に `NARRATION_DIR.mkdir()` が走るため、`template/public/narration` が無い状態では directory 作成が起きうる（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:531), Bash 実測: `code=8`, `events=cleanup,mkdir,vad`, `template/public/narration: missing`）。修正は `NARRATION_DIR.mkdir()` を `project_load_cut_segments()` 成功後へ移動。

他の 4 fix は OK:
- `collect_chunks`: `script-json` の plan dict / segments list guard が `.strip()` 前にあり、非 dict / text 非 str は `TranscriptSegmentError`（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:408), Bash 実測）。
- `build_telop` VAD: `validate_vad_schema()` 経由、main 呼び出しは 1 回（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:241), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:292)）。
- `SKILL.md`: exit 3 / exit 8 table 記載あり（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:156)）。
- `assert` は `RuntimeError` 化され、`python -O` でも消えない（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:606)）。

補足: 検証中に HEAD が `a9019c7` へ進んでおり、指定の `e2a1a39` までに加えて Phase 3-L core が入っています（Bash 実測: `git log -4`）。

**Part B**
推奨: **vi. integration_smoke を build_slide / build_telop / generate_slide_plan へ展開**。理由は、現テストは説明上 3 script 対象だが、実 import は `voicevox_narration` 寄りで、`build_slide_data` / `build_telop_data` / `generate_slide_plan` を直接叩いていないため（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:318), rg 実測）。`i` は現 HEAD では `require_timing` と一括 helper が既に入っています（[timeline.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/timeline.py:158), [timeline.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/timeline.py:199)）。

次点: **ii. build_telop cut helper の timeline 統合**。理由は、`build_telop_data.py` だけ local の `build_cut_segments_from_vad` / `ms_to_playback_frame` が残っており、timeline 共通化の残りとして明確だから（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:241)）。

**vi 設計概要**
- `test_timeline_integration.py` に slide/telop/generate_plan の pure Python test を追加。
- temp project に `transcript_fixed.json` / `vad_result.json` / `project-config.json` を置き、`PROJ` と module-level `FPS` を temp 側へ monkeypatch。
- `build_telop_data.call_budoux()` は Node と tempfile 依存なので deterministic phrases を返す stub に差し替え（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:217)）。
- negative: VAD 破損、segments 非 list、start/end 欠落。positive: frame monotonic、cut-aware mapping、plan fallback。

**危険ポイント top3**
1. `build_slide_data` / `build_telop_data` は `PROJ` / `FPS` が import 時に固定されるため、test は import 順か monkeypatch が重要（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:27), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:30)）。
2. `main()` は repo 側に生成物を書くので、必ず temp project に向ける（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:374), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:439)）。
3. `watchStaticFile` は Studio 専用で Player では発火しないので、iii は render path に混ぜない設計が必要（Remotion 公式: https://www.remotion.dev/docs/watchstaticfile）。

**Codex review 重点**
P1: VAD exit 8 前の `mkdir` 移動。P2: smoke test が実 script を temp project で通しているか。P2: telop の cut boundary clamp が timeline 統合後も同一 frame を返すか。
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
hook: Stop Completed
tokens used
147,799
**Part A**
結論: P1 は「synthesis 前 exit 8」は通るが、「何も書かず」は厳密には未達。`cleanup_stale_all()` 後、VAD 検証前に `NARRATION_DIR.mkdir()` が走るため、`template/public/narration` が無い状態では directory 作成が起きうる（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:531), Bash 実測: `code=8`, `events=cleanup,mkdir,vad`, `template/public/narration: missing`）。修正は `NARRATION_DIR.mkdir()` を `project_load_cut_segments()` 成功後へ移動。

他の 4 fix は OK:
- `collect_chunks`: `script-json` の plan dict / segments list guard が `.strip()` 前にあり、非 dict / text 非 str は `TranscriptSegmentError`（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:408), Bash 実測）。
- `build_telop` VAD: `validate_vad_schema()` 経由、main 呼び出しは 1 回（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:241), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:292)）。
- `SKILL.md`: exit 3 / exit 8 table 記載あり（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:156)）。
- `assert` は `RuntimeError` 化され、`python -O` でも消えない（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:606)）。

補足: 検証中に HEAD が `a9019c7` へ進んでおり、指定の `e2a1a39` までに加えて Phase 3-L core が入っています（Bash 実測: `git log -4`）。

**Part B**
推奨: **vi. integration_smoke を build_slide / build_telop / generate_slide_plan へ展開**。理由は、現テストは説明上 3 script 対象だが、実 import は `voicevox_narration` 寄りで、`build_slide_data` / `build_telop_data` / `generate_slide_plan` を直接叩いていないため（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:318), rg 実測）。`i` は現 HEAD では `require_timing` と一括 helper が既に入っています（[timeline.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/timeline.py:158), [timeline.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/timeline.py:199)）。

次点: **ii. build_telop cut helper の timeline 統合**。理由は、`build_telop_data.py` だけ local の `build_cut_segments_from_vad` / `ms_to_playback_frame` が残っており、timeline 共通化の残りとして明確だから（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:241)）。

**vi 設計概要**
- `test_timeline_integration.py` に slide/telop/generate_plan の pure Python test を追加。
- temp project に `transcript_fixed.json` / `vad_result.json` / `project-config.json` を置き、`PROJ` と module-level `FPS` を temp 側へ monkeypatch。
- `build_telop_data.call_budoux()` は Node と tempfile 依存なので deterministic phrases を返す stub に差し替え（[build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:217)）。
- negative: VAD 破損、segments 非 list、start/end 欠落。positive: frame monotonic、cut-aware mapping、plan fallback。

**危険ポイント top3**
1. `build_slide_data` / `build_telop_data` は `PROJ` / `FPS` が import 時に固定されるため、test は import 順か monkeypatch が重要（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:27), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:30)）。
2. `main()` は repo 側に生成物を書くので、必ず temp project に向ける（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:374), [build_telop_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_telop_data.py:439)）。
3. `watchStaticFile` は Studio 専用で Player では発火しないので、iii は render path に混ぜない設計が必要（Remotion 公式: https://www.remotion.dev/docs/watchstaticfile）。

**Codex review 重点**
P1: VAD exit 8 前の `mkdir` 移動。P2: smoke test が実 script を temp project で通しているか。P2: telop の cut boundary clamp が timeline 統合後も同一 frame を返すか。

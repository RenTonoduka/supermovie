Reading additional input from stdin...
2026-05-04T12:45:14.594815Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/rokumasuda/.claude/plugins/supermovie
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019df305-75e3-7292-8965-04db9922478c
--------
user
SuperMovie Plugin の roku/phase3h-narration-sequence branch 最新 commit d6f0846 を再 review + Phase 3-I 推奨 consultation、ワンショットで両方。

## Part A: d6f0846 fix re-review

前 review (CODEX_REVIEW_PHASE3H_20260504T213301) で指摘した 9 件 (P1×2 + P2×4 + P3×3) が全部 closed したか機械的 verify。

検査 checklist:
- P1#1 mode helper: src/Narration/mode.ts 新規、NarrationAudio.tsx と MainVideo.tsx が getNarrationMode 経由か
- P1#2 cleanup_stale_all: 旧 narration.wav も削除されるか、partial failure path で残らないか
- P2#3 atomic write: atomic_write_text/_bytes/concat_wavs_atomic、全出力 (narrationData.ts/chunk_meta.json/chunk_NNN.wav/narration.wav) 経由か
- P2#4 read_video_config_fps: VIDEO_CONFIG regex 経路、project-config.json 経路は撤去されたか
- P2#5 FPS source 統一: --fps <= 0 reject、videoConfig.ts 一次 source
- P2#6 wave.Error catch: measure_duration_seconds 呼出箇所すべてで catch、failure rollback
- P3#7 MainVideo redundancy: startsWith chunk_ 削除、helper 経由
- P3#8 Set lookup: getStaticFiles().some 重複の解消
- P3#9 SKILL.md 連携マップ: 3 出力 + getNarrationMode 三経路に追従

新規 regression / 副作用も厳しく見る:
- mode.ts の Set lookup が毎 frame 走るパフォーマンス影響 (memo 必要か)
- atomic_write_text の `.{name}.tmp` ファイル名衝突 (同じ file が複数箇所から書かれた時)
- concat_wavs_atomic の wave.Error が write 中 (open) で発生したら tmp ファイルが残るか
- cleanup_stale_all + atomic write の race (cleanup 中に他プロセスが narration.wav 書いたら)
- index.ts export 追加で ts-circular import 警告 (mode.ts → narrationData.ts → types.ts)

verdict 表は ✅ closed / ⚠️ partial / ❌ remaining + 新規指摘で。

## Part B: Phase 3-I 推奨 consultation

Phase 3-A〜3-H 完了 (基盤 + 視覚スモーク + per-segment narration)。次の Phase 3-I 候補:

i. **any 警告ゼロ化** (Phase 3-E から残置)
   - eslint.config.mjs の no-explicit-any を warning から error に
   - telop-templates-30.zip 由来の component の any を実型に置換
   - 手機械的タスク、自走可

ii. **slide_plan.v2 schema 拡張** (Phase 3-C 延長)
   - Phase 3-C の slide_plan.v1 に transition / animation / theme を追加
   - LLM 出力品質改善
   - Anthropic API 課金あり (Roku 判断要)

iii. **transcript-driven b-roll planner** (新領域、Roku ビジョン関連)
   - LLM が transcript_fixed.json を読んで「ここに静止画 / ここに動画」と判定
   - insertImageData.ts / video2 拡張に流す scene_plan.json 生成
   - Anthropic API 課金あり、画像/動画生成は Phase 3-J 以降に分離
   - Roku 「Reels 高度編集」ビジョンの土台

iv. **Phase 3-G visual smoke を CI 化** (P3 案)
   - GitHub Actions で `npm run visual-smoke` を generated project 上で実行
   - PR 時に dimension regression を自動検出
   - 段取り判断 (CI infra 設計 + main.mp4 fixture 戦略)、Roku 確認推奨

v. **Phase 3-D narration の transcript timing alignment** (Phase 3-H の真の完成)
   - 現状 startFrame は単純累積 (各 chunk 終端 = 次 chunk 開始)
   - transcript_fixed.json segments[].start を base にした tight alignment
   - synthesis silence + crossfade 検討も含む
   - 自走可、Phase 3-H 完了直結

聞きたいこと:
- どれを Phase 3-I 最優先にすべきか (推奨 1 + 次点 1 + 理由)
- 推奨 phase の設計概要
- 危険ポイント top3
- Codex review 重点項目

短く決定的に。Part A は表 + 新規指摘、Part B は推奨 + 設計 + 危険 + review 重点。
2026-05-04T12:45:14.790909Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
2026-05-04T12:45:14.795718Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
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
確認します。今回は `verification-gate` を使って、ローカル実体のファイル・git 差分・コマンド結果に根拠を寄せて re-review と Phase 3-I 推奨を分けて出します。
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
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

exec
/bin/zsh -lc 'git status --short --branch' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Mesh5PBV' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-u7QSLBeW' (errno=Operation not permitted)
## roku/phase3h-narration-sequence
?? docs/

exec
/bin/zsh -lc 'git rev-parse --abbrev-ref HEAD && git rev-parse HEAD && git show --stat --oneline --decorate --no-renames d6f0846' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ViY8F0sJ' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-g0SEIYWi' (errno=Operation not permitted)
roku/phase3h-narration-sequence
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-spY9X69I' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-3bazSoqT' (errno=Operation not permitted)
d6f0846185863c029cb6ad26d3f28f619ad72ab1
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-alrz1mYW' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-pshFI2vz' (errno=Operation not permitted)
d6f0846 (HEAD -> roku/phase3h-narration-sequence) fix(narration): Codex Phase 3-H review P1×2 + P2×4 + P3×3 全 fix
 skills/supermovie-narration/SKILL.md      |  19 ++--
 template/scripts/voicevox_narration.py    | 163 +++++++++++++++++++++++-------
 template/src/MainVideo.tsx                |  35 +++----
 template/src/Narration/NarrationAudio.tsx |  50 +++------
 template/src/Narration/index.ts           |   2 +
 template/src/Narration/mode.ts            |  41 ++++++++
 6 files changed, 206 insertions(+), 104 deletions(-)

codex
ブランチと HEAD はローカルで確認できました。次に、指摘項目ごとに実装経路を追えるよう、変更ファイルを行番号付きで読んで、必要な箇所だけ追加 grep します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/src/Narration/NarrationAudio.tsx' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import React from 'react';
     2	import { Audio, Sequence, staticFile } from 'remotion';
     3	import { getNarrationMode } from './mode';
     4	
     5	interface NarrationAudioProps {
     6	  volume?: number;
     7	}
     8	
     9	/**
    10	 * Phase 3-H: getNarrationMode() で chunks / legacy / none の三経路を分岐。
    11	 * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
    12	 *
    13	 * volume はコールバック形式 (Remotion lint 警告回避、
    14	 * https://www.remotion.dev/docs/audio/volume)。
    15	 */
    16	export const NarrationAudio: React.FC<NarrationAudioProps> = ({ volume = 1.0 }) => {
    17	  const mode = getNarrationMode();
    18	
    19	  if (mode.kind === 'chunks') {
    20	    return (
    21	      <>
    22	        {mode.segments.map((seg) => (
    23	          <Sequence
    24	            key={seg.id}
    25	            from={seg.startFrame}
    26	            durationInFrames={seg.durationInFrames}
    27	          >
    28	            <Audio src={staticFile(seg.file)} volume={() => volume} />
    29	          </Sequence>
    30	        ))}
    31	      </>
    32	    );
    33	  }
    34	
    35	  if (mode.kind === 'legacy') {
    36	    return <Audio src={staticFile(mode.file)} volume={() => volume} />;
    37	  }
    38	
    39	  return null;
    40	};

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
    27	 * 出典: https://www.remotion.dev/docs/getstaticfiles
    28	 */
    29	export const getNarrationMode = (): NarrationMode => {
    30	  const names = new Set(getStaticFiles().map((f) => f.name));
    31	  if (
    32	    narrationData.length > 0 &&
    33	    narrationData.every((seg) => names.has(seg.file))
    34	  ) {
    35	    return { kind: 'chunks', segments: narrationData };
    36	  }
    37	  if (names.has(NARRATION_LEGACY_FILE)) {
    38	    return { kind: 'legacy', file: NARRATION_LEGACY_FILE };
    39	  }
    40	  return { kind: 'none' };
    41	};

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

exec
/bin/zsh -lc 'nl -ba template/src/Narration/index.ts && nl -ba skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	export { NarrationAudio } from './NarrationAudio';
     2	export { narrationData } from './narrationData';
     3	export { getNarrationMode, NARRATION_LEGACY_FILE } from './mode';
     4	export type { NarrationSegment } from './types';
     5	export type { NarrationMode } from './mode';
     1	---
     2	name: supermovie-narration
     3	description: |
     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
     6	  「ナレーション」「TTS」「VOICEVOX」「読み上げ」と言われたときに使用。
     7	argument-hint: [プロジェクトパス] [--speaker N] [--script <path>]
     8	allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
     9	effort: medium
    10	---
    11	
    12	# SuperMovie Narration — VOICEVOX 自動ナレーション
    13	
    14	Senior video producer として、文字起こし結果から自動ナレーションを生成し、
    15	動画の元音声を差し替える形で動画コンテンツの語り直しを行う。
    16	
    17	**前提**: Phase 3-A SlideSequence、Phase 3-B/3-C supermovie-slides 完成後の運用想定。
    18	
    19	## 設計起点
    20	
    21	Codex Phase 3-D design (2026-05-04, CODEX_PHASE3D_VOICEVOX) 推奨:
    22	- engine 不在で skip (`--require-engine` 指定時のみ exit non-zero)
    23	- Phase 3-C と同じく optional 経路で deterministic フォールバックなし (engine 必須)
    24	- Anthropic API ではなく VOICEVOX ローカル engine、課金ゼロ
    25	
    26	## ワークフロー
    27	
    28	```
    29	┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    30	│ 1. engine│ → │ 2. 入力  │ → │ 3. 合成  │ → │ 4. Remotion │
    31	│   起動確認│    │   解決   │    │   結合   │    │   接合    │
    32	└──────────┘    └──────────┘    └──────────┘    └──────────┘
    33	```
    34	
    35	## Phase 1: VOICEVOX engine 起動確認
    36	
    37	VOICEVOX engine は localhost:50021 で REST API を提供する。
    38	Roku が以下のいずれかで起動した後に実行:
    39	
    40	- VOICEVOX デスクトップアプリ (https://voicevox.hiroshiba.jp/)
    41	- VOICEVOX engine Docker (https://github.com/VOICEVOX/voicevox_engine)
    42	
    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
    44	
    45	## Phase 2: 入力解決
    46	
    47	優先順位:
    48	1. `--script <path>` で plain-text 指定 (1 行 1 chunk)
    49	2. `--script-json <path>` で `{segments: [{text}]}` JSON 指定
    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
    51	
    52	## Phase 3: 合成 + 結合 (Phase 3-D legacy + Phase 3-H per-segment)
    53	
    54	各 chunk について:
    55	1. `POST /audio_query?text=...&speaker=<id>` → query JSON
    56	2. `POST /synthesis?speaker=<id>` body=query → WAV bytes
    57	
    58	**Phase 3-D legacy**: chunk wav を時系列で結合し `public/narration.wav` を生成。
    59	
    60	**Phase 3-H per-segment** (default、自動):
    61	- `public/narration/chunk_NNN.wav` を保持 (削除しない)
    62	- 各 chunk の wave header から実 duration 測定 → frame 換算
    63	- `src/Narration/narrationData.ts` を all-or-nothing で生成
    64	  (NarrationSegment[]: id / startFrame / durationInFrames / file / text)
    65	- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
    66	- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
    67	  reset + 部分 chunk を削除 (二重音声 / 中途半端 timeline 防止)
    68	
    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
    70	default 30 の優先順位で解決。
    71	
    72	stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
    73	
    74	## Phase 4: Remotion 接合 (asset gate、手動操作不要)
    75	
    76	Phase 3-F asset gate + Phase 3-H per-segment Sequence により
    77	`MainVideo.tsx` 編集は不要。
    78	
    79	| 状態 | NarrationAudio | base Video volume |
    80	|------|----------------|-------------------|
    81	| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
    84	
    85	優先順位は narrationData > narration.wav > null。
    86	`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
    87	`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
    88	に切り替わる。Roku の手作業ゼロ。
    89	
    90	実装参照:
    91	- `template/src/MainVideo.tsx` (`hasLegacyNarration` + `hasChunkNarration` で `baseVolume` 判定)
    92	- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
    93	- `template/src/Narration/types.ts` (NarrationSegment 型)
    94	- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
    95	
    96	## 実行コマンド
    97	
    98	```bash
    99	# default (transcript の segments すべて、speaker=3 = ずんだもんノーマル)
   100	python3 <PROJECT>/scripts/voicevox_narration.py
   101	
   102	# speaker 指定 (一覧は --list-speakers で確認)
   103	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
   104	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
   105	
   106	# 別スクリプト読み込み
   107	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
   108	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
   109	
   110	# engine 不在で fail させる (CI 用)
   111	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
   112	```
   113	
   114	## 出力
   115	
   116	- `<PROJECT>/public/narration.wav` (Phase 3-D legacy、結合済)
   117	- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
   118	- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
   119	- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
   120	
   121	## エラーハンドリング
   122	
   123	| エラー | 対応 |
   124	|--------|------|
   125	| engine 不在 | INFO ログ + exit 0 (skip)、`--require-engine` 時のみ exit 4 |
   126	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
   127	| `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
   128	| WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |
   129	| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk + 旧 narration.wav 全削除、narrationData.ts 空 array (all-or-nothing) |
   130	| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
   131	| FPS 不正 (--fps <= 0 / videoConfig.ts FPS regex 失敗) | exit 4 (前者) or default 30 fallback (後者) |
   132	
   133	## 連携マップ
   134	
   135	```
   136	/supermovie-init / transcribe / transcript-fix / cut / subtitles / slides
   137	    ↓ transcript_fixed.json
   138	/supermovie-narration         ← ★ここ: VOICEVOX で 3 出力を atomic 生成
   139	    ├─ public/narration/chunk_NNN.wav  (Phase 3-H、render 時に必要)
   140	    ├─ public/narration/chunk_meta.json (debug、fps + segments[])
   141	    ├─ src/Narration/narrationData.ts   (Phase 3-H render 駆動)
   142	    └─ public/narration.wav              (Phase 3-D legacy fallback)
   143	    ↓
   144	MainVideo.tsx + NarrationAudio.tsx が getNarrationMode() で判定
   145	    1) chunks complete → <Sequence> ループ + base mute
   146	    2) legacy narration.wav 存在 → 単一 <Audio> + base mute
   147	    3) どちらも不在 → null + base 元音声 1.0
   148	    ↓
   149	npm run render
   150	```
   151	
   152	**Studio を開いたまま narration.wav を生成した場合は再読み込み推奨**:
   153	`getStaticFiles()` は Studio 起動時の asset リストをキャッシュするため、
   154	新規ファイルは Studio reload (Cmd+R / `r` キー) で反映される
   155	(出典 https://www.remotion.dev/docs/getstaticfiles)。
   156	
   157	## VOICEVOX 利用規約
   158	
   159	- 商用/非商用利用可、音声ライブラリごとにクレジット表記必須 (https://voicevox.hiroshiba.jp/term/)
   160	- 話者選定 + クレジット明記は Roku 判断領域

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,260p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '260,560p'" in /Users/rokumasuda/.claude/plugins/supermovie
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
    45	import re
    46	import sys
    47	import urllib.error
    48	import urllib.parse
    49	import urllib.request
    50	import wave
    51	from pathlib import Path
    52	
    53	PROJ = Path(__file__).resolve().parent.parent
    54	ENGINE_BASE = "http://127.0.0.1:50021"
    55	DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
    56	DEFAULT_FPS = 30
    57	TIMEOUT = 30
    58	
    59	NARRATION_DIR = PROJ / "public" / "narration"
    60	NARRATION_LEGACY_WAV = PROJ / "public" / "narration.wav"
    61	NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
    62	CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
    63	VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
    64	FPS_LINE_RE = re.compile(r"^export const FPS\s*=\s*(\d+)\s*;", re.MULTILINE)
    65	EMPTY_NARRATION_DATA = (
    66	    "import type { NarrationSegment } from './types';\n"
    67	    "\n"
    68	    "export const narrationData: NarrationSegment[] = [];\n"
    69	)
    70	
    71	
    72	def atomic_write_bytes(path: Path, data: bytes) -> None:
    73	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
    74	    path.parent.mkdir(parents=True, exist_ok=True)
    75	    tmp = path.with_name(f".{path.name}.tmp")
    76	    tmp.write_bytes(data)
    77	    os.replace(tmp, path)
    78	
    79	
    80	def atomic_write_text(path: Path, content: str) -> None:
    81	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
    82	    path.parent.mkdir(parents=True, exist_ok=True)
    83	    tmp = path.with_name(f".{path.name}.tmp")
    84	    tmp.write_text(content, encoding="utf-8")
    85	    os.replace(tmp, path)
    86	
    87	
    88	def load_json(p: Path):
    89	    return json.loads(p.read_text(encoding="utf-8"))
    90	
    91	
    92	def http_request(method: str, path: str, params: dict | None = None,
    93	                 body: dict | None = None) -> bytes:
    94	    url = ENGINE_BASE + path
    95	    if params:
    96	        url += "?" + urllib.parse.urlencode(params)
    97	    data = json.dumps(body).encode("utf-8") if body is not None else None
    98	    headers = {"Content-Type": "application/json"} if body is not None else {}
    99	    req = urllib.request.Request(url, data=data, headers=headers, method=method)
   100	    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
   101	        return resp.read()
   102	
   103	
   104	def check_engine() -> tuple[bool, str | None]:
   105	    try:
   106	        body = http_request("GET", "/version")
   107	        return True, body.decode("utf-8").strip().strip('"')
   108	    except (urllib.error.URLError, OSError, urllib.error.HTTPError) as e:
   109	        return False, str(e)
   110	
   111	
   112	def list_speakers() -> list[dict]:
   113	    body = http_request("GET", "/speakers")
   114	    return json.loads(body.decode("utf-8"))
   115	
   116	
   117	def synthesize(text: str, speaker: int) -> bytes:
   118	    """audio_query → synthesis の二段階で WAV bytes を返す."""
   119	    aq_body = http_request("POST", "/audio_query", params={"text": text, "speaker": speaker}, body={})
   120	    aq = json.loads(aq_body.decode("utf-8"))
   121	    wav_bytes = http_request("POST", "/synthesis", params={"speaker": speaker}, body=aq)
   122	    return wav_bytes
   123	
   124	
   125	def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
   126	    """同一 sample rate / channel の wav 列を時系列で結合し atomic に書く.
   127	
   128	    wave.Error は呼び出し側で catch して all-or-nothing rollback する
   129	    (Codex Phase 3-H review P2 #6 反映)。
   130	    """
   131	    if not wavs:
   132	        return
   133	    out_path.parent.mkdir(parents=True, exist_ok=True)
   134	    tmp = out_path.with_name(f".{out_path.name}.tmp")
   135	    with wave.open(str(wavs[0]), "rb") as w0:
   136	        params = w0.getparams()
   137	        frames = [w0.readframes(w0.getnframes())]
   138	    for p in wavs[1:]:
   139	        with wave.open(str(p), "rb") as w:
   140	            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (params.framerate, params.nchannels, params.sampwidth):
   141	                print(f"WARN: {p.name} format mismatch、skip", file=sys.stderr)
   142	                continue
   143	            frames.append(w.readframes(w.getnframes()))
   144	    with wave.open(str(tmp), "wb") as out:
   145	        out.setparams(params)
   146	        for f in frames:
   147	            out.writeframes(f)
   148	    os.replace(tmp, out_path)
   149	
   150	
   151	def measure_duration_seconds(wav_path: Path) -> float:
   152	    """WAV header の (nframes / framerate) で正確な duration を返す.
   153	
   154	    wave.Error / EOFError は呼び出し側で catch (Codex P2 #6 反映)。
   155	    """
   156	    with wave.open(str(wav_path), "rb") as w:
   157	        return w.getnframes() / float(w.getframerate())
   158	
   159	
   160	def cleanup_stale_all() -> None:
   161	    """旧 chunk_*.wav / chunk_meta.json / narration.wav / narrationData.ts を全 reset.
   162	
   163	    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
   164	    legacy mode で stale narration が再生される事故を起こすため、必ず全削除する。
   165	    """
   166	    if NARRATION_DIR.exists():
   167	        for p in NARRATION_DIR.glob("chunk_*.wav"):
   168	            try:
   169	                p.unlink()
   170	            except OSError as e:
   171	                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
   172	        if CHUNK_META_JSON.exists():
   173	            try:
   174	                CHUNK_META_JSON.unlink()
   175	            except OSError as e:
   176	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
   177	    if NARRATION_LEGACY_WAV.exists():
   178	        try:
   179	            NARRATION_LEGACY_WAV.unlink()
   180	        except OSError as e:
   181	            print(f"WARN: stale narration.wav 削除失敗: {e}", file=sys.stderr)
   182	    reset_narration_data_ts()
   183	
   184	
   185	def reset_narration_data_ts() -> None:
   186	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
   187	    if NARRATION_DATA_TS.parent.exists():
   188	        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
   189	
   190	
   191	def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
   192	    """src/videoConfig.ts の `export const FPS = N;` を一次 source として読む.
   193	
   194	    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
   195	    malformed (cfg["source"] が None / str) で AttributeError を起こす経路と、
   196	    Remotion render が videoConfig.FPS を使う一方で script が project-config.json を
   197	    読むため両者がズレる経路の両方を、videoConfig.ts 直読で解消する。
   198	    """
   199	    if not VIDEO_CONFIG.exists():
   200	        return default
   201	    try:
   202	        text = VIDEO_CONFIG.read_text(encoding="utf-8")
   203	    except OSError:
   204	        return default
   205	    m = FPS_LINE_RE.search(text)
   206	    if not m:
   207	        return default
   208	    try:
   209	        fps = int(m.group(1))
   210	    except ValueError:
   211	        return default
   212	    return fps if fps > 0 else default
   213	
   214	
   215	def write_narration_data(
   216	    chunks: list[tuple[Path, str]],
   217	    fps: int,
   218	) -> tuple[list[dict], Path, Path]:
   219	    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く.
   220	
   221	    両方とも atomic 書換 (Codex P2 #3 反映)。wave.Error は呼び出し側で catch。
   222	    """
   223	    segments: list[dict] = []
   224	    cumulative_frame = 0
   225	    for i, (path, text) in enumerate(chunks):
   226	        duration_sec = measure_duration_seconds(path)
   227	        duration_frames = max(1, round(duration_sec * fps))
   228	        rel = path.relative_to(PROJ / "public").as_posix()
   229	        segments.append({
   230	            "id": i,
   231	            "startFrame": cumulative_frame,
   232	            "durationInFrames": duration_frames,
   233	            "file": rel,
   234	            "text": text[:100],  # debug 用、長文は切り詰め
   235	            "duration_sec": round(duration_sec, 3),
   236	        })
   237	        cumulative_frame += duration_frames
   238	
   239	    atomic_write_text(
   240	        CHUNK_META_JSON,
   241	        json.dumps(
   242	            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
   243	            ensure_ascii=False,
   244	            indent=2,
   245	        ),
   246	    )
   247	
   248	    ts_lines = [
   249	        "/**",
   250	        " * Phase 3-H: voicevox_narration.py が all-or-nothing + atomic で書換える narration timeline。",
   251	        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
   252	        " * 手動編集禁止 (script 再実行で上書きされる)。",
   253	        " */",
   254	        "import type { NarrationSegment } from './types';",
   255	        "",
   256	        "export const narrationData: NarrationSegment[] = [",
   257	    ]
   258	    for s in segments:
   259	        ts_lines.append(
   260	            "  { "

 succeeded in 0ms:
   260	            "  { "
   261	            f"id: {s['id']}, "
   262	            f"startFrame: {s['startFrame']}, "
   263	            f"durationInFrames: {s['durationInFrames']}, "
   264	            f"file: {json.dumps(s['file'])}, "
   265	            f"text: {json.dumps(s['text'], ensure_ascii=False)} "
   266	            "},"
   267	        )
   268	    ts_lines.append("];")
   269	    ts_lines.append("")
   270	    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
   271	
   272	    return segments, NARRATION_DATA_TS, CHUNK_META_JSON
   273	
   274	
   275	def _resolve_path(path_str: str) -> Path:
   276	    """非 absolute path は PROJ 相対に解決 (skill 実行時の cwd 揺れを吸収)."""
   277	    p = Path(path_str)
   278	    return p if p.is_absolute() else PROJ / p
   279	
   280	
   281	def collect_chunks(args, transcript: dict) -> list[str]:
   282	    if args.script:
   283	        text = _resolve_path(args.script).read_text(encoding="utf-8")
   284	        return [line.strip() for line in text.splitlines() if line.strip()]
   285	    if args.script_json:
   286	        plan = load_json(_resolve_path(args.script_json))
   287	        return [s.get("text", "").strip() for s in plan.get("segments", []) if s.get("text", "").strip()]
   288	    return [s.get("text", "").strip() for s in transcript.get("segments", []) if s.get("text", "").strip()]
   289	
   290	
   291	def main():
   292	    ap = argparse.ArgumentParser()
   293	    ap.add_argument("--speaker", type=int, default=DEFAULT_SPEAKER,
   294	                    help=f"VOICEVOX speaker id (default {DEFAULT_SPEAKER}=ずんだもんノーマル)")
   295	    ap.add_argument("--script", help="custom plain-text narration (1 line = 1 chunk)")
   296	    ap.add_argument("--script-json", help="custom JSON {segments:[{text}]} narration")
   297	    ap.add_argument("--list-speakers", action="store_true")
   298	    ap.add_argument("--require-engine", action="store_true",
   299	                    help="engine 不在で exit 4 (default は skip exit 0)")
   300	    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
   301	    ap.add_argument(
   302	        "--fps",
   303	        type=int,
   304	        default=None,
   305	        help=f"narrationData.ts に書き込む frame 換算 fps "
   306	             f"(default: src/videoConfig.ts FPS、読めなければ {DEFAULT_FPS})",
   307	    )
   308	    ap.add_argument("--allow-partial", action="store_true",
   309	                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
   310	                         "(default は全 chunk 成功必須)")
   311	    args = ap.parse_args()
   312	
   313	    ok, info = check_engine()
   314	    if not ok:
   315	        msg = f"VOICEVOX engine unavailable at {ENGINE_BASE}: {info}"
   316	        if args.require_engine:
   317	            print(f"ERROR: {msg}", file=sys.stderr)
   318	            return 4
   319	        print(f"INFO: {msg} -> narration generation skipped")
   320	        print(
   321	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
   322	            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
   323	            "(Phase 3-F asset gate + Phase 3-H per-segment Sequence)"
   324	        )
   325	        return 0
   326	    print(f"VOICEVOX engine OK (version: {info})")
   327	
   328	    if args.list_speakers:
   329	        speakers = list_speakers()
   330	        for s in speakers:
   331	            for style in s.get("styles", []):
   332	                print(f"  [{style.get('id'):3}] {s.get('name')} / {style.get('name')}")
   333	        return 0
   334	
   335	    transcript_path = PROJ / "transcript_fixed.json"
   336	    if not transcript_path.exists() and not (args.script or args.script_json):
   337	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
   338	        return 3
   339	    transcript = load_json(transcript_path) if transcript_path.exists() else {}
   340	    chunks = collect_chunks(args, transcript)
   341	    if not chunks:
   342	        print("ERROR: no narration chunks", file=sys.stderr)
   343	        return 3
   344	
   345	    fps = args.fps if args.fps is not None else read_video_config_fps()
   346	    if fps <= 0:
   347	        print(f"ERROR: invalid fps={fps} (--fps is positive integer required)", file=sys.stderr)
   348	        return 4
   349	    print(f"target fps: {fps}")
   350	
   351	    # Phase 3-H: stale narration を全 reset BEFORE synthesis
   352	    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
   353	    cleanup_stale_all()
   354	    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
   355	
   356	    chunk_paths: list[Path] = []
   357	    chunk_texts: list[str] = []
   358	    for i, text in enumerate(chunks):
   359	        try:
   360	            wav_bytes = synthesize(text, args.speaker)
   361	        except (urllib.error.HTTPError, urllib.error.URLError) as e:
   362	            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
   363	            continue
   364	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
   365	        atomic_write_bytes(p, wav_bytes)
   366	        chunk_paths.append(p)
   367	        chunk_texts.append(text)
   368	        print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
   369	
   370	    if not chunk_paths:
   371	        print("ERROR: no chunks succeeded", file=sys.stderr)
   372	        return 5
   373	    if not args.allow_partial and len(chunk_paths) < len(chunks):
   374	        print(
   375	            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
   376	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
   377	            file=sys.stderr,
   378	        )
   379	        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
   380	        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
   381	        for p in chunk_paths:
   382	            try:
   383	                p.unlink()
   384	            except OSError:
   385	                pass
   386	        return 6
   387	
   388	    out_path = _resolve_path(args.output)
   389	    try:
   390	        concat_wavs_atomic(chunk_paths, out_path)
   391	    except (wave.Error, EOFError) as e:
   392	        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
   393	        for p in chunk_paths:
   394	            try:
   395	                p.unlink()
   396	            except OSError:
   397	                pass
   398	        return 6
   399	    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
   400	    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
   401	
   402	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
   403	    pairs = list(zip(chunk_paths, chunk_texts))
   404	    try:
   405	        segments, ts_path, meta_path = write_narration_data(pairs, fps)
   406	    except (wave.Error, EOFError) as e:
   407	        print(f"ERROR: WAV duration probe failed (wave.Error / EOFError): {e}", file=sys.stderr)
   408	        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
   409	        # so user は再実行 or --allow-partial で部分書き出し選択可
   410	        for p in chunk_paths:
   411	            try:
   412	                p.unlink()
   413	            except OSError:
   414	                pass
   415	        if out_path.exists():
   416	            try:
   417	                out_path.unlink()
   418	            except OSError:
   419	                pass
   420	        return 6
   421	    print(f"wrote: {ts_path} ({len(segments)} segments, {sum(s['durationInFrames'] for s in segments)} frames)")
   422	    print(f"wrote: {meta_path}")
   423	
   424	    summary = {
   425	        "speaker": args.speaker,
   426	        "fps": fps,
   427	        "chunks": len(chunk_paths),
   428	        "total_chunks": len(chunks),
   429	        "total_frames": sum(s["durationInFrames"] for s in segments),
   430	        "narration_wav": str(out_path),
   431	        "narration_data_ts": str(ts_path),
   432	        "chunk_meta_json": str(meta_path),
   433	        "engine_version": info,
   434	    }
   435	    print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")
   436	    return 0
   437	
   438	
   439	if __name__ == "__main__":
   440	    sys.exit(main())

exec
/bin/zsh -lc "rg -n \"project-config|project_config|render_fps|read_video_config|VIDEO_CONFIG|fps|measure_duration_seconds|atomic_write|concat_wavs|cleanup_stale|narration\\.wav|chunk_meta|narrationData\" template/scripts/voicevox_narration.py template/src skills/supermovie-narration/SKILL.md" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
skills/supermovie-narration/SKILL.md:58:**Phase 3-D legacy**: chunk wav を時系列で結合し `public/narration.wav` を生成。
skills/supermovie-narration/SKILL.md:63:- `src/Narration/narrationData.ts` を all-or-nothing で生成
skills/supermovie-narration/SKILL.md:65:- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
skills/supermovie-narration/SKILL.md:66:- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
skills/supermovie-narration/SKILL.md:81:| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
skills/supermovie-narration/SKILL.md:85:優先順位は narrationData > narration.wav > null。
skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
skills/supermovie-narration/SKILL.md:92:- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
skills/supermovie-narration/SKILL.md:94:- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
skills/supermovie-narration/SKILL.md:116:- `<PROJECT>/public/narration.wav` (Phase 3-D legacy、結合済)
skills/supermovie-narration/SKILL.md:118:- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
skills/supermovie-narration/SKILL.md:119:- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
skills/supermovie-narration/SKILL.md:129:| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk + 旧 narration.wav 全削除、narrationData.ts 空 array (all-or-nothing) |
skills/supermovie-narration/SKILL.md:130:| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
skills/supermovie-narration/SKILL.md:131:| FPS 不正 (--fps <= 0 / videoConfig.ts FPS regex 失敗) | exit 4 (前者) or default 30 fallback (後者) |
skills/supermovie-narration/SKILL.md:140:    ├─ public/narration/chunk_meta.json (debug、fps + segments[])
skills/supermovie-narration/SKILL.md:141:    ├─ src/Narration/narrationData.ts   (Phase 3-H render 駆動)
skills/supermovie-narration/SKILL.md:142:    └─ public/narration.wav              (Phase 3-D legacy fallback)
skills/supermovie-narration/SKILL.md:146:    2) legacy narration.wav 存在 → 単一 <Audio> + base mute
skills/supermovie-narration/SKILL.md:152:**Studio を開いたまま narration.wav を生成した場合は再読み込み推奨**:
template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
template/scripts/voicevox_narration.py:8:- 出力: public/narration.wav (segments 個別 wav を結合、legacy fallback)
template/scripts/voicevox_narration.py:14:- src/Narration/narrationData.ts を all-or-nothing で生成
template/scripts/voicevox_narration.py:16:- public/narration/chunk_meta.json も debug 用に出力
template/scripts/voicevox_narration.py:17:- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
template/scripts/voicevox_narration.py:18:- partial failure 時は narrationData.ts を空に reset + 部分 chunk 削除、二重音声防止
template/scripts/voicevox_narration.py:21:- 全 narration 出力 (narration.wav / narrationData.ts / chunk_meta.json) を
template/scripts/voicevox_narration.py:24:  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
template/scripts/voicevox_narration.py:26:- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
template/scripts/voicevox_narration.py:34:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は src/videoConfig.ts FPS)
template/scripts/voicevox_narration.py:60:NARRATION_LEGACY_WAV = PROJ / "public" / "narration.wav"
template/scripts/voicevox_narration.py:61:NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
template/scripts/voicevox_narration.py:62:CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
template/scripts/voicevox_narration.py:63:VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
template/scripts/voicevox_narration.py:68:    "export const narrationData: NarrationSegment[] = [];\n"
template/scripts/voicevox_narration.py:72:def atomic_write_bytes(path: Path, data: bytes) -> None:
template/scripts/voicevox_narration.py:80:def atomic_write_text(path: Path, content: str) -> None:
template/scripts/voicevox_narration.py:125:def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
template/scripts/voicevox_narration.py:151:def measure_duration_seconds(wav_path: Path) -> float:
template/scripts/voicevox_narration.py:160:def cleanup_stale_all() -> None:
template/scripts/voicevox_narration.py:161:    """旧 chunk_*.wav / chunk_meta.json / narration.wav / narrationData.ts を全 reset.
template/scripts/voicevox_narration.py:163:    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
template/scripts/voicevox_narration.py:176:                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
template/scripts/voicevox_narration.py:181:            print(f"WARN: stale narration.wav 削除失敗: {e}", file=sys.stderr)
template/scripts/voicevox_narration.py:186:    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
template/scripts/voicevox_narration.py:188:        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
template/scripts/voicevox_narration.py:191:def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
template/scripts/voicevox_narration.py:194:    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
template/scripts/voicevox_narration.py:196:    Remotion render が videoConfig.FPS を使う一方で script が project-config.json を
template/scripts/voicevox_narration.py:199:    if not VIDEO_CONFIG.exists():
template/scripts/voicevox_narration.py:202:        text = VIDEO_CONFIG.read_text(encoding="utf-8")
template/scripts/voicevox_narration.py:209:        fps = int(m.group(1))
template/scripts/voicevox_narration.py:212:    return fps if fps > 0 else default
template/scripts/voicevox_narration.py:217:    fps: int,
template/scripts/voicevox_narration.py:219:    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く.
template/scripts/voicevox_narration.py:226:        duration_sec = measure_duration_seconds(path)
template/scripts/voicevox_narration.py:227:        duration_frames = max(1, round(duration_sec * fps))
template/scripts/voicevox_narration.py:239:    atomic_write_text(
template/scripts/voicevox_narration.py:242:            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
template/scripts/voicevox_narration.py:256:        "export const narrationData: NarrationSegment[] = [",
template/scripts/voicevox_narration.py:270:    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
template/scripts/voicevox_narration.py:300:    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
template/scripts/voicevox_narration.py:302:        "--fps",
template/scripts/voicevox_narration.py:305:        help=f"narrationData.ts に書き込む frame 換算 fps "
template/scripts/voicevox_narration.py:309:                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
template/scripts/voicevox_narration.py:321:            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
template/scripts/voicevox_narration.py:322:            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
template/scripts/voicevox_narration.py:345:    fps = args.fps if args.fps is not None else read_video_config_fps()
template/scripts/voicevox_narration.py:346:    if fps <= 0:
template/scripts/voicevox_narration.py:347:        print(f"ERROR: invalid fps={fps} (--fps is positive integer required)", file=sys.stderr)
template/scripts/voicevox_narration.py:349:    print(f"target fps: {fps}")
template/scripts/voicevox_narration.py:352:    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
template/scripts/voicevox_narration.py:353:    cleanup_stale_all()
template/scripts/voicevox_narration.py:365:        atomic_write_bytes(p, wav_bytes)
template/scripts/voicevox_narration.py:376:            f"(--allow-partial で部分成功でも narration.wav 出力可)",
template/scripts/voicevox_narration.py:379:        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
template/scripts/voicevox_narration.py:380:        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
template/scripts/voicevox_narration.py:390:        concat_wavs_atomic(chunk_paths, out_path)
template/scripts/voicevox_narration.py:402:    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
template/scripts/voicevox_narration.py:405:        segments, ts_path, meta_path = write_narration_data(pairs, fps)
template/scripts/voicevox_narration.py:408:        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
template/scripts/voicevox_narration.py:426:        "fps": fps,
template/scripts/voicevox_narration.py:432:        "chunk_meta_json": str(meta_path),
template/src/ネガティブテロップ/紫文字白背景.tsx:20:  fps: number;
template/src/ネガティブテロップ/黒紫グラデ.tsx:20:  fps: number;
template/src/ネガティブテロップ/残酷テロップ・紺.tsx:20:  fps: number;
template/src/ネガティブテロップ/白文字紫シャドウ.tsx:20:  fps: number;
template/src/MainVideo.tsx:26:      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
template/src/MainVideo.tsx:49:      {/* ナレーション (Phase 3-F asset gate、narration.wav 不在で null) */}
template/src/ネガティブテロップ/黒文字白背景.tsx:20:  fps: number;
template/src/Title/Title.tsx:25:  const { fps } = useVideoConfig();
template/src/Title/Title.tsx:37:    fps,
template/src/Root.tsx:14:        fps={FPS}
template/src/Narration/index.ts:2:export { narrationData } from './narrationData';
template/src/Narration/types.ts:3: * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
template/src/メインテロップ/白青テロップver2.tsx:20:  fps: number;
template/src/メインテロップ/白文字黒シャドウゴシック.tsx:20:  fps: number;
template/src/メインテロップ/緑文字白背景.tsx:20:  fps: number;
template/src/強調テロップ/白赤テロップver2.tsx:20:  fps: number;
template/src/メインテロップ/白文字黒シャドウ明朝体.tsx:20:  fps: number;
template/src/Narration/narrationData.ts:3: * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
template/src/Narration/narrationData.ts:7:export const narrationData: NarrationSegment[] = [];
template/src/テロップテンプレート/telopTemplateRegistry.tsx:53:  fps: number;
template/src/テロップテンプレート/telopTemplateRegistry.tsx:108:// project-config.json telopStyle.{main,emphasis,negative} 既定値の displayName とのマップ:
template/src/メインテロップ/黒文字.tsx:20:  fps: number;
template/src/メインテロップ/青文字白背景.tsx:20:  fps: number;
template/src/Narration/mode.ts:2:import { narrationData } from './narrationData';
template/src/Narration/mode.ts:5:export const NARRATION_LEGACY_FILE = 'narration.wav';
template/src/Narration/mode.ts:20: *   1) narrationData が non-empty + 全 chunk file が public/ 配下に存在 → chunks
template/src/Narration/mode.ts:21: *   2) public/narration.wav 存在 → legacy
template/src/Narration/mode.ts:32:    narrationData.length > 0 &&
template/src/Narration/mode.ts:33:    narrationData.every((seg) => names.has(seg.file))
template/src/Narration/mode.ts:35:    return { kind: 'chunks', segments: narrationData };
template/src/メインテロップ/白黒テロップ.tsx:20:  fps: number;
template/src/メインテロップ/白青テロップ.tsx:20:  fps: number;
template/src/強調テロップ/オレンジグラデーション.tsx:20:  fps: number;
template/src/メインテロップ/白文字黒シャドウ.tsx:20:  fps: number;
template/src/強調テロップ/赤文字白背景.tsx:20:  fps: number;
template/src/メインテロップ/白文字黒背景.tsx:20:  fps: number;
template/src/強調テロップ/黄色シャドウ.tsx:20:  fps: number;
template/src/メインテロップ/白文字青ピンク背景グラデ.tsx:20:  fps: number;
template/src/強調テロップ/黒文字黄色背景.tsx:20:  fps: number;
template/src/強調テロップ/金グラデ・紺背景.tsx:20:  fps: number;
template/src/テロップテンプレート/Telop.tsx:125:  fps: number;
template/src/テロップテンプレート/Telop.tsx:129:}> = ({ text, localFrame, fps, config, animation, duration }) => {
template/src/テロップテンプレート/Telop.tsx:152:          fps,
template/src/テロップテンプレート/Telop.tsx:201:  const { fps, width } = useVideoConfig();
template/src/テロップテンプレート/Telop.tsx:243:        fps,
template/src/テロップテンプレート/Telop.tsx:307:              fps={fps}
template/src/メインテロップ/白背景グラデ.tsx:20:  fps: number;
template/src/強調テロップ/緑グラデ金シャドウ.tsx:20:  fps: number;
template/src/強調テロップ/赤文字.tsx:20:  fps: number;
template/src/強調テロップ/白緑テロップ.tsx:20:  fps: number;
template/src/強調テロップ/白赤テロップ.tsx:20:  fps: number;
template/src/強調テロップ/黄色文字黒シャドウ.tsx:20:  fps: number;
template/src/強調テロップ/白文字赤シャドウ.tsx:20:  fps: number;
template/src/強調テロップ/青文字金枠.tsx:20:  fps: number;
template/src/テロップテンプレート/TelopPlayer.tsx:22:function segmentToSubtitleItem(segment: TelopSegment, fps: number): SubtitleItem {
template/src/テロップテンプレート/TelopPlayer.tsx:23:  const startSec = segment.startFrame / fps;
template/src/テロップテンプレート/TelopPlayer.tsx:24:  const endSec = segment.endFrame / fps;
template/src/テロップテンプレート/TelopPlayer.tsx:38:  const { fps } = useVideoConfig();
template/src/テロップテンプレート/TelopPlayer.tsx:54:      fps,
template/src/テロップテンプレート/TelopPlayer.tsx:55:      subtitles: [segmentToSubtitleItem(current, fps)],

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git diff --no-renames d6f0846''^ d6f0846 -- template/scripts/voicevox_narration.py template/src/MainVideo.tsx template/src/Narration/NarrationAudio.tsx template/src/Narration/mode.ts skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-62YDomnw' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-uGi9beWf' (errno=Operation not permitted)
diff --git a/skills/supermovie-narration/SKILL.md b/skills/supermovie-narration/SKILL.md
index 76fb7e8..7310aa3 100644
--- a/skills/supermovie-narration/SKILL.md
+++ b/skills/supermovie-narration/SKILL.md
@@ -126,18 +126,25 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
 | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
 | `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
 | WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |
-| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
+| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk + 旧 narration.wav 全削除、narrationData.ts 空 array (all-or-nothing) |
+| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
+| FPS 不正 (--fps <= 0 / videoConfig.ts FPS regex 失敗) | exit 4 (前者) or default 30 fallback (後者) |
 
 ## 連携マップ
 
 ```
 /supermovie-init / transcribe / transcript-fix / cut / subtitles / slides
     ↓ transcript_fixed.json
-/supermovie-narration         ← ★ここ: VOICEVOX で narration.wav 生成
-    ↓ public/narration.wav
-MainVideo.tsx が public/narration.wav を自動検出 (asset gate)
-    └ NarrationAudio: <Audio src=narration.wav /> マウント
-    └ base Video: volume=0 に切替 (二重音声防止)
+/supermovie-narration         ← ★ここ: VOICEVOX で 3 出力を atomic 生成
+    ├─ public/narration/chunk_NNN.wav  (Phase 3-H、render 時に必要)
+    ├─ public/narration/chunk_meta.json (debug、fps + segments[])
+    ├─ src/Narration/narrationData.ts   (Phase 3-H render 駆動)
+    └─ public/narration.wav              (Phase 3-D legacy fallback)
+    ↓
+MainVideo.tsx + NarrationAudio.tsx が getNarrationMode() で判定
+    1) chunks complete → <Sequence> ループ + base mute
+    2) legacy narration.wav 存在 → 単一 <Audio> + base mute
+    3) どちらも不在 → null + base 元音声 1.0
     ↓
 npm run render
 ```
diff --git a/template/scripts/voicevox_narration.py b/template/scripts/voicevox_narration.py
index 5a1baca..f85ccda 100644
--- a/template/scripts/voicevox_narration.py
+++ b/template/scripts/voicevox_narration.py
@@ -14,8 +14,16 @@ Phase 3-H 拡張 (Codex CODEX_PHASE3H_NEXT, 2026-05-04):
 - src/Narration/narrationData.ts を all-or-nothing で生成
   (NarrationSegment[] = [{id, startFrame, durationInFrames, file, text}])
 - public/narration/chunk_meta.json も debug 用に出力
-- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
-- partial failure 時は narrationData.ts を空に reset、二重音声防止
+- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
+- partial failure 時は narrationData.ts を空に reset + 部分 chunk 削除、二重音声防止
+
+Phase 3-H review fix (Codex CODEX_REVIEW_PHASE3H_20260504T213301, P1×2 + P2×4):
+- 全 narration 出力 (narration.wav / narrationData.ts / chunk_meta.json) を
+  tempfile + os.replace で atomic 書き換え (SIGINT/disk full 安全、P2 #3)
+- FPS は src/videoConfig.ts の `export const FPS = N;` を一次 source に
+  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
+- wave.Error / EOFError を catch して exit 6 で all-or-nothing rollback (P2 #6)
+- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
 
 Usage:
     python3 scripts/voicevox_narration.py
@@ -23,7 +31,7 @@ Usage:
     python3 scripts/voicevox_narration.py --script narration.txt
     python3 scripts/voicevox_narration.py --list-speakers
     python3 scripts/voicevox_narration.py --require-engine
-    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は src/videoConfig.ts FPS)
 
 Engine 起動 (Roku ローカル):
     https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
@@ -33,6 +41,8 @@ from __future__ import annotations
 
 import argparse
 import json
+import os
+import re
 import sys
 import urllib.error
 import urllib.parse
@@ -47,8 +57,11 @@ DEFAULT_FPS = 30
 TIMEOUT = 30
 
 NARRATION_DIR = PROJ / "public" / "narration"
+NARRATION_LEGACY_WAV = PROJ / "public" / "narration.wav"
 NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
 CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
+VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
+FPS_LINE_RE = re.compile(r"^export const FPS\s*=\s*(\d+)\s*;", re.MULTILINE)
 EMPTY_NARRATION_DATA = (
     "import type { NarrationSegment } from './types';\n"
     "\n"
@@ -56,6 +69,22 @@ EMPTY_NARRATION_DATA = (
 )
 
 
+def atomic_write_bytes(path: Path, data: bytes) -> None:
+    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
+    path.parent.mkdir(parents=True, exist_ok=True)
+    tmp = path.with_name(f".{path.name}.tmp")
+    tmp.write_bytes(data)
+    os.replace(tmp, path)
+
+
+def atomic_write_text(path: Path, content: str) -> None:
+    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
+    path.parent.mkdir(parents=True, exist_ok=True)
+    tmp = path.with_name(f".{path.name}.tmp")
+    tmp.write_text(content, encoding="utf-8")
+    os.replace(tmp, path)
+
+
 def load_json(p: Path):
     return json.loads(p.read_text(encoding="utf-8"))
 
@@ -93,10 +122,16 @@ def synthesize(text: str, speaker: int) -> bytes:
     return wav_bytes
 
 
-def concat_wavs(wavs: list[Path], out_path: Path) -> None:
-    """同一 sample rate / channel の wav 列を時系列で結合."""
+def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
+    """同一 sample rate / channel の wav 列を時系列で結合し atomic に書く.
+
+    wave.Error は呼び出し側で catch して all-or-nothing rollback する
+    (Codex Phase 3-H review P2 #6 反映)。
+    """
     if not wavs:
         return
+    out_path.parent.mkdir(parents=True, exist_ok=True)
+    tmp = out_path.with_name(f".{out_path.name}.tmp")
     with wave.open(str(wavs[0]), "rb") as w0:
         params = w0.getparams()
         frames = [w0.readframes(w0.getnframes())]
@@ -106,21 +141,28 @@ def concat_wavs(wavs: list[Path], out_path: Path) -> None:
                 print(f"WARN: {p.name} format mismatch、skip", file=sys.stderr)
                 continue
             frames.append(w.readframes(w.getnframes()))
-    with wave.open(str(out_path), "wb") as out:
+    with wave.open(str(tmp), "wb") as out:
         out.setparams(params)
         for f in frames:
             out.writeframes(f)
+    os.replace(tmp, out_path)
 
 
 def measure_duration_seconds(wav_path: Path) -> float:
-    """WAV header の (nframes / framerate) で正確な duration を返す."""
+    """WAV header の (nframes / framerate) で正確な duration を返す.
+
+    wave.Error / EOFError は呼び出し側で catch (Codex P2 #6 反映)。
+    """
     with wave.open(str(wav_path), "rb") as w:
         return w.getnframes() / float(w.getframerate())
 
 
-def cleanup_stale_chunks() -> None:
-    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
-    narrationData.ts も空 array に reset する。"""
+def cleanup_stale_all() -> None:
+    """旧 chunk_*.wav / chunk_meta.json / narration.wav / narrationData.ts を全 reset.
+
+    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
+    legacy mode で stale narration が再生される事故を起こすため、必ず全削除する。
+    """
     if NARRATION_DIR.exists():
         for p in NARRATION_DIR.glob("chunk_*.wav"):
             try:
@@ -132,35 +174,52 @@ def cleanup_stale_chunks() -> None:
                 CHUNK_META_JSON.unlink()
             except OSError as e:
                 print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
+    if NARRATION_LEGACY_WAV.exists():
+        try:
+            NARRATION_LEGACY_WAV.unlink()
+        except OSError as e:
+            print(f"WARN: stale narration.wav 削除失敗: {e}", file=sys.stderr)
     reset_narration_data_ts()
 
 
 def reset_narration_data_ts() -> None:
-    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
+    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
     if NARRATION_DATA_TS.parent.exists():
-        NARRATION_DATA_TS.write_text(EMPTY_NARRATION_DATA, encoding="utf-8")
+        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
+
 
+def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
+    """src/videoConfig.ts の `export const FPS = N;` を一次 source として読む.
 
-def read_render_fps(default: int = DEFAULT_FPS) -> int:
-    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
-    cfg_path = PROJ / "project-config.json"
-    if not cfg_path.exists():
+    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
+    malformed (cfg["source"] が None / str) で AttributeError を起こす経路と、
+    Remotion render が videoConfig.FPS を使う一方で script が project-config.json を
+    読むため両者がズレる経路の両方を、videoConfig.ts 直読で解消する。
+    """
+    if not VIDEO_CONFIG.exists():
+        return default
+    try:
+        text = VIDEO_CONFIG.read_text(encoding="utf-8")
+    except OSError:
+        return default
+    m = FPS_LINE_RE.search(text)
+    if not m:
         return default
     try:
-        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
-    except (json.JSONDecodeError, OSError):
+        fps = int(m.group(1))
+    except ValueError:
         return default
-    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
-    if isinstance(fps, (int, float)) and fps > 0:
-        return int(fps)
-    return default
+    return fps if fps > 0 else default
 
 
 def write_narration_data(
     chunks: list[tuple[Path, str]],
     fps: int,
 ) -> tuple[list[dict], Path, Path]:
-    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
+    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く.
+
+    両方とも atomic 書換 (Codex P2 #3 反映)。wave.Error は呼び出し側で catch。
+    """
     segments: list[dict] = []
     cumulative_frame = 0
     for i, (path, text) in enumerate(chunks):
@@ -177,19 +236,18 @@ def write_narration_data(
         })
         cumulative_frame += duration_frames
 
-    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
-    CHUNK_META_JSON.write_text(
+    atomic_write_text(
+        CHUNK_META_JSON,
         json.dumps(
             {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
             ensure_ascii=False,
             indent=2,
         ),
-        encoding="utf-8",
     )
 
     ts_lines = [
         "/**",
-        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
+        " * Phase 3-H: voicevox_narration.py が all-or-nothing + atomic で書換える narration timeline。",
         " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
         " * 手動編集禁止 (script 再実行で上書きされる)。",
         " */",
@@ -209,8 +267,7 @@ def write_narration_data(
         )
     ts_lines.append("];")
     ts_lines.append("")
-    NARRATION_DATA_TS.parent.mkdir(parents=True, exist_ok=True)
-    NARRATION_DATA_TS.write_text("\n".join(ts_lines), encoding="utf-8")
+    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
 
     return segments, NARRATION_DATA_TS, CHUNK_META_JSON
 
@@ -246,7 +303,7 @@ def main():
         type=int,
         default=None,
         help=f"narrationData.ts に書き込む frame 換算 fps "
-             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
+             f"(default: src/videoConfig.ts FPS、読めなければ {DEFAULT_FPS})",
     )
     ap.add_argument("--allow-partial", action="store_true",
                     help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
@@ -285,11 +342,15 @@ def main():
         print("ERROR: no narration chunks", file=sys.stderr)
         return 3
 
-    fps = args.fps if args.fps is not None else read_render_fps()
+    fps = args.fps if args.fps is not None else read_video_config_fps()
+    if fps <= 0:
+        print(f"ERROR: invalid fps={fps} (--fps is positive integer required)", file=sys.stderr)
+        return 4
     print(f"target fps: {fps}")
 
-    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
-    cleanup_stale_chunks()
+    # Phase 3-H: stale narration を全 reset BEFORE synthesis
+    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
+    cleanup_stale_all()
     NARRATION_DIR.mkdir(parents=True, exist_ok=True)
 
     chunk_paths: list[Path] = []
@@ -301,7 +362,7 @@ def main():
             print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
             continue
         p = NARRATION_DIR / f"chunk_{i:03d}.wav"
-        p.write_bytes(wav_bytes)
+        atomic_write_bytes(p, wav_bytes)
         chunk_paths.append(p)
         chunk_texts.append(text)
         print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
@@ -315,24 +376,48 @@ def main():
             f"(--allow-partial で部分成功でも narration.wav 出力可)",
             file=sys.stderr,
         )
-        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
+        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
+        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
         for p in chunk_paths:
             try:
                 p.unlink()
             except OSError:
                 pass
-        reset_narration_data_ts()
         return 6
 
     out_path = _resolve_path(args.output)
-    out_path.parent.mkdir(parents=True, exist_ok=True)
-    concat_wavs(chunk_paths, out_path)
+    try:
+        concat_wavs_atomic(chunk_paths, out_path)
+    except (wave.Error, EOFError) as e:
+        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
+        for p in chunk_paths:
+            try:
+                p.unlink()
+            except OSError:
+                pass
+        return 6
     print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
     print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
 
     # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
     pairs = list(zip(chunk_paths, chunk_texts))
-    segments, ts_path, meta_path = write_narration_data(pairs, fps)
+    try:
+        segments, ts_path, meta_path = write_narration_data(pairs, fps)
+    except (wave.Error, EOFError) as e:
+        print(f"ERROR: WAV duration probe failed (wave.Error / EOFError): {e}", file=sys.stderr)
+        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
+        # so user は再実行 or --allow-partial で部分書き出し選択可
+        for p in chunk_paths:
+            try:
+                p.unlink()
+            except OSError:
+                pass
+        if out_path.exists():
+            try:
+                out_path.unlink()
+            except OSError:
+                pass
+        return 6
     print(f"wrote: {ts_path} ({len(segments)} segments, {sum(s['durationInFrames'] for s in segments)} frames)")
     print(f"wrote: {meta_path}")
 
diff --git a/template/src/MainVideo.tsx b/template/src/MainVideo.tsx
index abd0fa5..225b475 100644
--- a/template/src/MainVideo.tsx
+++ b/template/src/MainVideo.tsx
@@ -1,36 +1,25 @@
-import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
+import { AbsoluteFill, Video, staticFile } from 'remotion';
 import { TelopPlayer } from './テロップテンプレート';
 import { SESequence } from './SoundEffects/SESequence';
 import { BGM } from './SoundEffects/BGM';
 import { ImageSequence } from './InsertImage';
 import { TitleSequence } from './Title';
 import { SlideSequence } from './Slides';
-import { NarrationAudio, narrationData } from './Narration';
+import { NarrationAudio } from './Narration';
+import { getNarrationMode } from './Narration/mode';
 import { VIDEO_FILE } from './videoConfig';
 
-const NARRATION_FILE = 'narration.wav';
-const NARRATION_CHUNK_PREFIX = 'narration/chunk_';
-
 export const MainVideo: React.FC = () => {
-  // Phase 3-F asset gate + Phase 3-H per-segment Sequence と連動:
-  // - legacy: public/narration.wav 存在 → base mute
-  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
-  // どちらも不在なら base 元音声 1.0 で再生。getStaticFiles は Studio/render 時に
-  // public/ 配下の asset 一覧を返す Remotion 公式 API
+  // Phase 3-F asset gate + Phase 3-H per-segment Sequence の mode helper を共有
+  // (Codex Phase 3-H review P1 #1 反映)。chunks / legacy / none のいずれでも
+  // narration が「鳴る」状態なら base 元音声を mute、'none' なら 1.0 で再生する。
+  // これで NarrationAudio と判定が一致し、無音バグ (chunk 不足 + legacy 存在で
+  // 両方消える) を防ぐ。
+  // 注意: Studio 起動後に narration を生成した場合、Studio reload (Cmd+R / `r` キー)
+  // で getStaticFiles cache を再生成する必要がある
   // (https://www.remotion.dev/docs/getstaticfiles)。
-  // 注意: Studio 起動後に narration を生成した場合、Studio リロード
-  // (Cmd+R / `r` キー) で反映する。新規 asset 追加に watchStaticFile を使う選択肢
-  // もあるが、現状は単純化のため reload 方式を採用。
-  const staticFiles = getStaticFiles();
-  const hasLegacyNarration = staticFiles.some((f) => f.name === NARRATION_FILE);
-  const hasChunkNarration =
-    narrationData.length > 0 &&
-    narrationData.every((seg) =>
-      staticFiles.some((f) => f.name === seg.file),
-    ) &&
-    staticFiles.some((f) => f.name.startsWith(NARRATION_CHUNK_PREFIX));
-  const hasNarration = hasLegacyNarration || hasChunkNarration;
-  const baseVolume = hasNarration ? 0 : 1.0;
+  const narrationMode = getNarrationMode();
+  const baseVolume = narrationMode.kind === 'none' ? 1.0 : 0;
 
   return (
     <AbsoluteFill style={{ backgroundColor: 'black' }}>
diff --git a/template/src/Narration/NarrationAudio.tsx b/template/src/Narration/NarrationAudio.tsx
index aa785dc..d8ba4f8 100644
--- a/template/src/Narration/NarrationAudio.tsx
+++ b/template/src/Narration/NarrationAudio.tsx
@@ -1,47 +1,25 @@
 import React from 'react';
-import { Audio, Sequence, getStaticFiles, staticFile } from 'remotion';
-import { narrationData } from './narrationData';
+import { Audio, Sequence, staticFile } from 'remotion';
+import { getNarrationMode } from './mode';
 
 interface NarrationAudioProps {
-  /** legacy 単一ファイル名 (public/ 配下、省略時 'narration.wav') */
-  file?: string;
   volume?: number;
 }
 
 /**
- * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
- * narrationData.ts を生成する経路)。
+ * Phase 3-H: getNarrationMode() で chunks / legacy / none の三経路を分岐。
+ * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
  *
- * 動作優先順位:
- *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
- *      → 各 chunk を <Sequence from={startFrame} durationInFrames={...}>
- *        + <Audio /> でループ再生 (https://www.remotion.dev/docs/sequence)
- *   2) narrationData が空 + public/narration.wav 存在
- *      → legacy 単一 wav (Phase 3-D 互換、deterministic test 用)
- *   3) どちらも不在 → null (asset gate、Phase 3-F 互換)
- *
- * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
- * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
- *
- * volume はコールバック形式 ((frame) => volume) で Remotion lint 警告を回避
- * (https://www.remotion.dev/docs/audio/volume)。
+ * volume はコールバック形式 (Remotion lint 警告回避、
+ * https://www.remotion.dev/docs/audio/volume)。
  */
-export const NarrationAudio: React.FC<NarrationAudioProps> = ({
-  file = 'narration.wav',
-  volume = 1.0,
-}) => {
-  const staticFiles = getStaticFiles();
+export const NarrationAudio: React.FC<NarrationAudioProps> = ({ volume = 1.0 }) => {
+  const mode = getNarrationMode();
 
-  if (narrationData.length > 0) {
-    const allChunksExist = narrationData.every((seg) =>
-      staticFiles.some((f) => f.name === seg.file),
-    );
-    if (!allChunksExist) {
-      return null;
-    }
+  if (mode.kind === 'chunks') {
     return (
       <>
-        {narrationData.map((seg) => (
+        {mode.segments.map((seg) => (
           <Sequence
             key={seg.id}
             from={seg.startFrame}
@@ -54,9 +32,9 @@ export const NarrationAudio: React.FC<NarrationAudioProps> = ({
     );
   }
 
-  const hasFile = staticFiles.some((f) => f.name === file);
-  if (!hasFile) {
-    return null;
+  if (mode.kind === 'legacy') {
+    return <Audio src={staticFile(mode.file)} volume={() => volume} />;
   }
-  return <Audio src={staticFile(file)} volume={() => volume} />;
+
+  return null;
 };
diff --git a/template/src/Narration/mode.ts b/template/src/Narration/mode.ts
new file mode 100644
index 0000000..14d8db8
--- /dev/null
+++ b/template/src/Narration/mode.ts
@@ -0,0 +1,41 @@
+import { getStaticFiles } from 'remotion';
+import { narrationData } from './narrationData';
+import type { NarrationSegment } from './types';
+
+export const NARRATION_LEGACY_FILE = 'narration.wav';
+
+/**
+ * Phase 3-H Codex review P1 #1 反映:
+ * NarrationAudio と MainVideo が narration の状態を別々に判定すると、
+ * chunk 不足 + legacy 存在で「narration も base 元音声も無音」になる
+ * 矛盾モードが発生する。本 helper を両者から呼ぶことで mode を一元化する。
+ */
+export type NarrationMode =
+  | { kind: 'chunks'; segments: readonly NarrationSegment[] }
+  | { kind: 'legacy'; file: string }
+  | { kind: 'none' };
+
+/**
+ * narration の有効モードを返す。優先順位:
+ *   1) narrationData が non-empty + 全 chunk file が public/ 配下に存在 → chunks
+ *   2) public/narration.wav 存在 → legacy
+ *   3) どちらも不在 → none
+ *
+ * getStaticFiles() の結果を一度 Set 化して O(1) lookup
+ * (Codex P3 #8 反映、毎 frame の some() 重複を防ぐ)。
+ *
+ * 出典: https://www.remotion.dev/docs/getstaticfiles
+ */
+export const getNarrationMode = (): NarrationMode => {
+  const names = new Set(getStaticFiles().map((f) => f.name));
+  if (
+    narrationData.length > 0 &&
+    narrationData.every((seg) => names.has(seg.file))
+  ) {
+    return { kind: 'chunks', segments: narrationData };
+  }
+  if (names.has(NARRATION_LEGACY_FILE)) {
+    return { kind: 'legacy', file: NARRATION_LEGACY_FILE };
+  }
+  return { kind: 'none' };
+};

codex
実装経路の大枠は見えています。追加で、`narrationData` 型、Root の FPS 利用、eslint/visual-smoke の現状、過去 phase の文書があるかを確認して Part B の推奨を repo 状態に寄せます。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba package.json && nl -ba template/package.json && nl -ba template/eslint.config.mjs' in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
nl: package.json: No such file or directory

exec
/bin/zsh -lc 'nl -ba template/src/Narration/types.ts && nl -ba template/src/Narration/narrationData.ts && nl -ba template/src/Root.tsx && nl -ba template/src/videoConfig.ts' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	/**
     2	 * Phase 3-H: per-segment narration timeline 用の型定義。
     3	 * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
     4	 * (https://www.remotion.dev/docs/sequence)。
     5	 */
     6	export interface NarrationSegment {
     7	  /** chunk index (0-based、生成順) */
     8	  id: number;
     9	  /** timeline 上での開始 frame (前 chunk の累積 duration) */
    10	  startFrame: number;
    11	  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
    12	  durationInFrames: number;
    13	  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
    14	  file: string;
    15	  /** debug 用に元 transcript text を保持 (省略可) */
    16	  text?: string;
    17	}
     1	/**
     2	 * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
     3	 * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
     4	 */
     5	import type { NarrationSegment } from './types';
     6	
     7	export const narrationData: NarrationSegment[] = [];
     1	import "./index.css";
     2	import { Composition } from "remotion";
     3	import { MainVideo } from "./MainVideo";
     4	import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
     5	
     6	// cut phase 完了後は cutData の CUT_TOTAL_FRAMES に切替: import { CUT_TOTAL_FRAMES } from "./cutData";
     7	export const RemotionRoot: React.FC = () => {
     8	  return (
     9	    <>
    10	      <Composition
    11	        id="MainVideo"
    12	        component={MainVideo}
    13	        durationInFrames={SOURCE_DURATION_FRAMES}
    14	        fps={FPS}
    15	        width={RESOLUTION.width}
    16	        height={RESOLUTION.height}
    17	      />
    18	    </>
    19	  );
    20	};
     1	// ==== 動画設定（Single Source of Truth） ====
     2	// /supermovie-init が自動設定します
     3	// format に応じて全コンポーネントが参照する値を一元管理
     4	
     5	export type VideoFormat = 'youtube' | 'short' | 'square';
     6	
     7	// ---- ここを /supermovie-init が書き換える ----
     8	export const FORMAT: VideoFormat = 'youtube';
     9	export const FPS = 30;
    10	// 元動画 (source) の総フレーム数。cut 後の総フレームは cutData.ts の CUT_TOTAL_FRAMES を使う
    11	export const SOURCE_DURATION_FRAMES = 1500; // placeholder
    12	export const VIDEO_FILE = 'main.mp4';
    13	// ---- ここまで ----
    14	
    15	// フォーマット別の解像度
    16	const RESOLUTION_MAP = {
    17	  youtube: { width: 1920, height: 1080 },
    18	  short: { width: 1080, height: 1920 },
    19	  square: { width: 1080, height: 1080 },
    20	} as const;
    21	
    22	// フォーマット別のテロップ設定
    23	const TELOP_CONFIG_MAP = {
    24	  youtube: {
    25	    fontSize: 80,
    26	    titleFontSize: 42,
    27	    maxCharsPerLine: 18,
    28	    lineBreakThreshold: 15,
    29	    maxCharsPerTelop: 36,
    30	    bottomOffset: 100,
    31	    titleTop: 40,
    32	    titleLeft: 40,
    33	    maxWidth: '85%',
    34	    containerPadding: '0 60px',
    35	    readingSpeed: 5, // 文字/秒
    36	  },
    37	  short: {
    38	    fontSize: 56,
    39	    titleFontSize: 30,
    40	    maxCharsPerLine: 12,
    41	    lineBreakThreshold: 10,
    42	    maxCharsPerTelop: 24,
    43	    bottomOffset: 200,
    44	    titleTop: 60,
    45	    titleLeft: 30,
    46	    maxWidth: '92%',
    47	    containerPadding: '0 30px',
    48	    readingSpeed: 4,
    49	  },
    50	  square: {
    51	    fontSize: 66,
    52	    titleFontSize: 36,
    53	    maxCharsPerLine: 15,
    54	    lineBreakThreshold: 12,
    55	    maxCharsPerTelop: 30,
    56	    bottomOffset: 140,
    57	    titleTop: 40,
    58	    titleLeft: 30,
    59	    maxWidth: '90%',
    60	    containerPadding: '0 40px',
    61	    readingSpeed: 4.5,
    62	  },
    63	} as const;
    64	
    65	// エクスポート（全コンポーネントがこれを参照する）
    66	export const RESOLUTION = RESOLUTION_MAP[FORMAT];
    67	export const TELOP_CONFIG = TELOP_CONFIG_MAP[FORMAT];

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg --files | sort | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
CLAUDE.md
LICENSE
README.md
agents.disabled/skill-architect.md
agents.disabled/skill-auditor.md
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md
skills/supermovie-cut/SKILL.md
skills/supermovie-image-gen/SKILL.md
skills/supermovie-init/SKILL.md
skills/supermovie-narration/SKILL.md
skills/supermovie-se/SKILL.md
skills/supermovie-skill-creator/SKILL.md
skills/supermovie-slides/SKILL.md
skills/supermovie-subtitles/SKILL.md
skills/supermovie-telop-creator/SKILL.md
skills/supermovie-transcribe/SKILL.md
skills/supermovie-transcript-fix/SKILL.md
sm-claude.sh
template/eslint.config.mjs
template/package.json
template/remotion.config.ts
template/scripts/budoux_split.mjs
template/scripts/build_slide_data.py
template/scripts/build_telop_data.py
template/scripts/compare_telop_split.py
template/scripts/generate_slide_plan.py
template/scripts/preflight_video.py
template/scripts/visual_smoke.py
template/scripts/voicevox_narration.py
template/src/InsertImage/ImageSequence.tsx
template/src/InsertImage/InsertImage.tsx
template/src/InsertImage/index.ts
template/src/InsertImage/insertImageData.ts
template/src/InsertImage/types.ts
template/src/MainVideo.tsx
template/src/Narration/NarrationAudio.tsx
template/src/Narration/index.ts
template/src/Narration/mode.ts
template/src/Narration/narrationData.ts
template/src/Narration/types.ts
template/src/Root.tsx
template/src/Slides/Slide.tsx
template/src/Slides/SlideSequence.tsx
template/src/Slides/index.tsx
template/src/Slides/slideData.ts
template/src/Slides/types.ts
template/src/SoundEffects/BGM.tsx
template/src/SoundEffects/SEPlayer.ts
template/src/SoundEffects/SESequence.tsx
template/src/SoundEffects/seData.ts
template/src/Title/Title.tsx
template/src/Title/index.ts
template/src/Title/titleData.ts
template/src/index.css
template/src/index.ts
template/src/videoConfig.ts
template/src/テロップテンプレート/Telop.tsx
template/src/テロップテンプレート/TelopPlayer.tsx
template/src/テロップテンプレート/index.tsx
template/src/テロップテンプレート/telopData.ts
template/src/テロップテンプレート/telopStyles.ts
template/src/テロップテンプレート/telopTemplateRegistry.tsx
template/src/テロップテンプレート/telopTypes.ts
template/src/ネガティブテロップ/残酷テロップ・紺.tsx
template/src/ネガティブテロップ/白文字紫シャドウ.tsx
template/src/ネガティブテロップ/紫文字白背景.tsx
template/src/ネガティブテロップ/黒文字白背景.tsx
template/src/ネガティブテロップ/黒紫グラデ.tsx
template/src/メインテロップ/白文字青ピンク背景グラデ.tsx
template/src/メインテロップ/白文字黒シャドウ.tsx
template/src/メインテロップ/白文字黒シャドウゴシック.tsx
template/src/メインテロップ/白文字黒シャドウ明朝体.tsx
template/src/メインテロップ/白文字黒背景.tsx
template/src/メインテロップ/白背景グラデ.tsx
template/src/メインテロップ/白青テロップ.tsx
template/src/メインテロップ/白青テロップver2.tsx
template/src/メインテロップ/白黒テロップ.tsx
template/src/メインテロップ/緑文字白背景.tsx
template/src/メインテロップ/青文字白背景.tsx
template/src/メインテロップ/黒文字.tsx
template/src/強調テロップ/オレンジグラデーション.tsx
template/src/強調テロップ/白文字赤シャドウ.tsx
template/src/強調テロップ/白緑テロップ.tsx
template/src/強調テロップ/白赤テロップ.tsx
template/src/強調テロップ/白赤テロップver2.tsx
template/src/強調テロップ/緑グラデ金シャドウ.tsx
template/src/強調テロップ/赤文字.tsx
template/src/強調テロップ/赤文字白背景.tsx
template/src/強調テロップ/金グラデ・紺背景.tsx
template/src/強調テロップ/青文字金枠.tsx
template/src/強調テロップ/黄色シャドウ.tsx
template/src/強調テロップ/黄色文字黒シャドウ.tsx
template/src/強調テロップ/黒文字黄色背景.tsx
template/tsconfig.json

exec
/bin/zsh -lc "rg -n \"visual-smoke|slide_plan|slide_plan\\.v|scene_plan|transcript_fixed|b-roll|broll|no-explicit-any|any\" ." in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
./LICENSE:5:Permission is hereby granted, free of charge, to any person obtaining a copy
./CLAUDE.md:11:    ↓ transcript_fixed.json
./CLAUDE.md:15:/supermovie-subtitles         ← transcript_fixed.json → telopData.ts + titleData.ts
./CLAUDE.md:142:### transcript.json / transcript_fixed.json
./CLAUDE.md:162:- transcript_fixed.json は追加で `fix_meta` を持つ
./CLAUDE.md:234:| 文字起こし修正済み | `<PROJECT>/transcript_fixed.json` |
./CLAUDE.md:264:| `transcript_fixed.json` | transcript_corrected.json |
./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./CLAUDE.md:324:- `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
./agents.disabled/skill-architect.md:140:    ↓ transcript_fixed.json
./skills/supermovie-skill-creator/SKILL.md:170:    ↓ transcript_fixed.json
./agents.disabled/skill-auditor.md:45:- [ ] transcript.json / transcript_fixed.json のスキーマが全スキルで同一か
./skills/supermovie-se/SKILL.md:204:    ↓ transcript_fixed.json
./template/eslint.config.mjs:6:// telop-templates-30.zip 由来の component が `any` を使っているため、
./template/eslint.config.mjs:7:// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
./template/eslint.config.mjs:12:      "@typescript-eslint/no-explicit-any": "warn",
./template/scripts/voicevox_narration.py:2:"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
./template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./template/scripts/voicevox_narration.py:335:    transcript_path = PROJ / "transcript_fixed.json"
./template/scripts/voicevox_narration.py:337:        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:20:- Phase 3-C: LLM optional plan (claude-haiku-4-5) + slide_plan.v1 schema validate
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:22:- Phase 3-E: lint unblock (eslint-config-flat 4.x default export 修正、no-explicit-any warn)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:37:v. Phase 3-H minimal: any 警告ゼロ化 (no-explicit-any error 化、telop template の TODO 残)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:485:template/scripts/generate_slide_plan.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:557:    20	- Phase 3-C: LLM optional plan (claude-haiku-4-5) + slide_plan.v1 schema validate
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:559:    22	- Phase 3-E: lint unblock (eslint-config-flat 4.x default export 修正、no-explicit-any warn)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:574:    37	v. Phase 3-H minimal: any 警告ゼロ化 (no-explicit-any error 化、telop template の TODO 残)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:846:     2	"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:850:     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:992:   148	    transcript_path = PROJ / "transcript_fixed.json"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:994:   150	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1354:   485	template/scripts/generate_slide_plan.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1403:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1449:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1507:   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1515:   116	    ↓ transcript_fixed.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2252:   557	    20	- Phase 3-C: LLM optional plan (claude-haiku-4-5) + slide_plan.v1 schema validate
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2254:   559	    22	- Phase 3-E: lint unblock (eslint-config-flat 4.x default export 修正、no-explicit-any warn)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2269:   574	    37	v. Phase 3-H minimal: any 警告ゼロ化 (no-explicit-any error 化、telop template の TODO 残)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2541:   846	     2	"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2545:   850	     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3023:     6	// telop-templates-30.zip 由来の component が `any` を使っているため、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3024:     7	// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3029:    12	      "@typescript-eslint/no-explicit-any": "warn",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3057:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3099:template/scripts/voicevox_narration.py:2:"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3119:template/src/テロップテンプレート/Telop.tsx:126:  config: any;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3120:template/src/テロップテンプレート/Telop.tsx:127:  animation: any;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3121:template/src/テロップテンプレート/Telop.tsx:131:  const charDelay = (animation as any).charDelay || 2;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3122:template/src/テロップテンプレート/Telop.tsx:133:  const fillGradient = (font as any).fillGradient;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3123:template/src/テロップテンプレート/Telop.tsx:249:  const slideDirection = (animation as any).slideDirection || 'up';
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3124:template/src/テロップテンプレート/Telop.tsx:320:    const fillGradient = (font as any).fillGradient;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3125:template/src/テロップテンプレート/Telop.tsx:394:  const strokeGradient = (textStroke as any).gradient || { start: '#ffffff', end: '#ffffff' };
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3126:template/src/テロップテンプレート/Telop.tsx:395:  const fillGradient = (font as any).fillGradient;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3127:template/src/テロップテンプレート/Telop.tsx:397:  const textOpacity = (font as any).opacity ?? 1;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3148:template/eslint.config.mjs:6:// telop-templates-30.zip 由来の component が `any` を使っているため、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3149:template/eslint.config.mjs:7:// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3150:template/eslint.config.mjs:12:      "@typescript-eslint/no-explicit-any": "warn",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3165:     2	"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3170:     7	    <PROJECT>/transcript_fixed.json  - segments[] / words[]
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3346:   183	        f"// {len(slides)} slides を transcript_fixed.json から生成",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3379:   216	PLAN_VERSION = "supermovie.slide_plan.v1"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3384:   221	def validate_slide_plan(plan: dict, words: list[dict], cut_total_frames: int | None,
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3429:     2	"""SuperMovie subtitles phase: transcript_fixed.json → telopData.ts (BudouX 分割版).
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3445:    18	入力: transcript_fixed.json + vad_result.json + (optional) typo_dict.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3699:     4	  transcript_fixed.json と project-config.json から SlideSegment[] を生成し、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3710:    15	Senior video editor として、transcript_fixed.json の segments から話題区間を抽出し、
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3727:    32	- `<PROJECT>/transcript_fixed.json` から `segments[]` (start/end ms + text) と `words[]`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3795:   100	ANTHROPIC_API_KEY=sk-ant-... python3 <PROJECT>/scripts/generate_slide_plan.py \
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3796:   101	  --output <PROJECT>/slide_plan.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3797:   102	python3 <PROJECT>/scripts/build_slide_data.py --plan <PROJECT>/slide_plan.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3806:   111	### slide_plan.json schema
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3810:   115	  "version": "supermovie.slide_plan.v1",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3828:   133	- `version` 完全一致 (`supermovie.slide_plan.v1`)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3867:   172	    ↓ transcript_fixed.json + cutData.ts
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4333:**P0 推奨: i. per-segment narration `<Sequence>` 化。次点: v. any 警告ゼロ化。**
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4335:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4391:**P0 推奨: i. per-segment narration `<Sequence>` 化。次点: v. any 警告ゼロ化。**
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4393:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./template/scripts/generate_slide_plan.py:2:"""SuperMovie Phase 3-C optional script: Anthropic API で slide_plan.json を生成.
./template/scripts/generate_slide_plan.py:5:- LLM は word index ベースの slide_plan.json を返す (frame は build_slide_data.py が変換)
./template/scripts/generate_slide_plan.py:10:    ANTHROPIC_API_KEY=sk-ant-... python3 scripts/generate_slide_plan.py \\
./template/scripts/generate_slide_plan.py:11:        --output slide_plan.json [--model claude-haiku-4-5-20251001]
./template/scripts/generate_slide_plan.py:22:PLAN_VERSION = "supermovie.slide_plan.v1"
./template/scripts/generate_slide_plan.py:25:あなたは動画編集者です。SuperMovie パイプラインの slide_plan を返してください。
./template/scripts/generate_slide_plan.py:75:    ap.add_argument("--output", default=str(PROJ / "slide_plan.json"))
./template/scripts/generate_slide_plan.py:82:        print("INFO: ANTHROPIC_API_KEY 未設定 → slide_plan 生成 skip")
./template/scripts/generate_slide_plan.py:86:    transcript_path = PROJ / "transcript_fixed.json"
./template/scripts/generate_slide_plan.py:89:        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
./skills/supermovie-transcript-fix/SKILL.md:265:**transcript_fixed.json** — 修正済み:
./skills/supermovie-transcript-fix/SKILL.md:346:  transcript_fixed.json（修正済み）
./skills/supermovie-transcript-fix/SKILL.md:350:→ transcript_fixed.json を確認
./skills/supermovie-transcript-fix/SKILL.md:379:    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:814:    11	    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:818:    15	/supermovie-subtitles         ← transcript_fixed.json → telopData.ts + titleData.ts
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:945:   142	### transcript.json / transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:965:   162	- transcript_fixed.json は追加で `fix_meta` を持つ
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1037:   234	| 文字起こし修正済み | `<PROJECT>/transcript_fixed.json` |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1067:   264	| `transcript_fixed.json` | transcript_corrected.json |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1127:   324	- `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1139:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1185:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1243:   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1251:   116	    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1438:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1532: | `transcript_fixed.json` | transcript_corrected.json |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2040:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1507:   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2048:./skills/supermovie-narration/SKILL.md:108:| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2068:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1243:   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2302: | 文字起こし修正済み | `<PROJECT>/transcript_fixed.json` |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2333: | `transcript_fixed.json` | transcript_corrected.json |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2371: - `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2534:   VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2580: 3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2647: | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2655:     ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2823: | 文字起こし修正済み | `<PROJECT>/transcript_fixed.json` |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2853: | `transcript_fixed.json` | transcript_corrected.json |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2913: - `supermovie-subtitles` は `transcript_fixed.json` を読む。独自の文字起こしは行わない
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4588:skills/supermovie-transcript-fix/SKILL.md:350:→ transcript_fixed.json を確認
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4983:     6	// telop-templates-30.zip 由来の component が `any` を使っているため、
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4984:     7	// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4989:    12	      "@typescript-eslint/no-explicit-any": "warn",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5168:   148	    transcript_path = PROJ / "transcript_fixed.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5170:   150	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./skills/supermovie-subtitles/SKILL.md:4:  transcript_fixed.jsonからテロップ（telopData.ts）とタイトル（titleData.ts）を
./skills/supermovie-subtitles/SKILL.md:37:- [ ] `transcript_fixed.json` が存在し `words` 配列がある
./skills/supermovie-subtitles/SKILL.md:68:- `transcript_fixed.json` → `words`, `segments`
./skills/supermovie-subtitles/SKILL.md:88:transcript_fixed.json の `words` を `segments` 単位でグループ化。
./skills/supermovie-subtitles/SKILL.md:403:transcript_fixed.json の `segments` を俯瞰し、話題の転換点を検出。
./skills/supermovie-subtitles/SKILL.md:513:| transcript_fixed.json なし | `/supermovie-transcribe` → `/supermovie-transcript-fix` を促す |
./skills/supermovie-subtitles/SKILL.md:531:    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:19:2. `git diff roku/phase3g-visual-smoke..HEAD` で Phase 3-H 範囲確認
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:43:   - tsc strict mode で any 漏れ・unused warn
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:105:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:107:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:108:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:200:/bin/zsh -lc 'git diff --name-status roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:238:-"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:239:+"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:244: - 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:508:/bin/zsh -lc 'git diff --stat roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:527:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/visual_smoke.py skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:707: 3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:784: | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:920:     2	"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:924:     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1196:   278	    transcript_path = PROJ / "transcript_fixed.json"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1198:   280	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1494:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1540:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1616:   126	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1625:   135	    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1710:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1768:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2039:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2050:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3099:template/scripts/voicevox_narration.py:2:"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2078:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4335:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2089:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4393:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2148:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2149:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1335:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2150:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1432:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2401:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2402:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2437:     6	// telop-templates-30.zip 由来の component が `any` を使っているため、
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2438:     7	// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2443:    12	      "@typescript-eslint/no-explicit-any": "warn",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2486:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2712:/bin/zsh -lc "git grep -n -- 'voicevox_narration.py' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2714:/bin/zsh -lc "git grep -n -- '--keep-chunks' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2720:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2721:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2722:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2723:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2724:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2725:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2726:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2727:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2728:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:12:    python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2729:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:13:    python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2730:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:14:    python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2731:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:15:    python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2732:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:16:    python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2733:roku/phase3g-visual-smoke:template/src/Narration/NarrationAudio.tsx:15: * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2740:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:59:`--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2741:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2742:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:121:    ap.add_argument("--keep-chunks", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3059:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD --name-only' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3091:     2	"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3096:     7	    <PROJECT>/transcript_fixed.json  - segments[] / words[]
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3189:template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3197:template/scripts/generate_slide_plan.py:87:    config_path = PROJ / "project-config.json"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3198:template/scripts/generate_slide_plan.py:89:        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3205:template/scripts/build_slide_data.py:2:"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3209:template/scripts/build_slide_data.py:322:        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3263:/bin/zsh -lc 'git diff --check roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3495:   250	    if any(f < 0 for f in frames):
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3508:   263	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3620:    fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3700:/bin/zsh -lc "git show roku/phase3g-visual-smoke:template/scripts/visual_smoke.py | nl -ba | sed -n '135,215p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3805:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3854:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
./template/scripts/compare_telop_split.py:138:    transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
./skills/supermovie-image-gen/SKILL.md:286:    ↓ transcript_fixed.json
./skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./skills/supermovie-narration/SKILL.md:50:3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./skills/supermovie-narration/SKILL.md:126:| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./skills/supermovie-narration/SKILL.md:137:    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:471:   237	    if any(f < 0 for f in frames):
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:685:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:731:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:789:   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:797:   116	    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:826:/bin/zsh -lc "rg -n \"visual-smoke|visual_smoke|test:visual-smoke|summary\\.json|mismatched|env_error|grid\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:828:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:829:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:833:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:834:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:838:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:839:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:840:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:868:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:872:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:874:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:876:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:877:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:879:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:880:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:881:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:882:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:883:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:884:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:885:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:903:./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:933:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:936:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:941:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:942:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:943:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:944:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:948:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:949:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:950:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:958:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:963:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:964:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:982:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1012:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1016:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1018:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1020:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1022:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1023:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1024:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1048:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1068:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1069:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1073:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1074:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1075:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1100:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1101:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1102:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1105:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1106:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1107:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1110:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1111:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1112:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1113:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1114:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1115:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1116:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1119:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1120:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1123:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1124:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1127:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1128:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1129:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1134:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1135:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1136:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1141:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1144:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1149:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1151:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1152:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1156:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1157:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1158:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1183:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1184:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1185:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1205:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1206:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1215:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1216:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1223:/bin/zsh -lc 'rg -n "exit 2|exit code|npm run test|visual smoke|visual-smoke" .' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1225:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1226:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1231:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1232:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1233:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1235:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1236:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1237:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1238:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1239:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1240:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1242:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1243:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1245:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1246:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1248:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1249:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1250:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1252:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1253:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1254:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1258:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1259:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1260:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1261:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1262:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1263:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1264:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1265:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1266:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1267:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1268:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1269:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1271:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1272:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1274:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1275:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1276:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1278:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1279:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1280:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1281:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1282:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1284:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1285:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1286:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1288:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1289:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1290:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1292:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1293:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1294:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1298:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1299:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1302:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1303:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1304:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1305:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1307:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1308:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1309:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1310:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1312:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1313:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1314:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1315:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1317:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1318:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1320:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1321:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:826:/bin/zsh -lc "rg -n \"visual-smoke|visual_smoke|test:visual-smoke|summary\\.json|mismatched|env_error|grid\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1322:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:828:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1323:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:829:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1325:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:833:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1326:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:834:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1327:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:838:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1328:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:839:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1329:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:840:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1330:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:868:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1331:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:872:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1332:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:874:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1333:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:876:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1334:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:877:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1335:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1336:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:879:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1337:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:880:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1338:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:881:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1339:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:882:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1340:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:883:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1341:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:884:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1342:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:885:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1343:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:903:./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1344:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:933:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1345:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:936:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1346:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:941:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1347:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:942:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1348:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:943:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1349:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:944:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1350:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:948:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1351:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:949:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1352:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:950:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1353:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:958:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1355:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:963:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1356:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:964:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1357:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:982:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1358:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1012:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1359:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1016:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1360:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1018:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1361:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1020:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1362:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1022:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1363:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1023:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1364:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1024:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1365:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1048:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1366:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1368:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1068:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1369:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1069:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1371:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1073:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1372:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1074:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1373:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1075:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1374:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1100:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1375:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1101:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1376:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1102:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1378:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1105:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1379:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1106:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1380:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1107:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1381:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1110:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1382:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1111:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1383:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1112:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1384:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1113:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1385:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1114:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1386:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1115:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1387:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1116:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1388:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1119:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1389:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1120:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1391:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1123:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1392:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1124:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1394:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1127:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1395:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1128:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1396:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1129:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1397:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1134:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1398:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1135:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1399:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1136:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1400:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1141:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1401:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1144:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1403:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1149:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1404:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1151:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1405:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1152:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1407:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1156:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1408:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1157:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1409:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1158:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1410:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1183:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1411:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1184:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1412:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1185:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1414:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1205:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1415:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1206:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1417:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1215:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1418:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1216:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1421:./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1422:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1423:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1424:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1426:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1428:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1429:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1430:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1431:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1432:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1433:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1434:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1435:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1436:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1437:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1440:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1441:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1454:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1466:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1468:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1469:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1491:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1615:+    if any(f < 0 for f in frames):
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1629:+        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2080:   264	| `transcript_fixed.json` | transcript_corrected.json |
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2087:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2088:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2261:/bin/zsh -lc "rg -n \"test:visual-smoke|visual-smoke|npm run test|summary\\.json|mismatched|env_error|grid\" template skills CLAUDE.md README.md .github .codex 2>/dev/null" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2263:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2264:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2267:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2268:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2282:template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2407:template/scripts/generate_slide_plan.py
./template/src/テロップテンプレート/Telop.tsx:126:  config: any;
./template/src/テロップテンプレート/Telop.tsx:127:  animation: any;
./template/src/テロップテンプレート/Telop.tsx:131:  const charDelay = (animation as any).charDelay || 2;
./template/src/テロップテンプレート/Telop.tsx:133:  const fillGradient = (font as any).fillGradient;
./template/src/テロップテンプレート/Telop.tsx:249:  const slideDirection = (animation as any).slideDirection || 'up';
./template/src/テロップテンプレート/Telop.tsx:320:    const fillGradient = (font as any).fillGradient;
./template/src/テロップテンプレート/Telop.tsx:394:  const strokeGradient = (textStroke as any).gradient || { start: '#ffffff', end: '#ffffff' };
./template/src/テロップテンプレート/Telop.tsx:395:  const fillGradient = (font as any).fillGradient;
./template/src/テロップテンプレート/Telop.tsx:397:  const textOpacity = (font as any).opacity ?? 1;
./skills/supermovie-cut/SKILL.md:5:  Silero VAD + transcript_fixed.json + Claude LLM分析の3層で高精度にカット判定。
./skills/supermovie-cut/SKILL.md:34:- [ ] `transcript_fixed.json` が存在し `words` 配列がある
./skills/supermovie-cut/SKILL.md:172:transcript_fixed.json の words 間のギャップからも無音を検出。
./skills/supermovie-cut/SKILL.md:193:transcript_fixed.json のテキストを分析し、**内容的に不要な区間**を判定。
./skills/supermovie-cut/SKILL.md:405:| transcript_fixed.json がない | `/supermovie-transcript-fix` を促す |
./skills/supermovie-cut/SKILL.md:420:    ↓ transcript_fixed.json
./skills/supermovie-init/SKILL.md:274:    ↓ transcript_fixed.json
./template/scripts/build_telop_data.py:2:"""SuperMovie subtitles phase: transcript_fixed.json → telopData.ts (BudouX 分割版).
./template/scripts/build_telop_data.py:18:入力: transcript_fixed.json + vad_result.json + (optional) typo_dict.json
./template/scripts/build_telop_data.py:271:    transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
./template/scripts/build_telop_data.py:395:        "// transcript_fixed.json の segments を BudouX phrase 単位で分割し、",
./skills/supermovie-slides/SKILL.md:4:  transcript_fixed.json と project-config.json から SlideSegment[] を生成し、
./skills/supermovie-slides/SKILL.md:15:Senior video editor として、transcript_fixed.json の segments から話題区間を抽出し、
./skills/supermovie-slides/SKILL.md:32:- `<PROJECT>/transcript_fixed.json` から `segments[]` (start/end ms + text) と `words[]`
./skills/supermovie-slides/SKILL.md:100:ANTHROPIC_API_KEY=sk-ant-... python3 <PROJECT>/scripts/generate_slide_plan.py \
./skills/supermovie-slides/SKILL.md:101:  --output <PROJECT>/slide_plan.json
./skills/supermovie-slides/SKILL.md:102:python3 <PROJECT>/scripts/build_slide_data.py --plan <PROJECT>/slide_plan.json
./skills/supermovie-slides/SKILL.md:111:### slide_plan.json schema
./skills/supermovie-slides/SKILL.md:115:  "version": "supermovie.slide_plan.v1",
./skills/supermovie-slides/SKILL.md:133:- `version` 完全一致 (`supermovie.slide_plan.v1`)
./skills/supermovie-slides/SKILL.md:172:    ↓ transcript_fixed.json + cutData.ts
./skills/supermovie-transcribe/SKILL.md:500:    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:45:i. **any 警告ゼロ化** (Phase 3-E から残置)
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:46:   - eslint.config.mjs の no-explicit-any を warning から error に
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:47:   - telop-templates-30.zip 由来の component の any を実型に置換
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:50:ii. **slide_plan.v2 schema 拡張** (Phase 3-C 延長)
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:51:   - Phase 3-C の slide_plan.v1 に transition / animation / theme を追加
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:55:iii. **transcript-driven b-roll planner** (新領域、Roku ビジョン関連)
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:56:   - LLM が transcript_fixed.json を読んで「ここに静止画 / ここに動画」と判定
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:57:   - insertImageData.ts / video2 拡張に流す scene_plan.json 生成
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:62:   - GitHub Actions で `npm run visual-smoke` を generated project 上で実行
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:68:   - transcript_fixed.json segments[].start を base にした tight alignment
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:400:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:446:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:522:   126	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:533:   137	    ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:570:     2	"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:574:     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:906:   335	    transcript_path = PROJ / "transcript_fixed.json"
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:908:   337	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1016:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1040:template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1178: | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1190:     ↓ transcript_fixed.json
./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1706:実装経路の大枠は見えています。追加で、`narrationData` 型、Root の FPS 利用、eslint/visual-smoke の現状、過去 phase の文書があるかを確認して Part B の推奨を repo 状態に寄せます。
./template/scripts/build_slide_data.py:2:"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
./template/scripts/build_slide_data.py:7:    <PROJECT>/transcript_fixed.json  - segments[] / words[]
./template/scripts/build_slide_data.py:183:        f"// {len(slides)} slides を transcript_fixed.json から生成",
./template/scripts/build_slide_data.py:216:PLAN_VERSION = "supermovie.slide_plan.v1"
./template/scripts/build_slide_data.py:221:def validate_slide_plan(plan: dict, words: list[dict], cut_total_frames: int | None,
./template/scripts/build_slide_data.py:314:    ap.add_argument("--plan", help="optional slide_plan.json (LLM 生成)")
./template/scripts/build_slide_data.py:319:    transcript_path = PROJ / "transcript_fixed.json"
./template/scripts/build_slide_data.py:322:        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
./template/scripts/build_slide_data.py:346:            errors = validate_slide_plan(plan, words, cut_total_frames, fmt)
./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./template/scripts/visual_smoke.py:250:    if any(f < 0 for f in frames):
./template/scripts/visual_smoke.py:263:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
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
    35	    "test": "npm run lint"
    36	  },
    37	  "sideEffects": [
    38	    "*.css"
    39	  ]
    40	}

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
/bin/zsh -lc "nl -ba template/scripts/build_slide_data.py | sed -n '200,390p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   200	                + " }"
   201	                for b in s["bullets"]
   202	            )
   203	            parts.append(f"bullets: [{bullets_ts}]")
   204	        if s.get("align"):
   205	            parts.append(f"align: '{s['align']}'")
   206	        if s.get("backgroundColor"):
   207	            parts.append(f"backgroundColor: {json.dumps(s['backgroundColor'], ensure_ascii=False)}")
   208	        if s.get("videoLayer"):
   209	            parts.append(f"videoLayer: '{s['videoLayer']}'")
   210	        lines.append("  { " + ", ".join(parts) + " },")
   211	    lines.append("];")
   212	    lines.append("")
   213	    return "\n".join(lines)
   214	
   215	
   216	PLAN_VERSION = "supermovie.slide_plan.v1"
   217	ALLOWED_ALIGN = ("center", "left")
   218	ALLOWED_VIDEO_LAYER = ("visible", "dimmed", "hidden")
   219	
   220	
   221	def validate_slide_plan(plan: dict, words: list[dict], cut_total_frames: int | None,
   222	                        fmt: str) -> list[str]:
   223	    """Codex Phase 3-C validate (Q4) を実装。invalid なら理由を返す (空 list = OK)."""
   224	    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
   225	    bullet_max = BULLET_MAX_CHARS.get(fmt, BULLET_MAX_CHARS["short"])
   226	    errors: list[str] = []
   227	    if not isinstance(plan, dict):
   228	        return ["plan is not a dict"]
   229	    if plan.get("version") != PLAN_VERSION:
   230	        errors.append(f"version mismatch (expect {PLAN_VERSION})")
   231	    slides = plan.get("slides")
   232	    if not isinstance(slides, list):
   233	        errors.append("slides is not a list")
   234	        return errors
   235	    n_words = len(words)
   236	    last_end_idx = -1
   237	    last_id = 0
   238	    for i, s in enumerate(slides):
   239	        if not isinstance(s, dict):
   240	            errors.append(f"slides[{i}] not a dict")
   241	            continue
   242	        sid = s.get("id")
   243	        if not isinstance(sid, int) or sid <= last_id:
   244	            errors.append(f"slides[{i}].id must be ascending int (got {sid})")
   245	        else:
   246	            last_id = sid
   247	        sw = s.get("startWordIndex")
   248	        ew = s.get("endWordIndex")
   249	        if not (isinstance(sw, int) and isinstance(ew, int)
   250	                and 0 <= sw <= ew < n_words):
   251	            errors.append(f"slides[{i}] startWordIndex/endWordIndex out of range (got {sw}/{ew}, words={n_words})")
   252	            continue
   253	        if sw <= last_end_idx:
   254	            errors.append(f"slides[{i}] word range overlaps previous (sw={sw} <= prev end {last_end_idx})")
   255	        last_end_idx = ew
   256	        title = s.get("title")
   257	        if not isinstance(title, str) or not title.strip():
   258	            errors.append(f"slides[{i}].title empty")
   259	        elif len(title) > title_max:
   260	            errors.append(f"slides[{i}].title too long ({len(title)} > {title_max})")
   261	        bullets = s.get("bullets") or []
   262	        if not isinstance(bullets, list) or len(bullets) > MAX_BULLETS_PER_SLIDE:
   263	            errors.append(f"slides[{i}].bullets exceeds {MAX_BULLETS_PER_SLIDE}")
   264	        else:
   265	            for j, b in enumerate(bullets):
   266	                bt = b.get("text") if isinstance(b, dict) else None
   267	                if not isinstance(bt, str) or not bt.strip():
   268	                    errors.append(f"slides[{i}].bullets[{j}] empty text")
   269	                elif len(bt) > bullet_max:
   270	                    errors.append(f"slides[{i}].bullets[{j}] too long ({len(bt)} > {bullet_max})")
   271	        align = s.get("align")
   272	        if align is not None and align not in ALLOWED_ALIGN:
   273	            errors.append(f"slides[{i}].align invalid ({align})")
   274	        video_layer = s.get("videoLayer")
   275	        if video_layer is not None and video_layer not in ALLOWED_VIDEO_LAYER:
   276	            errors.append(f"slides[{i}].videoLayer invalid ({video_layer})")
   277	    return errors
   278	
   279	
   280	def build_slides_from_plan(plan: dict, words: list[dict], cut_segments: list[dict],
   281	                           fmt: str, tone: str) -> list[dict]:
   282	    """validated plan を SlideSegment dict 列に変換 (frame は script 側で計算)."""
   283	    style = style_for_tone(tone)
   284	    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
   285	    slides: list[dict] = []
   286	    for s in plan["slides"]:
   287	        sw = s["startWordIndex"]
   288	        ew = s["endWordIndex"]
   289	        ms_start = words[sw].get("start", 0)
   290	        ms_end = words[ew].get("end", 0)
   291	        pb_start = ms_to_playback_frame(ms_start, cut_segments)
   292	        pb_end = ms_to_playback_frame(ms_end, cut_segments)
   293	        if pb_start is None or pb_end is None or pb_end <= pb_start:
   294	            continue
   295	        if cut_total is not None:
   296	            pb_end = min(pb_end, cut_total)
   297	        slides.append({
   298	            "id": s["id"],
   299	            "startFrame": pb_start,
   300	            "endFrame": pb_end,
   301	            "title": s["title"],
   302	            "subtitle": s.get("subtitle"),
   303	            "bullets": s.get("bullets") or None,
   304	            "align": s.get("align") or style["align"],
   305	            "backgroundColor": s.get("backgroundColor") or style["bg"],
   306	            "videoLayer": s.get("videoLayer") or "visible",
   307	        })
   308	    return slides
   309	
   310	
   311	def main():
   312	    ap = argparse.ArgumentParser()
   313	    ap.add_argument("--mode", choices=["topic", "segment"], default="topic")
   314	    ap.add_argument("--plan", help="optional slide_plan.json (LLM 生成)")
   315	    ap.add_argument("--strict-plan", action="store_true",
   316	                    help="--plan の validate 失敗時に exit 2 (default は warning + deterministic fallback)")
   317	    args = ap.parse_args()
   318	
   319	    transcript_path = PROJ / "transcript_fixed.json"
   320	    config_path = PROJ / "project-config.json"
   321	    if not transcript_path.exists() or not config_path.exists():
   322	        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
   323	
   324	    transcript = load_json(transcript_path)
   325	    config = load_json(config_path)
   326	    fmt = config.get("format", "short")
   327	    tone = config.get("tone", "プロフェッショナル")
   328	    segments = transcript.get("segments", [])
   329	    words = transcript.get("words", [])
   330	
   331	    vad_path = PROJ / "vad_result.json"
   332	    vad = load_json(vad_path) if vad_path.exists() else None
   333	    cut_segments = build_cut_segments_from_vad(vad)
   334	    cut_total_frames = cut_segments[-1]["playbackEnd"] if cut_segments else None
   335	
   336	    used_plan = False
   337	    if args.plan:
   338	        plan_path = Path(args.plan)
   339	        if not plan_path.exists():
   340	            msg = f"--plan path not found: {plan_path}"
   341	            if args.strict_plan:
   342	                raise SystemExit(msg)
   343	            print(f"WARN: {msg} → deterministic fallback")
   344	        else:
   345	            plan = load_json(plan_path)
   346	            errors = validate_slide_plan(plan, words, cut_total_frames, fmt)
   347	            if errors:
   348	                if args.strict_plan:
   349	                    print("ERROR: plan validation failed:")
   350	                    for e in errors:
   351	                        print(f"  - {e}")
   352	                    raise SystemExit(2)
   353	                print("WARN: plan validation failed, deterministic fallback:")
   354	                for e in errors:
   355	                    print(f"  - {e}")
   356	            else:
   357	                slides = build_slides_from_plan(plan, words, cut_segments, fmt, tone)
   358	                used_plan = True
   359	                print(f"=== plan accepted ({len(plan.get('slides', []))} slides) ===")
   360	
   361	    if not used_plan:
   362	        if args.mode == "topic":
   363	            slides = build_slides_topic_mode(segments, cut_segments, fmt, tone)
   364	        else:
   365	            slides = build_slides_segment_mode(segments, cut_segments, fmt, tone)
   366	
   367	    out_path = PROJ / "src" / "Slides" / "slideData.ts"
   368	    backup = PROJ / "src" / "Slides" / "slideData.backup.ts"
   369	    if out_path.exists() and not backup.exists():
   370	        backup.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")
   371	    ts = render_slide_data_ts(slides)
   372	    out_path.write_text(ts, encoding="utf-8")
   373	
   374	    mode_label = "plan" if used_plan else f"deterministic-{args.mode}"
   375	    print(f"=== slideData.ts 生成 (mode={mode_label}) ===")
   376	    print(f"path: {out_path}")
   377	    print(f"input segments: {len(segments)}")
   378	    print(f"output slides: {len(slides)}")
   379	    for s in slides:
   380	        bullets_count = len(s.get("bullets") or [])
   381	        print(f"  [{s['id']:2}] f{s['startFrame']:5}-{s['endFrame']:5} '{s['title']}' (bullets={bullets_count})")
   382	
   383	
   384	if __name__ == "__main__":
   385	    main()

exec
/bin/zsh -lc "nl -ba template/scripts/generate_slide_plan.py | sed -n '1,180p'" in /Users/rokumasuda/.claude/plugins/supermovie
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

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '220,290p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   220	
   221	
   222	def cli() -> int:
   223	    ap = argparse.ArgumentParser()
   224	    ap.add_argument(
   225	        "--formats",
   226	        default="youtube,short,square",
   227	        help="検証対象 format (カンマ区切り、default 全 3 種)",
   228	    )
   229	    ap.add_argument(
   230	        "--frames",
   231	        default="30,90",
   232	        help="検証 frame 番号 (カンマ区切り、default 30,90)",
   233	    )
   234	    ap.add_argument("--out-dir", default=str(SMOKE_OUT), help="出力ディレクトリ")
   235	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
   236	    args = ap.parse_args()
   237	
   238	    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
   239	    if not formats:
   240	        print("ERROR: --formats が空です (例: --formats youtube,short)", file=sys.stderr)
   241	        return 4
   242	    for f in formats:
   243	        if f not in FORMAT_DIMS:
   244	            print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
   245	            return 4
   246	    frames = [int(x) for x in args.frames.split(",") if x.strip()]
   247	    if not frames:
   248	        print("ERROR: --frames が空です (例: --frames 30,90)", file=sys.stderr)
   249	        return 4
   250	    if any(f < 0 for f in frames):
   251	        print(f"ERROR: --frames に負数: {frames}", file=sys.stderr)
   252	        return 4
   253	
   254	    out_dir = Path(args.out_dir).resolve()
   255	    out_dir.mkdir(parents=True, exist_ok=True)
   256	
   257	    # 環境チェック (Codex Phase 3-G review P1 #1 反映、render 失敗を環境問題として早期検知)
   258	    for tool in ("npx", "ffprobe", "ffmpeg"):
   259	        if shutil.which(tool) is None:
   260	            print(f"ERROR: {tool} コマンドが PATH にない", file=sys.stderr)
   261	            return 3
   262	    if not MAIN_VIDEO.exists():
   263	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
   264	        return 3
   265	    if not REMOTION_BIN.exists():
   266	        print(
   267	            f"ERROR: remotion CLI が無い: {REMOTION_BIN} "
   268	            f"(npm install を先に実行してください)",
   269	            file=sys.stderr,
   270	        )
   271	        return 3
   272	    grid_label = has_drawtext_filter()
   273	    if not grid_label and not args.no_grid:
   274	        print(
   275	            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
   276	            file=sys.stderr,
   277	        )
   278	
   279	    # videoConfig.ts 原本保持
   280	    if not VIDEO_CONFIG.exists():
   281	        print(f"ERROR: videoConfig.ts が無い: {VIDEO_CONFIG}", file=sys.stderr)
   282	        return 4
   283	    original = VIDEO_CONFIG.read_text(encoding="utf-8")
   284	
   285	    results: list[dict] = []
   286	    stills: list[Path] = []
   287	    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
   288	    env_error: str | None = None
   289	
   290	    try:

exec
/bin/zsh -lc 'nl -ba template/src/InsertImage/insertImageData.ts && nl -ba template/src/InsertImage/types.ts && nl -ba template/src/InsertImage/ImageSequence.tsx' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import type { ImageSegment } from './types';
     2	import { FPS } from '../videoConfig';
     3	
     4	const toFrame = (seconds: number) => Math.round(seconds * FPS);
     5	
     6	// ==== 挿入画像データ ====
     7	// /supermovie-image-gen で自動生成されます
     8	export const insertImageData: ImageSegment[] = [
     9	  // 例: { id: 1, startFrame: toFrame(5), endFrame: toFrame(10), file: 'generated/example.png', type: 'infographic' },
    10	];
     1	export interface ImageSegment {
     2	  id: number;
     3	  startFrame: number;
     4	  endFrame: number;
     5	  file: string;
     6	  type: 'photo' | 'infographic' | 'overlay';
     7	  scale?: number;
     8	}
     1	import React from 'react';
     2	import { Sequence } from 'remotion';
     3	import { InsertImage } from './InsertImage';
     4	import { insertImageData } from './insertImageData';
     5	
     6	export const ImageSequence: React.FC = () => {
     7	  return (
     8	    <>
     9	      {insertImageData.map((segment) => (
    10	        <Sequence
    11	          key={segment.id}
    12	          from={segment.startFrame}
    13	          durationInFrames={segment.endFrame - segment.startFrame}
    14	        >
    15	          <InsertImage segment={segment} />
    16	        </Sequence>
    17	      ))}
    18	    </>
    19	  );
    20	};

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"export \\*|from './Narration'|from './Narration/mode'|getNarrationMode|narrationData\" template/src" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "rg -n \"getStaticFiles\\(|startsWith\\('narration/chunk_|startsWith\\(\\\"narration/chunk_|NARRATION_CHUNK_PREFIX|hasChunkNarration|hasLegacyNarration|staticFiles\\.some\" template/src" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
template/src/MainVideo.tsx:8:import { NarrationAudio } from './Narration';
template/src/MainVideo.tsx:9:import { getNarrationMode } from './Narration/mode';
template/src/MainVideo.tsx:21:  const narrationMode = getNarrationMode();
template/src/Narration/narrationData.ts:7:export const narrationData: NarrationSegment[] = [];
template/src/Narration/types.ts:3: * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
template/src/Narration/NarrationAudio.tsx:3:import { getNarrationMode } from './mode';
template/src/Narration/NarrationAudio.tsx:10: * Phase 3-H: getNarrationMode() で chunks / legacy / none の三経路を分岐。
template/src/Narration/NarrationAudio.tsx:17:  const mode = getNarrationMode();
template/src/Narration/index.ts:2:export { narrationData } from './narrationData';
template/src/Narration/index.ts:3:export { getNarrationMode, NARRATION_LEGACY_FILE } from './mode';
template/src/Narration/mode.ts:2:import { narrationData } from './narrationData';
template/src/Narration/mode.ts:20: *   1) narrationData が non-empty + 全 chunk file が public/ 配下に存在 → chunks
template/src/Narration/mode.ts:29:export const getNarrationMode = (): NarrationMode => {
template/src/Narration/mode.ts:32:    narrationData.length > 0 &&
template/src/Narration/mode.ts:33:    narrationData.every((seg) => names.has(seg.file))
template/src/Narration/mode.ts:35:    return { kind: 'chunks', segments: narrationData };

 succeeded in 0ms:
template/src/SoundEffects/BGM.tsx:11: * 失敗させない。getStaticFiles() は public/ 以下の asset 一覧を返す Remotion 公式 API
template/src/SoundEffects/BGM.tsx:15:  const hasFile = getStaticFiles().some((f) => f.name === BGM_FILE);
template/src/Narration/mode.ts:24: * getStaticFiles() の結果を一度 Set 化して O(1) lookup
template/src/Narration/mode.ts:30:  const names = new Set(getStaticFiles().map((f) => f.name));

codex
`SKILL.md` の FPS 記述と実装の間に不一致がありそうです。あわせて、read-only で副作用が出にくい範囲の静的チェックだけ走らせます。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'test -d template/node_modules && echo node_modules_present || echo node_modules_absent' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
node_modules_absent

exec
/bin/zsh -lc 'find template -maxdepth 2 -type d -name node_modules -o -name public -print' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
exec
/bin/zsh -lc 'git diff --check d6f0846''^ d6f0846' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Veek83Hi' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-bmIV5heJ' (errno=Operation not permitted)

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "find . -maxdepth 3 -type f -name '*.yml' -o -name '*.yaml' -o -name '*.json' | sort" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
./.claude-plugin/marketplace.json
./.claude-plugin/plugin.json
./template/package.json
./template/tsconfig.json

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"CODEX_REVIEW_PHASE3H_20260504T213301|P1|P2|P3|mode helper|cleanup|atomic|read_video_config|wave\\.Error|SKILL\" docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2:2026-05-04T12:33:01.201276Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:45:E) Phase 3-G new P1 fix (vstack letterbox)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:49:F) skill SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:54:   - Phase 3-D (concat_wavs) と Phase 3-H (per-segment) の二重出力で disk 容量倍化、cleanup 戦略
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:59:- P0/P1/P2/P3 分類、各指摘 file:line / 詳細 / 修正案 / Effort / 自走可否
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:105:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:107:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:124:/bin/zsh -lc "sed -n '1,220p' /Users/rokumasuda/.claude/skills/verification-gate/SKILL.md" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:206:M	skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:256:+- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:298:+def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:440:+    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:487:+    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:514: skills/supermovie-narration/SKILL.md      |  53 ++++++---
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:527:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/visual_smoke.py skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:701:diff --git a/skills/supermovie-narration/SKILL.md b/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:703:--- a/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:704:+++ b/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:732:+stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:807:     (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:809:     (drawtext filter 不在環境向け、Codex P1 #2 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:814:+    再 review investigation で実証、新規 P1)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:935:    17	- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1039:   121	def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1210:   292	    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1251:   333	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1360:   124	    ことがあるため事前検査する (Codex Phase 3-G review P1 #2 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1388:   152	    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1390:   154	    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1395:   159	    再 review investigation で実証、新規 P1)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1489:/bin/zsh -lc "nl -ba skills/supermovie-narration/SKILL.md | sed -n '1,180p'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1562:    72	stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1663:./skills/supermovie-narration/SKILL.md:5:  Remotion の <NarrationAudio /> layer で再生するスキル。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1664:./skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1665:./skills/supermovie-narration/SKILL.md:61:- `public/narration/chunk_NNN.wav` を保持 (削除しない)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1666:./skills/supermovie-narration/SKILL.md:63:- `src/Narration/narrationData.ts` を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1667:./skills/supermovie-narration/SKILL.md:65:- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1668:./skills/supermovie-narration/SKILL.md:66:- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1669:./skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1670:./skills/supermovie-narration/SKILL.md:79:| 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1671:./skills/supermovie-narration/SKILL.md:81:| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1672:./skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1673:./skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1674:./skills/supermovie-narration/SKILL.md:85:優先順位は narrationData > narration.wav > null。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1675:./skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1676:./skills/supermovie-narration/SKILL.md:92:- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1677:./skills/supermovie-narration/SKILL.md:94:- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1678:./skills/supermovie-narration/SKILL.md:100:python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1679:./skills/supermovie-narration/SKILL.md:103:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1680:./skills/supermovie-narration/SKILL.md:104:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1681:./skills/supermovie-narration/SKILL.md:107:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1682:./skills/supermovie-narration/SKILL.md:108:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1683:./skills/supermovie-narration/SKILL.md:111:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1684:./skills/supermovie-narration/SKILL.md:117:- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1685:./skills/supermovie-narration/SKILL.md:118:- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1686:./skills/supermovie-narration/SKILL.md:119:- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1687:./skills/supermovie-narration/SKILL.md:129:| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1688:./skills/supermovie-narration/SKILL.md:139:    └ NarrationAudio: <Audio src=narration.wav /> マウント
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1689:./skills/supermovie-init/SKILL.md:130:- `fps.r_frame_rate` / `fps.avg_frame_rate` / `fps.vfr_metadata_suspect`
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1690:./skills/supermovie-init/SKILL.md:145:| VFR (可変 fps) | `r_frame_rate` ≠ `avg_frame_rate` (誤差 > 0.5%) | frame 換算で時間ずれ | render 前に CFR 化 (ffmpeg `-r`) を別タスクで |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1691:./skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1692:./skills/supermovie-init/SKILL.md:246:🎬 動画: <duration>秒 / <fps>fps / <frames>フレーム
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1693:./skills/supermovie-telop-creator/SKILL.md:262:  fps: 30,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1694:./skills/supermovie-telop-creator/SKILL.md:287:  fps={30}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1695:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:23:A) voicevox_narration.py 構造変化
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1696:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1697:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:27:   - read_render_fps の type 検証 (cfg["source"] が None の時の AttributeError)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1698:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:29:   - --keep-chunks 撤去で既存使用者影響範囲 (skill 内文書 / 他 script の引数)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1699:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:30:   - chunk_meta.json schema (fps/total_frames/segments[]) と narrationData.ts duplication
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1700:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:32:B) NarrationAudio.tsx の三段 fallback
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1701:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:33:   - narrationData non-empty + 一部 chunk 不在ケースで null 返り、render 全体が止まらないか
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1702:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:38:   - hasChunkNarration 三条件 AND の論理過剰 (narrationData.length > 0 だけで実質判定済みでは?)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1703:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:39:   - startsWith("narration/chunk_") の prefix collision (例: narration/chunk_meta.json は wav じゃないのに引っ掛かる)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1704:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:41:D) types.ts / narrationData.ts placeholder
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1705:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:50:   - エラーハンドリング table の exit 6 行が他コマンド (--allow-partial) と矛盾しないか
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1706:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:54:   - Phase 3-D (concat_wavs) と Phase 3-H (per-segment) の二重出力で disk 容量倍化、cleanup 戦略
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1707:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:208:M	template/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1708:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:210:M	template/src/Narration/NarrationAudio.tsx
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1709:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:212:A	template/src/Narration/narrationData.ts
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1710:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1711:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:232:diff --git a/template/scripts/voicevox_narration.py b/template/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1712:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:234:--- a/template/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1713:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:235:+++ b/template/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1714:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:251:+- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1715:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:253:+- src/Narration/narrationData.ts を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1716:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:255:+- public/narration/chunk_meta.json も debug 用に出力
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1717:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:257:+- partial failure 時は narrationData.ts を空に reset、二重音声防止
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1718:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:260:     python3 scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1719:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:261:     python3 scripts/voicevox_narration.py --speaker 3
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1720:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:262:     python3 scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1721:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:263:     python3 scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1722:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:264:     python3 scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1723:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1724:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:277:+NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1725:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:278:+CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1726:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:282:+    "export const narrationData: NarrationSegment[] = [];\n"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1727:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:288:@@ -92,6 +112,109 @@ def concat_wavs(wavs: list[Path], out_path: Path) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1728:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1729:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:300:+    narrationData.ts も空 array に reset する。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1730:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:302:+        for p in NARRATION_DIR.glob("chunk_*.wav"):
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1731:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1732:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:316:+    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1733:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1734:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:322:+    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1735:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:330:+    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1736:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:331:+    if isinstance(fps, (int, float)) and fps > 0:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1737:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:332:+        return int(fps)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1738:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:338:+    fps: int,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1739:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:340:+    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1740:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:345:+        duration_frames = max(1, round(duration_sec * fps))
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1741:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:360:+            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1742:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:369:+        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1743:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:370:+        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1744:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:375:+        "export const narrationData: NarrationSegment[] = [",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1745:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:402:-    ap.add_argument("--keep-chunks", action="store_true",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1746:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:405:+        "--fps",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1747:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:408:+        help=f"narrationData.ts に書き込む frame 換算 fps "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1748:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1749:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:411:     ap.add_argument("--allow-partial", action="store_true",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1750:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:413:+                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1751:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:422:-            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1752:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:424:+            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1753:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:425:+            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1754:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:436:+    fps = args.fps if args.fps is not None else read_render_fps()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1755:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:437:+    print(f"target fps: {fps}")
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1756:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1757:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:451:-        p = chunks_dir / f"chunk_{i:03d}.wav"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1758:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:452:+        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1759:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:460:             f"(--allow-partial で部分成功でも narration.wav 出力可)",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1760:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:463:+        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1761:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:487:+    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1762:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:489:+    segments, ts_path, meta_path = write_narration_data(pairs, fps)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1763:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:495:+        "fps": fps,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1764:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:502:+        "chunk_meta_json": str(meta_path),
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1765:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:516: template/scripts/voicevox_narration.py    | 187 ++++++++++++++++++++++++++----
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1766:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:518: template/src/Narration/NarrationAudio.tsx |  52 +++++++--
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1767:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:520: template/src/Narration/narrationData.ts   |   7 ++
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1768:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1769:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:541:-import { NarrationAudio } from './Narration';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1770:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:542:+import { NarrationAudio, narrationData } from './Narration';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1771:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1772:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:567:+    narrationData.length > 0 &&
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1773:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:568:+    narrationData.every((seg) =>
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1774:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:576:diff --git a/template/src/Narration/NarrationAudio.tsx b/template/src/Narration/NarrationAudio.tsx
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1775:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:578:--- a/template/src/Narration/NarrationAudio.tsx
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1776:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:579:+++ b/template/src/Narration/NarrationAudio.tsx
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1777:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:584:+import { narrationData } from './narrationData';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1778:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:586: interface NarrationAudioProps {
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1779:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:597:+ * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1780:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:598:+ * narrationData.ts を生成する経路)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1781:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:600:- * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1782:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:603:+ *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1783:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:606:+ *   2) narrationData が空 + public/narration.wav 存在
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1784:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1785:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:618: export const NarrationAudio: React.FC<NarrationAudioProps> = ({
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1786:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:625:+  if (narrationData.length > 0) {
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1787:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:626:+    const allChunksExist = narrationData.every((seg) =>
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1788:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:634:+        {narrationData.map((seg) => (
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1789:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:656: export { NarrationAudio } from './NarrationAudio';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1790:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:657:+export { narrationData } from './narrationData';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1791:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:659:diff --git a/template/src/Narration/narrationData.ts b/template/src/Narration/narrationData.ts
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1792:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:663:+++ b/template/src/Narration/narrationData.ts
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1793:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:666:+ * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1794:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:667:+ * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1795:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:671:+export const narrationData: NarrationSegment[] = [];
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1796:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:680:+ * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1797:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1798:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:690:+  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1799:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:717:-`--keep-chunks` で chunk 個別 wav も保持 (debug)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1800:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:721:+- `public/narration/chunk_NNN.wav` を保持 (削除しない)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1801:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:723:+- `src/Narration/narrationData.ts` を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1802:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:725:+- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1803:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:726:+- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1804:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1805:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:737:-`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1806:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:742:-| narration.wav 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1807:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:746:+| 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1808:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:748:+| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1809:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1810:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1811:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:752:-つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1812:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:755:+優先順位は narrationData > narration.wav > null。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1813:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:756:+`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1814:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:762:-- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1815:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:764:+- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1816:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:766:+- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1817:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:770:@@ -97,8 +113,10 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1818:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:775:-- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1819:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:777:+- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1820:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:778:+- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1821:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:779:+- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1822:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:783:@@ -108,6 +126,7 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1823:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:787:+| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1824:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:851:/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,380p'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1825:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:853:/bin/zsh -lc "nl -ba template/src/Narration/NarrationAudio.tsx | sed -n '1,140p'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1826:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:857:     3	import { narrationData } from './narrationData';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1827:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:859:     5	interface NarrationAudioProps {
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1828:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:866:    12	 * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1829:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:867:    13	 * narrationData.ts を生成する経路)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1830:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:870:    16	 *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1831:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:873:    19	 *   2) narrationData が空 + public/narration.wav 存在
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1832:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1833:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:883:    29	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1834:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:889:    35	  if (narrationData.length > 0) {
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1835:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:890:    36	    const allChunksExist = narrationData.every((seg) =>
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1836:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:898:    44	        {narrationData.map((seg) => (
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1837:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:930:    12	- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1838:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:932:    14	- src/Narration/narrationData.ts を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1839:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:934:    16	- public/narration/chunk_meta.json も debug 用に出力
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1840:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:936:    18	- partial failure 時は narrationData.ts を空に reset、二重音声防止
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1841:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:939:    21	    python3 scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1842:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:940:    22	    python3 scripts/voicevox_narration.py --speaker 3
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1843:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:941:    23	    python3 scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1844:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:942:    24	    python3 scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1845:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:943:    25	    python3 scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1846:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1847:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:968:    50	NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1848:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:969:    51	CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1849:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:973:    55	    "export const narrationData: NarrationSegment[] = [];\n"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1850:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1014:    96	def concat_wavs(wavs: list[Path], out_path: Path) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1851:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1852:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1041:   123	    narrationData.ts も空 array に reset する。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1853:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1043:   125	        for p in NARRATION_DIR.glob("chunk_*.wav"):
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1854:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1855:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1057:   139	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1856:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1857:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1063:   145	    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1858:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1071:   153	    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1859:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1072:   154	    if isinstance(fps, (int, float)) and fps > 0:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1860:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1073:   155	        return int(fps)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1861:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1079:   161	    fps: int,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1862:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1081:   163	    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1863:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1086:   168	        duration_frames = max(1, round(duration_sec * fps))
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1864:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1101:   183	            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1865:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1110:   192	        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1866:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1111:   193	        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1867:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1116:   198	        "export const narrationData: NarrationSegment[] = [",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1868:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1163:   245	        "--fps",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1869:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1166:   248	        help=f"narrationData.ts に書き込む frame 換算 fps "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1870:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1871:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1169:   251	    ap.add_argument("--allow-partial", action="store_true",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1872:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1170:   252	                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1873:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1182:   264	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1874:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1183:   265	            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1875:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1206:   288	    fps = args.fps if args.fps is not None else read_render_fps()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1876:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1207:   289	    print(f"target fps: {fps}")
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1877:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1878:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1221:   303	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1879:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1233:   315	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1880:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1236:   318	        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1881:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1247:   329	    concat_wavs(chunk_paths, out_path)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1882:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1251:   333	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1883:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1253:   335	    segments, ts_path, meta_path = write_narration_data(pairs, fps)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1884:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1259:   341	        "fps": fps,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1885:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1265:   347	        "chunk_meta_json": str(meta_path),
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1886:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1291:     8	import { NarrationAudio, narrationData } from './Narration';
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1887:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1888:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1310:    27	    narrationData.length > 0 &&
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1889:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1311:    28	    narrationData.every((seg) =>
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1890:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1344:    61	      <NarrationAudio volume={1.0} />
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1891:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1483:/bin/zsh -lc 'nl -ba template/src/Narration/types.ts template/src/Narration/narrationData.ts template/src/Narration/index.ts' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1892:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1495:     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1893:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1533:    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1894:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1551:    61	- `public/narration/chunk_NNN.wav` を保持 (削除しない)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1895:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1553:    63	- `src/Narration/narrationData.ts` を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1896:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1555:    65	- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1897:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1556:    66	- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1898:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1899:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1569:    79	| 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1900:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1571:    81	| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1901:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1902:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1903:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1575:    85	優先順位は narrationData > narration.wav > null。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1904:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1576:    86	`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1905:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1582:    92	- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1906:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1584:    94	- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1907:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1590:   100	python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1908:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1593:   103	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1909:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1594:   104	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1910:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1597:   107	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1911:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1598:   108	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1912:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1601:   111	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1913:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1607:   117	- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1914:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1608:   118	- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1915:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1609:   119	- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1916:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1619:   129	| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1917:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1629:   139	    └ NarrationAudio: <Audio src=narration.wav /> マウント
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1961:./template/scripts/voicevox_narration.py:291:    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1966:./template/scripts/voicevox_narration.py:333:    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2040:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3061:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2041:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3064:skills/supermovie-narration/SKILL.md:67:| narration.wav 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2042:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3065:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2043:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3067:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2044:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3068:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2045:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3069:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2046:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3070:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2047:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3071:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2048:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3072:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2049:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3074:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2130:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:149:    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2151:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1480:    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2180:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1440:skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2181:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1442:skills/supermovie-narration/SKILL.md:67:| narration.wav 状態 | NarrationAudio | base Video volume |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2182:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1443:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2205:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2046:./skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2207:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2072:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1440:skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2236:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4618:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2237:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2238:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4691:skills/supermovie-narration/SKILL.md:78:- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2257:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5243:7. [skills/supermovie-narration/SKILL.md:119](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:119) / Phase 4 本文は手作業不要に修正されていますが、連携マップの「`MainVideo.tsx <NarrationAudio /> 有効化`」は旧手順っぽく読めます。  
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2259:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5305:7. [skills/supermovie-narration/SKILL.md:119](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:119) / Phase 4 本文は手作業不要に修正されていますが、連携マップの「`MainVideo.tsx <NarrationAudio /> 有効化`」は旧手順っぽく読めます。  
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2469:M	skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2486:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2662:skills/supermovie-narration/SKILL.md:146:`getStaticFiles()` は Studio 起動時の asset リストをキャッシュするため、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2680:./skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2681:./skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2682:./skills/supermovie-narration/SKILL.md:100:python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2683:./skills/supermovie-narration/SKILL.md:103:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2684:./skills/supermovie-narration/SKILL.md:104:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2685:./skills/supermovie-narration/SKILL.md:107:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2686:./skills/supermovie-narration/SKILL.md:108:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2687:./skills/supermovie-narration/SKILL.md:111:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2720:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2721:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2722:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2723:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2724:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2725:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2726:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2727:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2740:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:59:`--keep-chunks` で chunk 個別 wav も保持 (debug)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2741:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2766:-rw-r--r--  1 rokumasuda  staff  191155 May  4 21:34 CODEX_REVIEW_PHASE3H_20260504T213301.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2769:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2770:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:37:C) MainVideo.tsx mute logic 拡張
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2771:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:55:   - Studio 起動中に narration を再生成した時の getStaticFiles cache 残存問題 (Phase 3-F 同様)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2772:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:56:   - Codex Phase 3-H consultation の危険ポイント top3 (chunk-only mute / FPS / stale) が全部 fix されているか
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2773:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:102:git: error: couldn't create cache file '/tmp/xcrun_db-TXyfxEjW' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2774:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:104:git: error: couldn't create cache file '/tmp/xcrun_db-AnWAsMGb' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2775:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:109:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2776:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:113:git: error: couldn't create cache file '/tmp/xcrun_db-qwiBqS0o' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2777:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:115:git: error: couldn't create cache file '/tmp/xcrun_db-ZslVDBsC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2778:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:203:git: error: couldn't create cache file '/tmp/xcrun_db-BxZNM0VB' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2779:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:205:git: error: couldn't create cache file '/tmp/xcrun_db-xP7OvmA5' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2780:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:229:git: error: couldn't create cache file '/tmp/xcrun_db-4CIv9r5q' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2781:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:231:git: error: couldn't create cache file '/tmp/xcrun_db-wxklg1BM' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2782:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:256:+- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2783:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2784:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:273:+DEFAULT_FPS = 30
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2785:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:298:+def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2786:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2787:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:306:+                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2788:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2789:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2790:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2791:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2792:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:440:+    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2793:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:511:git: error: couldn't create cache file '/tmp/xcrun_db-GBfpk1wn' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2794:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:513:git: error: couldn't create cache file '/tmp/xcrun_db-1kZvbhlE' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2795:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:530:git: error: couldn't create cache file '/tmp/xcrun_db-2yudiVke' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2796:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:532:git: error: couldn't create cache file '/tmp/xcrun_db-tKPT356H' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2797:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:549:-  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2798:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:552:+  // - legacy: public/narration.wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2799:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2800:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:612:+ * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2801:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2802:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2803:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:698:git: error: couldn't create cache file '/tmp/xcrun_db-Efofjwv1' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2804:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:700:git: error: couldn't create cache file '/tmp/xcrun_db-jrIXtF9L' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2805:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2806:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:732:+stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2807:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:745:-| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2808:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2809:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2810:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:753:-次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2811:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:757:+`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2812:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:877:    23	 * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2813:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2814:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:935:    17	- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2815:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2816:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:964:    46	DEFAULT_FPS = 30
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2817:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1039:   121	def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2818:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2819:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1047:   129	                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2820:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2821:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2822:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2823:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2824:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1210:   292	    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2825:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1299:    16	  // - legacy: public/narration.wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2826:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2827:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1320:    37	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2828:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2829:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1562:    72	stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2830:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2831:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2832:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1577:    87	`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2833:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1669:./skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2834:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1672:./skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2835:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1673:./skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2836:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1691:./skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2837:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1696:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2838:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1723:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2839:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1728:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2840:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1731:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2841:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1733:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2842:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1748:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2843:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1756:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2844:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1771:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2845:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1784:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2846:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1797:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2847:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1804:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2848:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1809:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2849:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1810:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2850:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1832:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2851:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1846:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2852:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1851:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2853:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1854:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2854:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1856:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2855:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1870:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2856:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1877:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2857:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1887:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2858:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1898:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2859:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1901:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2860:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1902:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2861:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1930:./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2862:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1935:./template/scripts/voicevox_narration.py:122:    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2863:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1938:./template/scripts/voicevox_narration.py:134:                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2864:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1940:./template/scripts/voicevox_narration.py:144:def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2865:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1954:./template/scripts/voicevox_narration.py:249:             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2866:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1961:./template/scripts/voicevox_narration.py:291:    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2867:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2075:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4050:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2868:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2085:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4346:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2869:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2087:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4352:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2870:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2096:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4404:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2871:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2098:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4410:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2872:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2123:./template/src/Narration/NarrationAudio.tsx:24: * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2873:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2179:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1423:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2874:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2237:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2875:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2241:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4799:   184	export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2876:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2262:./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2877:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2270:./template/src/MainVideo.tsx:17:  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2878:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2277:./template/src/Root.tsx:14:        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2879:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2322:    11	  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2880:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2465:git: error: couldn't create cache file '/tmp/xcrun_db-iNh40BTC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2881:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2467:git: error: couldn't create cache file '/tmp/xcrun_db-3IM4g8GC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2882:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2483:git: error: couldn't create cache file '/tmp/xcrun_db-GdpxoD42' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2883:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2485:git: error: couldn't create cache file '/tmp/xcrun_db-EYzaB1TH' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2884:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2547:     4	import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2885:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2557:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2886:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2580:     9	export const FPS = 30;
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2887:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2602:    31	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2888:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2615:    44	    titleTop: 60,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2889:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2628:    57	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2890:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2693:./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2891:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2697:./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2892:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2717:git: error: couldn't create cache file '/tmp/xcrun_db-y6FWzVDT' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2893:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2719:git: error: couldn't create cache file '/tmp/xcrun_db-IStL70W8' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2894:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2737:git: error: couldn't create cache file '/tmp/xcrun_db-JdwJD4NI' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2895:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2739:git: error: couldn't create cache file '/tmp/xcrun_db-MCSYmX0L' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2896:docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:24:- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2899:docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:561:    24	- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2910:docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2256:   561	    24	- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2931:docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2999:git: error: couldn't create cache file '/tmp/xcrun_db-P2NR6fuE' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2935:docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3066:skills/supermovie-narration/SKILL.md:73:次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2975:docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1755:git: error: couldn't create cache file '/tmp/xcrun_db-N38CJFP1' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3016:docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2155:git: error: couldn't create cache file '/tmp/xcrun_db-QLcplP1E' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3046:docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3065:skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3184:skills/supermovie-init/SKILL.md:73:### ヒアリング結果 → `project-config.json`
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3185:skills/supermovie-init/SKILL.md:121:  --write-config "<PROJECT>/project-config.json" \
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3186:skills/supermovie-init/SKILL.md:126:**抽出される値 (project-config.json `source.*` に nested で書き込まれる):**
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3187:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3188:skills/supermovie-init/SKILL.md:185:export const SOURCE_DURATION_FRAMES = <duration_frames>; // 元動画 frame、cut 後は cutData.CUT_TOTAL_FRAMES を使う
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3317:/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 -c 'import wave; print(wave.Error.__name__)'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3502:   257	    # 環境チェック (Codex Phase 3-G review P1 #1 反映、render 失敗を環境問題として早期検知)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3551:   306	                    # P1 #1: render 失敗は環境問題 (exit 3) として即終了
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3598:   353	        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3605:   360	            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3620:    fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3623:    で実証された新規 P1 を fix。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3660:     (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3662:     (drawtext filter 不在環境向け、Codex P1 #2 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3667:+    再 review investigation で実証、新規 P1)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3719:   148	    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3721:   150	    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3789:**結論: merge 前に P1 は潰すべきです。** P0 は出していません。P1×2 / P2×4 / P3×3。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3793:| P1 | **missing chunk + legacy wav で無音化する**。`NarrationAudio` は `narrationData.length > 0` かつ chunk 不足で即 `null` を返す一方、`MainVideo` は `narration.wav` があるだけで base を mute するため、chunk 不足 + legacy 存在時に narration も base 音声も消える（[NarrationAudio.tsx:35](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:35), [NarrationAudio.tsx:39](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:39), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25), [MainVideo.tsx:33](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:33)）。 | `getNarrationMode()` を共通化し、`chunks complete -> chunks / legacy exists -> legacy / none` に統一。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3794:| P1 | **all-or-nothing が legacy `narration.wav` を対象外にしている**。partial failure 時は chunk と `narrationData.ts` だけ消すが、既存 `public/narration.wav` は残るので、失敗後に古い narration が再生され得る（[voicevox_narration.py:318](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:318), [voicevox_narration.py:324](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:324), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25)）。 | staging dir に全生成して最後に atomic swap、または失敗時に legacy wav も消す。推奨は staging。Effort M / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3795:| P2 | **`narrationData.ts` 書き換えが atomic ではない**。コメントは “atomic” だが、実装は `write_text()` 直書きで、SIGINT/書き込み失敗時に TS が途中破損し得る（[voicevox_narration.py:141](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:141), [voicevox_narration.py:181](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:181), [voicevox_narration.py:213](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:213), [voicevox_narration.py:333](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:333)）。 | temp file + `os.replace()`。meta も同様。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3796:| P2 | **`read_render_fps()` が malformed config で落ちる**。`cfg.get("source", {}).get(...)` は `source: null` / string で `AttributeError` になる（[voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153), `python3 -c` Bash実測）。 | dict 型を段階検証。`--fps <= 0` も reject。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3797:| P2 | **FPS source が Remotion 実値と完全同期ではない**。render は `videoConfig.FPS` を使うが、script は `project-config.json` を読むため、両者がズレると Sequence duration がズレる（[Root.tsx:13](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [Root.tsx:14](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts:9](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153)）。 | `src/videoConfig.ts` から FPS を読む小 helper、または `--fps` 必須化。Effort S-M / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3798:| P2 | **WAV header 信頼が狭い**。Python `wave` は PCM WAV のみ対象で、unsupported WAV/非WAVなら `wave.Error` 系で落ちる（Python docs: https://docs.python.org/3/library/wave.html）。現実装は `measure_duration_seconds()` / `concat_wavs()` で捕捉していない（[voicevox_narration.py:100](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:100), [voicevox_narration.py:117](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:117)）。VOICEVOX の通常 `/synthesis` は `audio.wav` 例示なので主経路は妥当（https://github.com/VOICEVOX/voicevox_engine）。 | `wave.Error` を catch して exit 6 相当に rollback。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3799:| P3 | `MainVideo` の `startsWith("narration/chunk_")` は redundant かつ `chunk_meta.json` にも当たる。`every(seg.file)` が実質判定済み（[MainVideo.tsx:27](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:27), [MainVideo.tsx:31](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:31)）。 | `.endsWith(".wav")` 付きにするか削除。Effort XS / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3800:| P3 | `getStaticFiles().some()` が `MainVideo` と `NarrationAudio` で毎 render 重複する。Remotion docs 上 `getStaticFiles()` は Studio/render 中のみ有効（https://www.remotion.dev/docs/getstaticfiles）。 | `Set(staticFiles.map(f => f.name))` と mode helper 共有。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3801:| P3 | skill の連携マップが Phase 3-H 実装に追従していない。本文は chunk/data 経路だが、map は `public/narration.wav` と単一 `<Audio>` の旧説明のまま（[SKILL.md:131](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:131), [SKILL.md:137](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:137), [SKILL.md:139](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:139)）。 | map を `narrationData.ts + chunk_NNN.wav + legacy fallback` に更新。Effort XS / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3805:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3838:**結論: merge 前に P1 は潰すべきです。** P0 は出していません。P1×2 / P2×4 / P3×3。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3842:| P1 | **missing chunk + legacy wav で無音化する**。`NarrationAudio` は `narrationData.length > 0` かつ chunk 不足で即 `null` を返す一方、`MainVideo` は `narration.wav` があるだけで base を mute するため、chunk 不足 + legacy 存在時に narration も base 音声も消える（[NarrationAudio.tsx:35](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:35), [NarrationAudio.tsx:39](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:39), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25), [MainVideo.tsx:33](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:33)）。 | `getNarrationMode()` を共通化し、`chunks complete -> chunks / legacy exists -> legacy / none` に統一。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3843:| P1 | **all-or-nothing が legacy `narration.wav` を対象外にしている**。partial failure 時は chunk と `narrationData.ts` だけ消すが、既存 `public/narration.wav` は残るので、失敗後に古い narration が再生され得る（[voicevox_narration.py:318](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:318), [voicevox_narration.py:324](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:324), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25)）。 | staging dir に全生成して最後に atomic swap、または失敗時に legacy wav も消す。推奨は staging。Effort M / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3844:| P2 | **`narrationData.ts` 書き換えが atomic ではない**。コメントは “atomic” だが、実装は `write_text()` 直書きで、SIGINT/書き込み失敗時に TS が途中破損し得る（[voicevox_narration.py:141](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:141), [voicevox_narration.py:181](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:181), [voicevox_narration.py:213](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:213), [voicevox_narration.py:333](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:333)）。 | temp file + `os.replace()`。meta も同様。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3845:| P2 | **`read_render_fps()` が malformed config で落ちる**。`cfg.get("source", {}).get(...)` は `source: null` / string で `AttributeError` になる（[voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153), `python3 -c` Bash実測）。 | dict 型を段階検証。`--fps <= 0` も reject。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3846:| P2 | **FPS source が Remotion 実値と完全同期ではない**。render は `videoConfig.FPS` を使うが、script は `project-config.json` を読むため、両者がズレると Sequence duration がズレる（[Root.tsx:13](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [Root.tsx:14](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts:9](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153)）。 | `src/videoConfig.ts` から FPS を読む小 helper、または `--fps` 必須化。Effort S-M / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3847:| P2 | **WAV header 信頼が狭い**。Python `wave` は PCM WAV のみ対象で、unsupported WAV/非WAVなら `wave.Error` 系で落ちる（Python docs: https://docs.python.org/3/library/wave.html）。現実装は `measure_duration_seconds()` / `concat_wavs()` で捕捉していない（[voicevox_narration.py:100](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:100), [voicevox_narration.py:117](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:117)）。VOICEVOX の通常 `/synthesis` は `audio.wav` 例示なので主経路は妥当（https://github.com/VOICEVOX/voicevox_engine）。 | `wave.Error` を catch して exit 6 相当に rollback。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3848:| P3 | `MainVideo` の `startsWith("narration/chunk_")` は redundant かつ `chunk_meta.json` にも当たる。`every(seg.file)` が実質判定済み（[MainVideo.tsx:27](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:27), [MainVideo.tsx:31](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:31)）。 | `.endsWith(".wav")` 付きにするか削除。Effort XS / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3849:| P3 | `getStaticFiles().some()` が `MainVideo` と `NarrationAudio` で毎 render 重複する。Remotion docs 上 `getStaticFiles()` は Studio/render 中のみ有効（https://www.remotion.dev/docs/getstaticfiles）。 | `Set(staticFiles.map(f => f.name))` と mode helper 共有。Effort S / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3850:| P3 | skill の連携マップが Phase 3-H 実装に追従していない。本文は chunk/data 経路だが、map は `public/narration.wav` と単一 `<Audio>` の旧説明のまま（[SKILL.md:131](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:131), [SKILL.md:137](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:137), [SKILL.md:139](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:139)）。 | map を `narrationData.ts + chunk_NNN.wav + legacy fallback` に更新。Effort XS / 自走可 |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3854:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2:2026-05-04T12:45:14.594815Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:19:前 review (CODEX_REVIEW_PHASE3H_20260504T213301) で指摘した 9 件 (P1×2 + P2×4 + P3×3) が全部 closed したか機械的 verify。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:22:- P1#1 mode helper: src/Narration/mode.ts 新規、NarrationAudio.tsx と MainVideo.tsx が getNarrationMode 経由か
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:23:- P1#2 cleanup_stale_all: 旧 narration.wav も削除されるか、partial failure path で残らないか
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:24:- P2#3 atomic write: atomic_write_text/_bytes/concat_wavs_atomic、全出力 (narrationData.ts/chunk_meta.json/chunk_NNN.wav/narration.wav) 経由か
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:25:- P2#4 read_video_config_fps: VIDEO_CONFIG regex 経路、project-config.json 経路は撤去されたか
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:26:- P2#5 FPS source 統一: --fps <= 0 reject、videoConfig.ts 一次 source
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:27:- P2#6 wave.Error catch: measure_duration_seconds 呼出箇所すべてで catch、failure rollback
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:28:- P3#7 MainVideo redundancy: startsWith chunk_ 削除、helper 経由
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:29:- P3#8 Set lookup: getStaticFiles().some 重複の解消
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:30:- P3#9 SKILL.md 連携マップ: 3 出力 + getNarrationMode 三経路に追従
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:34:- atomic_write_text の `.{name}.tmp` ファイル名衝突 (同じ file が複数箇所から書かれた時)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:35:- concat_wavs_atomic の wave.Error が write 中 (open) で発生したら tmp ファイルが残るか
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:36:- cleanup_stale_all + atomic write の race (cleanup 中に他プロセスが narration.wav 書いたら)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:61:iv. **Phase 3-G visual smoke を CI 化** (P3 案)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:116:/bin/zsh -lc "sed -n '1,220p' /Users/rokumasuda/.claude/skills/verification-gate/SKILL.md" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:218:d6f0846 (HEAD -> roku/phase3h-narration-sequence) fix(narration): Codex Phase 3-H review P1×2 + P2×4 + P3×3 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:219: skills/supermovie-narration/SKILL.md      |  19 ++--
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:246:    11	 * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:287:     8	 * Phase 3-H Codex review P1 #1 反映:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:304:    25	 * (Codex P3 #8 反映、毎 frame の some() 重複を防ぐ)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:341:    13	  // Phase 3-F asset gate + Phase 3-H per-segment Sequence の mode helper を共有
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:342:    14	  // (Codex Phase 3-H review P1 #1 反映)。chunks / legacy / none のいずれでも
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:390:/bin/zsh -lc 'nl -ba template/src/Narration/index.ts && nl -ba skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:468:    72	stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:526:   130	| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:534:   138	/supermovie-narration         ← ★ここ: VOICEVOX で 3 出力を atomic 生成
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:585:    17	- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:588:    20	Phase 3-H review fix (Codex CODEX_REVIEW_PHASE3H_20260504T213301, P1×2 + P2×4):
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:590:    22	  tempfile + os.replace で atomic 書き換え (SIGINT/disk full 安全、P2 #3)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:592:    24	  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:593:    25	- wave.Error / EOFError を catch して exit 6 で all-or-nothing rollback (P2 #6)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:594:    26	- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:640:    72	def atomic_write_bytes(path: Path, data: bytes) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:641:    73	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:648:    80	def atomic_write_text(path: Path, content: str) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:649:    81	    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:693:   125	def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:694:   126	    """同一 sample rate / channel の wav 列を時系列で結合し atomic に書く.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:696:   128	    wave.Error は呼び出し側で catch して all-or-nothing rollback する
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:697:   129	    (Codex Phase 3-H review P2 #6 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:722:   154	    wave.Error / EOFError は呼び出し側で catch (Codex P2 #6 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:728:   160	def cleanup_stale_all() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:731:   163	    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:754:   186	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:756:   188	        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:759:   191	def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:762:   194	    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:789:   221	    両方とも atomic 書換 (Codex P2 #3 反映)。wave.Error は呼び出し側で catch。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:807:   239	    atomic_write_text(
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:818:   250	        " * Phase 3-H: voicevox_narration.py が all-or-nothing + atomic で書換える narration timeline。",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:841:   270	    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:916:   345	    fps = args.fps if args.fps is not None else read_video_config_fps()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:923:   352	    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:924:   353	    cleanup_stale_all()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:936:   365	        atomic_write_bytes(p, wav_bytes)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:950:   379	        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:951:   380	        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:961:   390	        concat_wavs_atomic(chunk_paths, out_path)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:962:   391	    except (wave.Error, EOFError) as e:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:963:   392	        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:973:   402	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:977:   406	    except (wave.Error, EOFError) as e:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:978:   407	        print(f"ERROR: WAV duration probe failed (wave.Error / EOFError): {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:979:   408	        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1014:/bin/zsh -lc "rg -n \"project-config|project_config|render_fps|read_video_config|VIDEO_CONFIG|fps|measure_duration_seconds|atomic_write|concat_wavs|cleanup_stale|narration\\.wav|chunk_meta|narrationData\" template/scripts/voicevox_narration.py template/src skills/supermovie-narration/SKILL.md" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1016:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1017:skills/supermovie-narration/SKILL.md:58:**Phase 3-D legacy**: chunk wav を時系列で結合し `public/narration.wav` を生成。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1018:skills/supermovie-narration/SKILL.md:63:- `src/Narration/narrationData.ts` を all-or-nothing で生成
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1019:skills/supermovie-narration/SKILL.md:65:- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1020:skills/supermovie-narration/SKILL.md:66:- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1021:skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1022:skills/supermovie-narration/SKILL.md:81:| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1023:skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1024:skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1025:skills/supermovie-narration/SKILL.md:85:優先順位は narrationData > narration.wav > null。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1026:skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1027:skills/supermovie-narration/SKILL.md:92:- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1028:skills/supermovie-narration/SKILL.md:94:- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1029:skills/supermovie-narration/SKILL.md:116:- `<PROJECT>/public/narration.wav` (Phase 3-D legacy、結合済)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1030:skills/supermovie-narration/SKILL.md:118:- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1031:skills/supermovie-narration/SKILL.md:119:- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1032:skills/supermovie-narration/SKILL.md:129:| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk + 旧 narration.wav 全削除、narrationData.ts 空 array (all-or-nothing) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1033:skills/supermovie-narration/SKILL.md:130:| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1034:skills/supermovie-narration/SKILL.md:131:| FPS 不正 (--fps <= 0 / videoConfig.ts FPS regex 失敗) | exit 4 (前者) or default 30 fallback (後者) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1035:skills/supermovie-narration/SKILL.md:140:    ├─ public/narration/chunk_meta.json (debug、fps + segments[])
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1036:skills/supermovie-narration/SKILL.md:141:    ├─ src/Narration/narrationData.ts   (Phase 3-H render 駆動)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1037:skills/supermovie-narration/SKILL.md:142:    └─ public/narration.wav              (Phase 3-D legacy fallback)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1038:skills/supermovie-narration/SKILL.md:146:    2) legacy narration.wav 存在 → 単一 <Audio> + base mute
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1039:skills/supermovie-narration/SKILL.md:152:**Studio を開いたまま narration.wav を生成した場合は再読み込み推奨**:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1044:template/scripts/voicevox_narration.py:17:- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1047:template/scripts/voicevox_narration.py:24:  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1048:template/scripts/voicevox_narration.py:26:- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1055:template/scripts/voicevox_narration.py:72:def atomic_write_bytes(path: Path, data: bytes) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1056:template/scripts/voicevox_narration.py:80:def atomic_write_text(path: Path, content: str) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1057:template/scripts/voicevox_narration.py:125:def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1059:template/scripts/voicevox_narration.py:160:def cleanup_stale_all() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1061:template/scripts/voicevox_narration.py:163:    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1064:template/scripts/voicevox_narration.py:186:    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1065:template/scripts/voicevox_narration.py:188:        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1066:template/scripts/voicevox_narration.py:191:def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1067:template/scripts/voicevox_narration.py:194:    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1077:template/scripts/voicevox_narration.py:239:    atomic_write_text(
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1080:template/scripts/voicevox_narration.py:270:    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1087:template/scripts/voicevox_narration.py:345:    fps = args.fps if args.fps is not None else read_video_config_fps()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1091:template/scripts/voicevox_narration.py:352:    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1092:template/scripts/voicevox_narration.py:353:    cleanup_stale_all()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1093:template/scripts/voicevox_narration.py:365:        atomic_write_bytes(p, wav_bytes)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1095:template/scripts/voicevox_narration.py:379:        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1096:template/scripts/voicevox_narration.py:380:        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1097:template/scripts/voicevox_narration.py:390:        concat_wavs_atomic(chunk_paths, out_path)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1098:template/scripts/voicevox_narration.py:402:    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1100:template/scripts/voicevox_narration.py:408:        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1167:/bin/zsh -lc 'git diff --no-renames d6f0846''^ d6f0846 -- template/scripts/voicevox_narration.py template/src/MainVideo.tsx template/src/Narration/NarrationAudio.tsx template/src/Narration/mode.ts skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1173:diff --git a/skills/supermovie-narration/SKILL.md b/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1175:--- a/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1176:+++ b/skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1183:+| WAV header 解析失敗 (wave.Error / EOFError) | exit 6、chunk + narration.wav 削除 (Codex Phase 3-H review P2 #6) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1196:+/supermovie-narration         ← ★ここ: VOICEVOX で 3 出力を atomic 生成
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1217:-- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1219:+- stale chunk + 旧 narration.wav (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1222:+Phase 3-H review fix (Codex CODEX_REVIEW_PHASE3H_20260504T213301, P1×2 + P2×4):
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1224:+  tempfile + os.replace で atomic 書き換え (SIGINT/disk full 安全、P2 #3)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1226:+  (P2 #4 + P2 #5、project-config.json の malformed AttributeError と Remotion 実値ズレを解消)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1227:+- wave.Error / EOFError を catch して exit 6 で all-or-nothing rollback (P2 #6)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1228:+- partial failure 時に旧 narration.wav も削除 (P1 #2、stale legacy 再生事故防止)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1266:+def atomic_write_bytes(path: Path, data: bytes) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1267:+    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1274:+def atomic_write_text(path: Path, content: str) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1275:+    """tempfile + os.replace で atomic 書換 (Codex Phase 3-H review P2 #3 反映)。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1291:+def concat_wavs_atomic(wavs: list[Path], out_path: Path) -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1292:+    """同一 sample rate / channel の wav 列を時系列で結合し atomic に書く.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1294:+    wave.Error は呼び出し側で catch して all-or-nothing rollback する
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1295:+    (Codex Phase 3-H review P2 #6 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1320:+    wave.Error / EOFError は呼び出し側で catch (Codex P2 #6 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1326:-def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1329:+def cleanup_stale_all() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1332:+    Codex Phase 3-H review P1 #2 反映: 旧 narration.wav が残ると partial failure 後に
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1338:@@ -132,35 +174,52 @@ def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1352:+    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)、atomic 書換。"""
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1355:+        atomic_write_text(NARRATION_DATA_TS, EMPTY_NARRATION_DATA)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1358:+def read_video_config_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1365:+    Codex Phase 3-H review P2 #4 + P2 #5 反映: project-config.json の
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1399:+    両方とも atomic 書換 (Codex P2 #3 反映)。wave.Error は呼び出し側で catch。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1410:+    atomic_write_text(
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1423:+        " * Phase 3-H: voicevox_narration.py が all-or-nothing + atomic で書換える narration timeline。",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1433:+    atomic_write_text(NARRATION_DATA_TS, "\n".join(ts_lines))
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1451:+    fps = args.fps if args.fps is not None else read_video_config_fps()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1457:-    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1458:-    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1460:+    # (chunk wav / chunk_meta.json / narration.wav / narrationData.ts 全部、Codex P1 #2)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1461:+    cleanup_stale_all()
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1470:+        atomic_write_bytes(p, wav_bytes)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1479:+        # Phase 3-H all-or-nothing (Codex P1 #2): 部分 chunk + narrationData 全削除
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1480:+        # cleanup_stale_all() で narration.wav も含めて clean されているので追加削除のみ
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1493:+        concat_wavs_atomic(chunk_paths, out_path)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1494:+    except (wave.Error, EOFError) as e:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1495:+        print(f"ERROR: WAV concat failed (wave.Error / EOFError): {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1505:     # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1510:+    except (wave.Error, EOFError) as e:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1511:+        print(f"ERROR: WAV duration probe failed (wave.Error / EOFError): {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1512:+        # narrationData/meta は temp 書き出しなので残らない、chunks は残るが atomic 失敗
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1555:+  // Phase 3-F asset gate + Phase 3-H per-segment Sequence の mode helper を共有
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1556:+  // (Codex Phase 3-H review P1 #1 反映)。chunks / legacy / none のいずれでも
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1602:+ * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1670:+ * Phase 3-H Codex review P1 #1 反映:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1687:+ * (Codex P3 #8 反映、毎 frame の some() 重複を防ぐ)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1846:docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1848:skills/supermovie-cut/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1849:skills/supermovie-image-gen/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1850:skills/supermovie-init/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1851:skills/supermovie-narration/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1852:skills/supermovie-se/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1853:skills/supermovie-skill-creator/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1854:skills/supermovie-slides/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1855:skills/supermovie-subtitles/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1856:skills/supermovie-telop-creator/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1857:skills/supermovie-transcribe/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1858:skills/supermovie-transcript-fix/SKILL.md
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1951:./skills/supermovie-skill-creator/SKILL.md:170:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1953:./skills/supermovie-se/SKILL.md:204:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1996:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3057:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2046:./skills/supermovie-transcript-fix/SKILL.md:265:**transcript_fixed.json** — 修正済み:
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2047:./skills/supermovie-transcript-fix/SKILL.md:346:  transcript_fixed.json（修正済み）
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2048:./skills/supermovie-transcript-fix/SKILL.md:350:→ transcript_fixed.json を確認
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2049:./skills/supermovie-transcript-fix/SKILL.md:379:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2070:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1438:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2048:./skills/supermovie-narration/SKILL.md:108:| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2124:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4588:skills/supermovie-transcript-fix/SKILL.md:350:→ transcript_fixed.json を確認
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2134:./skills/supermovie-subtitles/SKILL.md:4:  transcript_fixed.jsonからテロップ（telopData.ts）とタイトル（titleData.ts）を
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2135:./skills/supermovie-subtitles/SKILL.md:37:- [ ] `transcript_fixed.json` が存在し `words` 配列がある
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2136:./skills/supermovie-subtitles/SKILL.md:68:- `transcript_fixed.json` → `words`, `segments`
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2137:./skills/supermovie-subtitles/SKILL.md:88:transcript_fixed.json の `words` を `segments` 単位でグループ化。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2138:./skills/supermovie-subtitles/SKILL.md:403:transcript_fixed.json の `segments` を俯瞰し、話題の転換点を検出。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2139:./skills/supermovie-subtitles/SKILL.md:513:| transcript_fixed.json なし | `/supermovie-transcribe` → `/supermovie-transcript-fix` を促す |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2140:./skills/supermovie-subtitles/SKILL.md:531:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2141:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:19:2. `git diff roku/phase3g-visual-smoke..HEAD` で Phase 3-H 範囲確認
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2142:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:43:   - tsc strict mode で any 漏れ・unused warn
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2143:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:105:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2144:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:107:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2145:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:108:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2146:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:200:/bin/zsh -lc 'git diff --name-status roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2147:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2148:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:238:-"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2149:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:239:+"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2150:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:244: - 入力: transcript_fixed.json の segments[] / project-config.json の tone
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2151:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:508:/bin/zsh -lc 'git diff --stat roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2152:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2153:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:527:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/visual_smoke.py skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2154:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:707: 3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2155:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:784: | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2156:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:920:     2	"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2157:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:924:     6	- 入力: transcript_fixed.json の segments[] / project-config.json の tone
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2158:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1196:   278	    transcript_path = PROJ / "transcript_fixed.json"
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2159:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1198:   280	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2160:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1494:     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2161:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1540:    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2162:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1616:   126	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2163:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1625:   135	    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2164:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1710:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2165:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1768:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2166:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2039:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2167:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2050:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3099:template/scripts/voicevox_narration.py:2:"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2168:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2078:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4335:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2169:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2089:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4393:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2170:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2148:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2171:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2149:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1335:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2172:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2150:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1432:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2173:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2401:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2174:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2402:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2175:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2437:     6	// telop-templates-30.zip 由来の component が `any` を使っているため、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2176:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2438:     7	// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2177:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2443:    12	      "@typescript-eslint/no-explicit-any": "warn",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2178:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2486:85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2179:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2712:/bin/zsh -lc "git grep -n -- 'voicevox_narration.py' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2180:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2714:/bin/zsh -lc "git grep -n -- '--keep-chunks' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2181:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2720:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2182:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2721:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2183:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2722:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2184:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2723:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2185:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2724:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2186:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2725:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2187:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2726:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2188:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2727:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2189:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2728:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:12:    python3 scripts/voicevox_narration.py
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2190:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2729:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:13:    python3 scripts/voicevox_narration.py --speaker 3
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2191:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2730:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:14:    python3 scripts/voicevox_narration.py --script narration.txt
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2192:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2731:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:15:    python3 scripts/voicevox_narration.py --list-speakers
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2193:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2732:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:16:    python3 scripts/voicevox_narration.py --require-engine
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2194:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2733:roku/phase3g-visual-smoke:template/src/Narration/NarrationAudio.tsx:15: * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2195:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2740:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:59:`--keep-chunks` で chunk 個別 wav も保持 (debug)。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2196:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2741:roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2197:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2742:roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:121:    ap.add_argument("--keep-chunks", action="store_true",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2198:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3059:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD --name-only' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2199:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3091:     2	"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2200:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3096:     7	    <PROJECT>/transcript_fixed.json  - segments[] / words[]
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2201:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3189:template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2202:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3197:template/scripts/generate_slide_plan.py:87:    config_path = PROJ / "project-config.json"
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2203:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3198:template/scripts/generate_slide_plan.py:89:        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2204:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3205:template/scripts/build_slide_data.py:2:"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2205:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3209:template/scripts/build_slide_data.py:322:        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2206:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3263:/bin/zsh -lc 'git diff --check roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2207:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3495:   250	    if any(f < 0 for f in frames):
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2208:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3508:   263	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2209:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3620:    fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2210:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3700:/bin/zsh -lc "git show roku/phase3g-visual-smoke:template/scripts/visual_smoke.py | nl -ba | sed -n '135,215p'" in /Users/rokumasuda/.claude/plugins/supermovie
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2211:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3805:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2212:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:3854:Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2214:./skills/supermovie-image-gen/SKILL.md:286:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2215:./skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2216:./skills/supermovie-narration/SKILL.md:50:3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2217:./skills/supermovie-narration/SKILL.md:126:| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2218:./skills/supermovie-narration/SKILL.md:137:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2219:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2221:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2224:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2259:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:933:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2261:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:941:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2264:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:944:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2381:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1304:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2383:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1307:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2386:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1310:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2416:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1344:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:933:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2418:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1346:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:941:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2421:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1349:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:944:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2498:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1454:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2524:./skills/supermovie-cut/SKILL.md:5:  Silero VAD + transcript_fixed.json + Claude LLM分析の3層で高精度にカット判定。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2525:./skills/supermovie-cut/SKILL.md:34:- [ ] `transcript_fixed.json` が存在し `words` 配列がある
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2526:./skills/supermovie-cut/SKILL.md:172:transcript_fixed.json の words 間のギャップからも無音を検出。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2527:./skills/supermovie-cut/SKILL.md:193:transcript_fixed.json のテキストを分析し、**内容的に不要な区間**を判定。
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2528:./skills/supermovie-cut/SKILL.md:405:| transcript_fixed.json がない | `/supermovie-transcript-fix` を促す |
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2529:./skills/supermovie-cut/SKILL.md:420:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2530:./skills/supermovie-init/SKILL.md:274:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2535:./skills/supermovie-slides/SKILL.md:4:  transcript_fixed.json と project-config.json から SlideSegment[] を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2536:./skills/supermovie-slides/SKILL.md:15:Senior video editor として、transcript_fixed.json の segments から話題区間を抽出し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2537:./skills/supermovie-slides/SKILL.md:32:- `<PROJECT>/transcript_fixed.json` から `segments[]` (start/end ms + text) と `words[]`
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2538:./skills/supermovie-slides/SKILL.md:100:ANTHROPIC_API_KEY=sk-ant-... python3 <PROJECT>/scripts/generate_slide_plan.py \
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2539:./skills/supermovie-slides/SKILL.md:101:  --output <PROJECT>/slide_plan.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2540:./skills/supermovie-slides/SKILL.md:102:python3 <PROJECT>/scripts/build_slide_data.py --plan <PROJECT>/slide_plan.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2541:./skills/supermovie-slides/SKILL.md:111:### slide_plan.json schema
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2542:./skills/supermovie-slides/SKILL.md:115:  "version": "supermovie.slide_plan.v1",
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2543:./skills/supermovie-slides/SKILL.md:133:- `version` 完全一致 (`supermovie.slide_plan.v1`)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2544:./skills/supermovie-slides/SKILL.md:172:    ↓ transcript_fixed.json + cutData.ts
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2545:./skills/supermovie-transcribe/SKILL.md:500:    ↓ transcript_fixed.json
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:2564:./docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:1016:skills/supermovie-narration/SKILL.md:4:  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:3066:   257	    # 環境チェック (Codex Phase 3-G review P1 #1 反映、render 失敗を環境問題として早期検知)
docs/reviews/CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514.md:3176:`SKILL.md` の FPS 記述と実装の間に不一致がありそうです。あわせて、read-only で副作用が出にくい範囲の静的チェックだけ走らせます。

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "python3 -c \"import ast, pathlib; ast.parse(pathlib.Path('template/scripts/voicevox_narration.py').read_text(encoding='utf-8')); print('voicevox_narration.py ast_ok')\"" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
voicevox_narration.py ast_ok

hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/build_slide_data.py | sed -n '1,120p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba skills/supermovie-slides/SKILL.md | sed -n '25,140p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
    25	│  transcript  │    │  segments を │    │   生成       │    │   書き出し   │
    26	│  config      │    │  topic 単位に│    │  Slide[] へ  │    │  + verify    │
    27	└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
    28	```
    29	
    30	## Phase 1: 入力データ読込
    31	
    32	- `<PROJECT>/transcript_fixed.json` から `segments[]` (start/end ms + text) と `words[]`
    33	- `<PROJECT>/project-config.json` から `format` (youtube/short/square)、`tone`
    34	- (任意) `<PROJECT>/src/cutData.ts` から CutSegment[] (cut 後 frame に変換するため)
    35	- (任意) `<PROJECT>/src/Title/titleData.ts` から TitleSegment[] (タイトルとの重複回避)
    36	
    37	## Phase 2: 話題分割 (deterministic first)
    38	
    39	Codex Phase 3B design (2026-05-04) 推奨: deterministic first、LLM は別 phase で optional plan。
    40	
    41	### 2-1. 話題区間抽出 (mode=topic、推奨)
    42	
    43	連続する segments を「話題」単位にグループ化する:
    44	- 隣接 segments の境界が 1.5 秒以上の無音 (VAD silence) であれば話題区切り
    45	- または 4-5 segments で 1 group (機械的、フォールバック)
    46	
    47	各話題 group の代表 text を以下で抽出:
    48	- **title**: 先頭 segment の text 冒頭 12-15 字 (format に応じて trim)
    49	- **subtitle**: 任意。最も重要な segment.text の続き 20-30 字
    50	- **bullets**: group 内の各 segment.text の冒頭 12-18 字を 1 bullet に。最大 5 個
    51	
    52	### 2-2. segment 単位 (mode=segment、シンプル fallback)
    53	
    54	1 transcript segment = 1 slide。短い動画や test 用。
    55	- title = segment.text の冒頭
    56	- bullets なし
    57	- 表示時間 = segment 全長
    58	
    59	## Phase 3: SlideSegment 生成
    60	
    61	`SlideSegment` schema (`src/Slides/types.ts`):
    62	```typescript
    63	{ id, startFrame, endFrame, title, subtitle?, bullets?, align?, backgroundColor?, textColor?, videoLayer? }
    64	```
    65	
    66	frame 計算:
    67	- transcript の word.start (ms) → cutData 経由で playback frame に変換
    68	- cutData が存在しない場合は単純に `ms / 1000 * FPS`
    69	
    70	トーン別の見た目:
    71	| トーン | align | backgroundColor | bullet emphasis 比率 |
    72	|--------|-------|------------------|----------------------|
    73	| プロフェッショナル | center | `rgba(20, 26, 44, 0.92)` | 0-1 / slide |
    74	| エンタメ | left | `#101a2c` | 1-2 / slide |
    75	| カジュアル | left | `rgba(40, 30, 60, 0.9)` | 1 / slide |
    76	| 教育的 | left | `#0f2540` | 1-2 / slide |
    77	
    78	videoLayer:
    79	- 通常 `'visible'` (動画は背景のまま、スライドは半透明オーバーレイ)
    80	- フルスクリーンタイトル時のみ `'hidden'` を検討
    81	
    82	## Phase 4: ファイル書き出し + verify
    83	
    84	- 出力先: `<PROJECT>/src/Slides/slideData.ts`
    85	- バリデーション:
    86	  - frame 範囲が CUT_TOTAL_FRAMES 内
    87	  - title が空でない
    88	  - bullets が 0-5 個
    89	  - 隣接 slide が overlap しない
    90	- 既存 `slideData.ts` を `slideData.backup.ts` として退避
    91	
    92	## 実行コマンド
    93	
    94	```bash
    95	# Phase 3-B (deterministic、default)
    96	python3 <PROJECT>/scripts/build_slide_data.py
    97	python3 <PROJECT>/scripts/build_slide_data.py --mode topic
    98	
    99	# Phase 3-C (LLM optional plan、ANTHROPIC_API_KEY 必須):
   100	ANTHROPIC_API_KEY=sk-ant-... python3 <PROJECT>/scripts/generate_slide_plan.py \
   101	  --output <PROJECT>/slide_plan.json
   102	python3 <PROJECT>/scripts/build_slide_data.py --plan <PROJECT>/slide_plan.json
   103	# --strict-plan で plan 検証失敗時 exit 2 (default は warning + deterministic fallback)
   104	```
   105	
   106	## Phase 3-C: LLM optional plan (Codex CODEX_PHASE3C_LLM_PLAN_20260504T201229)
   107	
   108	**LLM 経路は word index ベースの plan を返し、frame は build script が変換する**。
   109	これにより LLM が frame 計算をミスっても整合性が保たれる。
   110	
   111	### slide_plan.json schema
   112	
   113	```json
   114	{
   115	  "version": "supermovie.slide_plan.v1",
   116	  "slides": [
   117	    {
   118	      "id": 1,
   119	      "startWordIndex": 0,
   120	      "endWordIndex": 30,
   121	      "title": "短い見出し",
   122	      "subtitle": "任意",
   123	      "bullets": [{ "text": "要点", "emphasis": true }],
   124	      "align": "left",
   125	      "videoLayer": "visible"
   126	    }
   127	  ]
   128	}
   129	```
   130	
   131	### validation ルール (build_slide_data.py)
   132	
   133	- `version` 完全一致 (`supermovie.slide_plan.v1`)
   134	- `slides` が配列、`id` 昇順
   135	- `0 <= startWordIndex <= endWordIndex < len(words)`
   136	- 隣接 slide の word range が overlap しない
   137	- `title` 非空 + format 別 max 文字数以内
   138	- `bullets` ≤ 5、各 `text` ≤ format 別 max
   139	- `align` ∈ {"center","left"}、`videoLayer` ∈ {"visible","dimmed","hidden"}
   140	

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
    24	from pathlib import Path
    25	
    26	PROJ = Path(__file__).resolve().parent.parent
    27	FPS = 60  # videoConfig.FPS と同期、後段で project-config から読むよう拡張可能
    28	SILENCE_THRESHOLD_MS = 1500  # 1.5 秒以上の無音で話題区切り
    29	TITLE_MAX_CHARS = {"youtube": 18, "short": 14, "square": 16}
    30	BULLET_MAX_CHARS = {"youtube": 24, "short": 18, "square": 20}
    31	MAX_BULLETS_PER_SLIDE = 5
    32	MAX_SEGMENTS_PER_SLIDE = 5  # silence 検出失敗時の機械 fallback
    33	
    34	
    35	def load_json(p: Path):
    36	    return json.loads(p.read_text(encoding="utf-8"))
    37	
    38	
    39	def build_cut_segments_from_vad(vad: dict | None) -> list[dict]:
    40	    if not vad or "speech_segments" not in vad:
    41	        return []
    42	    out = []
    43	    cursor_ms = 0
    44	    for i, seg in enumerate(vad["speech_segments"]):
    45	        s_ms = seg["start"]
    46	        e_ms = seg["end"]
    47	        dur_ms = e_ms - s_ms
    48	        out.append({
    49	            "id": i + 1,
    50	            "originalStartMs": s_ms,
    51	            "originalEndMs": e_ms,
    52	            "playbackStart": round(cursor_ms / 1000 * FPS),
    53	            "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
    54	        })
    55	        cursor_ms += dur_ms
    56	    return out
    57	
    58	
    59	def ms_to_playback_frame(ms: int, cut_segments: list[dict]) -> int | None:
    60	    if not cut_segments:
    61	        return round(ms / 1000 * FPS)
    62	    for cs in cut_segments:
    63	        if cs["originalStartMs"] <= ms <= cs["originalEndMs"]:
    64	            offset_ms = ms - cs["originalStartMs"]
    65	            return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
    66	    return None
    67	
    68	
    69	def truncate(text: str, max_chars: int) -> str:
    70	    text = text.strip()
    71	    if len(text) <= max_chars:
    72	        return text
    73	    return text[:max_chars - 1] + "…"
    74	
    75	
    76	def group_topics(segments: list[dict], threshold_ms: int = SILENCE_THRESHOLD_MS) -> list[list[dict]]:
    77	    """隣接 segments の間隔 >= threshold_ms で話題区切り."""
    78	    if not segments:
    79	        return []
    80	    groups: list[list[dict]] = [[segments[0]]]
    81	    for prev, cur in zip(segments, segments[1:]):
    82	        gap_ms = cur["start"] - prev["end"]
    83	        if gap_ms >= threshold_ms or len(groups[-1]) >= MAX_SEGMENTS_PER_SLIDE:
    84	            groups.append([cur])
    85	        else:
    86	            groups[-1].append(cur)
    87	    return groups
    88	
    89	
    90	def style_for_tone(tone: str) -> dict:
    91	    table = {
    92	        "プロフェッショナル": {"align": "center", "bg": "rgba(20, 26, 44, 0.92)", "emphasis_ratio": 0.2},
    93	        "エンタメ": {"align": "left", "bg": "#101a2c", "emphasis_ratio": 0.4},
    94	        "カジュアル": {"align": "left", "bg": "rgba(40, 30, 60, 0.9)", "emphasis_ratio": 0.3},
    95	        "教育的": {"align": "left", "bg": "#0f2540", "emphasis_ratio": 0.4},
    96	    }
    97	    return table.get(tone, table["プロフェッショナル"])
    98	
    99	
   100	def build_slides_topic_mode(segments: list[dict], cut_segments: list[dict],
   101	                            fmt: str, tone: str) -> list[dict]:
   102	    title_max = TITLE_MAX_CHARS.get(fmt, TITLE_MAX_CHARS["short"])
   103	    bullet_max = BULLET_MAX_CHARS.get(fmt, BULLET_MAX_CHARS["short"])
   104	    style = style_for_tone(tone)
   105	    cut_total = cut_segments[-1]["playbackEnd"] if cut_segments else None
   106	
   107	    slides: list[dict] = []
   108	    groups = group_topics(segments)
   109	    for group_idx, group in enumerate(groups):
   110	        first = group[0]
   111	        last = group[-1]
   112	
   113	        pb_start = ms_to_playback_frame(first["start"], cut_segments)
   114	        pb_end = ms_to_playback_frame(last["end"], cut_segments)
   115	        if pb_start is None or pb_end is None:
   116	            continue
   117	        if cut_total is not None:
   118	            pb_end = min(pb_end, cut_total)
   119	        if pb_end <= pb_start:
   120	            continue

exec
/bin/zsh -lc "nl -ba template/src/Slides/types.ts && nl -ba template/src/Slides/slideData.ts | sed -n '1,80p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	/**
     2	 * Phase 3 SlideSequence 用 schema (Codex Phase 3 推奨: 別レイヤー、画像扱いと分離).
     3	 *
     4	 * 1 Slide = タイトル + 箇条書き or 自由 React content。frame 範囲で表示制御。
     5	 *
     6	 * SuperMovie の他レイヤー (TelopPlayer / ImageSequence / TitleSequence) と同じく
     7	 * data 駆動で、後段 skill (将来の supermovie-slides) が slideData.ts を生成する想定。
     8	 */
     9	
    10	export type SlideAlignment = 'center' | 'left';
    11	
    12	export interface SlideBullet {
    13	  text: string;
    14	  /** highlighted bullet は色違いで強調 (Codex 推奨: skill 側で word→bullet 抽出時に true 設定) */
    15	  emphasis?: boolean;
    16	}
    17	
    18	export interface SlideSegment {
    19	  id: number;
    20	  startFrame: number;
    21	  endFrame: number;
    22	  /** スライドのメインタイトル */
    23	  title: string;
    24	  /** 副題 (任意) */
    25	  subtitle?: string;
    26	  /** 箇条書き (任意) */
    27	  bullets?: SlideBullet[];
    28	  /** 配置 */
    29	  align?: SlideAlignment;
    30	  /** 背景色 (CSS color、省略時はテーマ既定) */
    31	  backgroundColor?: string;
    32	  /** テキスト色 (CSS color、省略時はテーマ既定) */
    33	  textColor?: string;
    34	  /** 表示中の動画レイヤー (画面 0 透過 / dimmed / hidden) */
    35	  videoLayer?: 'visible' | 'dimmed' | 'hidden';
    36	}
     1	import type { SlideSegment } from './types';
     2	
     3	// ==== スライドデータ (Phase 3-A) ====
     4	// 将来の supermovie-slides skill で transcript 段落タイトル + Outline から自動生成。
     5	// 現時点は placeholder 空配列。サンプルはコメントアウトで残す。
     6	
     7	export const slideData: SlideSegment[] = [
     8	  // 例 (cut 後 frame 0-180 でフルスクリーンタイトル):
     9	  // {
    10	  //   id: 1,
    11	  //   startFrame: 0,
    12	  //   endFrame: 180,
    13	  //   title: 'Claude Code 完全自動編集',
    14	  //   subtitle: 'SuperMovie Phase 3 PoC',
    15	  //   align: 'center',
    16	  // },
    17	  // 例 (箇条書きスライド):
    18	  // {
    19	  //   id: 2,
    20	  //   startFrame: 600,
    21	  //   endFrame: 900,
    22	  //   title: 'パイプラインの強み',
    23	  //   bullets: [
    24	  //     { text: '文字起こし → 誤字修正 → カット → テロップ' },
    25	  //     { text: '30 templates から自動選択', emphasis: true },
    26	  //     { text: 'BudouX で意味境界を保つ改行' },
    27	  //   ],
    28	  //   align: 'left',
    29	  //   backgroundColor: '#101a2c',
    30	  // },
    31	];

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba skills/supermovie-image-gen/SKILL.md | sed -n '250,310p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   250	🎨 生成画像: <N>枚
   251	   - infographic: <n>枚
   252	   - photo: <n>枚
   253	   - overlay: <n>枚
   254	📂 保存先: public/images/generated/
   255	
   256	📄 insertImageData.ts 更新済み
   257	
   258	次のステップ:
   259	→ npm run dev で画像の表示タイミングを確認
   260	→ /supermovie-se でSE配置（画像出現タイミングにもSE付与）
   261	```
   262	
   263	---
   264	
   265	## エラーハンドリング
   266	
   267	| エラー | 対応 |
   268	|--------|------|
   269	| GEMINI_API_KEY 未設定 | 設定方法を案内。画像なしで続行も提案 |
   270	| Gemini API エラー（レート制限） | 5秒待って再試行。3回失敗で該当画像スキップ |
   271	| 生成画像の品質が低い | プロンプト調整して再生成を提案 |
   272	| telopData.ts が空 | `/supermovie-subtitles` の実行を促す |
   273	| project-config.json なし | デフォルト（youtube 16:9）で続行 |
   274	| gemini-api-image スキルが見つからない | インストール方法を案内 |
   275	
   276	---
   277	
   278	## 連携マップ
   279	
   280	```
   281	/supermovie-init              ← ヒアリング → プロジェクト作成
   282	    ↓
   283	/supermovie-transcribe        ← 文字起こし（ローカル無料）
   284	    ↓ transcript.json
   285	/supermovie-transcript-fix    ← 誤字修正（辞書 + Claude LLM）
   286	    ↓ transcript_fixed.json
   287	/supermovie-cut               ← 不要区間カット（VAD + LLM分析）
   288	    ↓ cutData.ts
   289	/supermovie-subtitles         ← テロップ＆タイトル生成
   290	    ↓ telopData.ts + titleData.ts
   291	/supermovie-image-gen         ← ★ここ: 画像生成 + 配置データ
   292	    ↓ insertImageData.ts
   293	/supermovie-se                ← SE自動配置
   294	    ↓
   295	npm run dev                   ← プレビュー
   296	```

codex
対象は `roku/phase3h-narration-sequence` の HEAD `d6f0846` として確認しました（Bash 実測: `git rev-parse --abbrev-ref HEAD && git rev-parse HEAD`）。`lint/tsc` は `template/node_modules` 不在で未実行、Python は AST parse のみ OK です（Bash 実測）。

**Part A**
| 指摘 | verdict | 根拠 |
|---|---:|---|
| P1#1 mode helper | ✅ closed | `mode.ts` 新規、`NarrationAudio` と `MainVideo` が `getNarrationMode()` 経由（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:29), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:17), [MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21)）。 |
| P1#2 cleanup stale all | ⚠️ partial | 通常 path では旧 `narration.wav` を削除し、partial failure では chunk を消す（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:177), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:381)）。ただし `unlink()` 失敗を warn で継続するため、削除失敗時は stale legacy が残る（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:180)）。 |
| P2#3 atomic write | ✅ closed | `narrationData.ts` / `chunk_meta.json` / `chunk_NNN.wav` / `narration.wav` は atomic helper または `concat_wavs_atomic()` 経由（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:72), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:125), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:365), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:390)）。 |
| P2#4 FPS config path | ✅ closed | narration script は `src/videoConfig.ts` regex 経路で、旧 `read_render_fps()` / `project-config.json` FPS 経路は撤去（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:191), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:345)）。 |
| P2#5 FPS source unified | ✅ closed | Remotion は `videoConfig.FPS` を使い、script も同じ `videoConfig.ts` を読む（[Root.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:345)）。`--fps <= 0` は生成 path で exit 4（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:346)）。 |
| P2#6 wave.Error catch | ✅ closed | concat と duration probe の両方で `wave.Error` / `EOFError` を catch し rollback（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:389), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:404)）。 |
| P3#7 MainVideo redundancy | ✅ closed | `startsWith("narration/chunk_")` / `NARRATION_CHUNK_PREFIX` は検出されず、helper 判定に集約（Bash 実測: `rg startsWith...`、[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21)）。 |
| P3#8 Set lookup | ✅ closed | `some()` 重複は `Set` lookup に変更（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:30)）。 |
| P3#9 SKILL.md map | ⚠️ partial | 連携マップは 3 出力 + `getNarrationMode()` 三経路に更新済み（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:133)）。ただし実装参照は旧 `hasLegacyNarration` / `hasChunkNarration` のまま、FPS 優先順位も旧 `project-config.json` のまま（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:69), [SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:90)）。 |

**新規指摘**
- P2: concurrent run 非対応。atomic temp が固定名 `.{name}.tmp` なので同一 project で同時実行すると tmp 衝突し、さらに `cleanup_stale_all()` が他プロセスの生成物を削除し得ます（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:75), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:134), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:353)）。
- P3: `concat_wavs_atomic()` は write 中例外時に `.narration.wav.tmp` を finally unlink しない（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:134), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:144), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:390)）。
- P3: `getNarrationMode()` は `MainVideo` と `NarrationAudio` から呼ばれ、毎回 `getStaticFiles()` から `Set` を作るため cache 化余地あり（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:17), [mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:30)）。
- ts circular はコード上見えません。`mode.ts` は `narrationData` と type だけを import し、`index.ts` は export 集約のみです（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:1), [index.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/index.ts:1)）。

**Part B**
推奨: **v. transcript timing alignment**。理由は、現状 `startFrame` が chunk duration の単純累積で、`collect_chunks()` が transcript の `start/end` を捨てて text だけにしているためです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:224), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:281)）。次点: **iii. transcript-driven b-roll planner**。`insertImageData.ts` は既に data-driven なので、`scene_plan.json` を足す拡張先があるためです（[insertImageData.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/insertImageData.ts:8), [types.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/types.ts:1)）。API 実行は Roku 判断領域です（Roku 発言: “Anthropic API 課金あり”）。

Phase 3-I 設計概要: `collect_chunks()` を `{text, sourceStartMs, sourceEndMs}` に変更し、`transcript_fixed.json segments[].start/end` を保持する。`startFrame` は transcript start を `videoConfig.FPS` で frame 化し、cut 後 timeline がある場合は既存 slide 側の `ms_to_playback_frame()` 相当を共通化する（[supermovie-slides/SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-slides/SKILL.md:32), [build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:59)）。`durationInFrames` は引き続き WAV 実測を使う（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:226)）。

危険ポイント top3: cut 後 mapping を外すとカット後動画で narration がズレる（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:39)）。生成音声が次 chunk 開始を越えると `<Sequence>` が重なり二重 narration になる（[NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:22)）。base 音声は narration mode で全 mute なので、意図しない gap は無音になる（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:22)）。

Codex review 重点: timestamp を捨てない schema、cut-aware frame 変換、overlap/gap policy、`videoConfig.FPS` 一次 source 維持、rollback が `narration.wav` / chunks / `narrationData.ts` / `chunk_meta.json` を一貫させるか。
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
200,841
対象は `roku/phase3h-narration-sequence` の HEAD `d6f0846` として確認しました（Bash 実測: `git rev-parse --abbrev-ref HEAD && git rev-parse HEAD`）。`lint/tsc` は `template/node_modules` 不在で未実行、Python は AST parse のみ OK です（Bash 実測）。

**Part A**
| 指摘 | verdict | 根拠 |
|---|---:|---|
| P1#1 mode helper | ✅ closed | `mode.ts` 新規、`NarrationAudio` と `MainVideo` が `getNarrationMode()` 経由（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:29), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:17), [MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21)）。 |
| P1#2 cleanup stale all | ⚠️ partial | 通常 path では旧 `narration.wav` を削除し、partial failure では chunk を消す（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:177), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:381)）。ただし `unlink()` 失敗を warn で継続するため、削除失敗時は stale legacy が残る（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:180)）。 |
| P2#3 atomic write | ✅ closed | `narrationData.ts` / `chunk_meta.json` / `chunk_NNN.wav` / `narration.wav` は atomic helper または `concat_wavs_atomic()` 経由（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:72), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:125), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:365), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:390)）。 |
| P2#4 FPS config path | ✅ closed | narration script は `src/videoConfig.ts` regex 経路で、旧 `read_render_fps()` / `project-config.json` FPS 経路は撤去（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:191), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:345)）。 |
| P2#5 FPS source unified | ✅ closed | Remotion は `videoConfig.FPS` を使い、script も同じ `videoConfig.ts` を読む（[Root.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:345)）。`--fps <= 0` は生成 path で exit 4（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:346)）。 |
| P2#6 wave.Error catch | ✅ closed | concat と duration probe の両方で `wave.Error` / `EOFError` を catch し rollback（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:389), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:404)）。 |
| P3#7 MainVideo redundancy | ✅ closed | `startsWith("narration/chunk_")` / `NARRATION_CHUNK_PREFIX` は検出されず、helper 判定に集約（Bash 実測: `rg startsWith...`、[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21)）。 |
| P3#8 Set lookup | ✅ closed | `some()` 重複は `Set` lookup に変更（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:30)）。 |
| P3#9 SKILL.md map | ⚠️ partial | 連携マップは 3 出力 + `getNarrationMode()` 三経路に更新済み（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:133)）。ただし実装参照は旧 `hasLegacyNarration` / `hasChunkNarration` のまま、FPS 優先順位も旧 `project-config.json` のまま（[SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:69), [SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:90)）。 |

**新規指摘**
- P2: concurrent run 非対応。atomic temp が固定名 `.{name}.tmp` なので同一 project で同時実行すると tmp 衝突し、さらに `cleanup_stale_all()` が他プロセスの生成物を削除し得ます（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:75), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:134), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:353)）。
- P3: `concat_wavs_atomic()` は write 中例外時に `.narration.wav.tmp` を finally unlink しない（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:134), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:144), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:390)）。
- P3: `getNarrationMode()` は `MainVideo` と `NarrationAudio` から呼ばれ、毎回 `getStaticFiles()` から `Set` を作るため cache 化余地あり（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:21), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:17), [mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:30)）。
- ts circular はコード上見えません。`mode.ts` は `narrationData` と type だけを import し、`index.ts` は export 集約のみです（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:1), [index.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/index.ts:1)）。

**Part B**
推奨: **v. transcript timing alignment**。理由は、現状 `startFrame` が chunk duration の単純累積で、`collect_chunks()` が transcript の `start/end` を捨てて text だけにしているためです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:224), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:281)）。次点: **iii. transcript-driven b-roll planner**。`insertImageData.ts` は既に data-driven なので、`scene_plan.json` を足す拡張先があるためです（[insertImageData.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/insertImageData.ts:8), [types.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/types.ts:1)）。API 実行は Roku 判断領域です（Roku 発言: “Anthropic API 課金あり”）。

Phase 3-I 設計概要: `collect_chunks()` を `{text, sourceStartMs, sourceEndMs}` に変更し、`transcript_fixed.json segments[].start/end` を保持する。`startFrame` は transcript start を `videoConfig.FPS` で frame 化し、cut 後 timeline がある場合は既存 slide 側の `ms_to_playback_frame()` 相当を共通化する（[supermovie-slides/SKILL.md](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-slides/SKILL.md:32), [build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:59)）。`durationInFrames` は引き続き WAV 実測を使う（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:226)）。

危険ポイント top3: cut 後 mapping を外すとカット後動画で narration がズレる（[build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:39)）。生成音声が次 chunk 開始を越えると `<Sequence>` が重なり二重 narration になる（[NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:22)）。base 音声は narration mode で全 mute なので、意図しない gap は無音になる（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:22)）。

Codex review 重点: timestamp を捨てない schema、cut-aware frame 変換、overlap/gap policy、`videoConfig.FPS` 一次 source 維持、rollback が `narration.wav` / chunks / `narrationData.ts` / `chunk_meta.json` を一貫させるか。

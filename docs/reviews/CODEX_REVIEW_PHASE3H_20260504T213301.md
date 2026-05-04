Reading additional input from stdin...
2026-05-04T12:33:01.201276Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/rokumasuda/.claude/plugins/supermovie
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019df2fa-4512-77f2-9f39-b239fb2eaa28
--------
user
SuperMovie Plugin の roku/phase3h-narration-sequence branch を超厳しめに review。直近 2 commit (41dbec5 Phase 3-H per-segment Sequence + 85e824e vstack letterbox fix) を対象。

照合手順:
1. `git log roku/phase3f-asset-gate..HEAD --oneline` で全 commit 把握
2. `git diff roku/phase3g-visual-smoke..HEAD` で Phase 3-H 範囲確認
3. 各変更ファイル Read

重点チェック (Phase 3-H、自走実装したので厳しく):
A) voicevox_narration.py 構造変化
   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
   - all-or-nothing: partial failure 時の chunk 削除 + reset_narration_data_ts() の race
   - measure_duration_seconds の wave header 信頼性 (HE-AAC や VOICEVOX 出力 wav 互換性)
   - read_render_fps の type 検証 (cfg["source"] が None の時の AttributeError)
   - write_narration_data の ts file generation で text に backslash や quote 含むケース
   - --keep-chunks 撤去で既存使用者影響範囲 (skill 内文書 / 他 script の引数)
   - chunk_meta.json schema (fps/total_frames/segments[]) と narrationData.ts duplication

B) NarrationAudio.tsx の三段 fallback
   - narrationData non-empty + 一部 chunk 不在ケースで null 返り、render 全体が止まらないか
   - <Sequence> の from/durationInFrames の境界 (durationInFrames=0 は Remotion で reject される、min 1 で防げているか)
   - useMemo 等の最適化が必要か (毎 frame staticFiles.some が回る) 

C) MainVideo.tsx mute logic 拡張
   - hasChunkNarration 三条件 AND の論理過剰 (narrationData.length > 0 だけで実質判定済みでは?)
   - startsWith("narration/chunk_") の prefix collision (例: narration/chunk_meta.json は wav じゃないのに引っ掛かる)

D) types.ts / narrationData.ts placeholder
   - eslint-config-flat 4.x で空 array のまま prettier 違反になるか (trailingComma)
   - tsc strict mode で any 漏れ・unused warn

E) Phase 3-G new P1 fix (vstack letterbox)
   - CELL_W=480 / CELL_H=360 hardcode の妥当性 (e.g., 4K 元画像で読みづらい問題)
   - drawtext label 位置 x=20 y=20 が letterbox の上下黒帯と被らないか

F) skill SKILL.md
   - エラーハンドリング table の exit 6 行が他コマンド (--allow-partial) と矛盾しないか
   - 連携マップ / 状態テーブルの記述が実装と一致するか

G) 横断
   - Phase 3-D (concat_wavs) と Phase 3-H (per-segment) の二重出力で disk 容量倍化、cleanup 戦略
   - Studio 起動中に narration を再生成した時の getStaticFiles cache 残存問題 (Phase 3-F 同様)
   - Codex Phase 3-H consultation の危険ポイント top3 (chunk-only mute / FPS / stale) が全部 fix されているか

出力フォーマット:
- P0/P1/P2/P3 分類、各指摘 file:line / 詳細 / 修正案 / Effort / 自走可否
- LGTM 禁止、最低 1 件は新規指摘
- Phase 3-G fix 再 review が token 切れで verdict 出なかったため、A〜G を網羅して欲しい。短く決定的に。
2026-05-04T12:33:01.438770Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
2026-05-04T12:33:01.446415Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
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
確認します。まず対象 branch と diff 範囲を実測し、その後に変更ファイルを読んで A〜G の観点で findings だけを優先して組み立てます。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git status --short --branch' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'git log roku/phase3f-asset-gate..HEAD --oneline' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-TXyfxEjW' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-AnWAsMGb' (errno=Operation not permitted)
85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
41dbec5 feat(narration): per-segment <Sequence> timeline (Phase 3-H)
7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-qwiBqS0o' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ZslVDBsC' (errno=Operation not permitted)
## roku/phase3h-narration-sequence
?? docs/

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
/bin/zsh -lc 'git diff --name-status roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-BxZNM0VB' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-xP7OvmA5' (errno=Operation not permitted)
M	skills/supermovie-narration/SKILL.md
M	template/scripts/visual_smoke.py
M	template/scripts/voicevox_narration.py
M	template/src/MainVideo.tsx
M	template/src/Narration/NarrationAudio.tsx
M	template/src/Narration/index.ts
A	template/src/Narration/narrationData.ts
A	template/src/Narration/types.ts

codex
verification-gate を併用します。`git log` では対象範囲に Phase 3-F hotfix も含まれていましたが、レビュー主対象は指定どおり直近 2 commit と Phase 3-H diff に絞り、Phase 3-G fix は vstack 変更だけ再確認します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-4CIv9r5q' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-wxklg1BM' (errno=Operation not permitted)
diff --git a/template/scripts/voicevox_narration.py b/template/scripts/voicevox_narration.py
index a226f24..5a1baca 100644
--- a/template/scripts/voicevox_narration.py
+++ b/template/scripts/voicevox_narration.py
@@ -1,19 +1,29 @@
 #!/usr/bin/env python3
-"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
+"""SuperMovie Phase 3-D/H: VOICEVOX で transcript_fixed.json から narration を生成.
 
-Codex Phase 3D design (2026-05-04, CODEX_PHASE3D_VOICEVOX) 推奨:
+Phase 3-D 設計起点 (Codex CODEX_PHASE3D_VOICEVOX, 2026-05-04):
 - engine 不在で skip (--require-engine 指定時のみ exit non-zero)
 - 入力: transcript_fixed.json の segments[] / project-config.json の tone
 - 入力 override: --script narration_script.txt / --script-json narration_script.json
-- 出力: public/narration.wav (segments 個別 wav を結合)
+- 出力: public/narration.wav (segments 個別 wav を結合、legacy fallback)
 - API: POST /audio_query → POST /synthesis (公式 https://github.com/VOICEVOX/voicevox_engine)
 
+Phase 3-H 拡張 (Codex CODEX_PHASE3H_NEXT, 2026-05-04):
+- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
+- 各 chunk の wave header から実 duration を測定
+- src/Narration/narrationData.ts を all-or-nothing で生成
+  (NarrationSegment[] = [{id, startFrame, durationInFrames, file, text}])
+- public/narration/chunk_meta.json も debug 用に出力
+- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
+- partial failure 時は narrationData.ts を空に reset、二重音声防止
+
 Usage:
     python3 scripts/voicevox_narration.py
     python3 scripts/voicevox_narration.py --speaker 3
     python3 scripts/voicevox_narration.py --script narration.txt
     python3 scripts/voicevox_narration.py --list-speakers
     python3 scripts/voicevox_narration.py --require-engine
+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
 
 Engine 起動 (Roku ローカル):
     https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
@@ -33,8 +43,18 @@ from pathlib import Path
 PROJ = Path(__file__).resolve().parent.parent
 ENGINE_BASE = "http://127.0.0.1:50021"
 DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
+DEFAULT_FPS = 30
 TIMEOUT = 30
 
+NARRATION_DIR = PROJ / "public" / "narration"
+NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
+CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
+EMPTY_NARRATION_DATA = (
+    "import type { NarrationSegment } from './types';\n"
+    "\n"
+    "export const narrationData: NarrationSegment[] = [];\n"
+)
+
 
 def load_json(p: Path):
     return json.loads(p.read_text(encoding="utf-8"))
@@ -92,6 +112,109 @@ def concat_wavs(wavs: list[Path], out_path: Path) -> None:
             out.writeframes(f)
 
 
+def measure_duration_seconds(wav_path: Path) -> float:
+    """WAV header の (nframes / framerate) で正確な duration を返す."""
+    with wave.open(str(wav_path), "rb") as w:
+        return w.getnframes() / float(w.getframerate())
+
+
+def cleanup_stale_chunks() -> None:
+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
+    narrationData.ts も空 array に reset する。"""
+    if NARRATION_DIR.exists():
+        for p in NARRATION_DIR.glob("chunk_*.wav"):
+            try:
+                p.unlink()
+            except OSError as e:
+                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
+        if CHUNK_META_JSON.exists():
+            try:
+                CHUNK_META_JSON.unlink()
+            except OSError as e:
+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
+    reset_narration_data_ts()
+
+
+def reset_narration_data_ts() -> None:
+    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
+    if NARRATION_DATA_TS.parent.exists():
+        NARRATION_DATA_TS.write_text(EMPTY_NARRATION_DATA, encoding="utf-8")
+
+
+def read_render_fps(default: int = DEFAULT_FPS) -> int:
+    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
+    cfg_path = PROJ / "project-config.json"
+    if not cfg_path.exists():
+        return default
+    try:
+        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
+    except (json.JSONDecodeError, OSError):
+        return default
+    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
+    if isinstance(fps, (int, float)) and fps > 0:
+        return int(fps)
+    return default
+
+
+def write_narration_data(
+    chunks: list[tuple[Path, str]],
+    fps: int,
+) -> tuple[list[dict], Path, Path]:
+    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
+    segments: list[dict] = []
+    cumulative_frame = 0
+    for i, (path, text) in enumerate(chunks):
+        duration_sec = measure_duration_seconds(path)
+        duration_frames = max(1, round(duration_sec * fps))
+        rel = path.relative_to(PROJ / "public").as_posix()
+        segments.append({
+            "id": i,
+            "startFrame": cumulative_frame,
+            "durationInFrames": duration_frames,
+            "file": rel,
+            "text": text[:100],  # debug 用、長文は切り詰め
+            "duration_sec": round(duration_sec, 3),
+        })
+        cumulative_frame += duration_frames
+
+    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
+    CHUNK_META_JSON.write_text(
+        json.dumps(
+            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
+            ensure_ascii=False,
+            indent=2,
+        ),
+        encoding="utf-8",
+    )
+
+    ts_lines = [
+        "/**",
+        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
+        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
+        " * 手動編集禁止 (script 再実行で上書きされる)。",
+        " */",
+        "import type { NarrationSegment } from './types';",
+        "",
+        "export const narrationData: NarrationSegment[] = [",
+    ]
+    for s in segments:
+        ts_lines.append(
+            "  { "
+            f"id: {s['id']}, "
+            f"startFrame: {s['startFrame']}, "
+            f"durationInFrames: {s['durationInFrames']}, "
+            f"file: {json.dumps(s['file'])}, "
+            f"text: {json.dumps(s['text'], ensure_ascii=False)} "
+            "},"
+        )
+    ts_lines.append("];")
+    ts_lines.append("")
+    NARRATION_DATA_TS.parent.mkdir(parents=True, exist_ok=True)
+    NARRATION_DATA_TS.write_text("\n".join(ts_lines), encoding="utf-8")
+
+    return segments, NARRATION_DATA_TS, CHUNK_META_JSON
+
+
 def _resolve_path(path_str: str) -> Path:
     """非 absolute path は PROJ 相対に解決 (skill 実行時の cwd 揺れを吸収)."""
     p = Path(path_str)
@@ -118,10 +241,16 @@ def main():
     ap.add_argument("--require-engine", action="store_true",
                     help="engine 不在で exit 4 (default は skip exit 0)")
     ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
-    ap.add_argument("--keep-chunks", action="store_true",
-                    help="chunk wav を public/narration/ に保存 (debug 用)")
+    ap.add_argument(
+        "--fps",
+        type=int,
+        default=None,
+        help=f"narrationData.ts に書き込む frame 換算 fps "
+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
+    )
     ap.add_argument("--allow-partial", action="store_true",
-                    help="一部 chunk synthesis 失敗でも narration.wav を出力 (default は全 chunk 成功必須)")
+                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
+                         "(default は全 chunk 成功必須)")
     args = ap.parse_args()
 
     ok, info = check_engine()
@@ -132,8 +261,9 @@ def main():
             return 4
         print(f"INFO: {msg} -> narration generation skipped")
         print(
-            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
-            "getStaticFiles で検出し null を返すため render は失敗しない (Phase 3-F asset gate)"
+            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
+            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
+            "(Phase 3-F asset gate + Phase 3-H per-segment Sequence)"
         )
         return 0
     print(f"VOICEVOX engine OK (version: {info})")
@@ -155,18 +285,25 @@ def main():
         print("ERROR: no narration chunks", file=sys.stderr)
         return 3
 
-    chunks_dir = PROJ / "public" / "narration"
-    chunks_dir.mkdir(parents=True, exist_ok=True)
+    fps = args.fps if args.fps is not None else read_render_fps()
+    print(f"target fps: {fps}")
+
+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
+    cleanup_stale_chunks()
+    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
+
     chunk_paths: list[Path] = []
+    chunk_texts: list[str] = []
     for i, text in enumerate(chunks):
         try:
             wav_bytes = synthesize(text, args.speaker)
         except (urllib.error.HTTPError, urllib.error.URLError) as e:
             print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
             continue
-        p = chunks_dir / f"chunk_{i:03d}.wav"
+        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
         p.write_bytes(wav_bytes)
         chunk_paths.append(p)
+        chunk_texts.append(text)
         print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
 
     if not chunk_paths:
@@ -178,6 +315,13 @@ def main():
             f"(--allow-partial で部分成功でも narration.wav 出力可)",
             file=sys.stderr,
         )
+        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
+        for p in chunk_paths:
+            try:
+                p.unlink()
+            except OSError:
+                pass
+        reset_narration_data_ts()
         return 6
 
     out_path = _resolve_path(args.output)
@@ -186,22 +330,21 @@ def main():
     print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
     print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
 
-    if not args.keep_chunks:
-        for p in chunk_paths:
-            try:
-                p.unlink()
-            except OSError:
-                pass
-        try:
-            chunks_dir.rmdir()
-        except OSError:
-            pass
+    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
+    pairs = list(zip(chunk_paths, chunk_texts))
+    segments, ts_path, meta_path = write_narration_data(pairs, fps)
+    print(f"wrote: {ts_path} ({len(segments)} segments, {sum(s['durationInFrames'] for s in segments)} frames)")
+    print(f"wrote: {meta_path}")
 
     summary = {
         "speaker": args.speaker,
+        "fps": fps,
         "chunks": len(chunk_paths),
         "total_chunks": len(chunks),
-        "output": str(out_path),
+        "total_frames": sum(s["durationInFrames"] for s in segments),
+        "narration_wav": str(out_path),
+        "narration_data_ts": str(ts_path),
+        "chunk_meta_json": str(meta_path),
         "engine_version": info,
     }
     print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")

exec
/bin/zsh -lc 'git diff --stat roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-GBfpk1wn' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-1kZvbhlE' (errno=Operation not permitted)
 skills/supermovie-narration/SKILL.md      |  53 ++++++---
 template/scripts/visual_smoke.py          |  19 ++-
 template/scripts/voicevox_narration.py    | 187 ++++++++++++++++++++++++++----
 template/src/MainVideo.tsx                |  25 ++--
 template/src/Narration/NarrationAudio.tsx |  52 +++++++--
 template/src/Narration/index.ts           |   2 +
 template/src/Narration/narrationData.ts   |   7 ++
 template/src/Narration/types.ts           |  17 +++
 8 files changed, 303 insertions(+), 59 deletions(-)

exec
/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/visual_smoke.py skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-2yudiVke' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-tKPT356H' (errno=Operation not permitted)
diff --git a/template/src/MainVideo.tsx b/template/src/MainVideo.tsx
index 0e3bff3..abd0fa5 100644
--- a/template/src/MainVideo.tsx
+++ b/template/src/MainVideo.tsx
@@ -5,20 +5,31 @@ import { BGM } from './SoundEffects/BGM';
 import { ImageSequence } from './InsertImage';
 import { TitleSequence } from './Title';
 import { SlideSequence } from './Slides';
-import { NarrationAudio } from './Narration';
+import { NarrationAudio, narrationData } from './Narration';
 import { VIDEO_FILE } from './videoConfig';
 
 const NARRATION_FILE = 'narration.wav';
+const NARRATION_CHUNK_PREFIX = 'narration/chunk_';
 
 export const MainVideo: React.FC = () => {
-  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
-  // 不在なら 1.0 で再生 (二重音声防止)。getStaticFiles は Studio/render 時に
+  // Phase 3-F asset gate + Phase 3-H per-segment Sequence と連動:
+  // - legacy: public/narration.wav 存在 → base mute
+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
+  // どちらも不在なら base 元音声 1.0 で再生。getStaticFiles は Studio/render 時に
   // public/ 配下の asset 一覧を返す Remotion 公式 API
   // (https://www.remotion.dev/docs/getstaticfiles)。
-  // 注意: Studio 起動後に narration.wav を生成した場合、Studio をリロード
-  // (Cmd+R / `r` キー) しないと反映されない。新規 asset 追加には watchStaticFile
-  // を使う選択肢もあるが、現状は単純化のため reload 方式を採用。
-  const hasNarration = getStaticFiles().some((f) => f.name === NARRATION_FILE);
+  // 注意: Studio 起動後に narration を生成した場合、Studio リロード
+  // (Cmd+R / `r` キー) で反映する。新規 asset 追加に watchStaticFile を使う選択肢
+  // もあるが、現状は単純化のため reload 方式を採用。
+  const staticFiles = getStaticFiles();
+  const hasLegacyNarration = staticFiles.some((f) => f.name === NARRATION_FILE);
+  const hasChunkNarration =
+    narrationData.length > 0 &&
+    narrationData.every((seg) =>
+      staticFiles.some((f) => f.name === seg.file),
+    ) &&
+    staticFiles.some((f) => f.name.startsWith(NARRATION_CHUNK_PREFIX));
+  const hasNarration = hasLegacyNarration || hasChunkNarration;
   const baseVolume = hasNarration ? 0 : 1.0;
 
   return (
diff --git a/template/src/Narration/NarrationAudio.tsx b/template/src/Narration/NarrationAudio.tsx
index 9a9223c..aa785dc 100644
--- a/template/src/Narration/NarrationAudio.tsx
+++ b/template/src/Narration/NarrationAudio.tsx
@@ -1,28 +1,60 @@
 import React from 'react';
-import { Audio, getStaticFiles, staticFile } from 'remotion';
+import { Audio, Sequence, getStaticFiles, staticFile } from 'remotion';
+import { narrationData } from './narrationData';
 
 interface NarrationAudioProps {
-  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
+  /** legacy 単一ファイル名 (public/ 配下、省略時 'narration.wav') */
   file?: string;
   volume?: number;
 }
 
 /**
- * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
- * Phase 3-F asset gate: public/narration.wav が無い時は null を返して render を
- * 失敗させない (BGM 同パターン)。
+ * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
+ * narrationData.ts を生成する経路)。
  *
- * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
- * 生成された後に自動で再生される。生成されていない時は静かに skip。
+ * 動作優先順位:
+ *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
+ *      → 各 chunk を <Sequence from={startFrame} durationInFrames={...}>
+ *        + <Audio /> でループ再生 (https://www.remotion.dev/docs/sequence)
+ *   2) narrationData が空 + public/narration.wav 存在
+ *      → legacy 単一 wav (Phase 3-D 互換、deterministic test 用)
+ *   3) どちらも不在 → null (asset gate、Phase 3-F 互換)
  *
- * volume はコールバック形式 ((frame) => volume) を使う。Remotion の lint が
- * 静的 number 値の volume を警告するため (https://www.remotion.dev/docs/audio/volume)。
+ * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
+ *
+ * volume はコールバック形式 ((frame) => volume) で Remotion lint 警告を回避
+ * (https://www.remotion.dev/docs/audio/volume)。
  */
 export const NarrationAudio: React.FC<NarrationAudioProps> = ({
   file = 'narration.wav',
   volume = 1.0,
 }) => {
-  const hasFile = getStaticFiles().some((f) => f.name === file);
+  const staticFiles = getStaticFiles();
+
+  if (narrationData.length > 0) {
+    const allChunksExist = narrationData.every((seg) =>
+      staticFiles.some((f) => f.name === seg.file),
+    );
+    if (!allChunksExist) {
+      return null;
+    }
+    return (
+      <>
+        {narrationData.map((seg) => (
+          <Sequence
+            key={seg.id}
+            from={seg.startFrame}
+            durationInFrames={seg.durationInFrames}
+          >
+            <Audio src={staticFile(seg.file)} volume={() => volume} />
+          </Sequence>
+        ))}
+      </>
+    );
+  }
+
+  const hasFile = staticFiles.some((f) => f.name === file);
   if (!hasFile) {
     return null;
   }
diff --git a/template/src/Narration/index.ts b/template/src/Narration/index.ts
index 83a289b..b0fe835 100644
--- a/template/src/Narration/index.ts
+++ b/template/src/Narration/index.ts
@@ -1 +1,3 @@
 export { NarrationAudio } from './NarrationAudio';
+export { narrationData } from './narrationData';
+export type { NarrationSegment } from './types';
diff --git a/template/src/Narration/narrationData.ts b/template/src/Narration/narrationData.ts
new file mode 100644
index 0000000..c56cc33
--- /dev/null
+++ b/template/src/Narration/narrationData.ts
@@ -0,0 +1,7 @@
+/**
+ * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
+ * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
+ */
+import type { NarrationSegment } from './types';
+
+export const narrationData: NarrationSegment[] = [];
diff --git a/template/src/Narration/types.ts b/template/src/Narration/types.ts
new file mode 100644
index 0000000..197da83
--- /dev/null
+++ b/template/src/Narration/types.ts
@@ -0,0 +1,17 @@
+/**
+ * Phase 3-H: per-segment narration timeline 用の型定義。
+ * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
+ * (https://www.remotion.dev/docs/sequence)。
+ */
+export interface NarrationSegment {
+  /** chunk index (0-based、生成順) */
+  id: number;
+  /** timeline 上での開始 frame (前 chunk の累積 duration) */
+  startFrame: number;
+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
+  durationInFrames: number;
+  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
+  file: string;
+  /** debug 用に元 transcript text を保持 (省略可) */
+  text?: string;
+}

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Efofjwv1' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-jrIXtF9L' (errno=Operation not permitted)
diff --git a/skills/supermovie-narration/SKILL.md b/skills/supermovie-narration/SKILL.md
index f79d728..76fb7e8 100644
--- a/skills/supermovie-narration/SKILL.md
+++ b/skills/supermovie-narration/SKILL.md
@@ -49,33 +49,49 @@ Roku が以下のいずれかで起動した後に実行:
 2. `--script-json <path>` で `{segments: [{text}]}` JSON 指定
 3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
 
-## Phase 3: 合成 + 結合
+## Phase 3: 合成 + 結合 (Phase 3-D legacy + Phase 3-H per-segment)
 
 各 chunk について:
 1. `POST /audio_query?text=...&speaker=<id>` → query JSON
 2. `POST /synthesis?speaker=<id>` body=query → WAV bytes
 
-すべての chunk wav を時系列で結合し `public/narration.wav` を生成。
-`--keep-chunks` で chunk 個別 wav も保持 (debug)。
+**Phase 3-D legacy**: chunk wav を時系列で結合し `public/narration.wav` を生成。
+
+**Phase 3-H per-segment** (default、自動):
+- `public/narration/chunk_NNN.wav` を保持 (削除しない)
+- 各 chunk の wave header から実 duration 測定 → frame 換算
+- `src/Narration/narrationData.ts` を all-or-nothing で生成
+  (NarrationSegment[]: id / startFrame / durationInFrames / file / text)
+- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
+- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
+  reset + 部分 chunk を削除 (二重音声 / 中途半端 timeline 防止)
+
+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
+default 30 の優先順位で解決。
+
+stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
 
 ## Phase 4: Remotion 接合 (asset gate、手動操作不要)
 
-Phase 3-F asset gate により `MainVideo.tsx` 編集は不要。
-`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
-`public/narration.wav` の有無を検出する:
+Phase 3-F asset gate + Phase 3-H per-segment Sequence により
+`MainVideo.tsx` 編集は不要。
 
-| narration.wav 状態 | NarrationAudio | base Video volume |
-|--------------------|----------------|-------------------|
-| 不在 | null (skip) | 1.0 (元音声再生) |
-| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
+| 状態 | NarrationAudio | base Video volume |
+|------|----------------|-------------------|
+| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
 
-つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
-次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
-切り替わる。Roku の手作業ゼロ。
+優先順位は narrationData > narration.wav > null。
+`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
+`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
+に切り替わる。Roku の手作業ゼロ。
 
 実装参照:
-- `template/src/MainVideo.tsx` (`hasNarration` 判定 + `baseVolume`)
-- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
+- `template/src/MainVideo.tsx` (`hasLegacyNarration` + `hasChunkNarration` で `baseVolume` 判定)
+- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
+- `template/src/Narration/types.ts` (NarrationSegment 型)
+- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
 
 ## 実行コマンド
 
@@ -97,8 +113,10 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
 
 ## 出力
 
-- `<PROJECT>/public/narration.wav` (本命、結合済)
-- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
+- `<PROJECT>/public/narration.wav` (Phase 3-D legacy、結合済)
+- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
+- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
+- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
 
 ## エラーハンドリング
 
@@ -108,6 +126,7 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
 | transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
 | `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
 | WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |
+| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
 
 ## 連携マップ
 
diff --git a/template/scripts/visual_smoke.py b/template/scripts/visual_smoke.py
index baf5094..32ed199 100644
--- a/template/scripts/visual_smoke.py
+++ b/template/scripts/visual_smoke.py
@@ -135,6 +135,10 @@ def has_drawtext_filter() -> bool:
     return False
 
 
+CELL_W = 480
+CELL_H = 360
+
+
 def make_grid(
     stills: list[Path],
     grid_out: Path,
@@ -148,6 +152,11 @@ def make_grid(
     (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
     label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
     (drawtext filter 不在環境向け、Codex P1 #2 反映)。
+
+    各 cell を CELL_W × CELL_H の固定 box に letterbox (scale + pad) で統一する。
+    youtube/short/square は aspect 比が異なるため、共通 height だけだと row ごとに
+    width が変わり vstack が input width 不一致で reject する (Codex Phase 3-G fix
+    再 review investigation で実証、新規 P1)。
     """
     if not stills:
         return
@@ -159,19 +168,23 @@ def make_grid(
     n_fmt = len(formats)
     n_frm = len(frames)
     filter_parts: list[str] = []
-    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
+    # 各 cell を CELL_W×CELL_H box に letterbox (aspect 維持で fit、余白は黒)
     for i, s in enumerate(stills):
         fmt = formats[i // n_frm]
         frm = frames[i % n_frm]
+        scale_pad = (
+            f"scale={CELL_W}:{CELL_H}:force_original_aspect_ratio=decrease,"
+            f"pad={CELL_W}:{CELL_H}:(ow-iw)/2:(oh-ih)/2:color=black"
+        )
         if label:
             txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
             filter_parts.append(
-                f"[{i}:v]scale=-2:360,"
+                f"[{i}:v]{scale_pad},"
                 f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
                 f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
             )
         else:
-            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
+            filter_parts.append(f"[{i}:v]{scale_pad}[c{i}]")
 
     # 各 format 行の hstack
     row_labels: list[str] = []

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,380p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba template/src/Narration/NarrationAudio.tsx | sed -n '1,140p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import React from 'react';
     2	import { Audio, Sequence, getStaticFiles, staticFile } from 'remotion';
     3	import { narrationData } from './narrationData';
     4	
     5	interface NarrationAudioProps {
     6	  /** legacy 単一ファイル名 (public/ 配下、省略時 'narration.wav') */
     7	  file?: string;
     8	  volume?: number;
     9	}
    10	
    11	/**
    12	 * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
    13	 * narrationData.ts を生成する経路)。
    14	 *
    15	 * 動作優先順位:
    16	 *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
    17	 *      → 各 chunk を <Sequence from={startFrame} durationInFrames={...}>
    18	 *        + <Audio /> でループ再生 (https://www.remotion.dev/docs/sequence)
    19	 *   2) narrationData が空 + public/narration.wav 存在
    20	 *      → legacy 単一 wav (Phase 3-D 互換、deterministic test 用)
    21	 *   3) どちらも不在 → null (asset gate、Phase 3-F 互換)
    22	 *
    23	 * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
    25	 *
    26	 * volume はコールバック形式 ((frame) => volume) で Remotion lint 警告を回避
    27	 * (https://www.remotion.dev/docs/audio/volume)。
    28	 */
    29	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
    30	  file = 'narration.wav',
    31	  volume = 1.0,
    32	}) => {
    33	  const staticFiles = getStaticFiles();
    34	
    35	  if (narrationData.length > 0) {
    36	    const allChunksExist = narrationData.every((seg) =>
    37	      staticFiles.some((f) => f.name === seg.file),
    38	    );
    39	    if (!allChunksExist) {
    40	      return null;
    41	    }
    42	    return (
    43	      <>
    44	        {narrationData.map((seg) => (
    45	          <Sequence
    46	            key={seg.id}
    47	            from={seg.startFrame}
    48	            durationInFrames={seg.durationInFrames}
    49	          >
    50	            <Audio src={staticFile(seg.file)} volume={() => volume} />
    51	          </Sequence>
    52	        ))}
    53	      </>
    54	    );
    55	  }
    56	
    57	  const hasFile = staticFiles.some((f) => f.name === file);
    58	  if (!hasFile) {
    59	    return null;
    60	  }
    61	  return <Audio src={staticFile(file)} volume={() => volume} />;
    62	};

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
    17	- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
    18	- partial failure 時は narrationData.ts を空に reset、二重音声防止
    19	
    20	Usage:
    21	    python3 scripts/voicevox_narration.py
    22	    python3 scripts/voicevox_narration.py --speaker 3
    23	    python3 scripts/voicevox_narration.py --script narration.txt
    24	    python3 scripts/voicevox_narration.py --list-speakers
    25	    python3 scripts/voicevox_narration.py --require-engine
    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
    27	
    28	Engine 起動 (Roku ローカル):
    29	    https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
    30	    127.0.0.1:50021 で REST API が立つ。Docker 版もあり (公式 README 参照)。
    31	"""
    32	from __future__ import annotations
    33	
    34	import argparse
    35	import json
    36	import sys
    37	import urllib.error
    38	import urllib.parse
    39	import urllib.request
    40	import wave
    41	from pathlib import Path
    42	
    43	PROJ = Path(__file__).resolve().parent.parent
    44	ENGINE_BASE = "http://127.0.0.1:50021"
    45	DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
    46	DEFAULT_FPS = 30
    47	TIMEOUT = 30
    48	
    49	NARRATION_DIR = PROJ / "public" / "narration"
    50	NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
    51	CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
    52	EMPTY_NARRATION_DATA = (
    53	    "import type { NarrationSegment } from './types';\n"
    54	    "\n"
    55	    "export const narrationData: NarrationSegment[] = [];\n"
    56	)
    57	
    58	
    59	def load_json(p: Path):
    60	    return json.loads(p.read_text(encoding="utf-8"))
    61	
    62	
    63	def http_request(method: str, path: str, params: dict | None = None,
    64	                 body: dict | None = None) -> bytes:
    65	    url = ENGINE_BASE + path
    66	    if params:
    67	        url += "?" + urllib.parse.urlencode(params)
    68	    data = json.dumps(body).encode("utf-8") if body is not None else None
    69	    headers = {"Content-Type": "application/json"} if body is not None else {}
    70	    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    71	    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
    72	        return resp.read()
    73	
    74	
    75	def check_engine() -> tuple[bool, str | None]:
    76	    try:
    77	        body = http_request("GET", "/version")
    78	        return True, body.decode("utf-8").strip().strip('"')
    79	    except (urllib.error.URLError, OSError, urllib.error.HTTPError) as e:
    80	        return False, str(e)
    81	
    82	
    83	def list_speakers() -> list[dict]:
    84	    body = http_request("GET", "/speakers")
    85	    return json.loads(body.decode("utf-8"))
    86	
    87	
    88	def synthesize(text: str, speaker: int) -> bytes:
    89	    """audio_query → synthesis の二段階で WAV bytes を返す."""
    90	    aq_body = http_request("POST", "/audio_query", params={"text": text, "speaker": speaker}, body={})
    91	    aq = json.loads(aq_body.decode("utf-8"))
    92	    wav_bytes = http_request("POST", "/synthesis", params={"speaker": speaker}, body=aq)
    93	    return wav_bytes
    94	
    95	
    96	def concat_wavs(wavs: list[Path], out_path: Path) -> None:
    97	    """同一 sample rate / channel の wav 列を時系列で結合."""
    98	    if not wavs:
    99	        return
   100	    with wave.open(str(wavs[0]), "rb") as w0:
   101	        params = w0.getparams()
   102	        frames = [w0.readframes(w0.getnframes())]
   103	    for p in wavs[1:]:
   104	        with wave.open(str(p), "rb") as w:
   105	            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (params.framerate, params.nchannels, params.sampwidth):
   106	                print(f"WARN: {p.name} format mismatch、skip", file=sys.stderr)
   107	                continue
   108	            frames.append(w.readframes(w.getnframes()))
   109	    with wave.open(str(out_path), "wb") as out:
   110	        out.setparams(params)
   111	        for f in frames:
   112	            out.writeframes(f)
   113	
   114	
   115	def measure_duration_seconds(wav_path: Path) -> float:
   116	    """WAV header の (nframes / framerate) で正確な duration を返す."""
   117	    with wave.open(str(wav_path), "rb") as w:
   118	        return w.getnframes() / float(w.getframerate())
   119	
   120	
   121	def cleanup_stale_chunks() -> None:
   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
   123	    narrationData.ts も空 array に reset する。"""
   124	    if NARRATION_DIR.exists():
   125	        for p in NARRATION_DIR.glob("chunk_*.wav"):
   126	            try:
   127	                p.unlink()
   128	            except OSError as e:
   129	                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
   130	        if CHUNK_META_JSON.exists():
   131	            try:
   132	                CHUNK_META_JSON.unlink()
   133	            except OSError as e:
   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
   135	    reset_narration_data_ts()
   136	
   137	
   138	def reset_narration_data_ts() -> None:
   139	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
   140	    if NARRATION_DATA_TS.parent.exists():
   141	        NARRATION_DATA_TS.write_text(EMPTY_NARRATION_DATA, encoding="utf-8")
   142	
   143	
   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
   145	    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
   146	    cfg_path = PROJ / "project-config.json"
   147	    if not cfg_path.exists():
   148	        return default
   149	    try:
   150	        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
   151	    except (json.JSONDecodeError, OSError):
   152	        return default
   153	    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
   154	    if isinstance(fps, (int, float)) and fps > 0:
   155	        return int(fps)
   156	    return default
   157	
   158	
   159	def write_narration_data(
   160	    chunks: list[tuple[Path, str]],
   161	    fps: int,
   162	) -> tuple[list[dict], Path, Path]:
   163	    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
   164	    segments: list[dict] = []
   165	    cumulative_frame = 0
   166	    for i, (path, text) in enumerate(chunks):
   167	        duration_sec = measure_duration_seconds(path)
   168	        duration_frames = max(1, round(duration_sec * fps))
   169	        rel = path.relative_to(PROJ / "public").as_posix()
   170	        segments.append({
   171	            "id": i,
   172	            "startFrame": cumulative_frame,
   173	            "durationInFrames": duration_frames,
   174	            "file": rel,
   175	            "text": text[:100],  # debug 用、長文は切り詰め
   176	            "duration_sec": round(duration_sec, 3),
   177	        })
   178	        cumulative_frame += duration_frames
   179	
   180	    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
   181	    CHUNK_META_JSON.write_text(
   182	        json.dumps(
   183	            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
   184	            ensure_ascii=False,
   185	            indent=2,
   186	        ),
   187	        encoding="utf-8",
   188	    )
   189	
   190	    ts_lines = [
   191	        "/**",
   192	        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
   193	        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
   194	        " * 手動編集禁止 (script 再実行で上書きされる)。",
   195	        " */",
   196	        "import type { NarrationSegment } from './types';",
   197	        "",
   198	        "export const narrationData: NarrationSegment[] = [",
   199	    ]
   200	    for s in segments:
   201	        ts_lines.append(
   202	            "  { "
   203	            f"id: {s['id']}, "
   204	            f"startFrame: {s['startFrame']}, "
   205	            f"durationInFrames: {s['durationInFrames']}, "
   206	            f"file: {json.dumps(s['file'])}, "
   207	            f"text: {json.dumps(s['text'], ensure_ascii=False)} "
   208	            "},"
   209	        )
   210	    ts_lines.append("];")
   211	    ts_lines.append("")
   212	    NARRATION_DATA_TS.parent.mkdir(parents=True, exist_ok=True)
   213	    NARRATION_DATA_TS.write_text("\n".join(ts_lines), encoding="utf-8")
   214	
   215	    return segments, NARRATION_DATA_TS, CHUNK_META_JSON
   216	
   217	
   218	def _resolve_path(path_str: str) -> Path:
   219	    """非 absolute path は PROJ 相対に解決 (skill 実行時の cwd 揺れを吸収)."""
   220	    p = Path(path_str)
   221	    return p if p.is_absolute() else PROJ / p
   222	
   223	
   224	def collect_chunks(args, transcript: dict) -> list[str]:
   225	    if args.script:
   226	        text = _resolve_path(args.script).read_text(encoding="utf-8")
   227	        return [line.strip() for line in text.splitlines() if line.strip()]
   228	    if args.script_json:
   229	        plan = load_json(_resolve_path(args.script_json))
   230	        return [s.get("text", "").strip() for s in plan.get("segments", []) if s.get("text", "").strip()]
   231	    return [s.get("text", "").strip() for s in transcript.get("segments", []) if s.get("text", "").strip()]
   232	
   233	
   234	def main():
   235	    ap = argparse.ArgumentParser()
   236	    ap.add_argument("--speaker", type=int, default=DEFAULT_SPEAKER,
   237	                    help=f"VOICEVOX speaker id (default {DEFAULT_SPEAKER}=ずんだもんノーマル)")
   238	    ap.add_argument("--script", help="custom plain-text narration (1 line = 1 chunk)")
   239	    ap.add_argument("--script-json", help="custom JSON {segments:[{text}]} narration")
   240	    ap.add_argument("--list-speakers", action="store_true")
   241	    ap.add_argument("--require-engine", action="store_true",
   242	                    help="engine 不在で exit 4 (default は skip exit 0)")
   243	    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
   244	    ap.add_argument(
   245	        "--fps",
   246	        type=int,
   247	        default=None,
   248	        help=f"narrationData.ts に書き込む frame 換算 fps "
   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
   250	    )
   251	    ap.add_argument("--allow-partial", action="store_true",
   252	                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
   253	                         "(default は全 chunk 成功必須)")
   254	    args = ap.parse_args()
   255	
   256	    ok, info = check_engine()
   257	    if not ok:
   258	        msg = f"VOICEVOX engine unavailable at {ENGINE_BASE}: {info}"
   259	        if args.require_engine:
   260	            print(f"ERROR: {msg}", file=sys.stderr)
   261	            return 4
   262	        print(f"INFO: {msg} -> narration generation skipped")
   263	        print(
   264	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
   265	            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
   266	            "(Phase 3-F asset gate + Phase 3-H per-segment Sequence)"
   267	        )
   268	        return 0
   269	    print(f"VOICEVOX engine OK (version: {info})")
   270	
   271	    if args.list_speakers:
   272	        speakers = list_speakers()
   273	        for s in speakers:
   274	            for style in s.get("styles", []):
   275	                print(f"  [{style.get('id'):3}] {s.get('name')} / {style.get('name')}")
   276	        return 0
   277	
   278	    transcript_path = PROJ / "transcript_fixed.json"
   279	    if not transcript_path.exists() and not (args.script or args.script_json):
   280	        print(f"ERROR: transcript_fixed.json missing under {PROJ}", file=sys.stderr)
   281	        return 3
   282	    transcript = load_json(transcript_path) if transcript_path.exists() else {}
   283	    chunks = collect_chunks(args, transcript)
   284	    if not chunks:
   285	        print("ERROR: no narration chunks", file=sys.stderr)
   286	        return 3
   287	
   288	    fps = args.fps if args.fps is not None else read_render_fps()
   289	    print(f"target fps: {fps}")
   290	
   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
   292	    cleanup_stale_chunks()
   293	    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
   294	
   295	    chunk_paths: list[Path] = []
   296	    chunk_texts: list[str] = []
   297	    for i, text in enumerate(chunks):
   298	        try:
   299	            wav_bytes = synthesize(text, args.speaker)
   300	        except (urllib.error.HTTPError, urllib.error.URLError) as e:
   301	            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
   302	            continue
   303	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
   304	        p.write_bytes(wav_bytes)
   305	        chunk_paths.append(p)
   306	        chunk_texts.append(text)
   307	        print(f"  chunk[{i:3}] {len(wav_bytes)} bytes  text='{text[:30]}…'")
   308	
   309	    if not chunk_paths:
   310	        print("ERROR: no chunks succeeded", file=sys.stderr)
   311	        return 5
   312	    if not args.allow_partial and len(chunk_paths) < len(chunks):
   313	        print(
   314	            f"ERROR: only {len(chunk_paths)}/{len(chunks)} chunks succeeded "
   315	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
   316	            file=sys.stderr,
   317	        )
   318	        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
   319	        for p in chunk_paths:
   320	            try:
   321	                p.unlink()
   322	            except OSError:
   323	                pass
   324	        reset_narration_data_ts()
   325	        return 6
   326	
   327	    out_path = _resolve_path(args.output)
   328	    out_path.parent.mkdir(parents=True, exist_ok=True)
   329	    concat_wavs(chunk_paths, out_path)
   330	    print(f"\nwrote: {out_path} ({out_path.stat().st_size} bytes)")
   331	    print(f"chunks succeeded: {len(chunk_paths)} / {len(chunks)} synthesized")
   332	
   333	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
   334	    pairs = list(zip(chunk_paths, chunk_texts))
   335	    segments, ts_path, meta_path = write_narration_data(pairs, fps)
   336	    print(f"wrote: {ts_path} ({len(segments)} segments, {sum(s['durationInFrames'] for s in segments)} frames)")
   337	    print(f"wrote: {meta_path}")
   338	
   339	    summary = {
   340	        "speaker": args.speaker,
   341	        "fps": fps,
   342	        "chunks": len(chunk_paths),
   343	        "total_chunks": len(chunks),
   344	        "total_frames": sum(s["durationInFrames"] for s in segments),
   345	        "narration_wav": str(out_path),
   346	        "narration_data_ts": str(ts_path),
   347	        "chunk_meta_json": str(meta_path),
   348	        "engine_version": info,
   349	    }
   350	    print(f"\nsummary: {json.dumps(summary, ensure_ascii=False)}")
   351	    return 0
   352	
   353	
   354	if __name__ == "__main__":
   355	    sys.exit(main())

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/src/MainVideo.tsx | sed -n '1,140p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '120,240p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
     2	import { TelopPlayer } from './テロップテンプレート';
     3	import { SESequence } from './SoundEffects/SESequence';
     4	import { BGM } from './SoundEffects/BGM';
     5	import { ImageSequence } from './InsertImage';
     6	import { TitleSequence } from './Title';
     7	import { SlideSequence } from './Slides';
     8	import { NarrationAudio, narrationData } from './Narration';
     9	import { VIDEO_FILE } from './videoConfig';
    10	
    11	const NARRATION_FILE = 'narration.wav';
    12	const NARRATION_CHUNK_PREFIX = 'narration/chunk_';
    13	
    14	export const MainVideo: React.FC = () => {
    15	  // Phase 3-F asset gate + Phase 3-H per-segment Sequence と連動:
    16	  // - legacy: public/narration.wav 存在 → base mute
    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
    18	  // どちらも不在なら base 元音声 1.0 で再生。getStaticFiles は Studio/render 時に
    19	  // public/ 配下の asset 一覧を返す Remotion 公式 API
    20	  // (https://www.remotion.dev/docs/getstaticfiles)。
    21	  // 注意: Studio 起動後に narration を生成した場合、Studio リロード
    22	  // (Cmd+R / `r` キー) で反映する。新規 asset 追加に watchStaticFile を使う選択肢
    23	  // もあるが、現状は単純化のため reload 方式を採用。
    24	  const staticFiles = getStaticFiles();
    25	  const hasLegacyNarration = staticFiles.some((f) => f.name === NARRATION_FILE);
    26	  const hasChunkNarration =
    27	    narrationData.length > 0 &&
    28	    narrationData.every((seg) =>
    29	      staticFiles.some((f) => f.name === seg.file),
    30	    ) &&
    31	    staticFiles.some((f) => f.name.startsWith(NARRATION_CHUNK_PREFIX));
    32	  const hasNarration = hasLegacyNarration || hasChunkNarration;
    33	  const baseVolume = hasNarration ? 0 : 1.0;
    34	
    35	  return (
    36	    <AbsoluteFill style={{ backgroundColor: 'black' }}>
    37	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
    38	      <Video
    39	        src={staticFile(VIDEO_FILE)}
    40	        volume={() => baseVolume}
    41	        style={{
    42	          width: '100%',
    43	          height: '100%',
    44	          objectFit: 'contain',
    45	        }}
    46	      />
    47	
    48	      {/* スライド (Phase 3-A、別レイヤーで動画の上に被せる) */}
    49	      <SlideSequence />
    50	
    51	      {/* 挿入画像 */}
    52	      <ImageSequence />
    53	
    54	      {/* テロップ */}
    55	      <TelopPlayer />
    56	
    57	      {/* タイトル */}
    58	      <TitleSequence />
    59	
    60	      {/* ナレーション (Phase 3-F asset gate、narration.wav 不在で null) */}
    61	      <NarrationAudio volume={1.0} />
    62	
    63	      {/* BGM (Phase 3-F asset gate、bgm.mp3 不在で null) */}
    64	      <BGM volume={0.08} />
    65	
    66	      {/* 効果音 */}
    67	      <SESequence />
    68	    </AbsoluteFill>
    69	  );
    70	};

 succeeded in 0ms:
   120	def has_drawtext_filter() -> bool:
   121	    """ffmpeg build に drawtext filter (libfreetype) が含まれるか確認。
   122	
   123	    Mac Homebrew 標準 build は drawtext を持つが、minimal build では落ちている
   124	    ことがあるため事前検査する (Codex Phase 3-G review P1 #2 反映)。
   125	    """
   126	    try:
   127	        out = subprocess.check_output(
   128	            ["ffmpeg", "-hide_banner", "-filters"], text=True, stderr=subprocess.STDOUT
   129	        )
   130	    except (subprocess.CalledProcessError, FileNotFoundError):
   131	        return False
   132	    for line in out.splitlines():
   133	        if " drawtext " in f" {line} ":
   134	            return True
   135	    return False
   136	
   137	
   138	CELL_W = 480
   139	CELL_H = 360
   140	
   141	
   142	def make_grid(
   143	    stills: list[Path],
   144	    grid_out: Path,
   145	    formats: list[str],
   146	    frames: list[int],
   147	    label: bool,
   148	) -> None:
   149	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
   150	
   151	    呼び出し側で full matrix (len(stills) == n_fmt * n_frm) を保証すること
   152	    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
   153	    label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
   154	    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
   155	
   156	    各 cell を CELL_W × CELL_H の固定 box に letterbox (scale + pad) で統一する。
   157	    youtube/short/square は aspect 比が異なるため、共通 height だけだと row ごとに
   158	    width が変わり vstack が input width 不一致で reject する (Codex Phase 3-G fix
   159	    再 review investigation で実証、新規 P1)。
   160	    """
   161	    if not stills:
   162	        return
   163	    grid_out.parent.mkdir(parents=True, exist_ok=True)
   164	    inputs: list[str] = []
   165	    for s in stills:
   166	        inputs.extend(["-i", str(s)])
   167	
   168	    n_fmt = len(formats)
   169	    n_frm = len(frames)
   170	    filter_parts: list[str] = []
   171	    # 各 cell を CELL_W×CELL_H box に letterbox (aspect 維持で fit、余白は黒)
   172	    for i, s in enumerate(stills):
   173	        fmt = formats[i // n_frm]
   174	        frm = frames[i % n_frm]
   175	        scale_pad = (
   176	            f"scale={CELL_W}:{CELL_H}:force_original_aspect_ratio=decrease,"
   177	            f"pad={CELL_W}:{CELL_H}:(ow-iw)/2:(oh-ih)/2:color=black"
   178	        )
   179	        if label:
   180	            txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
   181	            filter_parts.append(
   182	                f"[{i}:v]{scale_pad},"
   183	                f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
   184	                f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
   185	            )
   186	        else:
   187	            filter_parts.append(f"[{i}:v]{scale_pad}[c{i}]")
   188	
   189	    # 各 format 行の hstack
   190	    row_labels: list[str] = []
   191	    for r in range(n_fmt):
   192	        row_in = "".join(f"[c{r * n_frm + c}]" for c in range(n_frm))
   193	        row_label = f"row{r}"
   194	        if n_frm == 1:
   195	            filter_parts.append(f"{row_in}copy[{row_label}]")
   196	        else:
   197	            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
   198	        row_labels.append(f"[{row_label}]")
   199	
   200	    # vstack
   201	    if n_fmt == 1:
   202	        filter_parts.append(f"{row_labels[0]}copy[grid]")
   203	    else:
   204	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
   205	
   206	    cmd = (
   207	        ["ffmpeg", "-y"]
   208	        + inputs
   209	        + [
   210	            "-filter_complex",
   211	            ";".join(filter_parts),
   212	            "-map",
   213	            "[grid]",
   214	            "-frames:v",
   215	            "1",
   216	            str(grid_out),
   217	        ]
   218	    )
   219	    subprocess.check_call(cmd)
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

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/src/Narration/types.ts template/src/Narration/narrationData.ts template/src/Narration/index.ts' in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
usage: nl [-p] [-b type] [-d delim] [-f type] [-h type] [-i incr] [-l num]
          [-n format] [-s sep] [-v startnum] [-w width] [file]

exec
/bin/zsh -lc "nl -ba skills/supermovie-narration/SKILL.md | sed -n '1,180p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
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
   129	| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
   130	
   131	## 連携マップ
   132	
   133	```
   134	/supermovie-init / transcribe / transcript-fix / cut / subtitles / slides
   135	    ↓ transcript_fixed.json
   136	/supermovie-narration         ← ★ここ: VOICEVOX で narration.wav 生成
   137	    ↓ public/narration.wav
   138	MainVideo.tsx が public/narration.wav を自動検出 (asset gate)
   139	    └ NarrationAudio: <Audio src=narration.wav /> マウント
   140	    └ base Video: volume=0 に切替 (二重音声防止)
   141	    ↓
   142	npm run render
   143	```
   144	
   145	**Studio を開いたまま narration.wav を生成した場合は再読み込み推奨**:
   146	`getStaticFiles()` は Studio 起動時の asset リストをキャッシュするため、
   147	新規ファイルは Studio reload (Cmd+R / `r` キー) で反映される
   148	(出典 https://www.remotion.dev/docs/getstaticfiles)。
   149	
   150	## VOICEVOX 利用規約
   151	
   152	- 商用/非商用利用可、音声ライブラリごとにクレジット表記必須 (https://voicevox.hiroshiba.jp/term/)
   153	- 話者選定 + クレジット明記は Roku 判断領域

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg --files -g 'package.json' -g 'tsconfig*.json' -g '*eslint*' -g '*prettier*' -g 'pyproject.toml' -g 'ruff.toml' -g 'project-config.json' -g 'CLAUDE.md' -g 'AGENTS.md'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
CLAUDE.md
template/eslint.config.mjs
template/tsconfig.json
template/.prettierrc
template/package.json

exec
/bin/zsh -lc 'rg -n "keep-chunks|allow-partial|narrationData|chunk_meta|chunk_.*wav|concat_wavs|voicevox_narration|NarrationAudio|render_fps|fps" .' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
./CLAUDE.md:99:    "fps": {
./CLAUDE.md:102:      "render_fps": 60,
./skills/supermovie-narration/SKILL.md:5:  Remotion の <NarrationAudio /> layer で再生するスキル。
./skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./skills/supermovie-narration/SKILL.md:61:- `public/narration/chunk_NNN.wav` を保持 (削除しない)
./skills/supermovie-narration/SKILL.md:63:- `src/Narration/narrationData.ts` を all-or-nothing で生成
./skills/supermovie-narration/SKILL.md:65:- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
./skills/supermovie-narration/SKILL.md:66:- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
./skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
./skills/supermovie-narration/SKILL.md:79:| 状態 | NarrationAudio | base Video volume |
./skills/supermovie-narration/SKILL.md:81:| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
./skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
./skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
./skills/supermovie-narration/SKILL.md:85:優先順位は narrationData > narration.wav > null。
./skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
./skills/supermovie-narration/SKILL.md:92:- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
./skills/supermovie-narration/SKILL.md:94:- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
./skills/supermovie-narration/SKILL.md:100:python3 <PROJECT>/scripts/voicevox_narration.py
./skills/supermovie-narration/SKILL.md:103:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./skills/supermovie-narration/SKILL.md:104:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./skills/supermovie-narration/SKILL.md:107:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./skills/supermovie-narration/SKILL.md:108:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./skills/supermovie-narration/SKILL.md:111:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./skills/supermovie-narration/SKILL.md:117:- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
./skills/supermovie-narration/SKILL.md:118:- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
./skills/supermovie-narration/SKILL.md:119:- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
./skills/supermovie-narration/SKILL.md:129:| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
./skills/supermovie-narration/SKILL.md:139:    └ NarrationAudio: <Audio src=narration.wav /> マウント
./skills/supermovie-init/SKILL.md:130:- `fps.r_frame_rate` / `fps.avg_frame_rate` / `fps.vfr_metadata_suspect`
./skills/supermovie-init/SKILL.md:145:| VFR (可変 fps) | `r_frame_rate` ≠ `avg_frame_rate` (誤差 > 0.5%) | frame 換算で時間ずれ | render 前に CFR 化 (ffmpeg `-r`) を別タスクで |
./skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
./skills/supermovie-init/SKILL.md:246:🎬 動画: <duration>秒 / <fps>fps / <frames>フレーム
./skills/supermovie-telop-creator/SKILL.md:262:  fps: 30,
./skills/supermovie-telop-creator/SKILL.md:287:  fps={30}
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:23:A) voicevox_narration.py 構造変化
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:27:   - read_render_fps の type 検証 (cfg["source"] が None の時の AttributeError)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:29:   - --keep-chunks 撤去で既存使用者影響範囲 (skill 内文書 / 他 script の引数)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:30:   - chunk_meta.json schema (fps/total_frames/segments[]) と narrationData.ts duplication
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:32:B) NarrationAudio.tsx の三段 fallback
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:33:   - narrationData non-empty + 一部 chunk 不在ケースで null 返り、render 全体が止まらないか
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:38:   - hasChunkNarration 三条件 AND の論理過剰 (narrationData.length > 0 だけで実質判定済みでは?)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:39:   - startsWith("narration/chunk_") の prefix collision (例: narration/chunk_meta.json は wav じゃないのに引っ掛かる)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:41:D) types.ts / narrationData.ts placeholder
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:50:   - エラーハンドリング table の exit 6 行が他コマンド (--allow-partial) と矛盾しないか
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:54:   - Phase 3-D (concat_wavs) と Phase 3-H (per-segment) の二重出力で disk 容量倍化、cleanup 戦略
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:208:M	template/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:210:M	template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:212:A	template/src/Narration/narrationData.ts
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:226:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:232:diff --git a/template/scripts/voicevox_narration.py b/template/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:234:--- a/template/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:235:+++ b/template/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:251:+- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:253:+- src/Narration/narrationData.ts を all-or-nothing で生成
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:255:+- public/narration/chunk_meta.json も debug 用に出力
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:257:+- partial failure 時は narrationData.ts を空に reset、二重音声防止
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:260:     python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:261:     python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:262:     python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:263:     python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:264:     python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:277:+NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:278:+CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:282:+    "export const narrationData: NarrationSegment[] = [];\n"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:288:@@ -92,6 +112,109 @@ def concat_wavs(wavs: list[Path], out_path: Path) -> None:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:300:+    narrationData.ts も空 array に reset する。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:302:+        for p in NARRATION_DIR.glob("chunk_*.wav"):
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:316:+    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:322:+    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:330:+    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:331:+    if isinstance(fps, (int, float)) and fps > 0:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:332:+        return int(fps)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:338:+    fps: int,
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:340:+    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:345:+        duration_frames = max(1, round(duration_sec * fps))
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:360:+            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:369:+        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:370:+        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:375:+        "export const narrationData: NarrationSegment[] = [",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:402:-    ap.add_argument("--keep-chunks", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:405:+        "--fps",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:408:+        help=f"narrationData.ts に書き込む frame 換算 fps "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:411:     ap.add_argument("--allow-partial", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:413:+                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:422:-            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:424:+            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:425:+            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:436:+    fps = args.fps if args.fps is not None else read_render_fps()
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:437:+    print(f"target fps: {fps}")
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:451:-        p = chunks_dir / f"chunk_{i:03d}.wav"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:452:+        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:460:             f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:463:+        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:487:+    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:489:+    segments, ts_path, meta_path = write_narration_data(pairs, fps)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:495:+        "fps": fps,
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:502:+        "chunk_meta_json": str(meta_path),
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:516: template/scripts/voicevox_narration.py    | 187 ++++++++++++++++++++++++++----
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:518: template/src/Narration/NarrationAudio.tsx |  52 +++++++--
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:520: template/src/Narration/narrationData.ts   |   7 ++
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:525:/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD -- template/src/Narration/NarrationAudio.tsx template/src/MainVideo.tsx template/src/Narration/index.ts template/src/Narration/narrationData.ts template/src/Narration/types.ts' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:541:-import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:542:+import { NarrationAudio, narrationData } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:567:+    narrationData.length > 0 &&
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:568:+    narrationData.every((seg) =>
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:576:diff --git a/template/src/Narration/NarrationAudio.tsx b/template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:578:--- a/template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:579:+++ b/template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:584:+import { narrationData } from './narrationData';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:586: interface NarrationAudioProps {
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:597:+ * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:598:+ * narrationData.ts を生成する経路)。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:600:- * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:603:+ *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:606:+ *   2) narrationData が空 + public/narration.wav 存在
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:618: export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:625:+  if (narrationData.length > 0) {
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:626:+    const allChunksExist = narrationData.every((seg) =>
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:634:+        {narrationData.map((seg) => (
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:656: export { NarrationAudio } from './NarrationAudio';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:657:+export { narrationData } from './narrationData';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:659:diff --git a/template/src/Narration/narrationData.ts b/template/src/Narration/narrationData.ts
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:663:+++ b/template/src/Narration/narrationData.ts
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:666:+ * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:667:+ * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:671:+export const narrationData: NarrationSegment[] = [];
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:680:+ * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:690:+  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:717:-`--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:721:+- `public/narration/chunk_NNN.wav` を保持 (削除しない)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:723:+- `src/Narration/narrationData.ts` を all-or-nothing で生成
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:725:+- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:726:+- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:737:-`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:742:-| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:746:+| 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:748:+| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:752:-つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:755:+優先順位は narrationData > narration.wav > null。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:756:+`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:762:-- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:764:+- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:766:+- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:770:@@ -97,8 +113,10 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:775:-- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:777:+- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:778:+- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:779:+- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:783:@@ -108,6 +126,7 @@ python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:787:+| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:851:/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,380p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:853:/bin/zsh -lc "nl -ba template/src/Narration/NarrationAudio.tsx | sed -n '1,140p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:857:     3	import { narrationData } from './narrationData';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:859:     5	interface NarrationAudioProps {
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:866:    12	 * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:867:    13	 * narrationData.ts を生成する経路)。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:870:    16	 *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:873:    19	 *   2) narrationData が空 + public/narration.wav 存在
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:883:    29	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:889:    35	  if (narrationData.length > 0) {
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:890:    36	    const allChunksExist = narrationData.every((seg) =>
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:898:    44	        {narrationData.map((seg) => (
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:930:    12	- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:932:    14	- src/Narration/narrationData.ts を all-or-nothing で生成
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:934:    16	- public/narration/chunk_meta.json も debug 用に出力
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:936:    18	- partial failure 時は narrationData.ts を空に reset、二重音声防止
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:939:    21	    python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:940:    22	    python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:941:    23	    python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:942:    24	    python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:943:    25	    python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:968:    50	NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:969:    51	CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:973:    55	    "export const narrationData: NarrationSegment[] = [];\n"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1014:    96	def concat_wavs(wavs: list[Path], out_path: Path) -> None:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1041:   123	    narrationData.ts も空 array に reset する。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1043:   125	        for p in NARRATION_DIR.glob("chunk_*.wav"):
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1057:   139	    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1063:   145	    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1071:   153	    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1072:   154	    if isinstance(fps, (int, float)) and fps > 0:
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1073:   155	        return int(fps)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1079:   161	    fps: int,
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1081:   163	    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1086:   168	        duration_frames = max(1, round(duration_sec * fps))
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1101:   183	            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1110:   192	        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1111:   193	        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1116:   198	        "export const narrationData: NarrationSegment[] = [",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1163:   245	        "--fps",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1166:   248	        help=f"narrationData.ts に書き込む frame 換算 fps "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1169:   251	    ap.add_argument("--allow-partial", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1170:   252	                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1182:   264	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1183:   265	            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1206:   288	    fps = args.fps if args.fps is not None else read_render_fps()
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1207:   289	    print(f"target fps: {fps}")
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1221:   303	        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1233:   315	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1236:   318	        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1247:   329	    concat_wavs(chunk_paths, out_path)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1251:   333	    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1253:   335	    segments, ts_path, meta_path = write_narration_data(pairs, fps)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1259:   341	        "fps": fps,
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1265:   347	        "chunk_meta_json": str(meta_path),
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1291:     8	import { NarrationAudio, narrationData } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1310:    27	    narrationData.length > 0 &&
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1311:    28	    narrationData.every((seg) =>
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1344:    61	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1483:/bin/zsh -lc 'nl -ba template/src/Narration/types.ts template/src/Narration/narrationData.ts template/src/Narration/index.ts' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1495:     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1533:    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1551:    61	- `public/narration/chunk_NNN.wav` を保持 (削除しない)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1553:    63	- `src/Narration/narrationData.ts` を all-or-nothing で生成
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1555:    65	- `public/narration/chunk_meta.json` に fps + total_frames + segments[] を debug 出力
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1556:    66	- partial failure (途中 chunk synthesis 失敗) 時は `narrationData.ts` を空 array に
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1569:    79	| 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1571:    81	| narrationData 空 + narration.wav 不在 | null (skip) | 1.0 (元音声再生) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1575:    85	優先順位は narrationData > narration.wav > null。
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1576:    86	`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1582:    92	- `template/src/Narration/NarrationAudio.tsx` (narrationData / legacy / null の三経路 fallback)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1584:    94	- `template/src/Narration/narrationData.ts` (script が all-or-nothing で書換)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1590:   100	python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1593:   103	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1594:   104	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1597:   107	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1598:   108	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1601:   111	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1607:   117	- `<PROJECT>/public/narration/chunk_NNN.wav` (Phase 3-H、render 時に必要、常時保持)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1608:   118	- `<PROJECT>/public/narration/chunk_meta.json` (debug、fps + segments[])
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1609:   119	- `<PROJECT>/src/Narration/narrationData.ts` (Phase 3-H render 駆動データ)
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1619:   129	| partial chunk failure (--allow-partial なし) | exit 6、部分 chunk 削除 + narrationData.ts を空 array に reset |
./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1629:   139	    └ NarrationAudio: <Audio src=narration.wav /> マウント
./template/src/ネガティブテロップ/紫文字白背景.tsx:20:  fps: number;
./template/src/強調テロップ/白赤テロップver2.tsx:20:  fps: number;
./template/src/強調テロップ/白赤テロップ.tsx:20:  fps: number;
./template/scripts/voicevox_narration.py:12:- chunk_NNN.wav を public/narration/ に保持 (削除しない、render 時に必要)
./template/scripts/voicevox_narration.py:14:- src/Narration/narrationData.ts を all-or-nothing で生成
./template/scripts/voicevox_narration.py:16:- public/narration/chunk_meta.json も debug 用に出力
./template/scripts/voicevox_narration.py:18:- partial failure 時は narrationData.ts を空に reset、二重音声防止
./template/scripts/voicevox_narration.py:21:    python3 scripts/voicevox_narration.py
./template/scripts/voicevox_narration.py:22:    python3 scripts/voicevox_narration.py --speaker 3
./template/scripts/voicevox_narration.py:23:    python3 scripts/voicevox_narration.py --script narration.txt
./template/scripts/voicevox_narration.py:24:    python3 scripts/voicevox_narration.py --list-speakers
./template/scripts/voicevox_narration.py:25:    python3 scripts/voicevox_narration.py --require-engine
./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
./template/scripts/voicevox_narration.py:50:NARRATION_DATA_TS = PROJ / "src" / "Narration" / "narrationData.ts"
./template/scripts/voicevox_narration.py:51:CHUNK_META_JSON = NARRATION_DIR / "chunk_meta.json"
./template/scripts/voicevox_narration.py:55:    "export const narrationData: NarrationSegment[] = [];\n"
./template/scripts/voicevox_narration.py:96:def concat_wavs(wavs: list[Path], out_path: Path) -> None:
./template/scripts/voicevox_narration.py:122:    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
./template/scripts/voicevox_narration.py:123:    narrationData.ts も空 array に reset する。"""
./template/scripts/voicevox_narration.py:125:        for p in NARRATION_DIR.glob("chunk_*.wav"):
./template/scripts/voicevox_narration.py:134:                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
./template/scripts/voicevox_narration.py:139:    """narrationData.ts を空 array に戻す (Phase 3-H all-or-nothing)。"""
./template/scripts/voicevox_narration.py:144:def read_render_fps(default: int = DEFAULT_FPS) -> int:
./template/scripts/voicevox_narration.py:145:    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
./template/scripts/voicevox_narration.py:153:    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
./template/scripts/voicevox_narration.py:154:    if isinstance(fps, (int, float)) and fps > 0:
./template/scripts/voicevox_narration.py:155:        return int(fps)
./template/scripts/voicevox_narration.py:161:    fps: int,
./template/scripts/voicevox_narration.py:163:    """各 chunk の duration を測って narrationData.ts と chunk_meta.json を書く."""
./template/scripts/voicevox_narration.py:168:        duration_frames = max(1, round(duration_sec * fps))
./template/scripts/voicevox_narration.py:183:            {"fps": fps, "total_frames": cumulative_frame, "segments": segments},
./template/scripts/voicevox_narration.py:192:        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
./template/scripts/voicevox_narration.py:193:        " * NarrationAudio.tsx が <Sequence from={startFrame} durationInFrames={...}> でループ再生する。",
./template/scripts/voicevox_narration.py:198:        "export const narrationData: NarrationSegment[] = [",
./template/scripts/voicevox_narration.py:245:        "--fps",
./template/scripts/voicevox_narration.py:248:        help=f"narrationData.ts に書き込む frame 換算 fps "
./template/scripts/voicevox_narration.py:249:             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
./template/scripts/voicevox_narration.py:251:    ap.add_argument("--allow-partial", action="store_true",
./template/scripts/voicevox_narration.py:252:                    help="一部 chunk synthesis 失敗でも narration.wav を出力 + narrationData.ts 部分書き出し "
./template/scripts/voicevox_narration.py:264:            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在 + "
./template/scripts/voicevox_narration.py:265:            "narrationData.ts 空を asset gate で検出し null を返すため render は失敗しない "
./template/scripts/voicevox_narration.py:288:    fps = args.fps if args.fps is not None else read_render_fps()
./template/scripts/voicevox_narration.py:289:    print(f"target fps: {fps}")
./template/scripts/voicevox_narration.py:291:    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
./template/scripts/voicevox_narration.py:303:        p = NARRATION_DIR / f"chunk_{i:03d}.wav"
./template/scripts/voicevox_narration.py:315:            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./template/scripts/voicevox_narration.py:318:        # Phase 3-H all-or-nothing: 部分書き出した chunk を削除し narrationData も空に戻す
./template/scripts/voicevox_narration.py:329:    concat_wavs(chunk_paths, out_path)
./template/scripts/voicevox_narration.py:333:    # Phase 3-H: chunk metadata + narrationData.ts (atomic、最後に書く)
./template/scripts/voicevox_narration.py:335:    segments, ts_path, meta_path = write_narration_data(pairs, fps)
./template/scripts/voicevox_narration.py:341:        "fps": fps,
./template/scripts/voicevox_narration.py:347:        "chunk_meta_json": str(meta_path),
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:29:   - voicevox_narration.py の chunk wav 結合を per-chunk start/duration に変換
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:30:   - NarrationAudio.tsx を <Sequence from=... duration=...> ループ実装
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:31:   - chunk_meta.json (start_ms / duration_ms) を public/narration/ に書き出し
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:478:template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:484:template/scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:502:/bin/zsh -lc "nl -ba template/src/Narration/NarrationAudio.tsx | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:507:     4	interface NarrationAudioProps {
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:518:    15	 * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:524:    21	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:566:    29	   - voicevox_narration.py の chunk wav 結合を per-chunk start/duration に変換
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:567:    30	   - NarrationAudio.tsx を <Sequence from=... duration=...> ループ実装
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:568:    31	   - chunk_meta.json (start_ms / duration_ms) を public/narration/ に書き出し
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:793:     8	import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:831:    46	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:843:/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,260p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:856:    12	    python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:857:    13	    python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:858:    14	    python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:859:    15	    python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:860:    16	    python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:920:    76	def concat_wavs(wavs: list[Path], out_path: Path) -> None:
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:965:   121	    ap.add_argument("--keep-chunks", action="store_true",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:967:   123	    ap.add_argument("--allow-partial", action="store_true",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:979:   135	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1011:   167	        p = chunks_dir / f"chunk_{i:03d}.wav"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1022:   178	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1029:   185	    concat_wavs(chunk_paths, out_path)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1347:   478	template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1353:   484	template/scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1371:   502	/bin/zsh -lc "nl -ba template/src/Narration/NarrationAudio.tsx | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1376:   507	     4	interface NarrationAudioProps {
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1387:   518	    15	 * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1404:     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1442:    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1458:    59	`--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1463:    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1466:    67	| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1471:    72	つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1477:    78	- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1483:    84	python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1486:    87	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1487:    88	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1490:    91	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1491:    92	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1494:    95	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1500:   101	- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1518:   119	MainVideo.tsx <NarrationAudio /> 有効化
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2161:    22	function segmentToSubtitleItem(segment: TelopSegment, fps: number): SubtitleItem {
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2162:    23	  const startSec = segment.startFrame / fps;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2163:    24	  const endSec = segment.endFrame / fps;
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2177:    38	  const { fps } = useVideoConfig();
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2193:    54	      fps,
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2194:    55	      subtitles: [segmentToSubtitleItem(current, fps)],
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2219:   524	    21	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2261:   566	    29	   - voicevox_narration.py の chunk wav 結合を per-chunk start/duration に変換
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2262:   567	    30	   - NarrationAudio.tsx を <Sequence from=... duration=...> ループ実装
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2263:   568	    31	   - chunk_meta.json (start_ms / duration_ms) を public/narration/ に書き出し
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2488:   793	     8	import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2526:   831	    46	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2538:   843	/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '1,260p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2551:   856	    12	    python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2552:   857	    13	    python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2553:   858	    14	    python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2554:   859	    15	    python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2555:   860	    16	    python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2615:   920	    76	def concat_wavs(wavs: list[Path], out_path: Path) -> None:
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2721:`NarrationAudio.tsx` は現状 `public/narration.wav` 単体を `<Audio>` で鳴らすだけ、`voicevox_narration.py` も chunk を結合して最後に chunk ファイルを消す設計です。ここは Phase 3-H の i が既存設計の延長として一番まっすぐです。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2946:   218	     8	import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2984:   256	    46	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3061:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3064:skills/supermovie-narration/SKILL.md:67:| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3065:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3067:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3068:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3069:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3070:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3071:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3072:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3074:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3099:template/scripts/voicevox_narration.py:2:"""SuperMovie Phase 3-D: VOICEVOX で transcript_fixed.json から narration を生成.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3100:template/scripts/voicevox_narration.py:7:- 入力 override: --script narration_script.txt / --script-json narration_script.json
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3101:template/scripts/voicevox_narration.py:8:- 出力: public/narration.wav (segments 個別 wav を結合)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3102:template/scripts/voicevox_narration.py:9:- API: POST /audio_query → POST /synthesis (公式 https://github.com/VOICEVOX/voicevox_engine)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3103:template/scripts/voicevox_narration.py:12:    python3 scripts/voicevox_narration.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3104:template/scripts/voicevox_narration.py:13:    python3 scripts/voicevox_narration.py --speaker 3
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3105:template/scripts/voicevox_narration.py:14:    python3 scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3106:template/scripts/voicevox_narration.py:15:    python3 scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3107:template/scripts/voicevox_narration.py:16:    python3 scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3108:template/scripts/voicevox_narration.py:19:    https://voicevox.hiroshiba.jp/ から VOICEVOX をインストール、起動すると
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3109:template/scripts/voicevox_narration.py:115:    ap.add_argument("--script", help="custom plain-text narration (1 line = 1 chunk)")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3110:template/scripts/voicevox_narration.py:116:    ap.add_argument("--script-json", help="custom JSON {segments:[{text}]} narration")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3111:template/scripts/voicevox_narration.py:120:    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3112:template/scripts/voicevox_narration.py:122:                    help="chunk wav を public/narration/ に保存 (debug 用)")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3113:template/scripts/voicevox_narration.py:124:                    help="一部 chunk synthesis 失敗でも narration.wav を出力 (default は全 chunk 成功必須)")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3114:template/scripts/voicevox_narration.py:133:        print(f"INFO: {msg} -> narration generation skipped")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3115:template/scripts/voicevox_narration.py:135:            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3116:template/scripts/voicevox_narration.py:155:        print("ERROR: no narration chunks", file=sys.stderr)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3117:template/scripts/voicevox_narration.py:158:    chunks_dir = PROJ / "public" / "narration"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3118:template/scripts/voicevox_narration.py:178:            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3139:template/src/Narration/NarrationAudio.tsx:5:  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3140:template/src/Narration/NarrationAudio.tsx:11: * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3141:template/src/Narration/NarrationAudio.tsx:12: * Phase 3-F asset gate: public/narration.wav が無い時は null を返して render を
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3142:template/src/Narration/NarrationAudio.tsx:15: * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3143:template/src/Narration/NarrationAudio.tsx:22:  file = 'narration.wav',
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4050:    14	        fps={FPS}
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4130:    12	- 入力動画: `0503_テスト素材.MP4` (HEVC / 3840x2160 raw / rotation -90 / 60fps / 41.93s / 458MB / iPhone 撮影、DOVI profile 8 / 10-bit)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4131:    13	- 出力: `out/video.mp4` (h264 / 1080x1920 縦 / 39.21s / 60fps / aac 48kHz / 292.81MB)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4335:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4338:- 修正: `template/scripts/voicevox_narration.py`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4339:  - chunk wav を削除せず `public/narration/chunk_000.wav` 形式で保持。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4341:  - `public/narration/chunk_meta.json` は debug 用、render 本体用に `src/Narration/narrationData.ts` も生成する。既存 layer は TS data 駆動です（[ImageSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/ImageSequence.tsx:9), [SlideSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Slides/SlideSequence.tsx:15)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4342:- 修正: `template/src/Narration/NarrationAudio.tsx`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4343:  - `narrationData.map()` で `<Sequence from durationInFrames><Audio /></Sequence>`。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4344:  - `narrationData` が空なら legacy `narration.wav` 再生に fallback。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4346:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4347:- API 選定: 新規課金 API なし。既存 VOICEVOX local REST `/audio_query` → `/synthesis` を継続（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:68)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4352:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4355:- chunk file / `narrationData.ts` / `chunk_meta.json` の対応が崩れないか。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4393:理由: i は Phase 3-D の既存延長で、`voicevox_narration.py` は現状 chunk を `public/narration.wav` に結合し、`NarrationAudio.tsx` は単一 wav を鳴らすだけです（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:76), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:21)）。ii は Gemini API 課金、iv は deepfake 系で Roku 判断領域、iii は素材判断依存という制約に入ります（Roku 発言:「課金発生する API 利用」「法的/モラルリスク」「素材判断 Roku に依存」）。v は `no-explicit-any` が warning 緩和中なので次点として妥当ですが、体験価値は i より小さいです（[eslint.config.mjs](/Users/rokumasuda/.claude/plugins/supermovie/template/eslint.config.mjs:6)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4396:- 修正: `template/scripts/voicevox_narration.py`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4397:  - chunk wav を削除せず `public/narration/chunk_000.wav` 形式で保持。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4399:  - `public/narration/chunk_meta.json` は debug 用、render 本体用に `src/Narration/narrationData.ts` も生成する。既存 layer は TS data 駆動です（[ImageSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/ImageSequence.tsx:9), [SlideSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Slides/SlideSequence.tsx:15)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4400:- 修正: `template/src/Narration/NarrationAudio.tsx`
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4401:  - `narrationData.map()` で `<Sequence from durationInFrames><Audio /></Sequence>`。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4402:  - `narrationData` が空なら legacy `narration.wav` 再生に fallback。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4404:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4405:- API 選定: 新規課金 API なし。既存 VOICEVOX local REST `/audio_query` → `/synthesis` を継続（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:68)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4410:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4413:- chunk file / `narrationData.ts` / `chunk_meta.json` の対応が崩れないか。
./template/src/強調テロップ/オレンジグラデーション.tsx:20:  fps: number;
./template/src/ネガティブテロップ/黒紫グラデ.tsx:20:  fps: number;
./template/src/強調テロップ/黒文字黄色背景.tsx:20:  fps: number;
./template/src/Title/Title.tsx:25:  const { fps } = useVideoConfig();
./template/src/Title/Title.tsx:37:    fps,
./template/src/強調テロップ/白文字赤シャドウ.tsx:20:  fps: number;
./template/src/強調テロップ/金グラデ・紺背景.tsx:20:  fps: number;
./template/src/ネガティブテロップ/残酷テロップ・紺.tsx:20:  fps: number;
./template/scripts/preflight_video.py:203:    fps = detect_vfr(video)
./template/scripts/preflight_video.py:223:        "fps": {**fps, "render_fps": int(round(eval_fps(fps["r_frame_rate"])))},
./template/scripts/preflight_video.py:225:        "duration_frames": int(round(duration_sec * eval_fps(fps["r_frame_rate"]))),
./template/scripts/preflight_video.py:249:def eval_fps(rate_str: str) -> float:
./template/scripts/preflight_video.py:267:    if (source.get("fps") or {}).get("vfr_metadata_suspect"):
./template/src/強調テロップ/緑グラデ金シャドウ.tsx:20:  fps: number;
./template/src/Narration/narrationData.ts:2: * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
./template/src/Narration/narrationData.ts:3: * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
./template/src/Narration/narrationData.ts:7:export const narrationData: NarrationSegment[] = [];
./template/src/Narration/NarrationAudio.tsx:3:import { narrationData } from './narrationData';
./template/src/Narration/NarrationAudio.tsx:5:interface NarrationAudioProps {
./template/src/Narration/NarrationAudio.tsx:12: * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
./template/src/Narration/NarrationAudio.tsx:13: * narrationData.ts を生成する経路)。
./template/src/Narration/NarrationAudio.tsx:16: *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
./template/src/Narration/NarrationAudio.tsx:19: *   2) narrationData が空 + public/narration.wav 存在
./template/src/Narration/NarrationAudio.tsx:24: * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
./template/src/Narration/NarrationAudio.tsx:29:export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./template/src/Narration/NarrationAudio.tsx:35:  if (narrationData.length > 0) {
./template/src/Narration/NarrationAudio.tsx:36:    const allChunksExist = narrationData.every((seg) =>
./template/src/Narration/NarrationAudio.tsx:44:        {narrationData.map((seg) => (
./template/src/強調テロップ/黄色文字黒シャドウ.tsx:20:  fps: number;
./template/src/ネガティブテロップ/白文字紫シャドウ.tsx:20:  fps: number;
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:149:    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:628:     8	import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:670:    50	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:686:     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:724:    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:740:    59	`--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:745:    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:748:    67	| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:753:    72	つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:759:    78	- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:765:    84	python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:768:    87	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:769:    88	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:772:    91	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:773:    92	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:776:    95	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:782:   101	- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:801:   120	    └ NarrationAudio: <Audio src=narration.wav /> マウント
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1335:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1432:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1480:    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2150:template/scripts/voicevox_narration.py:165:            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2410:template/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2417:template/src/Narration/NarrationAudio.tsx
./template/src/強調テロップ/青文字金枠.tsx:20:  fps: number;
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:218:     8	import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:256:    46	      <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:902:    99	    "fps": {
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:905:   102	      "render_fps": 60,
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1140:     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1178:    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1194:    59	`--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1199:    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1202:    67	| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1207:    72	つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1213:    78	- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1219:    84	python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1222:    87	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1223:    88	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1226:    91	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1227:    92	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1230:    95	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1236:   101	- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1254:   119	MainVideo.tsx <NarrationAudio /> 有効化
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1352:/bin/zsh -lc 'nl -ba template/src/Narration/NarrationAudio.tsx' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1381:     4	interface NarrationAudioProps {
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1392:    15	 * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1398:    21	export const NarrationAudio: React.FC<NarrationAudioProps> = ({
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1423:    14	        fps={FPS}
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1440:skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1442:skills/supermovie-narration/SKILL.md:67:| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1443:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1452:template/scripts/voicevox_narration.py:8:- 出力: public/narration.wav (segments 個別 wav を結合)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1453:template/scripts/voicevox_narration.py:120:    ap.add_argument("--output", default=str(PROJ / "public" / "narration.wav"))
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1454:template/scripts/voicevox_narration.py:124:                    help="一部 chunk synthesis 失敗でも narration.wav を出力 (default は全 chunk 成功必須)")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1455:template/scripts/voicevox_narration.py:135:            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1456:template/scripts/voicevox_narration.py:136:            "getStaticFiles で検出し null を返すため render は失敗しない (Phase 3-F asset gate)"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1457:template/scripts/voicevox_narration.py:178:            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1501:template/src/Narration/NarrationAudio.tsx:2:import { Audio, getStaticFiles, staticFile } from 'remotion';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1502:template/src/Narration/NarrationAudio.tsx:5:  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1503:template/src/Narration/NarrationAudio.tsx:11: * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1504:template/src/Narration/NarrationAudio.tsx:12: * Phase 3-F asset gate: public/narration.wav が無い時は null を返して render を
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1505:template/src/Narration/NarrationAudio.tsx:22:  file = 'narration.wav',
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1506:template/src/Narration/NarrationAudio.tsx:25:  const hasFile = getStaticFiles().some((f) => f.name === file);
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1589: `--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1594:-`template/src/Narration/NarrationAudio.tsx` を `MainVideo.tsx` に追加。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1597:+`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1602:-import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1604:-// <NarrationAudio volume={1.0} />  ← narration 再生
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1606:+| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1611:+つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1617:+- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1960: import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2038:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1463:    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2046:./skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2066:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1199:    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2072:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1440:skills/supermovie-narration/SKILL.md:64:`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2077:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1506:template/src/Narration/NarrationAudio.tsx:25:  const hasFile = getStaticFiles().some((f) => f.name === file);
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2083:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1597:+`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2091:./template/scripts/voicevox_narration.py:119:                    help="engine 不在で exit 4 (default は skip exit 0)")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2102:./template/src/Narration/NarrationAudio.tsx:25:  const hasFile = getStaticFiles().some((f) => f.name === file);
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2216:       既存 BGM.tsx / NarrationAudio.tsx と同じ asset gate パターン。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2220:       asset gate auto-mount 方式に書き換え。voicevox_narration.py 実行 →
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2535:   Remotion の <NarrationAudio /> layer で再生するスキル。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2573: `voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2589: `--keep-chunks` で chunk 個別 wav も保持 (debug)。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2594:-`template/src/Narration/NarrationAudio.tsx` を `MainVideo.tsx` に追加。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2597:+`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2602:-import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2604:-// <NarrationAudio volume={1.0} />  ← narration 再生
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2606:+| narration.wav 状態 | NarrationAudio | base Video volume |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2611:+つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2617:+- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2623: python3 <PROJECT>/scripts/voicevox_narration.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2626: python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2627: python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2630: python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2631: python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2634: python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2640: - (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2658: MainVideo.tsx <NarrationAudio /> 有効化
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2680: import { NarrationAudio } from './Narration';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2720:       <NarrationAudio volume={1.0} />
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4545:template/scripts/voicevox_narration.py:18:Engine 起動 (Roku ローカル):
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4546:template/scripts/voicevox_narration.py:35:DEFAULT_SPEAKER = 3  # ずんだもん (ノーマル)、Roku が --speaker で上書き可
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4618:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4691:skills/supermovie-narration/SKILL.md:78:- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4745:   130	- `fps.r_frame_rate` / `fps.avg_frame_rate` / `fps.vfr_metadata_suspect`
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4760:   145	| VFR (可変 fps) | `r_frame_rate` ≠ `avg_frame_rate` (誤差 > 0.5%) | frame 換算で時間ずれ | render 前に CFR 化 (ffmpeg `-r`) を別タスクで |
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4799:   184	export const FPS = <render_fps>; // preflight source.fps.render_fps
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5029:template/src/Narration/NarrationAudio.tsx
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5087:/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '190,245p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5114:/bin/zsh -lc "nl -ba template/scripts/voicevox_narration.py | sed -n '110,190p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5116:/bin/zsh -lc 'rg -n "write_bytes|narration.wav|allow-partial|keep-chunks|output" template/scripts/voicevox_narration.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5120:121:    ap.add_argument("--keep-chunks", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5121:123:    ap.add_argument("--allow-partial", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5123:135:            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5125:178:            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5141:   121	    ap.add_argument("--keep-chunks", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5143:   123	    ap.add_argument("--allow-partial", action="store_true",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5155:   135	            "      Remotion 側の <NarrationAudio /> は public/narration.wav 不在を "
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5187:   167	        p = chunks_dir / f"chunk_{i:03d}.wav"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5198:   178	            f"(--allow-partial で部分成功でも narration.wav 出力可)",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5205:   185	    concat_wavs(chunk_paths, out_path)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5217:     1	export { NarrationAudio } from './NarrationAudio';
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5243:7. [skills/supermovie-narration/SKILL.md:119](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:119) / Phase 4 本文は手作業不要に修正されていますが、連携マップの「`MainVideo.tsx <NarrationAudio /> 有効化`」は旧手順っぽく読めます。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5246:8. [template/src/MainVideo.tsx:17](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:17) / `getStaticFiles()` の存在判定自体は二重音声防止として筋が通っています。`NarrationAudio` も同じ `narration.wav` を見ます（[NarrationAudio.tsx:22](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:22), [NarrationAudio.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:25)）。ただし Remotion 公式は `getStaticFiles()` が Studio/render 中だけ有効で、それ以外では空配列と明記しています（https://www.remotion.dev/docs/getstaticfiles）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5305:7. [skills/supermovie-narration/SKILL.md:119](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:119) / Phase 4 本文は手作業不要に修正されていますが、連携マップの「`MainVideo.tsx <NarrationAudio /> 有効化`」は旧手順っぽく読めます。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5308:8. [template/src/MainVideo.tsx:17](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:17) / `getStaticFiles()` の存在判定自体は二重音声防止として筋が通っています。`NarrationAudio` も同じ `narration.wav` を見ます（[NarrationAudio.tsx:22](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:22), [NarrationAudio.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:25)）。ただし Remotion 公式は `getStaticFiles()` が Studio/render 中だけ有効で、それ以外では空配列と明記しています（https://www.remotion.dev/docs/getstaticfiles）。  
./template/src/Narration/types.ts:3: * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
./template/src/Narration/types.ts:13:  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
./template/src/強調テロップ/赤文字.tsx:20:  fps: number;
./template/src/Narration/index.ts:1:export { NarrationAudio } from './NarrationAudio';
./template/src/Narration/index.ts:2:export { narrationData } from './narrationData';
./template/src/強調テロップ/赤文字白背景.tsx:20:  fps: number;
./template/src/ネガティブテロップ/黒文字白背景.tsx:20:  fps: number;
./template/src/MainVideo.tsx:8:import { NarrationAudio, narrationData } from './Narration';
./template/src/MainVideo.tsx:17:  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
./template/src/MainVideo.tsx:27:    narrationData.length > 0 &&
./template/src/MainVideo.tsx:28:    narrationData.every((seg) =>
./template/src/MainVideo.tsx:61:      <NarrationAudio volume={1.0} />
./template/src/強調テロップ/白緑テロップ.tsx:20:  fps: number;
./template/src/強調テロップ/黄色シャドウ.tsx:20:  fps: number;
./template/src/メインテロップ/白文字黒シャドウゴシック.tsx:20:  fps: number;
./template/src/Root.tsx:14:        fps={FPS}
./template/src/メインテロップ/白文字黒シャドウ明朝体.tsx:20:  fps: number;
./template/src/メインテロップ/白青テロップver2.tsx:20:  fps: number;
./template/src/メインテロップ/白文字青ピンク背景グラデ.tsx:20:  fps: number;
./template/src/メインテロップ/白青テロップ.tsx:20:  fps: number;
./template/src/テロップテンプレート/telopTemplateRegistry.tsx:53:  fps: number;
./template/src/メインテロップ/青文字白背景.tsx:20:  fps: number;
./template/src/メインテロップ/白文字黒背景.tsx:20:  fps: number;
./template/src/メインテロップ/白黒テロップ.tsx:20:  fps: number;
./template/src/メインテロップ/黒文字.tsx:20:  fps: number;
./template/src/メインテロップ/白背景グラデ.tsx:20:  fps: number;
./template/src/メインテロップ/白文字黒シャドウ.tsx:20:  fps: number;
./template/src/メインテロップ/緑文字白背景.tsx:20:  fps: number;
./template/src/テロップテンプレート/Telop.tsx:125:  fps: number;
./template/src/テロップテンプレート/Telop.tsx:129:}> = ({ text, localFrame, fps, config, animation, duration }) => {
./template/src/テロップテンプレート/Telop.tsx:152:          fps,
./template/src/テロップテンプレート/Telop.tsx:201:  const { fps, width } = useVideoConfig();
./template/src/テロップテンプレート/Telop.tsx:243:        fps,
./template/src/テロップテンプレート/Telop.tsx:307:              fps={fps}
./template/src/テロップテンプレート/TelopPlayer.tsx:22:function segmentToSubtitleItem(segment: TelopSegment, fps: number): SubtitleItem {
./template/src/テロップテンプレート/TelopPlayer.tsx:23:  const startSec = segment.startFrame / fps;
./template/src/テロップテンプレート/TelopPlayer.tsx:24:  const endSec = segment.endFrame / fps;
./template/src/テロップテンプレート/TelopPlayer.tsx:38:  const { fps } = useVideoConfig();
./template/src/テロップテンプレート/TelopPlayer.tsx:54:      fps,
./template/src/テロップテンプレート/TelopPlayer.tsx:55:      subtitles: [segmentToSubtitleItem(current, fps)],

codex
主要 diff は読みました。次は既存呼び出し・設定・Remotion 側の実際の fps 配線を横断検索して、破壊的互換性と runtime 条件の見落としを潰します。
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/src/Narration/types.ts | sed -n '1,80p'" in /Users/rokumasuda/.claude/plugins/supermovie
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

exec
/bin/zsh -lc "nl -ba template/src/Narration/narrationData.ts | sed -n '1,80p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	/**
     2	 * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
     3	 * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
     4	 */
     5	import type { NarrationSegment } from './types';
     6	
     7	export const narrationData: NarrationSegment[] = [];

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/package.json template/tsconfig.json template/eslint.config.mjs template/.prettierrc | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
usage: nl [-p] [-b type] [-d delim] [-f type] [-h type] [-i incr] [-l num]
          [-n format] [-s sep] [-v startnum] [-w width] [file]

exec
/bin/zsh -lc "nl -ba template/src/Narration/index.ts | sed -n '1,40p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	export { NarrationAudio } from './NarrationAudio';
     2	export { narrationData } from './narrationData';
     3	export type { NarrationSegment } from './types';

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
exec
/bin/zsh -lc "nl -ba template/tsconfig.json | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba template/package.json | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
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

hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/eslint.config.mjs | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
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
/bin/zsh -lc "nl -ba template/.prettierrc | sed -n '1,120p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	{
     2	  "singleQuote": true,
     3	  "trailingComma": "all",
     4	  "tabWidth": 2
     5	}

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git show --name-status --oneline --no-renames 41dbec5' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-iNh40BTC' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-3IM4g8GC' (errno=Operation not permitted)
41dbec5 feat(narration): per-segment <Sequence> timeline (Phase 3-H)
M	skills/supermovie-narration/SKILL.md
M	template/scripts/voicevox_narration.py
M	template/src/MainVideo.tsx
M	template/src/Narration/NarrationAudio.tsx
M	template/src/Narration/index.ts
A	template/src/Narration/narrationData.ts
A	template/src/Narration/types.ts

hook: PreToolUse
hook: PreToolUse
exec
/bin/zsh -lc 'git show --name-status --oneline --no-renames 85e824e' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-GdpxoD42' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-EYzaB1TH' (errno=Operation not permitted)
85e824e fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
M	template/scripts/visual_smoke.py

hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba CLAUDE.md | sed -n '70,115p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
    70	## データスキーマ（全スキル共通の信頼できる唯一の定義）
    71	
    72	### project-config.json
    73	
    74	```json
    75	{
    76	  "format": "youtube",
    77	  "resolution": { "width": 1920, "height": 1080 },
    78	  "videoType": "YouTube解説",
    79	  "targetAudience": "ビジネスパーソン",
    80	  "tone": "プロフェッショナル",
    81	  "telopStyle": {
    82	    "main": "白青テロップver2",
    83	    "emphasis": "オレンジグラデーション",
    84	    "negative": "黒紫グラデ"
    85	  },
    86	  "bgmMood": "アップテンポ",
    87	  "notes": "テンポ重視、キーワード「AI」を強調",
    88	  "createdAt": "2026-03-25",
    89	  "source": {
    90	    "video": "main.mp4",
    91	    "raw": { "width": 3840, "height": 2160 },
    92	    "display": { "width": 2160, "height": 3840 },
    93	    "rotation": { "raw": -90, "normalized": -90, "source": "Display Matrix" },
    94	    "aspect": 0.5625,
    95	    "sar": "1:1",
    96	    "dar": null,
    97	    "inferred_format": "short",
    98	    "chosen_format": "short",
    99	    "fps": {
   100	      "r_frame_rate": "60/1",
   101	      "avg_frame_rate": "503200/8387",
   102	      "render_fps": 60,
   103	      "vfr_metadata_suspect": false
   104	    },
   105	    "duration_sec": 41.93,
   106	    "duration_frames": 2516,
   107	    "codec": {
   108	      "name": "hevc",
   109	      "profile": "Main 10",
   110	      "pix_fmt": "yuv420p10le",
   111	      "field_order": "progressive"
   112	    },
   113	    "color": {
   114	      "range": "tv",
   115	      "space": "bt2020nc",

exec
/bin/zsh -lc "nl -ba template/src/Root.tsx | sed -n '1,80p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
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

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/src/videoConfig.ts | sed -n '1,120p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
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

exec
/bin/zsh -lc "rg -n \"--keep-chunks|keep_chunks|keep-chunks\" --glob '"'!docs/**'"' --glob '"'!node_modules/**'"' ." in /Users/rokumasuda/.claude/plugins/supermovie
 exited 2 in 0ms:
rg: unrecognized flag --keep-chunks|keep_chunks|keep-chunks

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'rg -n "voicevox_narration.py[''^'"\\n]*--|voicevox_narration.py\" --glob '"'!docs/**'"' --glob '"'!node_modules/**'"' ." in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "rg -n \"getStaticFiles|watchStaticFile|staticFile\" template/src skills --glob '"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
template/src/MainVideo.tsx:1:import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
template/src/MainVideo.tsx:18:  // どちらも不在なら base 元音声 1.0 で再生。getStaticFiles は Studio/render 時に
template/src/MainVideo.tsx:22:  // (Cmd+R / `r` キー) で反映する。新規 asset 追加に watchStaticFile を使う選択肢
template/src/MainVideo.tsx:24:  const staticFiles = getStaticFiles();
template/src/MainVideo.tsx:25:  const hasLegacyNarration = staticFiles.some((f) => f.name === NARRATION_FILE);
template/src/MainVideo.tsx:29:      staticFiles.some((f) => f.name === seg.file),
template/src/MainVideo.tsx:31:    staticFiles.some((f) => f.name.startsWith(NARRATION_CHUNK_PREFIX));
template/src/MainVideo.tsx:39:        src={staticFile(VIDEO_FILE)}
skills/supermovie-narration/SKILL.md:146:`getStaticFiles()` は Studio 起動時の asset リストをキャッシュするため、
template/src/InsertImage/InsertImage.tsx:2:import { useCurrentFrame, interpolate, Img, staticFile } from 'remotion';
template/src/InsertImage/InsertImage.tsx:43:          src={staticFile(`images/${segment.file}`)}
template/src/InsertImage/InsertImage.tsx:65:        src={staticFile(`images/${segment.file}`)}
template/src/SoundEffects/SESequence.tsx:1:import { Audio, Sequence, staticFile } from 'remotion';
template/src/SoundEffects/SESequence.tsx:11:            <Audio src={staticFile(`se/${se.file}`)} volume={() => v} />
template/src/SoundEffects/BGM.tsx:1:import { Audio, getStaticFiles, staticFile } from 'remotion';
template/src/SoundEffects/BGM.tsx:11: * 失敗させない。getStaticFiles() は public/ 以下の asset 一覧を返す Remotion 公式 API
template/src/SoundEffects/BGM.tsx:15:  const hasFile = getStaticFiles().some((f) => f.name === BGM_FILE);
template/src/SoundEffects/BGM.tsx:19:  return <Audio src={staticFile(BGM_FILE)} volume={() => volume} loop />;
template/src/Narration/NarrationAudio.tsx:2:import { Audio, Sequence, getStaticFiles, staticFile } from 'remotion';
template/src/Narration/NarrationAudio.tsx:33:  const staticFiles = getStaticFiles();
template/src/Narration/NarrationAudio.tsx:37:      staticFiles.some((f) => f.name === seg.file),
template/src/Narration/NarrationAudio.tsx:50:            <Audio src={staticFile(seg.file)} volume={() => volume} />
template/src/Narration/NarrationAudio.tsx:57:  const hasFile = staticFiles.some((f) => f.name === file);
template/src/Narration/NarrationAudio.tsx:61:  return <Audio src={staticFile(file)} volume={() => volume} />;

 succeeded in 0ms:
./skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
./skills/supermovie-narration/SKILL.md:86:`voicevox_narration.py` 成功 → `narrationData.ts` 上書き + chunk 配置 → 次回
./skills/supermovie-narration/SKILL.md:100:python3 <PROJECT>/scripts/voicevox_narration.py
./skills/supermovie-narration/SKILL.md:103:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
./skills/supermovie-narration/SKILL.md:104:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
./skills/supermovie-narration/SKILL.md:107:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
./skills/supermovie-narration/SKILL.md:108:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
./skills/supermovie-narration/SKILL.md:111:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
./template/scripts/voicevox_narration.py:21:    python3 scripts/voicevox_narration.py
./template/scripts/voicevox_narration.py:22:    python3 scripts/voicevox_narration.py --speaker 3
./template/scripts/voicevox_narration.py:23:    python3 scripts/voicevox_narration.py --script narration.txt
./template/scripts/voicevox_narration.py:24:    python3 scripts/voicevox_narration.py --list-speakers
./template/scripts/voicevox_narration.py:25:    python3 scripts/voicevox_narration.py --require-engine
./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
./template/scripts/voicevox_narration.py:192:        " * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換えた narration timeline。",
./template/src/Narration/NarrationAudio.tsx:12: * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
./template/src/Narration/types.ts:3: * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
./template/src/Narration/narrationData.ts:2: * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n -e \"--keep-chunks\" -e \"keep_chunks\" -e \"keep-chunks\" --glob '"'!docs/**'"' --glob '"'!node_modules/**'"' ." in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
exec
/bin/zsh -lc "git grep -n -- 'voicevox_narration.py' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "git grep -n -- '--keep-chunks' roku/phase3g-visual-smoke -- . ':"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-y6FWzVDT' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-IStL70W8' (errno=Operation not permitted)
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:43:`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:72:つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:84:python3 <PROJECT>/scripts/voicevox_narration.py
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:87:python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:88:python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:91:python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:92:python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:95:python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:12:    python3 scripts/voicevox_narration.py
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:13:    python3 scripts/voicevox_narration.py --speaker 3
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:14:    python3 scripts/voicevox_narration.py --script narration.txt
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:15:    python3 scripts/voicevox_narration.py --list-speakers
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:16:    python3 scripts/voicevox_narration.py --require-engine
roku/phase3g-visual-smoke:template/src/Narration/NarrationAudio.tsx:15: * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-JdwJD4NI' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-MCSYmX0L' (errno=Operation not permitted)
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:59:`--keep-chunks` で chunk 個別 wav も保持 (debug)。
roku/phase3g-visual-smoke:skills/supermovie-narration/SKILL.md:101:- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
roku/phase3g-visual-smoke:template/scripts/voicevox_narration.py:121:    ap.add_argument("--keep-chunks", action="store_true",

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"chunk-only|FPS|stale|危険|top3|Top|TOP|mute|cache\" docs/reviews --glob '*.md'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'ls -la docs docs/reviews' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
docs:
total 0
drwxr-xr-x   3 rokumasuda  staff   96 May  4 21:29 .
drwxr-xr-x  13 rokumasuda  staff  416 May  4 21:29 ..
drwxr-xr-x   6 rokumasuda  staff  192 May  4 21:33 reviews

docs/reviews:
total 2256
drwxr-xr-x  6 rokumasuda  staff     192 May  4 21:33 .
drwxr-xr-x  3 rokumasuda  staff      96 May  4 21:29 ..
-rw-r--r--  1 rokumasuda  staff  237956 May  4 21:29 CODEX_PHASE3H_NEXT_20260504T211444.md
-rw-r--r--  1 rokumasuda  staff  515011 May  4 21:29 CODEX_REVIEW_PHASE3G_20260504T211444.md
-rw-r--r--  1 rokumasuda  staff  190270 May  4 21:29 CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md
-rw-r--r--  1 rokumasuda  staff  191155 May  4 21:34 CODEX_REVIEW_PHASE3H_20260504T213301.md

 succeeded in 0ms:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:37:C) MainVideo.tsx mute logic 拡張
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:55:   - Studio 起動中に narration を再生成した時の getStaticFiles cache 残存問題 (Phase 3-F 同様)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:56:   - Codex Phase 3-H consultation の危険ポイント top3 (chunk-only mute / FPS / stale) が全部 fix されているか
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:102:git: error: couldn't create cache file '/tmp/xcrun_db-TXyfxEjW' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:104:git: error: couldn't create cache file '/tmp/xcrun_db-AnWAsMGb' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:109:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:113:git: error: couldn't create cache file '/tmp/xcrun_db-qwiBqS0o' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:115:git: error: couldn't create cache file '/tmp/xcrun_db-ZslVDBsC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:203:git: error: couldn't create cache file '/tmp/xcrun_db-BxZNM0VB' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:205:git: error: couldn't create cache file '/tmp/xcrun_db-xP7OvmA5' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:229:git: error: couldn't create cache file '/tmp/xcrun_db-4CIv9r5q' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:231:git: error: couldn't create cache file '/tmp/xcrun_db-wxklg1BM' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:256:+- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:273:+DEFAULT_FPS = 30
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:298:+def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:306:+                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:440:+    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:511:git: error: couldn't create cache file '/tmp/xcrun_db-GBfpk1wn' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:513:git: error: couldn't create cache file '/tmp/xcrun_db-1kZvbhlE' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:530:git: error: couldn't create cache file '/tmp/xcrun_db-2yudiVke' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:532:git: error: couldn't create cache file '/tmp/xcrun_db-tKPT356H' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:549:-  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:552:+  // - legacy: public/narration.wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:612:+ * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:698:git: error: couldn't create cache file '/tmp/xcrun_db-Efofjwv1' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:700:git: error: couldn't create cache file '/tmp/xcrun_db-jrIXtF9L' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:732:+stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:745:-| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:753:-次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:757:+`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:877:    23	 * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:935:    17	- stale chunk (前回実行の遺物) を synthesis 前に必ず cleanup
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:964:    46	DEFAULT_FPS = 30
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1039:   121	def cleanup_stale_chunks() -> None:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1047:   129	                print(f"WARN: stale chunk {p.name} 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1210:   292	    cleanup_stale_chunks()
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1299:    16	  // - legacy: public/narration.wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1320:    37	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1562:    72	stale chunk (前回実行の遺物) は synthesis 開始前に必ず cleanup。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1577:    87	`npm run dev` / `npm run render` で自動的に per-segment narration 再生 + base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1669:./skills/supermovie-narration/SKILL.md:69:FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1672:./skills/supermovie-narration/SKILL.md:82:| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1673:./skills/supermovie-narration/SKILL.md:83:| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1691:./skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1696:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:24:   - cleanup_stale_chunks() で Path.glob `chunk_*.wav` の削除順序、SIGINT 安全性
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1723:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:265:+    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1728:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:299:+    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1731:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:311:+                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1733:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:321:+def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1748:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:409:+             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1756:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:439:+    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1771:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:553:+  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1784:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:613:+ * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1797:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:688:+  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1804:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:729:+FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1809:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:749:+| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1810:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:750:+| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1832:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:878:    24	 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1846:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:944:    26	    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1851:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1040:   122	    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1854:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1052:   134	                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1856:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1062:   144	def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1870:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1167:   249	             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1877:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1209:   291	    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1887:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1300:    17	  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1898:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1559:    69	FPS は `--fps` 引数 → `<PROJECT>/project-config.json` の `source.fps.render_fps` →
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1901:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1572:    82	| narrationData 空 + narration.wav 存在 (Phase 3-D legacy) | 単一 `<Audio>` 再生 | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1902:./docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1573:    83	| narrationData non-empty + 全 chunk 存在 (Phase 3-H) | `<Sequence from durationInFrames>` で chunk ループ | 0 (mute) |
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1930:./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1935:./template/scripts/voicevox_narration.py:122:    """旧 chunk_*.wav と chunk_meta.json を削除 (stale prevention)、
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1938:./template/scripts/voicevox_narration.py:134:                print(f"WARN: stale chunk_meta.json 削除失敗: {e}", file=sys.stderr)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1940:./template/scripts/voicevox_narration.py:144:def read_render_fps(default: int = DEFAULT_FPS) -> int:
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1954:./template/scripts/voicevox_narration.py:249:             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:1961:./template/scripts/voicevox_narration.py:291:    # Phase 3-H: stale chunk + narrationData.ts cleanup BEFORE synthesis
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2075:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4050:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2085:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4346:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2087:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4352:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2096:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4404:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2098:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4410:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2123:./template/src/Narration/NarrationAudio.tsx:24: * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2179:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1423:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2237:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2241:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4799:   184	export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2262:./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2270:./template/src/MainVideo.tsx:17:  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2277:./template/src/Root.tsx:14:        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2322:    11	  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2465:git: error: couldn't create cache file '/tmp/xcrun_db-iNh40BTC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2467:git: error: couldn't create cache file '/tmp/xcrun_db-3IM4g8GC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2483:git: error: couldn't create cache file '/tmp/xcrun_db-GdpxoD42' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2485:git: error: couldn't create cache file '/tmp/xcrun_db-EYzaB1TH' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2547:     4	import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2557:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2580:     9	export const FPS = 30;
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2602:    31	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2615:    44	    titleTop: 60,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2628:    57	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2693:./template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2697:./template/src/Narration/types.ts:11:  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2717:git: error: couldn't create cache file '/tmp/xcrun_db-y6FWzVDT' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2719:git: error: couldn't create cache file '/tmp/xcrun_db-IStL70W8' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2737:git: error: couldn't create cache file '/tmp/xcrun_db-JdwJD4NI' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3H_20260504T213301.md:2739:git: error: couldn't create cache file '/tmp/xcrun_db-MCSYmX0L' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:24:- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:48:3. 実装着手前の **危険ポイント** top3 (Phase 3-A〜3-G で踏んだ罠の再発予防観点)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:61:短く決定的に (P0 推奨 1 件 + 設計概要 + 危険ポイント top3)。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:561:    24	- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:585:    48	3. 実装着手前の **危険ポイント** top3 (Phase 3-A〜3-G で踏んだ罠の再発予防観点)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:598:    61	短く決定的に (P0 推奨 1 件 + 設計概要 + 危険ポイント top3)。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:799:    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:807:    22	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1469:    70	| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1472:    73	次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1820:     2	import { FPS } from '../videoConfig';
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1822:     4	const toFrame = (seconds: number) => Math.round(seconds * FPS);
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2072:   183	const FPS = 30; // Root.tsxの値
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2073:   184	const toFrame = (seconds: number) => Math.round(seconds * FPS);
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2256:   561	    24	- Phase 3-F hotfix (今回): base Video volume 自動 mute when narration present、SKILL.md / docs 整合
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2280:   585	    48	3. 実装着手前の **危険ポイント** top3 (Phase 3-A〜3-G で踏んだ罠の再発予防観点)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2293:   598	    61	短く決定的に (P0 推奨 1 件 + 設計概要 + 危険ポイント top3)。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2494:   799	    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2502:   807	    22	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2660:     9	export const FPS = 30;
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2682:    31	    titleTop: 40,
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2695:    44	    titleTop: 60,
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2708:    57	    titleTop: 40,
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2755:    27	   - template/src/MainVideo.tsx で getStaticFiles() の SSR/Studio mount 時の挙動 (cache, 初期 false 警戒)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2898:   170	git: error: couldn't create cache file '/tmp/xcrun_db-boxAZJQW' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2900:   172	git: error: couldn't create cache file '/tmp/xcrun_db-WetrWrLY' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2902:   174	30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2908:   180	git: error: couldn't create cache file '/tmp/xcrun_db-gNtNg0C9' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2910:   182	git: error: couldn't create cache file '/tmp/xcrun_db-MtZXUNL5' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2925:   197	git: error: couldn't create cache file '/tmp/xcrun_db-zMwVT9P5' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2927:   199	git: error: couldn't create cache file '/tmp/xcrun_db-ZsWgN5sk' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2952:   224	    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2960:   232	    22	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2994:git: error: couldn't create cache file '/tmp/xcrun_db-8nphmsbx' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2996:git: error: couldn't create cache file '/tmp/xcrun_db-gBMybt8W' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2999:git: error: couldn't create cache file '/tmp/xcrun_db-P2NR6fuE' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3001:git: error: couldn't create cache file '/tmp/xcrun_db-ouvPQrjI' (errno=Operation not permitted)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3003:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3046:README.md:98:narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3066:skills/supermovie-narration/SKILL.md:73:次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3092:template/src/MainVideo.tsx:14:  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3093:template/src/MainVideo.tsx:22:      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3190:    27	FPS = 60  # videoConfig.FPS と同期、後段で project-config から読むよう拡張可能
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3215:    52	            "playbackStart": round(cursor_ms / 1000 * FPS),
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3216:    53	            "playbackEnd": round((cursor_ms + dur_ms) / 1000 * FPS),
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3224:    61	        return round(ms / 1000 * FPS)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3228:    65	            return cs["playbackStart"] + round(offset_ms / 1000 * FPS)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3458:    31	FPS = 60
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3463:    36	MIN_DURATION_FRAMES = round(1.5 * FPS)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3464:    37	MAX_DURATION_FRAMES = round(5.0 * FPS)
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3763:    68	- cutData が存在しない場合は単純に `ms / 1000 * FPS`
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3990:    73	│   ├── Root.tsx                    ← 動画設定（FPS, フレーム数）
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4015:    98	narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4040:     4	import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4050:    14	        fps={FPS}
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4346:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4349:**危険ポイント top3**
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4350:1. chunk 出力に変えると base mute が漏れる。`MainVideo.tsx` の `hasNarration` は現状 `narration.wav` 固定なので、chunk-only で二重音声化するリスクがあります（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:17)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4351:2. FPS / cut timeline の不一致。Root は `videoConfig.FPS` を使う一方、生成 script 側に hardcoded FPS が残っています（[Root.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [videoConfig.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:8), [build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:26)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4352:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4404:  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4407:**危険ポイント top3**
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4408:1. chunk 出力に変えると base mute が漏れる。`MainVideo.tsx` の `hasNarration` は現状 `narration.wav` 固定なので、chunk-only で二重音声化するリスクがあります（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:17)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4409:2. FPS / cut timeline の不一致。Root は `videoConfig.FPS` を使う一方、生成 script 側に hardcoded FPS が残っています（[Root.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [videoConfig.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:8), [build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:26)）。
docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4410:3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:36:- #8 MainVideo.tsx: getStaticFiles Studio cache 仕様の docs
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:95:git: error: couldn't create cache file '/tmp/xcrun_db-7oeAB6y2' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:97:git: error: couldn't create cache file '/tmp/xcrun_db-GgMmHuQs' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:100:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:108:git: error: couldn't create cache file '/tmp/xcrun_db-U0ewm0qy' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:110:git: error: couldn't create cache file '/tmp/xcrun_db-JFBUjGqe' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:116:git: error: couldn't create cache file '/tmp/xcrun_db-Cw1LCjxp' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:118:git: error: couldn't create cache file '/tmp/xcrun_db-ljkrXQxc' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:634:    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:646:    26	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:751:    70	| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:754:    73	次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1447:git: error: couldn't create cache file '/tmp/xcrun_db-ZTrjDfgd' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1449:git: error: couldn't create cache file '/tmp/xcrun_db-pZQurEGk' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1755:git: error: couldn't create cache file '/tmp/xcrun_db-N38CJFP1' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1757:git: error: couldn't create cache file '/tmp/xcrun_db-hdXSoui6' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2383:git: error: couldn't create cache file '/tmp/xcrun_db-vp8VzGVY' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:2385:git: error: couldn't create cache file '/tmp/xcrun_db-E341qqHS' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:27:   - template/src/MainVideo.tsx で getStaticFiles() の SSR/Studio mount 時の挙動 (cache, 初期 false 警戒)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:170:git: error: couldn't create cache file '/tmp/xcrun_db-boxAZJQW' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:172:git: error: couldn't create cache file '/tmp/xcrun_db-WetrWrLY' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:174:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:180:git: error: couldn't create cache file '/tmp/xcrun_db-gNtNg0C9' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:182:git: error: couldn't create cache file '/tmp/xcrun_db-MtZXUNL5' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:197:git: error: couldn't create cache file '/tmp/xcrun_db-zMwVT9P5' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:199:git: error: couldn't create cache file '/tmp/xcrun_db-ZsWgN5sk' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:224:    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:232:    22	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:271:git: error: couldn't create cache file '/tmp/xcrun_db-1ieLiBzr' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:273:git: error: couldn't create cache file '/tmp/xcrun_db-BX9F9oqC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:366:    73	│   ├── Root.tsx                    ← 動画設定（FPS, フレーム数）
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:391:    98	narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1126:   323	- `videoConfig.ts` がFPS, 解像度, テロップサイズのSingle Source of Truth。各.tsxは直接値を持たない
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1205:    70	| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1208:    73	次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1284:     9	export const FPS = 30;
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1306:    31	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1319:    44	    titleTop: 60,
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1332:    57	    titleTop: 40,
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1413:     4	import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1423:    14	        fps={FPS}
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1451:README.md:98:narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1475:template/src/テロップテンプレート/telopData.ts:2:import { FPS as CONFIG_FPS, SOURCE_DURATION_FRAMES } from '../videoConfig';
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1485:template/src/MainVideo.tsx:14:  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1488:template/src/MainVideo.tsx:22:      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1498:template/src/Root.tsx:4:import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1514:git: error: couldn't create cache file '/tmp/xcrun_db-j3IX2cTx' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1516:git: error: couldn't create cache file '/tmp/xcrun_db-oGS3d8m9' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1578:+narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1603:-// <Video ... volume={0} />  ← base 元音声 mute
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1609:+| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1612:+次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1966:+  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1975:+      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2050:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:27:   - template/src/MainVideo.tsx で getStaticFiles() の SSR/Studio mount 時の挙動 (cache, 初期 false 警戒)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2155:git: error: couldn't create cache file '/tmp/xcrun_db-QLcplP1E' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2157:git: error: couldn't create cache file '/tmp/xcrun_db-bjj0xRw8' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2158:30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2169:git: error: couldn't create cache file '/tmp/xcrun_db-euNKxtaB' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2171:git: error: couldn't create cache file '/tmp/xcrun_db-Ps7sb5jN' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2200:git: error: couldn't create cache file '/tmp/xcrun_db-cjiodEMs' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2202:git: error: couldn't create cache file '/tmp/xcrun_db-fWq2WiBa' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2207:    fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2222:       base mute、Roku の手作業ゼロを明示。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2370: - `videoConfig.ts` がFPS, 解像度, テロップサイズのSingle Source of Truth。各.tsxは直接値を持たない
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2445: │   ├── Root.tsx                    ← 動画設定（FPS, フレーム数）
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2471:+narration.wav 存在時は base 動画の元音声が自動 mute される (二重音声防止)。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2603:-// <Video ... volume={0} />  ← base 元音声 mute
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2609:+| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2612:+次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2686:+  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2695:+      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2735:git: error: couldn't create cache file '/tmp/xcrun_db-K8sSqMYp' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2737:git: error: couldn't create cache file '/tmp/xcrun_db-yrt2npZG' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2912: - `videoConfig.ts` がFPS, 解像度, テロップサイズのSingle Source of Truth。各.tsxは直接値を持たない
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3524:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_exit_plan_mode_stale_file_reference.md:20:- もしくは、新 plan file を別 path に作った後、ExitPlanMode 呼び出し前に Roku に「承認画面に出るのは古い内容で、実際のプランは新 path にあります」と明示して目視確認を促す
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3525:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_exit_plan_mode_stale_file_reference.md:21:- 自動承認系 (auto mode 等) で進めると、Roku が古いプランを承認する → 私が新プランを実装、というズレが起きる。最低でも Roku に「承認画面の表示と実体プランがズレています、新 path を別途確認してください」と人間目視を入れる
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3526:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_exit_plan_mode_stale_file_reference.md:22:- 今回 (2026-04-28 Phase 2 着手前) は私が気づいて Roku に再確認したのでズレなく進んだが、気づかないと致命的なズレ事故になる
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3878:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_subagent_quality_gates.md:18:| 2. 実装中レビュー | diff レビュー、既存セクションとの整合性、型安全、cache breakpoint 上限、誤発火リスク、文体、パス実在確認 | reviewer (sonnet) | Edit 直前、Roku pre-review と並列 |
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3881:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_subagent_quality_gates.md:36:- 制約条件 (cache breakpoint 上限、既存動作への影響範囲、Roku判断領域の非踏み込み)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4075:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/MEMORY.md:109:- [feedback_autonomous_loop_with_schedulewakeup.md](feedback_autonomous_loop_with_schedulewakeup.md) — **超上位原則**: bg job (codex/render/install) 完了待ちで止まらず ScheduleWakeup で自分を周期起動 (270s 推奨、cache 内) して自走継続。Roku が blocker な時のみ止まる。2026-05-04 18:09 Roku「止まるなよ、ScheduleWakeup 使うのもルール化で」
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4318:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_handoff_stale_quotation.md:3:description: handoff_*.md は作成時点スナップショット。"In Progress" "Next Session Should" を現状進捗として引用すると、既に Roku が対応済みの項目を未完了扱いで再質問する事故になる
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4319:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_handoff_stale_quotation.md:12:**Why**: 2026-04-30 09:20 Roku 指摘「18万のROI整理を伊藤さんに共有→DONE、Onefee 5/1 Mtg 用 KPI 切り分け案→DONE、Anthropic console 月予算上限設定→DONE、何回も言わせるな」(Roku 発言)。私は `handoff_2026-04-29_session-end.md:48-58` と `handoff_2026-04-28_haru-ai-school-named-and-billing-incident.md:72-91` を現状真として引用し、3項目すべて未完了扱いで「今日進めますか?」と再質問。Roku は既に対応済みで、過去にも同種確認をしているため「何回も言わせるな」となった。同型ミスの繰り返し = 構造的欺瞞 Pattern 1 の特殊ケース (compaction summary 引用と同根、handoff も時間スナップショット)。
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4320:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_handoff_stale_quotation.md:18:   - (a) Roku 発話の最新ログ検索 (`~/.claude/projects/-Users-rokumasuda/*.jsonl` を grep)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4321:/Users/rokumasuda/.claude/projects/-Users-rokumasuda/memory/feedback_handoff_stale_quotation.md:19:   - (b) Roku に「<項目> の現状を教えてください」とフラットに聞く (ハンドオフ記載と紐付けない)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4677:skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4799:   184	export const FPS = <render_fps>; // preflight source.fps.render_fps
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4811:   196	const FPS = <検出値>;
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4921:git: error: couldn't create cache file '/tmp/xcrun_db-0vDuvJfC' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4923:git: error: couldn't create cache file '/tmp/xcrun_db-I0TAUvgt' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5011:git: error: couldn't create cache file '/tmp/xcrun_db-2yX0NxNc' (errno=Operation not permitted)
docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5013:git: error: couldn't create cache file '/tmp/xcrun_db-0FwgSB7z' (errno=Operation not permitted)

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git diff roku/phase3g-visual-smoke..HEAD --name-only' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-1TcCf67G' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-3zvVkHTJ' (errno=Operation not permitted)
skills/supermovie-narration/SKILL.md
template/scripts/visual_smoke.py
template/scripts/voicevox_narration.py
template/src/MainVideo.tsx
template/src/Narration/NarrationAudio.tsx
template/src/Narration/index.ts
template/src/Narration/narrationData.ts
template/src/Narration/types.ts

exec
/bin/zsh -lc 'git status --short docs/reviews' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-YKdvozaa' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-tTJ2opmz' (errno=Operation not permitted)
?? docs/reviews/

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba template/scripts/build_slide_data.py | sed -n '1,60p'" in /Users/rokumasuda/.claude/plugins/supermovie
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

exec
/bin/zsh -lc "nl -ba docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md | sed -n '4338,4356p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
  4338	- 修正: `template/scripts/voicevox_narration.py`
  4339	  - chunk wav を削除せず `public/narration/chunk_000.wav` 形式で保持。
  4340	  - WAV の実 duration を `wave` で測り、`startFrame / durationInFrames / file / text` を作る。
  4341	  - `public/narration/chunk_meta.json` は debug 用、render 本体用に `src/Narration/narrationData.ts` も生成する。既存 layer は TS data 駆動です（[ImageSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/InsertImage/ImageSequence.tsx:9), [SlideSequence.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Slides/SlideSequence.tsx:15)）。
  4342	- 修正: `template/src/Narration/NarrationAudio.tsx`
  4343	  - `narrationData.map()` で `<Sequence from durationInFrames><Audio /></Sequence>`。
  4344	  - `narrationData` が空なら legacy `narration.wav` 再生に fallback。
  4345	- 修正: `template/src/MainVideo.tsx`
  4346	  - mute 判定を `narration.wav` だけでなく `narration/chunk_` にも対応。現状は `narration.wav` のみです（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:11)）。
  4347	- API 選定: 新規課金 API なし。既存 VOICEVOX local REST `/audio_query` → `/synthesis` を継続（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:68)）。
  4348	
  4349	**危険ポイント top3**
  4350	1. chunk 出力に変えると base mute が漏れる。`MainVideo.tsx` の `hasNarration` は現状 `narration.wav` 固定なので、chunk-only で二重音声化するリスクがあります（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:17)）。
  4351	2. FPS / cut timeline の不一致。Root は `videoConfig.FPS` を使う一方、生成 script 側に hardcoded FPS が残っています（[Root.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [videoConfig.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:8), [build_slide_data.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/build_slide_data.py:26)）。
  4352	3. stale chunk と partial failure。現状 script は `--keep-chunks` なしで chunk を消すので、Phase 3-H では古い chunk 清掃と all-or-nothing 書き出しが必要です（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:189)）。
  4353	
  4354	**Codex review 重点**
  4355	- chunk file / `narrationData.ts` / `chunk_meta.json` の対応が崩れないか。
  4356	- `durationInFrames > 0`、start が timeline 上で妥当か、overlap は WARN で見えるか。

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"render_fps|export const FPS|SOURCE_DURATION_FRAMES|project-config\" template/scripts skills/supermovie-init template/src --glob '"'!docs/**'"'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "find template -maxdepth 3 -type f \\( -name 'project-config.json' -o -name 'narration.wav' -o -name 'chunk_*.wav' -o -name 'chunk_meta.json' \\) -print" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
 succeeded in 0ms:
skills/supermovie-init/SKILL.md:73:### ヒアリング結果 → `project-config.json`
skills/supermovie-init/SKILL.md:121:  --write-config "<PROJECT>/project-config.json" \
skills/supermovie-init/SKILL.md:126:**抽出される値 (project-config.json `source.*` に nested で書き込まれる):**
skills/supermovie-init/SKILL.md:184:export const FPS = <render_fps>; // preflight source.fps.render_fps
skills/supermovie-init/SKILL.md:185:export const SOURCE_DURATION_FRAMES = <duration_frames>; // 元動画 frame、cut 後は cutData.CUT_TOTAL_FRAMES を使う
template/scripts/voicevox_narration.py:6:- 入力: transcript_fixed.json の segments[] / project-config.json の tone
template/scripts/voicevox_narration.py:26:    python3 scripts/voicevox_narration.py --fps 60      # FPS 明示 (default は project-config.json or 30)
template/scripts/voicevox_narration.py:144:def read_render_fps(default: int = DEFAULT_FPS) -> int:
template/scripts/voicevox_narration.py:145:    """project-config.json から source.fps.render_fps を取得、無ければ default。"""
template/scripts/voicevox_narration.py:146:    cfg_path = PROJ / "project-config.json"
template/scripts/voicevox_narration.py:153:    fps = cfg.get("source", {}).get("fps", {}).get("render_fps")
template/scripts/voicevox_narration.py:249:             f"(default: project-config.json source.fps.render_fps、無ければ {DEFAULT_FPS})",
template/scripts/voicevox_narration.py:288:    fps = args.fps if args.fps is not None else read_render_fps()
template/scripts/generate_slide_plan.py:87:    config_path = PROJ / "project-config.json"
template/scripts/generate_slide_plan.py:89:        print(f"ERROR: transcript_fixed.json or project-config.json missing under {PROJ}", file=sys.stderr)
template/scripts/preflight_video.py:6:project-config.json source.* schema (nested) と risks リストを生成する。
template/scripts/preflight_video.py:13:        --write-config project-config.json \\
template/scripts/preflight_video.py:223:        "fps": {**fps, "render_fps": int(round(eval_fps(fps["r_frame_rate"])))},
template/scripts/preflight_video.py:294:    ap.add_argument("--write-config", help="project-config.json path to write")
template/scripts/build_telop_data.py:32:# Phase 1 短尺 (short) format 既定値、後段で project-config.json から読むよう拡張可能
template/scripts/build_telop_data.py:398:        "export const FPS = CONFIG_FPS;",
template/scripts/build_slide_data.py:2:"""SuperMovie Phase 3-B: transcript_fixed.json + project-config.json → src/Slides/slideData.ts.
template/scripts/build_slide_data.py:8:    <PROJECT>/project-config.json    - format / tone
template/scripts/build_slide_data.py:27:FPS = 60  # videoConfig.FPS と同期、後段で project-config から読むよう拡張可能
template/scripts/build_slide_data.py:320:    config_path = PROJ / "project-config.json"
template/scripts/build_slide_data.py:322:        raise SystemExit(f"missing input: transcript_fixed.json or project-config.json under {PROJ}")
template/src/テロップテンプレート/telopTemplateRegistry.tsx:108:// project-config.json telopStyle.{main,emphasis,negative} 既定値の displayName とのマップ:
template/src/テロップテンプレート/telopData.ts:2:import { FPS as CONFIG_FPS, SOURCE_DURATION_FRAMES } from '../videoConfig';
template/src/テロップテンプレート/telopData.ts:8:export const FPS = CONFIG_FPS;
template/src/テロップテンプレート/telopData.ts:9:export const TOTAL_FRAMES = SOURCE_DURATION_FRAMES;
template/src/Root.tsx:4:import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";
template/src/Root.tsx:13:        durationInFrames={SOURCE_DURATION_FRAMES}
template/src/videoConfig.ts:9:export const FPS = 30;
template/src/videoConfig.ts:11:export const SOURCE_DURATION_FRAMES = 1500; // placeholder

hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc 'test -d template/node_modules && echo node_modules-present || echo node_modules-missing' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
node_modules-missing

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'rg -n "loop" template/node_modules/remotion/dist template/node_modules/remotion 2>/dev/null | head -80' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'rg -n "getStaticFiles|watchStaticFile" template/node_modules/remotion template/node_modules/@remotion 2>/dev/null | head -80' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'rg -n "durationInFrames.*0|durationInFrames.*must|Sequence" template/node_modules/remotion template/node_modules/@remotion 2>/dev/null | head -80' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
 succeeded in 0ms:
 succeeded in 0ms:
web search: 
web search: Remotion Sequence durationInFrames must be positive zero documentation
web search: 
web search: https://www.remotion.dev/docs/getstaticfiles
web search: 
web search: 'durationInFrames must' in https://www.remotion.dev/docs/sequence
web search: 
web search: https://github.com/remotion-dev/remotion/blob/main/packages/core/src/Sequence.tsx
web search: 
web search: https://raw.githubusercontent.com/remotion-dev/remotion/main/packages/core/src/Sequence.tsx
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'find template -maxdepth 2 -type d -name node_modules -print' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
exec
/bin/zsh -lc 'git diff --check roku/phase3g-visual-smoke..HEAD' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-5QuiwqkQ' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-F7uw6epQ' (errno=Operation not permitted)

exec
/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 template/scripts/voicevox_narration.py --help | sed -n '1,120p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
usage: voicevox_narration.py [-h] [--speaker SPEAKER] [--script SCRIPT]
                             [--script-json SCRIPT_JSON] [--list-speakers]
                             [--require-engine] [--output OUTPUT] [--fps FPS]
                             [--allow-partial]

options:
  -h, --help            show this help message and exit
  --speaker SPEAKER     VOICEVOX speaker id (default 3=ずんだもんノーマル)
  --script SCRIPT       custom plain-text narration (1 line = 1 chunk)
  --script-json SCRIPT_JSON
                        custom JSON {segments:[{text}]} narration
  --list-speakers
  --require-engine      engine 不在で exit 4 (default は skip exit 0)
  --output OUTPUT
  --fps FPS             narrationData.ts に書き込む frame 換算 fps (default: project-
                        config.json source.fps.render_fps、無ければ 30)
  --allow-partial       一部 chunk synthesis 失敗でも narration.wav を出力 +
                        narrationData.ts 部分書き出し (default は全 chunk 成功必須)

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
exec
/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 -c 'import json; samples=[\"quote '\\'' and \\\" double\", r\"backslash \\\\ path\", \"line\\nbreak\"]; [print(json.dumps(s, ensure_ascii=False)) for s in samples]'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
"quote ' and \" double"
"backslash \\\\ path"
"line\nbreak"

hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 -c 'cfg={\"source\":None}; print(cfg.get(\"source\", {}).get(\"fps\", {}).get(\"render_fps\"))'" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    cfg={"source":None}; print(cfg.get("source", {}).get("fps", {}).get("render_fps"))
                               ^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'

exec
/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 -c 'import wave; print(wave.Error.__name__)'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
Error

exec
/bin/zsh -lc "PYTHONDONTWRITEBYTECODE=1 python3 -c 'cfg={\"source\":\"bad\"}; print(cfg.get(\"source\", {}).get(\"fps\", {}).get(\"render_fps\"))'" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    cfg={"source":"bad"}; print(cfg.get("source", {}).get("fps", {}).get("render_fps"))
                                ^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'get'

web search: 
web search: https://docs.python.org/3/library/wave.html
web search: 
web search: VOICEVOX engine synthesis API audio/wav response official
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
exec
/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '222,360p'" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '1,120p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
     3	
     4	3 format (youtube/short/square) × N frame で `npx remotion still` を生成し、
     5	各 PNG の dimension が format 期待値と一致するか ffprobe で検証する。
     6	
     7	| format | width × height | aspect |
     8	|--------|---------------|--------|
     9	| youtube | 1920 × 1080 | 16:9 |
    10	| short   | 1080 × 1920 | 9:16 |
    11	| square  | 1080 × 1080 | 1:1 |
    12	
    13	不一致 = exit non-zero (regression として CI/Roku 視認の双方で検知)。
    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
    15	
    16	Codex Phase 3G design (2026-05-04, CODEX_PHASE3G_NEXT) 推奨:
    17	- videoConfig.ts FORMAT を try/finally で in-place 切替 + restore
    18	- per-format remotion still、frame 30/90 デフォルト
    19	- 各 still を ffprobe で width/height 検証
    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
    21	
    22	前提:
    23	- 対象 SuperMovie project (main.mp4 / node_modules / remotion installed)
    24	- ffprobe / ffmpeg コマンドが PATH に存在 (Phase 3-A 以降 preflight で検証済み)
    25	
    26	Usage:
    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
    28	    python3 scripts/visual_smoke.py --formats youtube,short
    29	    python3 scripts/visual_smoke.py --frames 30,90,180
    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
    31	
    32	Exit code:
    33	    0 = 全 still 出力 + dimension 一致
    34	    2 = 1 件以上 dimension mismatch (regression、render は成功している)
    35	    3 = 実行環境問題 (main.mp4 不在 / node_modules 不在 / remotion still failed /
    36	         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
    37	    4 = 入力 / 設定不正 (videoConfig.ts 不在 or FORMAT 行 regex 不一致 /
    38	         空 formats / 空 frames / 未知 format)
    39	"""
    40	from __future__ import annotations
    41	
    42	import argparse
    43	import json
    44	import re
    45	import shutil
    46	import subprocess
    47	import sys
    48	from pathlib import Path
    49	
    50	PROJ = Path(__file__).resolve().parent.parent
    51	VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
    52	SMOKE_OUT = PROJ / "out" / "visual_smoke"
    53	COMPOSITION_ID = "MainVideo"
    54	MAIN_VIDEO = PROJ / "public" / "main.mp4"
    55	REMOTION_BIN = PROJ / "node_modules" / ".bin" / "remotion"
    56	
    57	FORMAT_DIMS = {
    58	    "youtube": (1920, 1080),
    59	    "short": (1080, 1920),
    60	    "square": (1080, 1080),
    61	}
    62	FORMAT_LINE_RE = re.compile(
    63	    r"^(export const FORMAT: VideoFormat = ')(youtube|short|square)(';)$",
    64	    re.MULTILINE,
    65	)
    66	
    67	
    68	def patch_format(content: str, fmt: str) -> str:
    69	    """videoConfig.ts の FORMAT 行を fmt に書き換える。
    70	
    71	    一致 0 件で ValueError、複数一致でも先頭1件のみ書換 (Anchored multi-line)。
    72	    """
    73	    if not FORMAT_LINE_RE.search(content):
    74	        raise ValueError(
    75	            f"FORMAT 行が videoConfig.ts に見つからない: pattern={FORMAT_LINE_RE.pattern}"
    76	        )
    77	    return FORMAT_LINE_RE.sub(rf"\g<1>{fmt}\g<3>", content, count=1)
    78	
    79	
    80	def probe_dim(png: Path) -> tuple[int, int]:
    81	    """ffprobe で PNG の width × height を取得。"""
    82	    out = subprocess.check_output(
    83	        [
    84	            "ffprobe",
    85	            "-v",
    86	            "error",
    87	            "-select_streams",
    88	            "v:0",
    89	            "-show_entries",
    90	            "stream=width,height",
    91	            "-of",
    92	            "json",
    93	            str(png),
    94	        ],
    95	        text=True,
    96	    )
    97	    info = json.loads(out)
    98	    s = info["streams"][0]
    99	    return int(s["width"]), int(s["height"])
   100	
   101	
   102	def render_still(project: Path, frame: int, png_out: Path) -> None:
   103	    """`npx remotion still` で 1 frame の PNG 出力。"""
   104	    png_out.parent.mkdir(parents=True, exist_ok=True)
   105	    subprocess.check_call(
   106	        [
   107	            "npx",
   108	            "--no-install",
   109	            "remotion",
   110	            "still",
   111	            COMPOSITION_ID,
   112	            str(png_out),
   113	            "--frame",
   114	            str(frame),
   115	        ],
   116	        cwd=str(project),
   117	    )
   118	
   119	
   120	def has_drawtext_filter() -> bool:

 succeeded in 0ms:
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
   291	        for fmt in formats:
   292	            if env_error:
   293	                break
   294	            try:
   295	                patched = patch_format(original, fmt)
   296	            except ValueError as e:
   297	                print(f"ERROR: {e}", file=sys.stderr)
   298	                return 4
   299	            VIDEO_CONFIG.write_text(patched, encoding="utf-8")
   300	            print(f"\n[smoke] format={fmt} に切替て still を出力します")
   301	            for frame in frames:
   302	                png = out_dir / f"smoke_{fmt}_f{frame:04d}.png"
   303	                try:
   304	                    render_still(PROJ, frame, png)
   305	                except subprocess.CalledProcessError as e:
   306	                    # P1 #1: render 失敗は環境問題 (exit 3) として即終了
   307	                    print(
   308	                        f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
   309	                        file=sys.stderr,
   310	                    )
   311	                    env_error = "still_failed"
   312	                    results.append(
   313	                        {"format": fmt, "frame": frame, "ok": False, "error": "still_failed"}
   314	                    )
   315	                    break
   316	                try:
   317	                    w, h = probe_dim(png)
   318	                except subprocess.CalledProcessError as e:
   319	                    print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
   320	                    env_error = "probe_failed"
   321	                    results.append(
   322	                        {"format": fmt, "frame": frame, "ok": False, "error": "probe_failed"}
   323	                    )
   324	                    break
   325	                expected = FORMAT_DIMS[fmt]
   326	                ok = (w, h) == expected
   327	                if not ok:
   328	                    mismatched += 1
   329	                results.append(
   330	                    {
   331	                        "format": fmt,
   332	                        "frame": frame,
   333	                        "ok": ok,
   334	                        "expected": list(expected),
   335	                        "actual": [w, h],
   336	                        "png": str(png),
   337	                    }
   338	                )
   339	                stills.append(png)
   340	                marker = "OK" if ok else "MISMATCH"
   341	                print(
   342	                    f"  [{marker}] {png.name}: expected={expected[0]}x{expected[1]}, "
   343	                    f"actual={w}x{h}"
   344	                )
   345	    finally:
   346	        VIDEO_CONFIG.write_text(original, encoding="utf-8")
   347	        print(f"\n[smoke] videoConfig.ts を原本に restore しました")
   348	
   349	    grid_status = "skipped"
   350	    grid_error: str | None = None
   351	    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
   352	    if not args.no_grid and full_matrix:
   353	        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
   354	        grid_out = out_dir / "grid.png"
   355	        try:
   356	            make_grid(stills, grid_out, formats, frames, label=grid_label)
   357	            print(f"\n[smoke] grid: {grid_out}")
   358	            grid_status = "ok"
   359	        except subprocess.CalledProcessError as e:
   360	            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)

hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "git show 85e824e -- template/scripts/visual_smoke.py --stat --patch | sed -n '1,220p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-RjHnTycg' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Tmox269o' (errno=Operation not permitted)
commit 85e824e744d4717de6494cc874e0ba818b456444
Author: 増田朗空 <rokumasuda@RokuMacBook-Pro-M5.local>
Date:   Mon May 4 21:32:22 2026 +0900

    fix(visual-smoke): vstack 幅不一致を letterbox で解消 (Phase 3-G new P1)
    
    Codex Phase 3-G fix 再 review investigation (CODEX_REVIEW_PHASE3G_FIX_20260504T212554)
    で実証された新規 P1 を fix。
    
    問題:
    旧 grid logic は各 cell を `scale=-2:360` で height=360 統一していたが、
    youtube (16:9) → w=640 / short (9:16) → w=202 / square (1:1) → w=360 と
    row 幅が format ごとに異なる。hstack で row 内 width 揃いは OK だが、vstack
    は input 0 の width に他 row が一致しないと exited 234 (Invalid argument) で
    落ちる (ffmpeg 公式 vstack docs と investigation log で確認)。
    
    修正:
    各 cell を CELL_W × CELL_H = 480 × 360 の固定 box に letterbox (scale +
    force_original_aspect_ratio=decrease + pad で aspect 維持して中央配置、余白黒)。
    全 cell が均一 dimension になるため hstack/vstack 両方が安全に動く。
    
    検証 (Bash 実測):
    ffmpeg lavfi で 1920x1080 / 1080x1920 / 1080x1080 の 3 input を生成し、
    新 filter_complex (letterbox → vstack) で合成 → 480x1080 PNG 正常出力
    (ffprobe 確認 width=480 height=1080)。
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

diff --git a/template/scripts/visual_smoke.py b/template/scripts/visual_smoke.py
index baf5094..32ed199 100644
--- a/template/scripts/visual_smoke.py
+++ b/template/scripts/visual_smoke.py
@@ -135,6 +135,10 @@ def has_drawtext_filter() -> bool:
     return False
 
 
+CELL_W = 480
+CELL_H = 360
+
+
 def make_grid(
     stills: list[Path],
     grid_out: Path,
@@ -148,6 +152,11 @@ def make_grid(
     (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
     label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
     (drawtext filter 不在環境向け、Codex P1 #2 反映)。
+
+    各 cell を CELL_W × CELL_H の固定 box に letterbox (scale + pad) で統一する。
+    youtube/short/square は aspect 比が異なるため、共通 height だけだと row ごとに
+    width が変わり vstack が input width 不一致で reject する (Codex Phase 3-G fix
+    再 review investigation で実証、新規 P1)。
     """
     if not stills:
         return
@@ -159,19 +168,23 @@ def make_grid(
     n_fmt = len(formats)
     n_frm = len(frames)
     filter_parts: list[str] = []
-    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
+    # 各 cell を CELL_W×CELL_H box に letterbox (aspect 維持で fit、余白は黒)
     for i, s in enumerate(stills):
         fmt = formats[i // n_frm]
         frm = frames[i % n_frm]
+        scale_pad = (
+            f"scale={CELL_W}:{CELL_H}:force_original_aspect_ratio=decrease,"
+            f"pad={CELL_W}:{CELL_H}:(ow-iw)/2:(oh-ih)/2:color=black"
+        )
         if label:
             txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
             filter_parts.append(
-                f"[{i}:v]scale=-2:360,"
+                f"[{i}:v]{scale_pad},"
                 f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
                 f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
             )
         else:
-            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
+            filter_parts.append(f"[{i}:v]{scale_pad}[c{i}]")
 
     # 各 format 行の hstack
     row_labels: list[str] = []

exec
/bin/zsh -lc "git show roku/phase3g-visual-smoke:template/scripts/visual_smoke.py | nl -ba | sed -n '135,215p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-gn2rDeCo' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-hid5hFxH' (errno=Operation not permitted)
   135	    return False
   136	
   137	
   138	def make_grid(
   139	    stills: list[Path],
   140	    grid_out: Path,
   141	    formats: list[str],
   142	    frames: list[int],
   143	    label: bool,
   144	) -> None:
   145	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
   146	
   147	    呼び出し側で full matrix (len(stills) == n_fmt * n_frm) を保証すること
   148	    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
   149	    label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
   150	    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
   151	    """
   152	    if not stills:
   153	        return
   154	    grid_out.parent.mkdir(parents=True, exist_ok=True)
   155	    inputs: list[str] = []
   156	    for s in stills:
   157	        inputs.extend(["-i", str(s)])
   158	
   159	    n_fmt = len(formats)
   160	    n_frm = len(frames)
   161	    filter_parts: list[str] = []
   162	    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
   163	    for i, s in enumerate(stills):
   164	        fmt = formats[i // n_frm]
   165	        frm = frames[i % n_frm]
   166	        if label:
   167	            txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
   168	            filter_parts.append(
   169	                f"[{i}:v]scale=-2:360,"
   170	                f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
   171	                f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
   172	            )
   173	        else:
   174	            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
   175	
   176	    # 各 format 行の hstack
   177	    row_labels: list[str] = []
   178	    for r in range(n_fmt):
   179	        row_in = "".join(f"[c{r * n_frm + c}]" for c in range(n_frm))
   180	        row_label = f"row{r}"
   181	        if n_frm == 1:
   182	            filter_parts.append(f"{row_in}copy[{row_label}]")
   183	        else:
   184	            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
   185	        row_labels.append(f"[{row_label}]")
   186	
   187	    # vstack
   188	    if n_fmt == 1:
   189	        filter_parts.append(f"{row_labels[0]}copy[grid]")
   190	    else:
   191	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
   192	
   193	    cmd = (
   194	        ["ffmpeg", "-y"]
   195	        + inputs
   196	        + [
   197	            "-filter_complex",
   198	            ";".join(filter_parts),
   199	            "-map",
   200	            "[grid]",
   201	            "-frames:v",
   202	            "1",
   203	            str(grid_out),
   204	        ]
   205	    )
   206	    subprocess.check_call(cmd)
   207	
   208	
   209	def cli() -> int:
   210	    ap = argparse.ArgumentParser()
   211	    ap.add_argument(
   212	        "--formats",
   213	        default="youtube,short,square",
   214	        help="検証対象 format (カンマ区切り、default 全 3 種)",
   215	    )

codex
**結論: merge 前に P1 は潰すべきです。** P0 は出していません。P1×2 / P2×4 / P3×3。

| Sev | 指摘 | 修正案 / Effort / 自走 |
|---|---|---|
| P1 | **missing chunk + legacy wav で無音化する**。`NarrationAudio` は `narrationData.length > 0` かつ chunk 不足で即 `null` を返す一方、`MainVideo` は `narration.wav` があるだけで base を mute するため、chunk 不足 + legacy 存在時に narration も base 音声も消える（[NarrationAudio.tsx:35](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:35), [NarrationAudio.tsx:39](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:39), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25), [MainVideo.tsx:33](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:33)）。 | `getNarrationMode()` を共通化し、`chunks complete -> chunks / legacy exists -> legacy / none` に統一。Effort S / 自走可 |
| P1 | **all-or-nothing が legacy `narration.wav` を対象外にしている**。partial failure 時は chunk と `narrationData.ts` だけ消すが、既存 `public/narration.wav` は残るので、失敗後に古い narration が再生され得る（[voicevox_narration.py:318](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:318), [voicevox_narration.py:324](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:324), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25)）。 | staging dir に全生成して最後に atomic swap、または失敗時に legacy wav も消す。推奨は staging。Effort M / 自走可 |
| P2 | **`narrationData.ts` 書き換えが atomic ではない**。コメントは “atomic” だが、実装は `write_text()` 直書きで、SIGINT/書き込み失敗時に TS が途中破損し得る（[voicevox_narration.py:141](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:141), [voicevox_narration.py:181](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:181), [voicevox_narration.py:213](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:213), [voicevox_narration.py:333](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:333)）。 | temp file + `os.replace()`。meta も同様。Effort S / 自走可 |
| P2 | **`read_render_fps()` が malformed config で落ちる**。`cfg.get("source", {}).get(...)` は `source: null` / string で `AttributeError` になる（[voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153), `python3 -c` Bash実測）。 | dict 型を段階検証。`--fps <= 0` も reject。Effort S / 自走可 |
| P2 | **FPS source が Remotion 実値と完全同期ではない**。render は `videoConfig.FPS` を使うが、script は `project-config.json` を読むため、両者がズレると Sequence duration がズレる（[Root.tsx:13](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [Root.tsx:14](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts:9](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153)）。 | `src/videoConfig.ts` から FPS を読む小 helper、または `--fps` 必須化。Effort S-M / 自走可 |
| P2 | **WAV header 信頼が狭い**。Python `wave` は PCM WAV のみ対象で、unsupported WAV/非WAVなら `wave.Error` 系で落ちる（Python docs: https://docs.python.org/3/library/wave.html）。現実装は `measure_duration_seconds()` / `concat_wavs()` で捕捉していない（[voicevox_narration.py:100](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:100), [voicevox_narration.py:117](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:117)）。VOICEVOX の通常 `/synthesis` は `audio.wav` 例示なので主経路は妥当（https://github.com/VOICEVOX/voicevox_engine）。 | `wave.Error` を catch して exit 6 相当に rollback。Effort S / 自走可 |
| P3 | `MainVideo` の `startsWith("narration/chunk_")` は redundant かつ `chunk_meta.json` にも当たる。`every(seg.file)` が実質判定済み（[MainVideo.tsx:27](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:27), [MainVideo.tsx:31](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:31)）。 | `.endsWith(".wav")` 付きにするか削除。Effort XS / 自走可 |
| P3 | `getStaticFiles().some()` が `MainVideo` と `NarrationAudio` で毎 render 重複する。Remotion docs 上 `getStaticFiles()` は Studio/render 中のみ有効（https://www.remotion.dev/docs/getstaticfiles）。 | `Set(staticFiles.map(f => f.name))` と mode helper 共有。Effort S / 自走可 |
| P3 | skill の連携マップが Phase 3-H 実装に追従していない。本文は chunk/data 経路だが、map は `public/narration.wav` と単一 `<Audio>` の旧説明のまま（[SKILL.md:131](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:131), [SKILL.md:137](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:137), [SKILL.md:139](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:139)）。 | map を `narrationData.ts + chunk_NNN.wav + legacy fallback` に更新。Effort XS / 自走可 |

補足: `--keep-chunks` は current tree では参照なし、base branch では skill と script にだけ存在（`rg`/`git grep` Bash実測）。外部 CLI 互換だけ見るなら hidden no-op alias を残すのが安全です。

Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。
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
262,328
**結論: merge 前に P1 は潰すべきです。** P0 は出していません。P1×2 / P2×4 / P3×3。

| Sev | 指摘 | 修正案 / Effort / 自走 |
|---|---|---|
| P1 | **missing chunk + legacy wav で無音化する**。`NarrationAudio` は `narrationData.length > 0` かつ chunk 不足で即 `null` を返す一方、`MainVideo` は `narration.wav` があるだけで base を mute するため、chunk 不足 + legacy 存在時に narration も base 音声も消える（[NarrationAudio.tsx:35](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:35), [NarrationAudio.tsx:39](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:39), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25), [MainVideo.tsx:33](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:33)）。 | `getNarrationMode()` を共通化し、`chunks complete -> chunks / legacy exists -> legacy / none` に統一。Effort S / 自走可 |
| P1 | **all-or-nothing が legacy `narration.wav` を対象外にしている**。partial failure 時は chunk と `narrationData.ts` だけ消すが、既存 `public/narration.wav` は残るので、失敗後に古い narration が再生され得る（[voicevox_narration.py:318](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:318), [voicevox_narration.py:324](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:324), [MainVideo.tsx:25](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:25)）。 | staging dir に全生成して最後に atomic swap、または失敗時に legacy wav も消す。推奨は staging。Effort M / 自走可 |
| P2 | **`narrationData.ts` 書き換えが atomic ではない**。コメントは “atomic” だが、実装は `write_text()` 直書きで、SIGINT/書き込み失敗時に TS が途中破損し得る（[voicevox_narration.py:141](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:141), [voicevox_narration.py:181](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:181), [voicevox_narration.py:213](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:213), [voicevox_narration.py:333](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:333)）。 | temp file + `os.replace()`。meta も同様。Effort S / 自走可 |
| P2 | **`read_render_fps()` が malformed config で落ちる**。`cfg.get("source", {}).get(...)` は `source: null` / string で `AttributeError` になる（[voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153), `python3 -c` Bash実測）。 | dict 型を段階検証。`--fps <= 0` も reject。Effort S / 自走可 |
| P2 | **FPS source が Remotion 実値と完全同期ではない**。render は `videoConfig.FPS` を使うが、script は `project-config.json` を読むため、両者がズレると Sequence duration がズレる（[Root.tsx:13](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:13), [Root.tsx:14](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Root.tsx:14), [videoConfig.ts:9](/Users/rokumasuda/.claude/plugins/supermovie/template/src/videoConfig.ts:9), [voicevox_narration.py:153](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:153)）。 | `src/videoConfig.ts` から FPS を読む小 helper、または `--fps` 必須化。Effort S-M / 自走可 |
| P2 | **WAV header 信頼が狭い**。Python `wave` は PCM WAV のみ対象で、unsupported WAV/非WAVなら `wave.Error` 系で落ちる（Python docs: https://docs.python.org/3/library/wave.html）。現実装は `measure_duration_seconds()` / `concat_wavs()` で捕捉していない（[voicevox_narration.py:100](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:100), [voicevox_narration.py:117](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:117)）。VOICEVOX の通常 `/synthesis` は `audio.wav` 例示なので主経路は妥当（https://github.com/VOICEVOX/voicevox_engine）。 | `wave.Error` を catch して exit 6 相当に rollback。Effort S / 自走可 |
| P3 | `MainVideo` の `startsWith("narration/chunk_")` は redundant かつ `chunk_meta.json` にも当たる。`every(seg.file)` が実質判定済み（[MainVideo.tsx:27](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:27), [MainVideo.tsx:31](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:31)）。 | `.endsWith(".wav")` 付きにするか削除。Effort XS / 自走可 |
| P3 | `getStaticFiles().some()` が `MainVideo` と `NarrationAudio` で毎 render 重複する。Remotion docs 上 `getStaticFiles()` は Studio/render 中のみ有効（https://www.remotion.dev/docs/getstaticfiles）。 | `Set(staticFiles.map(f => f.name))` と mode helper 共有。Effort S / 自走可 |
| P3 | skill の連携マップが Phase 3-H 実装に追従していない。本文は chunk/data 経路だが、map は `public/narration.wav` と単一 `<Audio>` の旧説明のまま（[SKILL.md:131](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:131), [SKILL.md:137](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:137), [SKILL.md:139](/Users/rokumasuda/.claude/plugins/supermovie/skills/supermovie-narration/SKILL.md:139)）。 | map を `narrationData.ts + chunk_NNN.wav + legacy fallback` に更新。Effort XS / 自走可 |

補足: `--keep-chunks` は current tree では参照なし、base branch では skill と script にだけ存在（`rg`/`git grep` Bash実測）。外部 CLI 互換だけ見るなら hidden no-op alias を残すのが安全です。

Phase 3-G vstack fix は、旧 `scale=-2:360` が format ごとに幅を変えていたのに対し、現 commit は `CELL_W/CELL_H` + `scale,pad` で cell サイズを固定しており、vstack P1 の方向性は妥当です（[visual_smoke.py:138](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:138), [visual_smoke.py:175](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:175), base比較は `git show roku/phase3g-visual-smoke:...` Bash実測）。ただし 480×360 は目視レビュー用には小さく、short は実コンテンツ幅が約202px相当になるため、`--cell-width/--cell-height` 化は P3 で入れていいです。

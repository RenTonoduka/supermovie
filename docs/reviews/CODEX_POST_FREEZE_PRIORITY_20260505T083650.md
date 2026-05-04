結論: release branch に runtime hardening を積み増すなら「全部スキップで復帰待ち」が筋です。根拠は final verdict が「P0/P1/P2 なし、止めてよい」と明記し、残候補も release blocker ではないと整理しているためです（`docs/reviews/CODEX_REVIEW_PHASE3V_FINAL_20260505T064250.md:4985`, `:4992-4997`）。handoff でも technical freeze として A 系は post-freeze hardening 扱いです（`/Users/rokumasuda/0_Daily-Workspace/handoff_2026-05-05_supermovie-phase3-release-ready.md:75`）。

ただし、復帰前に「post-freeze backlog」として自走着手するなら優先順はこれです。

1. **空の未追跡 priority artifact を処理して worktree clean gate を復旧**
   目的: この作業木では `docs/reviews/CODEX_POST_FREEZE_PRIORITY_20260505T083650.md` が 0 byte の未追跡ファイルで、`check_release_ready.sh` は worktree gate で exit 3 になります（Bash 実測、`scripts/check_release_ready.sh:57-62`）。
   Effort: S / 6 gate 影響: 低ではなく復旧必須 / 推奨理由: gate 前提を戻す作業。
   着手判断: 即着手で良い。

2. **PHASE3_RELEASE_NOTE / PHASE3_PROGRESS の final-state 表記を c25767a に揃える**
   目的: 実 HEAD は `c25767a` ですが、release note 先頭は `ad15fd2` / 53 commit 表記です（Bash 実測、`docs/PHASE3_RELEASE_NOTE.md:3-7`）。handoff は `c25767a` / 57 commit 前提です（handoff `:5`, `:9`）。
   Effort: S / 6 gate 影響: 低 / 推奨理由: PR 文面・handoff の読み違い防止。release blocker ではない。
   着手判断: 即着手で良い。

3. **eslint no-explicit-any を warn から error に上げて any-free contract を固定**
   目的: release note は `as any` escape ゼロを主張し、後続候補にも error 化が残っています（`docs/PHASE3_RELEASE_NOTE.md:82`, `:115-118`）。現 config はまだ warn です（`template/eslint.config.mjs:6-13`）。`template/src` の `any` はコメント以外ヒットせず、`npm run lint` は exit 0 でした（Bash 実測）。
   Effort: S / 6 gate 影響: 低 / 推奨理由: 既に達成した品質を機械 gate に固定できる。
   着手判断: 即着手で良い。

4. **timeline.py / test_timeline_integration.py の境界 edge case を追加**
   目的: release note に edge case 強化候補があります（`docs/PHASE3_RELEASE_NOTE.md:111`）。既存 test は no-cut / cut gap の基本を押さえています（`template/scripts/test_timeline_integration.py:137-152`）。
   Effort: M / 6 gate 影響: 低 / 推奨理由: runtime を触らず smoke の防御範囲を広げられる。
   着手判断: test-only なら即着手で良い。挙動変更が必要になったら Codex consult。

5. **voicevox_narration.py の sentinel signal file hot-reload 厳密化**
   目的: release note の候補です（`docs/PHASE3_RELEASE_NOTE.md:112-113`）。現状は write order race を mitigated していますが（`template/scripts/voicevox_narration.py:595-601`）、`narrationData.ts` 自体の HMR は Remotion/Vite 依存とコメントされています（`template/src/Narration/useNarrationMode.ts:31-35`）。
   Effort: M/L / 6 gate 影響: 中 / 推奨理由: Studio UX hardening だが release blocker ではない（final verdict `:4992-4994`）。
   着手判断: 先に Codex consult 必要。

除外: `regen_phase3_progress.sh` の Phase 別 deliverable / 残候補 auto-gen 拡張は今回の優先対象外。script 自体が手動 section を触らない制約を持ち（`scripts/regen_phase3_progress.sh:23-26`）、final verdict も「commit message 推測を増やすだけ」と評価しています（`docs/reviews/CODEX_REVIEW_PHASE3V_FINAL_20260505T064250.md:4992-4994`）。

検証 caveat: この read-only sandbox では Python smoke と Vitest が temp/cache 書き込み EPERM で再実行できませんでした（Bash 実測）。実装側で gate を走らせ、Codex read-only は diff と実行ログを review する形が現実的です。

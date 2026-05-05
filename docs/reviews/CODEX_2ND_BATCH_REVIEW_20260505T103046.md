**Findings**

P0 (Blocker): 指摘なし。

P1 (High): `--json-log` は engine unavailable の正常 skip path で JSON を出しません。flag は「末尾に純 JSON」と説明されていますが、`check_engine()` failure は `return 0` で先に抜け、JSON emit は成功末尾だけです (`template/scripts/voicevox_narration.py:520`, `:528`, `:760`)。`python3 template/scripts/voicevox_narration.py --json-log` も exit 0 で INFO のみでした (Bash 実測)。test は engine OK の happy path だけです (`template/scripts/test_timeline_integration.py:1598`, `:1605`, `:1617`)。修正案: 全 return path に `status/exit_code` 付き JSON emit を集約。Effort: S。

P2 (Medium): P1 doc ledger の `PHASE3_PROGRESS` 本文が stale です。priority は `PHASE3_RELEASE_NOTE / PHASE3_PROGRESS` の test count 整合を求めています (`docs/reviews/CODEX_NEXT_PRIORITY_20260505T102232.md:5`)。release note は 27/27・22/22 ですが (`docs/PHASE3_RELEASE_NOTE.md:17`)、progress は 23 test のままです (`docs/PHASE3_PROGRESS.md:237`)。実 harness は 32 test 登録です (`template/scripts/test_timeline_integration.py:1715`)。修正案: Test gates 節を 32 test / React 22 に更新、または auto-gen 対象外と明記。Effort: S。

P2 (Medium): P4 fixture が stated scope より浅いです。priority は `patch_format / restore / mismatch summary` を要求しています (`docs/reviews/CODEX_NEXT_PRIORITY_20260505T102232.md:20`)。追加 test は `patch_format` と `FORMAT_DIMS` のみで (`template/scripts/test_timeline_integration.py:1644`)、`finally` restore と summary JSON は未検証です (`template/scripts/visual_smoke.py:345`, `:365`)。修正案: temp `videoConfig.ts` と monkeypatch で `cli()` を mock 実行し、restore と `mismatched`/exit 2 を assert。Effort: M。

Gate: `regen --verify` は diff 1 pass、`npm run lint` は exit 0。`check_release_ready.sh` は untracked review artifact で worktree gate fail (`scripts/check_release_ready.sh:57`, Bash 実測)。Python/React rerun は read-only temp EPERM で未証明。

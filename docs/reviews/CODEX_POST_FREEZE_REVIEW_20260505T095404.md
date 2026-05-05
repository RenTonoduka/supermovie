対象 range は 9 commits でした（Bash 実測）。指摘は以下です。

**P1 High**  
`check_release_ready.sh` は untracked を exit 3 にする設計ですが、現作業木に `docs/reviews/CODEX_POST_FREEZE_REVIEW_20260505T095404.md` が未追跡で残り、6 gate は `head: a85bdb1` で exit 3 でした（[scripts/check_release_ready.sh](/Users/rokumasuda/.claude/plugins/supermovie/scripts/check_release_ready.sh:57)、Bash 実測）。  
詳細: commit 差分外の作業木問題だが、照合対象「6 gate 維持」は現状満たしていません。  
修正案: artifact を commit 対象に含めるか削除してから `bash scripts/check_release_ready.sh` を再実行。  
Effort: S

**P2 Medium**  
`FUTURE_FEATURES_REQUIREMENTS_v0.md` は fill-in 後なのに、冒頭で「Codex 補完 pending」かつ `[要 Codex 補完]` を v0.1 で埋める方針のままです（[docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md:5)、[同](/Users/rokumasuda/.claude/plugins/supermovie/docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md:9)）。一方で §4 は Codex consult で全セル一次情報照合済みと書いており（[同](/Users/rokumasuda/.claude/plugins/supermovie/docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md:120)）、§8 は補完済み扱いです（[同](/Users/rokumasuda/.claude/plugins/supermovie/docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md:210)）。  
詳細: v0 doc の状態表示が矛盾し、fill-in 反映精度を落としています。  
修正案: pending 文言と残存 `[要 Codex 補完]` を「§4/§7 は補完済み、§2/§5 のコスト/法務は未補完」などに分離。`commit 9c1c3f0 系列` も実 commit `794e3bc` に直す（[docs/PHASE3_PROGRESS.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/PHASE3_PROGRESS.md:143)）。  
Effort: S/M

**P3 Low**  
`PHASE3_PROGRESS.md` の Test gates は `test:timeline` を 20 cases / 最新 `aacc5dc` と説明していますが（[docs/PHASE3_PROGRESS.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/PHASE3_PROGRESS.md:224)）、実際の `main()` は 23 tests を列挙しています（[template/scripts/test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:1197)）。  
修正案: 23 cases、post-freeze edge cases 3 件追加に更新。  
Effort: S

補足: `regen --verify` は exit 0、`npm run lint` は exit 0 でした（Bash 実測）。Python smoke と React test は read-only sandbox の temp/cache EPERM で再実行不能でした（Bash 実測）。

**Review**

P0/P1: 指摘なし。`--json-log` は default off で追加され、helper も flag なしでは no-op です（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:168), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:177)）。dry-run は既存単一 JSON のままです（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:297)）。

P2: [check_release_ready.sh](/Users/rokumasuda/.claude/plugins/supermovie/scripts/check_release_ready.sh:57)  
詳細: 現 worktree では 6 gate を green として再現できません。`check_release_ready.sh` は untracked file で exit 3 になり、`docs/reviews/CODEX_P3_SLIDE_PLAN_REVIEW_20260505T110504.md` が検出されました（Bash 実測）。  
修正案: review artifact を commit するか除外し、clean worktree で `check_release_ready.sh` を再実行。  
Effort: S

P3: [test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:1108)  
詳細: 新規 test は success / api_key_skipped の JSON tail だけを見ています（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:1161)）。Codex §4 の「既存 stdout 維持」観点では、`wrote:` / `slides:` の human stdout が残ることも assert した方が堅いです（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:371)）。  
修正案: success case で `lines[-3]` / `lines[-2]` を assert。flag なし success で JSON 行が増えないことも追加。  
Effort: S

P3: [PHASE3_PROGRESS.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/PHASE3_PROGRESS.md:249)  
詳細: docs は `test:timeline` を 35 test と書いていますが、現 test list は 43 件です（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:2407), Bash 実測）。`test = lint + test:timeline` という記述も、package は React test まで含みます（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:41)）。  
修正案: regen 対象の gate summary も現物から生成。  
Effort: S

補足: `regen --verify` は drift 1 で exit 0、`npm run lint` は exit 0 でした（Bash 実測）。Python/React は read-only sandbox の temp/cache EPERM で完全再実行不可でした（Bash 実測）。

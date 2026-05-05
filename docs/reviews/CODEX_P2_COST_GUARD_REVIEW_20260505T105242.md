P0: 指摘なし。

P1: [template/scripts/generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:161)  
詳細: design は「通常実行では API key 未設定 skip を先に維持」としているのに、実装は cost guard env/arg 解決を API key skip より前に実行しています（[design](/Users/rokumasuda/.claude/plugins/supermovie/docs/reviews/CODEX_P2_COST_GUARD_DESIGN_20260505T104428.md:21), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:197)）。実測でも `ANTHROPIC_API_KEY` unset + `SUPERMOVIE_MAX_TOKENS=bad` が skip 0 ではなく return 4 になります（Bash 実測）。既存 no-key skip 互換の破壊です。  
修正案: `not api_key and not args.dry_run` の skip 判定を cost guard 解決より前へ移動。dry-run のみ API key なしで env/arg validation する。Effort: S

P2: [template/scripts/generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:112)  
詳細: `--rate-input/--rate-output` は decimal `>=0` spec ですが、`type=float` と `v < 0` だけなので `nan` / `inf` が通ります（[design](/Users/rokumasuda/.claude/plugins/supermovie/docs/reviews/CODEX_P2_COST_GUARD_DESIGN_20260505T104428.md:12), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:154), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:131)）。`_resolve_decimal(float("nan"))` と `float("inf")` が non-finite のまま返ることも実測しました（Bash 実測）。  
修正案: `math.isfinite(v)` を必須化し、`Decimal` parser か有限 float のみに制限。`nan/inf` env/CLI の regression test を追加。Effort: S

P3: [template/scripts/generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:167)  
詳細: `--max-input-words` spec は int `>=1` ですが、実装は未記載の `1_000_000` 上限を入れています（[design](/Users/rokumasuda/.claude/plugins/supermovie/docs/reviews/CODEX_P2_COST_GUARD_DESIGN_20260505T104428.md:9), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:169)）。実害は小さいですが design 準拠としてはズレです。  
修正案: 上限を外す、または design に local cap として追記。Effort: S

補足: `regen --verify` は drift 1 で exit 0（Bash 実測）。ただし現 worktree は untracked `docs/reviews/CODEX_P2_COST_GUARD_REVIEW_20260505T105242.md` により composite gate が exit 3（Bash 実測）。Python gate は read-only sandbox で temp dir 作成不能のため 11/40 までしか実行確認できていません（Bash 実測）。

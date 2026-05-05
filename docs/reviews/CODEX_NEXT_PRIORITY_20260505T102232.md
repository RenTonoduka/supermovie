結論: **技術 freeze としては Roku 復帰待ちが本筋**です。根拠は final verdict が「P0/P1/P2 なし」「止めてよい」とし、残候補も release blocker ではないと整理しているためです (`docs/reviews/CODEX_REVIEW_PHASE3V_FINAL_20260505T064250.md:4985`, `:4992-4997`)。handoff も push/PR/merge/e2e を ROKU_BLOCKER に置いています (`/Users/rokumasuda/0_Daily-Workspace/handoff_2026-05-05_supermovie-phase3-release-ready.md:43-55`, `:75`)。

ただし第2弾を積むなら、推奨 priority は以下です。

1. **P1: Doc Ledger Alignment**
   目的: `PHASE3_RELEASE_NOTE` / `PHASE3_PROGRESS` の test count・HEAD・post-freeze addendum を現 HEAD 系に合わせる。release note は `467ceec` / 20 python / 18 React のままです (`docs/PHASE3_RELEASE_NOTE.md:3-8`, `:16-18`)。
   effort: S / 6 gate影響: 低 / 推奨理由: runtime 変更なしで review 誤読を減らせる。
   着手判断: 即。

2. **P2: Cost Guard for `generate_slide_plan.py`**
   目的: `--max-tokens` / input word cap / dry-run cost estimate field / 429分類を追加。現状は API key skip と `max_tokens=4096` 固定です (`template/scripts/generate_slide_plan.py:80-84`, `:128-149`)。
   effort: M / 6 gate影響: 低 / 推奨理由: API 課金系の前段防御になる。価格・rate limit の公開情報は未確認。
   着手判断: 仕様は Codex consult 先行、実装は mock-only なら即。

3. **P3: Structured Script Logging**
   目的: `print` 多用 script に任意 `--json-log` を追加し、既存 stdout は維持。`visual_smoke` は summary JSON あり (`template/scripts/visual_smoke.py:365-383`)。
   effort: M / 6 gate影響: 低 / 推奨理由: gate artifact 化しやすく、Codex review が diff + log schema で検証可能。
   着手判断: 即。

4. **P4: Mocked Visual-Smoke Regression Fixture**
   目的: 実 `main.mp4` なしで `patch_format` / restore / mismatch summary を test 化。実 visual-smoke は main.mp4/node_modules 前提です (`template/scripts/visual_smoke.py:22-24`, `:262-271`)。
   effort: M / 6 gate影響: 低 / 推奨理由: Roku 判断領域の実 e2e に触らず regressions を増やせる。
   着手判断: mock-only は即、実 fixture 同梱は Codex consult 先行。

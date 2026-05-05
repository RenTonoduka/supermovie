# CONTEXT_ANCHOR — SuperMovie Repo (Codex 主・Claude 従)

本 anchor は Roku 2026-05-05 11:38 確定の役割再定義 + 当時の Codex 命令 (CODEX_NEXT_STEP_INSTRUCTION 20260505T114718、artifact 喪失 / 内容は本 anchor §Verified Snapshot 〜 §Codex Review Protocol に反映済) に基づく作業中継 doc。push/PR 前に必ず最新化、Codex review prompt の先頭で本 doc 参照。欠落・stale なら Codex review で P1 扱い。

## Purpose

- **Codex CLI**: 命令 (priority / 設計 / review)
- **Claude Code**: 実装実行者のみ (方針判断禁止、Codex consult 経由)
- **Roku**: リスク領域判断のみ (push/PR/merge/deploy/外部副作用/段取り/モラル/法的/予定内容)

(Roku 発言 2026-05-05 11:38: 「Codex が命令し、あなたがそれに従い実装、そして Codex がレビューです、OK？」)

## Verified Snapshot (作成時点で Bash 実測、push/PR 前に再更新)

| 項目 | 値 (Bash 実測 2026-05-05 12:30) |
|---|---|
| HEAD | `31dd9cc` |
| branch | `roku/phase3j-timeline` |
| main..HEAD | 122 commits |
| roku/phase3i-transcript-alignment..HEAD | 104 commits |
| origin remote | `https://github.com/RenTonoduka/supermovie.git` |
| origin viewerPermission | READ (Roku gh account `blessing1031r-dotcom` は write 権限なし) |
| fork remote | 不在 (`git remote get-url fork` で error: No such remote、Step 6 で `gh repo fork` 後に `git remote add fork` 予定) |
| gh auth status | ✓ Logged in (account: blessing1031r-dotcom、scopes: gist read:org repo workflow) |
| worktree | clean (cleanup commit `e0f5107` で `docs/reviews/**` 38 files + `docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md` を release scope から外し済み、future doc は別 worktree `../supermovie-future-features-v0` の `roku/future-features-v0` branch `72a6ef4` に保全済) |
| 6 gate composite | ALL PASS (head 1bc6bab → cleanup `e0f5107` で diff は docs only、composite gate 影響なし、Step 5 で再検証) |

## Roku Authorized Decisions (2026-05-05 user prompt 確定)

Roku 「OK、推奨から進めて」(11:46 user prompt) で以下 5 項目の Codex 推奨を一括採用:

| # | 項目 | Codex 推奨 (採用済み) |
|---|---|---|
| 1 | push 戦略 | **fork → blessing1031r-dotcom → upstream PR** (Option A) |
| 2 | squash 範囲 | raw `docs/reviews` + `future doc` を release branch から **外す** |
| 3 | release note refresh | RELEASE_NOTE HEAD/commit count を **実測値で更新** |
| 4 | 実 e2e | fork CI 前に **local visual-smoke / render** (Roku 環境 main.mp4 fixture 必要) |
| 5 | future v0 doc | **別 PR** で切り出し (`roku/future-features-v0` branch、別途) |

## Release PR Scope (本 PR `roku/phase3j-timeline` の最終 diff target)

**Include** (release tree に含める):
- `template/scripts/` 配下全 (timeline.py / voicevox_narration.py / build_slide_data.py / build_telop_data.py / generate_slide_plan.py / visual_smoke.py / preflight_video.py / budoux_split.mjs / compare_telop_split.py / test_timeline_integration.py)
- `template/src/` 配下全 (Narration / Slides / InsertImage / Title / SoundEffects / テロップテンプレート / メインテロップ / 強調テロップ / ネガティブテロップ / MainVideo.tsx / Root.tsx / videoConfig.ts / index.ts / index.css)
- `template/package.json` / `template/eslint.config.mjs` / `template/vitest.config.ts` / `template/vitest.setup.ts` / `template/tsconfig.json` / `template/remotion.config.ts`
- `scripts/check_release_ready.sh` / `scripts/regen_phase3_progress.sh`
- `docs/PHASE3_PROGRESS.md` / `docs/PHASE3_RELEASE_NOTE.md`
- `CONTEXT_ANCHOR.md` (本 doc)
- `.gitignore`
- `skills/` 配下全 + plugin manifest (`.claude-plugin/plugin.json`)

**Exclude** (release tree から外す、Codex 命令 §C / D):
- `docs/reviews/**` (37+ tracked files / 155,397+ lines、review artifact noise)
- `docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md` (別 PR で出す、release delta と将来構想の混在防止)

`origin/main` 側には上記 exclude path が存在しないため、`git rm` で release branch から削除すれば final diff から消える (Codex 命令 §B 注記)。

## Required Gates (push/PR 前に Roku machine で実行必須、Codex 命令 §A)

```bash
# 1. self-driveable composite gate (Claude 自走 OK)
bash scripts/check_release_ready.sh                 # ALL PASS 必須

# 2. 実 project e2e (Roku 環境必要、main.mp4 fixture)
cd template
npm run test:visual-smoke                           # 3 format × 2 frame still + dimension regression
npm run render                                       # 実 render 1 周

# 3. final worktree clean check
git status --short                                   # 空必須
```

`visual-smoke` / `render` は composite script の対象外 (`scripts/check_release_ready.sh:30-31`、`template/package.json:34-40`)、Roku 環境で main.mp4 fixture を持つ実 project から実行。

## External Actions (権限分類)

| action | 実行者 | 理由 |
|---|---|---|
| `gh repo fork RenTonoduka/supermovie --clone=false --remote=false` | **Claude 自走可** (Roku 「OK、推奨から進めて」授権済) | 自分の account への fork、外部副作用なし |
| `git remote add fork https://github.com/blessing1031r-dotcom/supermovie.git` | Claude 自走可 | local 設定 |
| `git push -u fork roku/phase3j-timeline` | Claude 自走可 (auth scope `repo` あり、fork 先は own account) | 自 account への push |
| `gh pr create --repo RenTonoduka/supermovie --head blessing1031r-dotcom:roku/phase3j-timeline --base main --title <X> --body-file <Y>` | Claude 自走可 | fork PR 作成 (upstream maintainer = RenTonoduka が review) |
| PR review / merge | **Roku 判断 + RenTonoduka 操作必要** | upstream maintainer 権限、destructive action |
| `git push --force` (any branch) | **Roku 明示授権必要** | history rewrite、destructive |
| remote branch delete (`git push fork :branch`) | **Roku 明示授権必要** | destructive |
| PR close / reopen | **Roku 判断** | upstream PR の段取り |
| repo archive 作成 (raw review artifact 別保管用) | **Roku 判断** | 外部 repo 作成、段取り |
| GitHub re-auth (`gh auth login`) | **Roku 操作必要** (interactive) | Claude bash 経由不可 |
| rollback (`git revert <sha>`) | Claude 自走可 | local 操作 |
| force push rollback | **Roku 明示授権必要** | destructive |

## Codex Review Protocol

Codex review prompt の先頭で必ず本 anchor を参照させる:

```
まず `/CONTEXT_ANCHOR.md` を読み、Verified Snapshot / Release PR Scope / Required Gates / External Actions が現状と整合しているか確認してください。
欠落 / stale なら P1 (High) で指摘し、本 review の他項目より優先して fix を促してください。
```

## 更新責任

- **更新者**: Claude (Codex 命令経由で各 cycle 末に Verified Snapshot を再実測 + Roku Authorized Decisions / Release PR Scope を更新)
- **更新タイミング**: push/PR/merge 直前 + 各 commit cycle 末
- **gate 化**: 現時点では `check_release_ready.sh` + `git diff --check` + `git status --short` clean で十分 (anchor check の自動化は release scope 外、後続 PR で検討)

## Related Files

- 元 Codex 命令: CODEX_NEXT_STEP_INSTRUCTION 20260505T114718 (artifact 喪失、内容は本 anchor に反映済)
- 元 Codex full review: CODEX_FULL_SESSION_REVIEW 20260505T113913 (cleanup commit `e0f5107` で release branch から外し済み、commit history で参照可)
- セッション handoff: `/Users/rokumasuda/0_Daily-Workspace/handoff_2026-05-05_supermovie-codex-pivot-overage.md`
- Memory 運用ルール: `~/.claude/projects/-Users-rokumasuda/memory/feedback_codex_master_claude_implementer.md`

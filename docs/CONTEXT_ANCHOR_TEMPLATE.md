# CONTEXT_ANCHOR — {{PROJECT_NAME}} Repo (Codex 主・Claude 従)

本 anchor は Roku 役割再定義 + Codex 命令に基づく作業中継 doc。push/PR 前に必ず最新化、Codex review prompt の先頭で本 doc 参照。欠落・stale なら Codex review で P1 扱い。

> **Template note**: このファイルは {{}}-style placeholder 入りの汎用 template。新規 phase の release branch にコピーして実値で埋める。Phase 3 で確立した structure を抽象化したもの (元: `~/.claude/plugins/supermovie/CONTEXT_ANCHOR.md` @ commit `8310a4c`、2026-05-05)。

## Purpose

- **Codex CLI**: 命令 (priority / 設計 / review)
- **Claude Code**: 実装実行者のみ (方針判断禁止、Codex consult 経由)
- **Roku**: リスク領域判断のみ (push/PR/merge/deploy/外部副作用/段取り/モラル/法的/予定内容)

(Roku 発言出典: 「{{ROLE_DEFINITION_QUOTE}}」)

## Verified Snapshot (作成時点で Bash 実測、push/PR 前に再更新)

| 項目 | 値 (Bash 実測 {{TIMESTAMP}}) |
|---|---|
| HEAD (source commit) | `{{HEAD}}` (anchor 自身の document commit はこの後ろに 1 件積まれる、§Source commit vs Document commit 規約 参照) |
| branch | `{{BRANCH}}` (`{{FORK_TRACKING_BRANCH}}` を track) |
| main..HEAD | {{MAIN_HEAD_COUNT}} commits |
| `{{ANCESTOR_BRANCH}}..HEAD` | {{ANCESTOR_HEAD_COUNT}} commits |
| origin remote | `{{ORIGIN_REMOTE}}` |
| origin viewerPermission | {{ORIGIN_PERMISSION}} (Roku gh account `{{GH_ACCOUNT}}` の権限) |
| fork remote | `{{FORK_REMOTE}}` (Step 6 で `gh repo fork` + `git remote add fork` 完了済) |
| gh auth status | ✓ Logged in (account: `{{GH_ACCOUNT}}`、scopes: `{{SCOPES}}`、Claude Code 側 {{AUTH_CHECK_COUNT}} 回 valid 確認、Codex `--ephemeral` sandbox 内では token 不可視 = invalid 表示されるが Claude Code 実行環境に影響なし) |
| worktree | clean (or 不在 file の理由を明記) |
| 7 gate composite | ALL PASS at `{{HEAD}}` (env / worktree clean / regen drift 1 / python smoke / lint / React tests / **gate 7 anchor drift = 1 intrinsic OK**、Bash 実測 {{TIMESTAMP}}) |

## Roku Authorized Decisions ({{DATE}} user prompt 確定)

Roku 「{{AUTHORIZATION_QUOTE}}」で以下 {{AUTHORIZED_DECISION_COUNT}} 項目の Codex 推奨を一括採用:

| # | 項目 | Codex 推奨 (採用済み) |
|---|---|---|
| 1 | push 戦略 | (例: fork → 自 account → upstream PR) |
| 2 | squash 範囲 | (例: review artifact / future doc を release branch から外す) |
| 3 | release note refresh | (例: HEAD/commit count を実測値で更新) |
| 4 | 実 e2e | (例: fork CI 前に local visual-smoke / render) |
| 5 | future doc | (例: 別 PR で切り出し、別 branch で保全) |

## Release PR Scope (本 PR の最終 diff target)

**Include** (release tree に含める):
- (Phase 関連の主要 file path を列挙、例 `template/scripts/` 配下全)
- `CONTEXT_ANCHOR.md` (本 doc)
- `docs/PHASE{{N}}_RELEASE_NOTE.md` / `docs/PHASE{{N}}_PROGRESS.md`
- `scripts/check_release_ready.sh` / `scripts/regen_phase{{N}}_progress.sh`

**Exclude** (release tree から外す、Codex 命令注記):
- `docs/reviews/**` (review artifact noise、Roku 別 archive 候補)
- `docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v{{N}}.md` (別 PR で出す、release delta と将来構想の混在防止)

`origin/main` 側に上記 exclude path が存在しないため、`git rm` で release branch から削除すれば final diff から消える。

## Required Gates (Draft PR 開始は composite gate のみで可、merge 前に Roku machine で実 e2e 実行必須)

| 区分 | command | 実行環境 | merge blocker か |
|---|---|---|---|
| 1. composite gate (Draft PR 開始 OK) | `{{COMPOSITE_GATE_CMD}}` (例: `bash scripts/check_release_ready.sh`) | Claude 自走 OK、ALL PASS 必須 | yes (gate 不通過なら Draft PR 開始も停止) |
| 2. 実 project e2e (merge blocker) | `{{E2E_COMMANDS}}` (例: `cd template && npm run test:visual-smoke && npm run render`) | Roku 環境必要、`{{FIXTURE_NAME}}` fixture | **yes** (merge 前必須) |
| 3. final worktree clean | `git status --short` | Claude 自走 OK、空必須 | yes |
| 4. (option) `{{ADDITIONAL_GATES}}` | (例: 課金 API smoke、segment-level e2e) | (環境次第) | (Roku 判断) |

composite gate に含まれる sub-gate (`{{COMPOSITE_SUBGATES}}` の例): env / worktree clean / docs drift / unit smoke / lint / type test / **anchor drift (gate 7)**。
e2e は composite script の対象外、Roku 環境で fixture を持つ実 project から実行 (`{{E2E_REASON}}`、例: 実動画 fixture 必要 / 課金 / 専用環境必要)。

## External Actions (権限分類、authorization evidence ベース、safe-by-default)

> **重要**: default 実行者が `Roku 判断` の action は、`{{AUTHORIZATION_QUOTE}}` (Roku 直接発話、§Roku Authorized Decisions に記録) が無い限り Claude 自走不可。template instantiate 直後はまだ授権ゼロなので、新規 phase 開始時はすべて `Roku 判断` で残し、Roku が「{{AUTHORIZATION_QUOTE}} (例: 「OK、推奨から進めて」「fork して」)」と明示した後にのみ Claude 自走可へ昇格。

| action | 副作用 | default 実行者 | Claude 自走可 となる条件 |
|---|---|---|---|
| `gh repo fork {{UPSTREAM_OWNER}}/{{UPSTREAM_NAME}} --clone=false` | external service mutation: 自 account に fork repo 新規作成 | **Roku 判断** | Roku 「{{AUTHORIZATION_QUOTE}}」明示授権 + §Roku Authorized Decisions に記録済 |
| `git remote add fork {{FORK_REMOTE}}` | local 設定のみ (副作用なし) | Claude 自走可 | (常時 OK) |
| `git push -u fork {{BRANCH}}` | external service mutation: 自 account の fork repo に branch + commit 反映、commit history が公開可能になる | **Roku 判断** | 上記 fork 授権が継続有効、auth scope `repo` ある状態、PR 作成前段の準備として明示理解 |
| `gh pr create --repo {{UPSTREAM_OWNER}}/{{UPSTREAM_NAME}} --head {{GH_ACCOUNT}}:{{BRANCH}} --base main --draft --title <X> --body-file <Y>` | external service mutation: upstream repo に Draft PR (maintainer に通知、公開) | **Roku 判断** | Roku 「PR 作成 OK」明示授権、PR title / body 内容を Roku 確認後 (Draft なので merge は別 action) |
| `gh pr create --repo ... --base main` (non-Draft) | external: PR 公開 + merge-ready 主張 | **Roku 明示授権必要** | Draft PR と区別、merge-ready 状態 (gate 7 ALL PASS + e2e 完了) 確認後のみ |
| PR review / merge | external service mutation: upstream main 変更 (squash / merge / rebase いずれも history 改変) | **Roku 判断 + `{{UPSTREAM_OWNER}}` 操作必要** | upstream maintainer 権限、Claude が直接実行不可 |
| `git push --force` (any branch) | destructive: 既存 history rewrite | **Roku 明示授権必要** | 通常回避、必要時 Roku 「force push OK」明示授権 |
| remote branch delete (`git push fork :branch`) | destructive: branch 喪失 | **Roku 明示授権必要** | 通常回避 |
| PR close / reopen / コメント編集 | external: PR state / public comment 変更 | **Roku 判断** | upstream PR の段取り、Roku 確認後 |
| repo archive 作成 (raw artifact 別保管用) | external: 新 repo 作成 | **Roku 判断** | 外部 repo 作成、段取り |
| GitHub re-auth (`gh auth login`) | local interactive (Roku の terminal 操作必要) | **Roku 操作必要** | Claude bash 経由不可 |
| rollback (`git revert <sha>`) | local commit 追加 (副作用なし) | Claude 自走可 | (常時 OK、ただし push は別 action) |
| force push rollback | destructive: history rewrite | **Roku 明示授権必要** | 通常回避 |
| Codex consult / review (read-only) | external: API call (課金、Anthropic / OpenAI) | Claude 自走可 | (常時 OK、ただし大量実行は cost 監視) |

## Codex Review Protocol

Codex review prompt の先頭で必ず本 anchor を参照させる:

```
まず `/CONTEXT_ANCHOR.md` を読み、Verified Snapshot / Release PR Scope / Required Gates / External Actions が現状と整合しているか確認してください。
欠落 / stale なら P1 (High) で指摘し、本 review の他項目より優先して fix を促してください。
ただし drift 1 (anchor 自身の document commit が source commit の後ろに 1 つ積まれた intrinsic gap) は P1 扱いしない。詳細は §Source commit vs Document commit 規約 参照。
```

## Source commit vs Document commit 規約 (drift 1 intrinsic / drift 2+ stale 機械判定)

本 anchor §Verified Snapshot の `HEAD` は **source commit** を指す。anchor 自身の commit (= document commit) は含まない。これは `scripts/regen_phase{{N}}_progress.sh` と同じ off-by-one 設計で、Codex 命令「自己参照 commit hash は完全一致できない、PR body では必ず push 直前の Bash 実測値を使う」と整合。

| 用語 | 定義 |
|---|---|
| **source commit** | release assertion を指す最新の non-anchor commit (release scope 内の最終 code / docs commit、anchor 自身を除く) |
| **document commit** | anchor 自身 / release note / progress を refresh する docs commit |
| **drift** | `git rev-list <source_commit>..HEAD --count` (HEAD と source commit の差分 commit 数) |

**判定 rule**:

| drift | 状態 | Codex review verdict |
|---|---|---|
| 0 | anchor commit 前 (regen 中など過渡状態) | OK (anchor 未 publish) |
| **1** | anchor 自身の document commit が source commit の後ろに 1 つ積まれた状態 | **intrinsic、P1 扱いしない** |
| **≥2** | source commit の後に code / docs commit が 2 つ以上積まれた状態 | **stale、P1 扱い、anchor refresh 必要** |

**機械判定** (`scripts/check_release_ready.sh` gate 7 で実装):
```bash
SOURCE_COMMIT=$(grep -m 1 '^| HEAD' CONTEXT_ANCHOR.md | sed -nE 's/.*`([a-f0-9]{7,})`.*/\1/p' | head -1)
DRIFT=$(git rev-list ${SOURCE_COMMIT}..HEAD --count)
NON_DOCS=$(git diff --name-only ${SOURCE_COMMIT}..HEAD | grep -vE '^(CONTEXT_ANCHOR\.md|docs/)' | wc -l | tr -d ' ')
[ "$DRIFT" -le 1 ] && [ "$NON_DOCS" -eq 0 ]   # true なら intrinsic / 安全 (gate 7 OK)
```

drift > 1 で docs-only でも stale (exit 7)。drift = 1 でも source の後に code commit があれば (= `NON_DOCS` > 0) stale 扱い。

## 運用パターン (Phase 3 で確立、再利用可)

**新規 commit を打つ時**:
1. code / scripts / non-docs file 修正 → commit A (= source commit になる)
2. anchor / release note / progress を A の HEAD に refresh + regen → commit B (= document commit、A の直後)
3. 結果: anchor 内 source = A、HEAD = B、drift 1 intrinsic

**docs-only commit を打つ時**:
1. anchor / release note / progress 修正 → commit A
2. 同 commit に anchor 自身の HEAD を A 直前 (= 旧 HEAD) で refresh
3. 結果: anchor 内 source = 旧 HEAD、HEAD = A、drift 1 intrinsic

**判定をすり抜けるアンチパターン**:
- 1 commit に code 修正 + anchor 内 source = 自身を更新 → amend 必要 (HARD RULE 違反)
- 連続 commit で anchor refresh をサボる → drift 2+ で gate 7 fail

## 更新責任

- **更新者**: Claude (Codex 命令経由で各 cycle 末に Verified Snapshot を再実測 + Roku Authorized Decisions / Release PR Scope を更新)
- **更新タイミング**: push/PR/merge 直前 + 各 commit cycle 末
- **gate 化**: `check_release_ready.sh` gate 7 で自動検査 (drift > 1 or non-docs commit で exit 7)

## Related Files

- 元 Codex 命令: (artifact path or 内容反映先)
- 元 Codex full review: (artifact path or 内容反映先)
- セッション handoff: (`~/0_Daily-Workspace/handoff_{{DATE}}_{{SESSION_TITLE}}.md`)
- Memory 運用ルール: `~/.claude/projects/-Users-rokumasuda/memory/feedback_codex_master_claude_implementer.md`
- Codex CLI flag pattern: `~/.claude/projects/-Users-rokumasuda/memory/feedback_codex_cli_flag_pattern.md`

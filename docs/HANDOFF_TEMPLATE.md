# Session Handoff — {{DATE}} {{PROJECT_NAME}} {{SESSION_TITLE}}

セッション期間: {{START_TIME}} → {{END_TIME}} (約 {{HOURS}} 時間)
対象 repo: `{{REPO_PATH}}`
対象 branch: `{{BRANCH}}` (HEAD `{{HEAD}}`、main..HEAD = {{MAIN_HEAD_COUNT}} commits、Bash 実測)
**前セッション handoff**: `{{PREV_HANDOFF_PATH}}` (連続セッションの場合)

> **Template note**: このファイルは {{}}-style placeholder 入りの汎用 template。次セッション着手前にこの handoff を読むことで、Codex 主・Claude 従 sequence をゼロから組み立てない。Phase 3 で確立した structure を抽象化したもの (元: `~/0_Daily-Workspace/handoff_2026-05-05_supermovie-codex-pivot-overage.md`、2026-05-05)。

## Completed

- (実装した item を列挙、Codex consult / review cycle ごとの commit hash + 内容)
- 例:
  - **Phase X-A 完了**: 主要変更 ({{COMMIT_RANGE}}、{{N_COMMITS}} commits)
  - **Codex consult/review {{CYCLE_COUNT}} cycle 全消化**: 最終 verdict NONE
  - **Draft PR 作成**: {{PR_URL}} (Claude 自走可で実行、Roku 授権済)

## In Progress

- **bg job (例: Codex consult / 長時間実装) 走行中**:
  - kick: {{TIMESTAMP}}
  - 出力 path: {{OUT_PATH}}
  - 内容: 何を依頼したか / 何を待っているか
  - Roku /handoff 直前に bg job 走行中で完了通知未受信、次セッションで結果 read 必要

- (CONTEXT_ANCHOR.md / template 等の作成中 file)

## Blockers

- **Roku 判断領域**:
  - PR / merge 戦略
  - 実 e2e (Roku 環境 fixture 必要)
  - external service 操作
  - 段取り / 課金 / モラル / 法的

- **技術的 blocker**:
  - GitHub auth invalid (Codex sandbox 固有 vs Claude Code 実環境を区別)
  - upstream READ-only (fork strategy 採用必須)
  - その他 destructive action (force push 等) は Roku 明示授権必要

## Decisions Made

- **{{TIMESTAMP}} 役割再定義** (Roku 発言: "{{ROLE_QUOTE}}"):
  - Codex CLI = 命令 (priority / 設計 / review)
  - Claude Code = 実装実行者のみ
  - Roku = リスク領域判断

- **{{TIMESTAMP}} 8 step 手順** (毎ターン厳守):
  1. Snapshot: pwd / git status / git remote -v / gh repo view / git log
  2. CONTEXT_ANCHOR.md を読む。なければ作る前に Codex に作成指示を仰ぐ
  3. Codex に「次の1手」と「Roku 判断領域か」を聞く
  4. Claude Code は Codex の指示だけを実装
  5. test/lint/build/smoke
  6. Codex review
  7. P0/P1 は自己修正して再 review
  8. 非同期待ちが残るなら ScheduleWakeup

- **{{TIMESTAMP}} 禁止事項**:
  - Codex consult 前に Roku へ選択肢を出す
  - 「両方並行して良いか」「どこからやるか」を Roku に聞く
  - repo owner / 権限 / upstream 文脈を推測で埋める
  - Codex review が走っているだけで待機終了する

- **{{TIMESTAMP}} Roku Authorized Decisions** (CONTEXT_ANCHOR.md §Roku Authorized Decisions 参照):
  - ({{AUTHORIZED_DECISION_COUNT}} 項目を簡潔に記述)

## Key Context

- **repo**: `{{REPO_PATH}}` ({{PROJECT_DESCRIPTION}})
- **upstream**: `{{UPSTREAM_OWNER}}/{{UPSTREAM_NAME}}` (Roku 所有 / 非所有 / 権限)
- **Roku gh account**: `{{GH_ACCOUNT}}` (READ only or WRITE)
- **fork strategy**: Option A (fork → 自 account → upstream PR) etc
- **branch chain**: `main` → `{{ANCESTOR_BRANCH}}` → `{{BRANCH}}` (連続的 ancestry)
- **Codex consult artifact path 規約**: `~/0_Daily-Workspace/codex_{{PROJECT}}_{{PURPOSE}}_{{TIMESTAMP}}.md`
- **HARD RULE 学習** (本 session 中の違反 / 学習):
  - (例: HARD RULE「根拠なき具体性」、「技術可否は検証前に答えない」等)
  - (再発防止策: hook / memory / template 化)

## Codex consult / review cycle

| 時刻 | cycle | verdict | output path |
|---|---|---|---|
| {{TIME1}} | session resume consult | sequence 取得 | {{OUT1}} |
| {{TIME2}} | 1st review | P0 {{P0_COUNT}} / P1 {{P1_COUNT}} / P2 {{P2_COUNT}} | {{OUT2}} |
| ... | ... | ... | ... |
| {{TIMEn}} | Nth review | **NONE / Draft PR 開始 yes** | {{OUTn}} |

## Files Changed

main..HEAD = {{MAIN_HEAD_COUNT}} commits、本セッション分は {{SESSION_COMMITS}} commits ({{COMMIT_RANGE}})。

主要新規 / 拡張 file (`{{PRIMARY_CHANGED_DIRS}}` の例):

```
{{PRIMARY_CHANGED_DIRS}}            [Phase 固有の主要 dir、例: template/scripts/, template/src/, apps/web/, src/]
├── (file 1)                        [新規 / 拡張]
├── (file 2)                        [新規 / 拡張]
└── ...

docs/                               [PROGRESS / RELEASE_NOTE 等]
├── PHASE{{N}}_PROGRESS.md          [auto-gen by scripts/regen_phase{{N}}_progress.sh]
└── PHASE{{N}}_RELEASE_NOTE.md      [release assertion]

CONTEXT_ANCHOR.md                   [Verified Snapshot / Roku Authorized / Release Scope / 7 gate / Source vs Document commit 規約]
scripts/                            [{{RELEASE_GATE_SCRIPT}} / {{REGEN_SCRIPT}}、例: check_release_ready.sh / regen_phase{{N}}_progress.sh]
```

## Next Session Should

1. **本 handoff を読む**: `{{HANDOFF_PATH}}`

2. **bg job (もしあれば) の出力を Read**:
   - path: `{{BG_OUT_PATH}}`
   - 内容: 何を取得すべきか

3. **8 step 手順 厳守で進める**:
   - Step 1 Snapshot: pwd / git status / git remote -v / gh repo view / git log
   - Step 2 CONTEXT_ANCHOR.md (existing なら Read、不在なら Codex に作成指示)
   - Step 3 Codex に「次の1手」consult
   - Step 4 Codex 命令だけ実装 (Codex CLI flag pattern: `feedback_codex_cli_flag_pattern.md` 参照)
   - Step 5-7 test / lint / Codex review / 自己修正
   - Step 8 ScheduleWakeup

4. **Roku 判断領域** で必要なら Roku 合意取り (CONTEXT_ANCHOR.md:External Actions の Roku 判断 / Roku 明示授権必要 行)

5. **本 session 学習 feedback memory を読む**:
   - `~/.claude/projects/-Users-rokumasuda/memory/feedback_codex_master_claude_implementer.md`
   - `~/.claude/projects/-Users-rokumasuda/memory/feedback_codex_cli_flag_pattern.md`
   - 既存 `feedback_codex_first_principle.md` + `feedback_no_unsolicited_stop_in_autonomous_mode.md` と組み合わせ

---

(本 handoff は Roku /handoff 指示で作成、{{TIMESTAMP}} 役割再定義 + 8 step 確定後の引き継ぎ。次セッションは Codex consult 経由で sequence 取得から開始、8 step 手順厳守。)

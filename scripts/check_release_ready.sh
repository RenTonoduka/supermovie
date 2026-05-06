#!/usr/bin/env bash
# Phase 3 release readiness composite gate.
# 全 self-driveable check を 1 commands で走らせ、Codex review が release-ready
# 判定するための前提状態を verify。
#
# Usage:
#   bash scripts/check_release_ready.sh
#
# Exit codes:
#   0 = release-ready (全 gate pass、optional gate は node_modules 不在で skip 可)
#   1 = doc drift (regen --verify fail)
#   2 = integration test fail
#   3 = worktree dirty
#   4 = unknown env (git / python3 不在)
#   5 = npm run lint fail (node_modules 存在時のみ)
#   6 = npm run test:react fail (node_modules + vitest 存在時のみ)
#   7 = anchor drift stale (CONTEXT_ANCHOR.md の source commit から HEAD まで
#       drift > 1 or non-docs commit 含む = anchor refresh 必要)
#
# 走らせる gate:
#   1. git rev-parse / python3 / bash 環境チェック
#   2. worktree clean (untracked / modified なし)
#   3. scripts/regen_phase3_progress.sh --verify
#   4. python3 template/scripts/test_timeline_integration.py
#   5. (optional) cd template && npm run lint (Codex CODEX_GATE_VERIFY 推奨、
#      node_modules 不在で skip)
#   6. (optional) cd template && npm run test:react (Phase 3-S B5、useNarrationMode
#      hook の watchStaticFile + invalidation 検証、vitest + jsdom + RTL、
#      node_modules + vitest 不在で skip)
#   7. anchor drift check (CONTEXT_ANCHOR.md §Source commit vs Document commit 規約)
#      - source commit が git history に存在
#      - drift = `git rev-list source..HEAD --count` ≤ 1
#      - source..HEAD diff が docs-only (CONTEXT_ANCHOR.md / docs/ 配下のみ)
#      - 上記 3 条件全 OK で intrinsic、外れたら stale
#
# 走らせない gate (実 project / 課金):
#   - npm run visual-smoke (実 main.mp4 必要)
#   - render e2e
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "=== Phase 3 release readiness gate ==="
echo "repo: $REPO_DIR"
echo "head: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
echo

# 1. 環境チェック
for tool in git python3; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "  [FAIL] env: $tool not found"
        exit 4
    fi
done
echo "  [OK]   env: git + python3 available"

# 2. worktree clean
if ! git diff --quiet HEAD 2>/dev/null; then
    echo "  [FAIL] worktree: modified files present"
    git status --short
    exit 3
fi
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | head -5)
if [ -n "$UNTRACKED" ]; then
    echo "  [FAIL] worktree: untracked files present:"
    echo "$UNTRACKED" | sed 's/^/    /'
    exit 3
fi
echo "  [OK]   worktree: clean"

# 3. regen --verify (doc drift)
echo
echo "--- regen verify ---"
if ! bash "$REPO_DIR/scripts/regen_phase3_progress.sh" --verify; then
    echo "  [FAIL] regen --verify failed"
    exit 1
fi
echo "  [OK]   regen --verify pass"

# 4. integration smoke test
echo
echo "--- integration smoke test ---"
TEST_LOG=$(mktemp)
if python3 "$REPO_DIR/template/scripts/test_timeline_integration.py" > "$TEST_LOG" 2>&1; then
    PASS_LINE=$(grep -E "^Result: " "$TEST_LOG" | tail -1)
    echo "  [OK]   $PASS_LINE"
    rm -f "$TEST_LOG"
else
    echo "  [FAIL] integration test failed:"
    tail -20 "$TEST_LOG" | sed 's/^/    /'
    rm -f "$TEST_LOG"
    exit 2
fi

# 5. (optional) TS compile surface (lint + tsc)
# Codex CODEX_GATE_VERIFY_20260504T232227 推奨: 4 gate に足すなら lint のみ。
# node_modules 不在で skip (Roku 環境で npm install 後に再実行推奨)。
echo
echo "--- TS compile surface (optional) ---"
if [ -d "$REPO_DIR/template/node_modules" ] && [ -x "$REPO_DIR/template/node_modules/.bin/eslint" ]; then
    LINT_LOG=$(mktemp)
    if (cd "$REPO_DIR/template" && npm run lint > "$LINT_LOG" 2>&1); then
        echo "  [OK]   npm run lint pass (eslint + tsc)"
        rm -f "$LINT_LOG"
    else
        echo "  [FAIL] npm run lint failed:"
        tail -30 "$LINT_LOG" | sed 's/^/    /'
        rm -f "$LINT_LOG"
        exit 5
    fi
else
    echo "  [SKIP] template/node_modules 不在、Roku 環境で npm install 後に再実行推奨"
fi

# 6. (optional) React component test (Phase 3-S B5)
# vitest + jsdom + @testing-library/react で useNarrationMode hook 検証。
# node_modules + vitest 不在で skip。
echo
echo "--- React component test (optional) ---"
if [ -d "$REPO_DIR/template/node_modules" ] && [ -x "$REPO_DIR/template/node_modules/.bin/vitest" ]; then
    REACT_LOG=$(mktemp)
    if (cd "$REPO_DIR/template" && npm run test:react > "$REACT_LOG" 2>&1); then
        PASS_LINE=$(grep -E "Tests +[0-9]+ passed" "$REACT_LOG" | tail -1 || echo "passed")
        echo "  [OK]   $PASS_LINE"
        rm -f "$REACT_LOG"
    else
        echo "  [FAIL] npm run test:react failed:"
        tail -30 "$REACT_LOG" | sed 's/^/    /'
        rm -f "$REACT_LOG"
        exit 6
    fi
else
    echo "  [SKIP] template/node_modules + vitest 不在、Roku 環境で npm install 後に再実行推奨"
fi

# 7. anchor drift check (CONTEXT_ANCHOR.md §Source commit vs Document commit 規約)
echo
echo "--- anchor drift check ---"
ANCHOR_FILE="$REPO_DIR/CONTEXT_ANCHOR.md"
if [ ! -f "$ANCHOR_FILE" ]; then
    echo "  [FAIL] CONTEXT_ANCHOR.md 不在 (anchor 自身が欠落 = §Codex Review Protocol で P1 扱い)"
    exit 7
else
    SOURCE_COMMIT=$(grep -m 1 '^| HEAD' "$ANCHOR_FILE" | sed -nE 's/.*`([a-f0-9]{7,})`.*/\1/p' | head -1)
    if [ -z "$SOURCE_COMMIT" ]; then
        echo "  [FAIL] CONTEXT_ANCHOR.md HEAD 行から source commit を抽出できませんでした"
        echo "         anchor の §Verified Snapshot table が破損 = anchor stale 扱い"
        exit 7
    elif ! git rev-parse "$SOURCE_COMMIT" >/dev/null 2>&1; then
        echo "  [FAIL] anchor の source commit ($SOURCE_COMMIT) が git history に存在しません"
        echo "         CONTEXT_ANCHOR.md の HEAD を最新の release commit に refresh してください"
        exit 7
    else
        DRIFT=$(git rev-list "${SOURCE_COMMIT}..HEAD" --count 2>/dev/null || echo 0)
        NON_DOCS=$(git diff --name-only "${SOURCE_COMMIT}..HEAD" 2>/dev/null | grep -vE '^(CONTEXT_ANCHOR\.md|docs/)' | wc -l | tr -d ' ')
        if [ "$DRIFT" -le 1 ] && [ "$NON_DOCS" -eq 0 ]; then
            echo "  [OK]   anchor drift = $DRIFT (≤1 intrinsic), source..HEAD は docs-only (CONTEXT_ANCHOR + docs/)"
        else
            echo "  [FAIL] anchor stale: drift=$DRIFT, non-docs-files=$NON_DOCS"
            echo "         source commit: $SOURCE_COMMIT"
            echo "         current HEAD : $(git rev-parse --short HEAD)"
            echo "         §Source commit vs Document commit 規約 (CONTEXT_ANCHOR.md) で drift > 1 or 非 docs commit は stale 扱い"
            echo "         → CONTEXT_ANCHOR.md §Verified Snapshot を最新値に refresh + 1 commit"
            exit 7
        fi
    fi
fi

echo
echo "=== ALL GATES PASS ==="
echo "release-ready: yes (technical readiness only、Roku 判断領域は別途)"
echo "  - PR / merge 戦略 (1 PR squash 推奨、Codex)"
echo "  - 実 project visual-smoke / render e2e (main.mp4 fixture 必要)"
exit 0

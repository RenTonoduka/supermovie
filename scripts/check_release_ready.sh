#!/usr/bin/env bash
# Phase 3 release readiness composite gate.
# 全 self-driveable check を 1 commands で走らせ、Codex review が release-ready
# 判定するための前提状態を verify。
#
# Usage:
#   bash scripts/check_release_ready.sh
#
# Exit codes:
#   0 = release-ready (全 gate pass)
#   1 = doc drift (regen --verify fail)
#   2 = integration test fail
#   3 = worktree dirty
#   4 = unknown env (git / python3 不在)
#
# 走らせる gate:
#   1. git rev-parse / python3 / bash 環境チェック
#   2. worktree clean (untracked / modified なし)
#   3. scripts/regen_phase3_progress.sh --verify
#   4. python3 template/scripts/test_timeline_integration.py
#
# 走らせない gate (要 npm install / 実 project):
#   - npm run lint (eslint + tsc)
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

echo
echo "=== ALL GATES PASS ==="
echo "release-ready: yes (technical readiness only、Roku 判断領域は別途)"
echo "  - PR / merge 戦略 (1 PR squash 推奨、Codex)"
echo "  - 実 project visual-smoke / render e2e (main.mp4 fixture 必要)"
echo "  - npm run lint (要 npm install、Roku 環境で再実行推奨)"
exit 0

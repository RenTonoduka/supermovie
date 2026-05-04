#!/usr/bin/env bash
# Phase 3 progress note の commit chain section を git log から再生成する helper.
# Codex Phase 3-M review Part B 候補 vi 実装。
#
# Usage:
#   bash scripts/regen_phase3_progress.sh
#   (docs/PHASE3_PROGRESS.md の commit chain section を上書き、最新 commit を反映)
#
# 動作:
#   - git log roku/phase3i-transcript-alignment..HEAD --oneline を取得
#   - docs/PHASE3_PROGRESS.md の "## 全 commit count" セクションを書換
#
# 制約:
#   - 現 branch が roku/phase3j-timeline (or 後続) であること前提
#   - 手動編集セクション (Phase 別 deliverable, Codex review 履歴 table) は touch しない
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

PROGRESS_MD="docs/PHASE3_PROGRESS.md"
BASE_BRANCH="${BASE_BRANCH:-roku/phase3i-transcript-alignment}"

if [ ! -f "$PROGRESS_MD" ]; then
    echo "ERROR: $PROGRESS_MD not found" >&2
    exit 1
fi

if ! git rev-parse --verify "$BASE_BRANCH" >/dev/null 2>&1; then
    echo "ERROR: base branch $BASE_BRANCH not found" >&2
    exit 2
fi

COMMITS_FILE=$(mktemp)
git log "${BASE_BRANCH}..HEAD" --oneline > "$COMMITS_FILE"
COMMIT_COUNT=$(wc -l < "$COMMITS_FILE" | tr -d ' ')
NOW=$(date +%Y-%m-%d_%H:%M)

# Python で section 書換 (awk より複雑文字列に強い)
python3 - "$PROGRESS_MD" "$COMMITS_FILE" "$COMMIT_COUNT" "$NOW" <<'EOF'
import sys
from pathlib import Path

progress_path = Path(sys.argv[1])
commits_path = Path(sys.argv[2])
count = sys.argv[3]
now = sys.argv[4]

content = progress_path.read_text(encoding="utf-8")
commits = commits_path.read_text(encoding="utf-8").rstrip("\n")

new_section = f"""## 全 commit count (roku/phase3j-timeline branch、最新 {count} 件)

```
{commits}
```

(更新: {now}、`scripts/regen_phase3_progress.sh` で auto-gen、最新 commit を反映)

"""

import re
# "## 全 commit count" から次の "## " までを new_section に置換
pattern = re.compile(r"## 全 commit count.*?(?=^## )", re.DOTALL | re.MULTILINE)
if not pattern.search(content):
    # 末尾に "## " がない場合は EOF まで
    pattern = re.compile(r"## 全 commit count.*\Z", re.DOTALL)

new_content = pattern.sub(new_section, content, count=1)
progress_path.write_text(new_content, encoding="utf-8")
print(f"regenerated: {progress_path}")
print(f"commit count: {count}")
EOF

rm -f "$COMMITS_FILE"
echo "diff:"
git diff "$PROGRESS_MD" | head -30 || true

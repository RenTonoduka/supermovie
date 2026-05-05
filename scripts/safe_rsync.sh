#!/usr/bin/env bash
# safe_rsync.sh — guarded rsync wrapper for SuperMovie project sync.
#
# Codex consult bhrcsxwga (2026-05-05 16:36) verdict 準拠の最小 wrapper.
# 2026-05-05 16:14 の rsync --delete 副作用 (proj1 typo_dict.json / transcript_*
# / vad_result.json 等を Roku 前 work 削除) を二度起こさないため.
#
# Usage:
#   bash scripts/safe_rsync.sh --source <SOURCE_DIR> --dest <DEST_DIR>
#   bash scripts/safe_rsync.sh --source <SOURCE_DIR> --dest <DEST_DIR> --apply
#   bash scripts/safe_rsync.sh --init-sentinel --dest <DEST_DIR>
#
# Default mode: dry-run (rsync は走るが file は変更しない).
# --apply: dry-run safety scan を通った時のみ実 sync.
# --init-sentinel: destination に .supermovie-sandbox を作成 (apply とは排他).
#
# Exit codes:
#   0 = dry-run pass (or apply 完了 / sentinel 作成完了)
#   1 = arg error (--source / --dest 不足、相互排他違反 等)
#   2 = path safety violation (source==dest / source が dest 配下 / dest が source 配下)
#   3 = sentinel violation (destination に .supermovie-sandbox なしで apply 試行)
#   4 = protect violation (protected path に対して update/delete/overwrite が発生する dry-run 結果)
#   5 = backup dir violation (backup dir が destination 配下 or 相対 path)
#   6 = rsync 自身の non-zero exit (transport / permission 等)
#
# Codex review P0 観点 (consult bhrcsxwga):
#   - --apply は必ず dry-run safety scan 経由
#   - destination sentinel なしで --delete 走らない
#   - sentinel を通常 sync 中に暗黙作成しない (--init-sentinel mode のみ)
#   - .supermovie-sandbox 自体が protect list に入っている (scripts/safe_rsync.protect L1)
#   - protected path の deletion だけでなく update/overwrite も dry-run scan で停止
#   - backup dir が絶対 path で destination 外
#   - --delete-excluded 使わない (excluded を残す方針)
#   - source/dest 同一 path、dest が source 配下、source が dest 配下を拒否

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTECT_FILE="${SAFE_RSYNC_PROTECT_FILE:-$SCRIPT_DIR/safe_rsync.protect}"
BACKUP_ROOT_DEFAULT="${TMPDIR:-/tmp}/supermovie-rsync-backups"
BACKUP_ROOT="${SAFE_RSYNC_BACKUP_ROOT:-$BACKUP_ROOT_DEFAULT}"
SENTINEL=".supermovie-sandbox"

SOURCE=""
DEST=""
APPLY=0
INIT_SENTINEL=0

usage() {
    sed -n '2,40p' "$0"
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        --source) SOURCE="$2"; shift 2 ;;
        --dest)   DEST="$2";   shift 2 ;;
        --apply)  APPLY=1; shift ;;
        --init-sentinel) INIT_SENTINEL=1; shift ;;
        -h|--help) usage ;;
        *) echo "[safe_rsync] unknown arg: $1" >&2; usage ;;
    esac
done

# --- arg validation ---

if [ -z "$DEST" ]; then
    echo "[safe_rsync] FAIL: --dest required" >&2
    exit 1
fi

if [ "$INIT_SENTINEL" -eq 1 ] && [ "$APPLY" -eq 1 ]; then
    echo "[safe_rsync] FAIL: --init-sentinel と --apply は排他 (sentinel 暗黙作成禁止)" >&2
    exit 1
fi

if [ "$INIT_SENTINEL" -eq 1 ] && [ -n "$SOURCE" ]; then
    echo "[safe_rsync] FAIL: --init-sentinel は --source 不要" >&2
    exit 1
fi

if [ "$INIT_SENTINEL" -eq 0 ] && [ -z "$SOURCE" ]; then
    echo "[safe_rsync] FAIL: --source required (sync mode)" >&2
    exit 1
fi

# --- init-sentinel mode (apply / sync とは別経路) ---

if [ "$INIT_SENTINEL" -eq 1 ]; then
    mkdir -p "$DEST"
    SENTINEL_PATH="$DEST/$SENTINEL"
    if [ -e "$SENTINEL_PATH" ]; then
        echo "[safe_rsync] OK: sentinel 既存 $SENTINEL_PATH"
        exit 0
    fi
    : > "$SENTINEL_PATH"
    echo "[safe_rsync] OK: sentinel 作成 $SENTINEL_PATH"
    exit 0
fi

# --- path safety: source / dest 同一 / 包含関係 拒否 ---

# 絶対 path 化 (シンボリック解決込み)
ABS_SOURCE="$(cd "$SOURCE" && pwd -P 2>/dev/null || echo "$SOURCE")"
ABS_DEST="$(mkdir -p "$DEST" && cd "$DEST" && pwd -P)"

case "$ABS_SOURCE" in
    "$ABS_DEST")
        echo "[safe_rsync] FAIL: source==dest ($ABS_SOURCE)" >&2
        exit 2
        ;;
esac

case "$ABS_DEST" in
    "$ABS_SOURCE"/*)
        echo "[safe_rsync] FAIL: dest ($ABS_DEST) が source ($ABS_SOURCE) 配下" >&2
        exit 2
        ;;
esac

case "$ABS_SOURCE" in
    "$ABS_DEST"/*)
        echo "[safe_rsync] FAIL: source ($ABS_SOURCE) が dest ($ABS_DEST) 配下" >&2
        exit 2
        ;;
esac

# --- sentinel check (apply mode のみ厳格) ---

SENTINEL_PATH="$ABS_DEST/$SENTINEL"
if [ "$APPLY" -eq 1 ] && [ ! -e "$SENTINEL_PATH" ]; then
    echo "[safe_rsync] FAIL: destination に $SENTINEL なし → --apply 不可" >&2
    echo "  対処: bash $0 --init-sentinel --dest $DEST で作成、内容を確認してから --apply" >&2
    exit 3
fi

# --- backup dir 構築 (絶対 path、destination 外を保証) ---

DEST_BASENAME="$(basename "$ABS_DEST")"
TS="$(date +%Y%m%dT%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$DEST_BASENAME/$TS"

# backup dir も絶対 path 化
ABS_BACKUP_ROOT="$(mkdir -p "$BACKUP_ROOT" && cd "$BACKUP_ROOT" && pwd -P)"
ABS_BACKUP_DIR="$ABS_BACKUP_ROOT/$DEST_BASENAME/$TS"

case "$ABS_BACKUP_DIR" in
    "$ABS_DEST"|"$ABS_DEST"/*)
        echo "[safe_rsync] FAIL: backup dir ($ABS_BACKUP_DIR) が destination ($ABS_DEST) 配下" >&2
        exit 5
        ;;
    /*)
        : ;;  # 絶対 path OK
    *)
        echo "[safe_rsync] FAIL: backup dir ($ABS_BACKUP_DIR) が絶対 path でない" >&2
        exit 5
        ;;
esac

# --- protect list 構築 ---

if [ ! -f "$PROTECT_FILE" ]; then
    echo "[safe_rsync] FAIL: protect file 不在: $PROTECT_FILE" >&2
    exit 1
fi

# protect list を rsync filter rule に変換 (deletion protection 用)
PROTECT_RULES=()
PROTECT_PATTERNS=()
while IFS= read -r line; do
    case "$line" in
        ""|\#*) continue ;;
    esac
    PROTECT_RULES+=("--filter=P $line")
    PROTECT_PATTERNS+=("$line")
done < "$PROTECT_FILE"

# --- dry-run safety scan (常に走る) ---

echo "[safe_rsync] === dry-run safety scan ==="
echo "  source: $ABS_SOURCE/"
echo "  dest:   $ABS_DEST/"
echo "  protect: $PROTECT_FILE (${#PROTECT_PATTERNS[@]} patterns)"
echo "  backup: $ABS_BACKUP_DIR (apply 時のみ作成)"
echo

DRY_RUN_LOG="$(mktemp)"
trap 'rm -f "$DRY_RUN_LOG"' EXIT

# itemize-changes で全 update/delete/overwrite を出力
# --delete を含めて scan、protect は P filter で適用
rsync -avcn --delete --itemize-changes \
    "${PROTECT_RULES[@]}" \
    "$ABS_SOURCE/" "$ABS_DEST/" > "$DRY_RUN_LOG" 2>&1 || {
    echo "[safe_rsync] FAIL: rsync dry-run exit non-zero" >&2
    cat "$DRY_RUN_LOG" >&2
    exit 6
}

# protect list 内の path に対する任意の operation (update/delete/overwrite) を検出
VIOLATION=0
for pattern in "${PROTECT_PATTERNS[@]}"; do
    # `***` (recursive) を grep 互換に正規化
    grep_pattern="${pattern//\*\*\*/.*}"
    grep_pattern="${grep_pattern//\*\*/.*}"
    grep_pattern="${grep_pattern//\*/[^/]*}"
    if grep -qE "^[><ch][f.][.cstTpoguaxn+ ]+ $grep_pattern" "$DRY_RUN_LOG" 2>/dev/null; then
        echo "[safe_rsync] VIOLATION: protected path $pattern に operation 検出" >&2
        grep -E "^[><ch][f.][.cstTpoguaxn+ ]+ $grep_pattern" "$DRY_RUN_LOG" >&2
        VIOLATION=1
    fi
    # delete operation も別 grep
    if grep -qE "^\*deleting +$grep_pattern" "$DRY_RUN_LOG" 2>/dev/null; then
        echo "[safe_rsync] VIOLATION: protected path $pattern に delete 検出" >&2
        grep -E "^\*deleting +$grep_pattern" "$DRY_RUN_LOG" >&2
        VIOLATION=1
    fi
done

if [ "$VIOLATION" -eq 1 ]; then
    echo "[safe_rsync] FAIL: protect list 違反、--apply 中止" >&2
    echo "  対処: protect list ($PROTECT_FILE) を確認、または --source の構成を見直す" >&2
    exit 4
fi

echo "[safe_rsync] OK: dry-run safety scan pass (protect list 違反なし)"

# --- dry-run mode は ここで exit ---

if [ "$APPLY" -ne 1 ]; then
    echo
    echo "[safe_rsync] dry-run mode 完了。--apply で実 sync (sentinel + protect 全 pass 後のみ実行可)。"
    echo "  dry-run log: $DRY_RUN_LOG (この exit 後に削除)"
    exit 0
fi

# --- apply mode: 実 sync ---

mkdir -p "$ABS_BACKUP_DIR"
echo
echo "[safe_rsync] === apply mode ==="
echo "  backup dir: $ABS_BACKUP_DIR"
echo

rsync -av --delete \
    --backup --backup-dir="$ABS_BACKUP_DIR" \
    "${PROTECT_RULES[@]}" \
    "$ABS_SOURCE/" "$ABS_DEST/" || {
    echo "[safe_rsync] FAIL: rsync apply exit non-zero" >&2
    exit 6
}

echo
echo "[safe_rsync] OK: apply 完了 (backup: $ABS_BACKUP_DIR)"
exit 0

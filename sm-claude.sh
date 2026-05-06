#!/bin/bash
# SuperMovie wrapper: load plugin-local .env and start Claude Code with --plugin-dir
# Usage: sm-claude.sh [PROJECT_DIR]

PROJECT_DIR="${1:-$PWD}"

set -a
[ -f ~/.claude/plugins/supermovie/.env ] && source ~/.claude/plugins/supermovie/.env
set +a

cd "$PROJECT_DIR" && exec claude --plugin-dir ~/.claude/plugins/supermovie

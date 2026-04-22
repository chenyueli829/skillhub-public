#!/bin/bash
# 打包 agent-pay-skill 为 zip（用于上传市场）
#
# 用法: bash scripts/package.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT="$SKILL_DIR/agent-pay-skill.zip"

cd "$SKILL_DIR/.."

rm -f "$OUTPUT"

zip -r "$OUTPUT" "$(basename "$SKILL_DIR")" \
  -x "*/\.git/*" \
  -x "*/\.idea/*" \
  -x "*/\.vscode/*" \
  -x "*/\.cursor/*" \
  -x "*/\.claude/*" \
  -x "*/\.codebuddy/*" \
  -x "*/templates/*" \
  -x "*/__pycache__/*" \
  -x "*/*.pyc" \
  -x "*/*.zip" \
  -x "*/lib/keys/*" \
  -x "*/lib/config.json" \
  -x "*/setup/assets/*.png" \
  -x "*/setup/.pending_session.json" \
  -x "*/signer/*.go" \
  -x "*/signer/go.mod" \
  -x "*/signer/go.sum" \
  -x "*/signer/build.sh"

echo ""
echo "打包完成: $OUTPUT"
echo "文件大小: $(du -h "$OUTPUT" | cut -f1)"

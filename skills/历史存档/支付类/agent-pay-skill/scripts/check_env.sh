#!/bin/bash
# Agent Pay 环境前置检查
#
# 返回码：
#   0 = 一切就绪
#   1 = 签名工具未初始化
#   2 = 配置文件未生成或不完整
#   3 = 依赖未安装

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LIB_DIR="$SKILL_DIR/lib"
SIGNER_BIN_DIR="$SKILL_DIR/signer/bin"
PENDING_SESSION_FILE="$SKILL_DIR/setup/.pending_session.json"

# 0. 检查 Python
if command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "PYTHON_MISSING"
    exit 3
fi

# 0.5 检查是否有待激活的 session（register.py Phase1 已完成，等待用户验证码）
if [ -f "$PENDING_SESSION_FILE" ]; then
    # 读取 pending session 信息，检查是否过期（超过15分钟视为过期）
    PENDING_INFO=$($PYTHON -c "
import json, sys
from datetime import datetime, timezone, timedelta
try:
    data = json.load(open('$PENDING_SESSION_FILE'))
    session_id = data.get('session_id', '')
    session_type = data.get('type', 'register')
    created_at = data.get('created_at', '')
    if session_id and created_at:
        created = datetime.fromisoformat(created_at)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        age_minutes = (datetime.now(timezone.utc) - created).total_seconds() / 60
        if age_minutes <= 15:
            print(f'{session_type} {session_id}')
        else:
            print('EXPIRED')
    else:
        print('INVALID')
except Exception:
    print('INVALID')
" 2>/dev/null)

    case "$PENDING_INFO" in
        EXPIRED|INVALID)
            # 过期或无效，清理文件，继续正常检查流程
            rm -f "$PENDING_SESSION_FILE"
            ;;
        register\ *)
            SESSION_ID="${PENDING_INFO#register }"
            echo "PENDING_ACTIVATION $SESSION_ID"
            exit 4
            ;;
        sign_service\ *)
            # 签约会话不需要 pending 恢复（用户在小程序端完成即可），清理
            rm -f "$PENDING_SESSION_FILE"
            ;;
    esac
fi

# 1. 检查签名二进制 + 初始化状态
SIGNER_BIN=""
OS_NAME=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH_NAME=$(uname -m)
case "$ARCH_NAME" in
    x86_64)  ARCH_NAME="amd64" ;;
    aarch64) ARCH_NAME="arm64" ;;
esac
SIGNER_BIN="$SIGNER_BIN_DIR/skill_signer_${OS_NAME}_${ARCH_NAME}"

if [ ! -x "$SIGNER_BIN" ]; then
    echo "SIGNER_BINARY_MISSING"
    exit 1
fi

STATUS=$("$SIGNER_BIN" status 2>/dev/null)
if echo "$STATUS" | $PYTHON -c "import sys,json; s=json.load(sys.stdin).get('status',''); sys.exit(0 if s=='READY' else 1)" 2>/dev/null; then
    : # signer ready
else
    echo "SIGNER_NOT_INITIALIZED - 请执行首次接入流程"
    exit 1
fi

# 2. 检查配置文件
if [ ! -f "$LIB_DIR/config.json" ]; then
    echo "CONFIG_MISSING"
    exit 2
fi

AGENT_DID=$($PYTHON -c "import json; print(json.load(open('$LIB_DIR/config.json')).get('agent',{}).get('agent_did',''))" 2>/dev/null)
if [ -z "$AGENT_DID" ]; then
    echo "CONFIG_INCOMPLETE"
    exit 2
fi

# 3. 检查 Python 依赖
if ! $PYTHON -c "import httpx, cryptography" 2>/dev/null; then
    echo "DEPS_MISSING"
    exit 3
fi

echo "READY"
exit 0

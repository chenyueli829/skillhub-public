#!/usr/bin/env python3
"""
Agent Pay 全链路验证

用法: python setup/verify.py
"""

import json
import socket
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

SKILL_DIR = Path(__file__).resolve().parent.parent
LIB_DIR = SKILL_DIR / "lib"

_SETUP_DIR = str(Path(__file__).resolve().parent)
if _SETUP_DIR not in sys.path:
    sys.path.insert(0, _SETUP_DIR)

from common import get_signer_binary_path


def check_tcp(url: str, timeout: float = 5) -> bool:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, socket.timeout):
        return False


def check_balance_via_agent_pay(user_id: str, config_path: str = None) -> tuple[bool, str]:
    """通过 Agent Pay 后端查询余额（带 KYA 签名）。"""
    if not user_id:
        return False, "config.json 中缺少 user_id，无法验证"

    sys.path.insert(0, str(LIB_DIR))
    try:
        from agent_pay.config import Config
        from agent_pay.client import AgentPayClient
        from agent_pay.crypto import create_signer

        config = Config.load(config_path)
        signer = create_signer(config)
        client = AgentPayClient(config.agent_pay, signer)
        result = client.query_balance(user_id)
        client.close()

        if result.get("status") == "OK":
            available = result.get("available_balance", 0)
            return True, f"可达，余额: {available / 100:.2f} 元"
        else:
            return False, f"查询失败: {result.get('message', '未知错误')}"
    except Exception as e:
        return False, f"余额查询异常: {e}"


def check_signer_binary() -> tuple[bool, str]:
    """Check signer binary exists and vault is initialized."""
    binary_path = get_signer_binary_path()
    if not Path(binary_path).exists():
        return False, f"签名二进制不存在: {binary_path}"

    try:
        proc = subprocess.run(
            [binary_path, "status"],
            capture_output=True, text=True, timeout=10,
        )
        result = json.loads(proc.stdout)
        status = result.get("status", "")
        if status == "READY":
            return True, "签名工具已就绪"
        elif status == "NOT_INITIALIZED":
            return False, "签名工具未初始化，请先运行 generate_keys.py"
        else:
            return False, f"签名工具异常: {result.get('message', status)}"
    except Exception as e:
        return False, f"签名工具检查失败: {e}"


def verify_setup() -> dict:
    checks = []
    all_passed = True

    # 1. lib 代码
    config_py = LIB_DIR / "agent_pay" / "config.py"
    code_ok = config_py.exists()
    checks.append({"name": "支付库代码", "passed": code_ok, "detail": str(LIB_DIR)})
    if not code_ok:
        all_passed = False

    # 2. 签名工具
    signer_ok, signer_detail = check_signer_binary()
    checks.append({"name": "签名工具", "passed": signer_ok, "detail": signer_detail})
    if not signer_ok:
        all_passed = False

    # 3. 公钥文件
    public_key = LIB_DIR / "keys" / "agent_public_key.pem"
    pubkey_ok = public_key.exists()
    checks.append({"name": "公钥文件", "passed": pubkey_ok, "detail": "公钥存在" if pubkey_ok else "缺少公钥文件"})
    if not pubkey_ok:
        all_passed = False

    # 4. config.json
    config_file = LIB_DIR / "config.json"
    if not config_file.exists():
        checks.append({"name": "配置文件", "passed": False, "detail": "config.json 不存在"})
        all_passed = False
    else:
        try:
            with open(config_file) as f:
                config = json.load(f)

            agent_did = config.get("agent", {}).get("agent_did", "")
            user_id = config.get("user_id", "")
            agent_pay_url = config.get("agent_pay", {}).get("base_url", "")
            config_ok = bool(agent_did) and bool(agent_pay_url)
            checks.append({
                "name": "配置文件",
                "passed": config_ok,
                "detail": f"agent_did={agent_did}, user_id={user_id or '未设置'}" if config_ok else "缺少必要配置",
            })
            if not config_ok:
                all_passed = False

            if agent_pay_url:
                tcp_ok = check_tcp(agent_pay_url)
                checks.append({"name": "Agent Pay 后端", "passed": tcp_ok, "detail": f"{agent_pay_url} {'可达' if tcp_ok else '不可达'}"})
                if not tcp_ok:
                    all_passed = False

            if agent_pay_url and user_id:
                config_path = str(config_file) if config_file.exists() else None
                balance_ok, balance_detail = check_balance_via_agent_pay(user_id, config_path)
                checks.append({"name": "Agent Pay 余额查询", "passed": balance_ok, "detail": balance_detail})
                if not balance_ok:
                    all_passed = False

        except (json.JSONDecodeError, OSError) as e:
            checks.append({"name": "配置文件", "passed": False, "detail": f"解析错误: {e}"})
            all_passed = False

    # 5. Python 依赖
    missing = []
    for mod in ["httpx", "cryptography", "pydantic"]:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    deps_ok = len(missing) == 0
    checks.append({
        "name": "Python依赖",
        "passed": deps_ok,
        "detail": "所有依赖已安装" if deps_ok else f"缺少: {', '.join(missing)}",
    })
    if not deps_ok:
        all_passed = False

    return {
        "status": "PASS" if all_passed else "FAIL",
        "checks": checks,
        "summary": f"{'全部通过' if all_passed else '存在未通过项'}（{sum(1 for c in checks if c['passed'])}/{len(checks)}）",
    }


def main():
    result = verify_setup()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

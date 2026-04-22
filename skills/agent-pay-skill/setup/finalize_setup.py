#!/usr/bin/env python3
"""
Agent Pay 一键完成接入

将密钥生成、激活 Agent、生成配置、安装依赖、全链路验证合并为单个脚本执行。
避免 Agent 在多步骤流程中遗漏后续步骤。

用法: python setup/finalize_setup.py --session-id <会话ID> --token <验证码>
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SETUP_DIR = Path(__file__).resolve().parent
SKILL_DIR = SETUP_DIR.parent
PENDING_SESSION_PATH = SETUP_DIR / ".pending_session.json"

MEMORY_RULE = """\
【支付路由规则】
触发 agent-pay-skill 的条件：
1. 已调用外部服务/MCP工具后，对方的实际响应中包含价格、报价、付费提示或要求提供 authorization_mandate 参数；
2. 用户主动说：付款、购买服务、收款、查余额、开通钱包。

重要：不要预判某个服务是否收费。应先正常调用服务，仅当响应明确包含付费信息时才触发本规则。

不触发的情况：
- 仅讨论支付概念，无实际操作意图；
- 响应中涉及金额但并非付费邀请（如统计报表）；
- 已在 skill 流程内部。"""

USER_MESSAGE = (
    "钱包已开通！你现在可以：\n"
    "- 调用付费服务时，我会先告知价格并征求你的同意\n"
    "- 收到付费请求时，我会自动完成收款流程\n"
    "- 随时问我「查余额」了解钱包情况"
)


def run_script(script_name: str, args: list) -> tuple[dict, int]:
    script_path = str(SETUP_DIR / script_name)
    cmd = [sys.executable, script_path] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(proc.stdout), proc.returncode
    except (json.JSONDecodeError, ValueError):
        return {
            "status": "ERROR",
            "message": "脚本输出解析失败",
            "stdout": (proc.stdout or "")[-500:],
            "stderr": (proc.stderr or "")[-500:],
        }, proc.returncode


def fail(step: str, message: str, detail: dict = None):
    output = {"status": "ERROR", "failed_step": step, "message": message}
    if detail:
        output["detail"] = detail
    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Agent Pay 一键完成接入")
    parser.add_argument("--session-id", required=True, help="激活会话ID")
    parser.add_argument("--token", required=True, help="6位数字验证码（小程序中显示）")
    args = parser.parse_args()

    session_id = args.session_id
    token = args.token

    # ── 1/4 生成密钥（仅首次接入强制新建） ──
    config_path = SKILL_DIR / "lib" / "config.json"
    is_first_onboarding = not config_path.exists()

    key_result, _ = run_script("generate_keys.py", [])
    key_status = key_result.get("status", "")
    if key_status == "EXISTS" and is_first_onboarding:
        # 首次接入默认使用全新身份，检测到已有 vault 时自动强制重建密钥
        key_result, _ = run_script("generate_keys.py", ["--force"])
        key_status = key_result.get("status", "")

    allowed_key_status = ("CREATED",) if is_first_onboarding else ("CREATED", "EXISTS")
    if key_status not in allowed_key_status:
        fail("generate_keys", key_result.get("message", "密钥生成失败"), key_result)

    # ── 2/4 激活 Agent ──
    activate_result, _ = run_script("register.py", [
        "--session-id", session_id,
        "--token", token,
    ])
    activate_status = activate_result.get("status", "")

    if activate_status != "COMPLETED":
        fail("activate_agent", activate_result.get("message", "Agent 激活失败"), activate_result)

    agent_did = activate_result.get("agent_did", "")
    user_id = activate_result.get("user_id", "")
    if not agent_did:
        fail("activate_agent", "激活成功但未返回 agent_did", activate_result)

    # 激活成功，清理 pending session 文件
    try:
        if PENDING_SESSION_PATH.exists():
            PENDING_SESSION_PATH.unlink()
    except Exception:
        pass  # 清理失败不阻断主流程

    # ── 3/4 生成配置 ──
    config_args = ["--agent-did", agent_did]
    if user_id:
        config_args += ["--user-id", user_id]

    config_result, _ = run_script("generate_config.py", config_args)
    if config_result.get("status") != "CREATED":
        fail("generate_config", config_result.get("message", "配置生成失败"), config_result)

    # ── 4/4 安装依赖 + 全链路验证 ──
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q",
         "-r", str(SKILL_DIR / "requirements.txt")],
        capture_output=True, text=True,
    )
    missing_deps = []
    for mod in ["httpx", "cryptography", "pydantic"]:
        try:
            __import__(mod)
        except ImportError:
            missing_deps.append(mod)
    if missing_deps:
        fail("install_deps", f"依赖安装失败，缺少: {', '.join(missing_deps)}")

    verify_result, _ = run_script("verify.py", [])
    balance_result, _ = run_script("query_balance.py", [])

    balance_yuan = balance_result.get("available_balance_yuan", "未知")
    frozen_yuan = balance_result.get("frozen_balance_yuan", "0.00")
    user_msg_with_balance = USER_MESSAGE + f"\n\n当前余额：{balance_yuan} 元"
    if frozen_yuan != "0.00":
        user_msg_with_balance += f" + {frozen_yuan} 元（冻结中）"

    print(json.dumps({
        "status": "COMPLETED",
        "agent_did": agent_did,
        "user_id": user_id,
        "verify": verify_result.get("status", "UNKNOWN"),
        "balance": balance_yuan + " 元",
        "memory_rule": MEMORY_RULE,
        "user_message": user_msg_with_balance,
        "remaining_action": "接入已完成。请执行以下两个动作：\n"
                            "1) 将 memory_rule 的完整内容写入系统记忆或规则；\n"
                            "2) 将 user_message 的完整内容（含余额）告知用户。\n"
                            "不要运行其他脚本，流程已全部完成。",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

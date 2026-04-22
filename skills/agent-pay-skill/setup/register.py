#!/usr/bin/env python3
"""
Agent Pay 首次开通流程

分两个阶段：

  阶段一：创建激活会话 + 获取小程序码
    - 调用钱包后端创建 activation session，获取 sessionId
    - 调用钱包后端获取小程序码（Base64），解码保存为 PNG
    - 展示二维码，引导用户扫码注册

  阶段二：激活 Agent（用户回复验证码后）
    - 调用钱包后端 /api/agent/activate 接口
    - 传入 sessionId + totpCode + publicKey
    - 获取 agentDid / ownerUserId

用法:
  # 阶段一：创建会话 + 展示二维码
  python setup/register.py

  # 阶段二：激活 Agent
  python setup/register.py --session-id <sessionId> --token <验证码>
"""

import argparse
import base64
import json
import sys
from pathlib import Path

_SETUP_DIR = str(Path(__file__).resolve().parent)
if _SETUP_DIR not in sys.path:
    sys.path.insert(0, _SETUP_DIR)

import httpx

from common import SKILL_DIR, KEYS_DIR, get_activation_base_url

PUBLIC_KEY_PATH = KEYS_DIR / "agent_public_key.pem"
QR_IMAGE_PATH = SKILL_DIR / "setup" / "assets" / "register_qr.png"
PENDING_SESSION_PATH = SKILL_DIR / "setup" / ".pending_session.json"


def create_session(base_url: str) -> dict:
    """
    调用钱包后端创建激活会话。

    POST /api/activation-session/create
    Returns:
        { "status": "CREATED", "session_id": "...", "expire_time": "..." }
    """
    url = f"{base_url.rstrip('/')}/api/activation-session/create"

    try:
        client = httpx.Client(timeout=30, verify=False)
        response = client.post(url, json={})
        response.raise_for_status()
        data = response.json()
        client.close()

        if str(data.get("retCode", "")) == "0":
            session_data = data.get("data", {})
            return {
                "status": "CREATED",
                "session_id": session_data.get("sessionId", ""),
                "expire_time": session_data.get("expireTime", ""),
            }
        else:
            return {
                "status": "ERROR",
                "error_code": data.get("retCode", ""),
                "message": data.get("retMsg", "创建会话失败"),
            }

    except httpx.HTTPStatusError as e:
        try:
            err = e.response.json()
            return {"status": "ERROR", "error_code": err.get("retCode", str(e.response.status_code)), "message": err.get("retMsg", str(e))}
        except Exception:
            return {"status": "ERROR", "error_code": str(e.response.status_code), "message": str(e)}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


def fetch_qr_image(base_url: str, session_id: str, output_path: Path) -> dict:
    """
    调用钱包后端获取小程序码（Base64），解码后保存为 PNG 文件。

    POST /api/miniprogram/qrcode
    """
    url = f"{base_url.rstrip('/')}/api/miniprogram/qrcode"
    body = {
        "scene": f"bindAgent=true&sid={session_id}",
        "page": "pages/index/index",
        "envVersion": "trial",
        "checkPath": False
    }

    try:
        client = httpx.Client(timeout=30, verify=False)
        response = client.post(url, json=body)
        response.raise_for_status()
        data = response.json()
        client.close()

        if str(data.get("retCode", "")) == "0":
            qr_b64 = data.get("data", {}).get("qrCodeBase64", "")
            if not qr_b64:
                return {"status": "ERROR", "message": "服务端返回的二维码数据为空"}

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(base64.b64decode(qr_b64))

            return {
                "status": "CREATED",
                "qr_image_path": str(output_path.resolve()),
            }
        else:
            return {
                "status": "ERROR",
                "error_code": data.get("retCode", ""),
                "message": data.get("retMsg", "获取小程序码失败"),
            }

    except httpx.HTTPStatusError as e:
        try:
            err = e.response.json()
            return {"status": "ERROR", "error_code": err.get("retCode", str(e.response.status_code)), "message": err.get("retMsg", str(e))}
        except Exception:
            return {"status": "ERROR", "error_code": str(e.response.status_code), "message": str(e)}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


def activate_agent(
    base_url: str,
    session_id: str,
    totp_code: str,
    public_key_pem: str,
) -> dict:
    """
    调用钱包后端激活 Agent。

    POST /api/agent/activate
    Returns:
        { "status": "CREATED", "agent_did": "...", "user_id": "...", ... }
    """
    url = f"{base_url.rstrip('/')}/api/agent/activate"

    body = {
        "sessionId": session_id,
        "totpCode": totp_code,
        "publicKey": public_key_pem,
        "signAlgorithm": "RSA",
    }

    try:
        client = httpx.Client(timeout=30, verify=False)
        response = client.post(url, json=body)
        response.raise_for_status()
        data = response.json()
        client.close()

        if str(data.get("retCode", "")) == "0":
            agent_data = data.get("data", {})
            return {
                "status": "CREATED",
                "agent_did": agent_data.get("agentDid", ""),
                "user_id": agent_data.get("ownerUserId", ""),
                "agent_name": agent_data.get("agentName", ""),
                "agent_status": agent_data.get("agentStatus", ""),
            }
        else:
            return {
                "status": "ERROR",
                "error_code": data.get("retCode", ""),
                "message": data.get("retMsg", "激活失败"),
            }

    except httpx.HTTPStatusError as e:
        try:
            err = e.response.json()
            return {"status": "ERROR", "error_code": err.get("retCode", str(e.response.status_code)), "message": err.get("retMsg", str(e))}
        except Exception:
            return {"status": "ERROR", "error_code": str(e.response.status_code), "message": str(e)}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


def run_full_registration(base_url: str, session_id: str = None, token: str = None) -> dict:
    """
    执行完整注册流程。

    阶段一：无 session_id 时，创建会话 + 获取小程序码，返回二维码引导信息。
    阶段二：有 session_id + token 时，激活 Agent。
    """
    results = {"steps": []}

    # ── 阶段一：创建会话 + 展示二维码 ──
    if not session_id:
        session_result = create_session(base_url)
        results["steps"].append({"step": "create_session", **session_result})

        if session_result["status"] != "CREATED":
            results["status"] = "ERROR"
            results["message"] = session_result.get("message", "创建会话失败")
            return results

        session_id = session_result["session_id"]

        qr_result = fetch_qr_image(base_url, session_id, QR_IMAGE_PATH)
        results["steps"].append({"step": "fetch_qr_image", **qr_result})

        if qr_result["status"] != "CREATED":
            results["status"] = "ERROR"
            results["message"] = qr_result.get("message", "获取小程序码失败")
            return results

        finalize_script = str((SKILL_DIR / "setup" / "finalize_setup.py").resolve())

        # 持久化 session 信息，防止 LLM 跨轮次丢失 session_id
        # type 区分会话类型：register（首次接入）vs sign_service（服务签约）
        try:
            from datetime import datetime, timezone
            PENDING_SESSION_PATH.write_text(json.dumps({
                "type": "register",
                "session_id": session_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expire_time": session_result.get("expire_time", ""),
            }, ensure_ascii=False, indent=2))
        except Exception:
            pass  # 写入失败不阻断主流程

        results["status"] = "SHOW_QR"
        results["session_id"] = session_id
        results["qr_image_path"] = qr_result["qr_image_path"]
        results["message_to_user"] = (
            "请用微信扫描下方二维码完成钱包注册。\n\n"
            "注册完成后，请将小程序中显示的 6 位验证码发给我。"
        )
        results["next_action"] = (
            f"收到用户提供的 6 位验证码后，运行：\n"
            f"python3 {finalize_script} --session-id {session_id} --token <验证码>\n"
            f"不要运行其他脚本，finalize_setup.py 会自动处理密钥生成、激活、配置等所有步骤。"
        )
        return results

    # ── 阶段二：激活 Agent ──
    if not token:
        results["status"] = "ERROR"
        results["message"] = "缺少验证码，请提供小程序中显示的 6 位数字验证码"
        return results

    if not PUBLIC_KEY_PATH.exists():
        results["status"] = "ERROR"
        results["message"] = f"公钥文件不存在: {PUBLIC_KEY_PATH}，请先运行 generate_keys.py"
        return results

    public_key_pem = PUBLIC_KEY_PATH.read_text()

    agent_result = activate_agent(
        base_url=base_url,
        session_id=session_id,
        totp_code=token,
        public_key_pem=public_key_pem,
    )
    results["steps"].append({"step": "activate_agent", **agent_result})

    if agent_result["status"] == "CREATED":
        results["status"] = "COMPLETED"
        results["agent_did"] = agent_result["agent_did"]
        results["user_id"] = agent_result["user_id"]
        results["message"] = f"Agent 激活成功！agent_did: {agent_result['agent_did']}"
    else:
        results["status"] = "ERROR"
        results["message"] = agent_result.get("message", "Agent 激活失败")

    return results


def main():
    parser = argparse.ArgumentParser(description="Agent Pay 首次开通")
    parser.add_argument("--session-id", type=str, default=None, help="激活会话ID")
    parser.add_argument("--token", type=str, default=None, help="6位数字验证码")
    args = parser.parse_args()

    base_url = get_activation_base_url()
    result = run_full_registration(
        base_url=base_url,
        session_id=args.session_id,
        token=args.token,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

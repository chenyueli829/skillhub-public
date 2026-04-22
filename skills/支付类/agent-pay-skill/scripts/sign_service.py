#!/usr/bin/env python3
"""
L3 服务签约流程

用法:
  python3 scripts/sign_service.py --payee-did <收款方Agent DID>
  python3 scripts/sign_service.py --payee-did "did:agent:seller-001"
  python3 scripts/sign_service.py --payee <收款方服务名>

流程:
  1. 读取配置获取 agent_id
  2. 调用 wallet 创建签约会话:
     POST /api/activation-session/create
     body: { sessionType: "AUTHORIZE", agentId, payeeAgentDid, expireMinutes: 30 }
  3. 获取小程序码
  4. 返回 { qr_image_path, session_id, message_to_user }
     引导用户扫码在小程序端完成 L3 服务签约（设置额度、确认模式等）

注意：无需 finalize 脚本，用户在小程序端完成签约后，直接重新执行 authorize.py 即可。
"""

import argparse
import base64
import json
import sys
from pathlib import Path

# 将 lib 和 setup 加入 Python 路径
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "lib"))
sys.path.insert(0, str(SKILL_DIR / "setup"))

import httpx

from common import get_activation_base_url, load_config
from agent_pay.wallet_client import AIWalletClient
from agent_pay.config import Config

QR_IMAGE_PATH = SKILL_DIR / "setup" / "assets" / "sign_service_qr.png"


def create_sign_session(base_url: str, agent_id: str, payee_agent_did: str) -> dict:
    """
    调用钱包后端创建签约会话。

    POST /api/activation-session/create
    body: { sessionType: "AUTHORIZE", agentId, payeeAgentDid, expireMinutes: 30 }
    """
    url = f"{base_url.rstrip('/')}/api/activation-session/create"
    body = {
        "sessionType": "AUTHORIZE",
        "agentId": agent_id,
        "payeeAgentDid": payee_agent_did,
        "expireMinutes": 30,
    }

    try:
        client = httpx.Client(timeout=30, verify=False)
        response = client.post(url, json=body)
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
                "message": data.get("retMsg", "创建签约会话失败"),
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
        "scene": f"signPayeeAgent=true&sid={session_id}",
        "page": "pages/index/index",
        "envVersion": "trial",
        "checkPath": False,
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


def main():
    parser = argparse.ArgumentParser(description="L3 服务签约")
    parser.add_argument("--payee-did", type=str, default=None, help="收款方Agent DID")
    parser.add_argument("--payee", type=str, default=None, help="收款方服务名称（会自动查DID）")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    if not args.payee_did and not args.payee:
        print(json.dumps({"success": False, "error_message": "必须指定 --payee-did 或 --payee"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 加载配置
    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")
    config = Config.load(config_path if Path(config_path).exists() else None)

    # 解析收款方 DID
    payee_did = args.payee_did
    if not payee_did:
        wallet_client = AIWalletClient(config.ai_wallet)
        try:
            payee_did = wallet_client.query_agent_by_name(args.payee)
        except ValueError as e:
            print(json.dumps({"success": False, "error_message": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # 获取 agent_did 作为 agentId
    agent_id = config.agent.agent_did

    # 创建签约会话
    base_url = get_activation_base_url()
    session_result = create_sign_session(base_url, agent_id, payee_did)

    if session_result["status"] != "CREATED":
        result = {
            "success": False,
            "error_message": session_result.get("message", "创建签约会话失败"),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    session_id = session_result["session_id"]

    # 获取小程序码
    qr_result = fetch_qr_image(base_url, session_id, QR_IMAGE_PATH)

    if qr_result["status"] != "CREATED":
        result = {
            "success": False,
            "error_message": qr_result.get("message", "获取小程序码失败"),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 输出结果
    result = {
        "success": True,
        "session_id": session_id,
        "qr_image_path": qr_result["qr_image_path"],
        "message_to_user": (
            "请用微信扫描下方二维码，在小程序中完成服务签约。\n\n"
            "签约时可以设置：\n"
            "• 单笔限额\n"
            "• 每日/每月累计限额\n"
            "• 确认模式（自动放行或笔笔确认）\n\n"
            "签约完成后请告诉我，我将重新申请授权凭证。"
        ),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()

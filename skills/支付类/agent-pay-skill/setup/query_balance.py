#!/usr/bin/env python3
"""
查询用户钱包余额

通过 Agent Pay 后端的 /api/v1/balance/query 接口查询（需 KYA 签名）。
后端地址和 user_id 从 config.json 读取。

用法:
  python setup/query_balance.py
  python setup/query_balance.py --user-id <user_id>
"""

import argparse
import json
import sys
from pathlib import Path

_SETUP_DIR = str(Path(__file__).resolve().parent)
if _SETUP_DIR not in sys.path:
    sys.path.insert(0, _SETUP_DIR)

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "lib"))

from common import get_user_id, load_config


def query_balance(user_id: str, config_path: str = None) -> dict:
    """
    通过 AgentPayClient 查询用户钱包余额（带 KYA 签名）。
    """
    from agent_pay.config import Config
    from agent_pay.client import AgentPayClient
    from agent_pay.crypto import create_signer

    try:
        config = Config.load(config_path)
    except Exception as e:
        return {"status": "ERROR", "message": f"加载配置失败: {e}"}

    try:
        signer = create_signer(config)
        client = AgentPayClient(config.agent_pay, signer)
        result = client.query_balance(user_id)
        client.close()
        return result
    except Exception as e:
        return {"status": "ERROR", "message": f"查询余额失败: {e}"}


def main():
    parser = argparse.ArgumentParser(description="查询用户钱包余额")
    parser.add_argument("--user-id", type=str, default=None, help="用户ID（不传则从 config.json 读取）")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    config, _ = load_config()
    user_id = args.user_id or get_user_id(config)
    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")

    if not user_id:
        print(json.dumps({"status": "ERROR", "message": "未提供 user_id，且 config.json 中也没有"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = query_balance(user_id, config_path if Path(config_path).exists() else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "OK" else 1)


if __name__ == "__main__":
    main()

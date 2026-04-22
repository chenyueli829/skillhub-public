#!/usr/bin/env python3
"""
Agent Pay 配置文件生成

根据注册结果生成 lib/config.json。
后端地址从 lib/agent_pay/config.py 的默认值读取（唯一定义处）。

用法: python setup/generate_config.py --agent-did <did> [--user-id <id>]
"""

import argparse
import json
import sys
from pathlib import Path

_SETUP_DIR = str(Path(__file__).resolve().parent)
if _SETUP_DIR not in sys.path:
    sys.path.insert(0, _SETUP_DIR)

from common import LIB_DIR, CONFIG_PATH, _load_defaults, get_signer_binary_path


def generate_config(
    agent_did: str,
    user_id: str = "",
) -> dict:
    """生成 config.json 配置文件。"""
    defaults = _load_defaults()
    signer_binary_path = get_signer_binary_path()

    config = {
        "agent": {
            "agent_did": agent_did,
            "signer_binary_path": signer_binary_path,
        },
        "user_id": user_id,
        "agent_pay": {
            "base_url": defaults["agent_pay_base_url"],
            "timeout": 30,
            "api_prefix": "/api/v1",
        },
        "ai_wallet": {
            "base_url": defaults["ai_wallet_base_url"],
            "timeout": 30,
        },
        "log_level": "INFO",
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return {
        "status": "CREATED",
        "config_path": str(CONFIG_PATH),
        "config": config,
    }


def main():
    parser = argparse.ArgumentParser(description="Agent Pay 配置生成")
    parser.add_argument("--agent-did", type=str, required=True, help="Agent DID")
    parser.add_argument("--user-id", type=str, default="", help="用户ID")
    args = parser.parse_args()

    result = generate_config(
        agent_did=args.agent_did,
        user_id=args.user_id,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

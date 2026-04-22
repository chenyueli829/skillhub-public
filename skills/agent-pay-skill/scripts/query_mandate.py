#!/usr/bin/env python3
"""
查询凭证确认状态

用法:
  python3 scripts/query_mandate.py --mandate-id <凭证ID>

用途：
  CONFIRM_EACH 模式下，authorize.py 返回 confirm_status=PENDING_CONFIRM 后，
  用户在小程序中确认支付，然后运行本脚本查询凭证状态。

  - PENDING_CONFIRM → 用户尚未确认，稍后再试
  - CONFIRMED → 确认完成，返回 authorization_mandate
  - TIMEOUT → 凭证已超时，需重新申请
"""

import argparse
import json
import sys
from pathlib import Path

# 将 lib 加入 Python 路径
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "lib"))

from agent_pay.config import Config
from agent_pay.client import AgentPayClient
from agent_pay.crypto import create_signer
from agent_pay.models import MandateQueryRequest


def main():
    parser = argparse.ArgumentParser(description="查询凭证确认状态")
    parser.add_argument("--mandate-id", type=str, required=True, help="凭证ID")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    # 加载配置
    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")
    config = Config.load(config_path if Path(config_path).exists() else None)

    # 初始化客户端
    signer = create_signer(config)
    client = AgentPayClient(config.agent_pay, signer)

    # 查询凭证状态
    request = MandateQueryRequest(mandate_id=args.mandate_id)
    response = client.query_mandate(request)

    # 构建输出
    result = {"success": response.success}
    if response.success:
        result["mandate_id"] = response.mandate_id
        result["confirm_status"] = response.confirm_status

        if response.confirm_status == "CONFIRMED" and response.authorization_mandate:
            result["authorization_mandate"] = response.authorization_mandate
            result["message"] = "用户已确认，凭证可用"
        elif response.confirm_status == "PENDING_CONFIRM":
            result["message"] = "用户尚未确认，请稍后再试"
        elif response.confirm_status == "TIMEOUT":
            result["message"] = "凭证已超时，需重新申请授权"
        else:
            result["message"] = f"当前状态: {response.confirm_status}"
    else:
        result["error_code"] = response.error_code
        result["error_message"] = response.error_message

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()

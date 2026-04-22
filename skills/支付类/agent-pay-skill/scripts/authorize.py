#!/usr/bin/env python3
"""
申请授权凭证（L3 统一流程）

用法:
  python3 scripts/authorize.py --amount <金额分> --payee <收款方服务名或DID>
  python3 scripts/authorize.py --amount 500 --payee "财务分析"
  python3 scripts/authorize.py --amount 500 --payee "did:agent:seller-001"

流程：
  1. 解析收款方（服务名 → DID 查询）
  2. 调用后端 /api/v1/intent/authorize（传 payee_agent_did + amount）
  3. 后端自动基于 L3 签约关系处理
  4. 根据 confirm_mode 返回不同结果：
     - AUTO_WITHIN_QUOTA → 直接返回 authorization_mandate
     - CONFIRM_EACH → 返回 mandate_id + confirm_status=PENDING_CONFIRM（需用户在小程序确认）

错误码说明：
  - 60001 (QUOTA_NOT_FOUND) → 未签约，需先执行 sign_service.py 签约
  - 60004 (AMOUNT_EXCEED_QUOTA) → 超出签约额度
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
from agent_pay.models import AuthorizeIntentRequest
from agent_pay.wallet_client import AIWalletClient


def main():
    parser = argparse.ArgumentParser(description="申请授权凭证（L3统一流程）")
    parser.add_argument("--amount", type=int, required=True, help="授权金额（分）")
    parser.add_argument("--payee", type=str, required=True,
                        help="收款方服务名称或Agent DID（did:agent:开头）")
    parser.add_argument("--currency", type=str, default="CNY", help="币种")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    # 加载配置
    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")
    config = Config.load(config_path if Path(config_path).exists() else None)

    # 初始化客户端
    signer = create_signer(config)
    client = AgentPayClient(config.agent_pay, signer)
    wallet_client = AIWalletClient(config.ai_wallet)

    # 解析收款方 DID
    payee = args.payee.strip()
    if payee.startswith("did:agent:"):
        payee_did = payee
    else:
        try:
            payee_did = wallet_client.query_agent_by_name(payee)
        except ValueError as e:
            print(json.dumps({"success": False, "error_message": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)

    # 构建请求（L3 统一流程：payee_agent_did + amount）
    user_id = config.user_id
    request = AuthorizeIntentRequest(
        user_id=user_id,
        payee_agent_did=payee_did,
        amount=args.amount,
        currency=args.currency,
    )

    response = client.authorize_intent(request)

    # 构建输出
    result = {"success": response.success}
    if response.success:
        result["mandate_master_id"] = response.mandate_master_id
        result["confirm_mode"] = response.confirm_mode
        result["confirm_status"] = response.confirm_status

        if response.authorization_mandate:
            # AUTO_WITHIN_QUOTA 模式：直接返回凭证
            result["authorization_mandate"] = response.authorization_mandate
        else:
            # CONFIRM_EACH 模式：不返回凭证，需用户在小程序确认后通过 query_mandate.py 查询
            result["message"] = "用户需要在小程序中确认本次支付，确认后请运行 query_mandate.py 查询凭证"
    else:
        result["error_code"] = response.error_code
        result["error_message"] = response.error_message

        # 特殊错误码提示
        if response.error_code == "60001":
            result["hint"] = "未签约授权关系，请先运行 sign_service.py 完成服务签约"
        elif response.error_code == "60004":
            result["hint"] = "金额超过签约额度，请减少金额或重新签约"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()

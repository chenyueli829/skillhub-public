#!/usr/bin/env python3
"""
冻结资金

用法:
  python3 scripts/lock.py --mandate <JWT凭证> --amount <金额分>
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "lib"))

from agent_pay.config import Config
from agent_pay.client import AgentPayClient
from agent_pay.crypto import create_signer
from agent_pay.models import LockFundsRequest


def main():
    parser = argparse.ArgumentParser(description="冻结资金")
    parser.add_argument("--mandate", type=str, required=True, help="JWT授权凭证")
    parser.add_argument("--amount", type=int, required=True, help="冻结金额（分）")
    parser.add_argument("--description", type=str, default="商品预付款", help="冻结说明")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")
    config = Config.load(config_path if Path(config_path).exists() else None)

    signer = create_signer(config)
    client = AgentPayClient(config.agent_pay, signer)

    request_id = f"req-{int(datetime.now(timezone.utc).timestamp() * 1000)}-{uuid.uuid4().hex[:8]}"
    merchant_order_no = f"ORD{int(datetime.now(timezone.utc).timestamp() * 1000)}"

    request = LockFundsRequest(
        request_id=request_id,
        authorization_mandate=args.mandate,
        preauth_amount=args.amount,
        description=args.description,
        merchant_order_no=merchant_order_no,
    )

    response = client.lock_funds(request)

    result = {"success": response.success}
    if response.success:
        result.update({
            "payment_order_id": response.payment_order_id,
            "biz_order_no": response.biz_order_no,
            "frozen_amount": response.frozen_amount,
        })
    else:
        result.update({
            "error_code": response.error_code,
            "error_message": response.error_message,
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()

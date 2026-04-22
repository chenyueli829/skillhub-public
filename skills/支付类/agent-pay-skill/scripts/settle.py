#!/usr/bin/env python3
"""
结算支付

用法:
  python3 scripts/settle.py --mandate <JWT凭证> --amount <金额分>
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
from agent_pay.models import SettlePaymentRequest


def main():
    parser = argparse.ArgumentParser(description="结算支付")
    parser.add_argument("--mandate", type=str, required=True, help="JWT授权凭证")
    parser.add_argument("--amount", type=int, required=True, help="结算金额（分）")
    parser.add_argument("--proof", type=str, default="服务已完成", help="消费凭证")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径")
    args = parser.parse_args()

    config_path = args.config or str(SKILL_DIR / "lib" / "config.json")
    config = Config.load(config_path if Path(config_path).exists() else None)

    signer = create_signer(config)
    client = AgentPayClient(config.agent_pay, signer)

    request_id = f"req-{int(datetime.now(timezone.utc).timestamp() * 1000)}-{uuid.uuid4().hex[:8]}"

    request = SettlePaymentRequest(
        request_id=request_id,
        authorization_mandate=args.mandate,
        final_amount=args.amount,
        consumption_proof=args.proof,
    )

    response = client.settle_payment(request)

    result = {"success": response.success}
    if response.success:
        result.update({
            "payment_order_id": response.payment_order_id,
            "flow_no": response.flow_no,
            "settled_amount": response.settled_amount,
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

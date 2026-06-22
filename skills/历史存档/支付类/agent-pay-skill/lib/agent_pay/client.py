"""
HTTP Client for Agent Pay Service.

负责与 Agent Pay 后端通信：
- authorize_intent（授权）
- lock_funds / custodial_lock_funds（冻结）
- settle_payment / custodial_settle_payment（结算）
- query_balance（余额查询）

所有请求使用 Agent 私钥签名（MPP1.0 协议）。
Agent 名称查询等非支付操作由 AIWalletClient 负责。
"""

import logging
from typing import Any

import httpx

from .config import AgentPayConfig
from .crypto import BinaryAgentSigner
from .models import (
    AuthorizeIntentRequest,
    AuthorizeIntentResponse,
    CustodialLockFundsRequest,
    CustodialSettlePaymentRequest,
    LockFundsRequest,
    LockFundsResponse,
    MandateQueryRequest,
    MandateQueryResponse,
    SettlePaymentRequest,
    SettlePaymentResponse,
)

logger = logging.getLogger(__name__)


class AgentPayClient:
    """Agent Pay 支付服务 HTTP 客户端。"""
    
    def __init__(self, config: AgentPayConfig, signer: BinaryAgentSigner):
        self.config = config
        self.signer = signer
        self._client = httpx.Client(timeout=config.timeout)
    
    def _make_request(
        self,
        method: str,
        url: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Make an authenticated request to Agent Pay service.
        
        签名和发送必须使用同一份序列化后的body字节流，
        确保签名payload与实际发送的body完全一致。
        
        Args:
            method: HTTP method
            url: Full URL
            body: Request body
        
        Returns:
            Response JSON as dictionary
        
        Raises:
            httpx.HTTPStatusError: If request fails
        """
        import json
        
        # 关键：只序列化一次body，签名和发送都用这同一份
        body_json_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
        body_bytes = body_json_str.encode('utf-8')
        
        # 使用预序列化的JSON字符串进行签名
        signature_headers = self.signer.sign_request(body, body_json_str=body_json_str)
        
        headers = {
            "Content-Type": "application/json",
            **signature_headers,
        }
        
        logger.info(f"Making {method} request to {url}")
        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request body: {body_json_str}")
        
        # 使用content参数发送预序列化的body，而非json参数（避免二次序列化）
        response = self._client.request(method, url, content=body_bytes, headers=headers)
        
        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, response_data: dict) -> tuple[bool, str, str, dict]:
        """
        解析服务端统一响应格式。
        
        服务端响应格式: {"code": "0", "message": "success", "data": {...}, "timestamp": ...}
        code为"0"表示成功，其他为业务错误。
        
        Returns:
            (success, error_code, error_message, data)
        """
        code = str(response_data.get("code", ""))
        message = response_data.get("message", "")
        data = response_data.get("data", {})
        
        if code == "0":
            return True, "", "", data if isinstance(data, dict) else {}
        else:
            return False, code, message, {}

    def authorize_intent(self, request: AuthorizeIntentRequest) -> AuthorizeIntentResponse:
        """
        Authorize a payment intent.
        
        This is typically called by a buyer agent to get authorization
        from a user to spend funds.
        
        Args:
            request: Authorization request details
        
        Returns:
            Authorization response with mandate details
        """
        body = request.model_dump(exclude_none=True, mode="json")
        
        try:
            response_data = self._make_request(
                "POST",
                self.config.authorize_intent_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return AuthorizeIntentResponse(
                    success=True,
                    mandate_master_id=data.get("mandate_id") or data.get("mandateId"),
                    authorization_mandate=data.get("authorization_mandate") or data.get("authorizationMandate"),
                    confirm_mode=data.get("confirm_mode") or data.get("confirmMode"),
                    confirm_status=data.get("confirm_status") or data.get("confirmStatus"),
                )
            else:
                return AuthorizeIntentResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return AuthorizeIntentResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to authorize intent")
            return AuthorizeIntentResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )
    
    def lock_funds(self, request: LockFundsRequest) -> LockFundsResponse:
        """
        Lock/freeze funds for a transaction.
        
        This is typically called by a seller agent after receiving
        authorization from a buyer agent.
        
        Args:
            request: Lock funds request details
        
        Returns:
            Lock response with transaction details
        """
        body = request.model_dump(exclude_none=True, mode="json")
        
        try:
            response_data = self._make_request(
                "POST",
                self.config.lock_funds_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return LockFundsResponse(
                    success=True,
                    payment_order_id=data.get("paymentOrderId") or data.get("payment_order_id"),
                    biz_order_no=data.get("bizOrderNo") or data.get("biz_order_no"),
                    frozen_amount=data.get("frozenAmount") or data.get("frozen_amount"),
                )
            else:
                return LockFundsResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return LockFundsResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to lock funds")
            return LockFundsResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )
    
    def settle_payment(self, request: SettlePaymentRequest) -> SettlePaymentResponse:
        """
        Settle/capture a payment from frozen funds.
        
        This is typically called by a seller agent after service delivery
        to claim the frozen funds.
        
        Args:
            request: Settle request details
        
        Returns:
            Settle response with settlement details
        """
        body = request.model_dump(exclude_none=True, mode="json")
        
        try:
            response_data = self._make_request(
                "POST",
                self.config.settle_payment_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return SettlePaymentResponse(
                    success=True,
                    payment_order_id=data.get("paymentOrderId") or data.get("payment_order_id"),
                    flow_no=data.get("flowNo") or data.get("flow_no"),
                    settled_amount=data.get("settledAmount") or data.get("settled_amount"),
                )
            else:
                return SettlePaymentResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return SettlePaymentResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to settle payment")
            return SettlePaymentResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )
    
    def custodial_lock_funds(self, request: CustodialLockFundsRequest) -> LockFundsResponse:
        """
        Lock/freeze funds in custodial mode.
        
        Called by a platform agent on behalf of a payee agent.
        Uses the same backend endpoint as lock_funds, with payee_agent_did in body.
        """
        body = request.model_dump(exclude_none=True, mode="json")
        
        try:
            response_data = self._make_request(
                "POST",
                self.config.lock_funds_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return LockFundsResponse(
                    success=True,
                    payment_order_id=data.get("paymentOrderId") or data.get("payment_order_id"),
                    biz_order_no=data.get("bizOrderNo") or data.get("biz_order_no"),
                    frozen_amount=data.get("frozenAmount") or data.get("frozen_amount"),
                )
            else:
                return LockFundsResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return LockFundsResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to custodial lock funds")
            return LockFundsResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )

    def custodial_settle_payment(self, request: CustodialSettlePaymentRequest) -> SettlePaymentResponse:
        """
        Settle/capture payment in custodial mode.
        
        Called by a platform agent on behalf of a payee agent.
        Uses the same backend endpoint as settle_payment, with payee_agent_did in body.
        """
        body = request.model_dump(exclude_none=True, mode="json")
        
        try:
            response_data = self._make_request(
                "POST",
                self.config.settle_payment_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return SettlePaymentResponse(
                    success=True,
                    payment_order_id=data.get("paymentOrderId") or data.get("payment_order_id"),
                    flow_no=data.get("flowNo") or data.get("flow_no"),
                    settled_amount=data.get("settledAmount") or data.get("settled_amount"),
                )
            else:
                return SettlePaymentResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return SettlePaymentResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to custodial settle payment")
            return SettlePaymentResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )

    def query_mandate(self, request: MandateQueryRequest) -> MandateQueryResponse:
        """
        Query mandate status (CONFIRM_EACH 场景下 Skill 轮询凭证确认状态).

        Args:
            request: Query request with mandate_id

        Returns:
            MandateQueryResponse with confirm_status and (if confirmed) authorization_mandate
        """
        body = request.model_dump(exclude_none=True, mode="json")

        try:
            response_data = self._make_request(
                "POST",
                self.config.mandate_query_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return MandateQueryResponse(
                    success=True,
                    mandate_id=data.get("mandate_id") or data.get("mandateId"),
                    confirm_status=data.get("confirm_status") or data.get("confirmStatus"),
                    authorization_mandate=data.get("authorization_mandate") or data.get("authorizationMandate"),
                    signature_algorithm=data.get("signature_algorithm") or data.get("signatureAlgorithm"),
                    signer_identity=data.get("signer_identity") or data.get("signerIdentity"),
                )
            else:
                return MandateQueryResponse(
                    success=False,
                    error_code=error_code,
                    error_message=error_message,
                )
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return MandateQueryResponse(
                success=False,
                error_code=error_body.get("code", str(e.response.status_code)),
                error_message=error_body.get("message", str(e)),
            )
        except Exception as e:
            logger.exception("Failed to query mandate")
            return MandateQueryResponse(
                success=False,
                error_code="CLIENT_ERROR",
                error_message=str(e),
            )

    def query_balance(self, user_id: str) -> dict:
        """
        Query user balance via Agent Pay backend.

        Requires KYA authentication (request is signed with agent private key).

        Args:
            user_id: User ID to query balance for

        Returns:
            {"status": "OK", "available_balance": ..., ...} or {"status": "ERROR", ...}
        """
        body = {"userId": user_id}

        try:
            response_data = self._make_request(
                "POST",
                self.config.balance_query_url,
                body,
            )
            success, error_code, error_message, data = self._parse_response(response_data)
            if success:
                return {
                    "status": "OK",
                    "user_id": user_id,
                    "available_balance": data.get("availableBalance", 0),
                    "available_balance_yuan": f"{data.get('availableBalance', 0) / 100:.2f}",
                    "frozen_balance": data.get("frozenBalance", 0),
                    "frozen_balance_yuan": f"{data.get('frozenBalance', 0) / 100:.2f}",
                    "total_balance": data.get("totalBalance", 0),
                    "currency": data.get("currency", "CNY"),
                }
            else:
                return {
                    "status": "ERROR",
                    "error_code": error_code,
                    "message": error_message,
                }
        except httpx.HTTPStatusError as e:
            error_body = e.response.json() if e.response.content else {}
            return {
                "status": "ERROR",
                "error_code": error_body.get("code", str(e.response.status_code)),
                "message": error_body.get("message", str(e)),
            }
        except Exception as e:
            logger.exception("Failed to query balance")
            return {"status": "ERROR", "error_code": "CLIENT_ERROR", "message": str(e)}

    def close(self):
        """Close the HTTP client."""
        self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

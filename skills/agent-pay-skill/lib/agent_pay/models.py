"""
Data models for Agent Pay MCP Server.
Defines request/response structures for Agent Pay API.
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ============ Enums ============

class FailurePolicy(str, Enum):
    """Policy for handling authorization failures."""
    FAIL_FAST = "FAIL_FAST"
    RETRY_WITH_LIMIT = "RETRY_WITH_LIMIT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class SignatureAlgorithm(str, Enum):
    """Signature algorithm types."""
    RS256 = "RS256"
    ES256 = "ES256"
    HS256 = "HS256"


# ============ Authorize Intent ============

class MandateDetailRequest(BaseModel):
    """Single mandate detail for a payee agent. (Deprecated: 仅用于兼容旧逻辑)"""
    session_id: str = Field(..., description="会话ID")
    payee_agent_did: str = Field(..., description="卖方Agent DID")
    max_single_amount: int = Field(..., description="单笔最大授权金额（分）")
    max_total_amount: int = Field(..., description="总最大授权金额（分）")
    price_tolerance: int = Field(default=0, description="价格容差（分）")
    on_failure_policy: FailurePolicy = Field(
        default=FailurePolicy.FAIL_FAST,
        description="失败策略"
    )


class AuthorizeIntentRequest(BaseModel):
    """Request to authorize a payment intent (L3 统一流程)."""
    user_id: str = Field(..., description="授权用户ID")
    payee_agent_did: str = Field(..., description="收款方Agent DID（必填）")
    amount: int = Field(..., description="本次报价金额（分，必填）")
    currency: str = Field(default="CNY", description="币种")


class MandateDetailResponse(BaseModel):
    """Response for a single mandate detail."""
    mandate_detail_id: Optional[str] = Field(default=None, alias="mandateDetailId", description="授权凭证明细ID")
    payee_agent_did: Optional[str] = Field(default=None, alias="payeeAgentDid", description="卖方Agent DID")
    max_amount: Optional[int] = Field(default=None, alias="maxAmount", description="最大授权金额")
    available_amount: Optional[int] = Field(default=None, alias="availableAmount", description="可用金额")
    status: Optional[str] = Field(default=None, description="状态")

    model_config = {"populate_by_name": True}


class AuthorizeIntentResponse(BaseModel):
    """Response for authorize intent request."""
    success: bool = Field(..., description="是否成功")
    mandate_master_id: Optional[str] = Field(default=None, description="授权凭证主ID")
    authorization_mandate: Optional[str] = Field(default=None, description="授权凭证（AUTO_WITHIN_QUOTA模式返回，CONFIRM_EACH模式为null）")
    confirm_mode: Optional[str] = Field(default=None, description="确认模式（CONFIRM_EACH/AUTO_WITHIN_QUOTA）")
    confirm_status: Optional[str] = Field(default=None, description="确认状态（PENDING_CONFIRM/CONFIRMED/TIMEOUT）")
    error_code: Optional[str] = Field(default=None, description="错误码")
    error_message: Optional[str] = Field(default=None, description="错误信息")


# ============ Lock Funds ============

class LockFundsRequest(BaseModel):
    """Request to lock/freeze funds."""
    request_id: Optional[str] = Field(default=None, description="请求ID，用于幂等性控制，不传则自动生成")
    authorization_mandate: str = Field(..., description="JWT授权凭证")
    preauth_amount: int = Field(..., description="预授权冻结金额（分）")
    description: Optional[str] = Field(default=None, description="冻结说明")
    merchant_order_no: Optional[str] = Field(default=None, description="商户订单号")


class LockFundsResponse(BaseModel):
    """Response for lock funds request."""
    success: bool = Field(..., description="是否成功")
    payment_order_id: Optional[str] = Field(default=None, description="支付订单号")
    biz_order_no: Optional[str] = Field(default=None, description="业务订单号")
    frozen_amount: Optional[int] = Field(default=None, description="已冻结金额（分）")
    error_code: Optional[str] = Field(default=None, description="错误码")
    error_message: Optional[str] = Field(default=None, description="错误信息")


# ============ Settle Payment ============

class SettlePaymentRequest(BaseModel):
    """Request to settle/capture payment."""
    request_id: Optional[str] = Field(default=None, description="请求ID，用于幂等性控制，不传则自动生成")
    authorization_mandate: str = Field(..., description="JWT授权凭证")
    final_amount: int = Field(..., description="结算金额（分）")
    consumption_proof: Optional[str] = Field(default=None, description="消费证明")


# ============ Custodial Mode (托管支付模式) ============

class CustodialLockFundsRequest(BaseModel):
    """Request to lock/freeze funds in custodial mode (platform agent on behalf of payee)."""
    request_id: Optional[str] = Field(default=None, description="请求ID，用于幂等性控制，不传则自动生成")
    authorization_mandate: str = Field(..., description="JWT授权凭证")
    preauth_amount: int = Field(..., description="预授权冻结金额（分）")
    payee_agent_did: str = Field(..., description="收款方Agent DID（托管模式必填）")
    description: Optional[str] = Field(default=None, description="冻结说明")
    merchant_order_no: Optional[str] = Field(default=None, description="商户订单号")


class CustodialSettlePaymentRequest(BaseModel):
    """Request to settle/capture payment in custodial mode (platform agent on behalf of payee)."""
    request_id: Optional[str] = Field(default=None, description="请求ID，用于幂等性控制，不传则自动生成")
    authorization_mandate: str = Field(..., description="JWT授权凭证")
    final_amount: int = Field(..., description="结算金额（分）")
    payee_agent_did: str = Field(..., description="收款方Agent DID（托管模式必填）")
    consumption_proof: Optional[str] = Field(default=None, description="消费证明")


# ============ Settle Payment Response ============

class SettlePaymentResponse(BaseModel):
    """Response for settle payment request."""
    success: bool = Field(..., description="是否成功")
    payment_order_id: Optional[str] = Field(default=None, description="支付订单号")
    flow_no: Optional[str] = Field(default=None, description="流水号")
    settled_amount: Optional[int] = Field(default=None, description="已结算金额（分）")
    error_code: Optional[str] = Field(default=None, description="错误码")
    error_message: Optional[str] = Field(default=None, description="错误信息")


# ============ Mandate Query (凭证查询) ============

class MandateQueryRequest(BaseModel):
    """Request to query mandate status (CONFIRM_EACH 场景下 Skill 轮询)."""
    mandate_id: str = Field(..., description="凭证ID")


class MandateQueryResponse(BaseModel):
    """Response for mandate query request."""
    success: bool = Field(..., description="是否成功")
    mandate_id: Optional[str] = Field(default=None, description="凭证ID")
    confirm_status: Optional[str] = Field(default=None, description="确认状态（PENDING_CONFIRM/CONFIRMED/TIMEOUT）")
    authorization_mandate: Optional[str] = Field(default=None, description="授权凭证（仅CONFIRMED时返回）")
    signature_algorithm: Optional[str] = Field(default=None, description="签名算法")
    signer_identity: Optional[str] = Field(default=None, description="签名者身份")
    error_code: Optional[str] = Field(default=None, description="错误码")
    error_message: Optional[str] = Field(default=None, description="错误信息")

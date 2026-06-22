"""
Configuration management for Agent Pay.

两个后端服务：
- Agent Pay (agent_pay): 支付主流程（授权、冻结、结算）+ 注册、余额查询
- AI Wallet (ai_wallet): 钱包平台服务 — 查询Agent等（逐步迁移中）

Supports loading from environment variables and config file.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

AGENT_PAY_BASE_URL = "http://134.175.226.175:8290"
AI_WALLET_BASE_URL = "http://42.193.255.10:8000"

_CONFIG_SEARCH_PATHS = [
    "config.json",
    os.path.join(os.path.dirname(__file__), "..", "..", "config.json"),
]


@dataclass
class AgentIdentity:
    """Agent identity configuration."""

    agent_did: str
    """Agent's DID (Decentralized Identifier), e.g., 'did:agent:seller-agent-001'"""

    signer_binary_path: str
    """Path to the compiled signer binary (software HSM)."""

    def __post_init__(self):
        if not self.agent_did:
            raise ValueError("agent_did is required")
        if not self.signer_binary_path:
            raise ValueError("signer_binary_path is required")
        p = Path(self.signer_binary_path)
        if not p.exists():
            raise FileNotFoundError(f"Signer binary not found: {self.signer_binary_path}")
        if not os.access(str(p), os.X_OK):
            raise PermissionError(f"Signer binary is not executable: {self.signer_binary_path}")


@dataclass
class AgentPayConfig:
    """Agent Pay 服务配置 — 授权/冻结/结算/注册/余额查询。"""

    base_url: str = AGENT_PAY_BASE_URL
    timeout: float = 30.0
    api_prefix: str = "/api/v1"

    @property
    def authorize_intent_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/intent/authorize"

    @property
    def lock_funds_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/payment/lock"

    @property
    def settle_payment_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/payment/settle"

    @property
    def agent_register_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/agent/register"

    @property
    def mandate_query_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/intent/query"

    @property
    def balance_query_url(self) -> str:
        return f"{self.base_url}{self.api_prefix}/balance/query"


@dataclass
class AIWalletConfig:
    """AI 钱包平台服务配置 — 查询Agent等（注册和余额已迁移到 Agent Pay）。"""

    base_url: str = AI_WALLET_BASE_URL
    timeout: float = 30.0

    @property
    def query_agent_by_name_url(self) -> str:
        return f"{self.base_url}/api/agent/queryByName"


@dataclass
class Config:
    """主配置，聚合所有子配置。"""

    agent: AgentIdentity
    user_id: str = ""
    agent_pay: AgentPayConfig = field(default_factory=AgentPayConfig)
    ai_wallet: AIWalletConfig = field(default_factory=AIWalletConfig)
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        agent = AgentIdentity(
            agent_did=os.environ.get("AGENT_DID", ""),
            signer_binary_path=os.environ.get("AGENT_SIGNER_BINARY_PATH", ""),
        )
        agent_pay = AgentPayConfig(
            base_url=os.environ.get("AGENT_PAY_BASE_URL", AGENT_PAY_BASE_URL),
            timeout=float(os.environ.get("AGENT_PAY_TIMEOUT", "30")),
            api_prefix=os.environ.get("AGENT_PAY_API_PREFIX", "/api/v1"),
        )
        ai_wallet = AIWalletConfig(
            base_url=os.environ.get("AI_WALLET_BASE_URL", AI_WALLET_BASE_URL),
            timeout=float(os.environ.get("AI_WALLET_TIMEOUT", "30")),
        )
        return cls(
            agent=agent,
            user_id=os.environ.get("USER_ID", ""),
            agent_pay=agent_pay,
            ai_wallet=ai_wallet,
            log_level=os.environ.get("LOG_LEVEL", "INFO"),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Load configuration from a dictionary."""
        agent_data = data.get("agent", {})
        agent = AgentIdentity(
            agent_did=agent_data.get("agent_did", ""),
            signer_binary_path=agent_data.get("signer_binary_path", ""),
        )

        pay_data = data.get("agent_pay", {})
        agent_pay = AgentPayConfig(
            base_url=pay_data.get("base_url", AGENT_PAY_BASE_URL),
            timeout=float(pay_data.get("timeout", 30)),
            api_prefix=pay_data.get("api_prefix", "/api/v1"),
        )

        wallet_data = data.get("ai_wallet", {})
        ai_wallet = AIWalletConfig(
            base_url=wallet_data.get("base_url", AI_WALLET_BASE_URL),
            timeout=float(wallet_data.get("timeout", 30)),
        )

        return cls(
            agent=agent,
            user_id=data.get("user_id", ""),
            agent_pay=agent_pay,
            ai_wallet=ai_wallet,
            log_level=data.get("log_level", "INFO"),
        )

    @classmethod
    def load(cls, config_path: str = None) -> "Config":
        """
        智能加载配置：
        1. 如果指定了 config_path，从该文件加载
        2. 否则自动搜索 config.json（当前目录 → 项目根目录）
        3. 都找不到则从环境变量加载
        """
        if config_path:
            with open(config_path) as f:
                return cls.from_dict(json.load(f))

        for search_path in _CONFIG_SEARCH_PATHS:
            p = Path(search_path).resolve()
            if p.exists():
                with open(p) as f:
                    return cls.from_dict(json.load(f))

        return cls.from_env()

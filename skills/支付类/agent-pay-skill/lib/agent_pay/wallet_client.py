"""
HTTP Client for AI Wallet Service.

负责与 AI 钱包平台后端通信：
- 查询 Agent（按名称 → agentDid）

注册 Agent 和余额查询已迁移到 Agent Pay 后端，
通过 AgentPayClient 调用。
"""

import logging
from urllib.parse import quote

import httpx

from .config import AIWalletConfig

logger = logging.getLogger(__name__)


class AIWalletClient:
    """AI 钱包平台 HTTP 客户端。"""

    def __init__(self, config: AIWalletConfig):
        self.config = config
        self._client = httpx.Client(timeout=config.timeout)
        self._agent_did_cache: dict[str, str] = {}

    # ============ Agent 查询 ============

    def query_agent_by_name(self, agent_name: str) -> str:
        """
        根据 Agent 名称查询 agentDid。

        调用 /api/agent/queryByName 接口，结果自动缓存。

        Raises:
            ValueError: Agent 不存在或查询失败
        """
        if agent_name in self._agent_did_cache:
            return self._agent_did_cache[agent_name]

        url = f"{self.config.query_agent_by_name_url}?agentName={quote(agent_name)}"
        logger.info(f"Querying agent by name: {agent_name}")

        try:
            response = self._client.get(url)
            response.raise_for_status()
            data = response.json()

            ret_code = str(data.get("retCode", ""))
            if ret_code == "0":
                agent_did = data.get("data", {}).get("agentDid", "")
                if not agent_did:
                    raise ValueError(f"查询到 Agent '{agent_name}' 但缺少 agentDid")
                self._agent_did_cache[agent_name] = agent_did
                logger.info(f"Resolved '{agent_name}' -> {agent_did}")
                return agent_did
            else:
                raise ValueError(f"查询 Agent '{agent_name}' 失败: {data.get('retMsg', ret_code)}")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"查询 Agent '{agent_name}' 失败: HTTP {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise ValueError(f"查询 Agent '{agent_name}' 网络错误: {e}") from e

    def resolve_payee_dids(self, service_names: list[str]) -> list[str]:
        """
        将收款方标识列表解析为 DID 列表。

        - did:agent: 开头的直接使用
        - 其他视为 Agent 名称，调用 queryByName 接口查询
        """
        dids = []
        for name in service_names:
            name = name.strip()
            if not name:
                continue
            if name.startswith("did:agent:"):
                dids.append(name)
            else:
                dids.append(self.query_agent_by_name(name))
        return dids

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

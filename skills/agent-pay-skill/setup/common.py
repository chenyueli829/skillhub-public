"""
setup 脚本公共模块

统一管理路径和配置读取，所有 setup 脚本从这里获取路径和后端地址。
后端地址的唯一来源：
  1. 已生成的 lib/config.json（优先）
  2. lib/agent_pay/config.py 中的默认值（兜底）
"""

import json
import platform
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LIB_DIR = SKILL_DIR / "lib"
CONFIG_PATH = LIB_DIR / "config.json"
KEYS_DIR = LIB_DIR / "keys"
SIGNER_BIN_DIR = SKILL_DIR / "signer" / "bin"

ACTIVATION_BASE_URL = "https://agent-pay.test.ias.qq.com/agent-wallet"


def get_signer_binary_path() -> str:
    """Auto-detect platform and return the absolute path to the signer binary."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch_map = {"x86_64": "amd64", "amd64": "amd64", "arm64": "arm64", "aarch64": "arm64"}
    arch = arch_map.get(machine, machine)
    binary = SIGNER_BIN_DIR / f"skill_signer_{system}_{arch}"
    return str(binary.resolve())


def get_activation_base_url(config: dict = None) -> str:
    """获取钱包激活后端地址，优先从 config.json 读取，兜底用常量。"""
    if config is None:
        config, _ = load_config()
    return config.get("activation", {}).get("base_url", "") or ACTIVATION_BASE_URL


def _load_defaults() -> dict:
    """从 lib/agent_pay/config.py 中加载默认后端地址（唯一定义处）。"""
    result = {"agent_pay_base_url": "", "ai_wallet_base_url": ""}
    try:
        config_py = LIB_DIR / "agent_pay" / "config.py"
        for line in config_py.read_text().splitlines():
            line = line.strip()
            if line.startswith("AGENT_PAY_BASE_URL"):
                result["agent_pay_base_url"] = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("AI_WALLET_BASE_URL"):
                result["ai_wallet_base_url"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return result


def load_config() -> dict:
    """加载配置，优先从 config.json，缺失字段用默认值补。"""
    defaults = _load_defaults()
    config = {}

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    return config, defaults


def get_ai_wallet_base_url(config: dict = None, defaults: dict = None) -> str:
    if config is None or defaults is None:
        config, defaults = load_config()
    return config.get("ai_wallet", {}).get("base_url", "") or defaults["ai_wallet_base_url"]


def get_agent_pay_base_url(config: dict = None, defaults: dict = None) -> str:
    if config is None or defaults is None:
        config, defaults = load_config()
    return config.get("agent_pay", {}).get("base_url", "") or defaults["agent_pay_base_url"]


def get_user_id(config: dict = None) -> str:
    if config is None:
        config, _ = load_config()
    return config.get("user_id", "")

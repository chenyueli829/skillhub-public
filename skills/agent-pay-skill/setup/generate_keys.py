#!/usr/bin/env python3
"""
Agent Pay 密钥对生成

调用编译的 signer 二进制生成 RSA 2048 密钥对。
私钥经 AES-256-GCM 加密存储在 ~/.agent-pay/vault.enc，明文私钥从不落盘。
公钥保存到 lib/keys/ 目录。
仅输出公钥指纹，绝不输出私钥内容。

用法: python setup/generate_keys.py [--force]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

_SETUP_DIR = str(Path(__file__).resolve().parent)
if _SETUP_DIR not in sys.path:
    sys.path.insert(0, _SETUP_DIR)

from common import KEYS_DIR, get_signer_binary_path


def generate_keypair(force: bool = False) -> dict:
    binary_path = get_signer_binary_path()

    if not Path(binary_path).exists():
        return {
            "status": "ERROR",
            "message": f"签名二进制文件不存在: {binary_path}，请先运行 signer/build.sh",
        }

    cmd = [binary_path, "init"]
    if force:
        cmd.append("--force")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        result = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return {
            "status": "ERROR",
            "message": "signer 二进制输出解析失败",
            "stdout": (proc.stdout or "")[-500:],
            "stderr": (proc.stderr or "")[-500:],
        }

    if result.get("status") in ("CREATED", "EXISTS"):
        public_key_pem = result.get("public_key_pem", "")
        fingerprint = result.get("public_key_fingerprint", "")

        public_key_path = KEYS_DIR / "agent_public_key.pem"

        # If vault exists but public key file is missing, extract it via pubkey command
        if not public_key_pem and not public_key_path.exists():
            pubkey_proc = subprocess.run(
                [binary_path, "pubkey"], capture_output=True, text=True,
            )
            try:
                pubkey_result = json.loads(pubkey_proc.stdout)
                public_key_pem = pubkey_result.get("public_key_pem", "")
                fingerprint = pubkey_result.get("public_key_fingerprint", "")
            except (json.JSONDecodeError, ValueError):
                pass

        if public_key_pem:
            KEYS_DIR.mkdir(parents=True, exist_ok=True)
            public_key_path.write_text(public_key_pem)

        return {
            "status": result["status"],
            "message": result.get("message", ""),
            "public_key_path": str(public_key_path),
            "public_key_fingerprint": fingerprint,
        }

    return result


def main():
    parser = argparse.ArgumentParser(description="Agent Pay 密钥对生成")
    parser.add_argument("--force", action="store_true", help="强制重新生成")
    args = parser.parse_args()

    result = generate_keypair(force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

"""
Cryptographic utilities for Agent Pay MCP Server.
Handles RSA signature generation for request authentication.

MPP1.0 Signing Protocol:
- Header: X-Agent-ID (Agent DID)
- Header: X-Timestamp (ISO 8601 format)
- Header: Authorization (MPP1.0 Signature: <hex_signature>)
- Signing Payload: AgentDID|Timestamp(ms)|RequestBody
"""

import json
import subprocess
from typing import Any, Optional


class BinaryAgentSigner:
    """
    Agent request signer that delegates to a compiled binary (software HSM).

    The binary holds the encrypted private key and performs signing internally.
    The Python process never touches the raw private key material.
    """

    def __init__(self, agent_did: str, binary_path: str):
        self.agent_did = agent_did
        self._binary_path = binary_path

    def sign_request(
        self,
        request_body: dict[str, Any],
        body_json_str: Optional[str] = None,
        timestamp: Optional[int] = None,
        nonce: Optional[str] = None,
    ) -> dict[str, str]:
        """
        Sign a request via the compiled signer binary (MPP1.0 protocol).

        Args:
            request_body: Request body dict (used if body_json_str not provided)
            body_json_str: Pre-serialized JSON body string
            timestamp: Unused (binary generates its own)
            nonce: Unused (binary generates its own)

        Returns:
            Dictionary containing signature headers.
        """
        if body_json_str is None:
            body_json_str = json.dumps(
                request_body, separators=(",", ":"), ensure_ascii=False
            )

        proc = subprocess.run(
            [
                self._binary_path,
                "sign",
                "--agent-did", self.agent_did,
                "--body", body_json_str,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if proc.returncode != 0:
            stderr = (proc.stderr or "").strip()
            try:
                err_data = json.loads(proc.stdout)
                raise RuntimeError(
                    f"signer binary error: {err_data.get('message', stderr)}"
                )
            except (json.JSONDecodeError, ValueError):
                raise RuntimeError(f"signer binary failed: {stderr or proc.stdout}")

        result = json.loads(proc.stdout)
        if result.get("status") == "ERROR":
            raise RuntimeError(f"signer error: {result.get('message')}")

        return {
            "X-Agent-ID": result["X-Agent-ID"],
            "X-Timestamp": result["X-Timestamp"],
            "X-Nonce": result["X-Nonce"],
            "X-Signature-Algorithm": result["X-Signature-Algorithm"],
            "Authorization": result["Authorization"],
        }


def create_signer(config) -> BinaryAgentSigner:
    """Create a BinaryAgentSigner from a Config object."""
    return BinaryAgentSigner(
        agent_did=config.agent.agent_did,
        binary_path=config.agent.signer_binary_path,
    )

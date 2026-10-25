from typing import List, Dict, Any
from auctor.protocol.mandate import Mandate
from cryptography.hazmat.primitives.asymmetric import ed25519
import jcs

class PolicyEngine:
    @staticmethod
    def validate_action(mandate: Dict[str, Any], tool_name: str) -> bool:
        # Check tool in capabilities
        tools = mandate.get("capabilities", {}).get("tools", [])
        return tool_name in tools

    @staticmethod
    def verify_chain(chain: List[Dict[str, Any]]) -> bool:
        """
        Verify the chain of mandates:
        1. Each signature is valid.
        2. Delegation attenuates (each child is a subset of parent).
        """
        if not chain:
            return False

        # Verify root signature
        root = chain[0]
        if not PolicyEngine._verify_signature(root):
            return False

        # Verify delegations
        for i in range(1, len(chain)):
            child = chain[i]
            parent = chain[i-1]

            # Signature
            if not PolicyEngine._verify_signature(child):
                return False

            # Linkage
            if child.get("parent_id") != parent.get("id"):
                return False

            # Attenuation
            if not Mandate.is_subset(child["capabilities"]["tools"], parent["capabilities"]["tools"]):
                return False

        return True

    @staticmethod
    def _verify_signature(mandate: Dict[str, Any]) -> bool:
        sig_data = mandate.get("signature")
        if not sig_data:
            return False

        payload = jcs.canonicalize({k: v for k, v in mandate.items() if k != "signature"})
        pub_bytes = bytes.fromhex(sig_data["pubkey"])
        sig_bytes = bytes.fromhex(sig_data["value"])

        try:
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            pub_key.verify(sig_bytes, payload)
            return True
        except:
            return False

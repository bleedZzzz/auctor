import json
import jcs
import uuid
from typing import List, Optional
from auctor.identity.key import Identity

class Mandate:
    def __init__(self, issuer_id: str, subject_id: str, tools: List[str], parent_id: Optional[str] = None):
        self.data = {
            "type": "mandate",
            "id": f"m_{uuid.uuid4().hex[:8]}",
            "issuer": issuer_id,
            "subject": subject_id,
            "capabilities": {"tools": tools},
            "parent_id": parent_id
        }
        self.signature = None

    def sign(self, identity: Identity):
        payload = jcs.canonicalize(self.data)
        self.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return {**self.data, "signature": self.signature}

    @staticmethod
    def is_subset(child_tools: List[str], parent_tools: List[str]) -> bool:
        return set(child_tools).issubset(set(parent_tools))

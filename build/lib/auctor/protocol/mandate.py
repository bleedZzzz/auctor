import json
import jcs
from typing import List, Optional
from auctor.identity.key import Identity

class Mandate:
    def __init__(self, issuer_id: str, subject_id: str, tools: List[str], parent_id: Optional[str] = None):
        self.data = {
            "type": "mandate",
            "issuer": issuer_id,
            "subject": subject_id,
            "capabilities": {"tools": tools},
            "parent_id": parent_id
        }
        self.signature = None

    def sign(self, identity: Identity):
        # JCS canonicalization
        payload = jcs.canonicalize(self.data)
        self.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return {**self.data, "signature": self.signature}

    @staticmethod
    def verify(mandate_json: dict):
        # Implementation of verification
        pass

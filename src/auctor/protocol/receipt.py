from typing import Dict, Any, Optional
from auctor.identity.key import Identity
import jcs
import time
import hashlib
import json

class Receipt:
    def __init__(self, mandate_id: str, tool: str, input_data: Dict[str, Any], output_data: Dict[str, Any]):
        self.data = {
            "type": "receipt",
            "mandate_id": mandate_id,
            "timestamp": int(time.time()),
            "action": {
                "tool": tool,
                "input_hash": hashlib.sha256(json.dumps(input_data).encode()).hexdigest()
            },
            "outcome": {
                "output_hash": hashlib.sha256(json.dumps(output_data).encode()).hexdigest()
            }
        }
        self.signature = None

    def sign(self, identity: Identity):
        payload = jcs.canonicalize(self.data)
        self.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return {**self.data, "signature": self.signature}

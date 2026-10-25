from typing import Dict, Any
from auctor.identity.key import Identity
import jcs
import time

class Receipt:
    def __init__(self, mandate_id: str, tool: str, input_hash: str, output_hash: str):
        self.data = {
            "type": "receipt",
            "mandate_id": mandate_id,
            "timestamp": int(time.time()),
            "action": {
                "tool": tool,
                "input_hash": input_hash
            },
            "outcome": {
                "output_hash": output_hash
            }
        }

    def sign(self, identity: Identity):
        payload = jcs.canonicalize(self.data)
        self.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return {**self.data, "signature": self.signature}

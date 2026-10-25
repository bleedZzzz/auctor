from typing import Dict, Any
from auctor.identity.key import Identity
from auctor.protocol.models import ReceiptModel
import jcs
import hashlib
import json

class Receipt:
    def __init__(self, mandate_id: str, tool: str, input_data: Dict[str, Any], output_data: Dict[str, Any]):
        self.model = ReceiptModel(
            mandate_id=mandate_id,
            action={
                "tool": tool,
                "input_hash": hashlib.sha256(json.dumps(input_data).encode()).hexdigest()
            },
            outcome={
                "output_hash": hashlib.sha256(json.dumps(output_data).encode()).hexdigest()
            }
        )

    def sign(self, identity: Identity):
        data = self.model.model_dump(exclude={"signature"})
        payload = jcs.canonicalize(data)
        self.model.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return self.model.model_dump()

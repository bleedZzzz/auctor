from typing import List, Optional
from auctor.identity.key import Identity
from auctor.protocol.models import MandateModel
import jcs

class Mandate:
    def __init__(self, issuer_id: str, subject_id: str, tools: List[str], parent_id: Optional[str] = None):
        self.model = MandateModel(
            issuer=issuer_id,
            subject=subject_id,
            capabilities={"tools": tools},
            parent_id=parent_id
        )

    def sign(self, identity: Identity):
        data = self.model.model_dump(exclude={"signature"})
        payload = jcs.canonicalize(data)
        self.model.signature = {
            "pubkey": identity.get_public_bytes().hex(),
            "value": identity.sign(payload).hex()
        }
        return self.model.model_dump()

    @staticmethod
    def is_subset(child_tools: List[str], parent_tools: List[str]) -> bool:
        return set(child_tools).issubset(set(parent_tools))

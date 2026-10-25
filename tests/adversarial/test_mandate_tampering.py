import pytest
from auctor.protocol.mandate import Mandate
from auctor.identity.key import Identity
import json

def test_tamper_mandate_capabilities():
    id = Identity()
    m = Mandate("issuer", "subject", ["read"])
    signed = m.sign(id)

    # Tamper
    signed["capabilities"]["tools"].append("write")

    # Signature verification should fail
    sig_data = signed.pop("signature")
    import jcs
    from cryptography.hazmat.primitives.asymmetric import ed25519
    payload = jcs.canonicalize(signed)

    with pytest.raises(Exception):
        ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(sig_data["pubkey"])).verify(
            bytes.fromhex(sig_data["value"]), payload
        )

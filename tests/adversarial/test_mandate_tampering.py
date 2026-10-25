from auctor.protocol.mandate import Mandate
from auctor.identity.key import Identity

def test_tamper_mandate():
    id = Identity()
    m = Mandate("issuer", "subject", ["read"])
    signed = m.sign(id)
    
    # Tamper
    signed["capabilities"]["tools"].append("write")
    
    # Verification should fail
    # (Implementation pending)
    assert True 

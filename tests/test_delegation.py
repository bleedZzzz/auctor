from auctor.protocol.mandate import Mandate

def test_subset():
    parent = ["read", "write"]
    child = ["read"]
    assert Mandate.is_subset(child, parent) == True
    assert Mandate.is_subset(parent, child) == False

if __name__ == "__main__":
    test_subset()
    print("Delegation tests passed!")

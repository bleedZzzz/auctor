from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import os

class Identity:
    def __init__(self, private_key=None):
        if private_key:
            self._private_key = private_key
        else:
            self._private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self._private_key.public_key()

    def get_public_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def sign(self, data: bytes) -> bytes:
        return self._private_key.sign(data)

    @staticmethod
    def verify(public_key_bytes: bytes, signature: bytes, data: bytes):
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, data)
        return True

def generate_identity():
    return Identity()

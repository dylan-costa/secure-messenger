from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def derive_key(shared_secret: bytes) -> bytes:
    """
    Converts shared ECDH secret into a 32-byte symmetric key using HKDF.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"secure-messenger"
    )
    return hkdf.derive(shared_secret)

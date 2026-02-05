from cryptography.hazmat.primitives.asymmetric import ec


def derive_shared_secret(private_key, peer_public_key):
    """
    Performs Elliptic Curve Diffie-Hellman.
    Returns shared secret bytes.
    """
    return private_key.exchange(ec.ECDH(), peer_public_key)

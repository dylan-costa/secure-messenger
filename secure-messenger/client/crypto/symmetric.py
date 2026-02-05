from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt(key: bytes, plaintext: bytes):
    """
    Encrypt a message with AES-GCM.
    Returns nonce and ciphertext.
    """
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, plaintext, None)
    return nonce, ciphertext


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes):
    """
    Decrypt a message with AES-GCM.
    """
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)

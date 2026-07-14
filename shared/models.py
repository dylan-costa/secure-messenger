from pydantic import BaseModel

# -----------------------------
# User model
# -----------------------------
class User(BaseModel):
    username: str
    public_key_pem: str  # Store user's public key in PEM format

# -----------------------------
# Message model
# -----------------------------
class Message(BaseModel):
    sender: str
    receiver: str
    ciphertext_hex: str
    nonce_hex: str

from client.crypto.keygen import generate_keypair
from client.crypto.ecdh import derive_shared_secret
from client.crypto.kdf import derive_key
from client.crypto.symmetric import encrypt, decrypt

import os
from client.crypto.keygen import generate_keypair, save_private_key, save_public_key, load_private_key, load_public_key

# Paths to store keys
alice_priv_file = "client/keys/alice_private.pem"
alice_pub_file = "client/keys/alice_public.pem"
bob_priv_file = "client/keys/bob_private.pem"
bob_pub_file = "client/keys/bob_public.pem"

# Create keys folder if it doesn't exist
os.makedirs("client/keys", exist_ok=True)

# -----------------------------
# Load existing keys if they exist
# -----------------------------
if os.path.exists(alice_priv_file):
    alice_priv = load_private_key(alice_priv_file)
    alice_pub = load_public_key(alice_pub_file)
else:
    alice_priv, alice_pub = generate_keypair()
    save_private_key(alice_priv, alice_priv_file)
    save_public_key(alice_pub, alice_pub_file)

if os.path.exists(bob_priv_file):
    bob_priv = load_private_key(bob_priv_file)
    bob_pub = load_public_key(bob_pub_file)
else:
    bob_priv, bob_pub = generate_keypair()
    save_private_key(bob_priv, bob_priv_file)
    save_public_key(bob_pub, bob_pub_file)


# -----------------------------
# Derive shared secret
# -----------------------------
alice_secret = derive_shared_secret(alice_priv, bob_pub)
bob_secret = derive_shared_secret(bob_priv, alice_pub)

print("Alice secret:", alice_secret.hex())
print("Bob secret:  ", bob_secret.hex())
print("Match:", alice_secret == bob_secret)

# -----------------------------
# Derive symmetric AES keys
# -----------------------------
alice_key = derive_key(alice_secret)
bob_key = derive_key(bob_secret)

# -----------------------------
# Encrypt and decrypt a message
# -----------------------------
message = b"Hello Bob! This is Alice. Dylan made this!"
nonce, ciphertext = encrypt(alice_key, message)
plaintext = decrypt(bob_key, nonce, ciphertext)

print("\nOriginal message:", message.decode())
print("Ciphertext (hex):", ciphertext.hex())
print("Decrypted message:", plaintext.decode())

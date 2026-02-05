import tkinter as tk
import requests
from client.crypto.keygen import generate_keypair, serialize_public_key, load_private_key, save_private_key, load_public_key, save_public_key
from client.crypto.ecdh import derive_shared_secret
from client.crypto.kdf import derive_key
from client.crypto.symmetric import encrypt, decrypt
import os

SERVER_URL = "http://127.0.0.1:8000"

# -----------------------------
# Setup / load Alice keys
# -----------------------------
os.makedirs("client/keys", exist_ok=True)
alice_priv_file = "client/keys/alice_private.pem"
alice_pub_file = "client/keys/alice_public.pem"

if os.path.exists(alice_priv_file):
    alice_priv = load_private_key(alice_priv_file)
    alice_pub = load_public_key(alice_pub_file)
else:
    alice_priv, alice_pub = generate_keypair()
    save_private_key(alice_priv, alice_priv_file)
    save_public_key(alice_pub, alice_pub_file)

# Register Alice with server
alice_pub_pem = serialize_public_key(alice_pub).decode()
requests.post(f"{SERVER_URL}/register", json={"username": "Alice", "public_key_pem": alice_pub_pem})

# -----------------------------
# Fetch Bob's public key from server
# -----------------------------
response = requests.get(f"{SERVER_URL}/messages/Bob")  # For demo, messages endpoint to see if Bob exists
# In a real implementation, create a /users endpoint to fetch public key
# Here we simulate by registering Bob locally if not exists
bob_priv, bob_pub = generate_keypair()
bob_key_pem = serialize_public_key(bob_pub).decode()
requests.post(f"{SERVER_URL}/register", json={"username": "Bob", "public_key_pem": bob_key_pem})

# Derive shared secret and AES key
alice_secret = derive_shared_secret(alice_priv, bob_pub)
bob_secret = derive_shared_secret(bob_priv, alice_pub)
alice_key = derive_key(alice_secret)
bob_key = derive_key(bob_secret)

# -----------------------------
# Tkinter Window
# -----------------------------
root = tk.Tk()
root.title("Secure Messenger UI with Server")

chat_display = tk.Text(root, height=25, width=70)
chat_display.pack(pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(side=tk.LEFT, padx=(10,0))

# -----------------------------
# Send message to server
# -----------------------------
def send_message():
    message = message_entry.get().encode()

    # Encrypt locally
    nonce, ciphertext = encrypt(alice_key, message)

    # Send to server
    msg_payload = {
        "sender": "Alice",
        "receiver": "Bob",
        "ciphertext_hex": ciphertext.hex(),
        "nonce_hex": nonce.hex()
    }
    requests.post(f"{SERVER_URL}/send", json=msg_payload)

    chat_display.insert(tk.END, f"Alice sent (encrypted): {ciphertext.hex()}\n")
    chat_display.insert(tk.END, f"Alice sees decrypted: {message.decode()}\n\n")
    message_entry.delete(0, tk.END)

# -----------------------------
# Fetch messages for Bob (simulate receiving)
# -----------------------------
def fetch_messages():
    response = requests.get(f"{SERVER_URL}/messages/Bob").json()
    for m in response["messages"]:
        ciphertext_bytes = bytes.fromhex(m["ciphertext_hex"])
        nonce_bytes = bytes.fromhex(m["nonce_hex"])
        plaintext = decrypt(bob_key, nonce_bytes, ciphertext_bytes)
        chat_display.insert(tk.END, f"Bob received: {plaintext.decode()}\n")
    # Clear messages on server (optional)
    # requests.delete(f"{SERVER_URL}/messages/Bob")

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

fetch_button = tk.Button(root, text="Fetch Messages", command=fetch_messages)
fetch_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

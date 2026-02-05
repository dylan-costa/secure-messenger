import tkinter as tk
from client.crypto.keygen import generate_keypair, serialize_public_key
from client.crypto.ecdh import derive_shared_secret
from client.crypto.kdf import derive_key
from client.crypto.symmetric import encrypt, decrypt

# -----------------------------
# Generate keys for Alice and Bob
# -----------------------------
alice_priv, alice_pub = generate_keypair()
bob_priv, bob_pub = generate_keypair()

# Derive shared secrets
alice_secret = derive_shared_secret(alice_priv, bob_pub)
bob_secret = derive_shared_secret(bob_priv, alice_pub)

# Derive symmetric keys
alice_key = derive_key(alice_secret)
bob_key = derive_key(bob_secret)

# -----------------------------
# Tkinter Window
# -----------------------------
root = tk.Tk()
root.title("Secure Messenger Debug UI")

# Chat display
chat_display = tk.Text(root, height=25, width=70)
chat_display.pack(pady=10)

# Input box
message_entry = tk.Entry(root, width=50)
message_entry.pack(side=tk.LEFT, padx=(10,0))

# Send button
def send_message():
    message = message_entry.get().encode()
    
    # Show Alice's keys
    chat_display.insert(tk.END, f"\n--- Alice Keys ---\n")
    chat_display.insert(tk.END, f"Private key: {alice_priv.private_numbers()}\n")
    chat_display.insert(tk.END, f"Public key: {serialize_public_key(alice_pub).decode()}\n")
    
    # Show original message
    chat_display.insert(tk.END, f"\nOriginal message: {message.decode()}\n")
    
    # Encrypt
    nonce, ciphertext = encrypt(alice_key, message)
    chat_display.insert(tk.END, f"Encrypted message (hex): {ciphertext.hex()}\n")
    
    # Decrypt
    plaintext = decrypt(bob_key, nonce, ciphertext)
    chat_display.insert(tk.END, f"Decrypted message: {plaintext.decode()}\n")
    
    # Final message received by Bob
    chat_display.insert(tk.END, f"Bob received: {plaintext.decode()}\n")
    
    chat_display.insert(tk.END, "\n" + "-"*60 + "\n")
    message_entry.delete(0, tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10)

root.mainloop()

// The pluggable encryption-method registry. Every UI component (method
// picker, send, decrypt-on-render) dispatches through this list instead of
// branching on a method name directly -- adding a future method means
// writing one crypto module and one entry here.

import * as rsaFamily from "./rsaFamily.js"
import * as ecc from "./ecc.js"

export const ENCRYPTION_METHODS = [
    {
        id: "RSA",
        label: "RSA",
        scope: "identity",
        generateKeypair: () => rsaFamily.generateKeys(2, 512),
        encrypt: (message, publicKey) => rsaFamily.encrypt(message, publicKey),
        decrypt: (ciphertext, privateKey) => rsaFamily.decrypt(ciphertext, privateKey),
        serializePublicKey: rsaFamily.serializePublicKey,
        deserializePublicKey: rsaFamily.deserializePublicKey,
        serializePrivateKey: rsaFamily.serializePrivateKey,
        deserializePrivateKey: rsaFamily.deserializePrivateKey,
        maxMessageLength: (publicKey) => rsaFamily.maxMessageLength(publicKey.n),
    },
    {
        id: "MULTIPRIME_RSA",
        label: "Multiprime RSA (3-prime)",
        scope: "identity",
        // 3 primes of ~342 bits keep the overall modulus around the same
        // ~1024-bit size as standard RSA -- real multiprime RSA trades
        // security margin per bit for faster CRT-based decryption, it
        // doesn't make the key "stronger."
        generateKeypair: () => rsaFamily.generateKeys(3, 342),
        encrypt: (message, publicKey) => rsaFamily.encrypt(message, publicKey),
        decrypt: (ciphertext, privateKey) => rsaFamily.decrypt(ciphertext, privateKey),
        serializePublicKey: rsaFamily.serializePublicKey,
        deserializePublicKey: rsaFamily.deserializePublicKey,
        serializePrivateKey: rsaFamily.serializePrivateKey,
        deserializePrivateKey: rsaFamily.deserializePrivateKey,
        maxMessageLength: (publicKey) => rsaFamily.maxMessageLength(publicKey.n),
    },
    {
        id: "ECC",
        label: "Elliptic Curve Diffie-Hellman",
        scope: "conversation",
        generateKeypair: (domainParams) => ecc.generateKeys(domainParams),
        deriveSharedSecret: (privateKey, otherPublicKey, domainParams) =>
            ecc.generateSharedSecret(privateKey, otherPublicKey, domainParams),
        encrypt: (message, sharedSecret) => ecc.encrypt(message, sharedSecret),
        decrypt: (ciphertext, sharedSecret) => ecc.decrypt(ciphertext, sharedSecret),
        serializePublicKey: ecc.serializePublicKey,
        deserializePublicKey: ecc.deserializePublicKey,
    },
]

export function getMethod(id) {
    return ENCRYPTION_METHODS.find((method) => method.id === id)
}

// Identity-scoped methods encrypt for the recipient's public key, so the
// sender can't decrypt their own sent history without a second copy.
// Conversation-scoped methods derive a symmetric shared secret, so one
// ciphertext already works for both sides.
export function needsSelfCopy(method) {
    return method.scope === "identity"
}

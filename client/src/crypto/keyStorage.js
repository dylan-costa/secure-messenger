// Centralizes where private key material lives in the browser. This is a
// demo, not a secure key store -- localStorage is fine here, but keeping the
// naming/parsing in one place means every component agrees on it.
//
// Identity-scoped methods (RSA, Multiprime RSA, ...): one keypair per (user,
// method) -- reused across every conversation using that method. Both
// halves are kept locally: the private key to decrypt, the public key to
// re-encrypt a copy for yourself when sending (see methods.needsSelfCopy).
//
// Conversation-scoped methods (ECC, ...): one private scalar per
// (conversation, user) -- the public key is already on the server's
// Conversation row once submitted, so only the private half needs local
// storage.

function identityKeyStorageKey(userId, methodId) {
    return `secure_messenger.identity_key.${userId}.${methodId}`
}

function conversationKeyStorageKey(conversationId, userId) {
    return `secure_messenger.conversation_key.${conversationId}.${userId}`
}

export function getIdentityKeypair(userId, methodId, method) {
    const raw = localStorage.getItem(identityKeyStorageKey(userId, methodId))
    if (!raw) return null

    const { publicKey, privateKey } = JSON.parse(raw)
    return {
        publicKey: method.deserializePublicKey(publicKey),
        privateKey: method.deserializePrivateKey(privateKey),
    }
}

export function saveIdentityKeypair(userId, methodId, keypair, method) {
    localStorage.setItem(
        identityKeyStorageKey(userId, methodId),
        JSON.stringify({
            publicKey: method.serializePublicKey(keypair.publicKey),
            privateKey: method.serializePrivateKey(keypair.privateKey),
        })
    )
}

export function getConversationPrivateKey(conversationId, userId) {
    const raw = localStorage.getItem(conversationKeyStorageKey(conversationId, userId))
    if (raw === null) return null
    return JSON.parse(raw)
}

export function saveConversationPrivateKey(conversationId, userId, privateKey) {
    localStorage.setItem(
        conversationKeyStorageKey(conversationId, userId),
        JSON.stringify(privateKey)
    )
}

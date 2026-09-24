// VITE_API_BASE_URL is set in Vercel's project settings to the deployed
// Render backend's URL; locally it falls back to the dev server.
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"

async function request(path, options) {
    const response = await fetch(`${API_BASE}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
    })

    if (!response.ok) {
        const body = await response.json().catch(() => null)
        throw new Error(body?.detail || `Request to ${path} failed (${response.status})`)
    }

    if (response.status === 204) return null
    return response.json()
}

export function createUser(username, password) {
    return request("/users", { method: "POST", body: JSON.stringify({ username, password }) })
}

export function login(username, password) {
    return request("/login", { method: "POST", body: JSON.stringify({ username, password }) })
}

export function getUsers() {
    return request("/users")
}

export function getUser(username) {
    return request(`/users/${username}`)
}

export function addUserKey(userId, method, publicKeyJson) {
    return request(`/users/${userId}/keys`, {
        method: "POST",
        body: JSON.stringify({ method, public_key_json: publicKeyJson }),
    })
}

export async function lookupConversation(user1Id, user2Id) {
    try {
        return await request(`/conversations/lookup/${user1Id}/${user2Id}`)
    } catch {
        return null
    }
}

export function createConversation(user1Id, user2Id, encryptionMethod) {
    return request("/conversations", {
        method: "POST",
        body: JSON.stringify({ user1_id: user1Id, user2_id: user2Id, encryption_method: encryptionMethod }),
    })
}

export function getConversation(conversationId) {
    return request(`/conversations/${conversationId}`)
}

export function addConversationKey(conversationId, userId, publicKeyJson) {
    return request(`/conversations/${conversationId}/keys`, {
        method: "POST",
        body: JSON.stringify({ user_id: userId, public_key_json: publicKeyJson }),
    })
}

export function sendMessage(senderId, receiverId, ciphertext, ciphertextForSender) {
    return request("/messages", {
        method: "POST",
        body: JSON.stringify({
            sender_id: senderId,
            receiver_id: receiverId,
            ciphertext,
            ciphertext_for_sender: ciphertextForSender ?? null,
        }),
    })
}

export function getConversationMessages(user1Id, user2Id) {
    return request(`/conversations/${user1Id}/${user2Id}`)
}

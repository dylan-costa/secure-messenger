import { useState, useEffect, useRef } from "react"
import MessageInput from "./MessageInput"
import * as api from "../api"
import * as methods from "../crypto/methods"
import * as keyStorage from "../crypto/keyStorage"

const POLL_INTERVAL_MS = 3000

// Ensures this user has a keypair/private scalar for the conversation's
// method, generating and uploading one if this is the first time it's
// needed (checking localStorage FIRST so a reload mid-handshake doesn't
// silently overwrite an already-submitted public key).
async function ensureOwnKeyMaterial(conversation, method, currentUserId) {
    if (method.scope === "identity") {
        let keypair = keyStorage.getIdentityKeypair(currentUserId, method.id, method)

        if (!keypair) {
            keypair = method.generateKeypair()
            keyStorage.saveIdentityKeypair(currentUserId, method.id, keypair, method)
            await api.addUserKey(currentUserId, method.id, method.serializePublicKey(keypair.publicKey))
        }

        return keypair
    }

    // conversation-scoped
    const domainParams = JSON.parse(conversation.domain_params_json)
    let privateKey = keyStorage.getConversationPrivateKey(conversation.id, currentUserId)

    if (privateKey === null) {
        const keypair = method.generateKeypair(domainParams)
        privateKey = keypair.privateKey
        keyStorage.saveConversationPrivateKey(conversation.id, currentUserId, privateKey)
        await api.addConversationKey(conversation.id, currentUserId, method.serializePublicKey(keypair.publicKey))
    }

    return { privateKey }
}

// Looks for the peer's public key material. Returns null while it's still
// missing (peer hasn't opened/generated theirs yet).
async function findPeerKeyMaterial(conversation, method, currentUserId, peerUsername) {
    if (method.scope === "identity") {
        const peer = await api.getUser(peerUsername)
        const peerKey = peer.keys.find((k) => k.method === method.id)
        return peerKey ? method.deserializePublicKey(peerKey.public_key_json) : null
    }

    const fresh = await api.getConversation(conversation.id)
    const peerKeyRow = fresh.keys.find((k) => k.user_id !== currentUserId)
    return peerKeyRow ? method.deserializePublicKey(peerKeyRow.public_key_json) : null
}

function Conversation({ currentUserId, selectedUser }) {
    const [status, setStatus] = useState("idle") // idle | loading | choose-method | waiting-for-peer | ready | error
    const [method, setMethod] = useState(null)
    const [cryptoContext, setCryptoContext] = useState(null)
    const [messages, setMessages] = useState([])
    const [errorMessage, setErrorMessage] = useState("")

    const cancelledRef = useRef(false)
    const pollTimerRef = useRef(null)

    // Reads the given method/cryptoContext explicitly rather than from
    // component state, so it can be called with a just-computed context
    // before React has re-rendered with it (avoids a stale closure).
    const loadMessages = async (activeMethod, activeCryptoContext) => {
        const raw = await api.getConversationMessages(currentUserId, selectedUser.id)

        const decrypted = raw.map((m) => {
            try {
                let text
                if (methods.needsSelfCopy(activeMethod)) {
                    const ownPrivateKey = activeCryptoContext.ownKeypair.privateKey
                    text = m.sender_id === currentUserId
                        ? activeMethod.decrypt(m.ciphertext_for_sender, ownPrivateKey)
                        : activeMethod.decrypt(m.ciphertext, ownPrivateKey)
                } else {
                    text = activeMethod.decrypt(m.ciphertext, activeCryptoContext.sharedSecret)
                }
                return { ...m, text }
            } catch {
                return { ...m, text: "[unable to decrypt this message]" }
            }
        })

        setMessages(decrypted)
    }

    const buildCryptoContext = async (conv) => {
        const activeMethod = methods.getMethod(conv.encryption_method)
        setMethod(activeMethod)

        const ownKeyMaterial = await ensureOwnKeyMaterial(conv, activeMethod, currentUserId)
        const peerPublicKey = await findPeerKeyMaterial(conv, activeMethod, currentUserId, selectedUser.username)

        if (cancelledRef.current) return

        if (!peerPublicKey) {
            setStatus("waiting-for-peer")
            pollTimerRef.current = setTimeout(async () => {
                const refreshedConv = await api.getConversation(conv.id)
                if (!cancelledRef.current) buildCryptoContext(refreshedConv)
            }, POLL_INTERVAL_MS)
            return
        }

        let newCryptoContext
        if (activeMethod.scope === "identity") {
            newCryptoContext = {
                ownKeypair: ownKeyMaterial,
                recipientPublicKey: peerPublicKey,
                sharedSecret: null,
            }
        } else {
            const domainParams = JSON.parse(conv.domain_params_json)
            const sharedSecret = activeMethod.deriveSharedSecret(
                ownKeyMaterial.privateKey,
                peerPublicKey,
                domainParams
            )
            newCryptoContext = { ownKeypair: null, recipientPublicKey: null, sharedSecret }
        }

        setCryptoContext(newCryptoContext)
        await loadMessages(activeMethod, newCryptoContext)

        if (!cancelledRef.current) setStatus("ready")
    }

    useEffect(() => {
        cancelledRef.current = false

        if (pollTimerRef.current) {
            clearTimeout(pollTimerRef.current)
            pollTimerRef.current = null
        }

        if (!selectedUser) {
            return () => {
                cancelledRef.current = true
            }
        }

        async function start() {
            setStatus("loading")
            setErrorMessage("")
            setMessages([])
            setCryptoContext(null)

            try {
                const existing = await api.lookupConversation(currentUserId, selectedUser.id)
                if (cancelledRef.current) return

                if (!existing) {
                    setStatus("choose-method")
                    return
                }

                await buildCryptoContext(existing)
            } catch (error) {
                if (!cancelledRef.current) {
                    setErrorMessage(error.message)
                    setStatus("error")
                }
            }
        }

        start()

        return () => {
            cancelledRef.current = true
            if (pollTimerRef.current) clearTimeout(pollTimerRef.current)
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [currentUserId, selectedUser])

    const handleChooseMethod = async (methodId) => {
        try {
            setStatus("loading")
            const created = await api.createConversation(currentUserId, selectedUser.id, methodId)
            await buildCryptoContext(created)
        } catch (error) {
            setErrorMessage(error.message)
            setStatus("error")
        }
    }

    const handleSend = async (plainText) => {
        let ciphertext
        let ciphertextForSender = null

        if (methods.needsSelfCopy(method)) {
            ciphertext = method.encrypt(plainText, cryptoContext.recipientPublicKey)
            ciphertextForSender = method.encrypt(plainText, cryptoContext.ownKeypair.publicKey)
        } else {
            ciphertext = method.encrypt(plainText, cryptoContext.sharedSecret)
        }

        await api.sendMessage(currentUserId, selectedUser.id, ciphertext, ciphertextForSender)
        await loadMessages(method, cryptoContext)
    }

    if (!selectedUser) {
        return (
            <div className="chat-panel">
                <div className="chat-empty">
                    <p>Select a conversation to get started.</p>
                </div>
            </div>
        )
    }

    const maxMessageLength = (() => {
        if (status !== "ready" || !method?.maxMessageLength) return null
        if (!methods.needsSelfCopy(method)) return null
        return Math.min(
            method.maxMessageLength(cryptoContext.recipientPublicKey),
            method.maxMessageLength(cryptoContext.ownKeypair.publicKey)
        )
    })()

    return (
        <div className="chat-panel">
            <div className="chat-header">
                <h2>{selectedUser.username}</h2>
            </div>

            {status === "loading" && <p className="status-banner">Loading conversation…</p>}
            {status === "error" && <p className="status-banner error">Error: {errorMessage}</p>}

            {status === "choose-method" && (
                <div className="method-picker">
                    <p>Start a secure conversation with {selectedUser.username}. Choose an encryption method:</p>
                    <div className="method-picker-options">
                        {methods.ENCRYPTION_METHODS.map((m) => (
                            <button key={m.id} className="btn btn-primary" onClick={() => handleChooseMethod(m.id)}>
                                {m.label}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {status === "waiting-for-peer" && (
                <p className="status-banner">
                    Waiting for {selectedUser.username} to open this chat to finish the key exchange…
                </p>
            )}

            {status === "ready" && (
                <>
                    <div className="message-list">
                        {messages.length === 0 && <p className="message-list-empty">No messages yet.</p>}

                        {messages.map((message) => (
                            <div
                                key={message.id}
                                className={
                                    message.sender_id === currentUserId
                                        ? "message-row sent"
                                        : "message-row received"
                                }
                            >
                                <div className="message-bubble">
                                    <strong className="message-sender">
                                        {message.sender_id === currentUserId ? "You" : selectedUser.username}
                                    </strong>

                                    <p>{message.text}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <MessageInput onSend={handleSend} maxLength={maxMessageLength} />
                </>
            )}
        </div>
    )
}

export default Conversation

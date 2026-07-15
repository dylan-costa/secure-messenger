

import { useState } from "react"

function MessageInput({ currentUserId, selectedUser, onMessageSent }) {
    const [content, setContent] = useState("")

    const sendMessage = () => {
        if (!content.trim() || !selectedUser) {
            return
        }

        fetch("http://127.0.0.1:8000/messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender_id: currentUserId,
                receiver_id: selectedUser.id,
                content: content
            })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to send message")
            }

            return response.json()
        })
        .then(() => {
            setContent("")
            onMessageSent()
        })
        .catch((error) => {
            console.error(error)
        })
    }

    return (
        <div>
            <input
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Type a message..."
            />

            <button
                disabled={!content.trim() || !selectedUser}
                onClick={sendMessage}
            >
                Send
            </button>
        </div>
    )
}

export default MessageInput
import { useState } from "react"

function MessageInput({ onSend, maxLength }) {
    const [content, setContent] = useState("")
    const [error, setError] = useState("")

    const overLimit = maxLength != null && content.length > maxLength

    const sendMessage = () => {
        if (!content.trim() || overLimit) {
            return
        }

        setError("")

        Promise.resolve(onSend(content))
            .then(() => {
                setContent("")
            })
            .catch((error) => {
                setError(error.message)
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
                disabled={!content.trim() || overLimit}
                onClick={sendMessage}
            >
                Send
            </button>

            {maxLength != null && (
                <p>
                    {content.length}/{maxLength} characters
                    {overLimit && " — this encryption method can't fit a longer message in one go"}
                </p>
            )}

            {error && <p>{error}</p>}
        </div>
    )
}

export default MessageInput

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
            <div className="message-input-bar">
                <input
                    className="input"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    placeholder="Type a message..."
                />

                <button
                    className="btn btn-primary"
                    disabled={!content.trim() || overLimit}
                    onClick={sendMessage}
                >
                    Send
                </button>
            </div>

            {maxLength != null && (
                <p className={`message-input-meta${overLimit ? " over-limit" : ""}`}>
                    {content.length}/{maxLength} characters
                    {overLimit && " — this encryption method can't fit a longer message in one go"}
                </p>
            )}

            {error && <p className="form-error">{error}</p>}
        </div>
    )
}

export default MessageInput

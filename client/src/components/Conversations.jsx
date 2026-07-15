import { useState, useEffect } from "react"
import MessageInput from "./MessageInput"


function Conversation({currentUserId, selectedUser}) {
    const [messages, setMessages] = useState([])

    const loadMessages = () => {
        if (!selectedUser) {
            setMessages([])
            return
        }

        fetch(`http://127.0.0.1:8000/conversations/${currentUserId}/${selectedUser.id}`)
            .then((response) => response.json())
            .then((data) => {
                setMessages(data)
            })
    }


    useEffect(() => {
        loadMessages()
    }, [currentUserId, selectedUser])


    return (
        <div>
            <h2>
                {selectedUser ? selectedUser.username : "Select user"}
            </h2>
            {messages.length === 0 && selectedUser && (
            <p>No messages yet.</p>
            )}

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
                    <strong>
                        {message.sender_id === currentUserId
                            ? "You"
                            : selectedUser.username}
                    </strong>

                    <p>{message.content}</p>
                </div>
            </div>
        ))}


            {selectedUser && (
                <MessageInput
                    currentUserId={currentUserId}
                    selectedUser={selectedUser}
                    onMessageSent={loadMessages}
                />
            )}
        </div>
    )
}

export default Conversation
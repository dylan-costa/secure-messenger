import { useState, useEffect } from 'react'


function Conversation({currentUserId, selectedUser}) {
    const [messages, setMessages] = useState([])
    useEffect(() => {
        if (!selectedUser) {
            setMessages([])
            return }
        fetch(`http://127.0.0.1:8000/conversations/${currentUserId}/${selectedUser.id}`)
            .then((response) => response.json())
            .then((data) => {
                setMessages(data)
            })
        
        }
    , [currentUserId, selectedUser])

    return (
            <div>
                {messages.map((message) => (
                <p key={message.id}>
                    {message.content}
                </p>
                ))}
            </div>
            ) }

export default Conversation
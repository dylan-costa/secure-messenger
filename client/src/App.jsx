import './App.css'
import { useState, useEffect } from 'react'
import UserList from './components/UserList'
import Conversation from './components/Conversations'



function App() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [conversations, setConversations] = useState([])
  const currentUserId = 1

  

  useEffect(() => {
    fetch("http://127.0.0.1:8000/users")
        .then((response) => response.json())
        .then((data) => {
            setUsers(data)
        }).catch((error) => {
        console.error(error)
      })
      
}, [])
  console.log(selectedUser)
  return (
  <div>
    <h1>Secure Messenger</h1>

    
    <UserList
    users={users}
    setSelectedUser={setSelectedUser}
    />
    <Conversation
    currentUserId={currentUserId}
    selectedUser={selectedUser}
    />

  </div>
)
}
export default App
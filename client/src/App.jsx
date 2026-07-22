import './App.css'
import { useState, useEffect } from 'react'
import UserList from './components/UserList'
import Conversation from './components/Conversations'
import Login from './components/Login'

function App() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [currentUser, setCurrentUser] = useState(() => {
    const storedUser = localStorage.getItem("currentUser")
    return storedUser ? JSON.parse(storedUser) : null
  })

  useEffect(() => {
    if (!currentUser) {
      return
    }

    fetch("http://127.0.0.1:8000/users")
      .then((response) => response.json())
      .then((data) => {
        setUsers(data)
      })
      .catch((error) => {
        console.error(error)
      })
  }, [currentUser])

  if (!currentUser) {
    return <Login onLogin={setCurrentUser} />
  }

  return (
  <div>
    <h1>Secure Messenger</h1>

    <p>Logged in as: {currentUser.username}</p>

    <button
    onClick={() => {
        localStorage.removeItem("currentUser")
        setCurrentUser(null)
    }}
    >
        Logout
    </button>

    <UserList
      users={users}
      setSelectedUser={setSelectedUser}
    />

    <Conversation
      currentUserId={currentUser.id}
      selectedUser={selectedUser}
    />
  </div>
)
}

export default App
import './App.css'
import { useState, useEffect } from 'react'
import UserList from './components/UserList'
import Conversation from './components/Conversations'
import Login from './components/Login'
import * as api from './api'

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

    api.getUsers()
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

  const handleLogout = () => {
    localStorage.removeItem("currentUser")
    setCurrentUser(null)
    setSelectedUser(null)
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Secure Messenger</h1>

        <div className="app-header-user">
          <span>{currentUser.username}</span>
          <button className="btn btn-ghost" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="app-body">
        <UserList
          users={users.filter((user) => user.id !== currentUser.id)}
          selectedUser={selectedUser}
          setSelectedUser={setSelectedUser}
        />

        <Conversation
          currentUserId={currentUser.id}
          selectedUser={selectedUser}
        />
      </div>

      <footer className="app-footer">
        Built by{" "}
        <a href="https://github.com/dylan-costa/secure-messenger" target="_blank" rel="noreferrer">
          Dylan Costa
        </a>
      </footer>
    </div>
  )
}

export default App

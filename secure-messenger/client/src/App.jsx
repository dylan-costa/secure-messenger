import './App.css'
import { useState, useEffect } from 'react'
import UserList from './components/UserList'

function App() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)

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

  </div>
)
}
export default App
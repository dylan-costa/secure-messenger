import './App.css'
import { useState, useEffect } from 'react'

function App() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    fetch("http://localhost:3000/users")
        .then((response) => response.json())
        .then((data) => {
            setUsers(data)
        })
}, [])
  return (
  <div>
    <h1>Secure Messenger</h1>

    {users.map((user) => (
      <p>{user.username}</p>
    ))}

  </div>
)
}
export default App
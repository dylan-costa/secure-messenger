import './App.css'
import { useState, useEffect } from 'react'

function App() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    // Fetch users from the API
  }, [])

  return (
    <div>
      <h1>Secure Messenger</h1>
    </div>
  )
}

export default App
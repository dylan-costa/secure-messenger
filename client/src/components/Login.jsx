import { useState } from "react"

function Login({ onLogin }) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleLogin = () => {
        setError("")

        fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Invalid username or password")
            }

            return response.json()
        })
        .then((data) => {
        localStorage.setItem("currentUser", JSON.stringify(data))
        onLogin(data)
    })
        .catch((error) => {
            setError(error.message)
        })
    }

    return (
        <div>
            <h1>Secure Messenger</h1>

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={handleLogin}>
                Login
            </button>

            {error && (
                <p>{error}</p>
            )}
        </div>
    )
}

export default Login
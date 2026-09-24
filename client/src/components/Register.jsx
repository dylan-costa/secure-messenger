import { useState } from "react"
import * as api from "../api"

function Register({ onRegistered, onSwitchToLogin }) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleRegister = () => {
        setError("")

        api.createUser(username, password)
            .then((data) => {
                localStorage.setItem("currentUser", JSON.stringify(data))
                onRegistered(data)
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

            <button onClick={handleRegister}>
                Sign up
            </button>

            <p>
                Already have an account?{" "}
                <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToLogin() }}>
                    Log in
                </a>
            </p>

            {error && (
                <p>{error}</p>
            )}
        </div>
    )
}

export default Register

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
        <div className="auth-screen">
            <div className="auth-card">
                <h1>Secure Messenger</h1>
                <p className="auth-subtitle">Create an account</p>

                <div className="auth-form">
                    <input
                        className="input"
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />

                    <input
                        className="input"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    {error && <p className="form-error">{error}</p>}

                    <button className="btn btn-primary" onClick={handleRegister}>
                        Sign up
                    </button>
                </div>

                <p className="auth-switch">
                    Already have an account?{" "}
                    <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToLogin() }}>
                        Log in
                    </a>
                </p>
            </div>
        </div>
    )
}

export default Register

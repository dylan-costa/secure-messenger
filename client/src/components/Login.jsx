import { useState } from "react"
import * as api from "../api"
import Register from "./Register"

function Login({ onLogin }) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [showRegister, setShowRegister] = useState(false)

    const handleLogin = () => {
        setError("")

        api.login(username, password)
            .then((data) => {
                localStorage.setItem("currentUser", JSON.stringify(data))
                onLogin(data)
            })
            .catch((error) => {
                setError(error.message)
            })
    }

    if (showRegister) {
        return <Register onRegistered={onLogin} onSwitchToLogin={() => setShowRegister(false)} />
    }

    return (
        <div className="auth-screen">
            <div className="auth-card">
                <h1>Secure Messenger</h1>
                <p className="auth-subtitle">Log in to continue</p>

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

                    <button className="btn btn-primary" onClick={handleLogin}>
                        Login
                    </button>
                </div>

                <p className="auth-switch">
                    Need an account?{" "}
                    <a href="#" onClick={(e) => { e.preventDefault(); setShowRegister(true) }}>
                        Sign up
                    </a>
                </p>
            </div>
        </div>
    )
}

export default Login

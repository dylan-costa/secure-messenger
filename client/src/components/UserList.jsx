function UserList({ users, selectedUser, setSelectedUser }) {
    return (
        <aside className="sidebar">
            <h2 className="sidebar-title">Conversations</h2>

            {users.length === 0 && (
                <p className="sidebar-empty">No other users yet.</p>
            )}

            <ul className="user-list">
                {users.map((user) => (
                    <li
                        key={user.id}
                        className={`user-item${selectedUser?.id === user.id ? " active" : ""}`}
                        onClick={() => setSelectedUser(user)}
                    >
                        <span className="user-avatar">{user.username.slice(0, 1).toUpperCase()}</span>
                        <span className="user-name">{user.username}</span>
                    </li>
                ))}
            </ul>
        </aside>
    )
}

export default UserList

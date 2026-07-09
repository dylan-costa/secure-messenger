
function UserList({ users, setSelectedUser }) {
    return (
        <div>
            {users.map((user) => (
                <p 
                    key={user.id} 
                    onClick={() => setSelectedUser(user)}
                >
                    {user.username}
                </p>
            ))}
        </div>
    )
}

export default UserList
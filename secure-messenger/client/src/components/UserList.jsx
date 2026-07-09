
function UserList({ users }) {
    return (
        <div>
            {users.map((user) => (
                <p key={user.id}>{user.username}</p>
            ))}
        </div>
    )
}

export default UserList
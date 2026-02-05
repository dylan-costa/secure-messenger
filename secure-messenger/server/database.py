from shared.models import User, Message
from typing import List

# In-memory storage for now (replace with SQLite/Postgres later)
users: List[User] = []
messages: List[Message] = []

def add_user(user: User):
    users.append(user)

def get_user(username: str):
    for u in users:
        if u.username == username:
            return u
    return None

def store_message(message: Message):
    messages.append(message)

def get_messages_for_user(username: str):
    # Return messages where receiver matches
    return [m for m in messages if m.receiver == username]

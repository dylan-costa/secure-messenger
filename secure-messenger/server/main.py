from fastapi import FastAPI
from shared.models import User, Message
from server.database import add_user, get_user, store_message, get_messages_for_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Secure Messenger Server")

# Allow requests from any origin (for local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register a new user
# -----------------------------
@app.post("/register")
def register_user(user: User):
    if get_user(user.username):
        return {"error": "Username already exists"}
    add_user(user)
    return {"status": "User registered"}

# -----------------------------
# Send encrypted message
# -----------------------------
@app.post("/send")
def send_message(message: Message):
    if not get_user(message.receiver):
        return {"error": "Receiver does not exist"}
    store_message(message)
    return {"status": "Message stored"}

# -----------------------------
# Fetch messages for a user
# -----------------------------
@app.get("/messages/{username}")
def fetch_messages(username: str):
    msgs = get_messages_for_user(username)
    return {"messages": [m.dict() for m in msgs]}

import os

from fastapi import FastAPI

from server.routes import users, messages, auth, conversations
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Secure Messenger Server")

# ALLOWED_ORIGINS is a comma-separated list (e.g. the deployed Vercel URL in
# production); defaults to the local Vite dev server.
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema is managed by Alembic now (see migrations/) — run `alembic upgrade head`
# instead of relying on create_all to build/update the database.

app.include_router(users.router)
app.include_router(messages.router)
app.include_router(auth.router)
app.include_router(conversations.router)
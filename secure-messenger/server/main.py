from fastapi import FastAPI

from server.database import engine, Base
from server.routes import users, messages, auth

app = FastAPI(title="Secure Messenger Server")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(messages.router)
app.include_router(auth.router)

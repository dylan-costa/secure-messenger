from fastapi import FastAPI

from server.database import engine, Base
from server.routes import users, messages, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Secure Messenger Server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(messages.router)
app.include_router(auth.router)

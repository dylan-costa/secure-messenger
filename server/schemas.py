from datetime import datetime, timezone
from pydantic import BaseModel


class UserKeyCreate(BaseModel):
    method: str
    public_key_json: str


class UserKeyResponse(BaseModel):
    method: str
    public_key_json: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    keys: list[UserKeyResponse] = []

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    ciphertext: str
    ciphertext_for_sender: str | None = None

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    conversation_id: int | None = None
    ciphertext: str
    ciphertext_for_sender: str | None = None
    timestamp: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str
    keys: list[UserKeyResponse] = []

    class Config:
        from_attributes = True


class ConversationKeyCreate(BaseModel):
    user_id: int
    public_key_json: str


class ConversationKeyResponse(BaseModel):
    user_id: int
    public_key_json: str

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):

    user1_id: int
    user2_id: int

    encryption_method: str

class ConversationResponse(BaseModel):

    id: int
    user1_id: int
    user2_id: int
    encryption_method: str
    domain_params_json: str | None = None
    created_at: datetime
    keys: list[ConversationKeyResponse] = []

    class Config:
        from_attributes = True

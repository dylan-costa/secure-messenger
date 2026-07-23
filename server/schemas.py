from datetime import datetime, timezone
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str

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
    created_at: datetime

    class Config:
        from_attributes = True



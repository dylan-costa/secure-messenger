from server.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  

class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user1_id = Column(
        Integer,
        nullable=False
    )

    user2_id = Column(
        Integer,
        nullable=False
    )

    encryption_method = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

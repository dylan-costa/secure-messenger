from server.database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy import DateTime
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class UserKey(Base):
    __tablename__ = "user_keys"
    __table_args__ = (UniqueConstraint("user_id", "method", name="uq_user_keys_user_id_method"),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    method = Column(String, index=True)
    public_key_json = Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    conversation_id = Column(Integer, nullable=True)
    ciphertext = Column(String)
    ciphertext_for_sender = Column(String, nullable=True)
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

    domain_params_json = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

class ConversationKey(Base):
    __tablename__ = "conversation_keys"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    public_key_json = Column(String)

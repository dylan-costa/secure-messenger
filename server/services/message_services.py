# server/services/message_service.py

from sqlalchemy.orm import Session
from server import models
from server.services import conversation_services
from datetime import datetime, timezone

def send_message(
    db: Session,
    sender_id: int,
    receiver_id: int,
    ciphertext: str,
    ciphertext_for_sender: str | None = None
):
    sender = db.query(models.User).filter(models.User.id == sender_id).first()
    if sender is None:
        raise ValueError("Sender does not exist")

    receiver = db.query(models.User).filter(models.User.id == receiver_id).first()
    if receiver is None:
        raise ValueError("Receiver does not exist")

    conversation = conversation_services.get_conversation_between_users(db, sender_id, receiver_id)

    new_message = models.Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        conversation_id=conversation.id if conversation else None,
        ciphertext=ciphertext,
        ciphertext_for_sender=ciphertext_for_sender,
        timestamp=datetime.now(timezone.utc)  # Store timestamp in UTC
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

def get_conversation(db: Session, user1_id: int, user2_id: int, limit: int = 50, offset: int = 0):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == user1_id) & (models.Message.receiver_id == user2_id)) |
        ((models.Message.sender_id == user2_id) & (models.Message.receiver_id == user1_id))
    ).order_by(models.Message.timestamp.asc()).offset(offset).limit(limit).all()

    return messages

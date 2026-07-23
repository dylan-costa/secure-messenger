from sqlalchemy.orm import Session

from server import models


def create_conversation(
    db: Session,
    user1_id: int,
    user2_id: int,
    encryption_method: str
):

    conversation = models.Conversation(
        user1_id=user1_id,
        user2_id=user2_id,
        encryption_method=encryption_method
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

def get_conversation_by_id(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_conversation_between_users(
    db: Session,
    user1_id: int,
    user2_id: int
):

    return db.query(
        models.Conversation
    ).filter(
        (
            (models.Conversation.user1_id == user1_id)
            &
            (models.Conversation.user2_id == user2_id)
        )
        |
        (
            (models.Conversation.user1_id == user2_id)
            &
            (models.Conversation.user2_id == user1_id)
        )
    ).first()
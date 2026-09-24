import json

from sqlalchemy.orm import Session

from server import models, schemas
from server.services import encryption_services


def create_conversation(
    db: Session,
    user1_id: int,
    user2_id: int,
    encryption_method: str
):

    domain_params_json = None
    generate_domain_params = encryption_services.get_domain_param_generator(encryption_method)

    if generate_domain_params is not None:
        domain_params_json = json.dumps(generate_domain_params())

    conversation = models.Conversation(
        user1_id=user1_id,
        user2_id=user2_id,
        encryption_method=encryption_method,
        domain_params_json=domain_params_json
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


def get_conversation_keys(db: Session, conversation_id: int):
    return db.query(models.ConversationKey).filter(
        models.ConversationKey.conversation_id == conversation_id
    ).all()


def add_conversation_key(db: Session, conversation_id: int, user_id: int, public_key_json: str):
    conversation = get_conversation_by_id(db, conversation_id)

    if conversation is None:
        raise ValueError("Conversation does not exist")

    if user_id not in (conversation.user1_id, conversation.user2_id):
        raise ValueError("User is not a participant in this conversation")

    existing_key = db.query(models.ConversationKey).filter(
        models.ConversationKey.conversation_id == conversation_id,
        models.ConversationKey.user_id == user_id
    ).first()

    if existing_key:
        existing_key.public_key_json = public_key_json
        db.commit()
        db.refresh(existing_key)
        return existing_key

    new_key = models.ConversationKey(
        conversation_id=conversation_id,
        user_id=user_id,
        public_key_json=public_key_json
    )

    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return new_key


def serialize_conversation(db: Session, conversation: models.Conversation) -> schemas.ConversationResponse:
    keys = get_conversation_keys(db, conversation.id)

    return schemas.ConversationResponse(
        id=conversation.id,
        user1_id=conversation.user1_id,
        user2_id=conversation.user2_id,
        encryption_method=conversation.encryption_method,
        domain_params_json=conversation.domain_params_json,
        created_at=conversation.created_at,
        keys=[
            schemas.ConversationKeyResponse(user_id=key.user_id, public_key_json=key.public_key_json)
            for key in keys
        ]
    )

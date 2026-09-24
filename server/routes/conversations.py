from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server import schemas
from server.services import conversation_services


router = APIRouter()


@router.post(
    "/conversations",
    response_model=schemas.ConversationResponse
)
def create_conversation(
    request: schemas.ConversationCreate,
    db: Session = Depends(get_db)
):

    existing_conversation = (
        conversation_services
        .get_conversation_between_users(
            db,
            request.user1_id,
            request.user2_id
        )
    )

    if existing_conversation:

        return conversation_services.serialize_conversation(db, existing_conversation)

    new_conversation = conversation_services.create_conversation(
        db=db,
        user1_id=request.user1_id,
        user2_id=request.user2_id,
        encryption_method=request.encryption_method
    )

    return conversation_services.serialize_conversation(db, new_conversation)


# Distinct from GET /conversations/{user1_id}/{user2_id} in routes/messages.py,
# which returns MESSAGE HISTORY for a pair. This returns the Conversation row
# itself (method, domain params, participant keys) so a client can check
# whether it needs to create a conversation or complete a key handshake.
@router.get("/conversations/lookup/{user1_id}/{user2_id}", response_model=schemas.ConversationResponse)
def lookup_conversation(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    conversation = conversation_services.get_conversation_between_users(db, user1_id, user2_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="No conversation between these users yet")
    return conversation_services.serialize_conversation(db, conversation)


@router.get("/conversations/{conversation_id}", response_model=schemas.ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = conversation_services.get_conversation_by_id(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation_services.serialize_conversation(db, conversation)


#submit a participant's public key for a conversation-scoped method (e.g. ECC)
@router.post("/conversations/{conversation_id}/keys", response_model=schemas.ConversationResponse)
def add_conversation_key(
    conversation_id: int,
    key: schemas.ConversationKeyCreate,
    db: Session = Depends(get_db)
):
    try:
        conversation_services.add_conversation_key(
            db=db,
            conversation_id=conversation_id,
            user_id=key.user_id,
            public_key_json=key.public_key_json
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    conversation = conversation_services.get_conversation_by_id(db, conversation_id)
    return conversation_services.serialize_conversation(db, conversation)

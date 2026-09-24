from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server import models, schemas
from server.services import message_services
from datetime import datetime, timezone


router = APIRouter()



@router.post("/messages", response_model=schemas.MessageResponse)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    try:
        new_message = message_services.send_message(
            db=db,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            ciphertext=message.ciphertext,
            ciphertext_for_sender=message.ciphertext_for_sender
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return new_message

@router.get("/messages/{user_id}", response_model=list[schemas.MessageResponse])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(
        (models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id)
    ).all()

    return messages


# Message HISTORY for a pair, distinct from GET /conversations/{conversation_id}
# and /conversations/lookup/{user1_id}/{user2_id} in routes/conversations.py,
# which return the Conversation row itself (method, domain params, keys).
@router.get("/conversations/{user1_id}/{user2_id}", response_model=list[schemas.MessageResponse])
def get_conversation(user1_id: int, user2_id: int, db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return message_services.get_conversation(db, user1_id, user2_id, limit=limit, offset=offset)



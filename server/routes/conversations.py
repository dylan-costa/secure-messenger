from fastapi import APIRouter, Depends
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

        return existing_conversation

    return conversation_services.create_conversation(
        db=db,
        user1_id=request.user1_id,
        user2_id=request.user2_id,
        encryption_method=request.encryption_method
    )
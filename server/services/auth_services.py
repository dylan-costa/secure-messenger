from sqlalchemy.orm import Session

from server import models, schemas
from server.services import password_services


def login(db: Session, request: schemas.LoginRequest):
    user = db.query(models.User).filter(
        models.User.username == request.username
    ).first()

    if user is None:
        return None

    if not password_services.verify_password(
        request.password,
        user.password_hash
    ):
        return None

    return schemas.LoginResponse(
        id=user.id,
        username=user.username
    )
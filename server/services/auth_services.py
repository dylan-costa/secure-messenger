from sqlalchemy.orm import Session 

from server import models, schemas


def login(db: Session, request: schemas.LoginRequest):
    user = db.query(models.User).filter(
        models.User.username == request.username
    ).first()

    if user is None:
        return None

    if user.password_hash != request.password:
        return None

    return schemas.LoginResponse(id=user.id, username=user.username)
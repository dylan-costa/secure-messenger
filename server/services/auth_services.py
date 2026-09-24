from sqlalchemy.orm import Session

from server import models, schemas
from server.services import password_services, user_services


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

    keys = user_services.get_user_keys(db, user.id)

    return schemas.LoginResponse(
        id=user.id,
        username=user.username,
        keys=[
            schemas.UserKeyResponse(method=key.method, public_key_json=key.public_key_json)
            for key in keys
        ]
    )

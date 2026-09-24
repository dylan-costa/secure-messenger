from sqlalchemy.orm import Session

from server import models, schemas
from server.services import password_services


#create new user

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        return None

    new_user = models.User(
        username=user.username,
        password_hash=password_services.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users


def get_user_keys(db: Session, user_id: int):
    return db.query(models.UserKey).filter(models.UserKey.user_id == user_id).all()


def add_user_key(db: Session, user_id: int, method: str, public_key_json: str):
    existing_key = db.query(models.UserKey).filter(
        models.UserKey.user_id == user_id,
        models.UserKey.method == method
    ).first()

    if existing_key:
        existing_key.public_key_json = public_key_json
        db.commit()
        db.refresh(existing_key)
        return existing_key

    new_key = models.UserKey(
        user_id=user_id,
        method=method,
        public_key_json=public_key_json
    )

    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return new_key


def serialize_user(db: Session, user: models.User) -> schemas.UserResponse:
    keys = get_user_keys(db, user.id)

    return schemas.UserResponse(
        id=user.id,
        username=user.username,
        keys=[
            schemas.UserKeyResponse(method=key.method, public_key_json=key.public_key_json)
            for key in keys
        ]
    )

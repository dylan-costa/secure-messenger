from sqlalchemy.orm import Session

from server import models, schemas


#create new user

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        return None

    new_user = models.User(
        username=user.username,
        password_hash=user.password  # We'll hash this later.
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
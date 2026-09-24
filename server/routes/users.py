from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server import models, schemas
from server.services import user_services


router = APIRouter()

#create new user
@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = user_services.create_user(db=db, user=user)
    if new_user is None:
        raise HTTPException(status_code=409, detail="Username already exists")
    return user_services.serialize_user(db, new_user)

@router.get("/users/{username}", response_model=schemas.UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = user_services.get_user(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_services.serialize_user(db, user)

@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = user_services.get_all_users(db=db)
    return [user_services.serialize_user(db, user) for user in users]

#upload a public key for one encryption method (identity-scoped methods only)
@router.post("/users/{user_id}/keys", response_model=schemas.UserResponse)
def add_user_key(user_id: int, key: schemas.UserKeyCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_services.add_user_key(
        db=db,
        user_id=user_id,
        method=key.method,
        public_key_json=key.public_key_json
    )

    return user_services.serialize_user(db, user)

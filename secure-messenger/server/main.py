from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import engine, Base, SessionLocal
from server import models, schemas

from datetime import datetime, timezone

app = FastAPI(title="Secure Messenger Server")

Base.metadata.create_all(bind=engine)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new user
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=user.username,
        password_hash=user.password  # We'll hash this later.
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{username}", response_model=schemas.UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/messages", response_model=schemas.MessageResponse)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):

    sender = db.query(models.User).filter(models.User.id == message.sender_id).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender does not exist")

    receiver = db.query(models.User).filter(models.User.id == message.receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver does not exist")

    new_message = models.Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        timestamp=datetime.now(timezone.utc)  # Store timestamp in UTC
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

@app.get("/messages/{user_id}", response_model=list[schemas.MessageResponse])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(
        (models.Message.sender_id == user_id) | (models.Message.receiver_id == user_id)
    ).all()

    return messages
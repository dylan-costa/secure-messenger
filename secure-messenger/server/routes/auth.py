from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server import models, schemas

router = APIRouter()

#authentication endpoint
@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user is None or user.password_hash != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful"}


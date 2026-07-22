from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server import models, schemas
from server.services import auth_services

router = APIRouter()

#authentication endpoint
@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = auth_services.login(db, request)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return user


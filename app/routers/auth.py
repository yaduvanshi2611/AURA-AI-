from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_token, hash_password, verify_password
from app.models import User

router = APIRouter()

class RegisterInput(BaseModel):
    email: EmailStr
    password: str

@router.post('/register', status_code=201)
def register(data: RegisterInput, db: Session = Depends(get_db)):
    if len(data.password) < 10:
        raise HTTPException(400, 'Password must be at least 10 characters')
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, 'Email is already registered')
    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    return {'id': user.id, 'email': user.email}

@router.post('/token')
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, 'Email or password is incorrect', headers={'WWW-Authenticate': 'Bearer'})
    return {'access_token': create_token(user.email), 'token_type': 'bearer', 'expires_in': 43200}

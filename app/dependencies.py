from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import fingerprint, read_token
from app.models import ApiKey, User

oauth2 = OAuth2PasswordBearer(tokenUrl='/api/auth/token', auto_error=False)

def current_user(db: Session = Depends(get_db), token: str | None = Depends(oauth2),
                 x_api_key: str | None = Header(default=None)) -> User:
    if x_api_key:
        key = db.query(ApiKey).filter(ApiKey.key_hash == fingerprint(x_api_key)).first()
        if key:
            return key.user
        raise HTTPException(401, 'Invalid API key')
    if token:
        try:
            email = read_token(token)
        except ValueError as exc:
            raise HTTPException(401, 'Invalid or expired token') from exc
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
    raise HTTPException(401, 'Sign in with a bearer token or API key')

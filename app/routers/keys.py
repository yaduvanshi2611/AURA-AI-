from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import fingerprint, new_api_key
from app.dependencies import current_user
from app.models import ApiKey, User

router = APIRouter()

class KeyInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)

@router.post('', status_code=201)
def create_key(data: KeyInput, user: User = Depends(current_user), db: Session = Depends(get_db)):
    raw = new_api_key()
    item = ApiKey(user_id=user.id, name=data.name, key_hash=fingerprint(raw), prefix=raw[:12])
    db.add(item)
    db.commit()
    return {'id': item.id, 'name': item.name, 'key': raw, 'warning': 'Copy it now; it cannot be viewed again.'}

@router.get('')
def list_keys(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [{'id': k.id, 'name': k.name, 'prefix': k.prefix, 'created_at': k.created_at}
            for k in db.query(ApiKey).filter(ApiKey.user_id == user.id).all()]

@router.delete('/{key_id}', status_code=204)
def revoke_key(key_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.query(ApiKey).filter(ApiKey.id == key_id, ApiKey.user_id == user.id).first()
    if item:
        db.delete(item)
        db.commit()

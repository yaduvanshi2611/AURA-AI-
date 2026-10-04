from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import current_user
from app.models import User

router = APIRouter()

class TrainingJobInput(BaseModel):
    dataset_uri: str = Field(min_length=1, max_length=500)
    base_model: str = Field(min_length=1, max_length=200)

@router.post('/jobs', status_code=202)
def submit_job(data: TrainingJobInput, user: User = Depends(current_user)):
    return {'status': 'scaffold_only', 'message': 'Training worker is not configured yet.',
            'requested_by': user.email, 'dataset_uri': data.dataset_uri, 'base_model': data.base_model}

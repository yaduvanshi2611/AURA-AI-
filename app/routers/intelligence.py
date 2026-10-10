from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.dependencies import current_user
from app.models import User
from app.services.aura_intelligence import (
    add_feedback, clear_memories, feedback_summary, get_memories,
    remember, scientific_plan,
)

router = APIRouter()


def _user_key(user: User) -> str:
    # Keep each account's saved data isolated.
    return str(getattr(user, "email", None) or getattr(user, "id", "unknown"))


class MemoryInput(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class FeedbackInput(BaseModel):
    rating: int = Field(ge=1, le=5)
    note: str = Field(default="", max_length=1000)


class ResearchInput(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@router.get("/status")
def status(user: User = Depends(current_user)):
    return {
        "service": "AURA Intelligence",
        "engines": {
            "reasoning_support": "available",
            "persistent_memory": "available",
            "feedback_evaluation": "available",
            "scientific_planning": "available",
            "independent_model_training": "existing prototype; not automatically upgraded",
            "autonomous_self_modification": "disabled for safety",
            "online_research": "not performed by this endpoint",
        },
    }


@router.get("/memory")
def list_memory(user: User = Depends(current_user)):
    return {"memories": get_memories(_user_key(user))}


@router.post("/memory")
def create_memory(data: MemoryInput, user: User = Depends(current_user)):
    remember(_user_key(user), data.content)
    return {"saved": True, "message": "Memory saved for this account."}


@router.delete("/memory")
def delete_memory(user: User = Depends(current_user)):
    clear_memories(_user_key(user))
    return {"deleted": True}


@router.post("/feedback")
def submit_feedback(data: FeedbackInput, user: User = Depends(current_user)):
    add_feedback(_user_key(user), data.rating, data.note)
    return {"saved": True, "summary": feedback_summary(_user_key(user))}


@router.get("/feedback/summary")
def get_feedback_summary(user: User = Depends(current_user)):
    return feedback_summary(_user_key(user))


@router.post("/research/plan")
def research_plan(data: ResearchInput, user: User = Depends(current_user)):
    return scientific_plan(data.question)

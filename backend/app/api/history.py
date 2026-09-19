from fastapi import APIRouter, HTTPException

from app.knowledge.learner_store import LearnerStore


router = APIRouter(
    prefix="/history",
    tags=["History"],
)

learner_store = LearnerStore()


@router.get("/{learner_id}")
async def get_history(
    learner_id: int,
    limit: int = 50,
):
    if learner_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="learner_id must be greater than 0.",
        )

    if limit <= 0 or limit > 200:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 200.",
        )

    return {
        "learner_id": learner_id,
        "history": learner_store.get_history(
            learner_id=learner_id,
            limit=limit,
        ),
    }
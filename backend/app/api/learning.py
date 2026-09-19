from fastapi import APIRouter, HTTPException

from app.learning.learning_service import LearningService
from app.schemas.learning import TeachRequest

router = APIRouter(
    prefix="/learning",
    tags=["Learning"],
)

learning_service = LearningService()


@router.post("/teach")
async def teach(request: TeachRequest):

    if request.learner_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="learner_id must be greater than 0.",
        )

    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="topic cannot be empty.",
        )

    try:

        result = learning_service.teach(
            learner_id=request.learner_id,
            topic=request.topic,
            use_previous_material=request.use_previous_material,
        )

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
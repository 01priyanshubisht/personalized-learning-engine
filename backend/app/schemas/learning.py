from pydantic import BaseModel, Field


class TopicRequirement(BaseModel):
    concept: str = Field(..., min_length=1)
    importance: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(..., min_length=1)


class TopicRequirements(BaseModel):
    topic: str = Field(..., min_length=1)
    requirements: list[TopicRequirement] = Field(
        default_factory=list
    )

class TeachRequest(BaseModel):
    learner_id: int = Field(..., gt=0)
    topic: str = Field(..., min_length=1)
    use_previous_material: bool = True
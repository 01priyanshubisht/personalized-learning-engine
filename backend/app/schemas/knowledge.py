from pydantic import BaseModel, Field


class ExtractedConcept(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)


class ExtractedRelationship(BaseModel):
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)
    relationship_type: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)


class ConceptExtractionResult(BaseModel):
    concepts: list[ExtractedConcept]
    relationships: list[ExtractedRelationship] = []
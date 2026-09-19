from pydantic import BaseModel, Field


class TeachingSection(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
    )

    content: str = Field(
        ...,
        min_length=1,
    )


class TeachingSource(BaseModel):
    document_id: str | None = None
    page_number: int | None = None


class TeachingResponse(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
    )

    introduction: str = Field(
        ...,
        min_length=1,
    )

    sections: list[TeachingSection] = Field(
        default_factory=list,
    )

    summary: str = Field(
        ...,
        min_length=1,
    )

    sources: list[TeachingSource] = Field(
        default_factory=list,
    )
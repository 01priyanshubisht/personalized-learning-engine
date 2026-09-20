from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    page_number: int = Field(..., ge=1)
    text: str


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    page_count: int
    status: str


class DocumentContentResponse(BaseModel):
    document_id: str
    filename: str
    pages: list[DocumentPage]

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int = Field(..., ge=1)
    chunk_index: int = Field(..., ge=0)
    text: str
    metadata: dict[str, str | int | float | bool]
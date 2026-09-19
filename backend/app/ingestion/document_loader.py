from pathlib import Path

from app.ingestion.pdf_parser import PDFParser
from app.schemas.document import DocumentPage


class DocumentLoader:
    """Route documents to the correct parser."""

    def __init__(self) -> None:
        self.pdf_parser = PDFParser()

    def load(
        self,
        file_path: Path,
        file_type: str,
    ) -> list[DocumentPage]:

        normalized_type = file_type.lower()

        if normalized_type == ".pdf":
            return self.pdf_parser.parse(file_path)

        raise ValueError(
            f"Unsupported document type: {file_type}"
        )
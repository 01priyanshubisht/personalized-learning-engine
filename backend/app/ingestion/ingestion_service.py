from pathlib import Path

from app.ingestion.chunker import TextChunker
from app.ingestion.pdf_parser import PDFParser
from app.ingestion.text_cleaner import TextCleaner
from app.schemas.document import DocumentChunk


class IngestionService:

    def __init__(self) -> None:
        self.parser = PDFParser()
        self.cleaner = TextCleaner()
        self.chunker = TextChunker(
            chunk_size=500,
            overlap=75,
        )

    def process(
        self,
        document_id: str,
        file_path: Path,
    ) -> list[DocumentChunk]:

        pages = self.parser.parse(file_path)

        cleaned_pages = []

        for page in pages:

            cleaned_text = self.cleaner.clean(
                page.text
            )

            cleaned_pages.append(
                page.model_copy(
                    update={
                        "text": cleaned_text
                    }
                )
            )

        return self.chunker.chunk_pages(
            document_id=document_id,
            pages=cleaned_pages,
        )
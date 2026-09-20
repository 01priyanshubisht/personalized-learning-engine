import re
import uuid

from app.schemas.document import DocumentChunk, DocumentPage


class TextChunker:
    """
    Split document pages into overlapping chunks.

    The first implementation uses word boundaries so that
    concepts are not arbitrarily split in the middle of words.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 75,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(
        self,
        document_id: str,
        pages: list[DocumentPage],
    ) -> list[DocumentChunk]:

        chunks: list[DocumentChunk] = []
        global_index = 0

        for page in pages:

            words = re.findall(
                r"\S+",
                page.text,
            )

            if not words:
                continue

            start = 0

            while start < len(words):

                end = min(
                    start + self.chunk_size,
                    len(words),
                )

                chunk_text = " ".join(
                    words[start:end]
                ).strip()

                if chunk_text:

                    chunks.append(
                        DocumentChunk(
                            chunk_id=str(uuid.uuid4()),
                            document_id=document_id,
                            page_number=page.page_number,
                            chunk_index=global_index,
                            text=chunk_text,
                            metadata={
                                "page": page.page_number,
                                "source_type": "pdf",
                            },
                        )
                    )

                    global_index += 1

                if end == len(words):
                    break

                start = end - self.overlap

        return chunks
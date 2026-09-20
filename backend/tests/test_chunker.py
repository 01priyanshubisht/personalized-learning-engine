from app.ingestion.chunker import TextChunker
from app.schemas.document import DocumentPage


def test_chunker_creates_chunks() -> None:

    page = DocumentPage(
        page_number=1,
        text=" ".join(
            f"word{i}"
            for i in range(1200)
        ),
    )

    chunker = TextChunker(
        chunk_size=500,
        overlap=75,
    )

    chunks = chunker.chunk_pages(
        document_id="doc-1",
        pages=[page],
    )

    assert len(chunks) > 1

    assert all(
        chunk.document_id == "doc-1"
        for chunk in chunks
    )

    assert all(
        chunk.page_number == 1
        for chunk in chunks
    )
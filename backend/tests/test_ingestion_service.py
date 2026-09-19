from pathlib import Path

import fitz

from app.ingestion.ingestion_service import IngestionService


def create_test_pdf(path: Path) -> None:
    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        (
            "HashMap provides average O(1) lookup. "
            "It stores data using key value pairs."
        ),
    )

    page = document.new_page()

    page.insert_text(
        (72, 72),
        (
            "Doubly Linked List contains nodes with "
            "previous and next pointers."
        ),
    )

    document.save(path)
    document.close()


def test_complete_ingestion_pipeline(
    tmp_path: Path,
) -> None:

    pdf_path = tmp_path / "learning.pdf"

    create_test_pdf(pdf_path)

    service = IngestionService()

    chunks = service.process(
        document_id="test-document-1",
        file_path=pdf_path,
    )

    assert len(chunks) > 0

    assert all(
        chunk.document_id == "test-document-1"
        for chunk in chunks
    )

    assert all(
        chunk.text.strip()
        for chunk in chunks
    )

    assert all(
        chunk.page_number >= 1
        for chunk in chunks
    )

    pages = {
        chunk.page_number
        for chunk in chunks
    }

    assert 1 in pages
    assert 2 in pages
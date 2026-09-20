from pathlib import Path

import pymupdf

from app.schemas.document import DocumentPage


class PDFParser:
    """Extract text from a PDF while preserving page boundaries."""

    def parse(self, file_path: Path) -> list[DocumentPage]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        pages: list[DocumentPage] = []

        try:
            with pymupdf.open(file_path) as document:
                for index, page in enumerate(document):
                    text = page.get_text("text").strip()

                    pages.append(
                        DocumentPage(
                            page_number=index + 1,
                            text=text,
                        )
                    )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to parse PDF: {file_path.name}"
            ) from exc

        return pages
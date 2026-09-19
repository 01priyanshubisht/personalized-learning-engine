from pathlib import Path

from app.ingestion.ingestion_service import IngestionService


PDF_PATH = Path("data/documents/DSA.pdf")


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    service = IngestionService()

    chunks = service.process(
        document_id="real-dsa-test",
        file_path=PDF_PATH,
    )

    print(f"\nTotal chunks: {len(chunks)}\n")

    for chunk in chunks[:5]:
        print("=" * 80)
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Page: {chunk.page_number}")
        print(f"Text:\n{chunk.text[:1000]}")


if __name__ == "__main__":
    main()
from pathlib import Path

from app.ingestion.ingestion_service import IngestionService
from app.retrieval.rag_service import RAGService


PDF_PATH = Path(
    "data/documents/DSA.pdf"
)


def main() -> None:

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    ingestion = IngestionService()

    chunks = ingestion.process(
        document_id="dsa-real-test",
        file_path=PDF_PATH,
    )

    print(
        f"Generated {len(chunks)} chunks."
    )

    rag = RAGService()

    print("Indexing chunks...")

    rag.index_chunks(chunks)

    print(
        f"Vector DB contains: "
        f"{rag.vector_store.count()} chunks"
    )

    queries = [
        "What is a hash table?",
        "How does constant time lookup work?",
        "What is a linked list?",
    ]

    for query in queries:

        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = rag.search(
            query=query,
            top_k=3,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for index, (
            document,
            metadata,
            distance,
        ) in enumerate(
            zip(
                documents,
                metadatas,
                distances,
            ),
            start=1,
        ):

            print(f"\nResult {index}")
            print(
                f"Page: "
                f"{metadata['page_number']}"
            )
            print(
                f"Distance: {distance}"
            )
            print(
                f"Text: {document[:500]}"
            )


if __name__ == "__main__":
    main()
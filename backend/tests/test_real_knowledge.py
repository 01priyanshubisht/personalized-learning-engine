from pathlib import Path

from app.knowledge.knowledge_builder import KnowledgeBuilder


PDF_PATH = Path("data/documents/DSA.pdf")


def main() -> None:

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    builder = KnowledgeBuilder()

    print("Building knowledge from DSA.pdf...")
    print()

    result = builder.build_from_document(
        document_id="dsa-real-test",
        file_path=PDF_PATH,
    )

    print()
    print("=" * 70)
    print("KNOWLEDGE BUILD COMPLETED")
    print("=" * 70)

    print(f"Chunks processed: {result['chunks']}")
    print(
        f"Concept occurrences: "
        f"{result['concept_occurrences']}"
    )
    print(
        f"Relationships extracted: "
        f"{result['relationships']}"
    )

    print()
    print("Stored concepts:")
    print("-" * 70)

    concepts = builder.knowledge_store.list_concepts()

    for concept in concepts:
        print(
            f"{concept['id']}: "
            f"{concept['name']}"
        )


if __name__ == "__main__":
    main()
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
    print("This may take some time because each chunk is sent to the LLM.")

    total = builder.build_from_document(
        document_id="dsa-real-test",
        file_path=PDF_PATH,
    )

    print()
    print(f"Concept extraction completed.")
    print(f"Total extracted concept occurrences: {total}")

    print()
    print("Stored concepts:")

    concepts = builder.knowledge_store.list_concepts()

    for concept in concepts:
        print(
            f"{concept['id']}: "
            f"{concept['name']} "
            f"→ {concept['description']}"
        )


if __name__ == "__main__":
    main()
from pathlib import Path

from app.knowledge.knowledge_builder import KnowledgeBuilder


def main() -> None:

    learner_id = 1

    document_id = "dsa-real-test"

    file_path = Path(
        "data/documents/DSA.pdf"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    builder = KnowledgeBuilder()

    concepts = builder.build(
        learner_id=learner_id,
        document_id=document_id,
        file_path=file_path,
    )

    print("\n" + "=" * 70)
    print("LEARNER KNOWLEDGE BUILD")
    print("=" * 70)

    print(
        f"\nExtracted {len(concepts)} concepts."
    )

    for concept in concepts[:20]:
        print(
            f"- {concept['concept']}"
            f" | id={concept['concept_id']}"
        )

    print(
        "\n✅ Knowledge built for learner 1."
    )


if __name__ == "__main__":
    main()
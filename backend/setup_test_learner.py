from app.knowledge.knowledge_store import KnowledgeStore
from app.knowledge.learner_store import LearnerStore


def main() -> None:

    learner_store = LearnerStore()
    knowledge_store = KnowledgeStore()

    learner_id = 1

    concepts = knowledge_store.list_concepts()

    print("\nKnowledge Base Concepts")
    print("=" * 60)

    for concept in concepts:

        concept_id = concept["id"]
        concept_name = concept["name"]

        learner_store.add_known_concept(
            learner_id=learner_id,
            concept_id=concept_id,
            evidence=(
                "Previously uploaded learner material"
            ),
        )

        print(
            f"Added: {concept_name}"
        )

    print("\n✅ Learner knowledge initialized.")


if __name__ == "__main__":
    main()
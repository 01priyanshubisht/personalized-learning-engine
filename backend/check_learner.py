from app.knowledge.learner_store import LearnerStore


def main() -> None:

    store = LearnerStore()

    learner_id = 1

    learner = store.get_learner(
        learner_id
    )

    print("\nLEARNER")
    print("=" * 60)
    print(learner)

    concepts = store.get_learner_concepts(
        learner_id
    )

    print("\nLEARNER CONCEPTS")
    print("=" * 60)

    if not concepts:
        print("NO CONCEPTS FOUND")
        return

    for concept in concepts:

        print(
            f"Concept: {concept['concept_name']}"
        )

        print(
            f"Mastery: {concept['mastery']}"
        )

        print(
            f"Status: {concept['status']}"
        )

        print(
            f"Evidence: {concept['evidence']}"
        )

        print("-" * 60)


if __name__ == "__main__":
    main()
    
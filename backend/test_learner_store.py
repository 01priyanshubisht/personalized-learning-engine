from app.knowledge.learner_store import LearnerStore
from app.knowledge.knowledge_store import KnowledgeStore


DATABASE_PATH = "data/test_learner.db"


def main() -> None:
    knowledge_store = KnowledgeStore(DATABASE_PATH)
    learner_store = LearnerStore(DATABASE_PATH)

    print("Creating concepts...")

    hash_map_id = knowledge_store.add_concept(
        name="HashMap",
        description="A data structure providing key-value storage.",
    )

    linked_list_id = knowledge_store.add_concept(
        name="Doubly Linked List",
        description="A linked list with next and previous pointers.",
    )

    cache_id = knowledge_store.add_concept(
        name="Cache",
        description="A storage mechanism for fast access to frequently used data.",
    )

    print("Concept IDs:")
    print("HashMap:", hash_map_id)
    print("Doubly Linked List:", linked_list_id)
    print("Cache:", cache_id)

    print("\nCreating learner...")

    learner_id = learner_store.create_learner(
        "Priyanshu"
    )

    print("Learner ID:", learner_id)

    print("\nAdding learner knowledge...")

    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=hash_map_id,
        mastery=0.90,
        status="learned",
        evidence="DSA.pdf page 42",
    )

    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=linked_list_id,
        mastery=0.80,
        status="learned",
        evidence="DSA.pdf page 57",
    )

    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=cache_id,
        mastery=0.60,
        status="familiar",
        evidence="System Design.pdf page 18",
    )

    print("\nLearner knowledge:")

    concepts = learner_store.get_learner_concepts(
        learner_id
    )

    for concept in concepts:
        print(
            f"{concept['concept_name']} | "
            f"mastery={concept['mastery']} | "
            f"status={concept['status']} | "
            f"evidence={concept['evidence']}"
        )


if __name__ == "__main__":
    main()
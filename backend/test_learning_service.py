from app.knowledge.knowledge_store import KnowledgeStore
from app.knowledge.learner_store import LearnerStore
from app.learning.learning_service import LearningService


def main() -> None:

    # ---------------------------------------------------------
    # Use existing knowledge database
    # ---------------------------------------------------------
    knowledge_store = KnowledgeStore()
    learner_store = LearnerStore()

    # ---------------------------------------------------------
    # Find existing concepts
    # ---------------------------------------------------------
    concepts = learner_store.get_learner_concepts

    import sqlite3

    with sqlite3.connect(
        learner_store.database_path
    ) as connection:

        rows = connection.execute(
            """
            SELECT id, name
            FROM concepts
            WHERE name IN (
                'HashMap',
                'Doubly Linked List',
                'Cache'
            )
            """
        ).fetchall()

    concept_ids = {
        name: concept_id
        for concept_id, name in rows
    }

    # ---------------------------------------------------------
    # Make sure required concepts exist
    # ---------------------------------------------------------
    required = [
        "HashMap",
        "Doubly Linked List",
        "Cache",
    ]

    for concept in required:
        if concept not in concept_ids:
            concept_ids[concept] = (
                knowledge_store.add_concept(
                    name=concept,
                    description=f"Test concept: {concept}",
                )
            )

    # ---------------------------------------------------------
    # Create learner
    # ---------------------------------------------------------
    learner_id = learner_store.create_learner(
        "End To End Test Learner"
    )

    # ---------------------------------------------------------
    # Add learner knowledge
    # ---------------------------------------------------------
    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=concept_ids["HashMap"],
        mastery=0.9,
        status="learned",
        evidence="DSA.pdf page 42",
    )

    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=concept_ids[
            "Doubly Linked List"
        ],
        mastery=0.8,
        status="learned",
        evidence="DSA.pdf page 57",
    )

    learner_store.set_concept_mastery(
        learner_id=learner_id,
        concept_id=concept_ids["Cache"],
        mastery=0.6,
        status="familiar",
        evidence="System Design.pdf page 18",
    )

    # ---------------------------------------------------------
    # Run complete learning pipeline
    # ---------------------------------------------------------
    service = LearningService()

    result = service.teach(
        learner_id=learner_id,
        topic="LRU Cache",
    )

    # ---------------------------------------------------------
    # Display requirements
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("REQUIREMENTS")
    print("=" * 60)

    for requirement in result["requirements"].requirements:
        print(
            f"- {requirement.concept}"
            f" | importance={requirement.importance}"
        )

    # ---------------------------------------------------------
    # Display gaps
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("KNOWLEDGE GAPS")
    print("=" * 60)

    for gap in result["gaps"]:
        print(
            f"- {gap.concept}"
            f" | mastery={gap.mastery}"
            f" | status={gap.status}"
            f" | evidence={gap.evidence}"
        )

    # ---------------------------------------------------------
    # Display plan
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("LEARNING PLAN")
    print("=" * 60)

    for index, step in enumerate(
        result["learning_plan"],
        start=1,
    ):
        print(
            f"{index}. {step.concept}"
            f" | action={step.action}"
        )

    # ---------------------------------------------------------
    # Display lesson
    # ---------------------------------------------------------
    lesson = result["lesson"]

    print("\n" + "=" * 60)
    print("PERSONALIZED LESSON")
    print("=" * 60)

    print("\nINTRODUCTION:")
    print(lesson.introduction)

    for section in lesson.sections:
        print(f"\n### {section.title}")
        print(section.content)

    print("\nSUMMARY:")
    print(lesson.summary)

    print("\n✅ END-TO-END LEARNING PIPELINE PASSED!")


if __name__ == "__main__":
    main()
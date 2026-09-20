import sqlite3
import tempfile
from pathlib import Path

from app.knowledge.knowledge_store import KnowledgeStore
from app.knowledge.learner_store import LearnerStore
from app.learning.gap_detector import GapDetector
from app.schemas.learning import TopicRequirement, TopicRequirements


def main() -> None:
    # ---------------------------------------------------------
    # 1. Create a temporary database for testing
    # ---------------------------------------------------------
    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = Path(temp_dir) / "test_knowledge.db"

        # -----------------------------------------------------
        # 2. Create knowledge and learner stores
        # -----------------------------------------------------
        knowledge_store = KnowledgeStore(
            database_path=str(database_path)
        )

        learner_store = LearnerStore(
            database_path=str(database_path)
        )

        # -----------------------------------------------------
        # 3. Create concepts in the knowledge database
        # -----------------------------------------------------
        concept_ids = {}

        concepts = [
            (
                "HashMap",
                "A data structure that stores key-value pairs "
                "and provides efficient lookup.",
            ),
            (
                "Doubly Linked List",
                "A linked list whose nodes contain "
                "next and previous pointers.",
            ),
            (
                "Cache",
                "A storage mechanism used to store "
                "frequently accessed data.",
            ),
        ]

        for name, description in concepts:
            concept_ids[name] = knowledge_store.add_concept(
                name=name,
                description=description,
            )

        print("Created concepts:")
        for name, concept_id in concept_ids.items():
            print(f"- {name} | id={concept_id}")

        # -----------------------------------------------------
        # 4. Create a learner
        # -----------------------------------------------------
        learner_id = learner_store.create_learner(
            "Test Learner"
        )

        print(f"\nCreated learner: {learner_id}")

        # -----------------------------------------------------
        # 5. Add learner's existing knowledge
        # -----------------------------------------------------
        learner_store.set_concept_mastery(
            learner_id=learner_id,
            concept_id=concept_ids["HashMap"],
            mastery=0.9,
            status="learned",
            evidence="DSA.pdf page 42",
        )

        learner_store.set_concept_mastery(
            learner_id=learner_id,
            concept_id=concept_ids["Doubly Linked List"],
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

        # -----------------------------------------------------
        # 6. Simulate Requirement Agent output
        # -----------------------------------------------------
        requirements = TopicRequirements(
            topic="LRU Cache",
            requirements=[
                TopicRequirement(
                    concept="HashMap",
                    importance=0.9,
                    reason=(
                        "Provides fast key-based lookup "
                        "for cached items."
                    ),
                ),
                TopicRequirement(
                    concept="Doubly Linked List",
                    importance=0.8,
                    reason=(
                        "Maintains the order of recently "
                        "used items efficiently."
                    ),
                ),
                TopicRequirement(
                    concept="Cache",
                    importance=0.6,
                    reason=(
                        "Stores the items that are being "
                        "cached."
                    ),
                ),
                TopicRequirement(
                    concept="Eviction Policy",
                    importance=0.7,
                    reason=(
                        "Determines which item should be "
                        "removed when the cache is full."
                    ),
                ),
                TopicRequirement(
                    concept="O(1) Lookup",
                    importance=0.4,
                    reason=(
                        "Required for efficient cache "
                        "operations."
                    ),
                ),
            ],
        )

        # -----------------------------------------------------
        # 7. Run Gap Detector
        # -----------------------------------------------------
        detector = GapDetector(
            learner_store=learner_store
        )

        results = detector.detect(
            learner_id=learner_id,
            topic_requirements=requirements,
        )

        # -----------------------------------------------------
        # 8. Display results
        # -----------------------------------------------------
        print(
            f"\nLearning gap for: "
            f"{requirements.topic}\n"
        )

        for result in results:
            print(
                f"- {result.concept}"
                f" | mastery={result.mastery}"
                f" | status={result.status}"
                f" | importance={result.importance}"
                f" | evidence={result.evidence}"
            )

        # -----------------------------------------------------
        # 9. Verify expected behavior
        # -----------------------------------------------------
        expected_status = {
            "HashMap": "known",
            "Doubly Linked List": "known",
            "Cache": "weak",
            "Eviction Policy": "unknown",
            "O(1) Lookup": "unknown",
        }

        actual_status = {
            result.concept: result.status
            for result in results
        }

        assert actual_status == expected_status, (
            f"Unexpected statuses:\n"
            f"Expected: {expected_status}\n"
            f"Actual: {actual_status}"
        )

        print("\n✅ Gap Detector test passed!")


if __name__ == "__main__":
    main()
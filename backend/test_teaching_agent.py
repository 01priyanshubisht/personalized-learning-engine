from app.learning.learning_plan import (
    LearningPlanBuilder,
)
from app.learning.gap_detector import ConceptGap
from app.learning.teaching_agent import TeachingAgent


def main() -> None:

    gaps = [
        ConceptGap(
            concept="HashMap",
            importance=0.9,
            reason="Provides fast key-based lookup.",
            mastery=0.9,
            status="known",
            evidence="DSA.pdf page 42",
        ),
        ConceptGap(
            concept="Doubly Linked List",
            importance=0.8,
            reason="Maintains usage order efficiently.",
            mastery=0.8,
            status="known",
            evidence="DSA.pdf page 57",
        ),
        ConceptGap(
            concept="Cache",
            importance=0.6,
            reason="Stores cached elements.",
            mastery=0.6,
            status="weak",
            evidence="System Design.pdf page 18",
        ),
        ConceptGap(
            concept="Eviction Policy",
            importance=0.7,
            reason="Determines which item should be removed.",
            mastery=0.0,
            status="unknown",
            evidence=None,
        ),
        ConceptGap(
            concept="O(1) Lookup",
            importance=0.4,
            reason="Required for efficient cache operations.",
            mastery=0.0,
            status="unknown",
            evidence=None,
        ),
    ]

    # Build personalized learning plan.
    plan_builder = LearningPlanBuilder()

    plan = plan_builder.build(
        topic="LRU Cache",
        gaps=gaps,
    )

    print("\nLearning Plan:\n")

    for index, step in enumerate(plan, start=1):
        print(
            f"{index}. {step.concept}"
            f" | action={step.action}"
            f" | mastery={step.mastery}"
        )

    # ---------------------------------------------------------
    # Run Teaching Agent
    # ---------------------------------------------------------
    agent = TeachingAgent()

    print("\nGenerating personalized lesson...\n")

    result = agent.teach(
        topic="LRU Cache",
        learning_plan=plan,
    )

    print("=" * 60)
    print(f"TOPIC: {result.topic}")
    print("=" * 60)

    print("\nINTRODUCTION:")
    print(result.introduction)

    print("\nSECTIONS:")

    for section in result.sections:
        print(f"\n### {section.title}")
        print(section.content)

    print("\nSUMMARY:")
    print(result.summary)

    print("\n✅ Teaching Agent test passed!")


if __name__ == "__main__":
    main()
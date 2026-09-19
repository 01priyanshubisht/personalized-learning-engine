from app.learning.learning_service import LearningService


def main() -> None:

    service = LearningService()

    result = service.teach(
        learner_id=1,
        topic="LRU Cache",
        use_previous_material=True,
    )

    print("\n" + "=" * 70)
    print("PERSONALIZED LEARNING FLOW")
    print("=" * 70)

    print("\nREQUIRED CONCEPTS")
    print("-" * 70)

    for gap in result["gaps"]:

        source = (
            "RAG"
            if gap.known
            else "LLM"
        )

        print(
            f"{gap.concept:25}"
            f"| known={gap.known}"
            f"| source={source}"
        )

    print("\nLEARNING PLAN")
    print("-" * 70)

    for step in result["learning_plan"]:

        print(
            f"{step.concept:25}"
            f"| action={step.action}"
        )

    print("\nRAG MATERIAL")
    print("-" * 70)

    for material in result[
        "retrieved_material"
    ]:

        print(
            f"Concept: "
            f"{material['retrieved_for']}"
        )

        print(
            f"Document: "
            f"{material['document_id']}"
        )

        print(
            f"Page: "
            f"{material['page_number']}"
        )

        print(
            f"Text: "
            f"{material['text'][:200]}"
        )

        print("-" * 70)


if __name__ == "__main__":
    main()
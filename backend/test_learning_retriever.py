from app.retrieval.learning_retriever import (
    LearningRetriever,
)


def main() -> None:

    retriever = LearningRetriever()

    query = "LRU Cache HashMap doubly linked list"

    print(f"\nSearching learner material for:")
    print(query)

    results = retriever.retrieve(
        query=query,
        top_k=5,
    )

    print(
        f"\nRetrieved {len(results)} chunks:\n"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        print("=" * 60)

        print(f"Result: {index}")

        print(
            f"Document ID: "
            f"{result['document_id']}"
        )

        print(
            f"Page: "
            f"{result['page_number']}"
        )

        print(
            f"Distance: "
            f"{result['distance']}"
        )

        print("\nText:")
        print(result["text"][:500])

    if results:
        print(
            "\n✅ Learning retrieval test passed!"
        )
    else:
        print(
            "\n⚠️ No results found."
        )


if __name__ == "__main__":
    main()
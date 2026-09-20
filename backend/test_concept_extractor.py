from app.knowledge.concept_extractor import ConceptExtractor


def main() -> None:
    extractor = ConceptExtractor()

    text = """
    A linked list is a linear data structure consisting of nodes.
    Each node contains data and a pointer to the next node.

    A doubly linked list is a variation of a linked list.
    Each node contains pointers to both the next and previous nodes.
    This allows traversal in both directions.
    """

    result = extractor.extract(text)

    print("\nCONCEPTS")
    print("=" * 60)

    for concept in result.concepts:
        print(f"Name: {concept.name}")
        print(f"Description: {concept.description}")
        print(f"Confidence: {concept.confidence}")
        print()

    print("\nRELATIONSHIPS")
    print("=" * 60)

    for relationship in result.relationships:
        print(
            f"{relationship.source} "
            f"--[{relationship.relationship_type}]--> "
            f"{relationship.target}"
        )
        print(f"Confidence: {relationship.confidence}")
        print()


if __name__ == "__main__":
    main()
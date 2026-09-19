from app.knowledge.knowledge_store import KnowledgeStore


def main() -> None:
    store = KnowledgeStore()

    hashmap_id = store.add_concept(
        name="HashMap",
        description="A data structure providing key-value based lookup.",
    )

    linked_list_id = store.add_concept(
        name="Linked List",
        description="A linear data structure consisting of linked nodes.",
    )

    lru_id = store.add_concept(
        name="LRU Cache",
        description="A cache that evicts the least recently used item.",
    )

    store.add_source(
        concept_id=hashmap_id,
        document_id="dsa-real-test",
        page_number=42,
    )

    store.add_source(
        concept_id=linked_list_id,
        document_id="dsa-real-test",
        page_number=80,
    )

    store.add_relationship(
        source_concept_id=lru_id,
        target_concept_id=hashmap_id,
        relationship_type="requires",
    )

    store.add_relationship(
        source_concept_id=lru_id,
        target_concept_id=linked_list_id,
        relationship_type="requires",
    )

    print("Concepts:")

    for concept in store.list_concepts():
        print(concept)


if __name__ == "__main__":
    main()
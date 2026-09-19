from app.retrieval.rag_service import RAGService


class LearningRetriever:
    """
    Retrieves learning material belonging only to a specific learner.
    """

    def __init__(self, rag_service: RAGService | None = None) -> None:
        self.rag_service = rag_service or RAGService()

    def retrieve(
        self,
        learner_id: int,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        results = self.rag_service.search(
            query=query,
            learner_id=learner_id,
            top_k=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved = []

        for index, document in enumerate(documents):
            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            retrieved.append(
                {
                    "text": document,
                    "document_id": metadata.get("document_id"),
                    "page_number": metadata.get("page_number"),
                    "chunk_index": metadata.get("chunk_index"),
                    "distance": distance,
                    "retrieved_for": query,
                    "learner_id": learner_id,
                }
            )

        return retrieved

    def retrieve_for_concepts(
        self,
        learner_id: int,
        concepts: list[str],
        top_k_per_concept: int = 2,
    ) -> list[dict]:

        retrieved = []

        for concept in concepts:
            results = self.retrieve(
                learner_id=learner_id,
                query=concept,
                top_k=top_k_per_concept,
            )

            retrieved.extend(results)

        return retrieved
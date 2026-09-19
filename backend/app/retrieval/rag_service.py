
from typing import Any

from app.embeddings.embedder import (
    EmbeddingService,
    get_embedding_service,
)
from app.retrieval.vector_store import VectorStore
from app.schemas.document import DocumentChunk


class RAGService:
    """
    Coordinates embedding generation and learner-aware
    vector retrieval.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:

        self.embedding_service = (
            embedding_service
            or get_embedding_service()
        )

        self.vector_store = (
            vector_store
            or VectorStore()
        )

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
        learner_id: int,
    ) -> None:

        if not chunks:
            return

        embeddings = (
            self.embedding_service.embed_documents(
                [chunk.text for chunk in chunks]
            )
        )

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            learner_id=learner_id,
        )

    def search(
        self,
        query: str,
        learner_id: int,
        top_k: int = 5,
    ) -> dict[str, Any]:

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            learner_id=learner_id,
            top_k=top_k,
        )


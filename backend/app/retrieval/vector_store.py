
from pathlib import Path
from typing import Any

import chromadb

from app.schemas.document import DocumentChunk


class VectorStore:
    """
    Learner-aware Chroma vector store.

    Every chunk is associated with the learner who uploaded it.
    Retrieval is always filtered by learner_id so that one
    learner cannot retrieve another learner's material.
    """

    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "learning_chunks",
    ) -> None:

        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
        learner_id: int,
    ) -> None:

        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match "
                "number of embeddings."
            )

        self.collection.upsert(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],

            embeddings=embeddings,

            documents=[
                chunk.text
                for chunk in chunks
            ],

            metadatas=[
                {
                    "learner_id": learner_id,
                    "document_id": chunk.document_id,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        learner_id: int,
        top_k: int = 5,
    ) -> dict[str, Any]:

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        return self.collection.query(
            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

            where={
                "learner_id": learner_id
            },

            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self) -> int:
        return self.collection.count()

